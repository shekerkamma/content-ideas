---
name: hypercare-plan
description: Defines the post-go-live stabilisation period: support model, escalation paths, issue triage, and exit criteria for returning to BAU. Use in the final delivery phase, 2–4 weeks before cutover.
---

# Hypercare Plan

## When To Use

Use in the 2–4 weeks before go-live to define the support structure for the stabilisation period immediately after cutover. Hypercare without a defined exit criteria becomes permanent — the project team never leaves, BAU ownership is never transferred, and the organisation never internalises operational responsibility.

## Consulting Approach

Hypercare is a time-bounded, intensive support period — not an extended project phase. Its purpose is to stabilise the solution, transfer knowledge to BAU support, and resolve the issues that always emerge in the first weeks of live operation. A hypercare plan must answer three questions: who does a user call when something breaks, how quickly will it be fixed, and how will we know when we no longer need hypercare?

## Workflow

1. Define the hypercare window: start date (go-live), end date (typically 4–8 weeks), and exit criteria.
2. Design the support model: Level 1 (first contact), Level 2 (programme team), Level 3 (vendor/technical escalation).
3. Define issue triage categories: Critical (system down / data loss), High (major process blocked), Medium (workaround available), Low (cosmetic or minor).
4. Define SLAs per triage category and name the escalation owner for Critical and High issues.
5. Plan the knowledge transfer schedule: what the BAU support team must know before the programme team exits.
6. Define exit criteria: the specific conditions under which hypercare ends and BAU owns the solution.

## Output Format

```markdown
# Hypercare Plan — [Programme Name]
**Go-Live Date:** [YYYY-MM-DD]  **Hypercare End (Target):** [YYYY-MM-DD]

## Support Model
| Level | Role | Scope | Contact Method | Coverage Hours |
|---|---|---|---|---|
| L1 | | | | |
| L2 | | | | |
| L3 | | | | |

## Issue Triage & SLAs
| Category | Definition | Response SLA | Resolution SLA | Escalation Owner |
|---|---|---|---|---|
| Critical | | | | |
| High | | | | |
| Medium | | | | |
| Low | | | | |

## Escalation Path
[Who is called if an issue is not resolved within SLA? Name individuals, not teams.]

## Knowledge Transfer Schedule
| Topic | From (Programme) | To (BAU) | Method | Date | Sign-Off |
|---|---|---|---|---|---|

## Issue Tracker
| ID | Date | Description | Category | Owner | Status | Resolution Date |
|---|---|---|---|---|---|---|

## Hypercare Exit Criteria
| Criterion | Target | Actual | Met? |
|---|---|---|---|
| Critical / High issues open | 0 | | |
| L1 resolution rate | ≥ 80% | | |
| BAU team trained and signed off | 100% | | |
| Adoption rate | ≥ [target] | | |
| [Programme-specific criterion] | | | |

**Hypercare Exit Decision:** [Go to BAU / Extend — with named reason and new date]
```

## Quality Bar

- Exit criteria must be defined before go-live, not negotiated at the end of hypercare.
- Every SLA must have a named escalation owner — "the programme team" is not an owner.
- Knowledge transfer must be signed off by the BAU recipient, not declared complete by the programme team.
- If hypercare is extended beyond the original window, the reason must be documented against a specific unmet exit criterion.
