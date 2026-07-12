---
status: reviewed
use_case: "Claim Denial Management"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Claim Denial Management Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** revenue-cycle, billing, and claims leaders at providers and
RCM teams.

**Later ICPs:** adjacent billing teams once one denial class proves the appeal
workflow.

**Pain wedge:** denials still require manual cross-referencing, chart review,
and appeal drafting.

**Incumbent weakness:** RCM tools show status, but humans still do the work.

**Agentic disruption thesis:** draft cited appeals and cross-reference payer
policy automatically while preserving human signoff.

**Why now:** denial volume stays high, and existing tools still center on
reporting rather than execution.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

The score is inferred from RCM spend, denial labor, and the obvious execution
gap between status dashboards and actual appeal work.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** billing teams and coders working denied claims.

**Current workaround:** manual review and appeal letter drafting.

**Switching reason:** faster appeal cycles and fewer missed overturn chances.

**Payment signal:** enterprise RCM contracts and collections spend.

**30-day reachability:** one denial class and one payer policy set are enough to
prove value.

**Verdict: PROCEED, but keep chart access read-appropriate.**

## 2. The 30-Day Scope Definition

**Project name:** Denial Appeal Copilot

**Validated problem:** teams must manually draft appeals after a denial hits.

**Target user:** medical billing specialist or coder.

**Core hypothesis:** the agent can draft cited appeals and keep reviewers in the
loop.

### In Scope

1. **Denial ingest**
   - Acceptance criterion: 835 / 837 denial and payer context are loaded.
2. **Policy cross-reference**
   - Acceptance criterion: relevant payer policy is surfaced and cited.
3. **Appeal drafting**
   - Acceptance criterion: a complete appeal letter is drafted for review.

### Explicitly Out Of Scope

- Clearinghouse replacement.
- Full billing dashboard.
- Clinical decision engine.
- Autonomous submission without review.

### Week-By-Week Milestones

- **Week 1:** connect one denial class.
- **Week 2:** load payer policy documents.
- **Week 3:** draft cited appeals.
- **Week 4:** add reviewer workflow and outcome logging.

**Dependencies:** EDI feed, EMR/chart access, payer policies, and reviewer
approval.

**Acceptance test:** one denial produces a cited appeal packet.

**Top risks:** sparse chart data, policy drift, and PHI controls.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: billing review console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for payer policy and evidence.
- Auth: SSO plus billing-system service credentials.
- Database: Postgres for denials, policies, evidence, appeals, and approvals.
- Observability: OpenTelemetry and audit logs.
- Hosting: cloud app with queue worker.

**Architecture:** denial parse -> policy lookup -> evidence gather -> appeal
draft -> reviewer signoff -> submission / logging. The agent cites policy and
chart evidence explicitly.

**Critical design decisions:**

1. Keep the billing system and clearinghouse intact.
2. Use source citations for every appeal.
3. Retain human review before submission.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/denials/ingest` | ingest denial payload | EDI event | denial_id | service token | retry queue |
| POST | `/api/denials/draft` | draft appeal | denial_id | appeal draft | service token | fallback to review |
| POST | `/api/denials/approve` | approve appeal | denial_id, reviewer state | approved appeal | reviewer token | reject invalid state |

### Folder / Module Structure

- `app/revenue-cycle/`
- `app/api/denials/`
- `services/parse/`
- `services/policy/`
- `workers/appeals/`
- `lib/evidence/`

### Environment Variables

- `EDI_TOKEN`
- `EMR_TOKEN`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `EXPORT_BUCKET`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Clearinghouse / RCM | high | Waystar / Change Healthcare already exist | BUY | not the wedge |
| Appeal drafting | medium | humans still do it | BUILD | core wedge |
| Policy lookup | medium | changing payer docs are the pain | BUILD | high leverage |

**Bottom line:** buy the status/reporting shell and build the appeal engine.

## 5. MVP ROI Business Case

**Current-state cost model:** coder labor, appeal drafting time, and delayed
turnaround.

**Agentic MVP cost model:** EDI parsing, policy lookup, model usage, and review
labor.

**Pricing options:**

1. Low-risk pilot.
2. Usage / outcome model per drafted appeal.
3. Enterprise package with analytics.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | missing docs | 12-18 months | month 14+ | needs workflow access |
| Base | 50% drafting time reduction | 6-10 months | month 8-12 | moderate |
| Upside | strong overturn lift | 3-6 months | month 4-6 | strong citations |

**Formulas**

```text
Monthly value =
  drafting time saved + overturn improvement + turnaround reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if chart access is too sparse, appeal drafting becomes
guesswork.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Waystar | clearinghouse | claim rails | brittle workflows | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Claim_Denial_Management_Competitor_Teardown.md` |
| Change Healthcare | clearinghouse | broad integration | complex setup | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Claim_Denial_Management_Competitor_Teardown.md` |
| Epic Resolute | EHR billing | system access | boilerplate templates | bundled | `runs/2026-06-26-agentic-opportunity-blueprints/source/Claim_Denial_Management_Competitor_Teardown.md` |

**Direct threats:** clearinghouses and EHR billing modules.

**What not to build:** clearinghouse replacement, clinical decision engine, or
portal submission in v1.

**Agentic wedge:** autonomous drafting, automated policy cross-reference, and
zero-dashboard workflows.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| denial parse | 835 file | parse runs | denial fields extracted | fixture test |
| cited appeal | chart and policy | draft runs | citations included | replay test |
| missing docs | no evidence | draft runs | route to clinical team | negative test |

### Edge Cases

- No policy available.
- Malformed EDI rejected.
- Unsupported denial code.
- Appeal marked pending.
- Duplicate denial idempotent.
- PHI access restricted.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| denials | EDI | denial table | billing system | realtime | EDI validation |
| policies | payer docs | policy table | payer | versioned | citation required |
| evidence | EMR | evidence table | EMR | realtime | hash + source URI |
| appeals | agent | appeal table | agent | realtime | reviewer signoff |

**Retention and deletion:** retain appeal logs, citations, and review state;
delete transient prompts after retention; keep denial and appeal lineage.

**Privacy/security:** HIPAA controls, no model training on PHI, and restricted
access by role.

**Analytics questions:** which denial codes produce the highest overturn rate
when cited properly?

## 9. Deployment Sequencing

**Pre-deploy checklist:** EDI parser tested, payer policies loaded, reviewer UI
approved.

**Staging:** parallel run on historical denials.

**Production sequence:** shadow -> draft-only -> reviewer-assisted.

**Smoke test:** one denial generates a cited appeal.

**Rollback:** disable drafting and revert to manual appeal templates.

**Observability:**

- Logs: denial, policy, evidence, appeal.
- Metrics: draft time, overturn rate, reviewer acceptance.
- Alerts: policy sync failure, PHI error, EDI parse failure.
- Dashboards: denial types and turnaround.

## 10. Post-Launch Iteration Plan

**Metrics:** denied claims processed, repeat use, and appeal turnaround reduced.

**Week-by-week:**

- Week 1: add more denial codes.
- Week 2: improve citation quality.
- Week 3: add submission automation later.
- Week 4: package for payers and clinics.

**Pivot signals:** keep it as a draft assistant if charts are incomplete,
tighten source rules if citations are weak, and stop at review mode if portal
submission is blocked.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/Claim_Denial_Management_Competitor_Teardown.md` - RCM incumbent map and appeal drafting wedge.
- Waystar - https://www.waystar.com/ - accessed 2026-06-26 - clearinghouse backdrop.
- Waystar Denial Recovery - https://www.waystar.com/ - accessed 2026-06-26 - denial management and appeal workflow backdrop.
- athenahealth - https://www.athenahealth.com/ - accessed 2026-06-26 - ambulatory RCM and billing backdrop.
- Epic - https://www.epic.com/ - accessed 2026-06-26 - EHR billing and Resolute backdrop.
- Epic Resolute - https://www.epic.com/ - accessed 2026-06-26 - billing backdrop.
- AWS GovCloud - https://aws.amazon.com/govcloud-us/ - accessed 2026-06-26 - compliance backdrop.
