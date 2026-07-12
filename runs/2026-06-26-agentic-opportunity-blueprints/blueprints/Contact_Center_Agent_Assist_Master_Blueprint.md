---
status: reviewed
use_case: "Contact Center Agent Assist"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Contact Center Agent Assist Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** contact-center, CX, and operations leaders running high-volume
voice or chat queues with serious handle-time and QA pressure.

**Later ICPs:** adjacent support teams once one queue proves latency, QA, and
after-call-work gains.

**Pain wedge:** agents know the customer is waiting, but the answer is buried in
knowledge, scripts, product notes, or policy docs.

**Incumbent weakness:** NICE CXone, Verint, Cresta, Balto, Genesys, and Talkdesk
own routing and QA, but their agent-assist layers are expensive, brittle, and
hard to keep tuned.

**Agentic disruption thesis:** provide a semantic real-time copilot that answers
fast, drafts wrap-up notes, and captures QA evidence without replacing the CCaaS
platform.

**Why now:** the market already budgets for CCaaS and AI overlays, but there is
still a gap between "transcribe" and "actually help the human."

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

The score is inferred from high seat spend, visible AI overlay pricing, and the
ongoing complaint that live guidance still needs manual tuning.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** contact-center leaders with long handle times,
inconsistent QA, and repetitive scripts.

**Current workaround:** KB search, script trees, whisper support, and manual QA.

**Switching reason:** reduce handle time, raise first-contact resolution, and
eliminate after-call toil.

**Payment signal:** high CCaaS spend plus willingness to pay for AI add-ons.

**30-day reachability:** one queue, one script set, one QA workflow.

**Verdict: PROCEED, but do not compete on telephony.**

## 2. The 30-Day Scope Definition

**Project name:** Real-Time Agent Assist

**Validated problem:** live agents spend too long searching for answers and
writing summaries after the call ends.

**Target user:** frontline service and support agents.

**Core hypothesis:** a semantic assist layer can improve live call performance
without replacing the CCaaS stack.

### In Scope

1. **Real-time answer suggestions**
   - Acceptance criterion: agent receives a cited answer while the call is
     active.
2. **Post-call summary drafting**
   - Acceptance criterion: wrap-up notes and disposition are usable with light
     edits.
3. **QA evidence capture**
   - Acceptance criterion: reviewer can trace answer provenance for each call.

### Explicitly Out Of Scope

- Replacing telephony or call routing.
- Building a workforce-management suite.
- Autonomous customer-facing actions.
- Full call-recording system of record.

### Week-By-Week Milestones

- **Week 1:** ingest scripts, policies, and product docs.
- **Week 2:** build live transcript feed and answer retrieval.
- **Week 3:** launch agent overlay and post-call summary.
- **Week 4:** QA calibration, supervisor review, and pilot expansion.

**Dependencies:** CCaaS access, transcripts, approved policies, and a QA rubric.

**Acceptance test:** live agent gets a cited answer in under 2 seconds and the
summary is usable without heavy editing.

**Top risks:** latency, hallucination, and adoption.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: browser overlay or embedded agent desktop panel.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph or similar streaming router.
- Retrieval/data layer: Postgres + vector index for scripts, policies, and
  product docs.
- Auth: CCaaS SSO or signed workspace token.
- Database: Postgres for transcripts, QA outcomes, and feedback.
- Observability: OpenTelemetry and call-latency dashboards.
- Hosting: containerized service close to the CCaaS region.

**Architecture:** transcript stream -> retrieval -> policy filter -> response
suggestion -> agent. The assistant listens, classifies intent, retrieves
approved answers, suggests replies, and logs outcomes.

**Critical design decisions:**

1. Stream answers instead of waiting for the full call.
2. Keep transcripts and QA in the CCaaS layer as system of record.
3. Use a constrained answer library for regulated intents.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/calls/stream` | receive transcript tokens | call_id, transcript_chunk | ack, routed intent | workspace token | 429 / 503 if backpressure |
| POST | `/api/assist/answer` | return suggested answer | call_id, intent, context | answer text, citations | workspace token | return search fallback |
| POST | `/api/assist/postcall` | draft summary and QA notes | call_id, transcript | summary, dispositions | workspace token | retry on transient failure |

### Folder / Module Structure

- `app/desktop/`
- `app/api/calls/`
- `services/streaming/`
- `services/routing/`
- `workers/postcall/`
- `lib/qa/`

### Environment Variables

- `CCAAAS_API_TOKEN`
- `KB_SYNC_TOKEN`
- `QA_SYSTEM_URL`
- `VECTOR_DB_URL`
- `MODEL_API_KEY`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| CCaaS routing | High | Genesys / NICE / Talkdesk already own it | BUY | not the wedge |
| Real-time agent assist | Medium | Cresta / Balto are expensive and rigid | BUILD | semantic wedge |
| QA scoring automation | Medium | manual QA costly | BUILD | handles toil |

**Bottom line:** buy routing, build semantic assistance and post-call
automation.

## 5. MVP ROI Business Case

**Current-state cost model:** per-agent CCaaS plus AI add-ons, QA labor,
handle-time inflation, and supervisor interrupt cost.

**Agentic MVP cost model:** transcript streaming, retrieval and model usage, QA
log storage, and escalation / review ops.

**Pricing options:**

1. Per-active-agent monthly package.
2. Usage-based pricing on call minutes.
3. Enterprise deployment with routing integration.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low adoption, noisy transcripts | 12-18 months | month 14+ | needs tuning |
| Base | 15-20 sec handle-time reduction, 10% QA automation | 6-9 months | month 8-12 | conservative |
| Upside | larger handle-time reduction plus QA automation | 3-6 months | month 4-6 | strong volume |

**Formulas**

```text
Monthly value =
  handle-time reduction + QA labor avoided + supervisor interrupt reduction
  - agent monthly run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if latency cannot stay sub-second, the live-call wedge is
gone.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| NICE CXone | CCaaS | deep routing and ops coverage | seat-heavy and expensive | per-agent plus session fees | `runs/2026-06-26-agentic-opportunity-blueprints/source/ContactCenterAgentAssist_Competitor_Teardown.md` |
| Verint | WEM / QA | legacy enterprise footprint | heavy implementation | opaque enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/ContactCenterAgentAssist_Competitor_Teardown.md` |
| Cresta | AI assist | premium AI-native overlay | tuning burden and high spend | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/ContactCenterAgentAssist_Competitor_Teardown.md` |
| Balto | agent assist | real-time guidance | implementation time | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/ContactCenterAgentAssist_Competitor_Teardown.md` |

**Direct threats:** Cresta and Verint.

**What not to build:** a telephony platform, a WFM suite, or a full call
recording system.

**Agentic wedge:** replace keyword-trigger fragility with semantic
understanding, automate after-call work, and price on compute instead of a
bloated per-seat model.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Live answer | transcript token stream | agent asks for help | response appears before dead air | latency test |
| Post-call wrap-up | finished transcript | call ends | summary and disposition are drafted | diff against human summary |
| QA evidence | selected call | reviewer opens QA | cited evidence appears | audit replay |

### Edge Cases

- Noisy audio.
- Low transcript confidence.
- Regulated statement.
- Missing KB article.
- Concurrent calls.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| transcripts | CCaaS stream | transcript table | CCaaS | realtime | confidence filter |
| snippets | KB CMS | approved-answer store | knowledge ops | hourly | approval state |
| QA | review tool | QA table | QA team | realtime | immutable record |
| feedback | agent input | feedback table | agent assist app | realtime | dedupe |

**Retention and deletion:** retain call metadata and QA evidence, redact PII
from transcript logs, and expire raw transcript fragments by policy.

**Privacy/security:** role-based access for supervisors, tenant isolation, and
do-not-store rules for sensitive phrases.

**Analytics questions:** where do handles run long, which intents miss approved
coverage, and which answer snippets need better tuning?

## 9. Deployment Sequencing

**Pre-deploy checklist:** CCaaS transcript feed, approved script set, QA
rubric, rollback flag.

**Staging:** shadow mode, then a single-queue pilot.

**Production sequence:** one queue, one intent family, one supervisor.

**Smoke test:** ask three live intents and verify sub-second response
generation.

**Rollback:** disable overlay and fall back to search snippets.

**Observability:**

- Logs: transcript chunk, intent, latency, answer ID.
- Metrics: latency, deflection, handle time, QA score.
- Alerts: transcript lag, confidence drop, fallback spike.
- Dashboards: intent coverage and QA edit rate.

## 10. Post-Launch Iteration Plan

**Metrics:** handle time, QA edit rate, agent acceptance, and supervisor
interrupt reduction.

**Week-by-week:**

- Week 1: expand approved answer coverage.
- Week 2: calibrate latency and confidence thresholds.
- Week 3: add post-call automation improvements.
- Week 4: package for adjacent queues.

**Pivot signals:** simplify the UX if agents ignore it, narrow the intent set
if latency drifts, and constrain the response library if QA cannot trust the
output.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/ContactCenterAgentAssist_Competitor_Teardown.md` - incumbent map, pricing signals, and implementation friction.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Contact_Center_Agent_Assist_Disruptive_Teardown.md` - upstream teardown dossier for the agent-assist wedge.
- Official reference points reviewed: Genesys, Zendesk, Intercom, LivePerson, Ada, and Amazon Connect product pages.
