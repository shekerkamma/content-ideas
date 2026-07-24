#!/usr/bin/env python3
"""Report hosted presentation capability availability and portable fallbacks."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = Path(__file__).resolve().parents[1] / "references" / "skill-registry.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--available", action="append", default=[], help="capability exposed by the current host")
    parser.add_argument("--require", action="append", default=[], help="capability that must be present; missing required capabilities fail")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    env_available = os.environ.get("PPTX_EXTERNAL_CAPABILITIES", "").split(",")
    available = {value.strip() for value in [*env_available, *args.available] if value.strip()}
    required = set(args.require)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    known = {entry["name"] for entry in registry["external_capabilities"]}
    unknown = required - known
    failures = [f"unknown required capability: {name}" for name in sorted(unknown)]

    for entry in registry["external_capabilities"]:
        name = entry["name"]
        if name in available:
            print(f"READY {name}: {entry['discovery']}")
        else:
            print(
                f"FALLBACK {name}: {entry['fallback_skill']} -> "
                f"{entry['fallback_output']}"
            )
            if name in required:
                failures.append(f"missing required capability: {name}")

    if failures:
        print("\n".join(f"ERROR {failure}" for failure in failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
