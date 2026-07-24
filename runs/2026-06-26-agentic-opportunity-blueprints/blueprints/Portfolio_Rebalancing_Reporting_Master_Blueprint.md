---
status: reviewed
use_case: "Portfolio Rebalancing Reporting"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: medium-high
  competitor: medium-high
  pricing: medium-high
  implementation: medium-high
---

# Portfolio Rebalancing Reporting Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** wealth advisor, CIO, or client reporting lead at an RIA or
wealth platform.

**Later ICPs:** advisor teams once one report cycle proves the narrative layer.

**Pain wedge:** quarterly performance letters are repetitive but still require
careful tone and figure accuracy.

**Incumbent weakness:** reporting tools produce charts; they do not write
advisor voice well.

**Agentic disruption thesis:** generate source-grounded client narratives from
portfolio data and approved market context.

**Why now:** clients expect more personalization, while advisors want less
manual report assembly.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 22/30**

The score is inferred from predictable quarter-end reporting and the repeated
manual effort to produce advisor-style narratives.

- Problem realness: 8/10
- Solution fit: 7/10
- Buying signal + reachability: 7/10

**Who has the problem:** advisors sending recurring portfolio letters.

**Current workaround:** mail-merge templates and manual commentary.

**Switching reason:** improve personalization without increasing advisor time.

**Payment signal:** reporting and wealth stack budgets already exist.

**30-day reachability:** medium-high at firms with recurring client letters.

**Verdict: PROCEED, but keep the system of record intact.**

## 2. The 30-Day Scope Definition

**Project name:** Advisor Voice Reporting Copilot

**Validated problem:** advisor commentary is slow to produce and hard to
personalize.

**Target user:** advisor or client reporting specialist.

**Core hypothesis:** the agent can turn portfolio facts and approved commentary
into a publishable draft faster than manual writing.

### In Scope

1. **Portfolio data ingest**
   - Acceptance criterion: portfolio snapshots and benchmark data are loaded.
2. **Advisor-voice draft generation**
   - Acceptance criterion: the report draft follows approved tone samples.
3. **Financial figure validation**
   - Acceptance criterion: the numbers reconcile before export.

### Explicitly Out Of Scope

- Trade execution.
- Portfolio management decisions.
- Unreviewed client send.
- Replacing the portfolio ledger.

### Week-By-Week Milestones

- **Week 1:** ingest data and tone samples.
- **Week 2:** generate narrative draft.
- **Week 3:** validate figures and approvals.
- **Week 4:** publish pilot reports.

**Dependencies:** portfolio feed, commentary source, advisor examples, and
compliance review.

**Acceptance test:** report draft matches numbers, follows tone, and requires
approval before send.

**Top risks:** bad numbers, tone drift, and compliance issues.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: Next.js advisor review UI.
- Backend: Python FastAPI.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + pgvector.
- Auth: SSO / RBAC.
- Database: Postgres for portfolios, drafts, approvals.
- Observability: reconciliation and review logs.
- Hosting: secure cloud or advisor environment.

**Architecture:** portfolio data -> narrative draft -> validation -> advisor
review -> export. The agent summarizes holdings, maps approved commentary, and
blocks export on mismatch.

**Critical design decisions:**

1. Reconcile numbers before narrative.
2. Keep review approval before send.
3. Use approved commentary samples to anchor tone.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/portfolios` | ingest holdings snapshot | portfolio payload | portfolio id | service auth | 400 on malformed payload |
| POST | `/api/portfolios/{id}/draft` | generate narrative | portfolio id | draft | service auth | partial with validation flags |
| POST | `/api/drafts/{id}/approve` | approve export | approval note | approved status | reviewer role | block on failed validation |

### Folder / Module Structure

- `app/(console)/wealth/`
- `app/api/portfolios/`
- `services/report-agent/`
- `lib/validation/`

### Environment Variables

- `DATABASE_URL`
- `MARKET_DATA_KEY`
- `PORTFOLIO_API_KEY`
- `MODEL_API_KEY`
- `EXPORT_BUCKET`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Portfolio accounting | high | existing wealth platforms own it | BUY | not the wedge |
| Narrative generation | medium | templates are manual | BUILD | core wedge |
| Validation / approval | medium | compliance requires it | BUILD | high leverage |

**Bottom line:** buy portfolio data access and build the narrative layer.

## 5. MVP ROI Business Case

**Current-state cost model:** analyst time, report assembly, and rework.

**Agentic MVP cost model:** data pull, draft generation, validation, review,
and storage.

**Pricing options:**

1. Pilot by advisor team.
2. Per report.
3. Enterprise reporting package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low report volume | 12-18 months | month 14+ | learning only |
| Base | less manual writing | 6-9 months | month 8-12 | solid fit |
| Upside | more recurring client letters | 3-5 months | month 4-6 | strong leverage |

**Formulas**

```text
Monthly value =
  writing time saved + validation reduced + report throughput improved
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if the data cannot be reconciled cleanly, do not export.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Envestnet Tamarac | wealth platform | broad advisor stack | all-in-one bloat | tiered AUM | `runs/2026-06-26-agentic-opportunity-blueprints/source/Portfolio_Rebalancing_Reporting_Competitor_Teardown.md` |
| Orion Advisor Tech | reporting | customizable reporting | clunky setup | AUM / per-account | `runs/2026-06-26-agentic-opportunity-blueprints/source/Portfolio_Rebalancing_Reporting_Competitor_Teardown.md` |
| SS&C Black Diamond | reporting | polished deliverables | manual templates | tiered | `runs/2026-06-26-agentic-opportunity-blueprints/source/Portfolio_Rebalancing_Reporting_Competitor_Teardown.md` |
| Addepar | portfolio data | deep aggregation | expensive and complex | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Portfolio_Rebalancing_Reporting_Competitor_Teardown.md` |

**Direct threats:** Orion Advisor Tech and Envestnet Tamarac.

**What not to build:** another complex portfolio accounting ledger.

**Agentic wedge:** replace charts with narrative, solve alts discrepancies, and
remove zero-click customization.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| draft numbers | portfolio data loaded | draft runs | numbers reconcile | validation test |
| advisor voice | tone samples loaded | draft runs | commentary matches style | reviewer diff |
| publish guard | validation fails | send requested | export blocked | negative test |

### Edge Cases

- Alternative assets.
- Missing benchmarks.
- Negative performance quarter.
- Duplicate account snapshots.
- Client-specific restrictions.
- Mismatched dates.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| portfolios | custody / platform | portfolio table | custodian | scheduled | checksum |
| drafts | agent | draft table | agent | realtime | tone and number checks |
| validations | rules engine | validation table | agent | realtime | fail closed |
| approvals | reviewer | approval table | reviewer | realtime | immutable |

**Retention and deletion:** retain approved reports and validations, delete
transient prompt state after retention, and keep review lineage.

**Privacy/security:** client data must be tenant-scoped, encrypted, and review
gated.

**Analytics questions:** which report types need the most edits and which
portfolios create the most validation failures?

## 9. Deployment Sequencing

**Pre-deploy checklist:** portfolio feed, commentary source, advisor examples,
compliance review, rollback flag.

**Staging:** ingest, then draft, then validate, then review.

**Production sequence:** one team, one report template, one approval path.

**Smoke test:** draft one report and confirm reconciliation.

**Rollback:** disable drafting and keep manual report assembly.

**Observability:**

- Logs: data pull, draft, validation, approval.
- Metrics: report cycle time, validation failures, edit rate.
- Alerts: number mismatch, tone drift, export failure.
- Dashboards: reporting throughput and edit hotspots.

## 10. Post-Launch Iteration Plan

**Metrics:** report cycle time, edit rate, and client-send approval rate.

**Week-by-week:**

- Week 1: add another portfolio source.
- Week 2: improve narrative quality.
- Week 3: tighten validation.
- Week 4: package for adjacent advisors.

**Pivot signals:** keep it advisory if validation failures persist, tighten
tone controls if edits spike, and limit to one report type if complexity grows.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Portfolio_Rebalancing_Reporting_Disruptive_Teardown.md` - upstream teardown dossier for the portfolio-reporting wedge.
- Official reference points reviewed: Addepar, BlackRock Aladdin, Orion, Envestnet, and Morningstar product pages.
- `runs/2026-06-26-agentic-opportunity-blueprints/source/Portfolio_Rebalancing_Reporting_Competitor_Teardown.md` - wealth-platform incumbent map and narrative-reporting wedge.
