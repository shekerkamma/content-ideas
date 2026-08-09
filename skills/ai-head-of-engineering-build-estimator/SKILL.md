---
name: ai-head-of-engineering-build-estimator
description: Use when someone wants the estimation step of the AI Head of Engineering flow, or asks for hours, dollars, and risk for each scoped feature.
metadata:
  legacy-frontmatter: 'name: ai-head-of-engineering-build-estimator

    description: Use when someone wants the estimation step of the AI Head of Engineering flow, or asks for hours, dollars, and risk for each scoped feature.

    argument-hint: [scope] [team] [confidence-target]'
---

# Build Estimator

Estimate what the scoped build really costs in hours and dollars.

## Inputs

- Final scope
- Team shape
- Confidence target

## Process

1. Estimate each feature in a low/high hour range.
2. Convert hours to dollars at the blended rate.
3. Break each feature into frontend, backend, integration, testing, and polish.
4. List three risks that could blow the estimate.
5. Roll up totals and flag cuts if the plan exceeds capacity.
6. Save the result as `05-build-estimator.md`.

## Output

- Per-feature hour estimate
- Per-feature dollar estimate
- Confidence rating
- Risk list
- Roll-up total and capacity check

## Dependencies

- `04-build-vs-buy.md`
- `skills/ai-head-of-engineering/references/shared-templates.md`
- External research when live vendor behavior changes the estimate

## Skill Relationships

### Category
Business Automation

### Relationships
| Pattern | What it means here | Handoff artifact |
|---|---|---|
| Sequential | Feeds the AI fit validator and roadmap | `04-build-vs-buy.md` -> `05-build-estimator.md` -> `06-ai-fit.md` |
| Amplifier | Can be improved by research and analysis skills | estimation notes |
| Domain cluster | One member of the AI Head of Engineering family | `runs/ai-head-of-engineering/...` |

### Host compatibility
Shared. Use the same hour/dollar breakdown format everywhere.

## Gotchas

- Do not estimate the happy path only.
- Do not ignore auth, payments, and webhooks tax.
- Do not ship a plan that exceeds 160 hours without calling out the cuts needed.

