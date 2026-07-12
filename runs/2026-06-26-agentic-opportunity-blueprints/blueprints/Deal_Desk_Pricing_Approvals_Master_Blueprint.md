---
status: reviewed
use_case: "Deal Desk Pricing Approvals"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Deal Desk Pricing Approvals Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** sales ops, finance, and deal desk leaders.

**Later ICPs:** revops teams once one discount policy proves the orchestration
layer.

**Pain wedge:** discount approvals stall deals and clog Slack threads.

**Incumbent weakness:** CPQ and approval workflows are rigid and slow.

**Agentic disruption thesis:** check margin, policy, and history instantly, then
approve or escalate.

**Why now:** revenue teams want speed, but CPQ systems still add process drag.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 26/30**

The score is inferred from heavy implementation fees, CPQ complexity, and the
common habit of taking quotes offline.

- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 9/10

**Who has the problem:** reps requesting discounts and deal exceptions.

**Current workaround:** Slack approvals and manual margin spreadsheets.

**Switching reason:** faster approvals and fewer lost deals.

**Payment signal:** CPQ and revenue ops tools.

**30-day reachability:** one discount policy and one CRM object can prove the
wedge.

**Verdict: PROCEED, but keep the ERP catalog intact.**

## 2. The 30-Day Scope Definition

**Project name:** Margin Guard Copilot

**Validated problem:** discount requests wait too long for approval.

**Target user:** rep plus deal desk approver.

**Core hypothesis:** the agent can approve simple requests and escalate the
rest.

### In Scope

1. **Policy ingest**
   - Acceptance criterion: pricing rules and margin guardrails are indexed.
2. **Approval decisioning**
   - Acceptance criterion: the agent routes low-risk deals automatically.
3. **Explain / escalate**
   - Acceptance criterion: approver sees a policy explanation for every deal.

### Explicitly Out Of Scope

- New CPQ visual rule builder.
- ERP catalog replacement.
- Complex contract redlining.
- Replacing pricing governance.

### Week-By-Week Milestones

- **Week 1:** ingest one discount policy and one CRM object.
- **Week 2:** build margin checks and approval routing.
- **Week 3:** draft Slack / email approvals.
- **Week 4:** pilot with one sales pod.

**Dependencies:** CRM data, pricing policy, and approver owner.

**Acceptance test:** a low-risk request can be approved with a logged
explanation and the rest routed correctly.

**Top risks:** margin mistakes, policy drift, and approval trust.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: deal desk review console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for pricing policies and
  deal history.
- Auth: SSO plus CRM credentials.
- Database: Postgres for deals, policies, approvals, and logs.
- Observability: OpenTelemetry and deal audit logs.
- Hosting: cloud app with queue worker.

**Architecture:** deal request -> policy check -> approval routing -> log ->
escalation. The agent handles exceptions with history and margin context.

**Critical design decisions:**

1. Do not build a massive visual rule builder.
2. Use history and policy for explainability.
3. Slack is the approval surface, not the system of record.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/deals/ingest` | ingest discount request | deal payload | deal id | service token | retry queue |
| POST | `/api/deals/approve` | approve or escalate | deal id, context | approval result | approver token | fail closed on policy miss |
| POST | `/api/deals/explain` | explain decision | deal id | policy explanation | service token | fallback to rule summary |

### Folder / Module Structure

- `app/(console)/deal-desk/`
- `app/api/deals/`
- `services/policy/`
- `services/approve/`
- `workers/escalate/`
- `lib/margin/`

### Environment Variables

- `DATABASE_URL`
- `MODEL_ROUTER_API_KEY`
- `CRM_API_KEY`
- `APPROVAL_QUEUE_URL`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| CPQ platform | high | Salesforce / DealHub already exist | BUY | not the wedge |
| Approval orchestration | medium | rigid workflows are the pain | BUILD | core wedge |
| Slack / CRM integration | medium | commodity | BUY / REUSE | keep workflow native |

**Bottom line:** buy CPQ, build the approval orchestration layer.

## 5. MVP ROI Business Case

**Current-state cost model:** lost deal time, manual spreadsheets, and rep
friction.

**Agentic MVP cost model:** policy ingest, decisioning, approvals, and logs.

**Pricing options:**

1. Fixed pilot by sales pod.
2. Per approved request.
3. Enterprise revenue package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low request volume | 12-18 months | month 14+ | limited |
| Base | faster approvals | 6-9 months | month 8-12 | good fit |
| Upside | fewer lost deals | 3-5 months | month 4-6 | high leverage |

**Formulas**

```text
Monthly value =
  deal time saved + lost-deal reduction + admin reduction
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if pricing policy cannot be encoded clearly, do not
autoprovide approvals.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Salesforce CPQ | CPQ | CRM integration | massive SI burden | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Deal_Desk_Pricing_Approvals_Competitor_Teardown.md` |
| Conga CPQ | CPQ | quoting breadth | expensive enterprise pricing | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Deal_Desk_Pricing_Approvals_Competitor_Teardown.md` |
| DealHub | deal room | agile platform | scales expensively | per-user | `runs/2026-06-26-agentic-opportunity-blueprints/source/Deal_Desk_Pricing_Approvals_Competitor_Teardown.md` |
| Oracle CPQ | CPQ | enterprise depth | over-engineered | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Deal_Desk_Pricing_Approvals_Competitor_Teardown.md` |

**Direct threats:** Salesforce CPQ and DealHub.

**What not to build:** a rigid rules engine or ERP replacement.

**Agentic wedge:** orchestration over Slack, dynamic interpretation of quote
requests, and natural-language update of pricing logic.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| policy ingest | pricing doc loaded | system runs | policies are searchable | parser test |
| approval | simple request | agent evaluates | auto-approval or escalation | replay test |
| explanation | rep asks why | explanation runs | clear policy context returned | review test |

### Edge Cases

- Special discount.
- Multi-product bundle.
- Missing margin data.
- Duplicate approval.
- ERP outage.
- Policy override.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| policies | docs | policy table | pricing team | versioned | approval state |
| deals | CRM | deal table | CRM | realtime | field mapping |
| approvals | agent / manager | approval table | approver | realtime | audit trail |
| logs | Slack / CRM | log table | system | realtime | immutable |

**Retention and deletion:** retain deal and approval lineage, delete transient
prompt state after retention, and keep policy history.

**Privacy/security:** pricing data must be tenant-separated, encrypted, and
role-gated.

**Analytics questions:** which discount types are approved most often and
which policies create the most Slack churn?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one policy, one CRM object, approver owner, rollback
flag.

**Staging:** draft-only, then approval routing.

**Production sequence:** one sales pod, one deal type, one approval channel.

**Smoke test:** one discount request generates the right decision.

**Rollback:** disable auto-approval and keep explanation-only mode.

**Observability:**

- Logs: policy, deal, approval, escalation.
- Metrics: approval time, lost-deal rate, rep acceptance.
- Alerts: policy mismatch, CRM failure, routing delay.
- Dashboards: approval queue and deal aging.

## 10. Post-Launch Iteration Plan

**Metrics:** approval time, lost-deal rate, rep acceptance, and admin burden.

**Week-by-week:**

- Week 1: add another discount policy.
- Week 2: improve explanations.
- Week 3: tighten margin checks.
- Week 4: package for more pods.

**Pivot signals:** keep it explanation-only if trust is low and avoid building
custom pricing logic editors.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/Deal_Desk_Pricing_Approvals_Competitor_Teardown.md` - CPQ incumbent map and approval-orchestration wedge.
- Oracle CPQ - https://www.oracle.com/cx/sales/cpq/ - accessed 2026-06-26 - CPQ and automated approvals backdrop.
- Salesforce Revenue Cloud - https://www.salesforce.com/products/revenue-cloud/overview/ - accessed 2026-06-26 - revenue lifecycle and CPQ backdrop.
- DealHub - https://dealhub.io/ - accessed 2026-06-26 - guided selling and quote-to-revenue backdrop.
- The wedge is approval orchestration inside the rep workflow, not a new CPQ rules studio.
- The buyer still keeps CPQ and ERP as the system of record; the agent only removes the Slack bottleneck.
- That means the assistant should be conservative by default, explaining policy and margin before granting any exception.
- The narrow win is reducing approval lag and keeping reps from taking quote exceptions offline.
- For adoption, the assistant should make the approver faster, not make them irrelevant.
- If the policy is unclear, the right behavior is escalation, not cleverness.
- The best customer proof is fewer Slack threads and faster quote turnaround, not a brand-new pricing cockpit.
