# Agentic SaaS Exposure Diagnostic

## Executive Thesis

AI agents do not replace all SaaS. They replace the workflow layer where task volume is high, output is deterministic, and the underlying data moat is weak. They renegotiate seat economics where the system of record remains valuable but workflow seats shrink. They enrich platforms where proprietary data, auditability, or operational history is the moat.

This diagnostic converts the Agent Replacement Scorecard into a pre-sales conversation asset: which software categories are exposed, what has already been deployed, and where a buyer should run a fast agent pilot.

## Scorecard Snapshot

- Source: https://shekerkamma.github.io/content-ideas/scorecard.html
- Use cases analyzed: 25
- Replace: 10
- Renegotiate: 9
- Keep: 6
- Agent types: Code, Creative, Customer, Data, Employee, Security

## Buyer Interpretation

- **Replace** means the buyer should run build-vs-buy math immediately. The exposed spend is usually per-seat workflow tooling, BPO, or low-moat add-ons.
- **Renegotiate** means the buyer should keep the core platform but challenge per-seat modules, assistant add-ons, or workflow licenses.
- **Keep** means the platform owns data, audit trail, or system-of-record gravity. The agent should ride on top via API/MCP rather than replace the platform.

## Highest-Exposure Replace Zones

- **Conversational support** (Customer, Replace): Per-seat help desks (Zendesk) | proof: Mercedes MBUX, Wendy's FreshAI, Home Depot Magic Apron | why it matters: 80 support seats → 1 agent + KB.
- **Messaging-channel chatbot** (Customer, Replace): Chatbot / CCaaS bots | proof: LUXGEN (LINE), Banglalink REN, DT MINDR | why it matters: Bot-builder seats → 1 agent.
- **Document AI / extraction** (Data, Replace): IDP / OCR SaaS | proof: Document AI deployments | why it matters: IDP/OCR seats → agent + Document AI.
- **Agentic auto-remediation** (Security, Replace): SOAR / runbooks | proof: Security-agent deployments | why it matters: SOAR/runbook seats → agent in policy.
- **AI shopping / sales consultant** (Customer, Replace): Guided-selling SaaS | proof: Mercedes smart sales, Mobiauto, Best Buy | why it matters: Guided-selling seats → 1 agent.
- **Travel & booking planner** (Customer, Replace): Booking / itinerary tools | proof: Agoda, Priceline, LATAM Cosmos, Virgin Voyages | why it matters: Booking seats → agent + inventory API.
- **Doc summarization & drafting** (Employee, Replace): Doc / productivity add-ons | proof: KPMG, PwC, Deloitte | why it matters: Native LLM; drop add-on seats.
- **Ad & creative generation at scale** (Creative, Replace): Creative production seats | proof: WPP, Authentic Brands Group, PODS | why it matters: Production seats → gen pipeline.
- **Personalized marketing content** (Creative, Replace): Marketing content tools | proof: Adobe, ElevenLabs (voice) | why it matters: Content-tool seats → agent.
- **Legal research & drafting** (Employee, Replace): Westlaw, LexisNexis, CLM | proof: Harvey, Thomson Reuters, Deutsche Bank DB Lumina | why it matters: Per-lawyer research seats → agent.

## Renegotiate Zones

- **Enterprise knowledge search** (Employee, Renegotiate): Enterprise search SaaS | proof: Geotab, Bosch AskBosch, Glean | why it matters: Agent over your data; trim search seats.
- **Contact-center agent assist** (Employee, Renegotiate): CCaaS agent-assist | proof: Humana Agent Assist, Vodafone | why it matters: Keep CCaaS; agent-assist replaces add-on.
- **AI code assistant** (Code, Renegotiate): IDE / code-review add-ons | proof: Valeo, Broadcom (Gemini Code Assist) | why it matters: Enriches IDE; consumption not seats.
- **NL analytics (text-to-SQL)** (Data, Renegotiate): BI dashboards (Looker-class) | proof: Spotify, Etsy (BigQuery) | why it matters: Agent over warehouse; trim BI seats.
- **HR / onboarding agent** (Employee, Renegotiate): HR workflow SaaS | proof: Grupo Ruiz, employee-agent deployments | why it matters: Agent runs workflow; keep record system.
- **In-product owner assistant** (Customer, Renegotiate): Manuals / FAQ / deflection tools | proof: Volkswagen myVW, GM OnStar | why it matters: Keep platform; drop deflection seats.

## Keep / Enrich Zones

- **Threat detection / SecOps** (Security, Keep): SIEM tier-1 | proof: Google Security Operations deployments | why it matters: Agent rides on SIEM; keep record system.
- **Fraud & risk detection** (Security, Keep): Fraud / risk add-ons | proof: Citi, Wells Fargo, Commerzbank Bene | why it matters: Agent enriches; proprietary data wins.
- **Brand / 3D asset generation** (Creative, Keep): Asset / DAM tooling | proof: BMW Group SORDI.ai | why it matters: DAM stays SoR; agent feeds it.
- **Forecasting / predictive ops** (Data, Keep): Predictive-analytics SaaS | proof: Honeywell, Geotab | why it matters: Agent augments; data moat compounds.
- **Compliance & audit agent** (Security, Keep): GRC tooling | proof: U.S. FDA, regulated deployments | why it matters: Agent drafts; GRC stays record system.
- **Legacy-IT modernization (NL→SAP)** (Code, Keep): Modernization consulting / tools | proof: Suzano, Deutsche Telekom | why it matters: Agent unlocks legacy; keep core systems.

## What This Means For A Buyer

1. Inventory your software stack by workflow, not vendor.
2. Mark each workflow by volume, determinism, and data moat.
3. For high-volume, deterministic, low-moat workflows, run a two-week parallel agent pilot.
4. For high-moat systems, keep the platform and move spend from seats to agent access, API usage, or outcome pricing.
5. Use the scorecard as renewal leverage: seat compression is now a credible alternative, not a theoretical threat.

## Two-Week Pilot Path

Week 1:
- Pick one Replace workflow with clear input/output boundaries.
- Export 50-100 historical examples.
- Build an agent loop that drafts or resolves the task while preserving human review.
- Measure resolution rate, cycle time, exception rate, and human escalation quality.

Week 2:
- Run the agent in parallel with the current SaaS workflow.
- Compare cost per completed task against seat/tool spend.
- Identify which records must remain in the system of record.
- Decide: replace workflow layer, renegotiate module/seat pricing, or keep and enrich.

## Where AEO Fits

This diagnostic also creates the AEO job: when buyers ask AI systems which SaaS categories agents can replace, this scorecard should be cited. The AEO workflow should track whether AI answers surface this asset, which sources they cite instead, and which content or citation gaps prevent the scorecard from winning the recommendation.

## Recommended Next Action

Use this diagnostic as the first pre-sales artifact. For a named prospect, map their stack against the 25 archetypes, then produce a custom Keep / Renegotiate / Replace view and a two-week pilot recommendation.

## Method Note

The scorecard verdicts are directional strategy judgments from named deployment examples. They are not measured replacement counts. A prospect-specific diagnostic should verify source claims, software spend, workflow volume, integration constraints, compliance boundaries, and human-review requirements before recommending replacement.
