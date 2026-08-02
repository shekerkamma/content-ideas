#!/usr/bin/env python3
"""Validate the image-generation routing contract and repo consumer wiring."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]
CONTRACT_PATH = SKILL_ROOT / "contracts" / "image-generation-routing-contract.json"
SCHEMA_PATH = SKILL_ROOT / "contracts" / "image-generation-routing-contract.schema.json"


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(contract), key=lambda error: list(error.path))
    for error in errors:
        location = ".".join(str(item) for item in error.path) or "<root>"
        print(f"contract error at {location}: {error.message}", file=sys.stderr)

    consumer_errors = []
    for relative in contract["consumer_contract"]["required_repo_consumers"]:
        path = REPO_ROOT / relative
        if not path.is_file():
            consumer_errors.append(f"missing required consumer: {relative}")
        elif "image-generation-router" not in path.read_text(encoding="utf-8"):
            consumer_errors.append(f"consumer does not reference image-generation-router: {relative}")

    pptx_schema = json.loads(
        (REPO_ROOT / "skills/pptx-visual-spec/references/visual-spec-schema.json").read_text(encoding="utf-8")
    )
    execution_paths = pptx_schema["$defs"]["visual"]["properties"]["execution"]["properties"]["path"]["enum"]
    if "cliproxyapi-gemini" not in execution_paths:
        consumer_errors.append("PPTX visual-spec schema does not allow cliproxyapi-gemini")

    for error in consumer_errors:
        print(error, file=sys.stderr)
    if errors or consumer_errors:
        return 1
    print("image-generation routing contract: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
