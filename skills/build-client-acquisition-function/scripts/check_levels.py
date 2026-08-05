#!/usr/bin/env python3
"""Blocking check for framework Rule 1: do not skip levels.

SKILL.md has always said "do not skip levels". Prose did not stop it happening: a run
scaffolded prompts/ and chains/ as empty directories, built Level 3's six context files,
and reported Level 3 while Levels 1 and 2 did not exist. This makes that failure loud.

A level counts as BUILT only when its artifact exists AND carries real content — a file
that is still the untouched template (placeholder <angle-bracket> headings, empty code
fences) does not count.

Exit 1 if status.json claims a level above the highest contiguous built level.

Usage: check_levels.py <run-dir>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# level -> (label, glob for its artifact)
ARTIFACTS = {
    1: ("The Saved Prompt", "prompts/*.md"),
    2: ("The Chain", "chains/*.md"),
    3: ("The Brain", "context/0*.md"),
    4: ("The Skill", "skills/*/SKILL.md"),
    5: ("The Deliverable Machine", "deliverables/template*.md"),
    6: ("The Connection", "connections/*.md"),
    7: ("The Agent", "agents/*.md"),
    8: ("The Team", "handoffs/*/*.md"),
    9: ("Always On", "schedules/*.md"),
}

PLACEHOLDER = re.compile(r"<[a-z][a-z0-9 \-/]*>", re.I)


def is_real(path: Path) -> bool:
    """True when the file has been filled in rather than left as the scaffold."""
    text = path.read_text(encoding="utf-8", errors="replace")
    body = text.strip()
    if len(body) < 200:
        return False
    # An untouched template is mostly placeholders and empty fences.
    if len(PLACEHOLDER.findall(text)) >= 3:
        return False
    if re.search(r"```text\s*\n\s*```", text):
        return False
    return True


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    run = Path(sys.argv[1]).resolve()
    status_path = run / "control" / "status.json"
    if not status_path.exists():
        print(f"FAIL: no control/status.json under {run}")
        return 1
    claimed = int(json.loads(status_path.read_text()).get("current_level", 0))

    built: dict[int, bool] = {}
    for level, (label, pattern) in ARTIFACTS.items():
        files = [p for p in run.glob(pattern) if p.is_file()]
        built[level] = bool(files) and any(is_real(p) for p in files)
        mark = "built" if built[level] else ("EMPTY" if not files else "template only")
        print(f"  L{level} {label:<24} {mark:<14} ({len(files)} file(s))")

    highest = 0
    for level in sorted(ARTIFACTS):
        if built[level]:
            highest = level
        else:
            break

    print(f"\n  claimed current_level: {claimed}")
    print(f"  highest contiguous built level: {highest}")

    if claimed > highest:
        gaps = [f"L{n}" for n in range(1, claimed + 1) if not built.get(n)]
        print(
            f"\nFAIL: status.json claims Level {claimed} but {', '.join(gaps)} "
            f"{'is' if len(gaps) == 1 else 'are'} not built.\n"
            "Rule 1 — do not skip levels. A later level built on a missing one is a faster mess.\n"
            "Either build the missing level or lower current_level to "
            f"{highest}."
        )
        return 1

    print("\nOK: no level is claimed above what is actually built.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
