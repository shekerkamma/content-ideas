---
status: reviewed
use_case: "Supplier Dispute Resolution"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: medium-high
  competitor: medium-high
  pricing: medium-high
  implementation: medium-high
---

# Supplier Dispute Resolution Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** AP manager or procurement ops leader at a mid-market
distributor or manufacturer.

**Later ICPs:** finance ops teams once one exception queue proves the workflow.

**Pain wedge:** three-way matching and dispute emails are slow and repetitive.

**Incumbent weakness:** AP tools and portals still rely on manual exception
handling.

**Agentic disruption thesis:** match invoices to PO / receipt data, then draft
supplier disputes automatically for review.

**Why now:** AP teams already use email and ERP, so the wedge is workflow speed,
not system replacement.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 24/30**

The score is inferred from recurring invoice exceptions, supplier email churn,
and the cost of AP labor.

- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 7/10

**Who has the problem:** AP and procurement operations teams.

**Current workaround:** ERP portals, spreadsheets, and email threads.

**Switching reason:** reduce AP handling time and resolve exceptions faster.

**Payment signal:** AP automation and ERP spend already exists.

**30-day reachability:** high in companies with recurring invoice volume.

**Verdict: PROCEED, but keep the ERP as the system of record.**

## 2. The 30-Day Scope Definition

**Project name:** AP Exception Copilot

**Validated problem:** invoice exceptions slow AP and annoy suppliers.

**Target user:** AP analyst or manager.

**Core hypothesis:** the agent can match invoices, detect discrepancies, and
draft dispute emails with citations.

### In Scope

1. **Three-way match**
   - Acceptance criterion: invoice, PO, and receipt data are compared.
2. **Dispute drafting**
   - Acceptance criterion: supplier email cites the mismatch reason.
3. **Approval**
   - Acceptance criterion: a manager approves before any supplier send.

### Explicitly Out Of Scope

- ERP replacement.
- Full procurement suite.
- Autonomous supplier negotiation.
- Recreating core accounting records.

### Week-By-Week Milestones

- **Week 1:** define invoice types and threshold policy.
- **Week 2:** build match and exception classification.
- **Week 3:** draft supplier dispute emails.
- **Week 4:** pilot on one AP queue.

**Dependencies:** ERP data, email channel, threshold policy, and AP owner.

**Acceptance test:** the agent matches invoices, drafts a dispute, and logs the
approval.

**Top risks:** false disputes, stale ERP data, and supplier backlash.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: AP review console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for policies and vendor notes.
- Auth: ERP / SSO plus email service credentials.
- Database: Postgres for invoices, POs, receipts, disputes, and approvals.
- Observability: OpenTelemetry and AP audit logs.
- Hosting: cloud app with queue worker.

**Architecture:** invoice -> match -> dispute draft -> approval -> supplier
send -> audit log. The agent keeps AP review in the loop.

**Critical design decisions:**

1. Human approval before supplier send.
2. Tolerance thresholds to avoid frivolous disputes.
3. Email-first channel because suppliers already use it.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/ap/ingest` | ingest invoice / PO / receipt data | payload bundle | record id | service token | retry queue |
| POST | `/api/ap/match` | match documents | record id | match result | service token | fallback to review |
| POST | `/api/ap/dispute` | draft dispute email | record id | email draft | service token | require approval |

### Folder / Module Structure

- `app/(console)/ap/`
- `app/api/ap/`
- `services/match/`
- `services/dispute/`
- `workers/email/`
- `lib/audit/`

### Environment Variables

- `DATABASE_URL`
- `MODEL_ROUTER_API_KEY`
- `ERP_API_KEY`
- `EMAIL_API_KEY`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| AP matching | Medium | portals are clunky | BUILD | exception handling is the wedge |
| ERP system | High | existing | BUY / KEEP | source of truth stays |
| Email send | Low | commodity | BUY / REUSE | keep the workflow native |

**Bottom line:** keep the ERP, build the exception copilot.

## 5. MVP ROI Business Case

**Current-state cost model:** AP analyst time, supplier back-and-forth, and
duplicate email churn.

**Agentic MVP cost model:** match, draft, approval, email send, and model use.

**Pricing options:**

1. Fixed pilot per AP queue.
2. Per invoice exception.
3. Enterprise platform package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low exception volume | 12+ months | 12+ | learn only |
| Base | recurring exceptions | 4-8 months | 4-8 | best wedge |
| Upside | high invoice volume | 2-4 months | 2-4 | scale across vendors |

**Formulas**

```text
Monthly value =
  AP handling time saved + supplier resolution time reduced + duplicate work reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if the ERP data is too incomplete or supplier disputes
must be fully autonomous, stop.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| SAP Ariba | spend/AP | enterprise breadth | clunky workflows | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Procurement_Competitor_Teardown.md` |
| Coupa | spend/AP | footprint and integrations | heavy implementation | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Procurement_Competitor_Teardown.md` |
| Bill.com | AP automation | SMB reach | not exception-deep | subscription | `runs/2026-06-26-agentic-opportunity-blueprints/source/Procurement_Competitor_Teardown.md` |

**Direct threats:** ERP AP tools and spend suites.

**What not to build:** ERP replacement.

**Agentic wedge:** exception language, fast supplier follow-up, and AP-native
email resolution.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| 3-way match | invoice, PO, receipt present | match runs | discrepancy identified or cleared | match report |
| dispute draft | mismatch exists | draft runs | email cites PO and reason | reviewer view |
| approval | manager approves | send runs | supplier email is sent and logged | audit log |

### Edge Cases

- Rounding differences.
- Partial receipts.
- Duplicate invoices.
- Missing PO.
- Vendor name mismatch.
- ERP outage.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| invoices | ERP / AP | invoice table | ERP | API | vendor / ID validation |
| POs | ERP | PO table | ERP | API | line-item checks |
| receipts | ERP / WMS | receipt table | ERP | API | quantity validation |
| disputes | agent | dispute table | agent | per run | approval required |

**Retention and deletion:** retain audit trails and vendor dispute history;
delete transient prompts after retention; keep AP notes and approvals.

**Privacy/security:** AP data is financial and vendor-sensitive; enforce tenant
isolation, encryption, and audit trails.

**Analytics questions:** which vendors trigger the most exceptions and which
thresholds create the most false disputes?

## 9. Deployment Sequencing

**Pre-deploy checklist:** ERP scope confirmed, threshold policy set, AP owner
assigned.

**Staging:** test on historic invoice exceptions.

**Production sequence:** start with draft-only.

**Smoke test:** ingest, match, draft, approve, log.

**Rollback:** disable send, preserve audit.

**Observability:**

- Logs: invoice, match, draft, approval.
- Metrics: exception handling time, approval rate, supplier response speed.
- Alerts: ERP failure, send failure, threshold drift.
- Dashboards: exception backlog and turnaround.

## 10. Post-Launch Iteration Plan

**Metrics:** exception handling time, approval rate, supplier response speed.

**Week-by-week:**

- Week 1: tune thresholds.
- Week 2: improve match accuracy.
- Week 3: add one more vendor type.
- Week 4: measure AP time saved.

**Pivot signals:** too many false disputes or low AP trust should force
threshold tightening or scope reduction.

## Source Notes
- `runs/2026-06-26-agentic-opportunity-blueprints/source/Procurement_Competitor_Teardown.md` - AP/procurement incumbent map and exception-resolution wedge.
- `runs/2026-06-26-agentic-opportunity-blueprints/market-map-phase2.md` - procurement / dispute market-map backstop.
- Official reference points reviewed: Coupa, SAP Ariba, Oracle Procurement, Ivalua, and Workday product pages.
