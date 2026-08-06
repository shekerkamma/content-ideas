---
name: agentic-blueprint-pipeline
description: Use when generating or upgrading research-backed Agentic Master Implementation Blueprints for market-positioning portfolios from use-case scorecards, competitor teardowns, and deep research.
argument-hint: "[use-case-name|all|gold-standard]"
---

# agentic-blueprint-pipeline

This is the Codex/OpenHands discovery wrapper for the canonical project skill.

Paths below are repo-relative. Resolve them against the `content-ideas`
checkout root — do not hard-code an absolute home directory, which breaks the
moment the checkout moves or the user account changes.

Before doing blueprint work, read and follow:

- `.claude/skills/agentic-blueprint-pipeline/SKILL.md`
- `.claude/skills/agentic-blueprint-pipeline/references/master-blueprint-template.md`
- `.claude/skills/agentic-blueprint-pipeline/references/implementation-depth-checklist.md`
- `.claude/skills/agentic-blueprint-pipeline/references/quality-rubric.md`
- `.claude/skills/agentic-blueprint-pipeline/references/research-agent-brief.md`

Canonical source:
`.claude/skills/agentic-blueprint-pipeline/`

Default run root:
`runs/2026-06-26-agentic-opportunity-blueprints/`

## Source / Tool Order

This wrapper inherits the canonical pipeline's research policy. Before any
generic WebSearch/search_web call, use the wired dependency chain:

1. Local scorecards, prior run artifacts, and referenced canonical files.
2. GBrain recall for the use case, vertical, incumbents, and prior research.
3. `you-com-search`, Hermes `web.search_backend: you`, or equivalent You.com
   API wrapper for current-web discovery, livecrawl, research, and finance
   research.
4. Exa for semantic/source discovery and Firecrawl for page capture after URLs
   are identified.
5. Specialist MCPs/plugins for official docs, GitHub, finance, or regulatory
   sources.
6. Generic WebSearch/search_web only as a last fallback, never as the first
   research route.

## Cross-host copies

This wrapper is mirrored byte-identically to `.agents/skills/agentic-blueprint-pipeline/`
for Codex and OpenHands discovery. Keep the two copies in sync; change the
canonical skill under `.claude/skills/` and re-mirror rather than editing a
mirror directly.
