---
status: reviewed
use_case: "Financial Report Reconciliation"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Financial Report Reconciliation Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** controller, accounting, and finance transformation leaders.

**Later ICPs:** finance ops teams once one close cycle proves the value of the
reconciliation layer.

**Pain wedge:** month-end reconciliation still depends on spreadsheet
comparisons and manual exception hunting.

**Incumbent weakness:** close suites and ERP modules still demand configuration
and structured inputs.

**Agentic disruption thesis:** reconcile semi-structured statements and reports
without forcing a system replacement.

**Why now:** close platforms are strong, but fuzzy matching and document
variability still create friction.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 26/30**

The score is inferred from close labor, ERP spend, and the recurring complaint
that manual tie-outs consume analyst time.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 8/10

**Who has the problem:** accounting teams closing books across ERP, bank, and
document sources.

**Current workaround:** spreadsheets, manual tie-outs, and exported CSVs.

**Switching reason:** faster close, fewer errors, and less analyst time on rote
comparison.

**Payment signal:** finance close software and ERP spend.

**30-day reachability:** one reconciliation type and one bank feed are enough to
prove value.

**Verdict: PROCEED, but keep the system of record intact.**

## 2. The 30-Day Scope Definition

**Project name:** Close Reconciliation Copilot

**Validated problem:** teams spend days comparing similar but not identical
records.

**Target user:** accountant or controller reviewer.

**Core hypothesis:** an agent can perform fuzzy matching, surface gaps, and
draft a reconciliation summary.

### In Scope

1. **Document ingest**
   - Acceptance criterion: bank statements and source docs are parsed.
2. **Fuzzy matching**
   - Acceptance criterion: likely ledger / bank matches are proposed with a
     confidence score.
3. **Review summary**
   - Acceptance criterion: reviewer gets an exception report and signoff path.

### Explicitly Out Of Scope

- ERP replacement.
- Journal posting automation.
- Full accounting platform.
- Ownership of the accounting system of record.

### Week-By-Week Milestones

- **Week 1:** connect one forecast source.
- **Week 2:** add source-document ingest and parsing.
- **Week 3:** introduce fuzzy matching and exception scoring.
- **Week 4:** add reviewer signoff and reconciliation summary.

**Dependencies:** ledger export, bank feed, OCR / parsing, and approval path.

**Acceptance test:** a close reviewer can use the output to complete a single
reconciliation without manually redoing the search.

**Top risks:** source quality, OCR failure, and false matches.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: finance review console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for statements and notes.
- Auth: SSO plus finance-system service credentials.
- Database: Postgres for close periods, source docs, matches, and approvals.
- Observability: OpenTelemetry and close-cycle metrics.
- Hosting: cloud app with queue worker.

**Architecture:** document ingest -> OCR / parse -> fuzzy match -> exception
report -> reviewer signoff -> close summary. The agent surfaces likely pairs,
exposes reasons, and preserves auditability.

**Critical design decisions:**

1. Keep the ERP as system of record.
2. Make match reasons visible and auditable.
3. Use human signoff for the final close packet.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/close-periods/{id}/ingest` | ingest docs | files, source metadata | parse status | user auth | 422 on unreadable docs |
| POST | `/api/close-periods/{id}/match` | run fuzzy match | close_period_id | match candidates | service token | fallback to review |
| POST | `/api/close-periods/{id}/approve` | approve final report | period_id, approval | signed summary | reviewer token | reject invalid state |

### Folder / Module Structure

- `app/finance/`
- `app/api/close-periods/`
- `services/ocr/`
- `services/match/`
- `workers/close/`
- `lib/recon/`

### Environment Variables

- `ERP_TOKEN`
- `BANK_FEED_TOKEN`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `EXPORT_BUCKET`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Close suite | high | BlackLine / FloQast already exist | BUY | not the wedge |
| Matching engine | medium | manual today | BUILD | core wedge |
| Summary / signoff | medium | finance teams still need it | BUILD | high leverage |

**Bottom line:** buy the close suite where needed and build the reconciliation
layer.

## 5. MVP ROI Business Case

**Current-state cost model:** analyst time, close delays, and exception churn.

**Agentic MVP cost model:** OCR / parsing, model usage, reviewer labor, and
storage.

**Pricing options:**

1. Low-risk pilot.
2. Usage / outcome model per matched line or close period.
3. Enterprise package with controls and signoff.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low volume, poor source quality | 12-18 months | month 14+ | limited repeatability |
| Base | 2-day close reduction | 6-10 months | month 8-12 | moderate scope |
| Upside | multi-account adoption | 3-6 months | month 4-6 | repeated monthly value |

**Formulas**

```text
Monthly value =
  analyst time saved + close delay reduced + exception handling reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if ledger and bank data cannot be exported reliably, the
product becomes a file-cleanup tool.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| BlackLine | financial close | deep close footprint | heavy implementation | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Financial_Report_Reconciliation_Disruptive_Teardown.md` |
| FloQast | accounting platform | AI and close workflow | platform rollout | sales-led | `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Financial_Report_Reconciliation_Disruptive_Teardown.md` |
| ERP native recon | ERP module | already in SoR | rigid rules | bundled | `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Financial_Report_Reconciliation_Disruptive_Teardown.md` |

**Direct threats:** BlackLine and FloQast.

**What not to build:** an ERP replacement or a full accounting platform.

**Agentic wedge:** fuzzy matching, exception surfacing, and reviewer-ready
summaries with source provenance.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| fuzzy match | bank and ledger rows | engine runs | likely pairs are proposed | historical replay |
| exception report | unmatched rows | report generated | items are visible with reasons | QA checklist |
| re-upload | unreadable doc | upload fails | user sees precise error | input validation test |

### Edge Cases

- No statements loaded.
- OCR fails.
- Malformed CSV rejected.
- Bank file delayed.
- Duplicate runs do not overwrite signoff.
- Tenant-owned data only.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| ledger data | ERP | close tables | ERP | scheduled | checksum on export |
| bank data | bank statement | object store | bank | scheduled / upload | document integrity |
| matches | reconciliation engine | match table | engine | realtime | score thresholds |
| reports | reviewer | report table | reviewer | realtime | signoff required |

**Retention and deletion:** retain source docs, match reasons, and signed
reports; delete transient OCR artifacts after the retention window; keep close
history and signoff trail.

**Privacy/security:** encrypted financial documents, strict tenant isolation,
and signoff-only access for final reports.

**Analytics questions:** which accounts generate the most manual exceptions and
which source types produce the most false matches?

## 9. Deployment Sequencing

**Pre-deploy checklist:** source exports verified, OCR configured, signoff path
tested.

**Staging:** historical close replay.

**Production sequence:** shadow run -> reviewer approval -> live close assist.

**Smoke test:** one statement pair produces match candidates.

**Rollback:** disable match suggestions and fall back to manual process.

**Observability:**

- Logs: document hash, match reason, exception cause.
- Metrics: match rate, exception count, close-time reduction.
- Alerts: parse failure, threshold drift, signoff blocking.
- Dashboards: close-period status.

## 10. Post-Launch Iteration Plan

**Metrics:** activation, repeat close use, days saved, and audit effort reduced.

**Week-by-week:**

- Week 1: add a second account class.
- Week 2: add statement email ingestion.
- Week 3: improve fuzzy entity normalization.
- Week 4: package for controllers.

**Pivot signals:** focus on parsing only if exports are inconsistent, tighten
thresholds if review load remains high, and keep the product as close
assistance rather than automation if volume is low.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Financial_Report_Reconciliation_Disruptive_Teardown.md` - close-suite incumbent map and reconciliation wedge.
- BlackLine homepage - https://www.blackline.com/ - accessed 2026-06-26 - close and reconciliation platform positioning.
- FloQast homepage - https://www.floqast.com/ - accessed 2026-06-26 - automated reconciliations and record-to-report positioning.
- FloQast Pricing - https://www.floqast.com/ - accessed 2026-06-26 - pricing is sales-led from the product site.
- Oracle NetSuite - https://www.oracle.com/netsuite/ - accessed 2026-06-26 - ERP and account-reconciliation backdrop.
- SAP Account Reconciliation - https://www.sap.com/products/financial-management/account-reconciliation.html - accessed 2026-06-26 - ERP-native reconciliation and close workflow backdrop.
- Reconciliation platforms continue to emphasize workflows, templates, and platform rollout, so the wedge remains the messy-input reconciliation pack rather than a replacement close suite.
