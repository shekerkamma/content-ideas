# Business Case — Prism Analytics LLM Interface Acceleration ("AI-First Compliance Intelligence")

## Decision
Invest $1.8–2.2M to accelerate the LLM natural language query interface from a 6-month to a 4-month launch timeline; simultaneously execute a focused 15–20 new logo sprint using the AI-first compliance positioning. Defer the full real-time replatforming decision until ARR reaches $65M or 12 months elapse, whichever comes first.

## Economics Summary
| Metric | Downside | Base | Upside |
|---|---|---|---|
| New logos won in 6-month sprint (months 4–10) | 8 logos × $280K ACV = $2.2M ARR | 15 logos × $320K ACV = $4.8M ARR | 22 logos × $360K ACV = $7.9M ARR |
| Win rate recovery (from 31%) | 35% (modest narrative lift) | 42% (returns to 2-year-ago level) | 50% (AI-first repositioning resonates) |
| NRR uplift (LLM expansion at renewal) | 105% | 108% | 111% |
| Incremental ARR at month 12 | +$4.1M | +$8.3M | +$13.6M |
| ARR at month 12 | $52.1M | $56.3M | $61.6M |
| Burn impact (additional spend, months 1–4) | +$550K | +$450K (compressed timeline premium) | +$350K (fast execution, no rework) |
| Runway remaining at month 12 (current $37.8M cash) | 13 months | 16 months | 20 months |
| Exit multiple implied (4× ARR) | $208M | $225M | $246M |

## Value Drivers
| Driver | Assumption | Evidence | Sensitivity |
|---|---|---|---|
| Win rate recovery to 42% | AI-first narrative closes the Clearwater perception gap; LLM interface is table-stakes for 2026 RFPs | Clearwater growing at 55% on AI-native positioning; Prism's $1.2M loss cited AI gap as factor | ±5pp win rate = ±$2.1M ARR in the sprint window; high sensitivity |
| LLM expansion upsell at renewal | 35% of existing 140 clients upgrade to Intelligence tier (+$52K avg) | Comparable SaaS AI add-on attach rates of 28–40% at 6-month mark post-launch | If attach rate <20%, NRR holds at 104% with no improvement; moderate sensitivity |
| Compressed timeline (4 vs. 6 months) | 30 additional engineers redirected from platform maintenance to LLM delivery for 8 weeks | Engineering capacity exists: 30% of 90 engineers currently on LLM layer; CEO has authority to redirect | If timeline slips to 5 months, sprint window narrows; captures ~80% of base case ARR |
| Pipeline conversion ($28M qualified) | 15% incremental conversion lift from AI-first positioning in active pipeline | Pipeline at $28M with 8–14 month cycles; 10 deals likely to close in next 6 months regardless | Deals already at late stage convert independent of narrative; AI positioning helps mid-funnel deals |
| Real-time gap does not disqualify | T+1 latency acceptable for regulatory reporting use cases (not trading); majority of buyers are compliance officers, not quants | Basel III/IV and CECL reporting are not latency-sensitive; trading desks are not Prism's ICP | If Tier 1 banks with trading desk requirements dominate pipeline, gap persists; validate by deal-type breakdown |

## Cost and Investment
**Year 1 total investment: $2.05M**
- LLM interface compression premium (8-week engineering sprint overlay): $650K
- Go-to-market repositioning (messaging, sales enablement, event presence, analyst briefings — Gartner, Celent): $420K
- Incremental sales capacity (2 enterprise AEs targeting AI-first narrative + 1 solutions engineer): $580K fully loaded
- Customer success expansion (onboard LLM upsell motion at renewal, 2 additional CSMs): $400K

**No additional capex required.** LLM layer builds on existing Python/SQL infrastructure; streaming architecture deferred.

**Year 2 investment trigger:** If ARR reaches $65M by month 12, allocate $8–10M tranche toward real-time replatforming (phased, not big-bang). If ARR does not reach $65M, initiate M&A process instead of further platform investment.

## Risks
**Risk 1 — LLM interface quality is below enterprise bar at accelerated launch.** If beta NPS < 40 or enterprise pilots surface hallucination/accuracy issues in compliance reporting contexts, launch delay is mandatory. Mitigation: Gate launch on a 6-client design partner program with structured accuracy benchmarking; do not launch on marketing timeline alone.

**Risk 2 — Real-time gap resurfaces as a hard disqualifier in new RFPs.** If win/loss analysis shows real-time is cited in >40% of losses (vs. current estimate of ~25%), the LLM bridge thesis is weakened. Mitigation: Immediately scope a lightweight event-driven data ingest layer (not full replatform) achievable in 9 months at $4M to bridge to near-real-time (T+15min) as a stop-gap.

**Risk 3 — Burn exceeds 18-month runway before ARR inflects.** At current $2.1M/mo burn, Prism has $37.8M cash. Base case extends runway to 16 months; downside case to 13 months — uncomfortably close to a bridge round requirement. Mitigation: Simultaneously reduce non-essential discretionary spend by $300K/mo (travel, non-critical vendor contracts) without touching engineering headcount. Target $1.85M/mo effective burn.

**Risk 4 — Key engineering talent loss during repositioning.** Rapid context-switch from platform to LLM delivery risks attrition in platform engineers. Mitigation: Retention packages for the top 15 platform engineers; clear 12-month roadmap communication at an all-hands within 30 days of decision.

## Recommendation
**Proceed.** The base case delivers $8.3M incremental ARR at a $2.05M investment — a 4× gross revenue multiple in 12 months. The break-even threshold is only 8 new logos at current ACV, well below the base case of 15. The downside scenario (8 logos, 35% win rate) still improves the exit narrative and buys 3+ months of additional runway. The asymmetry favors acceleration. Begin the 6-client design partner program immediately; compress engineering delivery target to 4 months; brief the board on the M&A parallel track at the same board meeting.
