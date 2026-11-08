#!/usr/bin/env python3
"""Behaviour checks for a patched detox skill built by apply_patches.py.

Usage: python3 selftest.py <patched detox dir>     Exit 0 all pass, 1 a check failed.

Builds throwaway homes in a temp folder and runs the skill's own scripts against them:
Windows paths (simulated), app-folder detection, WSL terminal mode with symlinked repo
skills, the no-grep transcript scan, and the page build. Nothing outside the temp folder
is read or written.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import types
from pathlib import Path, PureWindowsPath

SK = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
FAILS = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{info}]" if info and not ok else ""))
    if not ok:
        FAILS.append(name)


def load(home, tag):
    os.environ["HOME"] = str(home)
    spec = importlib.util.spec_from_file_location(f"gather_{tag}", SK / "scripts/gather_local.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gather(home, out, cwd, **env):
    r = subprocess.run([sys.executable, "-I", str(SK / "scripts/gather_local.py"), str(out)], cwd=cwd,
                       env=dict(os.environ, HOME=str(home), **env), capture_output=True, text=True,
                       encoding="utf-8", timeout=120)
    return r, (json.loads(r.stdout) if r.returncode == 0 else None)


def skill_md(path, name):
    path.mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Does a thing, naïvely ✓\n---\nbody\n",
                                   encoding="utf-8")


def windows_checks(w):
    m = load(w / "unused-home", "win")
    m.HOME = PureWindowsPath(r"C:\Users\u")
    m.HOME_S = m.norm(m.HOME)
    m.ENABLED = {"content-ideas"}
    cases = {
        r"C:\Users\u\.claude\skills\foo\SKILL.md": "global",
        r"C:\Users\u\.claude\plugins\cache\ci\content-ideas\1.0\skills\bar\SKILL.md": "plugin",
        r"C:\Users\u\.claude\plugins\synced\org\x\skills\s\SKILL.md": "plugin",
        r"C:\Users\u\.claude\plugins\marketplaces\m\p\skills\q\SKILL.md": "plugin-stored",
        r"C:\Users\u\Documents\proj\.claude\skills\baz\SKILL.md": "folder",
        r"C:\Users\u\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\a\b\skills\d\SKILL.md": "desktop-harness",
        r"C:\Users\u\Documents\notes\SKILL.md": "loose",
    }
    wrong = {p: m.location_of(PureWindowsPath(p)) for p, want in cases.items()
             if m.location_of(PureWindowsPath(p)) != want}
    check("windows: every skill path classified", not wrong, str(wrong))

    real_os = m.os
    for label, rel in (("classic", "Roaming/Claude"),
                       ("store", "Local/Packages/Claude_x/LocalCache/Roaming/Claude")):
        base = w / f"appdata-{label}"
        (base / "Roaming").mkdir(parents=True)
        (base / "Local").mkdir(parents=True)
        (base / rel / "claude-code-sessions").mkdir(parents=True)
        os.environ["APPDATA"], os.environ["LOCALAPPDATA"] = str(base / "Roaming"), str(base / "Local")
        m.os = types.SimpleNamespace(name="nt", environ=os.environ)
        try:
            got = m.claude_app_dir()
        finally:
            m.os = real_os
        check(f"windows: finds the Claude app folder ({label} install)", got == base / rel, str(got))
    os.environ.pop("APPDATA")
    os.environ.pop("LOCALAPPDATA")


def app_mode_checks(w):
    home = w / "app-home"
    sess = home / ".config/Claude/claude-code-sessions/u/o"
    sess.mkdir(parents=True)
    now = int(time.time() * 1000)
    for i, title in enumerate(["Café ✓ test chat", "Résumé deck", "old"]):
        (sess / f"local_{i}.json").write_text(json.dumps(
            {"sessionId": f"s{i}", "title": title, "cwd": "/w/proj", "createdAt": now - 86400000,
             "lastActivityAt": now - 3600000}, ensure_ascii=False), encoding="utf-8")
    skill_md(home / ".claude/skills/foo", "foo")
    skill_md(home / ".claude/plugins/cache/mkt/content-ideas/1.0/skills/bar", "bar")
    (home / ".claude/settings.json").write_text(json.dumps({"enabledPlugins": {"content-ideas@mkt": True}}))
    r, o = gather(home, w / "app-raw", cwd=home)
    check("app: gather exits 0", r.returncode == 0, r.stderr[-300:])
    check("app: mode app, 3 sessions, non-ASCII titles kept",
          o and o["mode"] == "app" and o["code_sessions"] == 3 and "Café ✓ test chat" in
          [s["title"] for s in json.loads((w / "app-raw/sessions.json").read_text(encoding="utf-8"))["code_sessions"]],
          str(o))
    locs = {s["name"]: s["location"] for s in
            json.loads((w / "app-raw/skills.json").read_text(encoding="utf-8"))["skills"]}
    check("app: skill locations", locs == {"foo": "global", "bar": "plugin"}, str(locs))


def wsl_checks(w):
    home = w / "wsl-home"
    repo = home / "content-ideas"
    (repo / ".git").mkdir(parents=True)
    for rel in ("skills/alpha", "skills/beta", "plugins/content-ideas/skills/alpha"):
        skill_md(repo / rel, rel.split("/")[-1])
    (home / ".claude/skills").mkdir(parents=True)
    for s in ("alpha", "beta"):
        (home / ".claude/skills" / s).symlink_to(repo / "skills" / s)
    (home / ".claude/skills/loop").symlink_to(home / ".claude/skills")
    skill_md(home / ".claude/skills/real", "real")
    pd = home / ".claude/projects/-home-u-content-ideas"
    pd.mkdir(parents=True)
    lines = [
        {"type": "user", "cwd": str(repo), "timestamp": "2026-11-07T10:00:00.000Z", "isMeta": True,
         "message": {"role": "user", "content": "<command-name>/clear</command-name>"}},
        {"type": "user", "cwd": str(repo), "timestamp": "2026-11-07T10:00:01.000Z",
         "message": {"role": "user", "content": [{"type": "text", "text": "fix the scraper tests ✓\nmore"}]}},
        {"type": "assistant", "cwd": str(repo), "timestamp": "2026-11-07T10:01:00.000Z",
         "message": {"role": "assistant", "model": "claude-opus-5-5", "content": [
             {"type": "tool_use", "name": "Skill", "input": {"skill": "alpha"}},
             {"type": "tool_use", "name": "mcp__Exa__web_search_exa", "input": {}}]}},
    ]
    (pd / "abc.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False, separators=(",", ":"))
                                            for x in lines) + "\n", encoding="utf-8")
    (pd / "def.jsonl").write_text(json.dumps({"type": "summary", "summary": "Old research chat"}) + "\n")
    os.utime(pd / "def.jsonl", (time.time() - 60 * 86400,) * 2)

    r, o = gather(home, w / "wsl-raw", cwd=repo)
    check("wsl: gather exits 0 (symlink loop does not hang)", r.returncode == 0, r.stderr[-300:])
    check("wsl: terminal mode reported and explained", o and o["mode"] == "terminal" and "terminal mode" in r.stderr)
    sess = {s["id"]: s for s in json.loads((w / "wsl-raw/sessions.json").read_text(encoding="utf-8"))["code_sessions"]}
    check("wsl: CLI sessions read", set(sess) == {"abc", "def"}, str(list(sess)))
    check("wsl: title skips command lines, summary used, model read",
          sess.get("abc", {}).get("title") == "fix the scraper tests ✓"
          and sess.get("def", {}).get("title") == "Old research chat"
          and sess.get("abc", {}).get("model") == "claude-opus-5-5", str(sess))
    check("wsl: idle age from file time", (sess.get("def", {}).get("last_active_days_ago") or 0) >= 59)
    sk = json.loads((w / "wsl-raw/skills.json").read_text(encoding="utf-8"))["skills"]
    by = {(s["name"], s["location"]): s for s in sk}
    alpha = by.get(("alpha", "global"), {})
    check("wsl: symlinked repo skills found as global", ("beta", "global") in by and bool(alpha), str(list(by)))
    check("wsl: symlink target and repo ownership recorded",
          alpha.get("symlink_to") == repo.as_posix() + "/skills/alpha" and alpha.get("in_git_repo") == repo.as_posix(),
          str(alpha))
    check("wsl: plain global skill is not repo-owned", by.get(("real", "global"), {}).get("in_git_repo") is None)
    check("wsl: each SKILL.md counted once", len(sk) == len({os.path.realpath(s["path"]) for s in sk}))
    check("wsl: skill use counted from CLI transcript", alpha.get("uses") == 1)

    m = load(home, "nogrep")
    m.shutil.which = lambda name: None
    os.environ["CLAUDE_CODE_EXECPATH"] = "/nonexistent"
    usage, mcp = m.scan_logs()
    check("wsl: transcript scan works without rg or grep",
          usage.get("alpha", {}).get("uses") == 1 and mcp and mcp[0]["server"] == "Exa", f"{usage} {mcp}")


def page_checks(w):
    run = w / "run"
    (run / "findings").mkdir(parents=True)
    row = lambda rid, path: {"id": rid, "cells": ["Café skill ✓", "global"], "mode": "approve", "tick": True,
                             "folder": "", "tokens": 40, "tokens_est": False, "default": 0,
                             "actions": [{"label": "Move to backup", "apply": {"kind": "move_skill", "path": path}}]}
    (run / "findings/skills.json").write_text(json.dumps({"part": "skills", "title": "Skills", "summary": "s",
        "stats": [], "tables": [
            {"id": "t1", "title": "Unused", "columns": ["Skill", "Where"], "rows": [row("t1-a", r"C:\Users\u\.claude\skills\foo")]},
            {"id": "t2", "title": "Heavy", "columns": ["Skill", "Where"], "rows": [row("t2-a", "C:/Users/u/.claude/skills/foo/SKILL.md")]}]},
        ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(SK / "scripts/build_page.py"), str(run)],
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    check("page: builds", r.returncode == 0, r.stderr[-300:])
    check("page: one skill via \\ and / counts once; pre-ticks forced off",
          "approve all saves: 40 tokens" in r.stdout and "pre-ticked, forcing false" in r.stdout, r.stdout)
    html = (run / "page/index.html").read_text(encoding="utf-8")
    check("page: findings inlined", "Café skill ✓" in html and "__FINDINGS__" not in html)


def main():
    if SK is None or not (SK / "scripts/gather_local.py").is_file():
        print(__doc__)
        return 2
    saved = dict(os.environ)
    with tempfile.TemporaryDirectory(prefix="detox-selftest-") as tmp:
        w = Path(tmp)
        try:
            windows_checks(w)
            app_mode_checks(w)
            wsl_checks(w)
            page_checks(w)
        finally:
            os.environ.clear()
            os.environ.update(saved)
    print("ALL PASS" if not FAILS else f"{len(FAILS)} FAILED: {FAILS}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
