# KPI Architecture — Prism Analytics

## Strategic Objective

Manage the execution of the AI-first compliance intelligence repositioning: accelerate LLM interface to GA by Q4 2026, convert the $28M pipeline at a 42% win rate, recover NRR to 110%+, and reach $62M ARR by end of FY2026 — all within the existing 18-month cash runway without requiring a capital raise.

## KPI System

| KPI | Type | Decision It Supports | Owner | Threshold |
|---|---|---|---|---|
| ARR (monthly) | Lagging outcome | Is the strategy producing revenue growth fast enough to reach $62M by FY2026 end? | CFO | $54M by Q3 2026; $62M by Q4 2026 |
| Net Revenue Retention (quarterly) | Lagging outcome | Is the existing base expanding, or is churn eroding new logo gains? | Chief Customer Officer | ≥107% by Q2 2026; ≥110% by Q4 2026 |
| Win Rate (rolling 90-day) | Leading outcome | Is the AI-first repositioning improving competitive performance before GA? | VP Sales | ≥36% by Q3 2026 (pre-GA); ≥42% by Q4 2026 (post-GA) |
| LLM Interface Milestone Completion (sprint velocity %) | Leading driver | Is the engineering team on track to hit Q4 2026 GA? | CTO | ≥85% planned story points completed per 2-week sprint; 0 consecutive slippages |
| LLM Query Accuracy (UAT benchmark) | Leading driver | Is the LLM interface meeting compliance-grade accuracy thresholds required for bank UAT approval? | VP Product | ≥92% accuracy vs. validated Basel IV / CECL query test suite before design partner launch |
| Pipeline Qualified Opportunities (value at close) | Leading driver | Is the sales force building enough pipeline to sustain win-rate recovery into FY2027? | VP Sales | ≥$28M qualified pipeline maintained throughout FY2026; ≥$35M by Q4 2026 |
| Gross Churn Rate (monthly ARR) | Leading risk | Is regional bank attrition accelerating, threatening NRR recovery? | Chief Customer Officer | <0.5%/month; trigger review at 0.6%; escalate to CEO at 0.7% |
| Monthly Burn Rate | Financial control | Is the $3.2M investment being deployed within the 18-month runway constraint? | CFO | ≤$2.3M/mo during investment phase; ≤$2.1M/mo after SE hiring is complete (Q3 2026) |
| Design Partner Activation Count | Leading driver | Is early design partner engagement generating the reference customers needed for the commercial launch? | VP Sales + VP Product | ≥10 design partners live on LLM early access by September 2026 |
| New Logo Bookings (quarterly) | Leading outcome | Are new sales engineer hires accelerating pipeline conversion in the $28M book? | VP Sales | ≥$3.5M new bookings per quarter; ≥$5M in Q4 2026 (post-GA) |

## Driver Tree

**ARR ($62M target)**
- Net new ARR from new logos ($14M required): driven by win rate (42% target) × pipeline velocity ($28M+ qualified) × ACV maintenance ($343K)
  - Win rate: driven by LLM accuracy, design partner references, SE deployment effectiveness
  - Pipeline velocity: driven by new SE outbound coverage, inbound from AI-first repositioning, referral from design partners
  - ACV: maintained by positioning away from discount competition; compliance depth vs. Clearwater
- Expansion ARR from existing base: driven by NRR (110% target) × current ARR base
  - NRR: driven by gross churn control (<6%) + upsell of LLM add-on module to existing accounts
  - Gross churn: driven by regional bank retention (at-risk accounts covered by dedicated CSMs) + macro spend environment
- Burn control: limits the time available for strategy to prove out — every month of overrun compresses the window by one month

**Win Rate (42% target)**
- Current: 31% (down from 47% two years ago)
- Drivers: AI-first perception (LLM interface), compliance accuracy credibility (UAT results), SE coverage quality (4 new hires), reference customer availability (design partners)
- Lag: Win rate improvements will only appear in data 2–3 months after SE deployment and LLM launch, given the 8–14 month sales cycle — early signals must come from pipeline stage progression rates, not closed-won data

## Metrics To Remove

| Metric | Why Remove |
|---|---|
| Total registered users / platform logins | Prism is enterprise B2B; usage metrics across users conflate power users with obligated reviewers; not a signal of customer health or expansion readiness |
| Feature release count per sprint | Measures output, not outcomes; creates incentive to ship features that do not advance win rate or NRR |
| Total pipeline (gross, including unqualified) | Inflates confidence in a moment when pipeline conversion is the problem; replace with qualified pipeline value only |
| Employee count / hiring velocity | Prism is not in a headcount-growth phase; tracking hires distracts from burn discipline during the investment period |
| Social / PR mentions of AI repositioning | Vanity signal; does not predict win rate or pipeline conversion; replace with design partner activation count as the real-world signal |

## Review Cadence

**Weekly (CEO + CTO + VP Sales):**
- LLM milestone completion % vs. plan
- Pipeline stage progression on top 15 deals
- Escalation trigger: any sprint slippage or deal moving backward in pipeline stage

**Monthly (Full Leadership Team):**
- ARR vs. $62M trajectory
- Win rate (rolling 90-day)
- Gross churn rate vs. 0.5% threshold
- Burn rate vs. $2.3M cap
- LLM UAT accuracy score
- Decision: reallocation of SE headcount between new logo and retention if churn threshold is breached

**Quarterly (Board):**
- NRR vs. 110% target trajectory
- New logo bookings vs. quarterly milestone
- Design partner activation count
- Revised ARR forecast vs. $62M
- Strategic decision point: if ARR trajectory is below $54M at Q3 review, present Board with strategic sale option with updated data room

**Escalation Triggers:**
- Any single month gross churn >0.7%: CEO war-room within 48 hours
- Two consecutive sprint slippages: CTO presents revised engineering plan + contingency options to CEO within 5 days
- Win rate below 28% in any rolling 90-day period: VP Sales + CEO review pipeline quality and SE deployment immediately
- Monthly burn exceeds $2.5M: CFO presents tranche 2 hold recommendation to Board
