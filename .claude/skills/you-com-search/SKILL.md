---
name: you-com-search
description: Use when a task needs You.com Search, Research, livecrawl page retrieval, finance research, current competitor research, three-level search workflow, or high-fidelity source discovery before generic web search.
argument-hint: "<query> [--level 1|2|3] [--mode search|research|finance] [--livecrawl] [--site domain]"
---

# You.com Search

This is the Claude Code discovery wrapper for the canonical repo-local skill.

Before You.com-backed search or research work, read and follow the canonical
instructions completely:

- `/home/shekerk/content-ideas/skills/you-com-search/SKILL.md`
- `/home/shekerk/content-ideas/skills/you-com-search/scripts/search.py`

Canonical source:
`skills/you-com-search/`

## Runtime Preamble

I'm using the Claude Code wrapper for `you-com-search`; I will follow the
canonical repo-local skill so Claude Code, Codex, and agent hosts use the same
research route and fallback rules.

## Host Compatibility

### Target Hosts
- Claude Code: yes -- this wrapper is discoverable at `.claude/skills/you-com-search/SKILL.md`.
- Codex/OpenAI: yes -- canonical source is `skills/you-com-search/SKILL.md` through repo skill routing.
- OpenHands / generic agent hosts: yes -- use `.agents/skills/you-com-search/SKILL.md`.
- Antigravity IDE: use `scripts/sync-skills-to-antigravity.sh`; it copies the canonical skill to Windows `.gemini/antigravity/skills` and `.gemini/config/skills`.

### Canonical Source
`skills/you-com-search/` is the source of truth. Do not duplicate the full
workflow here.

## Skill Relationships

### Category
Data & Analysis

### Dependencies
- `you-com-search` canonical source -- `/home/shekerk/content-ideas/skills/you-com-search/SKILL.md`

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `you-com-search` | Behavioral overlay | always; this wrapper delegates to the canonical repo-local skill | `skills/you-com-search/SKILL.md` |

## Gotchas

- Substantive workflow changes belong in `skills/you-com-search/`.
- Do not copy the full canonical skill here; duplicated instructions will drift.
- Do not claim You.com-backed research unless the canonical helper or a host-native You.com tool actually ran successfully.
