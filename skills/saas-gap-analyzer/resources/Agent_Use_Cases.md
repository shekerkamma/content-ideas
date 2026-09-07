# Agent Replacement Scorecard - Top 25 Use Cases

This document contains 25 agentic use cases across 6 agent types and 11 industries, extracted from the Agent Replacement Scorecard.

### Conversational support
- **Agent Type**: Customer
- **SaaS Affected**: Per-seat help desks (Zendesk)
- **Verdict**: REPLACE
- **Proof**: Mercedes MBUX, Wendy&#x27;s FreshAI, Home Depot Magic Apron

**Proof — what’s actually deployed**: Mercedes-Benz routes drive-time questions through its MBUX Virtual Assistant (Gemini on Vertex AI); Wendy&#x27;s FreshAI takes drive-thru orders end-to-end; Home Depot&#x27;s “Magic Apron” and Macy&#x27;s “Ask Macy&#x27;s” resolve product and order questions in-app. These are live, branded tier-1 agents already handling the bulk of routine contacts — not pilots.
**SaaS in the crosshairs**: The exposed layer is the per-seat help desk (Zendesk-class) plus QA-scoring tools and the lower tier of BPO. Once an agent resolves ~80% of volume, the buyer stops paying for ~80% of the agent seats and the remaining staff become escalation managers. The ticketing system of record can survive — the seat count is what collapses, which is why this is a clear Replace.

---

### In-product owner assistant
- **Agent Type**: Customer
- **SaaS Affected**: Manuals / FAQ / deflection tools
- **Verdict**: RENEGOTIATE
- **Proof**: Volkswagen myVW, GM OnStar

**Proof — what’s actually deployed**: Volkswagen&#x27;s myVW app lets owners ask “how do I change a flat tire?” and point a phone camera at dashboard lights for multimodal answers; GM&#x27;s OnStar assistant interprets driver intent by voice. The manual and support content is embedded directly into the product experience.
**SaaS in the crosshairs**: This enriches more than it replaces — the value sits in proprietary product data, so the OEM keeps the platform. What erodes is spend on standalone FAQ / knowledge-base tools and call-deflection add-ons, now folded into one in-product agent. Verdict leans Renegotiate: keep the system, drop the bolt-ons.

---

### AI shopping / sales consultant
- **Agent Type**: Customer
- **SaaS Affected**: Guided-selling SaaS
- **Verdict**: REPLACE
- **Proof**: Mercedes smart sales, Mobiauto, Best Buy

**Proof — what’s actually deployed**: Mercedes-Benz added a gen-AI smart sales assistant to its online storefront; Mobiauto&#x27;s “Shopping Consultant” (Gemini + BigQuery) recommends the ideal car and auto-generates listings; Best Buy uses conversational agents for guided product selection. The agent does the consultative selling a human associate or a guided-selling tool used to script.
**SaaS in the crosshairs**: Guided-selling and product-recommendation SaaS — the per-seat configure / quote and merchandising assistants — is the exposed layer. An agent grounded in the catalog and inventory does this natively, so the per-seat tooling compresses. The commerce platform itself stays as system of record. Replace.

---

### Travel &amp; booking planner
- **Agent Type**: Customer
- **SaaS Affected**: Booking / itinerary tools
- **Verdict**: REPLACE
- **Proof**: Agoda, Priceline, LATAM Cosmos, Virgin Voyages

**Proof — what’s actually deployed**: Agoda&#x27;s AI Vacation Planner, Priceline&#x27;s trip tools, LATAM Airlines&#x27; “Cosmos” and Virgin Voyages&#x27; “Rovey” turn a natural-language request into a built itinerary against live inventory. The agent owns the plan-and-book loop end to end.
**SaaS in the crosshairs**: Standalone itinerary builders and booking-assist seats are displaced; the agent reads inventory / PMS via API and assembles the trip. The reservation system of record stays, but the human-facing booking-tool seats shrink. Replace.

---

### Messaging-channel chatbot
- **Agent Type**: Customer
- **SaaS Affected**: Chatbot / CCaaS bots
- **Verdict**: REPLACE
- **Proof**: LUXGEN (LINE), Banglalink REN, DT MINDR

**Proof — what’s actually deployed**: LUXGEN runs a Vertex AI agent on its official LINE account that cut human customer-service workload by ~30%; Banglalink&#x27;s “REN” and Deutsche Telekom&#x27;s “MINDR” handle high-volume conversational support on messaging channels. These are deterministic, high-throughput deflection agents.
**SaaS in the crosshairs**: Per-seat chatbot builders and CCaaS bot modules are the target — the same flows now run on a general agent at a fraction of the per-seat cost. The contact-center platform can remain; the bot-builder licenses do not. Replace.

---

### Enterprise knowledge search
- **Agent Type**: Employee
- **SaaS Affected**: Enterprise search SaaS
- **Verdict**: RENEGOTIATE
- **Proof**: Geotab, Bosch AskBosch, Glean

**Proof — what’s actually deployed**: Geotab moved research, document summarization, and status reporting onto Google Workspace with Gemini across HR and engineering; Bosch&#x27;s “AskBosch” and Glean surface answers across internal systems. The agent retrieves and synthesizes across silos on demand.
**SaaS in the crosshairs**: Standalone enterprise-search SaaS is squeezed because the agent indexes your own corpus and answers directly. But the value is your proprietary data, so you keep the substrate and trim the search seats. Renegotiate — agent over your data, fewer licenses.

---

### Doc summarization &amp; drafting
- **Agent Type**: Employee
- **SaaS Affected**: Doc / productivity add-ons
- **Verdict**: REPLACE
- **Proof**: KPMG, PwC, Deloitte

**Proof — what’s actually deployed**: KPMG, PwC, and Deloitte deploy agents that summarize, review, and draft across engagements — collapsing a manual research-and-brief task that used to eat an hour into a usable first draft in minutes.
**SaaS in the crosshairs**: This is native LLM capability, so per-seat document-productivity add-ons lose their reason to exist. The office suite stays; the bolt-on summarization / drafting seats go. Replace at the add-on layer.

---

### Contact-center agent assist
- **Agent Type**: Employee
- **SaaS Affected**: CCaaS agent-assist
- **Verdict**: RENEGOTIATE
- **Proof**: Humana Agent Assist, Vodafone

**Proof — what’s actually deployed**: Humana&#x27;s Agent Assist surfaces next-best actions to live reps in real time; Vodafone uses agents to guide and automate contact-center work. The agent rides alongside the human rather than replacing them.
**SaaS in the crosshairs**: This enriches the CCaaS platform rather than replacing it — but it displaces separate agent-assist and real-time-guidance add-ons. Keep the contact-center system of record; renegotiate the assist module. Renegotiate.

---

### Legal research &amp; drafting
- **Agent Type**: Employee
- **SaaS Affected**: Westlaw, LexisNexis, CLM
- **Verdict**: REPLACE
- **Proof**: Harvey, Thomson Reuters, Deutsche Bank DB Lumina

**Proof — what’s actually deployed**: Harvey and Legora run research, review, and drafting for AmLaw firms; Thomson Reuters embeds gen-AI research; Deutsche Bank&#x27;s “DB Lumina” drafts research at scale. Firms are quietly trimming junior classes citing the productivity gain.
**SaaS in the crosshairs**: Per-lawyer research platforms (Westlaw, LexisNexis) and contract-lifecycle tools are repricing fast as the agent does the lookup-and-draft loop. The proprietary case-law corpus retains value, but per-seat research licenses compress. Replace at the seat layer.

---

### HR / onboarding agent
- **Agent Type**: Employee
- **SaaS Affected**: HR workflow SaaS
- **Verdict**: RENEGOTIATE
- **Proof**: Grupo Ruiz, employee-agent deployments

**Proof — what’s actually deployed**: Grupo Ruiz uses Gemini Enterprise to streamline team workflows; employee-agent deployments orchestrate onboarding tasks, time-off requests, and policy questions. The agent runs the repetitive HR workflow end to end.
**SaaS in the crosshairs**: HR workflow SaaS keeps its system-of-record role (payroll, employee records), but the per-seat workflow and case-management modules are exposed to an agent that executes inside them. Renegotiate — keep the SoR, drop the workflow seats.

---

### Ad &amp; creative generation at scale
- **Agent Type**: Creative
- **SaaS Affected**: Creative production seats
- **Verdict**: REPLACE
- **Proof**: WPP, Authentic Brands Group, PODS

**Proof — what’s actually deployed**: WPP and Authentic Brands Group turn a single hypothesis into hundreds-to-thousands of personalized creative variations in hours; PODS built the “World&#x27;s Smartest Billboard” that generated 6,000+ headlines across NYC neighborhoods in 29 hours. Creative becomes a computational process.
**SaaS in the crosshairs**: Per-editor creative-production seats and the freelance long tail are displaced as generation moves from manual to computational. Brand / DAM systems stay; production seats shrink hard. Replace.

---

### Video generation
- **Agent Type**: Creative
- **SaaS Affected**: Video editing SaaS
- **Verdict**: RENEGOTIATE
- **Proof**: Veo deployments, Adobe

**Proof — what’s actually deployed**: Veo deployments and Adobe&#x27;s gen-video tools produce and edit footage from prompts; brands spin cinematic variations without a full production cycle. The agent drafts; editors refine the final cut.
**SaaS in the crosshairs**: Video-editing SaaS is partially displaced — the agent handles first-pass generation while editors finish high-stakes work. Hybrid: agent does the volume, humans own the last mile. Renegotiate.

---

### Personalized marketing content
- **Agent Type**: Creative
- **SaaS Affected**: Marketing content tools
- **Verdict**: REPLACE
- **Proof**: Adobe, ElevenLabs (voice)

**Proof — what’s actually deployed**: Adobe&#x27;s gen workflows and ElevenLabs&#x27; voice generation produce hyper-personalized, real-time creative; marketing teams generate variant copy, voice, and assets on demand instead of producing each by hand.
**SaaS in the crosshairs**: Per-seat marketing-content and copy tools are displaced by an agent that generates on brief. The campaign / martech platform stays as orchestration; the content-tool seats go. Replace at the content layer.

---

### Brand / 3D asset generation
- **Agent Type**: Creative
- **SaaS Affected**: Asset / DAM tooling
- **Verdict**: KEEP
- **Proof**: BMW Group SORDI.ai

**Proof — what’s actually deployed**: BMW Group&#x27;s SORDI.ai generates large synthetic 3D datasets and brand assets for industrial and creative use. The agent feeds a managed asset pipeline rather than replacing it.
**SaaS in the crosshairs**: The DAM / asset system remains the system of record and compounds in value as the agent fills it; tooling spend shifts rather than disappears. Keep — the agent enriches the moat.

---

### AI code assistant
- **Agent Type**: Code
- **SaaS Affected**: IDE / code-review add-ons
- **Verdict**: RENEGOTIATE
- **Proof**: Valeo, Broadcom (Gemini Code Assist)

**Proof — what’s actually deployed**: Valeo and Broadcom deploy Gemini Code Assist across engineering; developers move faster through problems they already understand. The assistant augments the IDE, not the engineer&#x27;s judgment.
**SaaS in the crosshairs**: This enriches the developer toolchain; the shift is from per-seat add-ons to consumption-based assistance. Architectural judgment still sits with humans. Renegotiate — consumption, not seats.

---

### Legacy-IT modernization (NL→SAP)
- **Agent Type**: Code
- **SaaS Affected**: Modernization consulting / tools
- **Verdict**: KEEP
- **Proof**: Suzano, Deutsche Telekom

**Proof — what’s actually deployed**: Suzano and Deutsche Telekom use Gemini to put natural-language interfaces over 40-year-old SAP, mainframe, and COBOL systems — letting non-technical staff query siloed data without a costly migration.
**SaaS in the crosshairs**: This is pure enrichment — the agent unlocks the legacy system rather than replacing it, and the system of record becomes more valuable. Modernization consulting / tooling spend shifts to the agent layer. Keep.

---

### App build / migration automation
- **Agent Type**: Code
- **SaaS Affected**: Low-code &amp; migration tooling
- **Verdict**: RENEGOTIATE
- **Proof**: Code-agent deployments

**Proof — what’s actually deployed**: Code-agent deployments scaffold applications and automate migrations that used to require specialist teams; experienced engineers ship faster while the agent handles boilerplate and conversions.
**SaaS in the crosshairs**: Low-code builders and migration tooling are partially displaced where the workflow is well-defined, but complex / bespoke work still needs humans. Hybrid — the agent replaces the routine slice. Renegotiate.

---

### NL analytics (text-to-SQL)
- **Agent Type**: Data
- **SaaS Affected**: BI dashboards (Looker-class)
- **Verdict**: RENEGOTIATE
- **Proof**: Spotify, Etsy (BigQuery)

**Proof — what’s actually deployed**: Spotify and Etsy let teams ask questions of BigQuery in natural language instead of building dashboards; the agent writes the query and returns the answer.
**SaaS in the crosshairs**: BI dashboard seats (Looker-class) are squeezed because the agent collapses the interface and answers directly — but the warehouse remains the system of record and a verification / dashboard layer stays for trust. Hybrid: trim BI seats, keep the warehouse. Renegotiate.

---

### Document AI / extraction
- **Agent Type**: Data
- **SaaS Affected**: IDP / OCR SaaS
- **Verdict**: REPLACE
- **Proof**: Document AI deployments

**Proof — what’s actually deployed**: Document AI deployments parse invoices, forms, and contracts at scale, replacing manual keying and template-based capture. Output is structured and deterministic.
**SaaS in the crosshairs**: IDP / OCR SaaS is directly displaced — the agent extracts and routes natively, absorbing the clerk role. The downstream system of record stays; the capture-tool seats go. Replace.

---

### Forecasting / predictive ops
- **Agent Type**: Data
- **SaaS Affected**: Predictive-analytics SaaS
- **Verdict**: KEEP
- **Proof**: Honeywell, Geotab

**Proof — what’s actually deployed**: Honeywell and Geotab apply agents to predictive maintenance and fleet / operations forecasting on top of proprietary sensor and telematics data. The agent augments existing models.
**SaaS in the crosshairs**: Predictive-analytics SaaS is enriched, not replaced — the moat is the operational data feeding the forecast. Spend consolidates onto the platform that owns the data. Keep.

---

### Research &amp; insight agent
- **Agent Type**: Data
- **SaaS Affected**: Market-research tooling
- **Verdict**: RENEGOTIATE
- **Proof**: MLB Scout Insights, NotebookLM

**Proof — what’s actually deployed**: MLB&#x27;s “Scout Insights” and NotebookLM-style agents synthesize large corpora into briefings; teams get a usable insight package in minutes instead of days.
**SaaS in the crosshairs**: Standalone market-research and insight tooling seats are displaced by an agent that synthesizes on demand, but proprietary data sources retain value. Renegotiate — fewer research-tool seats.

---

### Threat detection / SecOps
- **Agent Type**: Security
- **SaaS Affected**: SIEM tier-1
- **Verdict**: KEEP
- **Proof**: Google Security Operations deployments

**Proof — what’s actually deployed**: Google Security Operations deployments correlate signals and surface threats; security teams move from manual triage to agent-surfaced detection. The agent rides on the SIEM&#x27;s data.
**SaaS in the crosshairs**: SIEM tier-1 work is enriched — the agent reduces toil, but the SIEM remains the system of record and the incident history is the moat. Keep the platform; the L1 seat compresses.

---

### Agentic auto-remediation
- **Agent Type**: Security
- **SaaS Affected**: SOAR / runbooks
- **Verdict**: REPLACE
- **Proof**: Security-agent deployments

**Proof — what’s actually deployed**: Security-agent deployments write detection rules, isolate compromised workloads, and deploy honeytokens autonomously — neutralizing tier-1 threats without human intervention, within a policy envelope.
**SaaS in the crosshairs**: SOAR and runbook-automation seats are displaced as the agent becomes the responder. The system of record stays for audit; the playbook-authoring seats go. Replace within policy.

---

### Fraud &amp; risk detection
- **Agent Type**: Security
- **SaaS Affected**: Fraud / risk add-ons
- **Verdict**: KEEP
- **Proof**: Citi, Wells Fargo, Commerzbank Bene

**Proof — what’s actually deployed**: Citi and Wells Fargo apply agents to risk and fraud analysis; Commerzbank&#x27;s “Bene” assists risk workflows. The agent enriches detection on top of proprietary transaction data.
**SaaS in the crosshairs**: Fraud / risk add-ons are enriched, not replaced — the bank&#x27;s data and models are the moat, and being wrong is expensive, so humans stay in the loop. Keep — the agent augments, the data wins.

---

### Compliance &amp; audit agent
- **Agent Type**: Security
- **SaaS Affected**: GRC tooling
- **Verdict**: KEEP
- **Proof**: U.S. FDA, regulated deployments

**Proof — what’s actually deployed**: The U.S. Food and Drug Administration and other regulated bodies use agents to draft and review compliance documentation; the agent prepares, a human signs off. Auditability is mandatory.
**SaaS in the crosshairs**: GRC tooling stays the system of record because of audit and regulatory requirements; the agent drafts and accelerates rather than displacing the platform. Keep.

---

