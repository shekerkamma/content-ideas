---
status: reviewed
use_case: "IT Service Desk"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# IT Service Desk Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** IT operations and employee-experience leaders.

**Later ICPs:** adjacent internal ops teams once one request class proves the
chat-to-action loop.

**Pain wedge:** routine requests clog the service desk and force users into
ticket queues.

**Incumbent weakness:** ticket-first tools make simple actions feel slow.

**Agentic disruption thesis:** answer in chat, then execute safe IT actions with
approval.

**Why now:** ITSM vendors already sell AI, but the ticket remains the center of
gravity.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

The score is inferred from internal support load, ITSM spend, and the direct
cost of queue churn.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** internal IT teams handling password resets, access,
and provisioning.

**Current workaround:** ticket forms, chat macros, and manual approvals.

**Switching reason:** deflect tickets and reduce queue churn.

**Payment signal:** per-agent ITSM and employee-service pricing.

**30-day reachability:** password reset, access, and one approval path are
enough to prove the wedge.

**Verdict: PROCEED, but keep actions bounded.**

## 2. The 30-Day Scope Definition

**Project name:** Chat-Based IT Helper

**Validated problem:** employees want simple self-service instead of ticket
submission.

**Target user:** employee plus IT helpdesk admin.

**Core hypothesis:** a chat-native assistant can solve repetitive IT requests
and keep the ITSM record intact.

### In Scope

1. **Request intake**
   - Acceptance criterion: employee submits request in chat and receives a
     structured ticket or action path.
2. **Approval and execution**
   - Acceptance criterion: safe actions run only after policy approval.
3. **Ticket logging**
   - Acceptance criterion: all actions are written back to ITSM.

### Explicitly Out Of Scope

- New ITSM platform.
- Full endpoint management.
- Broad omnichannel support.
- Unbounded action execution.

### Week-By-Week Milestones

- **Week 1:** define request classes and approval flows.
- **Week 2:** build chat intake and KB answers.
- **Week 3:** add approved actions and logging.
- **Week 4:** pilot with one department.

**Dependencies:** KB, IAM, ITSM, and approval paths.

**Acceptance test:** one password reset and one access request succeed with a
full audit trail.

**Top risks:** permission mistakes, KB gaps, and action latency.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: chat surface and admin console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for KB and policies.
- Auth: SSO plus IAM / ITSM service credentials.
- Database: Postgres for requests, approvals, actions, and audit logs.
- Observability: OpenTelemetry and action metrics.
- Hosting: cloud app with queue worker.

**Architecture:** chat -> classify -> retrieve -> approval -> action -> ITSM
log. The assistant preserves the ITSM record while resolving simple requests.

**Critical design decisions:**

1. Keep ticketing as the system of record.
2. Limit actions to low-risk, policy-approved tasks.
3. Require approval for any privileged action.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/requests/ingest` | ingest employee request | message payload | request_id | service token | retry queue |
| POST | `/api/requests/answer` | answer with KB or action path | request_id | answer, citations | service token | fallback to ticket |
| POST | `/api/requests/execute` | run approved action | request_id, approval | action result | approver token | stop on policy miss |

### Folder / Module Structure

- `app/it/`
- `app/api/requests/`
- `services/classify/`
- `services/actions/`
- `workers/execution/`
- `lib/iam/`

### Environment Variables

- `ITSM_API_KEY`
- `IAM_API_KEY`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `KB_SYNC_TOKEN`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| ITSM platform | high | ServiceNow / Jira already own it | BUY | not the wedge |
| Chat helper | medium | ticket-first UX is the pain | BUILD | core wedge |
| Safe action execution | medium | needs policy + approval | BUILD | high leverage |

**Bottom line:** buy the ITSM shell and build the chat-to-action layer.

## 5. MVP ROI Business Case

**Current-state cost model:** helpdesk labor, queue churn, and provisioning
delays.

**Agentic MVP cost model:** chat intake, model usage, approvals, execution
logs, and storage.

**Pricing options:**

1. Per department.
2. Usage / outcome model per resolved request.
3. Enterprise package with analytics.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low chat adoption | 12-18 months | month 14+ | needs better placement |
| Base | 20-30% deflection | 6-9 months | month 8-12 | routine requests only |
| Upside | 40% deflection | 3-6 months | month 4-6 | strong adoption |

**Formulas**

```text
Monthly value =
  tickets avoided + provisioning time reduced + queue churn reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if permissions cannot be segmented by request type, the
assistant cannot safely execute.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| ServiceNow ITSM | ITSM | deep workflow | heavy implementation | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/IT_Service_Desk_Disruptive_Teardown.md` |
| Jira Service Management | ITSM | strong Atlassian fit | seat / add-on creep | public tiers | `runs/2026-06-26-agentic-opportunity-blueprints/source/IT_Service_Desk_Disruptive_Teardown.md` |
| Freshservice | ITSM | mid-market usability | ticket-first design | public tiers | `runs/2026-06-26-agentic-opportunity-blueprints/source/IT_Service_Desk_Disruptive_Teardown.md` |
| Zendesk Employee Service | employee service | familiar UX | support DNA | seat-based | `runs/2026-06-26-agentic-opportunity-blueprints/source/IT_Service_Desk_Disruptive_Teardown.md` |
| SysAid | ITSM | AI-native service management | quote-based enterprise packaging | custom / quote-based | `runs/2026-06-26-agentic-opportunity-blueprints/source/IT_Service_Desk_Disruptive_Teardown.md` |
| TOPdesk | service management platform | clear agent-based tiers | more than 50 agents requires contact sales | per-agent monthly pricing | `runs/2026-06-26-agentic-opportunity-blueprints/source/IT_Service_Desk_Disruptive_Teardown.md` |
| ManageEngine ServiceDesk Plus | ITSM | lower entry cost and tiered editions | technician/node licensing complexity | public technician pricing | `runs/2026-06-26-agentic-opportunity-blueprints/source/IT_Service_Desk_Disruptive_Teardown.md` |
| SolarWinds Service Desk | ITSM | clear public pricing and broad ITSM scope | still ticket-centered | public per-technician pricing | `runs/2026-06-26-agentic-opportunity-blueprints/source/IT_Service_Desk_Disruptive_Teardown.md` |

**Direct threats:** ITSM suites, chatbots, FAQ bots, and lower-cost ITSM entry products such as SysAid, TOPdesk, ServiceDesk Plus, and SolarWinds.

**What not to build:** a new ITSM platform or full endpoint management.

**Agentic wedge:** chat-native intake, safe actions with approval, and ticket
logging without forcing users into the queue.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| password reset | user request | approved flow runs | reset completes | audit log |
| software access | manager approval | action executes | access granted | IAM state check |
| troubleshooting | user asks | KB retrieval runs | steps are cited | scenario test |

### Edge Cases

- No approved KB.
- ITSM or IAM failure.
- Unsupported request rejected.
- Pending state visible.
- Duplicate request idempotent.
- User cannot self-approve restricted workflows.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| requests | chat / API | request table | assistant | realtime | validation |
| approvals | manager | approvals table | approval channel | realtime | idempotency |
| actions | downstream systems | action table | target system | realtime | permission checks |
| KB | docs | vector store | docs owner | batch | content approval |

**Retention and deletion:** retain request history, approvals, and action
audit; delete transient prompts after the retention window.

**Privacy/security:** least privilege, tenant isolation, and approval
traceability.

**Analytics questions:** which request types can be safely automated next and
which approvals cause the most delay?

## 9. Deployment Sequencing

**Pre-deploy checklist:** KB synced, IAM tested, approval path verified.

**Staging:** run against pilot users only.

**Production sequence:** shadow mode -> approval-only -> narrow automation.

**Smoke test:** one password reset and one access request succeed.

**Rollback:** disable actions, keep chat answers and ticket logging.

**Observability:**

- Logs: request, approval, action, failure.
- Metrics: deflection, latency, approval success.
- Alerts: IAM errors, ticketing failures, request spikes.
- Dashboards: request type and resolution rate.

## 10. Post-Launch Iteration Plan

**Metrics:** assistant usage, repeat requests through chat, tickets deflected,
and time saved.

**Week-by-week:**

- Week 1: add a second request type.
- Week 2: add better escalation.
- Week 3: add endpoint diagnostics.
- Week 4: expand to more teams.

**Pivot signals:** move the assistant into the primary workspace if users
bypass chat, limit to low-risk requests if approvals are too slow, and focus on
action-only requests if KB answers are weak.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/IT_Service_Desk_Disruptive_Teardown.md` - ITSM incumbent map and chat-to-action wedge.
- ServiceNow ITSM - https://www.servicenow.com/products/itsm.html - accessed 2026-06-26 - ITSM and employee service positioning.
- Jira Service Management Pricing - https://www.atlassian.com/software/jira/service-management/pricing - accessed 2026-06-26 - public per-agent pricing.
- Freshservice Pricing - https://www.freshworks.com/freshservice/pricing/ - accessed 2026-06-26 - ITSM pricing tiers.
- Zendesk Pricing - https://www.zendesk.com/pricing/ - accessed 2026-06-26 - employee service and AI packaging.
- SysAid Pricing - https://www.sysaid.com/pricing - accessed 2026-06-26 - quote-based ITSM with AI included and enterprise customization.
- TOPdesk Pricing - https://www.topdesk.com/en/pricing/ - accessed 2026-06-26 - per-agent service management tiers and contact-sales threshold.
- ManageEngine ServiceDesk Plus Pricing - https://www.manageengine.com/products/service-desk/pricing.html - accessed 2026-06-26 - technician-based ITSM pricing and edition tiers.
- SolarWinds Service Desk Pricing - https://www.solarwinds.com/service-desk/pricing - accessed 2026-06-26 - per-technician pricing and broad ITSM feature set.
