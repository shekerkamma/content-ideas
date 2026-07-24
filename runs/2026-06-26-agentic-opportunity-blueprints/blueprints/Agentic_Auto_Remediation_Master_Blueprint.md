---
status: reviewed
use_case: "Agentic Auto-remediation"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Agentic Auto-remediation Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** SecOps, SRE, and platform engineering leaders handling high-
confidence alerts and repetitive remediation actions.

**Later ICPs:** adjacent ops teams once one low-risk action proves that policy-
bound remediation is safe and auditable.

**Pain wedge:** manual remediation adds minutes or hours after an alert,
extending damage and downtime.

**Incumbent weakness:** SOAR and runbook tools break when environments drift.

**Agentic disruption thesis:** execute one approved remediation action with
durable auditability and bounded policy.

**Why now:** response platforms already have APIs, but the orchestration logic
still assumes static conditions.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 25/30**

The score is inferred from recurring containment actions, modern response
spend, and the fact that static playbooks keep drifting out of date.

- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 8/10

**Who has the problem:** teams with recurring containment and rollback actions.

**Current workaround:** runbooks, shell scripts, and manual approvals.

**Switching reason:** less MTTR, fewer errors, and less playbook maintenance.

**Payment signal:** enterprise SOAR, response, and incident-management
contracts.

**30-day reachability:** one low-risk remediation action can be proven safely.

**Verdict: PROCEED, but keep the action set tiny.**

## 2. The 30-Day Scope Definition

**Project name:** Bounded Response Executor

**Validated problem:** high-confidence alerts still require manual coordination
for safe containment.

**Target user:** SOC or SRE operator who approves or supervises the action.

**Core hypothesis:** a policy-bound agent can execute approved remediations
faster than a human-run playbook.

### In Scope

1. **Alert ingestion**
   - Acceptance criterion: the agent receives alert payloads from a limited set
     of sources.
2. **Action selection**
   - Acceptance criterion: the agent recommends one approved remediation.
3. **Execution with audit**
   - Acceptance criterion: approved remediation runs with full log capture and
     rollback path.

### Explicitly Out Of Scope

- Autonomous broad incident response.
- Unbounded shell access.
- Full SOAR replacement.
- Writing policy from scratch.

### Week-By-Week Milestones

- **Week 1:** define one low-risk action and policy boundaries.
- **Week 2:** connect alert source and dry-run execution.
- **Week 3:** add approval workflow and audit trail.
- **Week 4:** pilot one remediation in production with supervision.

**Dependencies:** alert sources, runbook approval, and rollback commands.

**Acceptance test:** the agent performs one approved action and logs every
step, source, and approval.

**Top risks:** bad action selection, environment drift, and overbroad access.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: ops console for approvals and audit replay.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for runbooks and policies.
- Auth: SSO plus scoped service credentials.
- Database: Postgres for alerts, actions, approvals, and audit logs.
- Observability: OpenTelemetry, SIEM export, and action tracing.
- Hosting: containerized service close to the incident-management stack.

**Architecture:** alert -> policy check -> proposed action -> approval ->
execution -> audit log -> rollback path. The agent remains bounded and
observable.

**Critical design decisions:**

1. Limit the action catalog to one or two safe remediations.
2. Require explicit policy match before execution.
3. Keep rollback one click away.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/alerts/ingest` | ingest alert payload | alert event | queued alert | service token | retry queue |
| POST | `/api/remediate/propose` | propose remediation | alert_id | proposed action | service token | fallback to manual |
| POST | `/api/remediate/execute` | execute approved action | alert_id, approval | execution result | approver token | stop on policy miss |

### Folder / Module Structure

- `app/ops/`
- `app/api/alerts/`
- `services/policy/`
- `services/remediate/`
- `workers/execution/`
- `lib/audit/`

### Environment Variables

- `ALERT_SOURCE_TOKEN`
- `RUNBOOK_TOKEN`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `SIEM_EXPORT_URL`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Incident platform | high | PagerDuty / ServiceNow own the workflow | BUY | not the wedge |
| Runbook orchestration | medium | SOAR tools drift with infra | BUILD | core wedge |
| Audit logging | low | existing stack helps | HYBRID | integrate tightly |

**Bottom line:** buy the incident shell and build the bounded execution layer.

## 5. MVP ROI Business Case

**Current-state cost model:** MTTR, engineer interrupt cost, and playbook
maintenance.

**Agentic MVP cost model:** alert ingestion, model usage, execution logs, and
human approval time.

**Pricing options:**

1. Per incident.
2. Per approved remediation.
3. Enterprise response package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | rare incidents, narrow use | 12-18 months | month 14+ | limited |
| Base | one action saves repeated toil | 6-9 months | month 8-12 | strong ops fit |
| Upside | recurring containment actions | 3-5 months | month 4-6 | high leverage |

**Formulas**

```text
Monthly value =
  MTTR reduction + engineer interrupt cost reduced + playbook maintenance saved
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if the action cannot be made fully auditable, do not
execute it.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Google SecOps | security ops | analytics and response breadth | still assumes manual orchestration | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_35_Competitor_Teardown.md` |
| Splunk | observability / security | massive telemetry footprint | workflow drift and complexity | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_35_Competitor_Teardown.md` |
| ServiceNow | workflow platform | enterprise approval flows | heavy implementation | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_35_Competitor_Teardown.md` |

**Direct threats:** Google SecOps and ServiceNow.

**What not to build:** a full incident-management platform or autonomous
security brain.

**Agentic wedge:** execute one approved remediation action safely, with policy
checks and rollback.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Alert ingest | high-confidence alert | system receives event | action candidate queued | replay test |
| Action proposal | policy match exists | agent evaluates | approved action suggested | policy fixture |
| Execution | approver grants approval | action runs | logs capture every step | audit replay |

### Edge Cases

- Missing rollback.
- Ambiguous alert.
- Environment drift.
- Policy mismatch.
- Execution timeout.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| alerts | monitoring / SIEM | alert table | source tools | realtime | schema validation |
| policies | runbooks | policy table | security owner | versioned | approval state |
| executions | agent output | execution log | remediation service | realtime | command allowlist |
| approvals | operator action | approval table | approver | realtime | RBAC |

**Retention and deletion:** retain audit logs and approvals, expire raw alert
payloads by policy, and keep rollback data available for the incident window.

**Privacy/security:** command allowlists, network limits, and least-privilege
service credentials.

**Analytics questions:** which alerts are safe to automate and which remediations
still need too much manual supervision?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one action, rollback command, approval owner, policy
map.

**Staging:** dry-run only, then supervised execution in one environment.

**Production sequence:** one action, one alert source, one approval flow.

**Smoke test:** trigger the action in a controlled environment and verify logs.

**Rollback:** disable execution and fall back to manual runbook.

**Observability:**

- Logs: alert, policy match, action, approval, result.
- Metrics: MTTR change, execution success, rollback rate.
- Alerts: policy miss, command failure, approval lag.
- Dashboards: approved actions and remediation success.

## 10. Post-Launch Iteration Plan

**Metrics:** MTTR reduction, approval time, remediation success rate, and
playbook maintenance reduction.

**Week-by-week:**

- Week 1: add one more safe action.
- Week 2: tighten policy matching.
- Week 3: improve audit replay.
- Week 4: package for adjacent teams.

**Pivot signals:** narrow the action set if drift appears, require stricter
approvals if trust drops, and keep to one class of incidents if the environment
is too heterogeneous.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Agentic_Auto_Remediation_Disruptive_Teardown.md` - upstream teardown dossier for the auto-remediation wedge.
- Official reference points reviewed: PagerDuty, Datadog, Splunk, Dynatrace, and AWS Systems Manager product pages.
- `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_35_Competitor_Teardown.md` - SOAR / response incumbents and bounded-remediation wedge.
