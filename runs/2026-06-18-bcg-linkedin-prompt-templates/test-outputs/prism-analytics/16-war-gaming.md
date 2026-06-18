# Strategy War Game — Prism Analytics

## Strategy Under Test

Invest $3.2M to accelerate the LLM natural language query interface by 2 months, reposition Prism as "AI-first compliance intelligence," convert the $28M qualified pipeline with 4 new sales engineers, and defer real-time replatforming until ARR reaches $65M. Target: $62M ARR, 42% win rate, and NRR above 110% by end of FY2026.

## Scenarios

| Scenario | Trigger | Impact | Likelihood | Severity |
|---|---|---|---|---|
| Clearwater launches a compliance-specific NLP feature and markets it aggressively to regional banks before Prism's GA | Clearwater product announcement Q3 2026; direct outreach to Prism's top 40 regional bank accounts | "AI-first" repositioning neutralized before it lands; pipeline conversion rate stays at 31% or lower; $5–8M of the $28M pipeline at risk of closing to Clearwater | High | Critical — removes the primary source of win-rate recovery; strategy economics do not work at <35% win rate |
| LLM interface ships on time but fails compliance accuracy thresholds in customer UAT — bank risk officers reject it for production use | 2–3 early design partners report query errors or unauditable outputs; word spreads in bank compliance community | Design partner program collapses; repositioning story becomes a liability rather than an asset; Prism loses 2–4 Tier 1 accounts citing AI reliability concerns | Medium | Severe — trust damage in bank compliance is extremely slow to repair; could accelerate NRR decline to below 100% |
| Macro credit cycle worsens — regional banks freeze discretionary software spend in response to rising loan loss provisions | Fed signals additional rate holds; regional bank earnings calls cite OpEx tightening; 3+ banks defer or cancel renewals | Gross churn accelerates from 6% to 9–11%; NRR drops below 100%; runway shortens without revenue offset; Board pressure for strategic sale intensifies | Medium | High — approximately 41% of ARR is exposed to regional bank spend decisions |
| Bloomberg Terminal announces an AI-native compliance module bundled at no incremental cost for existing Terminal subscribers | Bloomberg press release; outreach to Prism enterprise accounts in Tier 1 banks | 32% of ARR from Tier 1 banks faces existential competitive pressure; Bloomberg can bundle compliance AI at effectively zero marginal cost vs. Prism's $343K ACV | Low–Medium | Catastrophic — Bloomberg has distribution, brand, and data access that Prism cannot match on pure features; forces immediate pivot or sale |
| Prism's real-time data gap becomes a hard disqualifier as banks upgrade their risk infrastructure to T+0 requirements | OCC or ECB guidance mandates intraday risk reporting; 2+ Tier 1 RFPs specify real-time streaming as a must-have | Prism cannot compete in any deal requiring real-time data; total addressable pipeline shrinks by 35–40%; $14–17M of the $28M pipeline is disqualified | Low–Medium | High — invalidates the "defer replatforming" decision and forces a capital raise or sale earlier than planned |

## Vulnerabilities

| Weak Point | Why It Matters | Mitigation |
|---|---|---|
| 6-month window between strategy commitment and GA — no competitive repositioning defense during this period | Prism will be actively selling an "AI-first" vision it cannot yet demonstrate; sophisticated buyers will delay decisions rather than commit; pipeline ages and deal quality deteriorates | Soft-launch LLM to 10 design partners by September 2026; create early access program with reference-able outcomes before full announcement; use existing product strengths (Basel IV depth, CECL accuracy) as bridge narrative |
| $343K ACV and 8–14 month sales cycle makes the math fragile — a few lost deals materially miss the $62M ARR target | At $343K ACV, missing the win-rate target by 5 points (~3 deals) costs $1M+ in ARR; missing by 10 points costs $2.5M+ | Use new sales engineers on the top 15 pipeline deals only; apply deal qualification rigor to eliminate low-probability opportunities before committing SE time |
| 74% gross margin is adequate but provides limited flexibility to discount competitively against Clearwater's well-funded balance sheet ($180M ARR, ~$300M+ in capital raised) | Clearwater can afford to win deals at negative economics; Prism's 18-month runway means it cannot match a price war | Compete on compliance depth and audit-trail integrity, not price; build a "compliance accuracy guarantee" that Clearwater's AI-native approach structurally cannot match |
| 90-engineer team is split: 60% platform (batch), 30% LLM, 10% infra — reallocation to accelerate LLM layer risks platform stability regression | Any platform downtime or data quality issues during the critical pre-GA period undermines the AI-first narrative before it launches | Freeze non-critical platform changes for 90 days; establish a platform SLA war room; define minimum acceptable platform quality before any engineer is redeployed to LLM layer |

## Response Playbook

| Signal | Response | Owner |
|---|---|---|
| Clearwater announces competing compliance NLP capability | Immediately brief top 20 accounts; release a "compliance accuracy benchmark" study positioning auditability vs. Clearwater's generative fluency; accelerate design partner NDA and early access offers | CEO + VP Sales — within 5 business days of announcement |
| Two or more sprint slippages push LLM GA past Q4 2026 | Trigger Tranche 2 hold (CFO); evaluate contractor augmentation for LLM layer (3–4 specialized ML engineers on 3-month contracts); present revised timeline and revised $62M ARR risk scenario to Board | CTO + CFO — within 48 hours of second slip |
| Monthly gross churn exceeds 0.7% (>$400K ARR lost in a single month) | Activate churn war-room; CEO personally calls the two largest at-risk accounts; pause new SE outbound and redirect to retention; review whether rate-lock offer should be extended to next tier | Chief Customer Officer + CEO — trigger at month-end reporting |
| Regional bank macro freeze: 3+ accounts defer renewals citing OpEx | Shift positioning from productivity ROI to compliance risk reduction (cost of non-compliance > cost of Prism); offer 6-month payment deferrals with 12-month contract extensions to preserve ACV | VP Sales + CFO — trigger within 2 weeks of third deferral notification |
| Bloomberg announces compliance AI module | Convene emergency Board session; prepare strategic sale data room targeting Moody's Analytics, S&P Global, or Clearwater as acquirers; engage one M&A advisor under NDA | CEO + Board — trigger within 30 days of Bloomberg announcement |
