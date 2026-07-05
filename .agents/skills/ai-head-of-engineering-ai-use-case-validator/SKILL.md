---
name: ai-head-of-engineering-ai-use-case-validator
description: "Use when someone wants the AI fit step of the AI Head of Engineering flow, or asks whether AI should power a feature and which pattern to use."
argument-hint: "[use-case] [volume] [failure-cost]"
---

# AI Use-Case Validator

Check whether AI belongs in the feature at all, and if so which pattern is defensible.

## Inputs

- AI use case
- Volume
- Failure cost

## Process

1. Score the use case across structure, verifiability, failure tolerance, cost, latency, and hallucination risk.
2. Choose the smallest viable AI pattern.
3. Recommend a model family and cost per 1,000 uses.
4. List failure modes and the minimum eval set.
5. Save the result as `06-ai-fit.md`.

## Output

- AI fit score
- Recommended pattern
- Model recommendation
- Failure modes
- Minimum evaluation set

## Dependencies

- `05-build-estimator.md`
- `skills/ai-head-of-engineering/references/shared-templates.md`
- External research for model pricing, latency, or capability checks

## Skill Relationships

### Category
Business Automation

### Relationships
| Pattern | What it means here | Handoff artifact |
|---|---|---|
| Sequential | Feeds the internal tool designer | `05-build-estimator.md` -> `06-ai-fit.md` -> `07-tool-designer.md` |
| Amplifier | Can be improved by research and analysis skills | eval notes / benchmark notes |
| Domain cluster | One member of the AI Head of Engineering family | `runs/ai-head-of-engineering/...` |

### Host compatibility
Shared. Prefer current research tooling when model or platform facts matter.

## Gotchas

- Do not recommend AI just because the feature sounds modern.
- Do not skip the rules-based alternative check.
- Do not ignore hallucination cost when the output reaches customers.
