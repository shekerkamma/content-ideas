---
name: aeo-qa
description: Use when validating an AEO workflow run for schema conformance, grounded recommendations, capture integrity, source freshness, explicit status, and cross-host artifact completeness.
argument-hint: "[run-id]"
---

# aeo-qa

Validate AEO workflow artifacts before calling a report reviewed.

## Hard Gates

- `manifest.json` exists.
- required JSON/JSONL files exist.
- every query has required fields.
- every capture maps to a query and raw text file.
- every recommendation has evidence ids.
- every recommendation evidence id resolves to a capture or source.
- final report and evidence CSV exist.

## Output

Write:

`runs/<run-id>/qa/validation.json`

## Skill Relationships

### Category
Product Verification

### Dependencies
None.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `aeo-orchestrator` | Sequential upstream | always | full run folder |
| `branded-pptx-deck` | Gate / Prerequisite | before deck generation | `qa/validation.json` |

## Host Compatibility

Canonical source: `skills/aeo-qa/SKILL.md`.

## Gotchas

- Sample runs must remain `draft`, even when schemas pass.
- Do not allow orphan recommendations.
- Do not mark manual captures as automated evidence.
