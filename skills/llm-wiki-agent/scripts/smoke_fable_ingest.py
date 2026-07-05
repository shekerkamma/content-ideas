#!/usr/bin/env python3
"""Run a deterministic Fable/Karpathy LLM wiki ingest smoke test.

This creates a sample wiki, drops in one URL-style source and one PDF-extract
source under raw/, ingests them into linked wiki pages, and validates that
index/log/backlinks/query routing all exist.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


URL_SOURCE = """# URL Capture: Karpathy LLM Wiki Idea

Source type: url
Source URL: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Karpathy's idea is to keep an LLM-readable knowledge base as markdown. The
knowledge base should be organized so a model can progressively disclose
context: start from a routing surface, read only relevant pages, and follow
links when needed.

Important claims:
- Markdown keeps the knowledge base portable across model hosts.
- The index should route the model to the right pages.
- The model should avoid loading the entire corpus when a narrower path works.
"""


PDF_SOURCE = """# PDF Extract: Fable 5 LLM Wiki Demo Notes

Source type: pdf-extract
Original file: Claude Fable 5 LLM Wiki.pdf

The demo uses Claude Code and Obsidian to create a connected second brain. The
human drops sources into raw/. The agent reads the source material, splits it
into wiki pages, adds backlinks, updates index.md, and appends log.md.

The structure can be flat for homogeneous corpora such as meeting transcripts.
It can be foldered for mixed corpora such as YouTube videos, PDFs, URLs, tools,
concepts, entities, topics, and comparisons.

Important claims:
- raw/ is source input and should be treated as read-only.
- wiki/ is generated output.
- index.md is the routing surface.
- log.md is operation history.
- backlinks are what turn summaries into a connected second brain.
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def append(path: Path, text: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


def init_wiki(root: Path, profile: str, reset: bool) -> None:
    if reset and root.exists():
        shutil.rmtree(root)

    init_script = Path(__file__).with_name("init_llm_wiki.py")
    subprocess.run(
        [sys.executable, str(init_script), "--root", str(root), "--profile", profile, "--overwrite"],
        check=True,
    )


def ingest_sources(root: Path) -> None:
    raw = root / "raw"
    wiki = root / "wiki"

    write(raw / "karpathy-llm-wiki-url.md", URL_SOURCE)
    write(raw / "claude-fable-5-llm-wiki-pdf-extract.md", PDF_SOURCE)

    write(
        wiki / "sources" / "karpathy-llm-wiki-url.md",
        """---
type: source
source_path: raw/karpathy-llm-wiki-url.md
source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
---

# Karpathy LLM Wiki Idea

Karpathy's LLM wiki pattern uses markdown as a portable knowledge base. The
agent should start from a routing surface, read narrowly relevant pages, and
follow links only when needed.

Links: [LLM Wiki](../concepts/llm-wiki.md), [Progressive Disclosure](../concepts/progressive-disclosure.md)
""",
    )

    write(
        wiki / "sources" / "fable-5-llm-wiki-pdf.md",
        """---
type: source
source_path: raw/claude-fable-5-llm-wiki-pdf-extract.md
original_file: Claude Fable 5 LLM Wiki.pdf
---

# Fable 5 LLM Wiki Demo PDF Extract

The demo shows a Claude Code and Obsidian workflow where source material goes
into raw/, generated knowledge goes into wiki/, and every ingest updates
index.md, log.md, and backlinks.

Links: [LLM Wiki](../concepts/llm-wiki.md), [Flat vs Foldered Wiki](../concepts/flat-vs-foldered-wiki.md), [Obsidian](../entities/obsidian.md)
""",
    )

    write(
        wiki / "concepts" / "llm-wiki.md",
        """---
type: concept
---

# LLM Wiki

An LLM wiki is a markdown knowledge base designed for file-reading agents. It
keeps raw source material separate from generated knowledge pages, then uses an
index, logs, and backlinks to route future questions.

Use it when repeated sources should become a durable second brain instead of
one-off chat context.

Sources: [Karpathy LLM Wiki Idea](../sources/karpathy-llm-wiki-url.md), [Fable 5 LLM Wiki Demo PDF Extract](../sources/fable-5-llm-wiki-pdf.md)
Related: [Progressive Disclosure](progressive-disclosure.md), [Flat vs Foldered Wiki](flat-vs-foldered-wiki.md)
""",
    )

    write(
        wiki / "concepts" / "progressive-disclosure.md",
        """---
type: concept
---

# Progressive Disclosure

Progressive disclosure means the agent starts from `wiki/index.md`, reads only
the pages needed for the current question, and follows links when those pages
show a useful route. It avoids scanning the full corpus by default.

Sources: [Karpathy LLM Wiki Idea](../sources/karpathy-llm-wiki-url.md)
Related: [LLM Wiki](llm-wiki.md)
""",
    )

    write(
        wiki / "concepts" / "flat-vs-foldered-wiki.md",
        """---
type: concept
---

# Flat vs Foldered Wiki

Use a flat wiki for small or homogeneous corpora. Use a foldered wiki when
source types and page types diverge, such as URLs, PDFs, videos, tools,
concepts, entities, topics, and comparisons.

Sources: [Fable 5 LLM Wiki Demo PDF Extract](../sources/fable-5-llm-wiki-pdf.md)
Related: [LLM Wiki](llm-wiki.md)
""",
    )

    write(
        wiki / "entities" / "obsidian.md",
        """---
type: entity
---

# Obsidian

Obsidian is the markdown vault interface used in the demo. The wiki itself stays
plain markdown, so Codex, Claude Code, and other file-reading agents can operate
on the same files.

Sources: [Fable 5 LLM Wiki Demo PDF Extract](../sources/fable-5-llm-wiki-pdf.md)
""",
    )

    write(
        wiki / "topics" / "ai-os-second-brain.md",
        """---
type: topic
---

# AI OS Second Brain

The second-brain pattern turns repeated sources into a connected markdown graph
that an AI operating system can reason over. The value comes from routing,
source traceability, and links between concepts rather than isolated summaries.

Routes: [LLM Wiki](../concepts/llm-wiki.md), [Progressive Disclosure](../concepts/progressive-disclosure.md), [Obsidian](../entities/obsidian.md)
""",
    )

    write(
        wiki / "answers" / "how-to-build-fable-style-llm-wiki.md",
        """# How To Build A Fable-Style LLM Wiki

1. Initialize `raw/`, `wiki/`, `wiki/index.md`, `wiki/log.md`, `AGENTS.md`, and `CLAUDE.md`.
2. Drop source material into `raw/`.
3. Ingest each source into source, concept, entity, and topic pages as needed.
4. Add backlinks between related pages.
5. Update `wiki/index.md` with route hints.
6. Append `wiki/log.md`.
7. Answer questions by reading the index first, then relevant pages only.

Grounded in:
- [Karpathy LLM Wiki Idea](../sources/karpathy-llm-wiki-url.md)
- [Fable 5 LLM Wiki Demo PDF Extract](../sources/fable-5-llm-wiki-pdf.md)
""",
    )

    write(
        wiki / "index.md",
        """# LLM Wiki Index

Use this file as the routing surface before reading individual pages.

## Sources

- [Karpathy LLM Wiki Idea](sources/karpathy-llm-wiki-url.md) - markdown wiki, routing surface, progressive disclosure
- [Fable 5 LLM Wiki Demo PDF Extract](sources/fable-5-llm-wiki-pdf.md) - Claude Code, Obsidian, raw/wiki/index/log workflow

## Concepts

- [LLM Wiki](concepts/llm-wiki.md) - durable markdown second brain for file-reading agents
- [Progressive Disclosure](concepts/progressive-disclosure.md) - read index first, then relevant pages only
- [Flat vs Foldered Wiki](concepts/flat-vs-foldered-wiki.md) - structure decision for homogeneous vs mixed corpora

## Entities

- [Obsidian](entities/obsidian.md) - markdown vault UI used in the demo

## Topics

- [AI OS Second Brain](topics/ai-os-second-brain.md) - connected source-backed graph for agent reasoning

## Answer Routes

- "How do I build this?" -> [How To Build A Fable-Style LLM Wiki](answers/how-to-build-fable-style-llm-wiki.md)
- "Should my wiki be flat or foldered?" -> [Flat vs Foldered Wiki](concepts/flat-vs-foldered-wiki.md)
- "How should agents answer questions?" -> [Progressive Disclosure](concepts/progressive-disclosure.md)
""",
    )

    append(
        wiki / "log.md",
        """
## ingest | fable-karpathy-smoke

- ingested raw/karpathy-llm-wiki-url.md
- ingested raw/claude-fable-5-llm-wiki-pdf-extract.md
- created source, concept, entity, topic, and answer pages
- updated index routes and backlinks

## query | how to build this wiki

- read wiki/index.md
- followed route to wiki/answers/how-to-build-fable-style-llm-wiki.md
- checked source pages for traceability
""",
    )


def validate(root: Path) -> list[str]:
    required = [
        "raw/karpathy-llm-wiki-url.md",
        "raw/claude-fable-5-llm-wiki-pdf-extract.md",
        "wiki/index.md",
        "wiki/log.md",
        "wiki/sources/karpathy-llm-wiki-url.md",
        "wiki/sources/fable-5-llm-wiki-pdf.md",
        "wiki/concepts/llm-wiki.md",
        "wiki/concepts/progressive-disclosure.md",
        "wiki/concepts/flat-vs-foldered-wiki.md",
        "wiki/entities/obsidian.md",
        "wiki/topics/ai-os-second-brain.md",
        "wiki/answers/how-to-build-fable-style-llm-wiki.md",
        "AGENTS.md",
        "CLAUDE.md",
    ]
    failures = [path for path in required if not (root / path).exists()]

    checks = {
        "index routes answer": ("wiki/index.md", "How To Build A Fable-Style LLM Wiki"),
        "index routes flat/foldered": ("wiki/index.md", "Flat vs Foldered Wiki"),
        "log records ingest": ("wiki/log.md", "ingest | fable-karpathy-smoke"),
        "log records query": ("wiki/log.md", "query | how to build this wiki"),
        "answer cites karpathy source": ("wiki/answers/how-to-build-fable-style-llm-wiki.md", "Karpathy LLM Wiki Idea"),
        "answer cites pdf source": ("wiki/answers/how-to-build-fable-style-llm-wiki.md", "Fable 5 LLM Wiki Demo PDF Extract"),
        "concept backlinks sources": ("wiki/concepts/llm-wiki.md", "../sources/fable-5-llm-wiki-pdf.md"),
    }
    for label, (path, needle) in checks.items():
        text = (root / path).read_text(encoding="utf-8") if (root / path).exists() else ""
        if needle not in text:
            failures.append(label)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default="/tmp/llm-wiki-fable-smoke",
        help="Directory for the sample wiki",
    )
    parser.add_argument("--reset", action="store_true", help="Delete the target directory before running")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    init_wiki(root, "foldered", args.reset)
    (root / "wiki" / "answers").mkdir(parents=True, exist_ok=True)
    ingest_sources(root)

    failures = validate(root)
    if failures:
        print("Smoke test failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Fable/Karpathy LLM wiki smoke test passed: {root}")
    print("Try query route: wiki/index.md -> wiki/answers/how-to-build-fable-style-llm-wiki.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
