---
slug: sap-ai-transformation
title: SAP AI Transformation
version: 0.3
template_version: 2
freshness: 2026-06-10
keywords: [sap, s/4hana, ecc, odata, btp, abap, erp ai, sap agents, joule alternative, sap modernization, sap clean core]
status: draft
---

# SAP AI Transformation — Consulting Context Pack

> v0.2 — migrated to template v2 (Constitution-aligned, CIOS-ARCH-002).
> Content seeded from established stack rules and prior agent-platform work.
> Sections marked **[NEEDS ACQUISITION]** must be filled by a curated
> research pass before this pack goes `active`.

## 1. Executive summary & point of view

SAP estates hold the enterprise's most valuable operational data behind its
most change-resistant systems. The AI transformation opportunity is to make
that estate agent-addressable — through governed APIs, not vendor copilots —
so the client owns the intelligence layer while SAP remains the system of
record.

Theses we sell:

1. **Joule is not the strategy.** We do not build on SAP Joule. The agentic
   layer should be owned by the client, not rented from the ERP vendor —
   vendor-owned copilots lock the intelligence layer to the vendor's roadmap,
   pricing, and model choices. *(Standing position — see repo CLAUDE.md.)*
2. **The reference stack is Gemini + ADK + MCP → SAP OData APIs.** SAP becomes
   a system of record reached through governed APIs; the reasoning layer sits
   outside it. This keeps the agent layer model-agnostic and swappable.
3. **Clean-core discipline and agent readiness are the same program.** The work
   that makes an S/4 migration safe (API-first extensions, no core mods) is
   exactly what makes the estate agent-addressable. Sell them as one
   transformation, not two.
4. **Scoped keys, not prompts.** ERP agents get least-privilege OData service
   accounts (read-only first; writes earned per battle-tested use case).
   A prompt is never the permission layer on a system that posts journal
   entries.
5. **Start where the data exits SAP today.** The first agent use cases live in
   the reports people export to Excel weekly — order status, P2P exceptions,
   inventory positions. High-frequency read paths, zero write risk.

## 2. Market landscape

- **Joule commercial model** (SAP's own docs): Base AI free in cloud
  subscriptions; Premium AI = PUPM packages + AI Units; agents metered per
  step (Basic 5 / Standard 10 / Advanced 25 requests; custom agents
  0.005–0.025 AI Units/step); AI Foundation on BTPEA credits (source:
  learning.sap.com Joule commercial-model + Selling SAP Business AI
  courses, 2026-03/05; sap.com/products/artificial-intelligence/pricing).
- **Adoption reality:** DSAG Investment Survey 2026 — 3% of SAP customers
  run SAP Business AI in production; 77% of AI-active enterprises use
  non-SAP tools. Joule requires RISE/GROW (on-prem excluded); ~€7/AI Unit
  min package, 150–200% overage, no public price list; agentic workloads
  consume 3–20× copilot-era AI-Unit sizing (sources: innobu.com Joule-2026
  analysis, 2026-04; finoptory.ai SAP Business AI licensing, 2026-05 —
  Tier 3, verify DSAG primary at contract time).
- **SAP's own framing:** adoption gated by readiness not technology;
  clean-core customers "better positioned for AI"; >90% of projects
  delivered by SI partners; Joule positioned as SAP's "control point for
  business interaction"; Generative UI direction = A2UI payloads → Fiori
  controls grounded in Business Data Cloud (sources: sapinsider.org Joule
  readiness, 2026-05; SAP News Center 2026-03
  [gbrain:concepts/generative-ui-sap]).
- **SAP agent shipping cadence:** 40+ agents, 2,400+ Joule skills, A2A
  protocol across 35 solutions in Q1 2026; supply-chain agents (Production
  Master Data, Material Reservation) GA Q2 2026 (sources: innobu 2026-04;
  news.sap.com Hannover Messe 2026-04). Treat as build-vs-buy benchmarks
  per use case, not as platform.
- **Forcing function:** ECC 6.0 support ends 2027-12-31 — 10,000+ customers
  face migration decisions (source: innobu, 2026-04).
- Still to research: SI competitor offerings (Accenture/Deloitte/IBM SAP-AI
  practices); third-party agent platforms targeting SAP
  **[NEEDS ACQUISITION]**.

## 3. Capabilities

What a client organization gains, staged by the §5 maturity model:

- **API-addressable estate** — OData services exposed, governed, documented
  (clean-core byproduct, PoV #3).
- **Agent-read operations** — read-only agents answering live questions over
  orders, P2P exceptions, inventory (maturity stage 3).
- **Gated agent actions** — write actions behind approval gates with scoped
  service accounts (stage 4).
- **Agent-native process redesign** — processes built around agent execution
  with human exception handling (stage 5).
- **Generative UI over SAP data** — dashboard agents on the ADK + AG-UI
  pattern, proven transferable (see §7 evidence).

## 4. Reference architectures

### A. Agent layer over SAP (primary)
- **Reasoning/orchestration:** Google ADK agents (`gemini-2.5-flash` for
  interactive — 3.5-flash free-tier RPM limits hit fast in demos; see repo
  ADK rules), optionally CopilotKit AG-UI for generative UI frontends
  (server-side `tools` MUST include `AGUIToolset()` — verified pattern,
  repo CLAUDE.md).
- **Integration:** MCP servers wrapping SAP OData v2/v4 services; scoped
  service users per agent.
- **Autonomous execution:** OpenHands for coding/ops agents — ground all
  implementation claims in `github.com/OpenHands/OpenHands` and
  `docs.openhands.dev` (repo rule: verified primitives over invented
  orchestration).
- **Memory/knowledge:** knowledge-graph layer for entity memory across
  engagements (GBrain pattern, generalizable to client estates).

### B. Working proof pattern — generative UI dashboard over enterprise data
- Forked ADK + AG-UI dashboard demo, customized with domain tools — shipped
  as the real-estate dashboard PoC (`github.com/shekerkamma/real-estate-dashboard-agent`).
  Same pattern applies to SAP: swap domain tools for OData-backed tools.
  Scored 31/35 GO via vertical-scorer.

**[NEEDS ACQUISITION]** — verified BTP-side reference (when client insists on
BTP residency), current SAP AI Core/AI Foundation capability map, S/4 2025
API surface deltas.

## 5. Patterns & frameworks

### SAP agent-readiness maturity model (v0.1 — refine with use)
1. **Exporting** — insight leaves SAP via Excel/manual reports
2. **API-addressable** — OData services exposed, governed, documented
3. **Agent-read** — read-only agents answering questions over live data
4. **Agent-act (gated)** — write actions behind approval gates, scoped keys
5. **Agent-native processes** — processes redesigned around agent execution,
   human owns exceptions

### First-use-case selection rubric
Score candidates on: read-only feasibility / weekly frequency / Excel-export
pain today / single OData service touched / measurable cycle time. Highest
total wins the PoC slot.

## 6. Tools & skills

- **Google ADK** (`google/adk-python`, registry #2) — agent reasoning layer;
  `gemini-2.5-flash` for interactive demos (rate-limit rule)
- **CopilotKit AG-UI** (registry #5) — generative UI frontends; AGUIToolset
  pattern verified in-house
- **MCP servers** (registry #3) — OData service wrapping, scoped per agent
- **OpenHands** (registry #1) — autonomous coding/ops agents
- **printing-press CLI vs `api.sap.com`** — OData surface acquisition
  (CIOS-ACQ-007 step 3) — generate on first need, keep as capability
- **In-house skills:** presales-deal-prep, vertical-scorer, branded-pptx-deck
  for pursuit deliverables

## 7. Business case & roadmap

- **Value drivers:** report-to-answer cycle time (Excel-export elimination),
  exception-handling throughput (P2P, order status), S/4 migration
  de-risking (clean-core = agent-readiness, one program not two — PoV #3).
- **External benchmarks (Tier 3 vendor cases — frame as directional):**
  automotive electronics co. cut disruption response ~95% across ~30 plants
  with agentic workflows under progressive autonomy (source: news.sap.com
  Autonomous SCM whitepaper, 2026-06); Martur Fompak (automotive seating)
  runs Joule + embodied-AI intralogistics on S/4HANA+EWM, 400 daily line
  feeds, 5× efficiency target (source: news.sap.com Sapphire, 2026-05);
  JLR clean-core brownfield go-live, 120 integrations, production pace in
  days (source: sapinsider.org, 2026-03).
  **[NEEDS ACQUISITION — non-vendor operator metrics (Tier 2c) for SAP-AI
  deployments]**
- **Evidence (in-house):** real-estate dashboard agent PoC — ADK + AG-UI
  over domain data, working demo, pattern transferable to SAP OData
  [gbrain:generative-ui-use-case]; manufacturing predictive-maintenance
  pipeline run (`runs/2026-06-04-manufacturing-predictive-maintenance/`).
- **Roadmap skeleton:** Assess (maturity model + use-case rubric) → PoC
  (90 days, read-only, single OData service) → Gate review → Expand reads →
  Earn writes (per use case) → Agent-native process redesign.

## 8. Risks & objection library

Risks: write access to a system that posts journal entries (mitigate: PoV #4
scoped keys, read-first staging); ERP upgrade collisions (clean-core
discipline); vendor roadmap dependency if Joule-locked (PoV #1); free-tier
rate limits in demos (pin `gemini-2.5-flash`, repo rule).

Objections:
- **"We're waiting for Joule — it's included in our contract."** Joule answers
  SAP's roadmap, not yours. Included ≠ free: capability gaps get filled with
  SAP consulting at SAP rates. Build the thin agent layer you own; keep Joule
  where it's genuinely ahead. *(Response stance verified; sharpen with current
  Joule packaging facts — see §2 acquisition.)*
- **"Our basis/security team won't allow external models on ERP data."**
  The architecture sends queries through scoped read-only OData users; data
  residency and model choice are configurable (Vertex regional endpoints,
  or open-weight models on-prem for sensitive paths). Start with non-sensitive
  read paths to build trust.
- **"We just want to finish the S/4 migration first."** Clean-core work IS
  agent-readiness work (PoV #3). Sequencing them serially doubles the change
  program; one assessment serves both.
- **"Joule will be cheaper — it's bundled."** Base is free, but agentic
  Premium is step-metered with 3–20× sizing uncertainty, 150–200% overage,
  and no public price list (§2 citations) — while an owned layer prices at
  benchmarkable model-API rates. Bring the §2 table; ask SAP for binding
  multi-year overage pricing and watch the answer.

## 9. Assets index

- `assets/reference-architecture-sap-owned-agent-layer.md` — owned agent
  layer over SAP, adapted from the ANE platform asset (derived: engagement
  2026-06-10-automotive-sap-ai-strategy)

## 10. Source watchlist

Tiers per `consulting-os/sources.md` (CIOS-ACQ-006/007).

**Tier 1 (ground truth — technical claims; resolution order per CIOS-ACQ-007):**
- `https://github.com/OpenHands/OpenHands` + `https://docs.openhands.dev/` — PRIMARY for this domain like all others (registry #1; owner decision). Check first for agent/automation/integration claims.
- `google/adk-python` releases + `~/awesome-llm-apps/generative_ui_agents/` — agent-layer patterns (registry #2, #6)
- `modelcontextprotocol/*` — integration layer (registry #3)
- `https://api.sap.com/` — OData/API surface, acquired via printing-press CLI when OpenHands coverage runs out (CIOS-ACQ-007 step 3)

**Tier 2 (practitioner & vendor-engineering signal):**
- YouTube: **SAP on Azure** channel — SAP-on-hyperscaler architectures, AI integration patterns (acquire via `/watch`; cite URL @timestamp)
- YouTube: **SAP on AWS** channel — same class, AWS-side patterns
- LinkedIn: SAP-AI practitioner accounts **[build up during curation passes; start empty]**
- Operator engineering blogs (Tier 2c): SAP-running enterprises publishing agent metrics **[start empty]**

**Tier 3 (context narrative only — never sole citation):**
- SAP Community + SAP News AI topics — Joule/AI Foundation announcements
- Analyst coverage of ERP-agent market

## 11. Golden questions

1. *"A $2B manufacturer on ECC6, planning S/4 by 2028, asks: what should our
   AI strategy be?"* — Rubric: must lead with clean-core = agent-readiness
   (PoV #3), propose maturity-model staging (§5), name the reference stack
   without Joule, and pick a read-only first use case via the rubric.
2. *"CIO asks: why not just turn on Joule?"* — Rubric: objection #1 response,
   ownership-of-intelligence-layer argument, with current packaging facts.
3. *"Design a 90-day PoC for order-status agents over S/4."* — Rubric:
   scoped read-only OData user, ADK + MCP architecture from §4A, gated
   success metrics, explicit keys-not-prompts permission design.
