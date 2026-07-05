---
name: ai-head-of-engineering-build-vs-buy-auditor
description: Use when someone wants the build-vs-buy decision step of the AI Head of Engineering flow, or asks whether a feature should be built, bought, or hybrid.
argument-hint: [feature-list] [team-capacity] [revenue-plan]
---

# Build vs Buy Auditor

Decide where custom code adds moat and where commodity software should stay bought.

## Inputs

- Feature list
- Team capacity
- Rough 3-year revenue plan

## Process

1. Evaluate each feature as `BUILD`, `BUY`, or `HYBRID`.
2. Compare 3-year cost, data ownership, ship time, maintenance burden, and switching cost.
3. Flag expensive integrations and hidden lock-in.
4. Save the result as `04-build-vs-buy.md`.

## Output

- Per-feature recommendation
- Option table for build, buy, and hybrid
- 3-year cost math
- Integration burden callouts

## Dependencies

- `03-stack-picker.md`
- `skills/ai-head-of-engineering/references/shared-templates.md`
- External research when vendor pricing or current product capability matters

## Skill Relationships

### Category
Business Automation

### Relationships
| Pattern | What it means here | Handoff artifact |
|---|---|---|
| Sequential | Consumes the scoped feature list and feeds estimation | `03-stack-picker.md` -> `04-build-vs-buy.md` -> `05-build-estimator.md` |
| Amplifier | Can be improved by research and analysis skills | research notes / comparison table |
| Domain cluster | One member of the AI Head of Engineering family | `runs/ai-head-of-engineering/...` |

### Host compatibility
Shared. Prefer You.com search/livecrawl or equivalent current web research when the choice depends on live vendor facts.

## Gotchas

- Do not call something cheap if it takes weeks to integrate.
- Do not ignore data ownership and switching costs.
- Do not rebuild commodity primitives unless the integration burden is worse than the build.

