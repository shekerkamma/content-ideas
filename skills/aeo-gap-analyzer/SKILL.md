---
name: aeo-gap-analyzer
description: Use when converting AEO visibility scores, answer captures, entities, and source evidence into prioritized AI-search gap recommendations.
argument-hint: "[run-id]"
---

# aeo-gap-analyzer

Turn evidence into traceable recommendations. Every recommendation must cite
evidence ids.

## Gap Themes

Use these themes first:

- `competitor recommended`
- `brand absent`
- `citation gap`
- `owned source weak`
- `third-party source gap`
- `freshness gap`
- `entity ambiguity`
- `content format gap`

## Priority Rule

Priority derives from:

1. severity of lost recommendation or absence
2. number of affected queries
3. quality of evidence
4. expected effort

## Output

Write records to:

`runs/<run-id>/normalized/recommendations.jsonl`

## Skill Relationships

### Category
Data & Analysis

### Dependencies
None.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `aeo-orchestrator` | Sequential downstream | always | `normalized/recommendations.jsonl` |
| `ai-mode-content-brief` | Future downstream | when recommendations should become content briefs | `recommendations.jsonl` |
| `branded-pptx-deck` | Downstream | after QA passes and deck requested | final Markdown summary |

## Host Compatibility

Canonical source: `skills/aeo-gap-analyzer/SKILL.md`.

## Gotchas

- Do not recommend content solely because it sounds useful. It must map to
  observed evidence.
- Do not imply guaranteed AI-search ranking improvement.
