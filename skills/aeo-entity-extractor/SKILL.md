---
name: aeo-entity-extractor
description: Use when extracting brands, competitors, products, claims, citations, source domains, and buyer concerns from AEO answer captures and source records.
argument-hint: "[run-id]"
---

# aeo-entity-extractor

Extract normalized entities from answer captures and source records.

## Entity Types

Use:

`brand`, `competitor`, `product`, `feature`, `use_case`, `claim`, `source`,
`buyer_concern`.

## Rules

- Normalize aliases before scoring.
- Keep source/capture ids attached to every entity.
- Do not invent entities absent from captures or supplied configuration.
- Prefer deterministic extraction for names and URLs; use model judgment only
  for ambiguous claims or buyer concerns.

## Output

Write records to:

`runs/<run-id>/normalized/entities.jsonl`

## Skill Relationships

### Category
Data & Analysis

### Dependencies
None.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `aeo-orchestrator` | Sequential downstream | always | `normalized/entities.jsonl` |
| `aeo-gap-analyzer` | Sequential downstream | after extraction | `entities.jsonl` + `visibility_scores.json` |

## Host Compatibility

Canonical source: `skills/aeo-entity-extractor/SKILL.md`.

## Gotchas

- Avoid entity duplication caused by casing, punctuation, or URL variants.
- Do not classify a competitor mention as a recommendation unless the answer
  framing supports it.
