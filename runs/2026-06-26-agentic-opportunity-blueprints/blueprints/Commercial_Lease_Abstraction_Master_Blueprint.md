---
status: reviewed
use_case: "Commercial Lease Abstraction"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Commercial Lease Abstraction Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** CRE ops, legal ops, and property-management teams that need
fast lease abstraction without a full system rebuild.

**Later ICPs:** adjacent lease-admin and portfolio teams once one property
system proves the abstraction layer.

**Pain wedge:** leases are long, dense, and full of dates and financial terms
that need extraction.

**Incumbent weakness:** Yardi, MRI Software, and Visual Lease remain hard to
rip out, but they still depend on manual data entry and careful verification.

**Agentic disruption thesis:** read the lease, extract the key terms, and push
them to the property system.

**Why now:** portfolio teams need faster turn time on new lease intake.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

The score is inferred from lease-intake labor, custom enterprise pricing, and
the obvious pain of garbage-in / garbage-out abstraction work.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** property managers and lease admins.

**Current workaround:** manual reading and spreadsheet entry.

**Switching reason:** faster abstraction and fewer entry errors.

**Payment signal:** lease abstraction services and PropTech software.

**30-day reachability:** one lease type and one property system are enough to
prove the wedge.

**Verdict: PROCEED, but keep the scope to abstraction.**

## 2. The 30-Day Scope Definition

**Project name:** Lease Term Copilot

**Validated problem:** teams need a fast abstraction of financial and date
terms.

**Target user:** lease administrator with legal review.

**Core hypothesis:** the agent can extract 50+ fields and produce a validation
queue.

### In Scope

1. **Lease ingestion**
   - Acceptance criterion: PDF lease uploaded and indexed.
2. **Field extraction**
   - Acceptance criterion: 50+ key terms extracted with citations.
3. **Validation queue**
   - Acceptance criterion: legal / ops reviewer approves or corrects fields.

### Explicitly Out Of Scope

- Building a new lease database.
- Property management accounting.
- Tenant-facing workflows.
- Automated legal interpretation without review.

### Week-By-Week Milestones

- **Week 1:** ingest sample leases and define target fields.
- **Week 2:** build extraction and clause mapping.
- **Week 3:** add validation queue and export.
- **Week 4:** pilot one lease type with one property system.

**Dependencies:** lease files, property-system mapping, and reviewer approval.

**Acceptance test:** a lease can be abstracted into the property system with
source citations and minimal rework.

**Top risks:** clause ambiguity, bad OCR, and legal liability.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: lease review console.
- Backend: FastAPI service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for lease clauses and terms.
- Auth: SSO plus property-system service credentials.
- Database: Postgres for leases, fields, validations, and approvals.
- Observability: OpenTelemetry and audit logs.
- Hosting: cloud app with queue worker.

**Architecture:** lease PDF -> OCR / parse -> clause extraction -> field map ->
validation queue -> property-system push. The agent keeps provenance on each
term.

**Critical design decisions:**

1. Keep the property system as system of record.
2. Separate extraction from legal validation.
3. Preserve source citations for every extracted term.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/leases/ingest` | ingest lease file | pdf | lease_id | service token | retry queue |
| POST | `/api/leases/extract` | extract fields | lease_id | fields | service token | fallback review |
| POST | `/api/leases/publish` | publish validated terms | lease_id, approvals | publish result | service token | stop on validation miss |

### Folder / Module Structure

- `app/leases/`
- `app/api/leases/`
- `services/ocr/`
- `services/extract/`
- `workers/publish/`
- `lib/terms/`

### Environment Variables

- `LEASE_SOURCE_TOKEN`
- `PROPERTY_API_KEY`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `EXPORT_BUCKET`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Lease system of record | high | Yardi / MRI already own it | BUY | not the wedge |
| Abstraction extraction | medium | humans still read the lease | BUILD | core wedge |
| Validation queue | medium | needed for liability control | BUILD | keep humans in loop |

**Bottom line:** buy the portfolio system, build the abstraction layer.

## 5. MVP ROI Business Case

**Current-state cost model:** abstraction labor, legal review, rework, and
launch delays.

**Agentic MVP cost model:** OCR / parsing, model usage, validation labor, and
audit storage.

**Pricing options:**

1. Per lease.
2. Per document bundle.
3. Enterprise portfolio package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | small portfolio, sparse leases | 12-18 months | month 14+ | narrow fit |
| Base | 30-50% time reduction on abstraction | 6-9 months | month 8-12 | solid fit |
| Upside | high-volume intake and repeatable templates | 3-5 months | month 4-6 | strong leverage |

**Formulas**

```text
Monthly value =
  abstraction labor saved + legal review reduced + launch delay avoided
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if the buyer expects the agent to replace legal review,
do not proceed.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Yardi | property suite | core system of record | heavy UI / enterprise friction | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_36_Competitor_Teardown.md` |
| MRI Software | contract intelligence | compliance depth | manual data migration | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_36_Competitor_Teardown.md` |
| Visual Lease | lease admin | specialized workflow | enterprise quoting and manual oversight | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_36_Competitor_Teardown.md` |

**Direct threats:** Yardi and MRI Software.

**What not to build:** a new lease database or property management system.

**Agentic wedge:** zero-touch abstraction, transparent per-document pricing, and
API injection into the existing property system.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Lease ingest | PDF arrives | system parses it | lease indexed | parser test |
| Field extraction | lease loaded | extraction runs | term fields populated | fixture comparison |
| Publish | reviewer approves | publish runs | property system updated | integration test |

### Edge Cases

- Amortized TI clauses.
- Reimbursement structures.
- Missing exhibits.
- OCR errors.
- Conflicting amendment dates.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| leases | PDF / scans | lease store | source doc | realtime | OCR confidence |
| extracted fields | model output | field table | extraction service | realtime | citation requirement |
| validations | reviewer input | validation table | reviewer | realtime | approval state |
| property push | property API | publish log | property system | realtime | idempotency |

**Retention and deletion:** retain approved extractions and citations, keep
audit history for publish events, and expire raw drafts by policy.

**Privacy/security:** least-privilege property access and tenant isolation.

**Analytics questions:** which clause types create the most validation edits and
which property systems create the most push failures?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one lease type, one property system, validation owner,
rollback flag.

**Staging:** extraction-only, then validation, then publish.

**Production sequence:** one lease class, one property workflow, one approver.

**Smoke test:** abstract one lease and verify the exported terms.

**Rollback:** disable publish and keep manual abstraction only.

**Observability:**

- Logs: lease id, clause, field, confidence, publish state.
- Metrics: extraction coverage, rework rate, publish success.
- Alerts: OCR failure, validation backlog, publish error.
- Dashboards: field-edit hotspots and system push reliability.

## 10. Post-Launch Iteration Plan

**Metrics:** abstraction time, field accuracy, validation time, and time to
portfolio intake.

**Week-by-week:**

- Week 1: expand field list.
- Week 2: improve clause mapping.
- Week 3: tighten validation.
- Week 4: package for adjacent lease types.

**Pivot signals:** add more clause templates if legal review dominates, narrow
to one lease type if extraction quality drops, and keep to API injection rather
than UI replacement.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_36_Competitor_Teardown.md` - Yardi / MRI / Visual Lease incumbent map and abstraction pricing wedge.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Commercial_Lease_Abstraction_Disruptive_Teardown.md` - incumbent map and zero-touch abstraction wedge.
- Yardi - https://www.yardi.com/ - accessed 2026-06-26 - property management and lease workflow backdrop.
- MRI Software - https://www.mrisoftware.com/ - accessed 2026-06-26 - lease accounting and property workflow backdrop.
- Visual Lease - https://www.visuallease.com/ - accessed 2026-06-26 - lease admin backdrop.
- The wedge is abstraction and validation, not a new lease database or property-management system.
- Keeping the property system as the system of record is what makes the assistant sellable.
- The buyer gets faster lease intake and fewer legal/ops edits without rebuilding the property stack.
- That is the commercial case: extract terms once, verify them, and push them into the existing workflow.
