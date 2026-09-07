---
name: ai-head-of-engineering-30-day-build-roadmap
description: Use when someone wants the final roadmap step of the AI Head of Engineering flow, or asks for a 30-day sprint plan with Friday gates and rollback triggers.
metadata:
  legacy-frontmatter: 'name: ai-head-of-engineering-30-day-build-roadmap

    description: Use when someone wants the final roadmap step of the AI Head of Engineering flow, or asks for a 30-day sprint plan with Friday gates and rollback triggers.

    argument-hint: [scope] [capacity] [launch-date]'
---

# 30-Day Build Roadmap

Turn the final scope into a week-by-week build plan with real gates.

## Inputs

- Final scope
- Team capacity
- Hard launch date

## Process

1. Map the four-week sprint plan.
2. Put Friday deadlines on every week.
3. Define what gets demoed each Friday.
4. Add rollback triggers and a minimum lovable product fallback.
5. Save the result as `09-roadmap.md`.

## Output

- Week-by-week roadmap
- Dependency map
- Friday demo plan
- Rollback plan
- Minimum lovable product fallback

## Dependencies

- `08-pre-launch-audit.md`
- `skills/ai-head-of-engineering/references/shared-templates.md`

## Skill Relationships

### Category
Business Automation

### Relationships
| Pattern | What it means here | Handoff artifact |
|---|---|---|
| Sequential | Final step in the planning chain | `08-pre-launch-audit.md` -> `09-roadmap.md` |
| Domain cluster | One member of the AI Head of Engineering family | `runs/ai-head-of-engineering/...` |

### Host compatibility
Shared. The roadmap should be readable and enforceable in Claude Code, Codex/OpenAI, and OpenHands.

## Gotchas

- Do not treat Friday as a loose milestone.
- Do not overpack Week 1.
- Do not keep a drifting roadmap alive if the critical path is already broken.

