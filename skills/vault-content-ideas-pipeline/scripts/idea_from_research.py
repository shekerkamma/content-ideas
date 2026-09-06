#!/usr/bin/env python3
"""Create an Idea note and LinkedIn draft from one enriched research note."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def frontmatter_value(text: str, key: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    block = text[3:end]
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", block, flags=re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip('"')


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug[:90].rstrip("-") or "content-idea"


def first_sentence(text: str) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", clean)
    return parts[0] if parts and parts[0] else clean[:180]


def wikilink_for_source(source: Path, vault: Path) -> str:
    return f"[[{source.stem}]]"


def make_idea(title: str, source: Path, vault: Path, text: str) -> str:
    tldr = section(text, "TL;DR")
    integration = section(text, "Integration Potential")
    steal = section(text, "Steal-Worthy Elements")
    takeaways = section(text, "Key Takeaways")
    thesis = first_sentence(tldr or integration or takeaways or title)
    source_link = wikilink_for_source(source, vault)
    return f"""---
title: {title}
tags: [idea, content, content-research]
status: seed
created: {date.today().isoformat()}
source: {source_link}
---

# {title}

## Thesis
{thesis}

## Source Research
- {source_link}

## Why It Matters
{integration or "This needs a judgment pass against the source research."}

## Possible Angles
{steal or takeaways or "- Turn the core pattern into a practical enterprise AI lesson."}

## Next Action
- Decide whether this becomes a LinkedIn post, POC asset, or project note.

## Related
- [[Content Research MOC]]
- [[The Multi-Cloud POC Factory]]
- [[AI Agent Systems MOC]]
"""


def make_linkedin(title: str, source: Path, vault: Path, text: str) -> str:
    tldr = section(text, "TL;DR")
    takeaways = section(text, "Key Takeaways")
    integration = section(text, "Integration Potential")
    source_link = wikilink_for_source(source, vault)
    point = first_sentence(tldr or takeaways or title)
    return f"""---
title: {title}
tags: [content, linkedin, draft]
status: draft
created: {date.today().isoformat()}
source: {source_link}
---

# {title}

## Hook Options
- The best AI teams are not just writing better prompts. They are building better operating systems.
- Most agent failures are not model failures. They are context failures.
- A research note is wasted if it never becomes a decision, demo, or draft.

## Draft
{point}

The pattern is simple:

1. Capture the source.
2. Extract the reusable idea.
3. Link it to the operating wiki.
4. Turn it into a decision, POC, or public point of view.

That is the difference between content collection and a working knowledge system.

For enterprise AI, this matters because teams do not need more saved articles. They need reusable judgment.

## Source Notes
- {source_link}

## Repurpose
- X thread: break the four-step pattern into short points.
- POC Factory: turn the pattern into a demo workflow.
- Vault: add backlinks to related MOCs.

## Related
- [[Content Research MOC]]
- [[The Multi-Cloud POC Factory]]
- [[Claude Code Skills MOC]]
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", default=".")
    parser.add_argument("--source", required=True)
    parser.add_argument("--title")
    args = parser.parse_args()

    vault = Path(args.vault).resolve()
    source = (vault / args.source).resolve()
    text = read(source)
    raw_title = args.title or frontmatter_value(text, "title") or source.stem.replace("-", " ").title()
    title = raw_title.replace(":", " -")
    slug = slugify(title)

    ideas = vault / "Ideas"
    linkedin = vault / "Content" / "LinkedIn"
    ideas.mkdir(parents=True, exist_ok=True)
    linkedin.mkdir(parents=True, exist_ok=True)

    idea_path = ideas / f"{slug}.md"
    linkedin_path = linkedin / f"{slug}-linkedin.md"
    if not idea_path.exists():
        idea_path.write_text(make_idea(title, source, vault, text), encoding="utf-8")
    if not linkedin_path.exists():
        linkedin_path.write_text(make_linkedin(title, source, vault, text), encoding="utf-8")

    print(f"Idea: {idea_path.relative_to(vault)}")
    print(f"LinkedIn: {linkedin_path.relative_to(vault)}")


if __name__ == "__main__":
    main()
