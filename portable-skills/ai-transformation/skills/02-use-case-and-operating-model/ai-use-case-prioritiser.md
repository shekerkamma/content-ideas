---
name: ai-use-case-prioritiser
description: Scores and ranks AI use cases across business value, feasibility, data readiness, and strategic fit to produce a prioritised roadmap. Use after /ai-maturity-assessment when a long list of potential use cases must be narrowed to a funded portfolio.
---

# AI Use Case Prioritiser

## When To Use

Use when the organisation has generated a list of potential AI use cases (from workshops, benchmarking, or competitor analysis) and needs to decide which to fund, sequence, and resource. A common failure mode is pursuing too many use cases simultaneously — this framework produces a defended prioritisation that can survive executive challenge.

## Consulting Approach

Accenture's use case prioritisation uses a two-axis framework: Value (financial and strategic impact) versus Feasibility (data readiness, technical complexity, change required). The best use cases score high on both. The trap is over-investing in high-value but low-feasibility use cases that become multi-year data programmes before any AI runs. Sequence quick wins to build organisational confidence and fund the harder plays.

## Workflow

1. Collect the long list of candidate use cases — typically 15–40 from workshops and benchmarking.
2. Score each use case on Value (1–5): financial impact, strategic differentiation, customer/employee experience uplift.
3. Score each use case on Feasibility (1–5): data readiness, technical complexity, change management burden, vendor maturity.
4. Plot on a 2×2 Value × Feasibility matrix.
5. Apply strategic filters: regulatory constraints, dependencies, executive sponsorship, portfolio balance.
6. Produce a prioritised portfolio: Wave 1 (Quick Wins), Wave 2 (Strategic Bets), Wave 3 (Future Plays), Parking Lot.

## Output Format

```markdown
# AI Use Case Prioritiser — [Organisation / Scope]
**Date:** [YYYY-MM-DD]  **Long list size:** [n]

## Scoring Register
| # | Use Case | Domain | Value Score (1–5) | Feasibility Score (1–5) | Combined | Data Status | Sponsor | Notes |
|---|---|---|---|---|---|---|---|---|

## 2×2 Portfolio Map
```
              Feasibility →
              Low (1–2)        High (3–5)
Value  High | STRATEGIC BETS | QUICK WINS
(3–5)       |                |
       Low  | PARKING LOT    | INCREMENTAL
(1–2)       |                |
```
[List use case IDs in each quadrant.]

## Prioritised Portfolio

### Wave 1 — Quick Wins (deliver in 0–6 months)
| Use Case | Value | Feasibility | Expected Outcome | Owner |
|---|---|---|---|---|

### Wave 2 — Strategic Bets (6–18 months, data/platform investment required)
| Use Case | Value | Feasibility | Dependency | Owner |
|---|---|---|---|---|

### Wave 3 — Future Plays (18+ months or pending maturity)
| Use Case | Value | Feasibility | Gate Condition |
|---|---|---|---|

### Parking Lot (descoped — reason given)
| Use Case | Reason for Deferral |
|---|---|

## Portfolio Balance Check
| Dimension | Wave 1 | Wave 2 | Wave 3 |
|---|---|---|---|
| Cost reduction use cases | | | |
| Revenue / growth use cases | | | |
| Customer experience use cases | | | |
| Employee productivity use cases | | | |

## Recommended Next Step
[Which Wave 1 use cases to mobilise first, and what is needed to begin.]
```

## Quality Bar

- Scores must be justified with at least one evidence point per use case — not team gut feel.
- Wave 1 must contain at least one use case that can show value within 90 days.
- Strategic Bets must have a named data or platform dependency and a resolution path.
- Parking Lot entries must be documented with a reason — do not silently drop use cases.
