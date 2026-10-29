#!/usr/bin/env python3
"""Normalize repository skill frontmatter for Codex without changing bodies."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REPORT = ROOT / "runs" / "skill-port" / "frontmatter-normalization.tsv"
ALLOWED = {"name", "description", "license", "allowed-tools", "metadata"}


def fallback_description(frontmatter: str, name: str) -> str:
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^description:\s*(.*)$", line)
        if not match:
            continue
        value = match.group(1).strip()
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            block: list[str] = []
            for candidate in lines[index + 1 :]:
                if candidate.startswith((" ", "\t")) or not candidate.strip():
                    block.append(candidate.strip())
                else:
                    break
            value = " ".join(part for part in block if part)
        return value.strip(" '\"")
    return f"Ported skill {name}. Use when a request matches this skill's workflow."


def normalize_description(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        value = f"Ported skill {name}. Use when a request matches this skill's workflow."
    value = " ".join(value.split())
    value = value.replace("<", "[").replace(">", "]")
    return value[:1024]


def normalize_skill(skill_dir: Path) -> tuple[str, str]:
    path = skill_dir / "SKILL.md"
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", content, re.DOTALL)
    if not match:
        return "FAIL", "missing or malformed frontmatter delimiters"

    original_frontmatter = match.group(1)
    body = content[match.end() :]
    parsed: dict[str, object] | None = None
    parse_error = ""
    try:
        candidate = yaml.safe_load(original_frontmatter)
        if isinstance(candidate, dict):
            parsed = candidate
        else:
            parse_error = "frontmatter was not a mapping"
    except yaml.YAMLError as exc:
        parse_error = str(exc).splitlines()[0]

    folder_name = skill_dir.name
    if parsed is None:
        new_frontmatter: dict[str, object] = {
            "name": folder_name,
            "description": normalize_description(
                fallback_description(original_frontmatter, folder_name), folder_name
            ),
            "metadata": {"legacy-frontmatter": original_frontmatter},
        }
        action = f"recovered-invalid-yaml: {parse_error}"
    else:
        declared_name = parsed.get("name")
        name = declared_name.strip() if isinstance(declared_name, str) else folder_name
        if not re.fullmatch(r"[a-z0-9-]+", name) or len(name) > 64:
            name = folder_name

        description = normalize_description(parsed.get("description"), name)
        new_frontmatter = {"name": name, "description": description}
        for key in ("license", "allowed-tools"):
            if key in parsed:
                new_frontmatter[key] = parsed[key]

        metadata = parsed.get("metadata")
        normalized_metadata: dict[str, object] = (
            dict(metadata) if isinstance(metadata, dict) else {}
        )
        legacy = {key: value for key, value in parsed.items() if key not in ALLOWED}
        if legacy:
            normalized_metadata["legacy-frontmatter"] = legacy
        if normalized_metadata:
            new_frontmatter["metadata"] = normalized_metadata
        action = "normalized" if legacy or description != parsed.get("description") else "unchanged"

    rendered = yaml.safe_dump(
        new_frontmatter,
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    ).rstrip()
    updated = f"---\n{rendered}\n---\n{body}"
    if updated != content:
        path.write_text(updated, encoding="utf-8")
    return "PASS", action


def main() -> int:
    rows = ["skill\tstatus\taction"]
    failures = 0
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").is_file():
            continue
        status, action = normalize_skill(skill_dir)
        rows.append(f"{skill_dir.name}\t{status}\t{action}")
        failures += status != "PASS"
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"skills={len(rows) - 1} failures={failures} report={REPORT}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
