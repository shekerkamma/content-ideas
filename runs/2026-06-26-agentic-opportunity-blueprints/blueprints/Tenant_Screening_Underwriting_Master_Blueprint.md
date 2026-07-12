---
status: reviewed
use_case: "Tenant Screening & Underwriting"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: medium-high
  competitor: medium-high
  pricing: medium-high
  implementation: medium-high
---

# Tenant Screening & Underwriting Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** property manager, leasing ops leader, or portfolio owner.

**Later ICPs:** multi-property operators once one screening flow proves the
packet workflow.

**Pain wedge:** income verification and fraud review are slow and document-
heavy.

**Incumbent weakness:** screening tools catch some fraud, but teams still
manually review edge cases.

**Agentic disruption thesis:** ingest applicant docs, verify income, detect
tampering, and package a recommendation.

**Why now:** leasing teams need speed, but they still require fair, auditable
controls.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 24/30**

The score is inferred from recurring screening volume, document overload, and
the manual burden of edge cases.

- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 7/10

**Who has the problem:** leasing and property operations teams.

**Current workaround:** manual paystub and bank statement review.

**Switching reason:** reduce decision time and fraud risk.

**Payment signal:** screening and leasing software budgets exist.

**30-day reachability:** high in multi-unit operators.

**Verdict: PROCEED, but keep human approval in the loop.**

## 2. The 30-Day Scope Definition

**Project name:** Lease Underwriting Copilot

**Validated problem:** tenant screening is slow, manual, and error-prone.

**Target user:** leasing agent or property manager.

**Core hypothesis:** a document-aware agent can verify income and flag fraud
faster than manual review.

### In Scope

1. **Applicant doc ingest**
   - Acceptance criterion: paystubs, bank statements, and IDs are uploaded.
2. **OCR and income extraction**
   - Acceptance criterion: gross / net income and key dates are extracted.
3. **Tamper / fraud checks**
   - Acceptance criterion: suspicious edits or inconsistencies are flagged.

### Explicitly Out Of Scope

- Autonomous lease approval.
- Eviction workflow.
- Fair-housing decisioning without human review.
- Replacing screening data vendors.

### Week-By-Week Milestones

- **Week 1:** ingest docs and build OCR flow.
- **Week 2:** income and DTI logic.
- **Week 3:** tamper detection and review queue.
- **Week 4:** pilot on one property or portfolio segment.

**Dependencies:** application docs, rent rules, reviewer owner, and fair-
housing review.

**Acceptance test:** gross / net income is extracted, fraud is flagged, and a
reviewer can approve or override.

**Top risks:** fraud false negatives, bias concerns, and bad documents.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: Next.js application review UI.
- Backend: Python FastAPI.
- Agent orchestration: LangGraph / state machine.
- Retrieval/data layer: Postgres + object storage.
- Auth: SSO / RBAC.
- Database: Postgres for applications, documents, decisions.
- Observability: decision and audit logs.
- Hosting: secure cloud environment.

**Architecture:** applicant docs -> extract -> analyze -> packet -> review.
The agent extracts figures, validates docs, flags anomalies, and drafts a
decision packet.

**Critical design decisions:**

1. Human approval because housing decisions are sensitive.
2. Document-first review because not every applicant will connect bank data.
3. Conservative fraud flags because false negatives matter.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/applications` | create application | applicant payload | application id | service auth | reject missing fields |
| POST | `/api/applications/{id}/analyze` | analyze docs | application id | income / fraud packet | service auth | fail closed on missing docs |
| POST | `/api/applications/{id}/approve` | approve decision | reviewer note | approved status | reviewer role | block without review |

### Folder / Module Structure

- `app/(console)/screening/`
- `app/api/applications/`
- `services/underwrite/`
- `lib/fraud/`

### Environment Variables

- `DATABASE_URL`
- `MODEL_ROUTER_API_KEY`
- `PLAID_API_KEY`
- `SCREENING_VENDOR_KEY`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Fraud / document review | Medium | screening tools charge per scan | BUILD | combine fraud, income, and packeting |
| Screening data | High | vendor data already exists | BUY | do not recreate ID / verification data |
| Lease decision | High | manual review is default | HYBRID | keep humans in loop |

**Bottom line:** buy screening data, build the underwriting packet.

## 5. MVP ROI Business Case

**Current-state cost model:** screening tools, leasing review time, manual
follow-up, and fraud / approval errors.

**Agentic MVP cost model:** OCR, analysis, packet generation, and storage.

**Pricing options:**

1. Fixed pilot by property.
2. Per application.
3. Enterprise package by portfolio.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low volume, heavy manual review | 12+ months | 12+ | capability demo |
| Base | recurring applications | 4-8 months | 4-8 | good mid-market wedge |
| Upside | high-volume portfolio | 2-4 months | 2-4 | scale across communities |

**Formulas**

```text
Monthly value =
  leasing time saved + faster decisions + manual follow-up reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if fair-housing review or data quality blocks approval,
stop.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Snappt | fraud screening | known category leader | scan-fee model | per-scan | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_36_Competitor_Teardown.md` |
| Plaid | bank connection | direct bank data | not a full underwriting workflow | platform pricing | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_36_Competitor_Teardown.md` |
| Manual review | labor | flexible | slow and inconsistent | labor cost | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_36_Competitor_Teardown.md` |

**Direct threats:** Snappt and manual review.

**What not to build:** lease signing or eviction workflow.

**Agentic wedge:** combine fraud, income, and affordability into one packet.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| OCR | paystub uploaded | analysis runs | income fields extracted | extraction report |
| fraud flag | tampered doc | analysis runs | tampering is flagged | fraud report |
| packet | review complete | approval requested | reviewer sees recommendation | approval log |

### Edge Cases

- Gig-worker income.
- Unsupported doc format.
- Missing bank link.
- Duplicate applicant.
- Fair-housing review.
- Inconsistent dates.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| applications | portal / CRM | app table | leasing system | API | required-field check |
| docs | uploads | object store | source docs | upload | hash / OCR confidence |
| income | agent | metrics table | agent | per run | manual review fallback |
| decisions | agent / reviewer | decision table | reviewer | per run | approval required |

**Retention and deletion:** encrypt and minimize PII, retain decision lineage,
and keep audit trails; do not use PII for model training.

**Privacy/security:** RBAC, retention controls, and fair-housing review gates.

**Analytics questions:** which doc types trigger the most manual review and
which properties have the most override volume?

## 9. Deployment Sequencing

**Pre-deploy checklist:** fair-housing review, doc set, reviewer owner, rollback
flag.

**Staging:** test on sanitized applications.

**Production sequence:** start read-only and reviewer-facing.

**Smoke test:** ingest, OCR, flag, recommend, approve.

**Rollback:** disable decisioning and keep the review queue.

**Observability:**

- Logs: OCR confidence, decision path, approval outcome.
- Metrics: time to decision, fraud catches, override rate.
- Alerts: OCR failures, bias concern spikes, vendor outages.
- Dashboards: screening latency and reviewer load.

## 10. Post-Launch Iteration Plan

**Metrics:** time to decision, fraud catches, override rate, and reviewer
time saved.

**Week-by-week:**

- Week 1: fix document parsing.
- Week 2: tune DTI rules.
- Week 3: improve fraud detection.
- Week 4: measure time saved.

**Pivot signals:** stop if bias risk or low property-manager trust appears;
otherwise expand to more document types and more portfolio segments.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_36_Competitor_Teardown.md` - screening incumbent map and income/fraud packet wedge.
- Snappt - https://www.snappt.com/ - accessed 2026-06-26 - screening incumbent.
- RealPage Resident Screening - https://www.realpage.com/ - accessed 2026-06-26 - incumbent screening platform.
- AppFolio Property Management - https://www.appfolio.com/ - accessed 2026-06-26 - property management and resident onboarding incumbent.
- Plaid - https://plaid.com/ - accessed 2026-06-26 - bank verification reference.
- TransUnion - https://www.transunion.com/ - accessed 2026-06-26 - credit and identity data reference.
- Fair Housing Act - https://www.hud.gov/program_offices/fair_housing_equal_opp/fair_housing_act_overview - accessed 2026-06-26 - compliance context.
- FCRA - https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act - accessed 2026-06-26 - screening context.
