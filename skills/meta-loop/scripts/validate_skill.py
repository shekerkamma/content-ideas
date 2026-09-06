#!/usr/bin/env python3
"""Validate Meta LOOP structure and compile its adapters."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["SKILL.md", "agents/openai.yaml", "scripts/dispatch_codex_workers.py",
            "scripts/run_aggregator.py", "references/worker-brief.md",
            "references/verification-ledger.md", "references/security-boundaries.md",
            "references/attribution.md", "references/trigger-cases.json",
            "references/video-scenario-evals.json"]


def main() -> int:
    failures = []
    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty: {relative}")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.+)$", skill, re.DOTALL)
    if not match or "name: meta-loop" not in match.group(1):
        failures.append("invalid SKILL.md frontmatter")
    for term in ("Claude Code Opus", "Codex CLI", "PASS", "FIX", "ESCALATE", "ledger"):
        if term.lower() not in skill.lower():
            failures.append(f"SKILL.md missing invariant: {term}")
    try:
        cases = json.loads((ROOT / "references/trigger-cases.json").read_text(encoding="utf-8"))["cases"]
        if sum(case["should_trigger"] is True for case in cases) < 3 or sum(case["should_trigger"] is False for case in cases) < 3:
            failures.append("trigger cases need at least 3 positive and 3 negative cases")
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        failures.append(f"invalid trigger cases: {exc}")
    try:
        data = json.loads((ROOT / "references/video-scenario-evals.json").read_text(encoding="utf-8"))
        scenarios = data["cases"]
        required = {"id", "timestamp", "evidence", "prompt", "route", "expected"}
        allowed_evidence = {"visible_text", "transcript_reconstruction", "visual_only"}
        if len(scenarios) < 20:
            failures.append("video scenario evals need at least 20 cases")
        if len({case["id"] for case in scenarios}) != len(scenarios):
            failures.append("video scenario eval IDs must be unique")
        for case in scenarios:
            missing = required - case.keys()
            if missing:
                failures.append(f"video scenario {case.get('id', '<unknown>')} missing: {sorted(missing)}")
            elif case["evidence"] not in allowed_evidence:
                failures.append(f"video scenario {case['id']} has invalid evidence type")
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        failures.append(f"invalid video scenario evals: {exc}")
    for script in ("dispatch_codex_workers.py", "run_aggregator.py", "validate_skill.py"):
        try:
            source = (ROOT / "scripts" / script).read_text(encoding="utf-8")
            compile(source, str(ROOT / "scripts" / script), "exec")
        except (OSError, SyntaxError) as exc:
            failures.append(f"{script}: {exc}")
    if failures:
        print(json.dumps({"ok": False, "failures": failures}, indent=2))
        return 1
    print(json.dumps({"ok": True, "root": str(ROOT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
