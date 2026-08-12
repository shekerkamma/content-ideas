#!/usr/bin/env python3
"""Deterministic integrity checks for every skill in this repo.

This is the `verified_by` command behind the worked-example contract. It is
plain stdlib with no model in it: exit code 1 is exit code 1, and the builder
cannot argue with it.

Each --rule maps to exactly one contract criterion so the auditor can run a
single criterion in isolation.

Repo-wide skill integrity gate. Promoted out of
runs/2026-08-11-graph-engineering-contract-loop/worked-example/ once the rules
stopped changing; that run folder holds the record of how each rule was
derived, and every rule here carries the revision note explaining what it got
wrong first.

Usage:
    python3 scripts/check_skills.py                 # every rule
    python3 scripts/check_skills.py --rule name     # one rule
    python3 scripts/check_skills.py --json          # machine-readable

Enforced by tests/test_skill_integrity.py.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "skills"
MIRROR = REPO / "plugins" / "content-ideas" / "skills"

MIRRORED = (
    "content-ideas", "pipeline-runner", "second-brain",
    "plaid", "karpathy-guidelines", "graph-engineering",
    # meta-loop was named in CLAUDE.md's porting contract but omitted here, so
    # its mirror was policed by nothing at all. Keep this tuple and that
    # contract in sync; a skill documented as mirrored but absent from this
    # list is worse than one that was never claimed, because the docs promise a
    # guarantee no rule provides.
    "meta-loop",
)

MIN_DESC = 40

# Routing is fuzzy, so the duplicate check is too. Exact equality was defeated
# by appending a single period.
SIMILARITY_FLOOR = 0.95


def skill_dirs() -> list[Path]:
    return sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())


def frontmatter(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return None
    parts = text.split("\n---\n", 1)
    return parts[0] if len(parts) == 2 else None


def field(fm: str, key: str) -> str | None:
    m = re.search(rf"(?m)^{re.escape(key)}:\s*(.*)$", fm)
    return m.group(1).strip() if m else None


# --- rules ------------------------------------------------------------------

def rule_frontmatter() -> list[str]:
    return [f"{s.name}: SKILL.md has no closed YAML frontmatter block"
            for s in skill_dirs() if frontmatter(s / "SKILL.md") is None]


def rule_name() -> list[str]:
    fails = []
    for s in skill_dirs():
        fm = frontmatter(s / "SKILL.md")
        if fm is None:
            continue
        declared = (field(fm, "name") or "").strip("'\"")
        if not declared:
            fails.append(f"{s.name}: no `name:` in frontmatter")
        elif declared != s.name:
            fails.append(f"{s.name}: declares name {declared!r} — invocation "
                         f"name and directory disagree")
    return fails


def resolve_desc(fm: str) -> str | None:
    """Return the full description text, folded blocks included.

    Revision note: this originally returned early on `>` and `|`, so a folded
    description was never measured. Converting 36 skills to folded blocks would
    have made the criterion pass without checking anything — a criterion that
    stopped measuring rather than one that got satisfied.
    """
    lines = fm.splitlines()
    idx = next((i for i, l in enumerate(lines) if re.match(r"^description:", l)), None)
    if idx is None:
        return None
    first = lines[idx].split(":", 1)[1].strip()
    if not first.startswith((">", "|")):
        return first
    body = []
    for line in lines[idx + 1:]:
        if line.strip() and not line.startswith((" ", "\t")):
            break
        body.append(line.strip())
    return " ".join(x for x in body if x)


def rule_desc() -> list[str]:
    """Routing information must be reachable — not necessarily in the description.

    Revision note, and the important one. This began as "every description is
    at least 40 characters," which reported 14 failures and, chased upstream,
    looked like 36. It was wrong. gstack's catalog-trim (T4) deliberately
    trims the Claude-host description to its first sentence and moves routing
    prose into a `## When to invoke` body section plus a
    `proactive-suggestions.json` registry, so routing is available on demand
    "without paying the always-loaded cost."

    A short description is that optimization working. The criterion had
    encoded "longer is better" as if it were a fact, and enforcing it
    re-inflated the always-loaded catalog this repo is actively trying to
    shrink. What actually matters is that routing exists somewhere a reader
    or router can reach, so that is what is checked.
    """
    fails = []
    for s in skill_dirs():
        path = s / "SKILL.md"
        fm = frontmatter(path)
        if fm is None:
            continue
        desc = resolve_desc(fm)
        if not desc:
            fails.append(f"{s.name}: no `description:` in frontmatter")
            continue
        if len(desc) >= MIN_DESC:
            continue
        body = path.read_text(encoding="utf-8", errors="replace")
        has_body_routing = re.search(r"(?mi)^#{1,6}\s+when to invoke", body)
        has_triggers = re.search(r"(?m)^\s*triggers:\s*$", fm)
        if not (has_body_routing or has_triggers):
            fails.append(
                f"{s.name}: description is {len(desc)} chars and there is no "
                f"`## When to invoke` section or `triggers:` — routing is "
                f"unreachable: {desc!r}"
            )
    return fails


def rule_mirror() -> list[str]:
    """Packaged mirrors are byte-identical to canonical AND tracked in git.

    Revision note (second): the tracked-in-git half only ever asked about the
    *canonical* side. `skills/<name>/` tracked meant pass, whatever state the
    mirror was in — so `plugins/content-ideas/skills/meta-loop/` sat on disk
    with zero tracked files and the rule stayed green. Byte-identity is
    compared on disk, which means a mirror existing only in one developer's
    working directory satisfied every check while shipping nothing. The mirror
    is the copy the plugin actually installs, so it is the side that most needs
    to be in history. Both sides are now checked independently.
    """
    import subprocess
    tracked = subprocess.run(["git", "ls-files", "--", "skills/", "plugins/"],
                             cwd=str(REPO), capture_output=True, text=True, check=False)
    tracked_set = set(tracked.stdout.splitlines()) if tracked.returncode == 0 else None

    mirror_prefix = MIRROR.relative_to(REPO).as_posix()

    fails = []
    for name in MIRRORED:
        canonical, packaged = SKILLS / name, MIRROR / name
        # --rule bytecode asks git what ships; this one did not, so it passed on
        # a skill absent from history. Both rules now agree on what "ships" means.
        if tracked_set is not None:
            for label, prefix in (
                ("canonical", f"skills/{name}/"),
                ("packaged mirror", f"{mirror_prefix}/{name}/"),
            ):
                if not any(p.startswith(prefix) for p in tracked_set):
                    fails.append(
                        f"{name}: {label} ({prefix}) is untracked in git — it cannot "
                        f"ship and the mirror guarantee is unverifiable in history"
                    )
        if not packaged.is_dir():
            fails.append(f"{name}: no packaged mirror at {packaged}")
            continue
        def files(root: Path) -> set:
            return {p.relative_to(root) for p in root.rglob("*")
                    if p.is_file() and "__pycache__" not in p.parts}
        c_files, p_files = files(canonical), files(packaged)
        for missing in sorted(c_files - p_files):
            fails.append(f"{name}: {missing} missing from mirror")
        for extra in sorted(p_files - c_files):
            fails.append(f"{name}: {extra} only in mirror")
        for rel in sorted(c_files & p_files):
            if (canonical / rel).read_bytes() != (packaged / rel).read_bytes():
                fails.append(f"{name}: {rel} differs between canonical and mirror")
    return fails


def rule_bytecode() -> list[str]:
    """Committed bytecode only.

    Revision note: the first version of this rule walked the filesystem and
    reported 46 failures. All 46 were gitignored local build artifacts — the
    criterion was measuring the developer's working directory, not the repo.
    Portability is a property of what ships, so ask git what is tracked.
    """
    import subprocess
    res = subprocess.run(
        ["git", "ls-files", "--", "skills/", "plugins/"],
        cwd=str(REPO), capture_output=True, text=True, check=False,
    )
    if res.returncode != 0:
        return ["git ls-files failed — cannot verify tracked bytecode"]
    return [
        f"{line}: generated bytecode is committed and is not portable"
        for line in res.stdout.splitlines()
        if "__pycache__" in line or line.endswith(".pyc")
    ]


def rule_dupes() -> list[str]:
    """Two directories declaring one invocation name — last one loaded wins."""
    import collections
    declared = collections.defaultdict(list)
    for s in skill_dirs():
        fm = frontmatter(s / "SKILL.md")
        if fm is None:
            continue
        name = (field(fm, "name") or "").strip("'\"")
        if name:
            declared[name].append(s.name)
    return [
        f"{name!r} is declared by {len(dirs)} directories: {dirs} — "
        f"whichever loads last silently wins"
        for name, dirs in sorted(declared.items()) if len(dirs) > 1
    ]


TREES = {
    "skills": "skills",
    ".claude": ".claude/skills",
    ".agents": ".agents/skills",
    ".github": ".github/skills",
    "plugins": "plugins/content-ideas/skills",
    "portable": "portable-skills",
}
VARIANTS_FILE = Path(__file__).resolve().parent / "cross-tree-variants.json"


def _all_skill_files() -> list[tuple[Path, str, str]]:
    """(path, tree_label, key) for every SKILL.md in every in-repo tree."""
    out = []
    for label, rel in TREES.items():
        root = REPO / rel
        if not root.is_dir():
            continue
        for f in root.rglob("SKILL.md"):
            out.append((f, label, str(f.parent.relative_to(root))))
    return out


def rule_crosstree() -> list[str]:
    """Copies of one skill across repo trees must not silently diverge in body.

    Replaces the retired criterion 7 ("shadows nothing in the repo tree"), which
    was unsatisfiable by construction: this repo deliberately keeps one skill
    tree per harness, so every ported skill "shadows" itself by design and no
    amount of renaming could make that criterion pass.

    What is actually dangerous is a copy that has drifted — the harness loads
    one version while the maintained content lives in another. Frontmatter is
    excluded because per-harness serialization is intentional; only body drift
    counts. Known-deliberate variants live in cross-tree-variants.json with
    evidence, so the list stays reviewable instead of invisible.
    """
    import collections

    registered = {}
    if VARIANTS_FILE.is_file():
        registered = {k: v for k, v in
                      json.loads(VARIANTS_FILE.read_text(encoding="utf-8")).items()
                      if not k.startswith("_")}

    def body(path: Path) -> str:
        text = path.read_text(encoding="utf-8", errors="replace")
        part = text.split("\n---\n", 1)
        return re.sub(r"\s+", " ", (part[1] if len(part) > 1 else text)).strip()

    idx = collections.defaultdict(dict)
    for label, rel in TREES.items():
        root = REPO / rel
        if not root.is_dir():
            continue
        # rglob, not iterdir: nested skills are real and invocable. iterdir saw
        # 315 of skills/'s 364 SKILL.md files and 15 of portable-skills/'s 57,
        # so 42 cross-tree pairs were compared zero times — one of which had a
        # missing safety gate.
        for f in root.rglob("SKILL.md"):
            key = str(f.parent.relative_to(root))
            idx[key][label] = f

    fails = []
    for name, trees in sorted(idx.items()):
        if len(trees) < 2:
            continue
        bodies = {lab: body(f) for lab, f in trees.items()}
        if len(set(bodies.values())) == 1:
            continue
        entry = registered.get(name)
        if entry is not None:
            # The criterion says "registered ... with evidence". Checking only
            # that the key exists enforces the registration and not the
            # evidence, so an entry of `{}` would waive anything. Require both
            # fields, and only waive the trees the entry actually names.
            missing = [k for k in ("reason", "evidence")
                       if not str(entry.get(k, "")).strip()]
            if missing:
                fails.append(f"{name}: registry entry is missing {missing} — "
                             f"registration without evidence is a blanket waiver")
                continue
            listed = set(entry.get("trees") or [])
            unlisted = sorted(set(trees) - listed) if listed else []
            if not unlisted:
                continue
            fails.append(f"{name}: registered for {sorted(listed)} but also "
                         f"differs in {unlisted}, which the entry does not cover")
            continue
        sizes = ", ".join(f"{lab}={len(b)}" for lab, b in sorted(bodies.items()))
        fails.append(
            f"{name}: body differs across {sorted(trees)} ({sizes}) and is not "
            f"registered in cross-tree-variants.json — a harness may be loading "
            f"a copy that is not the maintained one"
        )
    return fails


def rule_routing_dupes() -> list[str]:
    """Two skills that route identically, whatever their names say.

    Revision note, and the one that matters most. `rule_dupes` hashes the
    `name:` field only. Three pairs were "fixed" by renaming, and the audit
    that followed found the collision had simply moved: each pair still had a
    byte-identical `description:` and `triggers:`, which is what natural-language
    routing actually selects on. The rename satisfied the check without
    changing the behavior the check existed to protect.

    A criterion is only worth what it measures. This one measures the routing
    surface rather than the label sitting above it.

    Three defects the audit found in the first version of this rule, all fixed
    here:

    - Exact-string equality was defeated by appending one period. Routing is
      fuzzy, so the comparison is too: near-duplicates above SIMILARITY_FLOOR
      are reported.
    - The `triggers:` parser split on the first `triggers:` substring and then
      matched every `- ` line to the end of the frontmatter, swallowing
      unrelated `matcher:` and `id:` entries. It mis-parsed 10 of the 71
      skills that declare triggers, and a genuine byte-identical trigger
      collision passed. It now parses by YAML indentation.
    - It ignored `## When to invoke`, which criterion 4 and the first
      amendment both establish as the authoritative routing surface after
      gstack's catalog trim. Both duplicate pairs collided there while this
      rule reported PASS.
    """
    import collections
    import difflib

    def trigger_block(fm: str) -> list[str]:
        lines = fm.splitlines()
        i = next((j for j, l in enumerate(lines)
                  if re.match(r"^(\s*)triggers:\s*$", l)), None)
        if i is None:
            return []
        indent = len(lines[i]) - len(lines[i].lstrip())
        out = []
        for line in lines[i + 1:]:
            if not line.strip():
                continue
            cur = len(line) - len(line.lstrip())
            m = re.match(r"^\s*-\s+(.*\S)\s*$", line)
            # YAML permits a sequence to sit at the SAME indent as its key, and
            # gstack's skills use that form:
            #     triggers:
            #     - be careful
            # Requiring cur > indent made this return [] for every such skill,
            # so the triggers half of the rule silently checked nothing. Only a
            # non-item at or above the key's level ends the block.
            if m and cur >= indent:
                out.append(m.group(1).lower())
                continue
            if cur <= indent:
                break
        return out

    def when_section(text: str) -> str:
        m = re.search(r"(?m)^#{1,6}\s+when to invoke.*$", text, re.I)
        if not m:
            return ""
        rest = text[m.end():]
        nxt = re.search(r"(?m)^#{1,6}\s", rest)
        return re.sub(r"\s+", " ", (rest[:nxt.start()] if nxt else rest)).strip().lower()

    descs: list[tuple[str, str]] = []
    whens: list[tuple[str, str]] = []
    by_trig = collections.defaultdict(list)

    # Every tree a harness routes from, not just skills/. Claude Code routes
    # from .claude/skills/ and .agents/skills/; scanning only skills/ covered
    # 315 of the repo's 443 SKILL.md files. Nested skills are included because
    # CLAUDE.md documents many of them as directly invocable.
    for path, label, key in _all_skill_files():
        s = type("S", (), {"name": f"{label}:{key}"})()
        fm = frontmatter(path)
        if fm is None:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        desc = re.sub(r"\s+", " ", (resolve_desc(fm) or "")).strip().lower()
        if desc:
            descs.append((s.name, desc))
        w = when_section(text)
        if w:
            whens.append((s.name, w))
        trig = trigger_block(fm)
        if trig:
            by_trig[tuple(trig)].append(s.name)

    fails = []

    def near_dupes(pairs: list[tuple[str, str]], label: str) -> None:
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                (na, a), (nb, b) = pairs[i], pairs[j]
                if na.split(":", 1)[-1] == nb.split(":", 1)[-1]:
                    continue  # one skill in two trees — rule_crosstree owns that
                if abs(len(a) - len(b)) / max(len(a), len(b), 1) > 0.25:
                    continue
                ratio = difflib.SequenceMatcher(None, a, b).ratio()
                if ratio >= SIMILARITY_FLOOR:
                    how = "identical" if a == b else f"{ratio:.0%} similar"
                    fails.append(
                        f"['{na}', '{nb}']: {how} `{label}` — natural-language "
                        f"routing cannot reliably tell them apart: {a[:60]!r}"
                    )

    near_dupes(descs, "description:")
    near_dupes(whens, "## When to invoke")
    for trig, dirs in sorted(by_trig.items()):
        distinct = {d.split(":", 1)[-1] for d in dirs}
        if len(distinct) > 1:
            fails.append(f"{sorted(dirs)}: identical `triggers:` {list(trig)[:3]}")
    return fails


RULES = {
    "frontmatter": rule_frontmatter,
    "name": rule_name,
    "desc": rule_desc,
    "dupes": rule_dupes,
    "routing": rule_routing_dupes,
    "crosstree": rule_crosstree,
    "mirror": rule_mirror,
    "bytecode": rule_bytecode,
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Skill integrity checks.")
    ap.add_argument("--rule", choices=sorted(RULES), help="Run one rule only")
    ap.add_argument("--json", action="store_true", help="Machine-readable output")
    ap.add_argument("--limit", type=int, default=25, help="Max failures to print")
    args = ap.parse_args(argv)

    selected = [args.rule] if args.rule else sorted(RULES)
    results = {name: RULES[name]() for name in selected}
    fails = [f for name in selected for f in results[name]]

    if args.json:
        print(json.dumps({
            "skills_checked": len(skill_dirs()),
            "rules": selected,
            "failures": {k: v for k, v in results.items()},
            "total_failures": len(fails),
            "verdict": "FAIL" if fails else "PASS",
        }, indent=2))
        return 1 if fails else 0

    print(f"skills checked: {len(skill_dirs())}")
    for name in selected:
        n = len(results[name])
        print(f"  {name:<12} {'FAIL' if n else 'PASS'} ({n})")
    print()
    print(f"{'FAIL' if fails else 'PASS'} ({len(fails)})")
    for f in fails[:args.limit]:
        print("  -", f)
    if len(fails) > args.limit:
        print(f"  … {len(fails) - args.limit} more")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
