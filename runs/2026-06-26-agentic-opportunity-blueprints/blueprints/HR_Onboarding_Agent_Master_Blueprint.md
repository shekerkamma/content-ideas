---
status: reviewed
use_case: "HR Onboarding Agent"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: medium-high
  competitor: medium-high
  pricing: medium
  implementation: medium
---

# HR Onboarding Agent Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** Head of People Operations or HR Ops leader at a 250-1,000
employee US company hiring at least 10 people/month and using BambooHR or Gusto
plus Slack/Teams, Google Workspace/Microsoft 365, and Okta or Entra.

**Later ICPs:** CIO/IT service owners and COO buyers at companies using
Rippling, Workday, SAP SuccessFactors, ServiceNow HRSD, or distributed/global
onboarding workflows after the simpler HRIS/identity wedge proves readiness
impact.

**Pain wedge:** Onboarding fails because ownership is split across HR, IT,
manager, payroll, benefits, facilities, security, and the new hire. The HRIS
stores records, but it rarely owns the full journey.

**Incumbent weakness:** HRIS/HCM suites are systems of record. Identity tools
provision access. ITSM tools track tickets. Employee journey tools nudge users.
The buyer still needs someone to coordinate the sequence and catch blockers.

**Agentic disruption thesis:** Do not replace the HRIS. Add an approval-first
orchestration layer that reads HRIS/ATS/identity/docs, generates a personalized
onboarding plan, answers policy questions with citations, drafts HR/IT/manager
tasks, and tracks day-one readiness.

**Why now:** Public pricing shows HR software cost fragments quickly across HR,
payroll, benefits, identity, workflow, and EOR modules. Enboarder already
positions around AI orchestration, which validates demand. The faster wedge is a
30-day, bring-your-existing-HRIS pilot with strong auditability and narrower
scope.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 25/30**

This score is inferred from public onboarding pain evidence, scorecard context,
and competitor/pricing research. It should be confirmed with at least three
buyer interviews before being used as a validated market claim.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 7/10

**Who has the problem:** People Ops teams at growing companies, hiring managers
who inherit onboarding gaps, IT teams provisioning devices/apps, and new hires
who cannot find policies or complete tasks.

**Last-time/recency evidence:** Onboarding is triggered every hiring cycle.
Gallup found only 12% of employees strongly agree their organization does a
great job onboarding. Business Insider reported Hitachi had a 10-15 day
onboarding process involving manual forms to IT and facilities before its AI
program targeted process delays and access readiness.

**Current workaround:** Static HRIS checklists, email reminders, Slack/Teams
messages, IT tickets, manager spreadsheets, Notion pages, onboarding buddies,
and manual follow-up from HR coordinators.

**Switching reason:** The agent does not ask buyers to migrate from Workday,
BambooHR, Gusto, Rippling, Okta, or ServiceNow. It coordinates the work across
them and makes the onboarding journey measurable.

**Payment signal:** BambooHR lists plans from `$10-$25/employee/month` for
companies over 25 employees, Gusto ranges from `$49/mo + $6/person` to
`$180/mo + $22/person`, Deel lists contractor/EOR/PEO prices, Okta lists
identity tiers from `$6-$17/user/month`, and Enboarder uses tailored pricing.
The buyer already pays for the stack; the wedge monetizes orchestration and
readiness gaps.

**30-day reachability:** High. HR Ops and IT leaders are reachable by company
size, hiring volume, HRIS stack, and onboarding/job-posting signals.

**Verdict: PROCEED, with ICP discipline.** This is strongest for mid-market
companies with enough onboarding volume to feel the pain but not enough custom
HR/IT automation to solve it internally.

## 2. The 30-Day Scope Definition

**Project name:** Day-One Readiness Agent

**Validated problem:** HRIS records are not the same as onboarding execution;
new hires still wait on access, equipment, manager tasks, policy answers, and
cross-functional coordination.

**Target user:** HR Ops manager at a 100-1,000 employee US company using
BambooHR or Gusto plus Google Workspace/Microsoft 365, Slack/Teams, and Okta or
Entra.

**Core hypothesis:** An approval-first onboarding agent can reduce time-to-ready
and HR/IT follow-up by coordinating tasks across existing tools.

### In Scope

1. **New-hire intake connector**
   - Acceptance criterion: agent ingests name, role, manager, department,
     location, employment type, start date, and required systems from HRIS/CSV.
2. **Policy/document Q&A**
   - Acceptance criterion: new hire receives cited answers from approved
     handbook, benefits, IT, and security documents.
3. **Personalized onboarding plan**
   - Acceptance criterion: plan includes owner, due date, dependency, and
     readiness status for HR, IT, manager, and new hire tasks.
4. **Task drafting and reminders**
   - Acceptance criterion: agent drafts Slack/Teams reminders, IT ticket, and
     manager checklist for human approval.
5. **Readiness dashboard**
   - Acceptance criterion: HR can see blockers, overdue owners, unanswered
     questions, and day-one readiness score.

### Explicitly Out Of Scope

- Replacing HRIS, payroll, benefits administration, ATS, identity provider, or
  ITSM.
- Autonomous payroll, tax, benefits, I-9, immigration, compensation, or
  employment eligibility changes.
- Performance scoring, productivity surveillance, sentiment monitoring, or
  hiring selection decisions.
- Full HR case-management migration.
- Unsupervised identity provisioning.
- Multi-country employment compliance in v1.
- Automated legal/benefits advice beyond cited source text.

### Week-By-Week Milestones

- **Week 1:** Define onboarding template, ingest approved documents, map HR/IT/
  manager/new-hire task owners, and import sample new-hire profiles.
- **Week 2:** Connect HRIS/CSV, Slack/Teams, ITSM or ticket drafting, and
  identity-readiness checklist. Build cited Q&A.
- **Week 3:** Run pilot in shadow mode for 3-5 upcoming hires. HR approves
  plans, reminders, and ticket drafts.
- **Week 4:** Use live for one hiring cohort. Measure readiness, blockers,
  ticket deflection, manager SLA, and unanswered questions.

**Dependencies:** HRIS export/API access, approved policy docs, manager task
template, Slack/Teams workspace, IT ticketing process, identity/app access
matrix, and named HR/IT approvers.

**Acceptance test:** For a pilot cohort, each new hire has a complete plan,
all required tasks have owners/dates, HR can identify blockers, and the agent
answers policy questions only with citations.

**Top risks:** HR data sensitivity, employment-law/bias concerns, and identity
provisioning blast radius. Mitigate with data minimization, approval gates, and
no autonomous payroll/benefits/identity writes.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: Next.js App Router + TypeScript for HR console and readiness views.
- Backend: Python FastAPI for workflow APIs and integrations.
- Agent orchestration: LangGraph or explicit state-machine for onboarding plan,
  blocker detection, reminders, and approvals.
- Retrieval: Postgres + pgvector or managed vector store for handbook, benefits,
  IT, and security documents.
- Database: Postgres for new-hire profiles, plans, tasks, approvals, questions,
  audit events, and integration state.
- Auth: SSO/OIDC with RBAC for HR admin, IT approver, manager, auditor, and new
  hire.
- Integrations: BambooHR/Gusto/Rippling/Workday export, Slack/Teams, Okta/Entra,
  Jira Service Management/ServiceNow/Zendesk IT, Google Workspace/Microsoft 365.
- Observability: audit log, task SLA dashboard, source citation trace, and model
  usage logs.

**Architecture:** HRIS/CSV remains source of truth for employee records. The
agent stores a minimal onboarding execution copy: task plan, owner, status,
source citation, and approval history. It can draft tickets and messages but
does not make payroll, benefits, I-9, or identity changes without approval.

**Core agent loop:** ingest profile, match role/location template, retrieve
policy and IT docs, generate plan, identify missing data, draft reminders/tickets,
answer new-hire questions with citations, monitor blockers, and escalate overdue
or sensitive items.

**Critical design decisions:**

1. **Approval-first writes:** avoids high-risk HRIS/identity mutation in MVP.
2. **Cited Q&A only:** prevents hallucinated benefits/legal guidance.
3. **Readiness score over productivity score:** keeps the product operational,
   not surveillance-oriented.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/onboarding/intake` | Ingest a new hire record or import | Employee payload, source system, tenant ID | Onboarding case ID | HR admin token | Reject on incomplete hire profile |
| GET | `/api/onboarding/cases/:caseId` | Fetch onboarding plan and blockers | Case ID | Tasks, blockers, citations, approvals | RBAC session | 404 if case missing; 403 on tenant mismatch |
| POST | `/api/onboarding/cases/:caseId/draft` | Draft reminder, ticket, or answer | Draft type, source data, recipient | Draft object | HR/IT approver role | Fail closed if policy source is missing |
| POST | `/api/onboarding/cases/:caseId/approve` | Approve a drafted action | Draft ID, approval note | Approved action status | Required approver role | Block writeback on missing approval |
| POST | `/api/webhooks/hris` | Receive HRIS status updates | HRIS webhook payload | Ack + queued sync | Signed webhook secret | Retry transient sync failures |

### Folder / Module Structure

- `app/(console)/onboarding/` for HR queue, hire timeline, and blocker views.
- `app/api/onboarding/` for intake, draft, approval, and case state APIs.
- `app/api/webhooks/` for HRIS, identity, and collaboration updates.
- `services/onboarding-agent/` for orchestration, policy retrieval, and reminder logic.
- `services/connectors/bamboohr/`, `services/connectors/rippling/`, `services/connectors/workday/` for HRIS adapters.
- `services/connectors/slack/`, `services/connectors/teams/`, `services/connectors/okta/` for workflow actions.
- `lib/templates/` for onboarding templates by role, location, and policy set.
- `tests/onboarding/` for edge cases, access controls, and workflow regressions.

### Environment Variables

- `DATABASE_URL`: Postgres for cases, tasks, and audit history.
- `REDIS_URL`: queue backend for reminders and sync jobs.
- `MODEL_ROUTER_API_KEY`: provider-router credential.
- `MODEL_ROUTER_BASE_URL`: model gateway endpoint.
- `BAMBOOHR_API_KEY`: HRIS read/write access.
- `RIPPLING_API_KEY`: HRIS and IT coordination access.
- `WORKDAY_CLIENT_ID`: Workday integration credential.
- `SLACK_BOT_TOKEN`: reminder and approval messaging.
- `TEAMS_BOT_TOKEN`: Microsoft Teams messaging.
- `OKTA_CLIENT_ID`: identity workflow integration.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: traces and metrics export.
- `SENTRY_DSN`: error tracking.

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| HRIS/payroll/benefits record | High | Existing Workday/BambooHR/Gusto/Rippling/Deel | BUY/KEEP | System-of-record migration is not the wedge. |
| Onboarding orchestration | Medium | Enboarder/ServiceNow/HRIS modules can be sales-led or suite-bound | BUILD | Cross-system execution and day-one readiness are the wedge. |
| Identity provisioning | High risk | Okta/Entra/Rippling IT already own access control | HYBRID | Read and draft; do not autonomously provision in v1. |
| Policy Q&A | Low-Medium | Generic knowledge bots exist | BUILD | HR needs source-grounded, access-controlled answers. |
| IT ticket/reminder automation | Low-Medium | ITSM/workflow tools exist | HYBRID | Draft into existing systems with approval. |
| Analytics | Medium | HRIS reports do not show execution blockers well | BUILD | Need readiness, blockers, manager SLA, and question gaps. |

**Bottom line:** Keep the system-of-record stack; build the coordination layer.
The payback comes from fewer HR/IT follow-ups, faster day-one readiness, lower
manager confusion, and fewer new-hire dead ends, not from replacing payroll.

## 5. MVP ROI Business Case

**Current-state cost model:** HR coordinator follow-up time, IT ticket churn,
manager reminder time, delayed access/equipment, repeated policy questions, and
new-hire ramp delay. Software spend is already fragmented across HRIS, payroll,
benefits, identity, ITSM, and collaboration tools.

**Agentic MVP cost model:** 30-day pilot build, HRIS/CSV connector, document
retrieval, task/reminder workflow, Q&A, dashboard, and monthly model/hosting
cost. Maintenance is mostly policy refresh, integration upkeep, and template
tuning.

**Pricing options:**

1. Fixed pilot for one hiring cohort and one HRIS/identity stack.
2. Per active onboarding journey with a platform minimum.
3. Enterprise readiness package with HR/IT integrations and audit controls.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | 5 hires/mo, 1 hour HR/IT follow-up saved per hire, `$55/hr` blended admin cost, `$18K` pilot | Slow | 12-24 months | Use as capability demo only. |
| Base | 20 hires/mo, 3 hours HR/IT/manager follow-up saved per hire, `$65/hr` blended cost, `$25K` pilot, `$2K/mo` run cost | Moderate | 4-9 months | Strong mid-market wedge. |
| Upside | 50+ hires/mo, 4+ hours saved per hire, distributed teams, multiple systems, `$35K` pilot, `$4K/mo` run cost | Fast | 2-4 months | Strong agency/enterprise pilot. |

**No-go condition:** If the buyer has fewer than 5 hires/month or refuses HR/IT
approver ownership, the MVP lacks enough volume and accountability.

Use buyer-specific inputs where available. Default formulas:

```text
Current monthly onboarding coordination cost =
  hires per month * hours of HR/IT/manager follow-up per hire
  * blended loaded hourly cost
  + delayed-readiness cost

Agentic monthly cost =
  platform/run cost + per-active-onboarding fee
  + residual human approval time

Monthly value =
  coordination cost avoided + readiness-delay cost avoided - agentic monthly cost

Payback period =
  pilot/build cost / monthly value
```

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| BambooHR | HRIS | SMB/midmarket HR record and onboarding features | Add-ons fragment total cost | `$10-$25/employee/month` for 25+ employees | BambooHR |
| Gusto | Payroll/HR | Payroll and SMB HR workflow | Add-ons and per-person pricing expand with needs | `$49-$180/mo + $6-$22/person` | Gusto |
| Rippling | HRIS/IT/workforce platform | Strong HR + IT + app/device footprint | Opaque/add-on-heavy enterprise packaging | Public pricing limited; quote/add-on friction | Rippling research |
| Workday / SAP SuccessFactors | Enterprise HCM | Deep enterprise HR system-of-record footprint | Heavy implementation and suite complexity | Enterprise sales-led | Enterprise HCM research |
| HiBob | Midmarket HRIS | Modern midmarket HR platform | Pricing opacity and module expansion risk | Sales-led/no simple public price | HiBob research |
| Deel | Global HR/EOR | Global contractor/EOR/payroll | EOR/PEO costs are material | `$49 contractor`, `$599 EOR`, `$125 PEO` | Deel |
| Okta | Identity | Strong lifecycle/access control | Workflow and lifecycle tiering | `$6-$17/user/month`, annual minimum | Okta |
| Enboarder | Journey orchestration | Closest onboarding orchestration competitor | Tailored quote, enterprise sales motion | No one-size-fits-all pricing | Enboarder |
| ServiceNow HRSD | Enterprise workflow | Strong HR service workflows | Enterprise implementation complexity | Sales-led | ServiceNow |

**Direct threats:** Enboarder and ServiceNow HRSD. **Table stakes:** templates,
nudges, HR/IT integrations, document Q&A, manager visibility. **Do not build:**
payroll, benefits, identity provider, HRIS. **Gaps to exploit:** fast
bring-your-HRIS pilot, approval-first cross-system execution, and readiness
analytics.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Profile intake | HR uploads/exports new hire | Agent ingests profile | Required fields are mapped or flagged missing | Profile mapping report |
| Plan generation | Role/location template exists | HR requests plan | Tasks have owner, due date, dependency, source | Plan audit view |
| Policy Q&A | New hire asks benefits/IT question | Agent answers | Answer cites approved source or escalates | Citation log |
| Reminder drafting | Task is due/overdue | Agent drafts reminder | HR/manager can approve before send | Approval event |
| IT ticket draft | Access/equipment task exists | Agent drafts ticket | Ticket includes role, apps, date, justification | ITSM draft |
| Boundary control | Payroll/benefits/I-9 question appears | Agent responds | Agent refuses action and routes to HR | Escalation log |

**Edge cases:** missing manager, role template absent, conflicting policy docs,
slow HRIS/API, duplicate new-hire record, user asks for another employee's data,
and manager ignores reminder.

## 8. Data Architecture Lite

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| Employee profile | HRIS/CSV | Minimal onboarding profile | HRIS | Batch/API | Required field validation |
| Tasks | Generated plan + templates | Postgres | Agent execution layer | Event updates | Owner/due-date required |
| Policies/docs | Handbook/IT/security docs | Document store + embeddings | Approved doc repository | Scheduled refresh | Version/citation |
| Identity readiness | Okta/Entra/export | Status cache | Identity provider | Read-only/API | No autonomous writes |
| Messages/tickets | Slack/Teams/ITSM drafts | Audit log | External tool after approval | Event callback | Approval required |

**Analytics questions:** Are hires ready by day one? Which owner blocks most
tasks? Which policy questions are unanswered? Which roles need better templates?
How many HR/IT follow-ups were avoided?

**Privacy/security:** minimize SSNs, bank data, tax data, compensation, I-9,
immigration, disability, and background-check fields. Enforce RBAC, audit logs,
retention limits, and no model training on HR data.

## 9. Deployment Sequencing

**Pre-deploy:** confirm HRIS data fields, approved policy docs, role templates,
Slack/Teams permissions, IT ticket process, and HR/IT approvers.

**Staging:** test with fictional hires and sanitized prior onboarding examples.
Verify citations, reminder drafts, missing-data flags, and access boundaries.

**Production:** start with one hiring cohort, HR-approved plans only, read-only
identity status, and draft-only IT tickets. Expand after HR and IT sign off on
readiness metrics.

**Smoke test:** import test hire, generate plan, ask policy question, draft IT
ticket, trigger overdue reminder, verify audit trail, and confirm restricted
data is not exposed.

**Rollback:** disable reminders and ticket drafting, retain read-only dashboard,
export audit, and return to manual HR checklist.

## 10. Post-Launch Iteration Plan

**Metrics:** activation equals percent of hires with complete plan before start
date; retention equals HR/manager weekly usage and next-cohort reuse; revenue
signal equals paid pilot extension or per-hire/onboarding package commitment.

**Week 1:** fix missing templates, source gaps, and bad reminders. No new
systems.

**Week 2:** interview HR, IT, managers, and 5 new hires. Identify the one
blocker most responsible for poor readiness.

**Week 3:** improve that blocker, such as identity status, manager checklist, or
policy Q&A.

**Week 4:** measure day-one readiness and ticket/follow-up reduction.

**Pivot signals:** fewer than 20% of hires use the assistant, HR still manually
tracks everything elsewhere, or policy/security concerns prevent approval.

## Source Notes

- BambooHR Pricing - https://www.bamboohr.com/pricing/ - accessed 2026-06-26 - HRIS pricing and onboarding feature packaging.
- Gusto Pricing - https://gusto.com/product/pricing - accessed 2026-06-26 - SMB HR/payroll per-person pricing.
- Deel Pricing - https://www.deel.com/pricing/ - accessed 2026-06-26 - EOR/PEO/contractor pricing signals.
- Okta Pricing - https://www.okta.com/pricing/ - accessed 2026-06-26 - identity pricing and lifecycle/workflow tiering.
- Enboarder - https://enboarder.com/ and https://enboarder.com/pricing/ -
  onboarding orchestration and pricing opacity.
- ServiceNow HRSD -
  https://www.servicenow.com/products/hr-service-delivery.html - HR workflow
  incumbent.
- Gallup, onboarding and retention -
  https://www.gallup.com/workplace/235121/why-onboarding-experience-key-retention.aspx.
- Business Insider, AI onboarding case -
  https://www.businessinsider.com/generative-ai-employee-onboarding-human-resources-2025-3.
- NIST AI RMF - https://www.nist.gov/itl/ai-risk-management-framework.
- OWASP LLM Top 10 -
  https://owasp.org/www-project-top-10-for-large-language-model-applications/.
