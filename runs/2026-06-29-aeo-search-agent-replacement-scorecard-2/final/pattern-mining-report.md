# AEO Semantic Pattern Mining Report: Agent Replacement Scorecard

## Purpose

This report mines captured AI-answer evidence for semantic pattern candidates. It does not use exact keyword-to-pattern hits as the basis for claims. It extracts answer evidence units, scores them against concept anchors, and requires semantic review before promotion.

## Evidence Base

- Run id: `2026-06-29-aeo-search-agent-replacement-scorecard-2`
- Captures analyzed: 12
- Evidence units analyzed: 542
- Evidence mix: {"manual_live_capture": 12}
- Engine evidence units: {"ChatGPT": 2, "Perplexity": 2, "Claude": 168, "Google AI Mode": 370}
- Target-seeded evidence units: 4

## Pattern Candidates

### Add-On Collapse (medium)

AI absorbs assistant modules, point tools, bolt-on workflow products, or specialist add-ons while the buyer keeps the core platform or system of record.

- Review question: Does the answer distinguish the durable core platform from replaceable add-ons or modules?
- Confidence rationale: Repeated across multiple captures and engines.
- Evidence captures: cap_live_004, cap_live_005, cap_live_007, cap_live_008, cap_live_009, cap_live_010, cap_live_012
- Engines: Claude, Google AI Mode
- Query intents: commercial investigation
- Source domains: none
- Evidence types: manual_live_capture
- Review status: needs_semantic_review

Representative evidence:

- `cap_live_008_u02` (Google AI Mode, score 0.25): The workflow revolves around these platforms.
- `cap_live_007_u01` (Claude, score 0.237): # Typical Support Software & Workflows ## Common Tools Teams Use **Helpdesk Platforms:**
- `cap_live_004_u04` (Google AI Mode, score 0.226): Core Workflow & Traditional Software (The Foundation)** Regardless of AI, a structured workflow is essential.

### Human Sign-Off Boundary (medium)

AI drafts, triages, recommends, or executes low-risk work while humans retain accountability for regulated, ambiguous, high-risk, or customer-sensitive decisions.

- Review question: Does the answer define where human approval or accountability remains necessary?
- Confidence rationale: Repeated across multiple captures and engines.
- Evidence captures: cap_live_005, cap_live_007, cap_live_008, cap_live_009, cap_live_010, cap_live_012
- Engines: Claude, Google AI Mode
- Query intents: commercial investigation
- Source domains: none
- Evidence types: manual_live_capture
- Review status: needs_semantic_review

Representative evidence:

- `cap_live_009_u20` (Claude, score 0.267): Requires human checkpoints at each stage ## Realistic Adoption Pattern **What actually works:** ``` Human defines scope → AI generates draft → Human edits → AI reformats → Human approves ``` **Not:** AI does everything autonomously **Successful teams use AI as:**
- `cap_live_005_u34` (Claude, score 0.194): **Multi-agent systems** (specialist bots for different departments) ## Bottom Line AI works as a **first-line triage and simple resolution tool**, not a complete human replacement.
- `cap_live_008_u49` (Google AI Mode, score 0.169): **Ambiguous or Vague Language:** Humans are better at interpreting unclear requests or reading between the lines.

### Data Moat Survival (medium)

Platforms survive when proprietary data, permissions, historical records, audit trails, governance, or operational context are the source of defensibility.

- Review question: Does the answer explain why a data-rich platform survives rather than gets replaced?
- Confidence rationale: Repeated across multiple captures and engines.
- Evidence captures: cap_live_003, cap_live_004, cap_live_006, cap_live_010, cap_live_012
- Engines: Claude, Google AI Mode
- Query intents: commercial investigation
- Source domains: none
- Evidence types: manual_live_capture
- Review status: needs_semantic_review

Representative evidence:

- `cap_live_006_u31` (Google AI Mode, score 0.239): Implement RAG to connect it to proprietary data.
- `cap_live_004_u26` (Google AI Mode, score 0.231): * **Data Feeds:** Integrate with product catalogs, CRM, or other data sources to personalize ads.
- `cap_live_006_u29` (Google AI Mode, score 0.2): **Data Collection & Preparation:** Gather all relevant product data, FAQs, historical customer interactions, sales scripts, and policies.

### Pilotability (medium)

The workflow can be tested in a bounded pilot using historical examples, parallel runs, measurable outputs, cycle time, exception rate, resolution rate, or human escalation quality.

- Review question: Does the answer describe a concrete way to test the replacement or renegotiation thesis?
- Confidence rationale: Repeated across multiple captures and engines.
- Evidence captures: cap_live_005, cap_live_006, cap_live_008, cap_live_010, cap_live_012
- Engines: Claude, Google AI Mode
- Query intents: commercial investigation
- Source domains: none
- Evidence types: manual_live_capture
- Review status: needs_semantic_review

Representative evidence:

- `cap_live_005_u07` (Claude, score 0.32): 70-80% resolution rate for common questions 3.
- `cap_live_005_u26` (Claude, score 0.261): **Containment rate**: % resolved without human (target: 40-70%)
- `cap_live_006_u26` (Google AI Mode, score 0.251): * **BI Tools:** Tableau, Power BI, Looker (for analyzing business metrics like conversion rates, resolution rates, customer satisfaction, and common queries).

### Renewal Leverage (medium)

A credible agent alternative changes procurement leverage, renewal negotiations, pricing models, seat commitments, outcome pricing, or vendor consolidation decisions.

- Review question: Does the answer connect agent capability to procurement, pricing, or renewal pressure?
- Confidence rationale: Repeated across multiple captures and engines.
- Evidence captures: cap_live_005, cap_live_006, cap_live_008, cap_live_009, cap_live_010
- Engines: Claude, Google AI Mode
- Query intents: commercial investigation
- Source domains: none
- Evidence types: manual_live_capture
- Review status: needs_semantic_review

Representative evidence:

- `cap_live_005_u13` (Claude, score 0.187): Custom pricing, bulk discounts, contract terms
- `cap_live_008_u19` (Google AI Mode, score 0.173): **Agent Interaction:** * An agent claims the ticket.
- `cap_live_006_u57` (Google AI Mode, score 0.162): **Creative Problem-Solving & Negotiation:** AI agents struggle with truly novel solutions or complex negotiation strategies that require adaptability and understanding of human psychology.

### Seat Compression (medium)

AI agents reduce paid user licenses, support seats, operator headcount, or per-seat software demand by completing the work that humans previously performed inside a SaaS interface.

- Review question: Does the answer describe fewer humans or paid seats needed to complete the same workflow?
- Confidence rationale: Repeated across multiple captures and engines.
- Evidence captures: cap_live_006, cap_live_007, cap_live_008, cap_live_009
- Engines: Claude, Google AI Mode
- Query intents: commercial investigation
- Source domains: none
- Evidence types: manual_live_capture
- Review status: needs_semantic_review

Representative evidence:

- `cap_live_006_u50` (Google AI Mode, score 0.224): **Multilingual Support:** Easily offering support in multiple languages without the need for human agents for each language.
- `cap_live_008_u03` (Google AI Mode, score 0.224): ### Software and Workflow for Conversational Support **Core Software Categories:** 1.
- `cap_live_008_u38` (Google AI Mode, score 0.204): **Agent Assist (for human agents):** AI tools can suggest relevant knowledge base articles, canned responses, or even analyze sentiment to help human agents provide better, faster service.

### Workflow Layer Replacement (low)

AI replaces the task execution layer of a workflow while records, databases, inventory systems, CRMs, ERPs, or compliance systems remain as durable systems underneath.

- Review question: Does the answer separate workflow execution from the underlying record system?
- Confidence rationale: Capture text or prompts are target-seeded; requires independent prompts.
- Evidence captures: cap_live_002, cap_live_003, cap_live_005, cap_live_006, cap_live_007, cap_live_009, cap_live_010, cap_live_012
- Engines: Claude, Google AI Mode, Perplexity
- Query intents: captured answer evidence, commercial investigation
- Source domains: shekerkamma.github.io
- Evidence types: manual_live_capture
- Review status: needs_semantic_review

Representative evidence:

- `cap_live_002_u02` (Perplexity, score 0.295 target-seeded): The Agent Replacement Scorecard argues that high-volume deterministic workflows with weak data moats are replace candidates, while strong systems of record are more likely to be kept and enriched.
- `cap_live_012_u32` (Google AI Mode, score 0.287): * **General Enterprise Systems:** SharePoint, Google Drive/Workspace, OneDrive are also used, though often for less sensitive or internal-facing documents, or as a secondary system.
- `cap_live_003_u05` (Claude, score 0.28): DAM systems for organizing thousands of assets

### Citation Authority Gap (low)

AI answers rely on external authorities, cited pages, comparison sources, community discussions, or trusted domains; the target asset must earn citation eligibility in those answer surfaces.

- Review question: Does the answer reveal which authorities or sources shape the recommendation?
- Confidence rationale: Needs more independent captures before promotion.
- Evidence captures: cap_live_003, cap_live_007
- Engines: Claude
- Query intents: commercial investigation
- Source domains: none
- Evidence types: manual_live_capture
- Review status: needs_semantic_review

Representative evidence:

- `cap_live_007_u14` (Claude, score 0.174): Helping *agents* find answers quickly from docs
- `cap_live_007_u19` (Claude, score 0.174): When the answer isn't in the documentation **Account actions with risk:**
- `cap_live_003_u30` (Claude, score 0.123): Tracking which asset is which across platforms 4.

### Interface Collapse (low)

Users stop navigating dashboards, search interfaces, reports, forms, or multi-screen tools because a natural-language answer layer gives them the needed outcome directly.

- Review question: Does the answer imply the user interface becomes less important than the answer/action layer?
- Confidence rationale: Needs more independent captures before promotion.
- Evidence captures: cap_live_004, cap_live_010
- Engines: Google AI Mode
- Query intents: commercial investigation
- Source domains: none
- Evidence types: manual_live_capture
- Review status: needs_semantic_review

Representative evidence:

- `cap_live_004_u62` (Google AI Mode, score 0.146): * **AI Agents/Tools:** ChatGPT (with web access), Perplexity AI, specialized research tools.
- `cap_live_010_u08` (Google AI Mode, score 0.125): * **Summarization:** Users copy-paste text into Google's AI tools or use built-in summarization features in Docs/Meet transcripts.
- `cap_live_004_u83` (Google AI Mode, score 0.121): It's a tool, not an autonomous creative director.

## Cited / Referenced Domains

- shekerkamma.github.io: 4

## Subagent Review Required

Before using any pattern externally, send `working/subagent-review-brief.md` to independent reviewers. One reviewer should validate whether the evidence really supports each pattern. Another should try to falsify the pattern and identify missing competitor/source evidence.

## How To Use This

Promote a pattern only when semantic review agrees that the evidence supports the mechanism, the captures are independent, and the cited/source landscape is strong enough. Treat low-confidence or target-seeded candidates as workflow validation, not market truth.
