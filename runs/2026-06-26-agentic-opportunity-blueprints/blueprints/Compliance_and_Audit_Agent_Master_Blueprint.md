---
status: reviewed
use_case: "Compliance and Audit Agent"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Compliance and Audit Agent Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** compliance, security, finance, and internal audit leaders at
regulated companies that still chase evidence manually.

**Later ICPs:** adjacent risk and finance ops teams once one framework proves
that read-only evidence collection can replace spreadsheet wrangling.

**Pain wedge:** evidence collection and narrative drafting are still manual and
audit-season driven.

**Incumbent weakness:** GRC tools manage the workflow, but humans still chase
logs, screenshots, configs, and policy proof.

**Agentic disruption thesis:** automate evidence gathering and report drafting
while preserving human sign-off.

**Why now:** Vanta, FloQast, ServiceNow, and other governance vendors are adding
AI, but the evidence chase remains expensive.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

The score is inferred from audit labor, GRC spend, and the obvious time sink of
collecting proof across source systems.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** regulated companies preparing SOC 2, HIPAA, PCI, or
similar audits.

**Current workaround:** spreadsheets, shared drives, and manual screenshot
collection.

**Switching reason:** faster audits and lower evidence-gathering cost.

**Payment signal:** enterprise GRC contracts and audit services.

**30-day reachability:** one framework and one evidence vault can prove the
wedge.

**Verdict: PROCEED, but keep evidence read-only.**

## 2. The 30-Day Scope Definition

**Project name:** Audit Evidence Copilot

**Validated problem:** teams lose hours finding logs, configs, and policy
evidence for one framework.

**Target user:** compliance operator with auditor oversight.

**Core hypothesis:** an agent can collect read-only evidence from source systems
and produce an audit packet.

### In Scope

1. **Evidence collection**
   - Acceptance criterion: read-only pull from source systems with provenance.
2. **Narrative drafting**
   - Acceptance criterion: agent drafts control narratives and test explanations.
3. **Review workflow**
   - Acceptance criterion: compliance owner approves, edits, or rejects.

### Explicitly Out Of Scope

- Acting as the system of record for compliance programs.
- Making policy decisions on behalf of auditors.
- Writing to source systems.
- Replacing the GRC platform.

### Week-By-Week Milestones

- **Week 1:** connect source systems and define the framework scope.
- **Week 2:** build evidence vault and control mapping.
- **Week 3:** draft evidence packets and narrative summaries.
- **Week 4:** pilot a single framework with human sign-off.

**Dependencies:** source-system read access, framework scope, and audit owner
approval.

**Acceptance test:** the team can produce a complete evidence packet without
manual file hunting.

**Top risks:** access limitations, stale evidence, and overclaiming automation.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: compliance review console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for evidence and controls.
- Auth: SSO plus service accounts for source systems.
- Database: Postgres for controls, evidence, packets, and approvals.
- Observability: OpenTelemetry and audit logs.
- Hosting: cloud app with queue worker.

**Architecture:** source systems -> evidence pull -> normalization -> control
mapping -> draft packet -> human review. The agent keeps read-only boundaries
and records provenance.

**Critical design decisions:**

1. Keep evidence read-only and provenance-heavy.
2. Separate control mapping from narrative drafting.
3. Preserve human approval before any audit packet is exported.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/evidence/pull` | collect source evidence | source target, control_id | evidence refs | service token | retry queue |
| POST | `/api/compliance/draft` | draft control narrative | control_id, evidence set | draft packet | service token | fallback to outline |
| POST | `/api/compliance/approve` | approve or edit packet | packet_id, reviewer_state | approved packet | reviewer token | reject invalid state |

### Folder / Module Structure

- `app/compliance/`
- `app/api/evidence/`
- `services/pull/`
- `services/draft/`
- `workers/packets/`
- `lib/mapping/`

### Environment Variables

- `EVIDENCE_SOURCES_TOKEN`
- `GRC_API_KEY`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `EXPORT_BUCKET`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| GRC workflow | high | Vanta / ServiceNow already own it | BUY | not the wedge |
| Evidence collection | medium | humans still do the chase | BUILD | core wedge |
| Narrative drafting | medium | manual and repetitive | BUILD | high leverage |

**Bottom line:** buy the workflow shell, build the evidence-capture and packet
drafting layer.

## 5. MVP ROI Business Case

**Current-state cost model:** audit labor, evidence hunting, and consultant time.

**Agentic MVP cost model:** source-system access, model usage, evidence storage,
and review labor.

**Pricing options:**

1. Fixed audit pilot.
2. Per framework.
3. Enterprise audit package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | one framework, limited automation | 12-18 months | month 14+ | narrow fit |
| Base | 30-40% less evidence-hunting time | 6-9 months | month 8-12 | strong ops fit |
| Upside | multiple frameworks and repeat use | 3-5 months | month 4-6 | high leverage |

**Formulas**

```text
Monthly value =
  audit labor avoided + consultant time reduced + evidence-search time saved
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if source-system access is read-write only, the product is
too risky.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Vanta | GRC | system of action branding | evidence chase remains manual | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_34_Competitor_Teardown.md` |
| FloQast | close / compliance | finance workflow depth | still requires human evidence chasing | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_34_Competitor_Teardown.md` |
| ServiceNow GRC | workflow platform | broad enterprise footprint | heavy implementation | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_34_Competitor_Teardown.md` |

**Direct threats:** Vanta and ServiceNow GRC.

**What not to build:** a new compliance system of record or policy engine.

**Agentic wedge:** pull evidence automatically, draft packet narratives, and
leave sign-off with the auditor or compliance owner.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Evidence pull | control selected | system queries source | refs captured with provenance | source replay |
| Packet draft | evidence set ready | agent drafts narrative | packet is reviewable | diff against template |
| Approval | reviewer edits | state changes | export reflects approval | workflow test |

### Edge Cases

- Missing source access.
- Conflicting evidence dates.
- Stale control owner.
- Partial framework coverage.
- Auditor requests extra proof.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| evidence refs | source systems | evidence vault | source system | realtime | provenance required |
| control map | compliance team | control table | GRC owner | versioned | approval state |
| packet drafts | agent output | packet table | compliance owner | realtime | human review |
| approvals | reviewer action | approval table | reviewer | realtime | role-based access |

**Retention and deletion:** retain approved packets and provenance, expire raw
drafts by policy, and keep audit trails for every export.

**Privacy/security:** least-privilege source access, tenant isolation, and
redaction of regulated data where required.

**Analytics questions:** which controls take the longest to evidence and which
source systems create the most manual search time?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one framework, source access, control map, rollback
flag.

**Staging:** read-only pull, then draft-only mode.

**Production sequence:** one framework, one compliance owner, one auditor
review path.

**Smoke test:** produce one complete evidence packet for a single control.

**Rollback:** disable evidence pull and fall back to manual collection.

**Observability:**

- Logs: source, control, evidence ref, packet version.
- Metrics: evidence pull success, packet completion, review time.
- Alerts: source access failure, stale evidence, export errors.
- Dashboards: control coverage and evidence chase time.

## 10. Post-Launch Iteration Plan

**Metrics:** evidence-hunt time saved, packet completion rate, review time, and
framework coverage.

**Week-by-week:**

- Week 1: expand source coverage.
- Week 2: improve evidence mapping.
- Week 3: shorten packet drafting.
- Week 4: package for adjacent frameworks.

**Pivot signals:** add more source connectors if access is the bottleneck,
constrain to one framework if compliance objects to breadth, and prioritize
read-only sources if security concerns increase.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Compliance_and_Audit_Agent_Disruptive_Teardown.md` - upstream teardown dossier for the compliance/audit wedge.
- Official reference points reviewed: Workiva, AuditBoard, Thomson Reuters, and SAP GRC product pages.
- `runs/2026-06-26-agentic-opportunity-blueprints/source/Use_Case_34_Competitor_Teardown.md` - GRC incumbent map and evidence-chase wedge.
