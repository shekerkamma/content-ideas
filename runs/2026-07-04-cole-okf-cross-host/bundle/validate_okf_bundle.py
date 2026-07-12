#!/usr/bin/env python3
"""Validate the Cole Medin AI-coding OKF bundle.

Checks both generic OKF requirements and this bundle's profile:
- every concept document has YAML frontmatter
- every concept document has a non-empty type
- video pages include source/resource/related_concepts
- concept pages include related_videos
- required indexes and log are present
- related slugs point at existing pages
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESERVED = {
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "index.md",
    "log.md",
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
        if not line:
            continue
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


def as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str) and value:
        return [value]
    return []


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for required in ["README.md", "AGENTS.md", "CLAUDE.md", "index.md", "log.md", "okf-cli.py"]:
        if not (ROOT / required).exists():
            errors.append(f"missing required file: {required}")

    for required_dir in ["videos", "concepts"]:
        if not (ROOT / required_dir / "index.md").exists():
            errors.append(f"missing required index: {required_dir}/index.md")

    video_slugs = {p.stem for p in (ROOT / "videos").glob("*.md") if p.name != "index.md"}
    concept_slugs = {p.stem for p in (ROOT / "concepts").glob("*.md") if p.name != "index.md"}

    for md in sorted(ROOT.rglob("*.md")):
        rel = md.relative_to(ROOT).as_posix()
        if md.name in RESERVED:
            continue
        frontmatter, body = split_frontmatter(md.read_text(encoding="utf-8", errors="replace"))
        page_type = str(frontmatter.get("type", "")).strip()
        if not frontmatter:
            errors.append(f"{rel}: missing parseable YAML frontmatter")
            continue
        if not page_type:
            errors.append(f"{rel}: missing required OKF field `type`")
            continue
        if "title" not in frontmatter:
            warnings.append(f"{rel}: missing recommended field `title`")
        if "description" not in frontmatter:
            warnings.append(f"{rel}: missing recommended field `description`")
        if not body.strip():
            warnings.append(f"{rel}: empty markdown body")

        if rel.startswith("videos/"):
            if page_type != "video":
                errors.append(f"{rel}: expected type `video`, got `{page_type}`")
            for field in ["resource", "source", "related_concepts"]:
                if field not in frontmatter:
                    errors.append(f"{rel}: missing Cole video field `{field}`")
            for slug in as_list(frontmatter.get("related_concepts")):
                if slug not in concept_slugs:
                    errors.append(f"{rel}: related_concepts points to missing concept `{slug}`")

        if rel.startswith("concepts/"):
            if page_type != "concept":
                errors.append(f"{rel}: expected type `concept`, got `{page_type}`")
            if "related_videos" not in frontmatter:
                errors.append(f"{rel}: missing Cole concept field `related_videos`")
            for slug in as_list(frontmatter.get("related_videos")):
                if slug not in video_slugs:
                    errors.append(f"{rel}: related_videos points to missing video `{slug}`")

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

    print("OK: bundle passes OKF and Cole AI-coding profile validation.")
    print(f"Videos: {len(video_slugs)}")
    print(f"Concepts: {len(concept_slugs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

