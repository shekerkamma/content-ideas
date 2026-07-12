---
status: reviewed
use_case: "Maintenance Ticket Orchestration"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Maintenance Ticket Orchestration Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** property-management and resident-experience leaders who need
faster dispatch and fewer stuck tickets.

**Later ICPs:** adjacent multifamily and HOA operations teams once one building
proves the orchestration layer.

**Pain wedge:** tenant requests require human triage and vendor coordination,
and requests fall through the cracks when vendors do not update the system.

**Incumbent weakness:** PMS portals track tickets but do not orchestrate action
end-to-end.

**Agentic disruption thesis:** intake, diagnose, dispatch, and track from a
chat / SMS interface.

**Why now:** 24/7 resident expectations and staffing shortages make
orchestration valuable.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

The score is inferred from recurring dispatch toil, portal adoption friction,
and the direct labor cost of chasing vendors.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** property managers and maintenance coordinators.

**Current workaround:** phone calls and manual vendor dispatch.

**Switching reason:** faster response and less PM time.

**Payment signal:** property-management labor and PMS spend.

**30-day reachability:** one building and one vendor set can prove the wedge.

**Verdict: PROCEED, but do not require a new vendor portal.**

## 2. The 30-Day Scope Definition

**Project name:** Maintenance Copilot

**Validated problem:** maintenance requests need diagnosis and dispatch.

**Target user:** tenant and property manager.

**Core hypothesis:** the agent can ask clarifying questions, classify issues,
and dispatch work orders.

### In Scope

1. **Intake**
   - Acceptance criterion: SMS / email / portal request becomes a structured
     ticket.
2. **Diagnosis**
   - Acceptance criterion: photo or text context is used to classify the issue.
3. **Dispatch and follow-up**
   - Acceptance criterion: vendor is contacted and the PMS is updated.

### Explicitly Out Of Scope

- Building another resident portal app.
- Full property management accounting.
- Vendor marketplace creation.
- Autonomous repair approvals beyond policy.

### Week-By-Week Milestones

- **Week 1:** define ticket types and vendor contacts.
- **Week 2:** build intake and classification.
- **Week 3:** add SMS / email dispatch and follow-up.
- **Week 4:** pilot one building and one vendor group.

**Dependencies:** PMS access, vendor contacts, ticket taxonomy, and owner
approval.

**Acceptance test:** one maintenance request can be diagnosed, dispatched, and
tracked to closure.

**Top risks:** vendor adoption, stale status updates, and escalations.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: ops console and resident chat surface.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for maintenance SOPs.
- Auth: PMS / portal OAuth plus SMS provider credentials.
- Database: Postgres for tickets, vendors, updates, and approvals.
- Observability: OpenTelemetry and dispatch metrics.
- Hosting: cloud app with queue worker.

**Architecture:** intake -> classify -> dispatch -> follow-up -> PMS update.
The agent handles clarifying questions, diagnosis, vendor outreach, and status
tracking.

**Critical design decisions:**

1. Use vendor-native SMS / text instead of forcing portal adoption.
2. Analyze photos only to improve triage, not to replace inspection policy.
3. Keep the PMS as system of record.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/tickets/ingest` | ingest resident request | message payload | ticket_id | service token | retry queue |
| POST | `/api/tickets/classify` | diagnose issue | ticket_id, attachments | classification | service token | fallback review |
| POST | `/api/tickets/dispatch` | contact vendor | ticket_id, vendor | dispatch result | service token | retry and alert |

### Folder / Module Structure

- `app/maintenance/`
- `app/api/tickets/`
- `services/intake/`
- `services/classify/`
- `workers/dispatch/`
- `lib/vendors/`

### Environment Variables

- `PMS_API_KEY`
- `SMS_API_KEY`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `VENDOR_CONTACTS_TOKEN`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| PMS ticketing | high | AppFolio / Buildium already own it | BUY | not the wedge |
| Orchestration layer | medium | vendor portals are the bottleneck | BUILD | core wedge |
| Vendor dispatch | medium | human chasing is expensive | BUILD | high leverage |

**Bottom line:** buy the portal shell, build the orchestration layer.

## 5. MVP ROI Business Case

**Current-state cost model:** PM labor, vendor chasing, and delayed repairs.

**Agentic MVP cost model:** ticket ingestion, model usage, vendor messaging,
and status logging.

**Pricing options:**

1. Per unit / building.
2. Per dispatch.
3. Portfolio package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low ticket volume, weak vendor adoption | 12-18 months | month 14+ | limited |
| Base | fewer callbacks and better follow-up | 6-9 months | month 8-12 | strong fit |
| Upside | lots of repeat vendor dispatches | 3-5 months | month 4-6 | high leverage |

**Formulas**

```text
Monthly value =
  PM labor saved + delayed-repair cost avoided + vendor-chase cost reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if vendors must download a new app, adoption will fail.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| AppFolio | PMS | scale and embedded portal | over-complicated maintenance modules | subscription / unit | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_35_Competitor_Teardown.md` |
| Buildium | PMS | simpler work-order tracking | vendor adoption friction | subscription / unit | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_35_Competitor_Teardown.md` |
| Property Meld | maintenance platform | specialized focus | portal adoption friction | unit-based | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_35_Competitor_Teardown.md` |

**Direct threats:** AppFolio and Property Meld.

**What not to build:** another resident portal app.

**Agentic wedge:** SMS-first vendor communication, automated triage from photos,
and self-healing follow-up loops.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Intake | resident sends request | system ingests | ticket is structured | replay test |
| Diagnosis | photo + description | classifier runs | correct issue category suggested | fixture test |
| Dispatch | vendor assigned | agent follows up | work order updated | integration test |

### Edge Cases

- No response from vendor.
- Duplicate requests.
- Incorrect category.
- After-hours escalation.
- Tenant inaccessible.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| tickets | tenant messages | ticket table | PMS | realtime | dedupe |
| vendors | owner roster | vendor table | ops team | versioned | contact verification |
| dispatches | SMS / email | dispatch log | orchestration service | realtime | idempotency |
| updates | vendor replies | status log | PMS | realtime | timestamp required |

**Retention and deletion:** retain dispatch logs and ticket history, expire
raw photos by policy, and keep status updates audit-ready.

**Privacy/security:** tenant isolation, least-privilege vendor contact access,
and no unnecessary image retention.

**Analytics questions:** which vendors miss updates most often and which ticket
categories need better clarifying questions?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one building, one vendor set, SMS credentials, PMS
rollback flag.

**Staging:** ticket intake only, then dispatch in shadow mode.

**Production sequence:** one building, one maintenance category, one vendor
group.

**Smoke test:** submit a maintenance request and verify dispatch and status
update.

**Rollback:** disable orchestration and fall back to manual dispatch.

**Observability:**

- Logs: ticket, vendor, dispatch, reply, status.
- Metrics: time to dispatch, time to close, vendor response rate.
- Alerts: no-reply, dispatch failure, status lag.
- Dashboards: open ticket aging and vendor SLA adherence.

## 10. Post-Launch Iteration Plan

**Metrics:** time to dispatch, time to close, vendor follow-up rate, and PM
hours saved.

**Week-by-week:**

- Week 1: add more ticket types.
- Week 2: improve photo-based triage.
- Week 3: expand vendor follow-up automation.
- Week 4: package for adjacent properties.

**Pivot signals:** add more SMS automation if portal adoption stays low, keep
to one building if operations get noisy, and narrow to one ticket class if
classification quality drops.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_35_Competitor_Teardown.md` - AppFolio / Buildium / Property Meld incumbent map and vendor-friction wedge.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Maintenance_Ticket_Orchestration_Disruptive_Teardown.md` - upstream teardown dossier for the maintenance-routing wedge.
- Official reference points reviewed: AppFolio, Buildium, Yardi, MRI Software, and Property Meld product pages.
