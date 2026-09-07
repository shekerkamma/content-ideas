---
name: vault-content-ideas-pipeline
description: Use when turning content research, clippings, agent notes, POC patterns, or wiki insights into content ideas, LinkedIn drafts, X drafts, reusable hooks, or a content backlog grounded in Sheker's Obsidian wiki.
---

# Vault Content Ideas Pipeline

Convert research into publishable thinking.

## Pipe

1. Start from one or more `content-research/` notes.
2. Extract the thesis, reusable pattern, enterprise relevance, and strongest hook.
3. Create or update an `Ideas/` note with source backlinks.
4. Create a draft in `Content/LinkedIn/` when the idea is strong enough.
5. Add follow-up tasks to `Boards/Work.md` only if action is needed.
6. Link everything back to source research, relevant MOCs, and projects.

## Required Idea Note Shape

- `## Thesis`
- `## Source Research`
- `## Why It Matters`
- `## Possible Angles`
- `## Next Action`
- `## Related`

## Required LinkedIn Draft Shape

- `## Hook Options`
- `## Draft`
- `## Source Notes`
- `## Repurpose`

## Script

Use `scripts/idea_from_research.py --source <path>` to create a first-pass idea and LinkedIn draft from one enriched research note. Edit after generation for judgment and voice.

## Grounding Rules

- Every content idea must cite at least one source note.
- Do not create generic content advice.
- Tie ideas to [[The Multi-Cloud POC Factory]], [[TMNA]], [[SAP]], [[Codex]], [[MCP]], or [[agentic AI]] when the connection is real.
- Keep the voice strategic, direct, and non-marketing.

