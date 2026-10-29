---
name: continuous-improvement-backlog
description: Captures, scores, and sequences post-go-live enhancement requests and improvement ideas into a prioritised backlog with funding recommendations. Use as the improvement layer of the operating rhythm.
---

# Continuous Improvement Backlog

## When To Use

Use from go-live onwards as the mechanism for managing post-launch enhancement requests, operational improvements, and technical debt. Organisations that do not maintain a structured CI backlog either freeze their capability at go-live maturity (no improvements) or allow unconstrained enhancement requests that absorb all available capacity with no prioritisation.

## Consulting Approach

A CI backlog is governed differently from a project backlog. Items enter through defined intake channels (performance reviews, operational forums, user feedback, technology updates), are scored on value and effort, and are approved through the operating rhythm governance — not by whoever shouts loudest. The backlog has three horizons: quick wins (deliver within the current quarter), roadmap items (funded in the next planning cycle), and future consideration (not yet prioritised).

## Workflow

1. Define intake channels: where do improvement ideas come from? (operational forum issues, user feedback, performance review variances, technology roadmap changes, regulatory requirements).
2. Triage all items in the backlog against four criteria: Value (business impact), Urgency (time sensitivity), Effort (delivery complexity), and Risk (what happens if not done).
3. Score and rank items; assign to the three horizons.
4. Present the prioritised backlog to the performance review forum for funding approval.
5. For approved items: assign an owner, define success criteria, and set a delivery date.
6. Review and re-prioritise the full backlog quarterly.

## Output Format

```markdown
# Continuous Improvement Backlog — [Capability / Function]
**Last Updated:** [YYYY-MM-DD]  **Backlog Owner:** [Role]

## Intake Log (Unscored)
| ID | Date | Description | Source | Submitted By |
|---|---|---|---|---|

## Scored Backlog
| ID | Description | Value (1–5) | Urgency (1–5) | Effort (1–5, inv.) | Risk if Deferred (1–5) | Score | Horizon |
|---|---|---|---|---|---|---|---|

**Score = Value + Urgency + (6 - Effort) + Risk if Deferred**
**Horizon:** Quick Win · Roadmap · Future

## Horizon 1 — Quick Wins (current quarter)
| ID | Description | Owner | Effort (days) | Start Date | Completion Date | Success Measure |
|---|---|---|---|---|---|---|

## Horizon 2 — Roadmap (next planning cycle)
| ID | Description | Estimated Effort | Funding Required | Proposed Quarter | Dependency |
|---|---|---|---|---|---|

## Horizon 3 — Future Consideration
| ID | Description | Why Deferred | Review Date |
|---|---|---|---|

## Capacity Plan
| Resource | Available Capacity (days/quarter) | Committed to Quick Wins | Available for Roadmap |
|---|---|---|---|

## Funding Request (for Horizon 2)
[Summary of Horizon 2 items requiring investment approval at the next planning cycle, with business case for each.]
```

## Quality Bar

- Every item in the backlog must have a score — an unscored backlog defaults to FIFO, which is not a prioritisation method.
- Effort scores must be realistic — teams consistently underestimate effort for enhancement work.
- Horizon 3 items must have a review date — a future consideration list with no review date is a graveyard.
- Capacity must be explicitly reserved for CI work — if all capacity is consumed by BAU operations, the backlog is theoretical.
