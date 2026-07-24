---
status: reviewed
use_case: "Loan Origination Underwriting"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Loan Origination Underwriting Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** mortgage operations and underwriting leaders.

**Later ICPs:** adjacent lender operations teams once one loan product proves
the document-to-decision loop.

**Pain wedge:** loan teams spend days extracting data from income and bank docs.

**Incumbent weakness:** LOS systems are monolithic and hard to customize.

**Agentic disruption thesis:** extract, normalize, calculate DTI / LTV, and
draft pre-approval support.

**Why now:** borrower speed matters, and manual processing still slows
approvals.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 28/30**

The score is inferred from high per-loan fees, universal UI complaints, and the
ongoing need for manual document review.

- Problem realness: 10/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** lenders and loan officers.

**Current workaround:** manual document review and calculator spreadsheets.

**Switching reason:** faster time-to-decision and lower origination cost.

**Payment signal:** LOS and underwriting operations.

**30-day reachability:** one borrower file and one loan product can prove the
wedge.

**Verdict: PROCEED, but keep the LOS intact.**

## 2. The 30-Day Scope Definition

**Project name:** Underwrite Copilot

**Validated problem:** loan applications need structured extraction and metric
calculation.

**Target user:** loan officer plus underwriter.

**Core hypothesis:** the agent can pre-fill structured data and recommend a
decision path.

### In Scope

1. **Document ingest**
   - Acceptance criterion: income, asset, and identity docs are loaded.
2. **Extraction and calculation**
   - Acceptance criterion: DTI, LTV, and other required metrics are computed.
3. **Decision packet**
   - Acceptance criterion: underwriter receives a review-ready packet.

### Explicitly Out Of Scope

- New core LOS.
- Autonomous loan approval.
- Secondary-market sale workflow.
- Replacing compliance controls.

### Week-By-Week Milestones

- **Week 1:** ingest docs and define product scope.
- **Week 2:** build extraction and DTI / LTV logic.
- **Week 3:** add decision packet and review queue.
- **Week 4:** pilot with one loan product.

**Dependencies:** borrower files, LOS mapping, compliance review, and underwriter
approval.

**Acceptance test:** the agent pre-fills data and drafts a review-ready packet
for one borrower file.

**Top risks:** OCR errors, incomplete files, and compliance mistakes.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: Next.js underwriting review UI.
- Backend: Python FastAPI.
- Agent orchestration: LangGraph / state machine.
- Retrieval/data layer: Postgres + object storage.
- Auth: SSO / RBAC.
- Database: Postgres for applications, documents, decisions.
- Observability: decision and audit logs.
- Hosting: secure cloud environment.

**Architecture:** borrower docs -> extract -> calculate -> packet -> review.
The agent extracts figures, calculates ratios, drafts support, and routes to
review.

**Critical design decisions:**

1. Human approval because lending is highly regulated.
2. Document-first review because not every file is structured.
3. Conservative calculations because compliance and accuracy matter.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/applications` | create application | borrower payload | application id | service auth | reject missing fields |
| POST | `/api/applications/{id}/analyze` | analyze docs | application id | underwriting packet | service auth | fail closed on missing docs |
| POST | `/api/applications/{id}/approve` | approve decision | reviewer note | approved status | reviewer role | block without review |

### Folder / Module Structure

- `app/(console)/underwriting/`
- `app/api/applications/`
- `services/underwrite/`
- `lib/calculation/`

### Environment Variables

- `DATABASE_URL`
- `MODEL_ROUTER_API_KEY`
- `LOS_API_KEY`
- `DOCUMENT_STORAGE_KEY`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Core LOS | High | existing systems own it | BUY | not the wedge |
| Document extraction | Medium | manual review persists | BUILD | core wedge |
| Decision packet | Medium | underwriter review required | BUILD | high leverage |

**Bottom line:** buy the LOS and build the intelligent underwriting layer.

## 5. MVP ROI Business Case

**Current-state cost model:** underwriting labor, processing delays, and
rework.

**Agentic MVP cost model:** OCR, extraction, calculation, review, and storage.

**Pricing options:**

1. Fixed pilot by loan team.
2. Per application.
3. Enterprise package by lender.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low volume, heavy manual review | 12+ months | 12+ | capability demo |
| Base | recurring borrower files | 4-8 months | 4-8 | good wedge |
| Upside | high-volume lender | 2-4 months | 2-4 | scale across products |

**Formulas**

```text
Monthly value =
  underwriting time saved + faster decisions + rework reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if loan files cannot be interpreted reliably, do not
auto-populate decision packets.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| ICE Mortgage Technology (Encompass) | LOS | system of record | Windows-95-era UX | per-loan / enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Loan_Origination_Underwriting_Competitor_Teardown.md` |
| Black Knight (Empower) | LOS | compliance trails | clunky workflows | per-loan / enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Loan_Origination_Underwriting_Competitor_Teardown.md` |
| Finastra | LOS | mortgage breadth | expensive and rigid | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Loan_Origination_Underwriting_Competitor_Teardown.md` |
| Blend | digital origination | borrower UX | still requires processing | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Loan_Origination_Underwriting_Competitor_Teardown.md` |

**Direct threats:** Encompass and Finastra.

**What not to build:** a new core LOS.

**Agentic wedge:** eradicate stare-and-compare, bypass the clunky UI, and
undercut the per-loan tax.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| DTI calc | income docs uploaded | analysis runs | DTI calculated | calculation test |
| LTV calc | asset and value docs | analysis runs | LTV calculated | calculation test |
| packet | review complete | approval requested | reviewer sees packet | approval log |

### Edge Cases

- Self-employed borrower.
- Incomplete tax return.
- Missing bank statement.
- Multiple income sources.
- Gift funds.
- Compliance hold.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| applications | LOS / portal | app table | lending system | API | required-field check |
| docs | uploads | object store | source docs | upload | hash / OCR confidence |
| calculations | agent | metrics table | agent | per run | audit tracked |
| decisions | reviewer | decision table | reviewer | per run | approval required |

**Retention and deletion:** encrypt and minimize PII, retain decision lineage,
and keep audit trails; do not train on borrower PII.

**Privacy/security:** role-based access, encryption, and compliance review gates.

**Analytics questions:** which loan types need the most manual review and
which document classes cause the most rework?

## 9. Deployment Sequencing

**Pre-deploy checklist:** borrower file set, compliance review, LOS mapping,
rollback flag.

**Staging:** test on sanitized applications.

**Production sequence:** start read-only and reviewer-facing.

**Smoke test:** ingest, extract, calculate, packet, approve.

**Rollback:** disable decisioning and keep review queue.

**Observability:**

- Logs: OCR confidence, calculation path, approval outcome.
- Metrics: time to decision, override rate, extraction accuracy.
- Alerts: OCR failures, compliance flags, LOS outages.
- Dashboards: underwriting latency and reviewer load.

## 10. Post-Launch Iteration Plan

**Metrics:** time to decision, override rate, and reviewer time saved.

**Week-by-week:**

- Week 1: fix document parsing.
- Week 2: tune DTI rules.
- Week 3: improve packet quality.
- Week 4: measure time saved.

**Pivot signals:** broaden only if compliance is stable and underwriter trust
stays high; otherwise keep the product as a packet-prep copilot.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/Loan_Origination_Underwriting_Competitor_Teardown.md` - LOS incumbent map and intelligent-underwriter wedge.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Loan_Origination_Underwriting_Disruptive_Teardown.md` - upstream teardown dossier for the loan-packet wedge.
- Official reference points reviewed: Encompass, Blend, nCino, and Byte product pages.
