# Strategic Risk Register — Prism Analytics

## Strategy Under Review

Accelerate the LLM natural language query interface by 2 months (targeting GA in Q4 2026), reposition Prism Analytics as "AI-first compliance intelligence," deploy 4 additional sales engineers to convert the $28M qualified pipeline, and defer full real-time replatforming until ARR reaches $65M. Total incremental investment: $3.2M. Target outcome: $62M ARR by end of FY2026, win rate restored to 42%, NRR back above 110%.

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Owner | Trigger |
|---|---|---|---|---|---|
| LLM interface ships late or with material defects — technical debt in Python/SQL batch layer creates integration friction, delaying GA beyond Q4 2026 | High | Critical — delays competitive repositioning by 1+ quarter; pipeline stalls while $28M in deals continue to age | Dedicate 18 engineers exclusively to LLM layer (currently 27 assigned); introduce weekly QA gates vs. feature milestones; establish a 6-week code-freeze buffer before target GA | CTO | Two or more sprint slippages in June–August 2026; LLM query accuracy below 85% threshold in internal UAT |
| Clearwater Analytics accelerates AI feature announcements to neutralize "AI-first" repositioning before Prism reaches GA | Medium–High | High — removes differentiation before it is established; could deepen win-rate decline from 31% to sub-25% | Soft-launch LLM interface to 10–15 design partners (Tier 1 banks) by September 2026; generate reference customers and case studies before full market announcement | CEO + VP Sales | Clearwater public product announcement referencing natural language compliance queries; loss of 2+ Tier 1 deals citing AI gap |
| NRR continues to erode during the 6-month pre-GA window — churn among regional banks outpaces new logo wins | Medium | High — NRR at 104% leaves no margin for incremental churn; drop below 100% reframes strategic narrative from "turnaround" to "distress" | Assign dedicated CSM coverage to the 30 regional bank accounts representing >60% of gross churn risk; offer 12-month rate locks in exchange for early LLM design partner participation | Chief Customer Officer | Monthly gross churn exceeds 0.6% for two consecutive months; any Tier 1 bank issues formal notice of non-renewal |
| $3.2M investment is insufficient to achieve 2-month acceleration — engineering capacity constraints (60% of 90 engineers on platform work) require reallocation that slows platform stability | Medium | Medium — runway of 18 months at $2.1M/mo burn is non-negotiable; cost overrun compresses options without Board flexibility | Gate $3.2M in two tranches: $1.8M at kickoff (engineering + 2 SEs), $1.4M upon hitting September LLM milestone; CFO holds approval on tranche 2 | CFO | Monthly burn exceeds $2.5M for any single month; engineering velocity (story points completed vs. planned) falls below 75% for two consecutive sprints |
| Regulatory environment shifts — Basel IV implementation timelines accelerate or CECL guidance is revised, obsoleting current compliance reporting modules before LLM layer is customer-ready | Low–Medium | Medium — 41% of revenue from regional banks highly sensitive to compliance reporting accuracy; any regulatory gap triggers competitive review | Retain outside regulatory counsel (one FTE equivalent); maintain a 90-day regulatory watch cadence with product; flag material changes to product roadmap within 30 days of guidance publication | Chief Compliance Counsel + CPO | OCC, Fed Reserve, or FASB issues material interpretive guidance affecting Basel IV or CECL reporting requirements |

## Highest-Risk Assumptions

1. **LLM accuracy is sufficient for compliance use cases at GA.** The strategy assumes that the natural language query interface will meet the accuracy and auditability standards required by bank compliance officers. Regulatory-grade financial analytics tolerates near-zero error rates; general LLM performance benchmarks do not apply. This assumption must be validated through structured UAT with at least 3 bank compliance teams before any sales commitment.

2. **Win-rate recovery is primarily an AI perception gap, not a product gap.** The hypothesis is that the 16-point win-rate decline (47% → 31%) is driven by Clearwater's AI-native positioning rather than functional deficiencies in Prism's core analytics. If win/loss analysis reveals that customers are switching for real-time data capabilities — not just AI UX — the LLM investment addresses the wrong problem and replatforming becomes unavoidable sooner.

3. **18-month runway is a hard floor, not a buffer.** The strategy operates at $2.1M/mo burn with 18 months of runway. Any combination of revenue shortfall and cost overrun that compresses runway below 12 months will force the Board toward a strategic sale before the LLM strategy has time to prove itself. The strategy has no explicit contingency for a capital raise.

4. **The $28M pipeline converts at ≥20% within FY2026.** The target ARR of $62M requires approximately $14M in net new ARR — implying $14–18M in new bookings given expansion dynamics. Converting 50–65% of the qualified pipeline assumes no further win-rate deterioration during the pre-GA period.

## Contingency Moves

**If the LLM interface slips beyond Q4 2026:**
- Immediately activate a "NLP-powered compliance copilot" limited release to design partners only, positioning the partial capability as exclusive early access rather than a delay.
- Redirect 2 of the 4 new sales engineers to defending the renewal base rather than new logo pursuit.

**If Clearwater announces a competing AI feature before Prism's GA:**
- Accelerate the design-partner announcement; release anonymized benchmark data showing Prism's compliance accuracy advantages over AI-native competitors (position accuracy and auditability vs. generative fluency).
- Brief the top 20 accounts personally before the public response.

**If NRR falls below 100% in any single quarter:**
- Trigger an emergency churn war-room led by the CEO; personally engage the three largest at-risk accounts.
- Pause new-logo sales engineer deployment and redirect headcount to retention.

**If the Board moves toward strategic sale before ARR reaches $65M:**
- Prepare a data room structured around the LLM-differentiated vision and $28M pipeline; position Clearwater, SS&C, or Moody's as natural acquirers; target deal at $180–220M (4–5x forward ARR) rather than a distressed exit.
