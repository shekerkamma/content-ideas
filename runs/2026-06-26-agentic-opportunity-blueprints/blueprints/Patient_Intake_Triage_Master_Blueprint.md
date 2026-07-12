---
status: reviewed
use_case: "Patient Intake Triage"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Patient Intake Triage Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** clinic operations and patient access leaders.

**Later ICPs:** adjacent specialty clinics once one intake path proves the
conversational triage loop.

**Pain wedge:** intake calls and forms clog schedulers and staff.

**Incumbent weakness:** intake systems still require manual triage and
back-and-forth.

**Agentic disruption thesis:** triage the patient request, gather needed info,
and route to the right path.

**Why now:** access teams need speed without dropping safety and compliance.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

The score is inferred from call-center burden, scheduling pressure, and the
clear cost of manual intake.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** clinics and patient access teams.

**Current workaround:** call center scripts, forms, and manual scheduling.

**Switching reason:** faster intake and less staff burden.

**Payment signal:** patient access and scheduling budgets.

**30-day reachability:** one intake path and one specialty can prove the wedge.

**Verdict: PROCEED, but keep clinical safety explicit.**

## 2. The 30-Day Scope Definition

**Project name:** Patient Intake Copilot

**Validated problem:** intake information needs to be collected, summarized,
and routed.

**Target user:** patient access rep or clinic scheduler.

**Core hypothesis:** the agent can collect triage info and hand off a structured
summary.

### In Scope

1. **Conversational intake**
   - Acceptance criterion: the patient can answer questions via secure chat.
2. **Triage summary**
   - Acceptance criterion: the agent produces a structured handoff summary.
3. **Routing**
   - Acceptance criterion: the request is routed to the correct clinic path.

### Explicitly Out Of Scope

- New patient portal app.
- Proprietary tablet hardware.
- Autonomous diagnosis.
- Replacing clinician judgment.

### Week-By-Week Milestones

- **Week 1:** define one intake path and required questions.
- **Week 2:** build conversational intake and summary.
- **Week 3:** add routing and secure handoff.
- **Week 4:** pilot one specialty with review.

**Dependencies:** scheduling system, secure messaging, and clinic approval.

**Acceptance test:** one intake flow produces a structured summary and route.

**Top risks:** safety, compliance, and message quality.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: secure chat surface and admin console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for intake scripts and FAQs.
- Auth: secure messaging plus clinic auth.
- Database: Postgres for sessions, triage notes, and routing.
- Observability: OpenTelemetry and routing metrics.
- Hosting: cloud app with queue worker.

**Architecture:** patient message -> triage questions -> summary -> routing ->
handoff. The agent collects structured information and passes it into the clinic
workflow.

**Critical design decisions:**

1. Do not build a patient portal.
2. Use conversational intake rather than static forms.
3. Route to the EHR / scheduling system only after structured summary.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/intake/ingest` | ingest patient request | message payload | session_id | service token | retry queue |
| POST | `/api/intake/triage` | collect required details | session_id | structured summary | service token | fallback to rep |
| POST | `/api/intake/route` | route to clinic path | session_id, summary | route result | service token | escalate to human |

### Folder / Module Structure

- `app/intake/`
- `app/api/intake/`
- `services/triage/`
- `services/route/`
- `workers/handoff/`
- `lib/clinical/`

### Environment Variables

- `SECURE_MSG_TOKEN`
- `EHR_API_KEY`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `ROUTING_MAP_TOKEN`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Patient portal | high | Phreesia / MyChart already exist | BUY | not the wedge |
| Conversational intake | medium | forms create friction | BUILD | core wedge |
| Routing / handoff | medium | manual triage is the pain | BUILD | high leverage |

**Bottom line:** buy the patient-system shell and build the conversational
triage layer.

## 5. MVP ROI Business Case

**Current-state cost model:** intake labor, scheduler time, and abandoned
appointments.

**Agentic MVP cost model:** chat intake, model usage, routing, and review.

**Pricing options:**

1. Per clinic / specialty.
2. Usage / outcome model per completed triage.
3. Enterprise package with analytics.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low chat adoption | 12-18 months | month 14+ | needs better channel placement |
| Base | faster intake, less staff burden | 6-9 months | month 8-12 | good fit |
| Upside | meaningful deflection and routing lift | 3-5 months | month 4-6 | strong leverage |

**Formulas**

```text
Monthly value =
  intake labor saved + scheduling time saved + fewer abandoned appointments
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if clinical compliance cannot be maintained, do not
expand.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Phreesia | patient intake | dominant standalone intake | forced check-in / bolt-on friction | quote-based | `runs/2026-06-26-agentic-opportunity-blueprints/source/Patient_Intake_Triage_Competitor_Teardown.md` |
| Epic MyChart | patient portal | enterprise EHR integration | inbox burden / app fatigue | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Patient_Intake_Triage_Competitor_Teardown.md` |
| Cerner HealtheLife | patient portal | enterprise reach | clunky patient experience | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Patient_Intake_Triage_Competitor_Teardown.md` |
| Weave | SMB comms | simple messaging | limited triage depth | SMB pricing | `runs/2026-06-26-agentic-opportunity-blueprints/source/Patient_Intake_Triage_Competitor_Teardown.md` |

**Direct threats:** Phreesia and Epic MyChart.

**What not to build:** a new patient portal app or proprietary tablet hardware.

**Agentic wedge:** conversational intake, diagnostic pre-population, and
triage automation through secure messaging.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| conversational intake | patient message | agent runs | structured triage data produced | scenario test |
| summary | intake complete | agent finishes | clinician handoff summary created | replay test |
| routing | triage data ready | routing runs | correct clinic path selected | integration test |

### Edge Cases

- Missing symptoms.
- High-risk language.
- Unclear specialty.
- Duplicate intake.
- Message channel failure.
- PHI handling.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| messages | secure chat | session table | chat system | realtime | PHI controls |
| triage answers | agent | triage table | agent | realtime | structured schema |
| routing | clinic workflow | routing table | clinic | realtime | idempotency |
| feedback | staff | feedback table | staff | realtime | audit trail |

**Retention and deletion:** retain triage history and routing logs, delete raw
transient prompts by policy, and keep handoff summaries.

**Privacy/security:** secure SMS capability, least-privilege access, and PHI
controls.

**Analytics questions:** which specialties have the most repetitive intake
questions and where do routing handoffs fail?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one intake path, routing map, security review,
rollback flag.

**Staging:** intake-only, then summary, then routing.

**Production sequence:** one specialty, one clinic, one review path.

**Smoke test:** one intake request produces the correct structured summary.

**Rollback:** disable routing and fall back to manual triage.

**Observability:**

- Logs: message, triage step, route, handoff.
- Metrics: completion rate, time to triage, routing accuracy.
- Alerts: PHI error, routing failure, message lag.
- Dashboards: intake funnel and handoff latency.

## 10. Post-Launch Iteration Plan

**Metrics:** time to intake, staff burden, and appointment completion.

**Week-by-week:**

- Week 1: add one more intake path.
- Week 2: improve triage prompts.
- Week 3: refine routing.
- Week 4: package for adjacent specialties.

**Pivot signals:** move to another channel if chat adoption is weak, keep the
scope narrow if safety concerns appear, and stay away from diagnostic claims.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Patient_Intake_Triage_Disruptive_Teardown.md` - upstream teardown dossier for the intake-triage wedge.
- Official reference points reviewed: Epic, athenahealth, PointClickCare, and Salesforce Health Cloud product pages.
- `runs/2026-06-26-agentic-opportunity-blueprints/source/Patient_Intake_Triage_Competitor_Teardown.md` - patient intake incumbent map and conversational-triage wedge.
