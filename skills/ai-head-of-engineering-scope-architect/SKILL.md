---
name: ai-head-of-engineering-scope-architect
description: Use when someone wants the 30-day scope spec step of the AI Head of Engineering flow, or asks for in-scope, out-of-scope, milestones, and Friday decisions.
metadata:
  legacy-frontmatter: 'name: ai-head-of-engineering-scope-architect

    description: Use when someone wants the 30-day scope spec step of the AI Head of Engineering flow, or asks for in-scope, out-of-scope, milestones, and Friday decisions.

    argument-hint: [mvp-statement] [kept-features] [constraints]'
---

# 30-Day Scope Architect

Turn the kept scope into a short build contract the team can execute against.

## Inputs

- MVP statement from Scope Killer
- Kept features
- Hard constraints

## Process

1. Convert the MVP into a 1.5-2 page scope spec.
2. Separate `IN SCOPE` from `OUT OF SCOPE` with explicit boundaries.
3. Define weekly milestones and Friday decisions.
4. Write assumptions and a testable definition of done.
5. Save the result as `02-scope-architect.md`.

## Output

- In-scope and out-of-scope lists
- Weekly milestones
- Decisions owed by Friday
- Assumptions
- Definition of done

## Dependencies

- `01-scope-killer.md`
- `skills/ai-head-of-engineering/references/shared-templates.md`

## Skill Relationships

### Category
Business Automation

### Relationships
| Pattern | What it means here | Handoff artifact |
|---|---|---|
| Sequential | Consumes the scope cut result and feeds stack choice | `01-scope-killer.md` -> `02-scope-architect.md` -> `03-stack-picker.md` |
| Domain cluster | One member of the AI Head of Engineering family | `runs/ai-head-of-engineering/...` |

### Host compatibility
Shared. Use the same artifact names in Claude Code, Codex/OpenAI, and OpenHands.

## Gotchas

- Do not leave the definition of done vague.
- Do not hide assumptions about auth, design, Stripe, or team capacity.
- Do not let v1.1 ideas sneak back into scope.

