---
name: firecrawl
description: Use Firecrawl from Codex or Claude Code through the installed firecrawl-pp-cli binary for live web scraping, crawling, search, page ingestion, extraction, and deep research. Use when market research, competitor analysis, buyer-pain validation, documentation ingestion, or full-page evidence capture needs more than generic web search.
license: Apache-2.0
metadata:
  legacy-frontmatter:
    category: Research
    argument-hint: <command> [args] | scrape <url> | search <query> | deep-research <query> | doctor
---

# Firecrawl

This repository-local skill exposes Firecrawl to Codex, Claude Code, and other
hosts that support portable skills.

## Availability

Before using Firecrawl, verify the CLI:

```bash
command -v firecrawl-pp-cli
firecrawl-pp-cli --version
firecrawl-pp-cli doctor
```

If `doctor` reports network unreachable inside Codex, the CLI is installed but
the current sandbox blocks external API access. In that case, request
escalation for the specific Firecrawl command or mark Firecrawl as blocked for
the run. Do not silently fall back to generic search for validated research.

For search/discovery, prefer `you-com-search` before generic WebSearch when it
is available. Firecrawl is primarily the full-page capture/crawl/extract layer
after important URLs are known, or a deep-research route when explicitly needed.

## Auth

The CLI can use its local OAuth/config file or `FIRECRAWL_BEARER_AUTH`.

Do not print tokens. Check auth with:

```bash
firecrawl-pp-cli doctor
```

## Direct Commands

Always use agent mode for machine-readable output:

```bash
firecrawl-pp-cli <command> [subcommand] [args] --agent
```

Common commands:

- `firecrawl-pp-cli scrape <url> --agent`
- `firecrawl-pp-cli firecrawl-search "<query>" --agent`
- `firecrawl-pp-cli deep-research start "<query>" --agent`
- `firecrawl-pp-cli deep-research get-status <id> --agent`
- `firecrawl-pp-cli crawl urls <url> --agent`
- `firecrawl-pp-cli map <url> --agent`
- `firecrawl-pp-cli extract data <url> --agent`
- `firecrawl-pp-cli team get-credit-usage --agent`

When unsure, ask the CLI:

```bash
firecrawl-pp-cli which "<capability in your own words>"
```

## Research Usage Rules

Use Firecrawl after discovery to ingest important pages deeply:

- vendor pricing and packaging pages,
- docs and implementation guides,
- changelogs and release notes,
- review pages and support threads,
- competitor websites,
- regulatory or source documents.

For validated strategy work, Firecrawl should capture the important pages found
by You.com, Exa, Reddit tools, subagents, or other discovery routes. Record
exact URL, access date, command used, and whether output was live or blocked.

## Failure Policy

If Firecrawl is unavailable, unauthenticated, out of credits, or blocked by
sandbox/network policy:

1. Record the exact failure.
2. Downgrade the research mode if Firecrawl was part of the evidence bar.
3. Produce a Firecrawl command pack for a later live run.
4. Do not claim Firecrawl-backed validation.
5. If `you-com-search` is available, use it before generic WebSearch for
   discovery or source replacement.
