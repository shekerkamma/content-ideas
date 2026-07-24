# Phase 1 Market Map

Date: 2026-06-26

This matrix is retained as a compact index for the phase-1 use cases. Canonical teardown dossiers now exist for the full manifest in `teardowns/`.

| Use case | Incumbent category | Direct threats | Pricing friction | Agentic wedge |
|---|---|---|---|---|
| In-product owner assistant | Embedded FAQ / product help | OEM manuals, app KBs, call-deflection tools | Usually hidden inside platform or support contracts | Put the assistant inside the product and remove standalone FAQ seats |
| AI shopping / sales consultant | Guided-selling SaaS | Product recommendation engines, merch tools, sales chat | Seat-based, quote-based, or bundled with commerce suites | Turn catalog + inventory into a consultative agent |
| Travel & booking planner | Booking / itinerary tools | OTA trip planners, travel agency tools, itinerary SaaS | Transaction fees, supplier commissions, and platform fees | Convert natural language into a live itinerary and booking loop |
| Messaging-channel chatbot | Chatbot / CCaaS bots | Bot-builder modules, messaging automation, CCaaS add-ons | Seat and channel pricing with enterprise minimums | Replace scripted bots with a general agent on messaging channels |
| Enterprise knowledge search | Enterprise search SaaS | Search platforms, intranet search, enterprise copilots | Per-seat knowledge/search licenses and expansion modules | Answer directly from proprietary corpus and trim seats |
| Doc summarization & drafting | Productivity / doc add-ons | Office-suite AI add-ons, research tooling | Per-seat credits and suite add-ons | Collapse research and drafting into native LLM output |
| Contact-center agent assist | CCaaS agent-assist | Real-time guidance, next-best-action, QA add-ons | Seat-based guidance add-ons and enterprise services | Keep CCaaS, replace the assist module |
| Legal research & drafting | Legal research / CLM | Westlaw, Lexis, CLM tools, legal copilots | Per-seat research licenses and enterprise quotes | Draft and research on top of legal corpora with governed review |
| Ad & creative generation at scale | Creative production seats | Production suites, agency workflows, freelance labor | Seat licenses, project fees, and services markup | Convert creative production into computational output |
| Video generation | Video editing SaaS | Gen-video tools, editing suites | Seat pricing plus render/usage add-ons | Agent does first-pass generation; editors finish the last mile |
| Personalized marketing content | Marketing content tools | Copy tools, campaign content suites, voice tools | Per-seat and usage-based content licenses | Generate variants on brief, not one asset at a time |
| Brand / 3D asset generation | DAM / asset tooling | DAM, synthetic data tooling, asset libraries | Usually platform or enterprise bundle pricing | Feed the asset pipeline rather than replacing it |
| Legacy-IT modernization (NL→SAP) | Modernization consulting / tools | Legacy query tools, SAP helpers, migration consultants | Services-heavy, project-priced, long SOW cycles | Add NL over legacy systems and shrink migration services |
| App build / migration automation | Low-code / migration tooling | Low-code builders, migration accelerators | Seat or project pricing with specialist services | Automate boilerplate and routine transformations |
| NL analytics (text-to-SQL) | BI dashboards | Dashboard tools, semantic layers, analytics copilots | Seat licensing and dashboard sprawl | Ask questions directly against the warehouse |
| Document AI / extraction | IDP / OCR SaaS | OCR, invoice capture, document extraction suites | Per-page/per-document pricing and template maintenance | Extract and route natively, replacing clerk work |
| Forecasting / predictive ops | Predictive analytics SaaS | Forecasting platforms, ops analytics tools | Often bundled into platform contracts | Keep the data moat, compress the analyst seat |
| Research & insight agent | Market research tooling | Research platforms, note tools, synthesis apps | Per-seat research licenses and premium add-ons | Synthesize briefs on demand from proprietary data |
| Threat detection / SecOps | SIEM tier-1 | SIEM, alert triage, detection engineering tools | Enterprise seat/platform pricing | Reduce triage toil while keeping the SIEM as SoR |
| Agentic auto-remediation | SOAR / runbooks | SOAR tools, playbook automation, runbook builders | Per-seat/platform plus services | Let the agent execute bounded remediation inside policy |
| Fraud & risk detection | Fraud / risk add-ons | Fraud monitoring, risk engines, alerting tools | Add-on and enterprise pricing with data dependencies | Enrich detection with proprietary transaction data |
| Compliance & audit agent | GRC tooling | GRC suites, audit workflow tools | Enterprise contracts and compliance services | Draft and package; keep humans as sign-off |

## Market-Mapping Takeaway

Across phase 1, the pattern is consistent:

- If the incumbent is seat-based, the wedge is usually to compress seats into a governed agent layer.
- If the incumbent is services-heavy, the wedge is usually to standardize the workflow and remove manual coordination.
- If the incumbent is the system of record, keep it and build the execution layer above it.

The detailed teardown dossiers now exist for the full phase-1 set, including Conversational Support, HR Onboarding Agent, KYC/AML Onboarding Agent, Prior Authorization Agent, AI Code Assistant, In-Product Owner Assistant, Agentic Auto-remediation, Compliance and Audit Agent, Financial Report Reconciliation, Fraud and Risk Detection, IT Service Desk, and Threat Detection / SecOps.
