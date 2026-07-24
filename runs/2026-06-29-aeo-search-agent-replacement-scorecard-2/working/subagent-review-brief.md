# Subagent Review Brief: Agent Replacement Scorecard AEO Patterns

## Assignment

Review the semantic pattern candidates below. Do not accept a candidate because the label sounds plausible. Decide whether the evidence units actually support the mechanism, whether the captures are independent, and what evidence is missing.

## Evidence Warnings

- Captures: 12
- Evidence mix: {"manual_live_capture": 12}
- Target-seeded evidence units: 4

## Review Output Schema

Return JSON lines with: `pattern_id`, `decision` (`accept`, `revise`, `reject`), `rationale`, `missing_evidence`, `better_label`.

## Candidates

### add-on-collapse - Add-On Collapse

Question: Does the answer distinguish the durable core platform from replaceable add-ons or modules?
Current confidence: medium (Repeated across multiple captures and engines.)

- cap_live_008_u02 [Google AI Mode | commercial investigation | best conversational support platforms]: The workflow revolves around these platforms.
- cap_live_007_u01 [Claude | commercial investigation | best conversational support platforms]: # Typical Support Software & Workflows ## Common Tools Teams Use **Helpdesk Platforms:**
- cap_live_004_u04 [Google AI Mode | commercial investigation | best ad & creative generation at scale wpp, authentic brands group, pods creative production seats creative platforms]: Core Workflow & Traditional Software (The Foundation)** Regardless of AI, a structured workflow is essential.
- cap_live_010_u04 [Google AI Mode | commercial investigation | best doc summarization & drafting kpmg, pwc, deloitte doc / productivity add-ons empl platforms]: ### Core Collaboration & Document Management Tools These are the foundational platforms where the actual documents live and are shared.
- cap_live_008_u04 [Google AI Mode | commercial investigation | best conversational support platforms]: **Customer Support Platforms / Help Desks:** These are the foundational tools.

### human-signoff-boundary - Human Sign-Off Boundary

Question: Does the answer define where human approval or accountability remains necessary?
Current confidence: medium (Repeated across multiple captures and engines.)

- cap_live_009_u20 [Claude | commercial investigation | best doc summarization & drafting kpmg, pwc, deloitte doc / productivity add-ons empl platforms]: Requires human checkpoints at each stage ## Realistic Adoption Pattern **What actually works:** ``` Human defines scope → AI generates draft → Human edits → AI reformats → Human approves ``` **Not:** AI does everything autonomously **Successful teams use AI as:**
- cap_live_005_u34 [Claude | commercial investigation | best ai shopping / sales consultant platforms]: **Multi-agent systems** (specialist bots for different departments) ## Bottom Line AI works as a **first-line triage and simple resolution tool**, not a complete human replacement.
- cap_live_008_u49 [Google AI Mode | commercial investigation | best conversational support platforms]: **Ambiguous or Vague Language:** Humans are better at interpreting unclear requests or reading between the lines.
- cap_live_010_u26 [Google AI Mode | commercial investigation | best doc summarization & drafting kpmg, pwc, deloitte doc / productivity add-ons empl platforms]: **First Draft Generation (AI-assisted):** * Provide the AI with the outline and key information, asking it to draft sections or even the whole document (e.g., "Draft a project proposal for X, based on these points...").
- cap_live_012_u59 [Google AI Mode | commercial investigation | best legal research & drafting harvey, thomson reuters, deutsche bank db lumina westlaw, lexisnexis, clm employee platforms]: * **Initial Draft Generation:** For highly standardized documents or sections, AI can generate a very rough first draft.

### data-moat-survival - Data Moat Survival

Question: Does the answer explain why a data-rich platform survives rather than gets replaced?
Current confidence: medium (Repeated across multiple captures and engines.)

- cap_live_006_u31 [Google AI Mode | commercial investigation | best ai shopping / sales consultant platforms]: Implement RAG to connect it to proprietary data.
- cap_live_004_u26 [Google AI Mode | commercial investigation | best ad & creative generation at scale wpp, authentic brands group, pods creative production seats creative platforms]: * **Data Feeds:** Integrate with product catalogs, CRM, or other data sources to personalize ads.
- cap_live_006_u29 [Google AI Mode | commercial investigation | best ai shopping / sales consultant platforms]: **Data Collection & Preparation:** Gather all relevant product data, FAQs, historical customer interactions, sales scripts, and policies.
- cap_live_006_u59 [Google AI Mode | commercial investigation | best ai shopping / sales consultant platforms]: **When Data is Scarce, Ambiguous, or Outdated:** AI is only as good as the data it's trained on.
- cap_live_012_u69 [Google AI Mode | commercial investigation | best legal research & drafting harvey, thomson reuters, deutsche bank db lumina westlaw, lexisnexis, clm employee platforms]: * **Bias:** AI models trained on historical data can perpetuate or amplify existing biases in the legal system.

### pilotability - Pilotability

Question: Does the answer describe a concrete way to test the replacement or renegotiation thesis?
Current confidence: medium (Repeated across multiple captures and engines.)

- cap_live_005_u07 [Claude | commercial investigation | best ai shopping / sales consultant platforms]: 70-80% resolution rate for common questions 3.
- cap_live_005_u26 [Claude | commercial investigation | best ai shopping / sales consultant platforms]: **Containment rate**: % resolved without human (target: 40-70%)
- cap_live_006_u26 [Google AI Mode | commercial investigation | best ai shopping / sales consultant platforms]: * **BI Tools:** Tableau, Power BI, Looker (for analyzing business metrics like conversion rates, resolution rates, customer satisfaction, and common queries).
- cap_live_010_u75 [Google AI Mode | commercial investigation | best doc summarization & drafting kpmg, pwc, deloitte doc / productivity add-ons empl platforms]: * **Example:** An AI agent generating a historical report or a scientific study without its output being cross-referenced with reliable sources by a human.
- cap_live_010_u25 [Google AI Mode | commercial investigation | best doc summarization & drafting kpmg, pwc, deloitte doc / productivity add-ons empl platforms]: * Human reviews and refines this initial output.

### renewal-leverage - Renewal Leverage

Question: Does the answer connect agent capability to procurement, pricing, or renewal pressure?
Current confidence: medium (Repeated across multiple captures and engines.)

- cap_live_005_u13 [Claude | commercial investigation | best ai shopping / sales consultant platforms]: Custom pricing, bulk discounts, contract terms
- cap_live_008_u19 [Google AI Mode | commercial investigation | best conversational support platforms]: **Agent Interaction:** * An agent claims the ticket.
- cap_live_006_u57 [Google AI Mode | commercial investigation | best ai shopping / sales consultant platforms]: **Creative Problem-Solving & Negotiation:** AI agents struggle with truly novel solutions or complex negotiation strategies that require adaptability and understanding of human psychology.
- cap_live_008_u27 [Google AI Mode | commercial investigation | best conversational support platforms]: ### Where AI Agents are Realistically Useful vs.
- cap_live_010_u37 [Google AI Mode | commercial investigation | best doc summarization & drafting kpmg, pwc, deloitte doc / productivity add-ons empl platforms]: ### Where AI Agents Are Realistically Useful: 1.

### seat-compression - Seat Compression

Question: Does the answer describe fewer humans or paid seats needed to complete the same workflow?
Current confidence: medium (Repeated across multiple captures and engines.)

- cap_live_006_u50 [Google AI Mode | commercial investigation | best ai shopping / sales consultant platforms]: **Multilingual Support:** Easily offering support in multiple languages without the need for human agents for each language.
- cap_live_008_u03 [Google AI Mode | commercial investigation | best conversational support platforms]: ### Software and Workflow for Conversational Support **Core Software Categories:** 1.
- cap_live_008_u38 [Google AI Mode | commercial investigation | best conversational support platforms]: **Agent Assist (for human agents):** AI tools can suggest relevant knowledge base articles, canned responses, or even analyze sentiment to help human agents provide better, faster service.
- cap_live_009_u20 [Claude | commercial investigation | best doc summarization & drafting kpmg, pwc, deloitte doc / productivity add-ons empl platforms]: Requires human checkpoints at each stage ## Realistic Adoption Pattern **What actually works:** ``` Human defines scope → AI generates draft → Human edits → AI reformats → Human approves ``` **Not:** AI does everything autonomously **Successful teams use AI as:**
- cap_live_007_u27 [Claude | commercial investigation | best conversational support platforms]: Helps agents work faster (not replacing them entirely)

### workflow-layer-replacement - Workflow Layer Replacement

Question: Does the answer separate workflow execution from the underlying record system?
Current confidence: low (Capture text or prompts are target-seeded; requires independent prompts.)

- cap_live_002_u02 [Perplexity | captured answer evidence | Agentic AI vs SaaS replacement scorecard]: The Agent Replacement Scorecard argues that high-volume deterministic workflows with weak data moats are replace candidates, while strong systems of record are more likely to be kept and enriched.
- cap_live_012_u32 [Google AI Mode | commercial investigation | best legal research & drafting harvey, thomson reuters, deutsche bank db lumina westlaw, lexisnexis, clm employee platforms]: * **General Enterprise Systems:** SharePoint, Google Drive/Workspace, OneDrive are also used, though often for less sensitive or internal-facing documents, or as a secondary system.
- cap_live_003_u05 [Claude | commercial investigation | best ad & creative generation at scale wpp, authentic brands group, pods creative production seats creative platforms]: DAM systems for organizing thousands of assets
- cap_live_005_u20 [Claude | commercial investigation | best ai shopping / sales consultant platforms]: Requires system access and exception handling
- cap_live_009_u28 [Claude | commercial investigation | best doc summarization & drafting kpmg, pwc, deloitte doc / productivity add-ons empl platforms]: API integrations with document management systems

### citation-authority-gap - Citation Authority Gap

Question: Does the answer reveal which authorities or sources shape the recommendation?
Current confidence: low (Needs more independent captures before promotion.)

- cap_live_007_u14 [Claude | commercial investigation | best conversational support platforms]: Helping *agents* find answers quickly from docs
- cap_live_007_u19 [Claude | commercial investigation | best conversational support platforms]: When the answer isn't in the documentation **Account actions with risk:**
- cap_live_003_u30 [Claude | commercial investigation | best ad & creative generation at scale wpp, authentic brands group, pods creative production seats creative platforms]: Tracking which asset is which across platforms 4.

### interface-collapse - Interface Collapse

Question: Does the answer imply the user interface becomes less important than the answer/action layer?
Current confidence: low (Needs more independent captures before promotion.)

- cap_live_004_u62 [Google AI Mode | commercial investigation | best ad & creative generation at scale wpp, authentic brands group, pods creative production seats creative platforms]: * **AI Agents/Tools:** ChatGPT (with web access), Perplexity AI, specialized research tools.
- cap_live_010_u08 [Google AI Mode | commercial investigation | best doc summarization & drafting kpmg, pwc, deloitte doc / productivity add-ons empl platforms]: * **Summarization:** Users copy-paste text into Google's AI tools or use built-in summarization features in Docs/Meet transcripts.
- cap_live_004_u83 [Google AI Mode | commercial investigation | best ad & creative generation at scale wpp, authentic brands group, pods creative production seats creative platforms]: It's a tool, not an autonomous creative director.
- cap_live_010_u05 [Google AI Mode | commercial investigation | best doc summarization & drafting kpmg, pwc, deloitte doc / productivity add-ons empl platforms]: AI features are increasingly integrated directly into these: 1.
