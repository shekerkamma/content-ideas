#!/usr/bin/env python3
"""Moved. The rules stabilized, so this checker was promoted to the repo root.

    python3 scripts/check_skills.py [--rule NAME]

This run folder keeps the record of how each rule was derived and what it got
wrong first; the tool itself now lives at scripts/check_skills.py and is
enforced by tests/test_skill_integrity.py.
"""
import pathlib, runpy, sys

target = pathlib.Path(__file__).resolve().parents[3] / "scripts" / "check_skills.py"
if not target.is_file():
    sys.exit(f"promoted checker not found at {target}")
sys.argv[0] = str(target)
runpy.run_path(str(target), run_name="__main__")
