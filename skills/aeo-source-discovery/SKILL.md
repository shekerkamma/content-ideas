---
name: aeo-source-discovery
description: Use when discovering, normalizing, and classifying sources for an AEO audit, including official pages, competitor pages, cited URLs, Reddit/forum pages, analyst pages, news, and review sites.
argument-hint: "[run-id|topic|domain]"
---

# aeo-source-discovery

Discover and normalize sources for an AEO audit. Prefer current, primary, and
crawlable sources.

## Source Order

1. Local run inputs and supplied URLs.
2. GBrain/second-brain recall when available.
3. `you-com-search` or Hermes You.com backend for current-web search,
   livecrawl, research, and finance research when available.
4. Exa/research plugins or specialist MCPs when available for semantic/source
   discovery.
5. Firecrawl for page capture/crawl/extract after URLs are known.
6. Official product pages, docs, pricing pages, public filings, and media kits.
7. Community/operator sources such as Reddit only when relevant.
8. Generic web search last.

## Classification

Use `source_type`:

`official`, `docs`, `pricing`, `review`, `forum`, `analyst`, `news`,
`competitor`, `social`, `unknown`.

## Output

Write records to:

`runs/<run-id>/stage_outputs/sources.jsonl`

## Skill Relationships

### Category
Data & Analysis

### Dependencies
None.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `aeo-orchestrator` | Sequential downstream | always | `stage_outputs/sources.jsonl` |
| `enterprise-ai-competitor-landscape` | Sequential upstream | when competitor universe exists | sourced company table |
| `pr-target-prescreen` | Peer | when PR outlet crawlability is the main question | ranked PR source table |

## Host Compatibility

Canonical source: `skills/aeo-source-discovery/SKILL.md`.

## Gotchas

- Do not treat raw search results as source evidence until URLs are classified.
- Do not mark freshness as current unless the page date or retrieval date
  supports it.
