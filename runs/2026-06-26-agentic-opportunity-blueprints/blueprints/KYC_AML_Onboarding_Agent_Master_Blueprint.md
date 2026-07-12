---
status: reviewed
use_case: "KYC/AML Onboarding Agent"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: medium
  implementation: medium-high
---

# KYC/AML Onboarding Agent Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** Head of Financial Crime, Compliance Operations leader, or COO
at a fintech, sponsor-bank program manager, payments company, or lending
platform processing at least 500 business/KYB onboarding reviews per month with
manual L1 analyst queues.

**Later ICPs:** larger banks, brokers, wealth platforms, and enterprise CLM
teams after the CDD packet workflow proves auditability and analyst-time
reduction in a narrower fintech/payments setting.

**Pain wedge:** KYC onboarding is not just ID verification. Teams reconcile IDV,
sanctions, adverse media, corporate registries, beneficial ownership, CRM/core
banking data, internal policy, analyst notes, and audit requirements before a
defensible decision can be made.

**Incumbent weakness:** Persona, Sumsub, Veriff, Trulioo, Alloy, Socure,
Sardine, ComplyAdvantage, Fenergo, Actimize, and Arva solve important pieces,
but many buyers still have a human review layer stitching evidence into a
decision packet.

**Agentic disruption thesis:** Do not replace regulated data vendors on day one.
Overlay them with a CDD/EDD review copilot that turns messy onboarding evidence
into an auditable recommendation packet.

**Why now:** Public pricing exists for some IDV/AML checks, but full enterprise
platforms are often sales-led. Vendors are already marketing agentic workflows,
which validates demand. The sharper wedge is vendor-neutral, policy-specific,
auditable review acceleration.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 26/30**

This score is inferred from public regulatory guidance, vendor/pricing evidence,
and workflow research. It should be confirmed with at least three compliance or
onboarding operations buyer interviews before being used as a validated sales
claim.

- Problem realness: 10/10
- Solution fit: 9/10
- Buying signal + reachability: 7/10

**Who has the problem:** Compliance analysts, onboarding operations teams,
relationship managers, and compliance leaders handling business onboarding,
beneficial ownership checks, sanctions/adverse-media hits, and EDD escalations.

**Last-time/recency evidence:** Every new customer/business onboarding and every
screening hit creates the work. FFIEC BSA/AML guidance makes clear that banks
need customer risk profiles, ongoing monitoring, beneficial ownership updates,
alert management, SAR decisioning, and documented conclusions.

**Current workaround:** Analysts manually assemble evidence from KYC vendors,
registries, CRM, web research, sanctions/adverse-media tools, PDFs, UBO forms,
and policy documents. They then write rationales and prepare audit trails.

**Switching reason:** The agent does not ask the buyer to rip out Persona,
Sumsub, Alloy, ComplyAdvantage, or Fenergo. It sits above them and compresses
the human review layer.

**Payment signal:** Persona Essential starts at `$250/month`; Sumsub publishes
per-verification and minimum-commit pricing; Veriff publishes per-verification
pricing and add-ons; ComplyAdvantage Starter begins at `$99/month`; enterprise
platforms such as Alloy, Socure, Trulioo, Sardine, and Arva are mostly
sales-led. The market already pays for identity/compliance infrastructure.

**30-day reachability:** Medium-high. Buyers are identifiable by regulated
vertical, onboarding volume, sponsor bank relationships, compliance hiring, and
vendor stack.

**Verdict: PROCEED, with compliance guardrails.** The wedge is strong only if
positioned as analyst-assist and audit-pack generation, not autonomous
regulated decisioning.

## 2. The 30-Day Scope Definition

**Project name:** CDD Packet Copilot

**Validated problem:** KYC/KYB teams spend too much analyst time reconciling
fragmented evidence into defensible onboarding decisions.

**Target user:** Compliance operations team at a fintech/payments/lending
company using at least one KYC provider and manual analyst review.

**Core hypothesis:** A policy-specific agent can reduce L1 review time by 50%+
for low/medium-risk business onboarding cases while preserving human approval.

### In Scope

1. **Case intake**
   - Acceptance criterion: system ingests CSV/API case data, PDF docs, UBO
     forms, vendor exports, website URL, and sanctions/adverse-media hits.
2. **Evidence extraction and normalization**
   - Acceptance criterion: entity name, address, registration, ownership,
     officers, industry, geography, and risk indicators are extracted with
     source references.
3. **Policy mapping**
   - Acceptance criterion: agent maps evidence to buyer SOP, risk matrix,
     prohibited industries, geography rules, and escalation criteria.
4. **Discrepancy detection**
   - Acceptance criterion: conflicting names, addresses, UBO percentages,
     registry data, or watchlist/adverse-media matches are flagged.
5. **Decision packet generation**
   - Acceptance criterion: output includes evidence table, recommendation,
     rationale, open questions, and required human approval.

### Explicitly Out Of Scope

- Replacing licensed IDV/sanctions/adverse-media data providers.
- Autonomous final approval/rejection in the pilot.
- SAR filing decisions, transaction monitoring, fraud adjudication, credit
  eligibility, employment/housing/insurance decisions, or FCRA-regulated use.
- Bank-core migration or CLM replacement.
- Unbounded web research without source snapshots.
- Biometric verification, liveness detection, or document authenticity scoring.

### Week-By-Week Milestones

- **Week 1:** Select one customer segment, ingest policy/SOP/risk matrix, define
  case labels, and collect 50-100 historic reviewed cases.
- **Week 2:** Build intake, document extraction, field normalization, and source
  evidence table.
- **Week 3:** Add policy mapping, discrepancy detection, decision memo, and
  reviewer queue. Run shadow evaluation.
- **Week 4:** Pilot on new low/medium-risk cases with mandatory human approval.
  Measure review time, completeness, escalation, and override reasons.

**Dependencies:** KYC vendor exports or webhooks, policy/SOP, risk matrix,
sample reviewed cases, compliance owner, approved storage/retention rules, and
security review.

**Acceptance test:** For a sample case, the agent generates a complete packet
with all evidence cited, flags discrepancies, labels open questions, and records
human approval or override.

**Top risks:** regulatory defensibility, false positives/negatives, model risk,
PII/biometric handling, and source integrity.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: Next.js + TypeScript reviewer queue and case packet UI.
- Backend: Python FastAPI for intake, extraction, policy checks, and audit APIs.
- Orchestration: deterministic state-machine or LangGraph with explicit stages:
  ingest, extract, compare, policy-map, recommend, review.
- Models: strong extraction/reasoning model with structured-output validation;
  no training on customer data.
- Data: Postgres for cases, evidence, risk factors, recommendations, approvals,
  audit events; object storage for source docs; vector index for policy/SOP.
- Integrations: Persona/Sumsub/Veriff export, Alloy/ComplyAdvantage export,
  Salesforce/HubSpot/CSV, registry docs, licensed screening outputs.
- Security: tenant isolation, encryption, field-level access, redaction,
  retention policy, immutable audit log.
- Observability: model/prompt version, evidence citation, reviewer override,
  rule ID, and confidence logs.

**Architecture:** Existing KYC vendors remain sources for IDV/screening. The
agent creates an evidence graph and decision packet. The compliance reviewer
remains accountable for final disposition.

**Critical design decisions:**

1. **Overlay, not data vendor:** avoids licensing and regulatory source-of-truth
   risk in v1.
2. **Human final decision:** preserves compliance accountability and model-risk
   defensibility.
3. **Source snapshots:** every claim in the packet must trace to a document,
   vendor result, registry, policy, or reviewer note.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/kyc/intake` | Start a new onboarding or screening case | Applicant payload, tenant ID, source system | Case ID | Compliance admin token | Reject if required identity fields are missing |
| GET | `/api/kyc/cases/:caseId` | Fetch evidence packet and status | Case ID | Evidence graph, risk factors, reviewer notes | RBAC session | 404 if case missing; 403 on tenant mismatch |
| POST | `/api/kyc/cases/:caseId/recommend` | Generate a decision memo | Case ID, policy version | Recommendation + citations | Analyst role | Fail closed if evidence is incomplete |
| POST | `/api/kyc/cases/:caseId/approve` | Record reviewer decision | Case ID, reviewer decision, note | Approved disposition | Reviewer role | Block if required review fields are absent |
| POST | `/api/webhooks/vendor-results` | Receive IDV/screening updates | Vendor webhook payload | Ack + queued sync | Signed webhook secret | Retry transient failures and dedupe by event ID |

### Folder / Module Structure

- `app/(console)/kyc/` for reviewer queue, evidence packet, and audit views.
- `app/api/kyc/` for intake, packet, recommendation, and approval APIs.
- `app/api/webhooks/` for vendor result ingestion and sync jobs.
- `services/kyc-agent/` for extraction, policy mapping, and recommendation logic.
- `services/connectors/persona/`, `services/connectors/sumsub/`, `services/connectors/veriff/` for IDV adapters.
- `services/connectors/complyadvantage/`, `services/connectors/alloy/` for screening and decisioning adapters.
- `lib/evidence/` for claim snapshots, citation formatting, and packet assembly.
- `tests/kyc/` for evidence integrity, auth, and reviewer workflow tests.

### Environment Variables

- `DATABASE_URL`: Postgres for cases, evidence, decisions, and audit logs.
- `OBJECT_STORAGE_BUCKET`: storage for source documents and snapshots.
- `REDIS_URL`: queue backend for vendor sync and async processing.
- `MODEL_ROUTER_API_KEY`: provider-router credential.
- `MODEL_ROUTER_BASE_URL`: model gateway endpoint.
- `PERSONA_API_KEY`: identity verification integration.
- `SUMSUB_API_KEY`: identity and screening integration.
- `VERIFF_API_KEY`: identity verification integration.
- `COMPLYADVANTAGE_API_KEY`: sanctions/adverse-media integration.
- `ALLOY_API_KEY`: orchestration and decisioning integration.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: traces and metrics export.
- `SENTRY_DSN`: error tracking.

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| ID verification/liveness | High | Persona, Sumsub, Veriff, Trulioo already mature | BUY | Not the wedge; use vendor outputs. |
| Sanctions/adverse media | High | ComplyAdvantage, Dow Jones, LSEG, Moody's, etc. | BUY | Licensed data matters; do not recreate. |
| Case evidence normalization | Medium | Platforms offer some orchestration but often vendor-bound | BUILD | Vendor-neutral evidence packet is the wedge. |
| Policy-specific review | Medium | Enterprise platforms are sales-led/custom | BUILD | Buyer SOP/risk matrix specificity drives value. |
| Reviewer queue | Medium | CLM/case tools exist | HYBRID | Build focused queue; export to existing case system. |
| Audit trail | Medium | Incumbents have logs but not always cross-vendor rationale | BUILD | Defensibility is central to the product. |

**Bottom line:** Buy regulated data and verification. Build the analyst-assist
layer that packages evidence, applies policy, and accelerates review.

## 5. MVP ROI Business Case

**Current-state cost model:** analyst review time per case, compliance manager
escalation time, onboarding drop-off from delays, vendor check costs,
remediation/rework, audit prep, and false-positive review burden.

**Agentic MVP cost model:** intake/extraction pipeline, policy mapping,
reviewer UI, audit storage, model/API cost, and security/compliance operations.

**Pricing options:**

1. Fixed pilot for 100-250 cases with measured analyst time reduction.
2. Per reviewed case with minimum monthly platform fee.
3. Enterprise package for multiple onboarding teams and policy sets.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | 100 cases/mo, bespoke EDD-heavy mix, 15% analyst-time reduction, `$45/hr` analyst cost, `$35K` pilot | Slow | 12-24 months | Keep as compliance quality tool. |
| Base | 500+ cases/mo, 35% analyst-time reduction, 35 min current review time, `$55/hr` analyst cost, `$50K` pilot, `$4K/mo` run cost | Moderate | 4-8 months | Strong fintech/payments wedge. |
| Upside | 2,000+ cases/mo, 50% analyst-time reduction, high false-positive queue, `$65/hr` blended cost, `$75K` pilot, `$8K/mo` run cost | Fast | 2-4 months | Strong sponsor bank/platform case. |

**No-go condition:** If the buyer cannot provide policy/SOP, representative
reviewed cases, or human reviewer ownership, the MVP cannot be defensible.

Use buyer-specific inputs where available. Default formulas:

```text
Current monthly review cost =
  monthly cases * current analyst minutes per case / 60
  * loaded analyst hourly cost
  + escalation/rework/audit-prep cost

Agentic monthly cost =
  platform/run cost + per-reviewed-case fee
  + residual analyst review minutes / 60 * loaded analyst hourly cost

Monthly value =
  review cost avoided + rework/audit-prep cost avoided - agentic monthly cost

Payback period =
  pilot/build cost / monthly value
```

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Persona | IDV/KYC workflows | Modular identity stack | Advanced capabilities gated by tiers | Essential `$250/month`; higher plans sales-led | Persona |
| Sumsub | Verification/AML | Public per-check pricing and workflows | Packaged feature billing and enterprise sales | `$1.35-$1.85/verification` plus minimums | Sumsub |
| Veriff | IDV | Transparent self-serve checks | Add-ons for PEP/sanctions/monitoring | `$0.80-$1.89/verification` plus add-ons | Veriff |
| ComplyAdvantage | AML screening | Risk intelligence and agentic workflows | Enterprise features sales-led | Starter `$99/month`; enterprise sales-led | ComplyAdvantage |
| Alloy/Socure/Sardine | Decisioning/risk | Orchestration and risk graphs | Sales-led enterprise platform motion | Demo/contact sales | Vendor sites |
| Arva AI | Agentic compliance | Close wedge competitor | Vendor/platform-specific threat | Sales-led | Arva |
| Fenergo / Pega / nCino / Salesforce FSC | CLM/bank onboarding | Deep enterprise workflow footprint | Heavy implementation and suite adoption | Enterprise sales-led | CLM category research |
| NICE Actimize / Feedzai / Oracle FCCM / Unit21 | Financial crime platforms | Transaction monitoring, case management, enterprise controls | Broader AML/fraud platform versus narrow onboarding packet wedge | Enterprise sales-led | Financial crime platform research |
| Middesk / Dun & Bradstreet / Creditsafe | KYB/business data | Business registry and KYB data coverage | Data source, not full policy-specific review copilot | Usage/sales-led | KYB category research |

**Direct threats:** Arva AI and ComplyAdvantage agentic workflows. **Table
stakes:** evidence table, case management, policy mapping, audit trail, reviewer
override. **Do not build:** raw IDV, licensed sanctions data, biometric
verification. **Gaps to exploit:** vendor neutrality, 30-day deployment, and
policy-specific packets over platform replacement.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Case intake | Vendor export + docs uploaded | Case is created | Required fields are extracted or missing fields flagged | Evidence table |
| Policy mapping | Buyer SOP loaded | Agent reviews case | Each risk finding maps to rule/policy section | Rule ID citations |
| Discrepancy detection | Conflicting names/addresses/UBOs exist | Agent compares evidence | Discrepancy is flagged with source references | Discrepancy report |
| Recommendation | Case review completes | Agent produces packet | Recommendation is approve/RFI/EDD/escalate/reject with rationale | Reviewer packet |
| Human approval | Reviewer decides | Reviewer approves/overrides | Decision and rationale are logged | Audit log |
| Source integrity | Web/adverse media used | Packet is generated | Source URLs/snapshots and match confidence are stored | Source log |

**Edge cases:** fuzzy name match, stale registry data, multiple UBO layers,
foreign-language documents, low-confidence OCR, sanctions false positive,
missing policy section, conflicting vendor outputs, and duplicate cases.

## 8. Data Architecture Lite

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| Vendor checks | Persona/Sumsub/Veriff/etc. | Case evidence records | Vendor | API/export | Vendor result ID |
| Documents | PDFs/forms/uploads | Object storage + extracted fields | Source doc | Upload/version | Hash and OCR confidence |
| Policy/SOP | Compliance docs | Versioned policy store + embeddings | Compliance owner | Manual/versioned | Rule IDs |
| Entity data | Forms/registries/CRM | Normalized case tables | CRM/registry/form | Import/API | Field provenance |
| Recommendation | Agent output | Postgres packet | Agent/reviewer | Per review | Human approval required |
| Audit | System events | Immutable audit log | Audit log | Append-only | Timestamp/model/source |

**Analytics questions:** Which cases consume analyst time? Which rules trigger
most escalations? Which vendors create false positives? Which data fields are
most often missing? What is review-time reduction by case type?

**Privacy/security:** KYC data includes sensitive PII, government IDs,
biometrics, addresses, ownership, adverse media, and financial context. Require
encryption, least-privilege access, redaction, retention controls, tenant
isolation, deletion workflows, and model/data-retention restrictions.

## 9. Deployment Sequencing

**Pre-deploy:** confirm use-case boundary, policy/SOP, sample cases, data
retention, reviewer roles, vendor exports, and security controls.

**Staging:** run historic cases in shadow mode. Compare agent packet to prior
human decision and measure missing evidence, false flags, and review time.

**Production:** start with low/medium-risk business onboarding cases only.
Require human final approval. Export packet to existing case/CLM system if
needed.

**Smoke test:** upload case, extract docs, flag discrepancy, map policy, produce
recommendation, approve/override, and verify audit trail.

**Rollback:** disable new case intake, preserve case packets/audit, return to
manual review queue, and export evidence for compliance review.

## 10. Post-Launch Iteration Plan

**Metrics:** activation equals percent of cases with complete packet; retention
equals weekly reviewer usage and repeated case processing; revenue signal equals
paid pilot extension or per-case pricing agreement.

**Week 1:** fix extraction, evidence, policy mapping, and reviewer UX. No new
case type.

**Week 2:** interview analysts and compliance manager. Identify the largest
packet defect or false-positive source.

**Week 3:** improve that defect, add one vendor export, or add one policy rule
cluster.

**Week 4:** measure analyst time reduction and override quality.

**Pivot signals:** unresolved audit concerns, poor source traceability, high
false-negative risk, or inability to access enough representative cases.

## Source Notes

- Persona - https://withpersona.com/ and https://withpersona.com/pricing - accessed 2026-06-26 - KYC workflow and Essential pricing signal.
- Sumsub - https://sumsub.com/pricing/ - accessed 2026-06-26 - per-verification pricing and compliance packaging.
- Veriff - https://www.veriff.com/pricing - accessed 2026-06-26 - IDV and screening add-on pricing.
- ComplyAdvantage - https://complyadvantage.com/ and
  https://complyadvantage.com/pricing/.
- Alloy - https://www.alloy.com/.
- Socure - https://www.socure.com/.
- Trulioo - https://www.trulioo.com/.
- Sardine - https://www.sardine.ai/.
- Arva AI - https://arva.ai/.
- FFIEC BSA/AML CDD -
  https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/02.
- FFIEC Beneficial Ownership -
  https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/03.
- FFIEC Suspicious Activity Reporting -
  https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04.
- Federal Reserve/OCC SR 11-7 -
  https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm.
