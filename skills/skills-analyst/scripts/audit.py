#!/usr/bin/env python3
"""skills-analyst audit engine (stdlib only).

Scans every skill root across hosts, mines real usage from Claude Code
transcripts and Codex history, and emits a markdown audit report:

  - inventory matrix (which roots carry each skill)
  - diverged duplicates (same name, different SKILL.md content)
  - bloated SKILL.md files (>500 lines -> extract references)
  - dirs missing SKILL.md
  - usage counts (Skill tool invocations + slash commands typed)
  - never-used skills (candidates for merge/archive -- NEVER auto-deleted)

Usage:
  python3 audit.py [--out report.md] [--days N]
"""
import argparse
import collections
import glob
import hashlib
import json
import os
import re
import sys
from datetime import datetime

DEFAULT_ROOTS = {
    "claude-global": "~/.claude/skills",
    "codex-global": "~/.codex/skills",
    "agents-global": "~/.agents/skills",
    "gemini-global": "~/.gemini/skills",
    "repo": "~/content-ideas/skills",
    "repo-.claude": "~/content-ideas/.claude/skills",
    "repo-.agents": "~/content-ideas/.agents/skills",
    "plugin": "~/content-ideas/plugins/content-ideas/skills",
}
# Asset/support dirs that legitimately have no SKILL.md
NON_SKILL_DIRS = {"_shared", "scripts", "templates", "imported", ".system",
                  "compound-engineering", "standup"}
BLOAT_LINES = 500


def scan_roots(roots):
    info = collections.defaultdict(dict)  # name -> root -> dict
    for root, path in roots.items():
        p = os.path.expanduser(path)
        if not os.path.isdir(p):
            continue
        for name in sorted(os.listdir(p)):
            d = os.path.join(p, name)
            if not os.path.isdir(d):
                continue
            sm = os.path.join(d, "SKILL.md")
            entry = {"symlink": os.path.islink(d), "hash": None, "lines": 0,
                     "mtime": None}
            if os.path.isfile(sm):
                data = open(sm, "rb").read()
                entry["hash"] = hashlib.md5(data).hexdigest()[:8]
                entry["lines"] = data.count(b"\n")
                entry["mtime"] = datetime.fromtimestamp(
                    os.path.getmtime(sm)).strftime("%Y-%m-%d")
            info[name][root] = entry
    return info


def mine_claude_usage():
    skills = collections.Counter()
    cmds = collections.Counter()
    cmd_re = re.compile(r"<command-name>/?([\w:-]+)</command-name>")
    for f in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        try:
            with open(f, errors="replace") as fh:
                for line in fh:
                    if '"Skill"' in line:
                        try:
                            obj = json.loads(line)
                        except ValueError:
                            continue
                        content = obj.get("message", {}).get("content")
                        if isinstance(content, list):
                            for c in content:
                                if (isinstance(c, dict)
                                        and c.get("type") == "tool_use"
                                        and c.get("name") == "Skill"):
                                    s = c.get("input", {}).get("skill")
                                    if s:
                                        skills[s] += 1
                    if "<command-name>" in line:
                        for m in cmd_re.findall(line):
                            cmds[m] += 1
        except OSError:
            continue
    return skills, cmds


def mine_codex_usage():
    cmds = collections.Counter()
    p = os.path.expanduser("~/.codex/history.jsonl")
    if not os.path.isfile(p):
        return cmds
    with open(p, errors="replace") as fh:
        for line in fh:
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            m = re.match(r"^/([\w-]+)", (obj.get("text") or "").strip())
            if m:
                cmds[m.group(1)] += 1
    return cmds


def base_name(s):
    return s.split(":")[-1]


def build_report(info, skills, cmds, codex_cmds):
    used = collections.Counter()
    for s, c in skills.items():
        used[base_name(s)] += c
    for s, c in cmds.items():
        used[base_name(s)] += c
    for s, c in codex_cmds.items():
        used[base_name(s)] += c
    for noise in ("clear", "model", "compact", "login", "resume", "exit", "mnt"):
        used.pop(noise, None)

    lines = ["# Skills Audit Report", "",
             f"Generated: {datetime.now():%Y-%m-%d %H:%M}", ""]
    lines.append(f"- Distinct skill names across roots: **{len(info)}**")
    multi = {k: v for k, v in info.items() if len(v) > 1}
    diverged = {k: v for k, v in multi.items()
                if len({e['hash'] for e in v.values() if e['hash']}) > 1}
    lines.append(f"- Present in >1 root: **{len(multi)}**")
    lines.append(f"- Diverged duplicates: **{len(diverged)}**")
    ever_used = {k for k in used if k in info}
    lines.append(f"- Skills with recorded usage: **{len(ever_used)}**")
    lines.append("")

    lines.append("## Usage (Skill invocations + slash commands, all hosts)")
    lines.append("")
    for s, c in used.most_common(50):
        mark = " (not found in any root)" if s not in info else ""
        lines.append(f"- {c:3d}  `{s}`{mark}")
    lines.append("")

    lines.append("## Diverged duplicates (FIX: pick canonical, resync)")
    lines.append("")
    for k in sorted(diverged):
        parts = ", ".join(
            f"{r}={e['hash']}({e['lines']}L, {e['mtime']})"
            for r, e in sorted(diverged[k].items()) if e["hash"])
        flag = " **<- USED**" if k in ever_used else ""
        lines.append(f"- `{k}`{flag}: {parts}")
    lines.append("")

    lines.append(f"## Bloated SKILL.md (> {BLOAT_LINES} lines -> extract references)")
    lines.append("")
    big = sorted(((max(e['lines'] for e in v.values()), k)
                  for k, v in info.items()), reverse=True)
    for l, k in big:
        if l <= BLOAT_LINES:
            break
        flag = " **<- USED**" if k in ever_used else ""
        lines.append(f"- {l:5d}L  `{k}`{flag}")
    lines.append("")

    lines.append("## Dirs without SKILL.md")
    lines.append("")
    for k, v in sorted(info.items()):
        if k in NON_SKILL_DIRS:
            continue
        for r, e in v.items():
            if e["hash"] is None:
                lines.append(f"- `{k}` @ {r}")
    lines.append("")

    lines.append("## Never used (merge/archive candidates -- ASK BEFORE DELETING)")
    lines.append("")
    never = sorted(k for k in info if k not in ever_used
                   and k not in NON_SKILL_DIRS)
    lines.append(f"{len(never)} skills have no recorded usage. Note: transcript "
                 "retention is limited and inline-read sub-skills do not appear "
                 "as Skill invocations -- treat as a signal, not proof.")
    lines.append("")
    lines.append(", ".join(f"`{k}`" for k in never))
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="write report to file")
    args = ap.parse_args()
    info = scan_roots(DEFAULT_ROOTS)
    skills, cmds = mine_claude_usage()
    codex_cmds = mine_codex_usage()
    report = build_report(info, skills, cmds, codex_cmds)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(report)
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(report)


if __name__ == "__main__":
    main()
