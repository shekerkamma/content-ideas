#!/usr/bin/env python3
"""Validate a template profile and its selected slide archetypes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


SKILL_DIR = Path(__file__).resolve().parents[1]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_template_profile.py <template-profile.json>", file=sys.stderr)
        return 2

    profile_path = Path(sys.argv[1])
    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        schema = json.loads(
            (SKILL_DIR / "references/template-profile-schema.json").read_text(encoding="utf-8")
        )
        catalog = json.loads(
            (SKILL_DIR / "references/slide-archetypes.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{profile_path}: {exc}", file=sys.stderr)
        return 1

    problems = []
    for error in Draft202012Validator(schema).iter_errors(profile):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        problems.append(f"{profile_path}:{location}: {error.message}")

    known = {entry["id"] for entry in catalog["archetypes"]}
    for archetype in profile.get("archetypes", []):
        if archetype not in known:
            problems.append(f"{profile_path}:archetypes: unknown archetype {archetype}")

    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"valid: {profile_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
