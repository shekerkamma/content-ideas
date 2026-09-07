---
name: delivery-risk-assessment
description: Identifies and scores delivery-specific risks — scope creep, integration failures, resource gaps, dependency slippage — producing a prioritised risk heat map and mitigation plan. Use at the start of each delivery phase and when the RAID log shows multiple Amber items converging.
---

# Delivery Risk Assessment

## When To Use

Use at the start of a delivery phase, at a stage gate, or when multiple RAID items are converging. Delivery risk assessment is distinct from strategic risk assessment — it focuses on what can go wrong during execution, not whether the strategy is right.

## Consulting Approach

Delivery risks cluster in five areas: scope (what is being built), integration (how components connect), resources (who is doing the work), dependencies (what the programme needs from outside), and change (whether the organisation can absorb what is being delivered). A risk that touches more than one area is a compound risk and should be treated as higher priority than its individual scores suggest.

## Workflow

1. Collect input from workstream leads, the RAID log, and the stage gate review (if one has occurred).
2. Identify risks in each of the five delivery risk categories.
3. Score each risk on probability (1–5) and impact (1–5); calculate exposure score (P × I).
4. Flag compound risks (those that span two or more categories).
5. Assign mitigation owner and define the mitigation action for all risks with exposure ≥ 12.
6. Produce a heat map and a prioritised mitigation plan.

## Output Format

```markdown
# Delivery Risk Assessment — [Programme / Phase]
**Date:** [YYYY-MM-DD]  **Phase:** [Name]

## Risk Register
| ID | Category | Description | Probability (1–5) | Impact (1–5) | Exposure | RAG | Compound? | Owner | Mitigation |
|---|---|---|---|---|---|---|---|---|---|

## Heat Map
```
         Impact →
         1    2    3    4    5
P  5  |  5   10   15   20   25
r  4  |  4    8   12   16   20
o  3  |  3    6    9   12   15
b  2  |  2    4    6    8   10
   1  |  1    2    3    4    5
```
[List which risk IDs fall in each cell.]

## Top 5 Risks (Exposure ≥ 12)
[For each: description, why this phase, mitigation, owner, residual exposure after mitigation.]

## Compound Risks
[Risks spanning multiple categories — these require cross-workstream owners.]

## Mitigation Prioritisation
| Risk ID | Mitigation Action | Owner | Target Date | Residual Exposure |
|---|---|---|---|---|
```

## Quality Bar

- Every risk with exposure ≥ 12 must have a named individual owner and a mitigation action — not "monitor."
- Compound risks must have a cross-workstream owner, not a single workstream lead.
- Probability and impact scores must be justified — a "5" on either dimension requires evidence, not intuition.
- Residual exposure after mitigation must be lower than pre-mitigation exposure; if not, escalate.
