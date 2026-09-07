---
name: post-implementation-review
description: Structured retrospective that compares delivered outcomes against the business case, captures root causes of variance, and produces reusable lessons. Use 90 days after go-live or at programme closure.
---

# Post-Implementation Review

## When To Use

Use 90 days after go-live (when enough operational data exists to measure benefits) and again at formal programme closure. A post-implementation review conducted at go-live is a project completion review, not a value assessment — the two should not be confused. If benefits realisation is on track, the review validates the approach; if it is off track, the review produces the recovery plan.

## Consulting Approach

The purpose of a post-implementation review is not to assign credit or blame — it is to produce reusable intelligence. Every major variance (positive or negative) has a root cause that can inform future programme design. A review that concludes "we should communicate more next time" without naming the specific failure mode in communications is not useful.

## Workflow

1. Pull the benefits register and compare actual metrics at 90 days against the 90-day targets set at baseline.
2. Assess delivery: what was committed in the business case vs. what was delivered (scope, timeline, cost).
3. For each significant variance (>20% off target), conduct a five-why root cause analysis.
4. Review the adoption metrics: are users using the solution as designed? Where is adoption below target?
5. Identify 3–5 lessons that are specific enough to change how the next programme is designed or governed.
6. Produce a forward view: what actions are needed to close remaining benefit gaps?

## Output Format

```markdown
# Post-Implementation Review — [Programme Name]
**Review Date:** [YYYY-MM-DD]  **Go-Live Date:** [YYYY-MM-DD]  **Days Post Go-Live:** [n]

## Executive Summary
[One paragraph: overall assessment — on track / partially on track / off track — and the key factor driving the outcome.]

## Benefits Scorecard
| Benefit | Business Case Target | 90-Day Target | Actual | Variance | Trend |
|---|---|---|---|---|---|

## Delivery Assessment
| Dimension | Plan | Actual | Variance |
|---|---|---|---|
| Scope | | | |
| Timeline | | | |
| Cost | | | |
| Quality | | | |

## Variance Root Causes
[For each variance > 20%:]

### [Benefit / Dimension]
- **Variance:** [What the gap is]
- **Root cause (five-why):** [Chain of causation]
- **Was this foreseeable?** [Yes / No — if yes, what should have caught it?]
- **Recovery action:** [What will close the gap, who owns it, by when]

## Adoption Status
| Stakeholder Group | Target Usage | Actual Usage | Gap | Root Cause |
|---|---|---|---|---|

## Lessons Register
| Lesson | Category | Specific Change for Next Programme | Owner to Embed |
|---|---|---|---|

## Forward Actions
| Action | Owner | Target Date | Expected Impact |
|---|---|---|---|
```

## Quality Bar

- Benefits comparison must use actual operational data, not programme team estimates.
- Root causes must reach the structural or process level — "poor communication" is a symptom, not a root cause.
- Lessons must be specific enough that a programme manager reading them 12 months later could act on them without additional context.
- A forward actions table is mandatory if any benefit is more than 20% below target.
