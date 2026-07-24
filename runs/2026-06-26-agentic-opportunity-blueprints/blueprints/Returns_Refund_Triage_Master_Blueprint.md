---
status: reviewed
use_case: "Returns Refund Triage"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Returns Refund Triage Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** ecommerce CX and operations leaders handling high-volume
returns, exchanges, and refund exceptions.

**Later ICPs:** adjacent post-purchase ops teams once one merchant proves edge-
case handling and carrier-claim automation.

**Pain wedge:** the happy path is automated, but the real labor is torn items,
missing packages, late returns, and policy exceptions.

**Incumbent weakness:** Loop Returns, Narvar, and ReturnGo handle the standard
flow well, but they still force humans into edge cases and charge per-return or
enterprise-level fees.

**Agentic disruption thesis:** keep the brand surface native, triage edge cases
inside the help desk, and automate the investigation steps that humans still do
manually.

**Why now:** merchants are under margin pressure and support pressure at the
same time.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 26/30**

The score is inferred from returns volume, per-return SaaS fees, and the human
escalation burden on edge cases.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 8/10

**Who has the problem:** ecommerce teams with return volume and messy
exceptions.

**Current workaround:** manual CX triage and refund approvals.

**Switching reason:** reduce labor, protect margin, and keep customers happy.

**Payment signal:** returns SaaS, CX headcount, and shipping exception costs.

**30-day reachability:** one store and one return-policy family.

**Verdict: PROCEED, but keep the customer experience native.**

## 2. The 30-Day Scope Definition

**Project name:** Refund Triage Agent

**Validated problem:** edge-case returns create manual work and delays.

**Target user:** CX agents and ecommerce ops.

**Core hypothesis:** an agent can resolve the majority of exception cases
without a portal rework.

### In Scope

1. **Return intake and classification**
   - Acceptance criterion: cases are assigned to refund, exchange, claim, or
     human review.
2. **Decisioning**
   - Acceptance criterion: refund, exchange, or investigation actions are
     drafted with policy references.
3. **Helpdesk-native updates**
   - Acceptance criterion: customer replies and internal notes are written back
     to the support system.

### Explicitly Out Of Scope

- Rebuilding the storefront.
- Full warehouse management.
- Autonomous fraud enforcement.
- Separate customer portal as the primary UI.

### Week-By-Week Milestones

- **Week 1:** ingest policy and return feeds.
- **Week 2:** build edge-case classifier.
- **Week 3:** connect helpdesk actions and customer messages.
- **Week 4:** pilot with one store and exception queue.

**Dependencies:** help desk, order data, carrier status, and policy docs.

**Acceptance test:** 80%+ of exceptions are resolved or routed correctly with
an audit trail.

**Top risks:** refund abuse, carrier data quality, and customer anger.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: CX admin console.
- Backend: FastAPI service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for policy and order context.
- Auth: store / helpdesk OAuth.
- Database: Postgres for orders, cases, and decisions.
- Observability: OpenTelemetry plus exception dashboards.
- Hosting: cloud app with queue worker.

**Architecture:** order / return event -> classify -> policy check -> action
draft -> helpdesk update. The agent reads, compares against policy, drafts a
resolution, and writes the audit trail.

**Critical design decisions:**

1. Keep the merchant's help desk as the customer-facing surface.
2. Use policy versioning so refunds stay auditable.
3. Escalate ambiguous or high-value cases to humans.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/returns/ingest` | ingest order / return payload | order event | ack | store token | retry queue |
| POST | `/api/returns/decide` | classify and propose action | return_id | decision draft | service token | fallback to review |
| POST | `/api/returns/update` | apply helpdesk / customer update | return_id, action | update result | service token + helpdesk token | log and retry |

### Folder / Module Structure

- `app/cx/`
- `app/api/returns/`
- `services/classify/`
- `services/policy/`
- `workers/claims/`
- `lib/orders/`

### Environment Variables

- `SHOPIFY_APP_TOKEN`
- `HELPDESK_API_KEY`
- `CARRIER_API_KEY`
- `DATABASE_URL`
- `MODEL_API_KEY`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Returns portal | high | Loop / Narvar already exist | BUY / DO NOT BUILD | not the wedge |
| Exception triage | medium | humans still do it | BUILD | edge-case wedge |
| Carrier claims | medium | manual today | BUILD | high leverage |

**Bottom line:** buy a commodity portal if needed, but build the exception
resolver inside the help desk.

## 5. MVP ROI Business Case

**Current-state cost model:** CX labor, refund leakage, delayed resolutions,
and shipping-claim labor.

**Agentic MVP cost model:** order-event ingestion, model calls, exception
review labor, and audit storage.

**Pricing options:**

1. Per-order.
2. Per-exception case.
3. Merchant bundle.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | few exceptions, weak policy clarity | 12-18 months | month 14+ | marginal |
| Base | 30-40% of exception cases automated or accelerated | 6-8 months | month 8-10 | moderate |
| Upside | high-volume store, strong carrier automation | 3-5 months | month 4-5 | strong fit |

**Formulas**

```text
Monthly value =
  CX labor avoided + refund leakage reduced + claims labor avoided
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if the merchant insists on a separate customer portal,
the wedge weakens.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Loop Returns | returns platform | exchange retention | per-return fees | enterprise / usage | `runs/2026-06-26-agentic-opportunity-blueprints/source/UC49_Returns_Refund_Triage_Competitor_Teardown.md` |
| Narvar | post-purchase | enterprise logistics footprint | complex implementation | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/UC49_Returns_Refund_Triage_Competitor_Teardown.md` |
| ReturnGo | returns platform | mid-market friendly | rule-tree complexity | lower-cost SaaS | `runs/2026-06-26-agentic-opportunity-blueprints/source/UC49_Returns_Refund_Triage_Competitor_Teardown.md` |

**Direct threats:** Loop Returns and Narvar.

**What not to build:** a separate customer portal, warehouse suite, or fraud
adjudication engine.

**Agentic wedge:** handle edge cases, automate carrier disputes, and flatten
the execution cost.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Edge-case intake | unique complaint | case enters system | correct disposition suggested | replay test |
| Carrier dispute | package lost | claim triggered | investigation opened | API fixture test |
| Helpdesk update | refund approved | action executed | customer note is written | integration test |

### Edge Cases

- Damaged item with photo evidence.
- Late return window.
- International shipments.
- Partial refund.
- Duplicate case.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| orders | Shopify | order table | Shopify | realtime | idempotency |
| policies | ops docs | policy store | ops team | versioned | approval state |
| cases | helpdesk | return table | helpdesk | realtime | audit log |
| carrier status | carrier API | carrier table | carrier | realtime | retry |

**Retention and deletion:** retain audit trails and policy versions, delete raw
PII per merchant policy, and mask payment details.

**Privacy/security:** customer PII redaction, tenant isolation, and least-
privilege helpdesk scope.

**Analytics questions:** which exception types drive the most human escalation
and which carriers produce the most claim volume?

## 9. Deployment Sequencing

**Pre-deploy checklist:** Shopify app, helpdesk access, carrier keys, policy map.

**Staging:** review-only mode, then limited auto-resolution.

**Production sequence:** one store, one policy family, one queue.

**Smoke test:** verify a damaged-item case routes correctly and writes the right
note.

**Rollback:** disable auto-action and keep triage-only mode.

**Observability:**

- Logs: order id, policy hit, action draft, final outcome.
- Metrics: automation rate, refund value saved, resolution time.
- Alerts: carrier API failure, policy ambiguity, customer escalation spike.
- Dashboards: exception backlog and claim resolution rate.

## 10. Post-Launch Iteration Plan

**Metrics:** automation rate, refund leakage reduction, support time saved, and
customer satisfaction.

**Week-by-week:**

- Week 1: expand policy coverage.
- Week 2: improve image / photo handling.
- Week 3: add carrier claim automation.
- Week 4: package for adjacent stores.

**Pivot signals:** offer brandable UI as an optional wrapper if portal demand
is strong, deepen claims automation if carrier disputes dominate, and move high-
value cases to human approval if policy is too loose.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/UC49_Returns_Refund_Triage_Competitor_Teardown.md` - returns incumbents, pricing friction, and edge-case weakness.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/UC49_Returns_Refund_Triage_Disruptive_Teardown.md` - upstream teardown dossier for the returns/refund wedge.
- Official reference points reviewed: Shopify, Gorgias, Loop Returns, AfterShip, and Zendesk product pages.
