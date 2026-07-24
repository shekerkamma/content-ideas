---
status: reviewed
use_case: "Commission Dispute Resolution"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Commission Dispute Resolution Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** sales ops and revops teams.

**Later ICPs:** finance ops and compensation admins once one comp plan proves
the reconciliation loop.

**Pain wedge:** month-end commission disputes waste weeks.

**Incumbent weakness:** comp systems are complex and require rule tuning plus
manual override handling.

**Agentic disruption thesis:** read the comp plan, reconcile CRM data, and
explain the result.

**Why now:** reps want clarity and revops wants less manual reconciliation.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 26/30**

The score is inferred from recurring comp disputes, heavy implementation fees,
and the clear Excel / admin burden.

- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 9/10

**Who has the problem:** companies with complex tiered compensation plans.

**Current workaround:** spreadsheets and manual adjustments.

**Switching reason:** faster dispute resolution and improved trust.

**Payment signal:** commission platforms and revops time.

**30-day reachability:** one comp plan and one sales pod can prove the wedge.

**Verdict: PROCEED, but keep the SPM intact.**

## 2. The 30-Day Scope Definition

**Project name:** Commission Copilot

**Validated problem:** disputes arise from mismatches between CRM and comp
plan.

**Target user:** RevOps analyst plus rep.

**Core hypothesis:** the agent can reconcile standard cases and route anomalies.

### In Scope

1. **Comp plan ingest**
   - Acceptance criterion: a commission PDF or rules document is indexed.
2. **Reconciliation**
   - Acceptance criterion: closed-won CRM data is matched against the plan.
3. **Explanation / dispute drafting**
   - Acceptance criterion: reps get a plain-language explanation and a dispute
     packet.

### Explicitly Out Of Scope

- Standalone SPM platform.
- Custom coding rule builder.
- Replacing the CRM.
- Automated payout execution without review.

### Week-By-Week Milestones

- **Week 1:** ingest one comp plan and one sales pod.
- **Week 2:** build reconciliation logic and CRM mapping.
- **Week 3:** draft explanations and dispute packets.
- **Week 4:** pilot with a monthly close cycle.

**Dependencies:** comp plan, CRM feed, and payout review owner.

**Acceptance test:** one disputed payout can be explained and routed for
review.

**Top risks:** plan complexity, data mismatch, and trust.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: commissions review console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for comp plans and CRM data.
- Auth: SSO plus CRM / commission-system service credentials.
- Database: Postgres for plans, payouts, disputes, and approvals.
- Observability: OpenTelemetry and payout audit logs.
- Hosting: cloud app with queue worker.

**Architecture:** comp plan -> CRM data -> reconcile -> explain -> dispute
packet -> review. The agent reads the policy, matches the data, and explains
the result.

**Critical design decisions:**

1. Do not build a standalone SPM platform.
2. Keep humans in the loop for disputes.
3. Make the explanation plain-language and auditable.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/comp/ingest` | ingest comp plan | plan document | plan id | service token | retry queue |
| POST | `/api/comp/reconcile` | reconcile payout | plan id, CRM data | payout result | service token | fallback to review |
| POST | `/api/comp/dispute` | draft dispute packet | payout id | dispute packet | service token | require approval |

### Folder / Module Structure

- `app/(console)/comp/`
- `app/api/comp/`
- `services/reconcile/`
- `services/explain/`
- `workers/dispute/`
- `lib/payouts/`

### Environment Variables

- `DATABASE_URL`
- `MODEL_ROUTER_API_KEY`
- `CRM_API_KEY`
- `COMP_PLAN_STORAGE_KEY`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| SPM platform | high | Xactly / Spiff already exist | BUY | not the wedge |
| Reconciliation | medium | Excel / admin burden is the pain | BUILD | core wedge |
| Explanation / dispute | medium | reps want clarity | BUILD | high leverage |

**Bottom line:** buy the SPM shell and build the dispute copilot.

## 5. MVP ROI Business Case

**Current-state cost model:** month-end analyst time, manual adjustments, and
rep trust loss.

**Agentic MVP cost model:** plan ingest, reconciliation, explanation,
approval, and model usage.

**Pricing options:**

1. Fixed pilot by sales pod.
2. Per dispute.
3. Enterprise comp package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low dispute volume | 12-18 months | month 14+ | learn only |
| Base | faster dispute resolution | 6-9 months | month 8-12 | strong fit |
| Upside | high dispute volume and trust lift | 3-5 months | month 4-6 | high leverage |

**Formulas**

```text
Monthly value =
  analyst time saved + dispute cycle reduced + trust improved
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if comp-plan logic cannot be represented clearly, do not
automate the explanation.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Xactly | SPM | enterprise breadth | heavy configuration | $40-$60+/user/mo | `runs/2026-06-26-agentic-opportunity-blueprints/source/Commission_Dispute_Resolution_Competitor_Teardown.md` |
| CaptivateIQ | commission platform | spreadsheet-like flexibility | implementation fees | $35-$55/user/mo | `runs/2026-06-26-agentic-opportunity-blueprints/source/Commission_Dispute_Resolution_Competitor_Teardown.md` |
| Spiff | commission platform | real-time visibility | admin burden | ~$75/user/mo | `runs/2026-06-26-agentic-opportunity-blueprints/source/Commission_Dispute_Resolution_Competitor_Teardown.md` |
| Varicent | SPM | complex comp handling | support heavy | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Commission_Dispute_Resolution_Competitor_Teardown.md` |

**Direct threats:** Xactly and Spiff.

**What not to build:** a standalone SPM platform.

**Agentic wedge:** bypass the implementation fee, answer rep payout questions,
and remove support-ticket churn.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| comp ingest | plan uploaded | ingest runs | plan indexed | parser test |
| reconciliation | CRM and plan data loaded | reconcile runs | payout differences explained | replay test |
| dispute | discrepancy found | draft runs | packet ready for review | approval test |

### Edge Cases

- Mid-cycle plan changes.
- Multi-currency comp.
- Split credit.
- Missing CRM close-won data.
- Duplicate records.
- Rep override request.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| comp plans | PDF / rules doc | plan table | comp team | versioned | approval state |
| CRM data | CRM | CRM snapshot | CRM | scheduled | field mapping |
| payouts | commission system | payout table | SPM | scheduled | hash / checksum |
| disputes | agent | dispute table | agent | per run | reviewer required |

**Retention and deletion:** retain comp-plan lineage, reconciliation reasons,
and dispute history; delete transient prompts after retention.

**Privacy/security:** payout data and CRM data are sensitive; enforce tenant
isolation, encryption, and role-based access.

**Analytics questions:** which plan clauses produce the most disputes and
which reps ask the most clarification questions?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one comp plan, CRM access, payout owner, rollback
flag.

**Staging:** historic payout replay.

**Production sequence:** shadow run -> explanation only -> dispute packets.

**Smoke test:** one dispute produces a clear explanation.

**Rollback:** disable reconciliation and keep manual review.

**Observability:**

- Logs: plan, CRM field, payout, explanation.
- Metrics: dispute cycle time, analyst time saved, rep acceptance.
- Alerts: CRM mapping failure, plan parse failure, trust drop.
- Dashboards: dispute volume and resolution time.

## 10. Post-Launch Iteration Plan

**Metrics:** dispute cycle time, rep acceptance, and analyst time saved.

**Week-by-week:**

- Week 1: add another compensation plan type.
- Week 2: improve CRM mapping.
- Week 3: tighten explanations.
- Week 4: package for more sales pods.

**Pivot signals:** narrow to explanation-only if trust is weak, and keep the
product away from custom coding if plan complexity grows.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/Commission_Dispute_Resolution_Competitor_Teardown.md` - SPM incumbent map and commission reconciliation wedge.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Commission_Dispute_Resolution_Disruptive_Teardown.md` - upstream teardown dossier for the commission-reconciliation wedge.
- Official reference points reviewed: Salesforce, Xactly, SAP Commissions, Oracle Incentive Compensation, and Spiff product pages.
