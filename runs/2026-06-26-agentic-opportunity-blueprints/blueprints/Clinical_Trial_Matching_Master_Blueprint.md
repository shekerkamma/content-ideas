---
status: reviewed
use_case: "Clinical Trial Matching"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Clinical Trial Matching Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** clinical research operations and site recruiters.

**Later ICPs:** trial sponsors and adjacent research sites once one protocol
proves the matching loop.

**Pain wedge:** matching patients to trials is labor-intensive and criteria-
heavy.

**Incumbent weakness:** site workflows and registries do not do full evidence
mapping well.

**Agentic disruption thesis:** parse eligibility criteria, match patient
records, and explain the fit.

**Why now:** trials need enrollment speed and screened candidates are expensive
to source.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

The score is inferred from enrollment bottlenecks, high trial spend, and the
manual chart-review burden.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** research sites, coordinators, and sponsors.

**Current workaround:** manual chart review and eligibility spreadsheets.

**Switching reason:** faster screening and fewer missed matches.

**Payment signal:** site operations and recruitment budgets.

**30-day reachability:** one trial and one patient population can prove the
wedge.

**Verdict: PROCEED, but keep the scope to pre-screening.**

## 2. The 30-Day Scope Definition

**Project name:** Trial Match Copilot

**Validated problem:** patient records must be compared to complex protocol
criteria.

**Target user:** coordinator or site recruiter.

**Core hypothesis:** the agent can pre-screen records and explain eligibility
reasoning.

### In Scope

1. **Protocol ingest**
   - Acceptance criterion: inclusion / exclusion criteria are parsed.
2. **Patient pre-screening**
   - Acceptance criterion: patient records are matched against criteria.
3. **Explanation**
   - Acceptance criterion: the agent explains why a patient fits or does not
     fit.

### Explicitly Out Of Scope

- Full CTMS.
- Full EDC replacement.
- Site management platform.
- Autonomous enrollment decisions.

### Week-By-Week Milestones

- **Week 1:** ingest one trial protocol and define criteria.
- **Week 2:** build patient record parsing and scoring.
- **Week 3:** add explainability and reviewer workflow.
- **Week 4:** pilot with one site population.

**Dependencies:** protocol text, patient record access, and site reviewer.

**Acceptance test:** a patient record can be pre-screened and explained against
one protocol.

**Top risks:** PHI safety, ambiguous criteria, and protocol drift.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: coordinator review console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for protocols and records.
- Auth: HIPAA-ready SSO plus service credentials.
- Database: Postgres for protocols, patients, matches, explanations, and
  approvals.
- Observability: OpenTelemetry and audit logs.
- Hosting: cloud app with queue worker.

**Architecture:** protocol ingest -> criteria parse -> patient match ->
explanation -> reviewer workflow. The agent stays as a pre-screening layer.

**Critical design decisions:**

1. Do not build a CTMS or EDC.
2. Keep matching explainable.
3. Keep PHI handling strict and auditable.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/trials/ingest` | ingest protocol | protocol bundle | trial_id | service token | retry queue |
| POST | `/api/trials/match` | pre-screen patient | trial_id, patient_ref | match result | service token | fallback to review |
| POST | `/api/trials/explain` | explain decision | match_id | rationale | service token | return partial explanation |

### Folder / Module Structure

- `app/trials/`
- `app/api/trials/`
- `services/parse/`
- `services/match/`
- `workers/explain/`
- `lib/phi/`

### Environment Variables

- `PHI_ACCESS_TOKEN`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `EXPORT_BUCKET`
- `REVIEW_QUEUE_URL`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| CTMS / EDC | high | IQVIA / Medidata / Veeva own it | BUY | not the wedge |
| Trial matching | medium | manual review is the pain | BUILD | core wedge |
| Explainability | medium | coordinators need it | BUILD | high leverage |

**Bottom line:** buy the clinical system shell and build the matching layer.

## 5. MVP ROI Business Case

**Current-state cost model:** coordinator labor, screened-out patients, and
missed enrollment.

**Agentic MVP cost model:** protocol ingest, matching, review, and secure
storage.

**Pricing options:**

1. Per trial.
2. Per site.
3. Enterprise sponsor package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | weak patient population fit | 12-18 months | month 14+ | narrower |
| Base | fewer failed screeners | 6-9 months | month 8-12 | strong fit |
| Upside | faster enrollment speed | 3-5 months | month 4-6 | high leverage |

**Formulas**

```text
Monthly value =
  coordinator time saved + failed screening reduced + enrollment speed improved
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if PHI handling cannot be guaranteed, do not ship.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| IQVIA CTM | CTMS | massive scale | legacy complexity | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Clinical_Trial_Matching_Competitor_Teardown.md` |
| Medidata | clinical cloud | dominant platform | expensive rollout | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Clinical_Trial_Matching_Competitor_Teardown.md` |
| Veeva Vault | clinical data suite | regulatory depth | heavy deployment | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Clinical_Trial_Matching_Competitor_Teardown.md` |
| Antidote | patient matching | specialized matching | still criteria-heavy | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Clinical_Trial_Matching_Competitor_Teardown.md` |

**Direct threats:** IQVIA and Tempus AI.

**What not to build:** full CTMS or EDC systems.

**Agentic wedge:** unstructured criterion matching, micro-deployments, and
instant ROI from reduced screening waste.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| protocol parse | trial loaded | ingest runs | criteria extracted | fixture test |
| patient match | record loaded | match runs | fit score and reasons returned | replay test |
| explainability | match result | explanation requested | rationale is clear | reviewer test |

### Edge Cases

- Ambiguous criteria.
- Missing chart data.
- Conflicting patient history.
- PHI access issue.
- Duplicate patient records.
- Protocol amendment drift.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| protocols | trial docs | protocol store | sponsor / site | versioned | amendment tracking |
| patient records | EHR / chart | patient table | EHR | realtime | PHI controls |
| matches | agent | match table | agent | realtime | explanation required |
| reviews | coordinator | review table | coordinator | realtime | immutable log |

**Retention and deletion:** retain approved match history and rationale, delete
transient prompts after retention, and keep audit logs for reviewer actions.

**Privacy/security:** HIPAA controls, secure data handling, and no full CTMS
replacement.

**Analytics questions:** which criteria create the most false negatives and
which patient populations are most likely to match quickly?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one trial, one population, PHI review, rollback flag.

**Staging:** protocol ingest, then matching, then explanation.

**Production sequence:** one site, one protocol, one reviewer workflow.

**Smoke test:** one patient record produces a match explanation.

**Rollback:** disable matching and fall back to manual chart review.

**Observability:**

- Logs: protocol, patient, match, explanation.
- Metrics: match rate, screen failure reduction, reviewer acceptance.
- Alerts: PHI error, protocol drift, match failure.
- Dashboards: enrollment funnel and false-negative hotspots.

## 10. Post-Launch Iteration Plan

**Metrics:** screening time saved, failed screeners reduced, and enrollment
speed improved.

**Week-by-week:**

- Week 1: add more criteria normalization.
- Week 2: improve chart extraction.
- Week 3: tighten explanation quality.
- Week 4: package for adjacent trials.

**Pivot signals:** keep it site-local if deployment is too slow, narrow to
one trial if criteria drift is high, and stay pre-screen only if PHI risk
increases.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/Clinical_Trial_Matching_Competitor_Teardown.md` - trial-matching incumbent map and pre-screening wedge.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Clinical_Trial_Matching_Disruptive_Teardown.md` - upstream teardown dossier for the matching wedge.
- Official reference points reviewed for grounding: ClinicalTrials.gov, IQVIA, Medidata, Veeva Vault Clinical, Tempus, Antidote, and OpenClinica product and overview pages.
- The implementation stance stays narrow: pre-screening and eligibility explanation only, with CTMS / EDC left to incumbents.
