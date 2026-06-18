# Operating Model Design — Prism Analytics

## Strategic Requirement
The operating model must enable Prism to execute three simultaneous imperatives over the next 12–18 months: (1) compress the LLM interface launch from 6 to 4 months without sacrificing quality, (2) run a focused new logo sprint targeting 15–20 wins in the Tier 1 bank and insurance segments, and (3) manage burn to extend runway while keeping the M&A parallel track credible. The current model — built for steady-state product development and a broad horizontal go-to-market — is not designed for this level of focused, time-pressured execution.

## Capability Model
| Capability | Current State | Required State | Gap |
|---|---|---|---|
| AI product development and delivery velocity | 90 engineers split 60/30/10 across platform/LLM/infra; LLM team is 27 engineers on a 6-month timeline; limited design partner feedback loop | 4-month compressed LLM delivery with 6 enterprise design partners providing weekly feedback; dedicated product-engineering squad with a single accountable owner | LLM team lacks a dedicated product manager with compliance domain depth; no structured design partner program; no "launch readiness" gate process |
| Vertical-specialized sales execution | Generalist enterprise AE model; 8–14 month cycles across all verticals; no dedicated vertical coverage for insurance; win rate 31% | Vertical-aligned AE pods (Tier 1 banks, Regional banks, Insurance) with vertical-specific ROI models, reference stories, and competitive playbooks | Insurance vertical has no dedicated coverage; no ACV floor governance; competitive playbooks for Clearwater are ad hoc; no formal win/loss review process |
| Customer success and expansion | CS team manages full install base reactively; LLM upsell motion not yet designed; no lighthouse account program | Proactive expansion motion: lighthouse account program (3 Tier 1, 2 Insurance); LLM Intelligence tier onboarding playbook; health scoring for churn-risk regional bank accounts | No expansion playbook exists; CS is reactive; no health scoring below $250K ACV; no documented LLM onboarding process |
| Regulatory intelligence and compliance R&D | Updates driven reactively by customer support tickets and annual regulatory calendars | Proactive regulatory monitoring function: 60-day advance notice on Basel IV, DORA, CECL updates; automated product update scheduling | No dedicated regulatory affairs function; engineers discover regulatory changes through customer escalations; 2 regulatory update delays in FY2025 created churn risk |
| M&A readiness and investor relations | Series C investor relations are standard reporting; no M&A process infrastructure | Clean financial model, data room, CIM narrative, and banker relationship ready to activate within 60 days if board triggers M&A process | No data room exists; no CIM; CFO bandwidth is fully consumed by board reporting and budget management |

## Target Model
| Element | Recommendation | Rationale |
|---|---|---|
| Engineering structure | Reorganize from functional teams to three outcome-based squads: LLM Intelligence Squad (27 engineers + 3 platform engineers temporarily, 1 PM, 1 compliance domain expert), Compliance Engine Squad (remaining platform engineers maintaining and extending regulatory modules), and Infrastructure Squad (current 9 infra engineers) | Current team structure distributes attention; LLM launch requires a focused, accountable squad with clear OKRs and weekly milestone reviews through month 4 |
| Go-to-market structure | Shift from generalist AE model to three vertical pods: Tier 1 Banking Pod (3 AEs + 1 SE + 1 CSM), Insurance Pod (2 AEs + 1 SE + 1 CSM, newly resourced from wealth management redeployment), Regional Bank Pod (3 AEs + 2 CSMs focused on retention and $200K+ upsell only) | Vertical alignment enables faster deal cycles, better reference-ability, and clearer competitive positioning; insurance pod is currently understaffed for the segment's upside |
| Pricing and packaging governance | Establish a deal desk function (VP Sales + Finance + 1 deal desk analyst) with a 48-hour SLA on non-standard deals; maximum 12% discount without VP approval; 15% requires CEO sign-off | Current discount leakage is unmanaged; deal desk prevents margin erosion without slowing deal velocity |
| Product launch process | Implement a 5-gate launch readiness process for the LLM interface: (1) design partner NPS ≥40, (2) accuracy benchmarking on 3 regulatory modules, (3) security and data privacy review, (4) CS onboarding playbook complete, (5) sales enablement kit delivered | No formal launch process currently; risk of rushing a compliance product to market before it is enterprise-grade, which would damage Prism's regulatory credibility |
| M&A readiness function | Assign CFO 20% of bandwidth to M&A readiness; engage a financial advisor in month 1 for a preliminary buyer landscape assessment; build a data room skeleton by month 3 | Board has explicitly stated exit as a valid path; being unprepared for a buyer conversation is a risk at 18 months of runway |

## Decision Rights
| Decision | Owner | Contributors | Governance |
|---|---|---|---|
| LLM interface launch go/no-go | CEO + CPO | CTO, Head of Design Partners, VP Customer Success | Monthly launch readiness review against 5-gate checklist; final go/no-go at week 14 |
| ACV floor and deal discount approval | VP Sales | CFO, CEO (for >$500K deals) | Deal desk weekly review; quarterly pricing realization report to board |
| Engineering squad resource allocation | CTO | CPO, VP Engineering, squad leads | Bi-weekly sprint review; reallocation requests require CEO approval if >10 FTEs |
| M&A process activation | Board (majority vote) | CEO, CFO, financial advisor | Quarterly board review of M&A vs. continue triggers; CFO presents data room readiness update |
| New vertical or segment investment | CEO | VP Sales, CFO, CPO | Annual planning process; mid-year reallocation requires CFO sign-off |

## Transition Plan
**Phase 1 (Months 1–2): Reorganize and mobilize.** Announce the three engineering squads; assign squad leads and single-threaded PMs. Redeploy 2 AEs from wealth management to insurance. Onboard 6 design partner accounts for LLM beta. Install deal desk governance. Communicate the 4-month LLM launch commitment to the all-hands with weekly milestone visibility.

**Phase 2 (Months 3–4): Deliver and launch.** LLM Intelligence Squad delivers against 5-gate checklist. Insurance pod closes first 2 logos. Tier 1 pod runs lighthouse onboarding with 3 accounts. CFO completes preliminary data room build. Win/loss analysis findings shared with board.

**Phase 3 (Months 5–10): Scale and decide.** New logo sprint runs with AI-first positioning. NRR expansion motion activates across LLM Intelligence tier renewals. At month 6, board reviews ARR trajectory vs. $55M checkpoint — decide on M&A process activation or continued independent execution. At month 10, review real-time replatforming business case.

**Transition risks:**
- Engineering squad reorg may slow platform maintenance velocity for 6–8 weeks; communicate to customers with a service continuity commitment.
- Insurance pod ramp takes 90 days; first logos unlikely before month 5.
- Deal desk governance will create initial friction with senior AEs accustomed to CEO-level deal exceptions; requires active CEO sponsorship in month 1.
