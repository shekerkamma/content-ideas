# AI Strategy — SAP Estate of a Global Automotive Manufacturer

**Prepared:** 2026-06-10 · **Status:** draft (first real-engagement output;
see governance note in §10)
**Domain pack:** sap-ai-transformation v0.2 + acquisition delta 2026-06-10
**Citation discipline:** every load-bearing claim cited inline (CIOS-GOV-002)

---

## 1. Executive summary

Your SAP estate is where the enterprise's most valuable operational truth
lives — orders, BOMs, materials, suppliers, financials — behind its most
change-resistant systems. The strategic question is not *whether* AI reaches
that data, but **who owns the intelligence layer that does**: you, or your
ERP vendor.

The market data says the vendor path is stalling: per the DSAG Investment
Survey 2026, **only 3% of SAP customers run SAP Business AI in production,
and 77% of AI-active enterprises use non-SAP tools instead** (source:
innobu.com SAP Joule 2026 analysis, 2026-04). The reasons are structural —
Joule requires RISE/GROW contracts, pricing is opaque with 150–200% overage
rates, and agentic workloads consume 3–20× the AI Units of copilot-era
sizing (sources: innobu 2026-04; finoptory.ai SAP Business AI licensing,
2026-05).

**Our recommendation in one sentence:** treat your S/4 migration's clean-core
program and your AI program as one transformation; build an **owned agent
layer** (Gemini + ADK + MCP → governed SAP OData APIs) over the estate;
take what's free (Joule Base ships with cloud subscriptions); and earn
autonomy use case by use case — read paths first, writes behind gates.

Three decisions are requested (§9).

## 2. Where you are

A global automotive manufacturer mid-journey to S/4HANA — multiple plants,
deep PLM/ERP/EWM integration, weekly operational reporting that still exits
SAP via Excel. On the pack's agent-readiness maturity model
(1 Exporting → 2 API-addressable → 3 Agent-read → 4 Agent-act gated →
5 Agent-native), most of the estate sits at **stage 1–2**. The strategy
targets stage 3 within 90 days of approval, stage 4 within 12 months on
selected processes.

Automotive peers prove both halves of the journey are real:
- **JLR** runs a disciplined clean-core S/4HANA program — extensibility
  pyramid governance (standard → key-user → BAdIs → core mods), Fiori-only
  policy, BTP/RAP sidecars — and went live brownfield at Halewood with 120
  integrations, 200+ cars on track by day three (sources: studiocelanie.com
  JLR clean-core, 2026-06; sapinsider.org JLR scaling, 2026-03).
- An automotive electronics company centralized ordering across ~30 plants
  and cut disruption response time ~95% with agentic workflows under
  human-in-the-loop governance (source: news.sap.com Autonomous SCM
  whitepaper, 2026-06).

## 3. Market reality: the Joule question, answered with data

Every SAP AI conversation starts with "don't we just turn on Joule?" The
evidence-based answer:

| Fact | Implication |
|---|---|
| Joule **Base** is included free in cloud subscriptions — navigational, informational, basic CRUD (source: learning.sap.com Selling SAP Business AI, 2026-05) | Take it where entitled. It is a UI convenience, not a strategy. |
| Joule **Premium** agents are metered per step: Basic 5 / Standard 10 / Advanced 25 requests per step, or 0.005–0.025 AI Units/step for custom agents (source: learning.sap.com Joule commercial model, 2026-03) | Agentic costs scale with *process volume*, not user count — a high-frequency plant process multiplies steps. |
| Agentic deployments consume **3–20×** copilot-era AI-Unit sizing; overage at 150–200% of contract rate; **no public price list** (sources: finoptory.ai, 2026-05; innobu, 2026-04) | Production-scale economics are unknowable upfront — a structural negotiation disadvantage. |
| Joule requires **RISE/GROW**; on-premise estates are excluded entirely (source: innobu, 2026-04) | Your ECC/hybrid plants cannot use it at all during the migration window — exactly when AI value is highest. |
| **DSAG 2026: 3% production adoption; 77% of AI-active SAP customers use non-SAP AI tools** (source: innobu citing DSAG Investment Survey 2026) | The market has already voted for the owned-layer pattern. |
| SAP's own leadership: clean-core customers are "better positioned for AI"; adoption is gated by readiness, not technology; >90% of projects delivered by SI partners (source: sapinsider.org Joule readiness, 2026-05) | SAP agrees with our PoV #3 — and the delivery model means *you* will own the integration work either way. |

**Position:** do not build your agent layer on Joule. Use free Base
entitlements opportunistically; track SAP's agent GA waves (supply-chain
agents GA Q2 2026 — source: news.sap.com Hannover Messe, 2026-04) as
*competitive benchmarks* for your owned agents, and keep SAP's Generative UI
direction (A2UI protocol → Fiori controls, grounded in Business Data Cloud —
source: SAP News Center, March 2026, Chief AI Officer J. von Rueden
[gbrain:concepts/generative-ui-sap]) on the watchlist: it validates the
agent-renders-UI pattern our stack already implements with AG-UI.

## 4. The strategy: own the layer, earn the autonomy

1. **One program, not two.** Clean-core discipline IS agent-readiness
   (pack PoV #3, now corroborated by SAP's own customer-success leadership —
   sapinsider.org, 2026-05). Every API-first extension decision in the S/4
   program doubles as agent surface. Adopt JLR's extensibility-pyramid
   governance for both.
2. **Owned reference stack:** Google ADK agents (Gemini) + MCP servers
   wrapping SAP OData v2/v4 + scoped service users per agent; CopilotKit
   AG-UI for generative dashboards; OpenHands for engineering/ops agents
   (pack §4A; ADK/AG-UI pattern proven in-house — working generative-UI
   dashboard PoC, vertical-scored 31/35 GO
   [gbrain:deals/generative-ui-enterprise]).
3. **Keys, not prompts.** ERP agents get least-privilege, read-only OData
   service accounts first; write scopes are granted per battle-tested use
   case. A prompt is never the permission layer on a system that posts
   journal entries (pack PoV #4). Industry operators independently converge
   on the same pattern — "progressive autonomy thresholds" (news.sap.com
   Autonomous SCM, 2026-06).
4. **Start where data exits SAP today** (pack PoV #5): the Excel-export
   reports are your highest-frequency, zero-write-risk agent candidates.

## 5. Use-case portfolio (scored by the pack's selection rubric)

Rubric: read-only feasibility / weekly frequency / Excel-export pain /
single OData service / measurable cycle time.

| # | Use case | Stage | OData surface | Why first |
|---|----------|-------|---------------|-----------|
| 1 | Order-status & backlog agent (sales + production orders) | 3 read | Sales Order, Production Order APIs | Highest ask-frequency; pure read |
| 2 | P2P exception triage (blocked invoices, GR/IR) | 3 read | Supplier Invoice APIs | Weekly Excel pain today |
| 3 | Inventory & material-availability agent (plant-level) | 3 read | Material Stock APIs | Feeds daily production meetings |
| 4 | Supply-disruption sensing across plants | 3→4 | Multiple + external signals | Peer-proven ~95% response-time gain (cited §2) |
| 5 | Generative dashboard over plant KPIs (AG-UI) | 3 read | Aggregation services | In-house pattern, demo-ready |
| 6 | Material reservation & master-data assistance | 4 gated | Reservation APIs | Benchmark against SAP's own GA agents (Q2 2026) before building |

Use cases 1–3 are the 90-day pilot set. Use case 6 is deliberately deferred —
if SAP's included agents cover it adequately under Base/existing
entitlements, buying beats building there.

## 6. Reference architecture

```
Context layer    engagement brain: specs · skills · process knowledge
Reasoning        ADK agents (Gemini) · AG-UI generative dashboards
Integration      MCP servers → SAP OData v2/v4 · scoped service users
Systems          S/4HANA (clean core) · EWM · PLM · non-SAP (MES, quality)
Governance       read-first scopes · approval gates on writes · budget caps
                 · audit logging · pinned model versions for unattended runs
```
(Derived from the domain asset `reference-architecture-owned-agent-platform`,
adapted to the SAP estate; all agent-layer primitives verified per pack §4.)

## 7. Roadmap (pack skeleton, populated)

- **Assess (wks 1–3):** OData surface inventory across pilot plants;
  maturity-model baseline; clean-core/extension governance alignment with
  the S/4 program; capture pre-pilot cycle-time baselines (TST-005 logic:
  prove the delta).
- **PoC (wks 4–14):** use cases 1–3, read-only, one scoped service account
  each; weekly metric reviews.
- **Gate review (wk 15):** evidence vs baseline; data-residency findings;
  Joule-Base overlap check (don't duplicate what's free).
- **Expand reads (mo 4–6):** disruption sensing (UC4), generative dashboards
  (UC5); plant rollout of UC1–3.
- **Earn writes (mo 6–12):** first gated write actions (P2P release
  recommendations → approvals); UC6 build-vs-buy decision on SAP agent GA
  evidence.
- **Agent-native processes (yr 2):** redesign 1–2 processes around agent
  execution with human exception ownership.

## 8. Risks & objections (pre-answered)

- **"Wait for Joule — it's in our contract."** Base is free — use it; the
  agent layer is what you must own. 3% production adoption, RISE-lock, and
  3–20× cost uncertainty are the vendor-path risks, all cited in §3.
- **"Security won't allow external models on ERP data."** Read-only scoped
  OData users; regional Vertex endpoints or open-weight models for sensitive
  paths; start on non-sensitive read paths. The permission layer is keys and
  scopes — provable to your CISO, not promised.
- **"Finish the S/4 migration first."** Serializing doubles the change
  program. JLR's clean-core governance shows the joint pattern working in
  automotive at brownfield scale (§2).
- **Cost runaway:** budget caps per agent service account; weekly spend
  alerts; the owned layer prices at model-API rates you can benchmark —
  unlike AI Units, which have no public price list (finoptory.ai, 2026-05).

## 9. Decisions requested

1. Approve the **90-day read-only pilot** (use cases 1–3) under the joint
   clean-core/agent-readiness governance.
2. Approve the **OData surface inventory** as a formal S/4-program
   workstream (one assessment serving migration AND agents).
3. Adopt the **owned-agent-layer position** for the estate: Joule Base
   consumed where free, no strategic build on Joule Premium; revisit at the
   month-6 gate with SAP's GA-agent evidence on the table.

## 10. Governance note (CIOS)

Draft status: produced from pack v0.2 (`draft`) plus a same-day acquisition
delta on the market landscape; §3 pricing facts are from SAP's own learning/
pricing pages (strong) and named-survey secondary analysis (DSAG via innobu —
verify the survey primary at contract time). Traceability per CIOS-MM-005:
registry sources → inbox item 2026-06-10-joule-market-landscape → domain
sap-ai-transformation → pack v0.2→v0.3 → asset
reference-architecture-owned-agent-platform (adapted) → this output.
