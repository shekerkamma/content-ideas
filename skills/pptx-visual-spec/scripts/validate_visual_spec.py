#!/usr/bin/env python3
"""Validate a deck visual specification against the shared contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_visual_spec.py <visual-spec.json>", file=sys.stderr)
        return 2

    spec_path = Path(sys.argv[1])
    schema_path = Path(__file__).resolve().parents[1] / "references" / "visual-spec-schema.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(spec), key=lambda err: list(err.path))
    if errors:
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            print(f"{location}: {error.message}", file=sys.stderr)
        return 1

    print(f"valid: {spec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
