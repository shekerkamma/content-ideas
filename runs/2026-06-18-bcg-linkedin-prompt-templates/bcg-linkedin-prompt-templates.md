# The Consultant's Guide to Claude — 21 BCG-Style LinkedIn Post Prompt Templates

> Source: Anthropic × BCG · "21 BCG-Style Skills to Push Claude Opus to Its Limits"
> Skills repo: `/home/sheke/.claude/skills/strategy-consulting/`
> Format: Each entry = ready-to-publish LinkedIn post + the exact Claude prompt that powers it.

---

## HOW TO USE THIS FILE

Copy the **LinkedIn Post** section, personalise the [bracket fields], publish.
Copy the **Claude Prompt** section, paste into Claude Code, paste your context, run.

The 21 skills follow the MBB consulting operating system:
**Diagnose → Map → Choose → Execute → Govern → Communicate**

---

## 01 — PROBLEM-FRAMING: Situation Assessment

### LinkedIn Post

**Most strategy projects fail before a single slide is built.**

They fail because the team spent three weeks answering the wrong question.

BCG's first move is never "what should we do?"
It's "where are we, really?"

I now run a Situation Assessment through Claude every time I open a new engagement.
Here's the prompt I use — and what it produces in 90 seconds that would take a team three days.

**The prompt:**
```
/situation-assessment

[Paste your business context: financials, market position, KPIs, recent changes, key decisions pending]
```

Claude returns:
→ Executive read (one paragraph)
→ Fact base with confidence labels (facts vs. interpretations vs. unknowns)
→ Momentum signals (trend, not snapshot)
→ Top 3 strategic issues
→ Open questions to answer before choosing strategy

The quality bar is strict: it separates facts from hypotheses, highlights trend over point-in-time, and forces you to see what you don't know.

You can't pick the right strategy until you've done this.

What's your first move on a new engagement?

#strategyConsulting #BCG #ClaudeAI #MBB #ExecutiveStrategy

---

### Claude Prompt (copy-paste ready)

```
/situation-assessment

Context: [Company name], [industry], [revenue/size]
Key facts available: [financials, growth rate, market share, recent events]
Decision being made: [what leadership must decide in the next 30–90 days]
Available data: [list what you have]
```

---

## 02 — PROBLEM-FRAMING: Growth Barriers

### LinkedIn Post

**Revenue plateau is never what it looks like on the surface.**

The CEO says "we need more pipeline."
The CRO says "we need better product."
The CPO says "we need clearer positioning."

They're all wrong. Or rather — they're all seeing symptoms.

BCG's diagnostic question is: *What is the ONE constraint that, if removed, unlocks everything else?*

This skill makes Claude find it.

**The prompt:**
```
/growth-barriers

[Describe your growth stall: revenue trend, what you've tried, what's NOT working]
```

Claude returns:
→ Growth barrier tree (symptoms → root causes → the true constraint)
→ What has already been tried and why it didn't work
→ The lever that actually moves the number
→ 90-day diagnostic plan

I used this with a $30M SaaS company stuck at the same ARR for 18 months.
The real barrier wasn't sales. It was a retention problem hiding in the enterprise tier.

Stop treating symptoms.

#GrowthStrategy #RevenueGrowth #BCGConsulting #ClaudeAI #B2B

---

### Claude Prompt (copy-paste ready)

```
/growth-barriers

Business: [description]
Revenue trend (last 12–24 months): [flat/declining/slow growth + numbers]
What we've tried: [initiatives, investments, pivots]
What hasn't moved: [the metric that won't budge]
Hypothesis (if any): [your current theory]
```

---

## 03 — PROBLEM-FRAMING: Assumption Audit

### LinkedIn Post

**Every strategy has a hidden assumption that will kill it.**

Most strategies fail not because the plan was bad.
They fail because one belief no longer true, and nobody checked.

BCG calls these "load-bearing assumptions" — the beliefs the entire strategy rests on.

I now run an Assumption Audit through Claude before any major recommendation.

**The prompt:**
```
/assumption-audit

[Paste the strategy or investment case you want to pressure-test]
```

Claude returns:
→ Every load-bearing assumption, ranked by evidence strength
→ What would have to be true for each one to hold
→ The test to run if evidence is weak
→ Kill criteria — what would make this strategy wrong

An assumption with weak evidence is not a fact. It's a bet.
This skill makes sure you know which bets you're making.

What assumption is YOUR strategy resting on right now?

#StrategyExecution #BusinessStrategy #BCG #RiskManagement #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/assumption-audit

Strategy or plan: [describe the strategy, investment, or decision in 3–5 sentences]
Decision context: [who will decide, what's at stake, timeline]
Evidence available: [what data supports it]
Known risks: [concerns already flagged]
```

---

## 04 — MARKET INTELLIGENCE: Market Mapping

### LinkedIn Post

**TAM is not a market strategy.**

Saying "our market is $50B" tells an investor nothing about where to compete.

BCG's Market Mapping skill answers a different question:
*Where in this market is value created, growing, and capturable — and which segment is actually worth entering?*

**The prompt:**
```
/market-mapping

[Describe the market, your current position, and the strategic question you're trying to answer]
```

Claude returns:
→ Top-down AND bottom-up market sizing
→ Segment attractiveness matrix (growth × profitability × competitive intensity)
→ White space with entry logic
→ Where-to-play recommendation with trade-offs

The output isn't a number. It's a targeting decision.

#MarketStrategy #MarketEntry #BCGConsulting #GoToMarket #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/market-mapping

Market: [name/description]
Our current position: [where we play today, revenue, share]
Strategic question: [market entry / segment focus / expansion / where to double down]
Data available: [market reports, revenue by segment, customer data]
Decision timeline: [when this needs to be decided]
```

---

## 05 — MARKET INTELLIGENCE: Competitive Intelligence

### LinkedIn Post

**Your biggest competitor risk is not what they're doing today.**

It's what they'll do the day you announce your new strategy.

BCG doesn't ask "what are competitors doing?" 
They ask "what are competitors *incentivised* to do next — and when?"

I use this skill before every go-to-market decision.

**The prompt:**
```
/competitive-intel

[Name your key rivals, describe your planned move, and what you know about their position]
```

Claude returns:
→ Competitor intent model (incentives, capabilities, constraints)
→ Likely response scenarios (base, aggressive, defensive)
→ Your vulnerabilities they'll target
→ Pre-emptive moves to make their response harder

Strategy is a game. Model the other players.

#CompetitiveIntelligence #MarketStrategy #BCG #StrategicPlanning #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/competitive-intel

Your planned strategic move: [new product, price change, market entry, M&A, etc.]
Key competitors: [list 2–4, with what you know about their position/resources]
Your current position vs. each: [stronger/weaker in what dimensions]
What you fear they'll do: [your instinct on their response]
```

---

## 06 — MARKET INTELLIGENCE: Customer Segmentation

### LinkedIn Post

**"SMB mid-market enterprise" is not a segmentation. It's a size sort.**

BCG's Customer Segmentation skill builds MECE segments based on:
- What customers actually need (not what they say)
- The economics of serving each segment
- Which segments are strategically valuable vs. unprofitable noise

**The prompt:**
```
/customer-segmentation

[Describe your current customer base, revenue by type, and what strategic decision depends on this segmentation]
```

Claude returns:
→ Needs-based segments (MECE — no overlap, no gaps)
→ Economics per segment (CAC, LTV, retention, margin)
→ Strategic value matrix
→ Priority segments + resource allocation recommendation

The right segmentation changes your pricing, product, and GTM.
The wrong one explains why you're growing slowly.

#CustomerStrategy #GTM #BCGConsulting #SaaS #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/customer-segmentation

Current customer base: [description, approximate count, industries, company sizes]
Revenue breakdown (if known): [by type, size, or channel]
Strategic decision depending on this: [pricing / product / GTM focus / retention]
Available data: [CRM data, surveys, NPS, usage data — describe what exists]
```

---

## 07 — MARKET INTELLIGENCE: Profit Pool Analysis

### LinkedIn Post

**Revenue is vanity. Profit pool is strategy.**

Most companies compete for revenue.
The best companies compete for profit.

BCG's Profit Pool Analysis maps where in your market, product portfolio, or value chain profit is actually created — and where it's quietly leaking.

**The prompt:**
```
/profit-pool-analysis

[Describe your product set, customer tiers, and channels — include what margin data you have]
```

Claude returns:
→ Profit pool map (segment × margin × strategic position)
→ Where you're over-serving low-margin customers
→ Where competitors capture more profit than you in the same market
→ Pricing power assessment
→ Strategic reallocation recommendation

If you can't explain where your margin comes from, someone else will.

#ProfitStrategy #Margins #BCG #BusinessStrategy #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/profit-pool-analysis

Products/services: [list with approximate revenue and gross margin for each]
Customer segments: [and what margin you make serving each]
Value chain role: [where you sit — vendor/platform/distributor/integrator]
Where you suspect margin is leaking: [your hypothesis]
```

---

## 08 — STRATEGIC CHOICE: Strategic Options

### LinkedIn Post

**The worst strategic mistake is choosing between only two options.**

Binary choices are a cognitive trap.
Real strategy requires generating a full set of meaningful alternatives — and then choosing.

BCG's Strategic Options skill forces you to build 3–5 truly distinct paths before evaluating any.

**The prompt:**
```
/strategic-options

[State the decision, constraints, and what you're optimising for]
```

Claude returns:
→ 3–5 distinct, viable options (not variations of one idea)
→ Decision criteria matrix (attractiveness × feasibility × risk × fit)
→ Trade-off table
→ Recommended path with "what must be true" conditions
→ Hybrid / sequencing options if relevant

One recommendation is not a strategy. It's a conclusion.
Strategy is the comparison that earns the conclusion.

#StrategicDecisions #BCGConsulting #Leadership #ClaudeAI #ExecutiveStrategy

---

### Claude Prompt (copy-paste ready)

```
/strategic-options

Decision: [what must be decided]
Constraints: [budget, timeline, regulatory, resource limitations]
Optimising for: [growth / margin / market position / resilience]
Options already considered: [list what you've thought of — Claude will expand and challenge]
Deadline: [when the decision must be made]
```

---

## 09 — STRATEGIC CHOICE: Pricing Strategy

### LinkedIn Post

**Every discounting problem is a pricing strategy problem in disguise.**

When your team discounts 30% to close deals, it doesn't mean your sales team is weak.
It means your pricing architecture has no anchor.

BCG's Pricing Strategy skill diagnoses where pricing power exists and where it's leaking.

**The prompt:**
```
/pricing-strategy

[Describe your current pricing model, discount patterns, and what decision you're trying to make]
```

Claude returns:
→ Willingness-to-pay analysis by segment
→ Discount leakage map (where and why margin is lost)
→ Packaging and tiering recommendations
→ Price increase feasibility + communication approach
→ Value pricing vs. cost-plus vs. competitive anchoring

Most companies leave 15–25% of revenue on the table in pricing.
This skill finds it.

#PricingStrategy #SaaS #RevenueOps #BCG #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/pricing-strategy

Current pricing model: [per seat / usage / flat fee / custom — describe tiers]
Average discount rate: [% and where discounting happens most]
Win/loss patterns: [where you win on price vs. lose on price]
Customer segments: [and what each pays vs. what they'd likely pay]
Decision: [price increase / new packaging / reduce discounting / new tier]
```

---

## 10 — STRATEGIC CHOICE: Business Case Builder

### LinkedIn Post

**A business case that can't survive a hostile CFO isn't a business case. It's a wish.**

BCG's business case standard is brutal: every assumption is labelled, every sensitivity is modelled, and the recommendation survives the worst plausible scenario.

Most decks show NPV at base case. BCG shows you at what point the investment breaks.

**The prompt:**
```
/business-case-builder

[Describe the investment, initiative, or bet you need to justify]
```

Claude returns:
→ Economics model (revenue, cost, payback, NPV, IRR)
→ Assumption register with evidence strength labels
→ Sensitivity table (which assumptions matter most)
→ Break-even analysis
→ Risk-adjusted recommendation

If the business case only works at base case — it doesn't work.

#BusinessCase #CFO #InvestmentDecision #BCGConsulting #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/business-case-builder

Initiative: [what you're proposing to fund]
Investment required: [CapEx, OpEx, headcount — by year if known]
Revenue / cost benefit expected: [your estimate and basis]
Key assumptions: [what has to be true for this to work]
Decision maker: [who approves — CFO, board, CEO — and what they care about]
Timeline: [payback horizon expected]
```

---

## 11 — STRATEGIC CHOICE: Portfolio Review

### LinkedIn Post

**Most companies are spread too thin and won't admit it.**

When everything is a priority, nothing is.

BCG's Portfolio Review skill applies the same logic McKinsey uses with Fortune 500 CEOs to any portfolio — products, markets, initiatives, or customer segments.

**The prompt:**
```
/portfolio-review

[List your portfolio: products / markets / initiatives — with rough revenue and strategic context for each]
```

Claude returns:
→ Portfolio map (market attractiveness × competitive position)
→ Invest / Hold / Harvest / Exit recommendation per element
→ Resource allocation logic
→ Dependency and sequencing map
→ Pruning candidates with rationale

A focused portfolio isn't a retreat.
It's how you win the bets that matter.

#PortfolioStrategy #ResourceAllocation #BCGMatrix #ClaudeAI #Leadership

---

### Claude Prompt (copy-paste ready)

```
/portfolio-review

Portfolio elements: [list products / markets / initiatives]
For each: [revenue/size, growth rate, margin, competitive position, strategic importance]
Current resource allocation: [where headcount and budget are concentrated]
Strategic goal: [growth / profitability / resilience / transformation]
Constraint: [what you can't change — brand, geography, technology platform]
```

---

## 12 — EXECUTION: Operating Model Design

### LinkedIn Post

**Strategy without an operating model is just a deck.**

You can have the right strategy and still fail to execute it.
Because execution depends on who owns what, how decisions get made, and what capabilities exist.

BCG's Operating Model Design skill translates strategy into:
capabilities, roles, decision rights, governance, and ways of working.

**The prompt:**
```
/operating-model-design

[Describe the strategy you're executing and what's currently broken in how work gets done]
```

Claude returns:
→ Capability model (what the org must do well to win)
→ Operating structure options
→ Decision rights RACI for critical decisions
→ Governance design
→ Ways-of-working changes
→ Transition risks

Where the operating model doesn't fit the strategy, the strategy loses.

#OperatingModel #OrgDesign #BCGConsulting #TransformationLeadership #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/operating-model-design

Strategy: [1–2 sentences on what you're trying to achieve]
Current operating model pain points: [where things break down — decisions, ownership, speed]
Org structure today: [rough description]
Key capabilities needed: [what the business must do well to win]
Constraints: [headcount budget, union rules, geography, existing systems]
```

---

## 13 — EXECUTION: Initiative Prioritization

### LinkedIn Post

**Your transformation roadmap has 47 initiatives. It will deliver 3.**

Capacity is the real constraint in every transformation.
Most initiative lists are wish lists that haven't been stress-tested against bandwidth.

BCG's Initiative Prioritization skill cuts through it.

**The prompt:**
```
/initiative-prioritizer

[List your initiatives with what you know about impact, effort, and dependencies]
```

Claude returns:
→ Priority matrix (strategic impact × feasibility × dependencies)
→ Must-do vs. should-do vs. can-wait classification
→ Quick wins (high impact, low effort — fund immediately)
→ Kill list with rationale
→ Sequenced portfolio with resource logic

Your roadmap should be a commitment, not a catalogue.

#Transformation #RoadmapPlanning #BCG #Prioritization #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/initiative-prioritizer

Initiatives (list each): [name, description, estimated impact, estimated effort, status]
Strategic goals they serve: [growth / cost / resilience / transformation]
Available resources: [headcount, budget, time horizon]
Dependencies known: [what must happen before what]
Non-negotiables: [initiatives that cannot be cut — and why]
```

---

## 14 — EXECUTION: Transformation Roadmap

### LinkedIn Post

**The strategy is approved. Now what?**

Most transformations fail in the 90 days after the strategy deck is signed.
Not because the strategy was wrong — because no one built the bridge from "approved" to "running."

BCG's Transformation Roadmap skill builds that bridge.

**The prompt:**
```
/transformation-roadmap

[Describe the strategy and what "done" looks like in 12–24 months]
```

Claude returns:
→ Phased workstreams (Sprint → Scale → Sustain)
→ Milestone map with dependencies
→ Owner assignments
→ Risk and interdependency log
→ First-90-days plan
→ Governance and PMO design

Transformation is not a project. It's a program.
This skill designs the program.

#Transformation #ChangeManagement #BCGConsulting #StrategicExecution #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/transformation-roadmap

Strategy being executed: [1–2 sentences]
Target state: [what success looks like in 12–24 months]
Workstreams identified: [list major tracks — technology / people / process / commercial]
Key dependencies: [what must happen first]
Governance structure: [steering committee, sponsor, PMO — current state]
Top risks: [what you're most worried about]
```

---

## 15 — GOVERNANCE: Risk and Mitigation

### LinkedIn Post

**The risks that sink strategies are the ones marked "low likelihood."**

Every strategy team puts the obvious risks on the register.
BCG puts the non-obvious ones there too — and pre-commits the response.

**The prompt:**
```
/risk-and-mitigation

[Describe the strategy or initiative and what you're most worried about]
```

Claude returns:
→ Risk register (likelihood × impact × velocity)
→ Root cause per risk
→ Mitigation actions with owners and triggers
→ Contingency plans for high-severity scenarios
→ Early warning indicators to monitor

A risk register is not a list of fears.
It's a commitment to watch, own, and act.

#RiskManagement #StrategicRisk #BCGConsulting #Governance #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/risk-and-mitigation

Strategy or initiative: [description]
Top risks you already see: [list known concerns]
Risk categories to cover: [execution / competitive / regulatory / technology / financial / people]
Decision makers: [who owns risk at the board/exec level]
Timeline: [launch date or transformation horizon]
```

---

## 16 — GOVERNANCE: War Gaming

### LinkedIn Post

**Your strategy looks brilliant on paper.**

Paper doesn't compete back.

BCG war games every major strategy before commitment.
Three teams: your team, the aggressive competitor, the market.
Each plays to win.

**The prompt:**
```
/war-gaming

[Describe your strategy and your top 2–3 competitive threats]
```

Claude returns:
→ Scenario set (base, aggressive competitor, market disruption, execution failure)
→ Vulnerability map — where your strategy breaks under pressure
→ Early warning signals for each scenario
→ Pre-committed response playbook

The goal isn't to predict the future.
It's to make your strategy less fragile before reality tests it.

#WarGaming #ScenarioPlanning #BCGConsulting #CompetitiveStrategy #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/war-gaming

Strategy to test: [your plan in 3–5 sentences]
Top competitors: [who could respond aggressively]
Market risks: [disruption vectors — technology, regulation, customer behavior]
Your biggest vulnerability: [what you're most worried about]
Time horizon: [12 months / 3 years / 5 years]
```

---

## 17 — GOVERNANCE: KPI Architecture

### LinkedIn Post

**Most companies measure what's easy to measure, not what matters.**

You have 40 KPIs on your dashboard.
You know which ones the CEO actually cares about at 9am on a Monday.

BCG's KPI Architecture skill designs a measurement system tied to strategic decisions — not reporting convenience.

**The prompt:**
```
/kpi-architect

[Describe your strategy and what decisions you need the metrics to support]
```

Claude returns:
→ Strategic KPI hierarchy (outcome → driver → leading indicator)
→ Owner per metric
→ Vanity metric kill list
→ Operating cadence design (daily / weekly / monthly / quarterly)
→ Threshold and alert logic

You manage what you measure.
Make sure you're measuring the right things.

#KPIStrategy #PerformanceManagement #BCG #OKRs #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/kpi-architect

Strategy: [what the business is trying to achieve]
Current metrics: [list what you track today]
Decisions these metrics support: [what do leaders actually use them to decide]
Cadence: [how often reporting happens and who reviews it]
Problems with current metrics: [lagging / too many / not actionable / contested]
```

---

## 18 — GOVERNANCE: Value Realization

### LinkedIn Post

**The business case was approved 18 months ago.**

Has anyone checked if the benefits are actually landing?

BCG builds a Value Realization plan before the project launches — not after it goes live.
Because by the time the benefits fail to show, it's too late to change the design.

**The prompt:**
```
/value-realization

[Describe the initiative and the benefits promised in the business case]
```

Claude returns:
→ Benefits register with ownership and measurement method
→ Tracking cadence and review gates
→ Benefit dependency map (what must happen for each benefit to materialise)
→ Contingency triggers (what to do if benefits are off track)
→ Synergy capture plan for M&A / transformation programs

Value doesn't realize itself.
Someone has to own every number.

#ValueRealization #BCGConsulting #TransformationROI #BenefitsManagement #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/value-realization

Initiative: [name and description]
Benefits promised: [list each with $ or % value and timeline]
Current tracking: [how benefits are currently measured, if at all]
Owners: [who committed to each benefit]
Risk to realization: [what could prevent benefits from landing]
Review governance: [who reviews progress and how often]
```

---

## 19 — COMMUNICATION: Stakeholder Alignment

### LinkedIn Post

**Every strategy dies in a meeting that the right people didn't attend.**

Or worse — in a conversation that happened after the meeting where the decision was made.

BCG's Stakeholder Alignment skill maps who must be moved, how, and in what sequence — before the strategy reaches the room.

**The prompt:**
```
/stakeholder-alignment

[Describe the strategy and who needs to approve, support, or not block it]
```

Claude returns:
→ Stakeholder map (influence × disposition)
→ Decision criteria per stakeholder
→ Pre-wire sequence (who to move first)
→ Objections and pre-committed answers
→ Coalition-building plan

You can have the right strategy and still lose the vote.
This skill ensures you don't.

#StakeholderManagement #ExecutiveAlignment #BCGConsulting #ChangeLeadership #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/stakeholder-alignment

Strategy requiring alignment: [description]
Key stakeholders: [list names/roles and their current disposition — supportive/neutral/resistant]
Decision being sought: [what you need them to approve or support]
Known objections: [what you've already heard or expect]
Timeline: [when alignment must be achieved]
Political context: [any history, tensions, or dynamics relevant to the decision]
```

---

## 20 — COMMUNICATION: Narrative Builder

### LinkedIn Post

**The best strategy in the room loses to the best-told story.**

BCG's senior partners don't present findings. They tell stories.

The structure is always the same: Situation → Complication → Question → Answer.
The answer comes first. The evidence follows.

This is the Pyramid Principle — and Claude executes it precisely.

**The prompt:**
```
/narrative-builder

[Paste your analysis, recommendation, or strategy — and describe your audience]
```

Claude returns:
→ SCQA storyline (Situation / Complication / Question / Answer)
→ Pyramid logic (recommendation + 3 supporting arguments + evidence)
→ Headline sequence (the story if you only read the slide titles)
→ Hostile Q&A (the five worst questions, with answers)

If your audience is still debating after your presentation — the narrative failed.

#ExecutiveCommunication #PyramidPrinciple #BCGConsulting #StorytellingForLeaders #ClaudeAI

---

### Claude Prompt (copy-paste ready)

```
/narrative-builder

Audience: [who will receive this — board / CEO / investors / leadership team]
Recommendation: [your core recommendation in one sentence]
Supporting evidence: [key facts, analyses, and data supporting the recommendation]
Likely objections: [concerns your audience will raise]
Desired action: [what you need them to do after receiving this]
Tone: [direct / diplomatic / urgent / confidence-building]
```

---

## 21 — COMMUNICATION: Decision Memo

### LinkedIn Post

**Every major decision deserves a one-page memo.**

Not a 40-slide deck. Not a 20-page report. One page.

BCG structures every major recommendation as a Decision Memo:
recommendation → context → options considered → evidence → risks → next steps.

The person who reads it should be able to decide in under five minutes.

**The prompt:**
```
/decision-memo

[Describe the decision, your recommendation, and what evidence supports it]
```

Claude returns:
→ Executive summary (recommendation in one sentence)
→ Context and burning platform
→ Options considered and why rejected
→ Evidence for the recommendation
→ Risks and mitigations
→ Recommended next steps with owners and dates

A great decision memo makes the recommendation impossible to ignore and easy to act on.

What's the last major decision you made without one?

#DecisionMaking #ExecutiveLeadership #BCGConsulting #ClaudeAI #LeadershipCommunication

---

### Claude Prompt (copy-paste ready)

```
/decision-memo

Decision required: [what must be decided and by when]
Recommendation: [your preferred path]
Context: [why this decision matters now]
Options considered: [what alternatives were evaluated]
Evidence: [key facts supporting the recommendation]
Risks: [top 2–3 risks and how they're mitigated]
Decision maker: [who signs off — name/role]
Next steps: [what happens immediately after approval]
```

---

## BONUS: The Reusable Consulting Operating System

### LinkedIn Post

**21 skills. One operating system. Any engagement.**

The BCG consulting backbone is not a method. It's a chain.

Every engagement follows the same architecture:

```
01 Diagnose   →  Situation Assessment + Growth Barriers + Assumption Audit
02 Map        →  Market Mapping + Competitive Intel + Customer Segmentation + Profit Pools
03 Choose     →  Strategic Options + Pricing + Business Case + Portfolio Review
04 Execute    →  Operating Model + Initiative Prioritization + Transformation Roadmap
05 Govern     →  Risk Register + War Gaming + KPI Architecture + Value Realization
06 Communicate → Stakeholder Alignment + Narrative Builder + Decision Memo
```

I've wired all 21 into Claude Code as slash commands.

Every engagement now starts with `/situation-assessment` and ends with `/decision-memo`.

The strategy infrastructure used to cost $500K in consulting fees.
Now it runs on Claude Opus in your terminal.

Drop a 🧠 if you want the full skill library.

#ConsultingIntelligence #BCGConsulting #ClaudeAI #MBBStrategy #AIforConsultants

---

### Claude Prompt (chain the full OS)

```
# Full consulting engagement chain

Step 1 — Diagnose:
/situation-assessment [context]
/growth-barriers [context]
/assumption-audit [strategy to test]

Step 2 — Map:
/market-mapping [market + strategic question]
/competitive-intel [planned move + rivals]
/customer-segmentation [customer base + decision]
/profit-pool-analysis [portfolio + margin data]

Step 3 — Choose:
/strategic-options [decision + constraints]
/business-case-builder [investment to justify]
/portfolio-review [portfolio list + allocation question]

Step 4 — Execute:
/operating-model-design [strategy + org pain points]
/initiative-prioritizer [initiative list + resources]
/transformation-roadmap [strategy + target state]

Step 5 — Govern:
/risk-and-mitigation [strategy + risk categories]
/war-gaming [strategy + top threats]
/kpi-architect [strategy + current metrics]
/value-realization [initiative + benefits promised]

Step 6 — Communicate:
/stakeholder-alignment [strategy + stakeholder map]
/narrative-builder [analysis + audience]
/decision-memo [decision + recommendation + evidence]
```

---

*Generated: 2026-06-18 | Source: Anthropic × BCG "Consultant's Guide to Claude"*
*Skills repo: `/home/sheke/.claude/skills/strategy-consulting/`*
*Format: LinkedIn post + Claude prompt per skill | Total: 21 skills + 1 OS chain*
