#!/usr/bin/env python3
"""Audit governed slide/PPTX skills for the shared contract pin and stale policy."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = Path(__file__).resolve().parents[1] / "references" / "skill-registry.json"
STALE = re.compile(
    r"all (?:image )?routes (?:are )?blocked|every image-model route is blocked|"
    r"blocked as of 2026-07-17|codex rate-limited",
    re.IGNORECASE,
)


def resolve(entry: dict[str, object]) -> Path | None:
    if entry["ownership"] == "external":
        root = os.environ.get(str(entry["root_env"]))
        if not root:
            return None
        return Path(root).expanduser() / str(entry["source_relative"]) / "SKILL.md"
    return ROOT / str(entry["source"]) / "SKILL.md"


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    failures: list[str] = []
    checked = 0
    skipped = 0
    for entry in registry["skills"]:
        path = resolve(entry)
        if path is None:
            skipped += 1
            continue
        if not path.exists():
            failures.append(f"missing [{entry['tier']}]: {path}")
            continue
        checked += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        if "pptx-visual-spec" not in text:
            failures.append(f"un-pinned [{entry['tier']}]: {path}")
        match = STALE.search(text)
        if match:
            failures.append(f"stale route status [{entry['tier']}]: {path}: {match.group(0)}")

    if failures:
        print("\n".join(failures))
        return 1
    suffix = f"; optional external skipped: {skipped}" if skipped else ""
    print(f"governed skills: {checked}; pins: complete; stale route status: none{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
