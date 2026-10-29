---
name: ai-head-of-engineering-stack-picker
description: Use when someone wants the stack choice step of the AI Head of Engineering flow, or asks for framework, database, auth, payments, email, hosting, and analytics trade-offs.
metadata:
  legacy-frontmatter: 'name: ai-head-of-engineering-stack-picker

    description: Use when someone wants the stack choice step of the AI Head of Engineering flow, or asks for framework, database, auth, payments, email, hosting, and analytics trade-offs.

    argument-hint: [use-case] [team-experience] [cost-ceiling] [lock-in-tolerance]'
---

# Stack Picker

Choose the fastest stack the team can actually ship, with explicit trade-offs.

## Inputs

- Use case
- Team experience level
- Monthly cost ceiling
- Lock-in tolerance

## Process

1. Pick the stack layer by layer.
2. Provide the primary choice plus two alternatives.
3. Explain cost, ramp time, and lock-in for each layer.
4. Flag choices that add more than five days of ramp time.
5. Save the result as `03-stack-picker.md`.

## Output

- Frontend, backend, database, auth, payments, email, hosting, and analytics choices
- Two alternatives per layer
- Trade-off reasoning
- Ramp-time flags

## Dependencies

- `02-scope-architect.md`
- `skills/ai-head-of-engineering/references/shared-templates.md`

## Skill Relationships

### Category
Business Automation

### Relationships
| Pattern | What it means here | Handoff artifact |
|---|---|---|
| Sequential | Feeds the build-vs-buy and estimator steps | `02-scope-architect.md` -> `03-stack-picker.md` -> `04-build-vs-buy.md` |
| Domain cluster | One member of the AI Head of Engineering family | `runs/ai-head-of-engineering/...` |

### Host compatibility
Shared. Use host-neutral language for the stack recommendation and file outputs.

## Gotchas

- Do not optimize for benchmarks over ramp time.
- Do not understate vendor lock-in.
- Do not introduce a stack that adds real setup delay to a 30-day build without calling that out.

