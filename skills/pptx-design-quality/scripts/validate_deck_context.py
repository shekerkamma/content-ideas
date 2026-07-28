#!/usr/bin/env python3
"""Validate deck-brief.md and deck-design.json before PPTX construction."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


REQUIRED_HEADINGS = (
    "## Audience",
    "## Decision",
    "## Narrative promise",
    "## Voice and tone",
    "## Anti-references",
    "## Evidence and editability",
    "## Success criteria",
)


def _section_body(markdown: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)",
        markdown,
    )
    if match is None:
        return ""
    without_comments = re.sub(r"<!--.*?-->", "", match.group(1), flags=re.DOTALL)
    return without_comments.strip()


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: validate_deck_context.py <deck-brief.md> <deck-design.json>",
            file=sys.stderr,
        )
        return 2

    brief_path = Path(sys.argv[1])
    design_path = Path(sys.argv[2])
    problems: list[str] = []

    if not brief_path.is_file():
        problems.append(f"missing brief: {brief_path}")
    else:
        brief = brief_path.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            if heading not in brief:
                problems.append(f"{brief_path}: missing heading {heading}")
            elif not _section_body(brief, heading):
                problems.append(f"{brief_path}: empty section {heading}")

    if not design_path.is_file():
        problems.append(f"missing design contract: {design_path}")
    else:
        try:
            design = json.loads(design_path.read_text(encoding="utf-8"))
            schema_path = (
                Path(__file__).resolve().parents[1]
                / "references"
                / "deck-design-schema.json"
            )
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            errors = sorted(
                Draft202012Validator(schema).iter_errors(design),
                key=lambda error: list(error.path),
            )
            for error in errors:
                location = ".".join(str(part) for part in error.absolute_path) or "<root>"
                problems.append(f"{design_path}:{location}: {error.message}")
            if not errors:
                ignored = set(design["qa"]["ignore_rules"])
                waivers = design["qa"]["waivers"]
                for rule_id in sorted(ignored):
                    reason = waivers.get(rule_id)
                    if not isinstance(reason, str) or not reason.strip():
                        problems.append(
                            f"{design_path}:qa.waivers: missing reason for ignored rule {rule_id}"
                        )
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"{design_path}: {exc}")

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1

    print(f"valid: {brief_path} + {design_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
