---
name: benefits-register
description: Creates a structured benefits ledger that links business case commitments to measurable outcomes, baseline values, owners, and measurement schedules. Use after /business-case-builder to make promised benefits trackable and owned.
---

# Benefits Register

## When To Use

Use immediately after the business case is approved to lock in the baseline and measurement contract for every benefit that was used to justify the investment. Benefits registers built after go-live cannot establish credible baselines. A business case that cannot be linked to a benefits register should not be approved.

## Consulting Approach

MSP (Managing Successful Programmes) treats benefits management as a programme discipline, not a finance function. Benefits are owned by business change managers, not project managers — the person accountable for the benefit must be in a position to drive the organisational change that realises it. A benefit with no owner is a forecast, not a commitment.

## Workflow

1. Extract every claimed benefit from the business case (financial and non-financial).
2. For each benefit, establish the baseline: what is the current state metric that the benefit will improve?
3. Define the measurement method: data source, calculation, frequency.
4. Assign an operational owner — the role accountable for realising the benefit post go-live.
5. Set intermediate milestones: expected benefit trajectory at 30, 90, 180 days.
6. Define the disbenefits: what negative consequences are accepted as part of achieving the benefit?

## Output Format

```markdown
# Benefits Register — [Programme Name]
**Business Case Approved:** [YYYY-MM-DD]  **Go-Live Target:** [YYYY-MM-DD]

## Benefits Ledger
| ID | Benefit Name | Type (Financial / Operational / Strategic) | Business Case Value | Baseline | Measurement Method | Data Source | Owner | 30-Day Target | 90-Day Target | 180-Day Target | Full Realisation Date |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Benefit Deep-Dives
[For each benefit with a value ≥ 10% of total programme value:]

### [Benefit Name]
- **Claim from business case:** [Exact statement]
- **Baseline:** [Current state metric, date measured, source]
- **Realisation mechanism:** [What has to change in the business to deliver this?]
- **Owner:** [Named role/individual]
- **Risk to realisation:** [What could prevent this benefit from materialising?]
- **Dependency:** [Which programme component must be live for this benefit to accrue?]

## Disbenefits Register
| Disbenefit | Affected Group | Magnitude | Mitigation | Owner |
|---|---|---|---|---|

## Measurement Calendar
| Benefit ID | Measurement Dates | Reporting Recipient | Escalation Threshold |
|---|---|---|---|
```

## Quality Bar

- Every benefit must have a baseline established before go-live — post hoc baselines cannot be verified.
- Benefit owners must be operational leaders, not programme managers or finance leads.
- Financial benefits must specify whether they are cost avoidance, cost reduction, or revenue uplift — these have different tracking methods.
- Disbenefits must be registered — a programme that claims only upsides is not credible.
