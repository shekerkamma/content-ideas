---
name: stage-gate-review
description: Conducts a structured phase-end review: assesses exit criteria, produces a Go/No-Go decision with conditions, and captures lessons for the next phase. Use at the end of every delivery phase before committing resources to the next.
---

# Stage Gate Review

## When To Use

Use at the end of every defined delivery phase (Foundation, Core, Scale, or equivalent). The stage gate is the programme's primary Go/No-Go decision point. Skipping it under schedule pressure is the single most common cause of late-phase failure — issues that could have been corrected at the gate become blockers at go-live.

## Consulting Approach

PRINCE2 defines stage boundaries as mandatory management decision points, not optional reviews. A stage gate has three possible outcomes: Go (proceed as planned), Go with conditions (proceed with named remediation actions and a named accountable), or No-Go (pause or re-plan). "Go with reservations" without named conditions is a deferred No-Go and should be treated as one.

## Workflow

1. Assemble the stage gate pack: delivery status vs. plan, RAID log update, benefits progress, budget actuals vs. forecast, quality metrics, open items.
2. Assess exit criteria for the completed phase: define which criteria are met, partially met, or not met.
3. Review RAID log: escalate any newly Red items before the gate decision.
4. Assess readiness for the next phase: are entry criteria for the next phase met?
5. Produce the gate decision: Go / Go with conditions / No-Go.
6. Capture lessons: what worked, what didn't, what must change in the next phase.

## Output Format

```markdown
# Stage Gate Review — Phase [Name]
**Programme:** [Name]  **Date:** [YYYY-MM-DD]  **Gate Decision:** [Go / Go with Conditions / No-Go]

## Phase Summary
[One paragraph: what was planned, what was delivered, key variances.]

## Exit Criteria Assessment
| Criterion | Status (Met / Partial / Not Met) | Evidence | Owner of Gap |
|---|---|---|---|

## RAID Highlights
[Top 3 risks/issues entering the next phase. New Red items flagged.]

## Budget & Schedule
| Dimension | Plan | Actual | Variance | Forecast to Complete |
|---|---|---|---|---|

## Gate Decision
**Decision:** [Go / Go with Conditions / No-Go]
**Rationale:** [One paragraph.]

## Conditions (if applicable)
| Condition | Owner | Completion Date | Consequence if Not Met |
|---|---|---|---|

## Lessons Captured
| What Worked | What Didn't | Action for Next Phase | Owner |
|---|---|---|---|

## Next Phase Entry Criteria
[Confirm entry criteria for the next phase are met or state what is outstanding.]
```

## Quality Bar

- Exit criteria must be defined before the phase begins, not at the review.
- A "Go with conditions" decision must name a consequence for each unmet condition — not "to be resolved."
- Lessons must result in at least one named change to the next phase plan.
- Budget and schedule variance must be explained, not just reported.
