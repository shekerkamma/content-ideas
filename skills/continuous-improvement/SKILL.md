---
name: continuous-improvement
description: 5 post-delivery consulting frameworks — operating rhythm design, quarterly performance review, CI backlog, capability maturity progression, and consulting exit strategy. Closes the loop after solution-delivery.
version: 1.0.0
triggers:
  - /continuous-improvement
  - /operating-rhythm-design
  - /performance-review
  - /continuous-improvement-backlog
  - /capability-maturity-progression
  - /exit-strategy
---

# continuous-improvement — 5 Post-Delivery Frameworks

## When To Use

Use after the hypercare period ends and the organisation transitions to BAU ownership. These skills close the loop between solution-delivery and the next strategy cycle — ensuring that what was built keeps improving and that the organisation does not revert to prior behaviours.

## The 5 Skills

### Domain 1 — Operations
| Trigger | When to Use |
|---|---|
| `/operating-rhythm-design` | End of hypercare — design the BAU governance and meeting cadence |
| `/performance-review` | Monthly / quarterly — KPI vs target, root-cause variances, corrective actions |

### Domain 2 — Improvement
| Trigger | When to Use |
|---|---|
| `/continuous-improvement-backlog` | Ongoing — capture, score, and sequence post-go-live enhancements |
| `/capability-maturity-progression` | Annual — assess maturity level, identify blockers, plan progression to next level |

### Domain 3 — Transition
| Trigger | When to Use |
|---|---|
| `/exit-strategy` | 4–6 weeks pre-exit — readiness criteria, knowledge transfer, retained advisory, sign-off |

## Chain Position

```
solution-delivery                      continuous-improvement
─────────────────────────────────────────────────────────────
/hypercare-plan (end)       →  /operating-rhythm-design
/post-implementation-review →  /performance-review (quarterly)
/benefits-register          →  /performance-review (benefits tracking)
                                /continuous-improvement-backlog (ongoing)
                                /capability-maturity-progression (annual)
                                /exit-strategy (before team exits)
                                       ↓
                              Back to strategy-consulting
                              /situation-assessment (next cycle)
```

## Dispatch Logic

1. Individual trigger (e.g. `/performance-review`) — read `skills/01-operations/performance-review.md` and execute inline.
2. Top-level with argument — same as above.
3. No argument — ask which domain (Operations / Improvement / Transition), then which skill, then execute.

**Execution**: Read skill `.md` from `~/.claude/skills/continuous-improvement/skills/<domain>/<skill>.md`, load its Workflow and Output Format, apply to user context. Do not invoke Skill tool — run inline.

## Chaining Out

- `/performance-review` findings → `/growth-barriers` (strategy-consulting) if performance is structurally below target
- `/capability-maturity-progression` → `/transformation-roadmap` (strategy-consulting) for the next improvement wave
- `/exit-strategy` → `/engagement-closeout` (engagement-management) for the full commercial closeout
- Annual review → `/situation-assessment` (strategy-consulting) to restart the next engagement cycle
