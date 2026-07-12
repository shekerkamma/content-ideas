#!/usr/bin/env python3
"""Validate the Hyundai vault-derived OKF bundle."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESERVED = {"README.md", "AGENTS.md", "CLAUDE.md", "index.md", "log.md"}
EXPECTED_TYPES = {
    "use-cases": "use_case",
    "architecture": "architecture",
    "technologies": "technology",
}


def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    data: dict[str, object] = {}
    key = ""
    for raw in lines[1:end]:
        line = raw.rstrip()
        if line.startswith("- ") and key:
            current = data.setdefault(key, [])
            if isinstance(current, list):
                current.append(line[2:].strip().strip("'\""))
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if value == "":
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()]
        else:
            data[key] = value.strip("'\"")
    return data, "\n".join(lines[end + 1 :])


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    counts = {kind: 0 for kind in EXPECTED_TYPES.values()}

    for required in ["README.md", "AGENTS.md", "CLAUDE.md", "index.md", "log.md", "okf-cli.py"]:
        if not (ROOT / required).exists():
            errors.append(f"missing required file: {required}")

    for folder in EXPECTED_TYPES:
        if not (ROOT / folder / "index.md").exists():
            errors.append(f"missing required index: {folder}/index.md")

    for md in sorted(ROOT.rglob("*.md")):
        rel = md.relative_to(ROOT).as_posix()
        if rel.startswith("source-vault/"):
            continue
        if md.name in RESERVED:
            continue
        folder = md.relative_to(ROOT).parts[0]
        if folder not in EXPECTED_TYPES:
            warnings.append(f"{rel}: markdown file outside known bundle folders")
            continue
        frontmatter, body = split_frontmatter(md.read_text(encoding="utf-8", errors="replace"))
        page_type = str(frontmatter.get("type", "")).strip()
        if not frontmatter:
            errors.append(f"{rel}: missing parseable YAML frontmatter")
            continue
        if not page_type:
            errors.append(f"{rel}: missing required OKF field `type`")
        elif page_type != EXPECTED_TYPES[folder]:
            errors.append(f"{rel}: expected type `{EXPECTED_TYPES[folder]}`, got `{page_type}`")
        else:
            counts[page_type] += 1
        for required in ["title", "description", "source_path", "timestamp"]:
            if required not in frontmatter:
                errors.append(f"{rel}: missing required bundle field `{required}`")
        if not body.strip():
            warnings.append(f"{rel}: empty markdown body")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
        print()
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("OK: Hyundai vault-derived OKF bundle passes validation.")
    for key in ["use_case", "architecture", "technology"]:
        print(f"{key}: {counts[key]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
