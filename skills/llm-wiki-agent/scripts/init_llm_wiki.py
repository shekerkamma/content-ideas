#!/usr/bin/env python3
"""Initialize a cross-host markdown LLM wiki.

Creates the raw/wiki/index/log/AGENTS/CLAUDE structure described by the
llm-wiki-agent skill. Standard library only.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def write_once(path: Path, text: str, overwrite: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return
    path.write_text(text, encoding="utf-8")


def host_instructions(host: str, profile: str) -> str:
    filename = "AGENTS.md" if host == "codex" else "CLAUDE.md"
    label = "Codex/generic agents" if host == "codex" else "Claude Code"
    return f"""# LLM Wiki Instructions - {label}

This project is a markdown LLM wiki. It is intentionally host-neutral and should
work in Codex, Claude Code, Fable-enabled Claude Code sessions, and any agent
that can read local files.

## Structure

- `raw/` - source material. Treat as read-only input unless the user explicitly
  asks you to edit it.
- `wiki/` - generated knowledge pages.
- `wiki/index.md` - table of contents and routing surface.
- `wiki/log.md` - append-only operation history.
- `{filename}` - this host's operating rules.

Profile: `{profile}`

## Ingest

1. Read `wiki/index.md` and recent entries in `wiki/log.md`.
2. Inspect the new source in `raw/` or the URL/content provided by the user.
3. Decide whether to update existing pages or create new pages.
4. Write source, concept, entity, topic, comparison, or note pages as useful.
5. Add markdown backlinks between related pages.
6. Update `wiki/index.md`.
7. Append an entry to `wiki/log.md`.
8. Report changed files and source traceability.

## Query

1. Start from `wiki/index.md`.
2. Read relevant pages only.
3. Follow links when they are useful.
4. Cite source paths/page names.
5. Mark inference explicitly.

## Maintenance

After several ingests, check for orphan pages, duplicate concepts, stale links,
contradictions, oversized pages, and missing source traceability. Log the pass in
`wiki/log.md`.
"""


def index_text(profile: str) -> str:
    sections = ["sources", "concepts", "entities", "topics"] if profile in {"foldered", "okf"} else ["pages"]
    rows = [
        "# LLM Wiki Index",
        "",
        "Use this file as the routing surface before reading individual pages.",
        "",
        "## Sections",
        "",
    ]
    for section in sections:
        rows.append(f"- `{section}` - add one-line route hints here as the wiki grows.")
    rows.extend([
        "",
        "## Recent Route Hints",
        "",
        "- No ingested sources yet.",
        "",
    ])
    return "\n".join(rows)


def log_text() -> str:
    return """# LLM Wiki Log

Use newest-first entries. Keep entries short and parseable.

## Initial setup

- initialized raw/wiki/index/log cross-host wiki structure
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Wiki root directory to create")
    parser.add_argument("--profile", choices=["flat", "foldered", "okf"], default="foldered")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing instruction/index files")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    raw = root / "raw"
    raw.mkdir(parents=True, exist_ok=True)

    if args.profile == "okf":
        for folder in ["sources", "concepts", "entities", "topics"]:
            (root / folder).mkdir(parents=True, exist_ok=True)
        write_once(root / "index.md", index_text(args.profile), args.overwrite)
        write_once(root / "log.md", log_text(), args.overwrite)
        write_once(root / "AGENTS.md", host_instructions("codex", args.profile), args.overwrite)
        write_once(root / "CLAUDE.md", host_instructions("claude", args.profile), args.overwrite)
        write_once(raw / ".gitkeep", "", args.overwrite)
        print(f"Initialized LLM wiki at {root}")
        print(f"Profile: {args.profile}")
        print("Next: put a source in raw/ or provide a URL, then ask the agent to ingest it.")
        return 0

    wiki = root / "wiki"
    wiki.mkdir(parents=True, exist_ok=True)

    if args.profile == "foldered":
        for folder in ["sources", "concepts", "entities", "topics"]:
            (wiki / folder).mkdir(parents=True, exist_ok=True)

    write_once(wiki / "index.md", index_text(args.profile), args.overwrite)
    write_once(wiki / "log.md", log_text(), args.overwrite)
    write_once(root / "AGENTS.md", host_instructions("codex", args.profile), args.overwrite)
    write_once(root / "CLAUDE.md", host_instructions("claude", args.profile), args.overwrite)
    write_once(raw / ".gitkeep", "", args.overwrite)

    print(f"Initialized LLM wiki at {root}")
    print(f"Profile: {args.profile}")
    print("Next: put a source in raw/ or provide a URL, then ask the agent to ingest it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
