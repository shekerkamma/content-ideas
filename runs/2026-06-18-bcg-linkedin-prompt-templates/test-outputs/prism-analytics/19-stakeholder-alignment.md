# Stakeholder Alignment Plan — Prism Analytics

## Decision Path

The $3.2M investment in LLM acceleration requires Board approval for capital allocation (Tranche structure recommended: $1.8M at kickoff, $1.4M upon Q3 LLM milestone). The CEO sponsors and presents the recommendation. CFO provides financial model and runway analysis. CTO provides technical feasibility confirmation on the 2-month acceleration timeline. The Board must decide by end of June 2026 to preserve the engineering runway needed for Q4 2026 GA. Without a decision by June 30, the acceleration benefit is lost: the LLM interface defaults to the existing Q1 2027 timeline and the competitive repositioning window closes.

## Stakeholder Map

| Stakeholder | Role | Influence | Current Stance | What They Need To Hear |
|---|---|---|---|---|
| CEO | Strategy sponsor, Board presenter | Decision architect | Committed — this is his strategic bet; faces personal credibility risk if the strategy fails | Needs the Board aligned behind the plan with clear milestones; most concerned about the Board framing the situation as distress rather than opportunity |
| Board / Lead Investor | Capital approval; path-to-profitability or sale mandate | Veto power | Skeptical but open — Series C investors are 4 years in; they need a credible exit horizon | "This investment is the fastest path to $65M ARR which unlocks the strategic sale at 4–5x; deferring it guarantees the sub-optimal outcome" |
| CFO | Runway custodian; tranche structure designer | High — controls spend authority and flags any deviation from $2.1M burn | Cautiously supportive — built the runway model; concerned that $3.2M is not enough and that a second ask is coming | Tranche structure with hold trigger at sprint slippage protects runway; break-even math works if win rate recovers by just 6 percentage points |
| CTO | Builds the LLM acceleration; owns engineering reallocation | High — has to deliver the technical feasibility | Supportive of the goal; anxious about platform stability regression if engineers are redeployed too aggressively | Engineering plan freezes non-critical platform changes for 90 days; 18-engineer LLM squad is fully ring-fenced; platform SLA war-room mitigates regression risk |
| VP Sales | Must convert the $28M pipeline with 4 new SEs; accountable for win-rate recovery | High — without their buy-in, the sales execution falls apart | Strongly supportive — has been losing deals to Clearwater and wants the product story to improve | 4 new SE hires arrive before Q3 2026; design partner launches generate reference customers before SE team presents to new prospects |
| Chief Customer Officer | Accountable for NRR recovery and churn reduction | Medium-High — owns the 30 at-risk regional bank accounts that drive gross churn risk | Neutral — supportive of LLM upsell potential but worried CSM team will be overwhelmed by both churn defense and onboarding design partners | Dedicated CSM coverage for 30 at-risk accounts is a separate workstream from design partner onboarding; no CSM will be asked to do both |
| VP Product | Owns the LLM product roadmap and design partner program | Medium — can accelerate or slow the GA timeline through scope decisions | Cautiously supportive — concerned that the LLM accuracy bar (92% UAT threshold) may be too aggressive for Q4 2026 | Accuracy bar of 92% was set with design partner input; if UAT results fall short, a limited GA with flagged query types is an acceptable middle path |

## Resistance Points

| Concern | Who Holds It | Response |
|---|---|---|
| "We've been through two years of deceleration — why will this time be different?" | Board / Lead Investor | The prior decelerations were capability gaps (no AI, no NLP); this investment closes the specific gap that win/loss analysis confirms is the deciding factor in >50% of losses. The $28M pipeline is already qualified — we are converting it at a higher rate, not building new pipeline from scratch. |
| "What if the LLM interface doesn't meet bank compliance standards?" | Board, CTO, CFO | The UAT gate with 3 bank design partners is a hard go/no-go before any commercial announcement. We will not position the LLM as production-ready until compliance officers sign off. A delayed or scoped GA is explicitly planned for; a failed GA is not catastrophic — it is a phased rollout. |
| "Are 4 sales engineers the right bet — what if the problem is product, not coverage?" | CFO, CEO | Win/loss confirms two drivers: AI perception gap (product answer) and insufficient SE coverage for technical evaluation depth (coverage answer). We are addressing both. If win/loss analysis in Week 1 shows coverage is not a factor, we hold the SE hiring and redirect the budget. |
| "Eighteen months of runway is not enough margin. What happens if we miss the ARR target?" | Board / Lead Investor | If Q3 2026 ARR trajectory falls below $54M, we have two pre-committed responses: (1) activate strategic sale process with a data room built on LLM GA and NRR recovery evidence; (2) present a profitability path to the Board based on restructuring to $1.7M/mo burn at current ARR. Neither is a surprise — both are in the Board deck. |
| "Why not raise a Series D now and replatform to real-time properly?" | Board growth faction | A Series D in the current growth-rate environment (14% YoY) would be significantly dilutive — likely at a flat or down round from the 2022 Series C valuation. Replatforming at $48M ARR with 18 months of runway is too risky a parallel workstream. The LLM investment restores the growth rate and the valuation story before any raise. |

## Pre-Wire Plan

| Action | Owner | Timing | Desired Outcome |
|---|---|---|---|
| Win/loss analysis summary brief to Board lead director — establishes the competitive evidence base | CEO + VP Sales | Week 1 of June 2026 | Board lead director understands the AI perception gap before the formal recommendation; neutralizes the "why now?" objection |
| CTO technical feasibility memo — confirms 2-month acceleration is achievable with ring-fenced squad and platform freeze | CTO | Week 2 of June 2026 | CFO and Board have written confirmation that the engineering plan is credible; reduces "is this technically real?" resistance |
| CFO 1:1 with Board lead investor — walk the tranche structure, break-even math, and runway sensitivity model | CFO | Week 2 of June 2026 | Lead investor understands that the $3.2M is structured with a hold trigger; burn discipline is built into the approval |
| VP Sales pipeline briefing to CEO — stage-by-stage review of top 15 deals and where SE coverage accelerates close | VP Sales | Week 3 of June 2026 | CEO can present specific deal names and expected close timelines in the Board meeting; makes pipeline conversion tangible |
| Design partner commitment letter from 3 Tier 1 bank contacts — confirms customer appetite for early LLM access | VP Product + VP Sales | Week 3 of June 2026 | Board sees customer pull, not just internal conviction; the three bank CISOs who have agreed to participate are named in the Board deck |
| Full Board pre-read: strategy deck + financial model + engineering plan + tranche term sheet | CEO + CFO | Week 4 of June 2026 (5 business days before meeting) | No surprises in the room; Board members can read, question, and pre-form views before the meeting; formal vote is confirmation, not deliberation |
| Board decision meeting | CEO (presenter), CFO + CTO (in room) | End of June 2026 | Approved: $1.8M Tranche 1 authorized; CTO begins engineering reallocation; VP Sales begins SE hiring process |
