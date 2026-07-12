---
status: reviewed
use_case: "In-Product Owner Assistant"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# In-Product Owner Assistant Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** product, CX, and support leaders at SaaS or hardware companies
with high "how do I" volume and a real help-center tax.

**Later ICPs:** product ops and support ops teams once one surface proves the
value of in-context guidance.

**Pain wedge:** users hit a dead end inside the product, leave the session, or
open a ticket because the answer lives in a portal, not in the UI state they are
already looking at.

**Incumbent weakness:** manuals, FAQ portals, and chat widgets live outside the
product session and tax editor seats.

**Agentic disruption thesis:** move guidance into the product, bind answers to
live UI state, and keep the help desk as system of record for escalation only.

**Why now:** support suites are monetizing AI, but the user still has to leave
the product to get help.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 26/30**

This score is inferred from support-suite pricing, KB friction, and the fact
that product guidance is still a separate workflow. It should be validated with
buyers before being used as a sales claim.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 8/10

**Who has the problem:** product teams with high "how do I" ticket volume and
poor feature adoption.

**Current workaround:** static manuals, external help centers, and support
macros.

**Switching reason:** reduce deflection, shorten time-to-value, and surface
guidance in the exact product state.

**Payment signal:** support-suite seats, knowledge-base seats, and AI outcome
pricing.

**30-day reachability:** one product surface, one doc source, and one embedded
assistant can prove value fast.

**Verdict: PROCEED, but keep the scope tightly in-product.**

## 2. The 30-Day Scope Definition

**Project name:** Context-Aware Product Guide

**Validated problem:** users cannot find the right feature or workflow in the
moment they need it.

**Target user:** end users inside the app plus product-support admins.

**Core hypothesis:** a product-native assistant can deflect "how do I" tickets
and improve feature adoption without replacing the help desk.

### In Scope

1. **In-app assistant overlay**
   - Acceptance criterion: answers 10 approved "how do I" questions with
     citations from approved sources.
2. **Context binding**
   - Acceptance criterion: uses current screen, role, and object state as
     input.
3. **Support fallback**
   - Acceptance criterion: low-confidence answers route to the help desk with a
     structured handoff.

### Explicitly Out Of Scope

- Rebuilding the help desk or ticketing system.
- Full voice or multimodal support in v1.
- Autonomous account changes or money-moving actions.
- Generic site-wide chatbot positioning.

### Week-By-Week Milestones

- **Week 1:** ingest manuals, release notes, and approved KB articles.
- **Week 2:** build the assistant API, context extractor, and retrieval layer.
- **Week 3:** embed the overlay in one product surface and tune fallback.
- **Week 4:** shadow/live pilot with telemetry and support review.

**Dependencies:** product UI access, approved docs, user-role metadata, and a
support escalation path.

**Acceptance test:** 90% of approved questions answered with source-backed
responses in under 10 seconds.

**Top risks:** hallucination, UI drift, and weak adoption.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: React/Next.js overlay or native webview layer.
- Backend: FastAPI service.
- Agent orchestration: LangGraph for routing and answer planning.
- Retrieval/data layer: Postgres + pgvector or Pinecone for KB chunks.
- Auth: existing app auth + signed session token.
- Database: Postgres for sessions, conversations, citations, and feedback.
- Observability: OpenTelemetry plus structured logs.
- Hosting: Vercel or containerized app service with managed database.

**Architecture:** client overlay -> API -> retrieval -> policy filter ->
answer/fallback. The assistant sits above the app UI and below the support
stack.

**Critical design decisions:**

1. Use doc-grounded retrieval instead of fine-tuning because source content
   changes faster than a model.
2. Keep the help desk as system of record because the assistant should reduce
   tickets, not replace governance.
3. Use live UI metadata because static FAQ search does not solve in-product
   confusion.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/assistant/query` | answer a user question | question, screen_state, user_role | answer, citations, confidence | session JWT | 422 if context missing, 503 on retrieval failure |
| POST | `/api/assistant/feedback` | capture response feedback | conversation_id, rating, reason | ack | session JWT | 400 on invalid conversation |
| POST | `/api/assistant/escalate` | create support handoff | conversation_id, reason | ticket_ref | session JWT + support token | retry on ticketing failure |

### Folder / Module Structure

- `app/overlay/`
- `app/api/assistant/`
- `services/retrieval/`
- `services/policy/`
- `workers/indexing/`
- `lib/session/`

### Environment Variables

- `APP_BASE_URL`
- `SUPPORT_API_KEY`
- `KB_SOURCE_TOKEN`
- `VECTOR_STORE_URL`
- `LLM_API_KEY`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| In-product assistant | moderate | embedded help widgets are seat-based and context-light | BUILD | context binding is the wedge |
| Knowledge management | low | Document360 / Guru / Help Scout seat and admin costs | BUY | source content already exists |
| Ticketing / escalation | low | support suite already installed | BUY | keep the SoR |

**Bottom line:** buy the help desk and knowledge repository, build the live
guidance layer.

## 5. MVP ROI Business Case

**Current-state cost model:** help desk spend, KB spend, L1 support labor,
content maintenance, and repeated feature-discovery tickets.

**Agentic MVP cost model:** one embedded assistant, ingestion pipeline, monthly
model usage, vector search, and support handoff traffic.

**Pricing options:**

1. Fixed-fee pilot for one product area.
2. Usage / outcome pricing per resolved "how do I" question.
3. Enterprise package with assistant, analytics, and support handoff.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | weak content, low adoption, 10% deflection | 12-18 months | month 14+ | needs more content ops |
| Base | 20-30% ticket deflection, one surface, good docs | 6-9 months | month 8-12 | conservative adoption |
| Upside | 40% deflection plus onboarding lift | 3-6 months | month 4-6 | strong content coverage |

**Formulas**

```text
Monthly value =
  ticket avoidance + time saved in feature discovery + reduced onboarding
  - agent monthly run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if the buyer cannot expose approved content and live UI
state, the wedge collapses into generic search.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Zendesk | help desk | entrenched system of record | heavy ops tax and context switching | per-seat + AI packaging | `runs/2026-06-26-agentic-opportunity-blueprints/source/Zendesk_Competitor_Teardown.md` |
| Intercom | support platform | strong support UX | support-stack coupling and seat tax | seat + outcome pricing | `runs/2026-06-26-agentic-opportunity-blueprints/source/Zendesk_Competitor_Teardown.md` |
| Guru | knowledge base | content governance + Slack/Teams reach | manual maintenance tax | per-user AI pricing | `runs/2026-06-26-agentic-opportunity-blueprints/source/FAQ_KnowledgeBase_Competitor_Teardown.md` |
| Document360 | knowledge base | docs-first structure | portal model and quote-only sales | custom quote | `runs/2026-06-26-agentic-opportunity-blueprints/source/FAQ_KnowledgeBase_Competitor_Teardown.md` |

**Direct threats:** Zendesk and Intercom.

**What not to build:** a standalone help center, omni-channel support suite, or
custom model-training loop.

**Agentic wedge:** collapse the seat and answer in-product from live context,
while the help desk only receives structured escalations.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Context answer | user on a product screen | asks how to complete a task | assistant answers with citations | replay fixture test |
| Low-confidence fallback | missing context | user asks an ambiguous question | assistant routes to support | ticket created and logged |
| UI element identification | screenshot or screen metadata | question references a visible element | assistant names the element correctly | image / screen fixture test |

### Edge Cases

- Empty state: assistant explains no approved source exists yet.
- Retrieval failure: return a support handoff.
- Invalid input: unsupported screenshot or malformed question is rejected.
- Slow dependency: answer degrades gracefully to KB search.
- Concurrent escalation: one ticket per session.
- Auth/data boundary: tenant data cannot bleed across orgs.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| approved docs | KB CMS | chunk store | docs team | hourly | checksum + approval state |
| product context | app telemetry | session table | product app | realtime | schema validation |
| conversations | assistant API | conversation table | assistant | realtime | PII redaction |
| support handoffs | ticketing API | audit log | support desk | realtime | idempotency keys |

**Retention and deletion:** retain citations and handoff metadata; delete raw
transient prompts after the retention window.

**Analytics questions:** which screens drive the most unanswered questions and
which docs are missing?

**Privacy/security:** PII is minimized in prompts, tenant isolation uses row-
level security, and export / delete requests follow the parent app policy.

## 9. Deployment Sequencing

**Pre-deploy checklist:** approved content set, support escalation path,
telemetry schema, rollback flag.

**Staging:** shadow traffic, then staff-only beta.

**Production sequence:** one surface, one workflow, one support queue.

**Smoke test:** ask three approved questions and verify citations.

**Rollback:** disable overlay and fall back to KB link plus support desk.

**Observability:**

- Logs: query, context, retrieval hits, fallback reason.
- Metrics: answer rate, deflection rate, latency, escalation rate.
- Alerts: retrieval failure, confidence drop, spike in unsupported questions.
- Dashboards: unanswered questions by product area.

## 10. Post-Launch Iteration Plan

**Metrics:** activation, repeat use, ticket deflection, and feature-adoption
lift.

**Week-by-week:**

- Week 1: expand content coverage and identify missing docs.
- Week 2: add role-aware guidance and better citations.
- Week 3: introduce proactive help on stuck screens.
- Week 4: package the assistant for other product areas.

**Pivot signals:** move the overlay closer to the task flow if users ignore
it, tighten source governance if citations fail, and reduce scope to help-
center search if product state is unavailable.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/Zendesk_Competitor_Teardown.md` - help desk incumbent map and pricing signals.
- `runs/2026-06-26-agentic-opportunity-blueprints/source/FAQ_KnowledgeBase_Competitor_Teardown.md` - KB incumbents, maintenance tax, and wedge framing.
- Zendesk Pricing - https://www.zendesk.com/pricing/ - accessed 2026-06-26 - support-suite pricing and AI packaging.
- Help Scout Pricing - https://www.helpscout.com/pricing/ - accessed 2026-06-26 - per-user plans and AI Answers pricing.
- Document360 Pricing - https://document360.com/pricing/ - accessed 2026-06-26 - knowledge-base pricing signals.
- Intercom Pricing - https://www.intercom.com/pricing - accessed 2026-06-26 - AI support and seat/outcome packaging.
- These incumbents reinforce that the wedge is contextual help inside the product session, not another external help portal.
