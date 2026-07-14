---
name: competitor-analysis-pipeline
description: Use when the user asks for competitor analysis, competitive landscape, competitor benchmarking, battlecards, market map, positioning analysis, consulting-firm positioning comparisons, or client-ready competitor-analysis deliverables. Use especially when outputs must include sourced research, a structured storyline, a branded PPTX deck, an interactive HTML page, GitHub Pages publishing, or review gates such as grill-me, story-architect, STORM, GStack strategy/design review, and PPTX/HTML QA.
---

# Competitor Analysis Pipeline

This is the Claude Code discovery wrapper for the canonical repo-local skill.

Before competitor-analysis work, read and follow the canonical instructions completely:

- `/home/shekerk/content-ideas/skills/competitor-analysis-pipeline/SKILL.md`
- `/home/shekerk/content-ideas/skills/competitor-analysis-pipeline/references/quality-gates.md` before finalizing client-facing deck or HTML output

Canonical source:
`skills/competitor-analysis-pipeline/`

## Runtime Preamble

I'm using the Claude Code wrapper for `competitor-analysis-pipeline`; I will follow the canonical repo-local skill so Claude, Codex, and OpenHands stay aligned.

## Host Compatibility

### Target Hosts
- Claude Code: yes -- this wrapper is discoverable at `.claude/skills/competitor-analysis-pipeline/SKILL.md`.
- Codex/OpenAI: yes -- canonical source is `skills/competitor-analysis-pipeline/SKILL.md` through repo skill routing.
- OpenHands: yes -- use the canonical repo-local source or mirror/wrapper through `.agents/skills/competitor-analysis-pipeline/SKILL.md` if needed.

### Canonical Source
`skills/competitor-analysis-pipeline/` is the source of truth. Do not duplicate the full workflow here.

### Tool Mapping
Follow the canonical skill's host-neutral tool mapping and source/tool order.

## Skill Relationships

### Category
Business Automation

### Dependencies
- `competitor-analysis-pipeline` canonical source -- `/home/shekerk/content-ideas/skills/competitor-analysis-pipeline/SKILL.md`

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `competitor-analysis-pipeline` | Behavioral overlay | always; this wrapper delegates to the canonical repo-local skill | `skills/competitor-analysis-pipeline/SKILL.md` |

## Gotchas

- Do not edit this wrapper instead of the canonical skill. Substantive workflow changes belong in `skills/competitor-analysis-pipeline/`.
- Do not copy the full canonical skill here; duplicated instructions will drift.
- This wrapper exists for Claude Code auto-discovery. Codex and OpenHands should use the canonical repo-local skill unless a host-specific wrapper is required.
