---
name: aeo-answer-capture
description: Use when capturing or ingesting AI-search answer evidence for an AEO audit, including manual pasted captures, API captures, browser captures, citations, model/surface metadata, and timestamps.
argument-hint: "[run-id|capture file]"
---

# aeo-answer-capture

Capture AI-answer evidence without hiding state in chat. Preserve raw answer
text before analysis.

## Capture Rules

Every capture must record:

- query id
- engine or surface
- timestamp
- raw answer text path
- citation URLs as a separate list
- metadata such as model, region, account state, or collection method when known

Manual pasted answers are valid for V1, but mark engine as `manual` or include
the actual surface if known.

## Output

Write records to:

`runs/<run-id>/stage_outputs/answer_captures.jsonl`

Raw text lives under:

`runs/<run-id>/stage_outputs/raw/<capture-id>.txt`

## Skill Relationships

### Category
Data & Analysis

### Dependencies
None.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `aeo-orchestrator` | Sequential downstream | always | `stage_outputs/answer_captures.jsonl` |
| `playwright-cli` | Optional upstream | when browser capture is required | screenshot/trace/raw text |

## Host Compatibility

Canonical source: `skills/aeo-answer-capture/SKILL.md`.

## Gotchas

- Never overwrite raw answer files on retry.
- Do not scrape protected surfaces without user-approved access.
- Do not treat answer order as stable without timestamp and surface metadata.
