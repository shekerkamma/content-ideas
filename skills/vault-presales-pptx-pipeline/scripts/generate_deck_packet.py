#!/usr/bin/env python3
"""Generate a pre-sales deck source packet from vault notes."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


SECTION_MAP = {
    "Problem Statement": "problem",
    "Solution": "solution",
    "Solution Architecture": "architecture",
    "Business Metrics": "metrics",
    "Recommended Pilot": "pilot",
    "Related": "related",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def frontmatter_title(text: str, fallback: str) -> str:
    match = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", text, flags=re.MULTILINE)
    return match.group(1) if match else fallback


def extract_section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug[:90].rstrip("-") or "deck-packet"


def render_template(template: str, values: dict[str, str]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value or "TBD")
    return out


def wikilink_for(path: Path) -> str:
    return f"[[{path.stem}]]"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", default=".")
    parser.add_argument("--source", required=True, help="Vault-relative source note")
    parser.add_argument("--deck-type", default="use-case-realization", choices=["use-case-realization", "solution-on-page"])
    parser.add_argument("--output-dir", default="Decks/_packets")
    args = parser.parse_args()

    vault = Path(args.vault).resolve()
    source = (vault / args.source).resolve()
    text = read(source)
    title = frontmatter_title(text, source.stem)
    values = {
        "title": f"{title} - {args.deck_type.replace('-', ' ').title()}",
        "date": date.today().isoformat(),
        "source": wikilink_for(source),
        "source_links": f"- {wikilink_for(source)}",
    }
    for heading, key in SECTION_MAP.items():
        values[key] = extract_section(text, heading)
    values.setdefault("related", "- [[Hyundai Plant Operations MOC]]")

    template_name = "solution-on-page-packet.md" if args.deck_type == "solution-on-page" else "use-case-realization-packet.md"
    template_path = vault / ".claude" / "skills" / "vault-presales-pptx-pipeline" / "assets" / template_name
    template = read(template_path)
    output_dir = vault / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    packet_path = output_dir / f"{slugify(values['title'])}.md"
    packet_path.write_text(render_template(template, values), encoding="utf-8")
    print(packet_path.relative_to(vault))


if __name__ == "__main__":
    main()

