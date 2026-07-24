---
status: reviewed
use_case: "Prior Authorization Agent"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: medium-high
  pricing: low-medium
  implementation: medium-high
---

# Prior Authorization Agent Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** Revenue cycle leader, ambulatory operations leader, or
specialty-practice administrator at a provider group with high prior-
authorization volume in one narrow transaction class, such as outpatient
imaging, MSK, DME, cardiology procedures, or specialty drugs.

**Later ICPs:** health-system access leaders and enterprise RCM transformation
owners after one specialty/payer workflow proves packet completeness, staff-time
reduction, and safety controls.

**Pain wedge:** Prior authorization is an administrative packet-completion and
follow-up problem. Staff must determine requirements, collect chart evidence,
map payer criteria, fill forms, submit through inconsistent channels, and chase
status.

**Incumbent weakness:** Cohere, Anterior, EviCore, Carelon, CoverMyMeds,
Surescripts, Availity, Waystar, Experian Health, and payer portals each cover
part of the workflow. Providers still carry the cross-channel burden, especially
when portals, faxes, EHRs, and payer policies do not align.

**Agentic disruption thesis:** Do not claim autonomous adjudication. Build a
provider-side copilot that completes the packet, cites evidence, submits through
available channels, and follows until disposition with human review.

**Why now:** CMS-0057-F creates regulatory forcing functions around prior-auth
APIs, denial reasons, decision timeframes, and public metrics. AMA and KFF data
show public pain and workflow burden. Agent benchmarks also show that full
autonomy remains risky, which supports a constrained copilot wedge.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 28/30**

This score is inferred from public pain data, regulatory forcing functions, and
competitor research. It is not yet buyer-interview validated and should be
confirmed with at least three provider/RCM interviews before being used as a
sales claim.

- Problem realness: 10/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** Prior-auth coordinators, revenue cycle teams,
specialty practices, physicians, and patients waiting for approval. High-volume
specialties include outpatient imaging, MSK, cardiology, DME, and specialty
drugs.

**Last-time/recency evidence:** AMA's 2025 survey says practices average 40
prior authorizations per physician per week and spend 13 hours weekly. KFF's
July 2025 poll found 51% of insured adults had needed prior authorization in
the prior two years.

**Current workaround:** Staff use payer portals, phone, fax, clearinghouses,
EHR tasks, spreadsheets, prior-auth vendors, and manual follow-up.

**Switching reason:** The agent finishes a complete, auditable packet and
status-follow-up loop without asking providers to wait for full payer-side API
maturity.

**Payment signal:** Vendor pricing is mostly opaque and enterprise-sales led.
The stronger evidence is cost-of-pain: physician time, dedicated staff, delayed
care, denial increases, and regulatory deadlines.

**30-day reachability:** High. Specialty practices and RCM leaders with high
prior-auth volume are identifiable by specialty, payer mix, and staffing.

**Verdict: PROCEED.** The wedge is strong, but it must be narrow and safety-
bounded.

## 2. The 30-Day Scope Definition

**Project name:** Prior Auth Packet Copilot

**Validated problem:** Providers spend excessive staff time assembling,
submitting, and tracking prior-auth packets across payer-specific requirements.

**Target user:** Prior-auth coordinator or RCM manager in one specialty with a
repetitive transaction class.

**Core hypothesis:** A constrained agent can reduce staff minutes per
authorization by preparing complete packets and tracking status, while leaving
clinical judgment and final submission approval to humans.

### In Scope

1. **Case intake**
   - Acceptance criterion: staff can upload/order-import patient, payer,
     provider, CPT/HCPCS/NDC, ICD, chart note, and requested service details.
2. **Requirement detection**
   - Acceptance criterion: system identifies whether PA is likely required and
     what documentation is needed for selected payers/policies.
3. **Evidence extraction**
   - Acceptance criterion: chart evidence is extracted and mapped to criteria
     with source citations.
4. **Packet generation**
   - Acceptance criterion: form fields, medical necessity letter, codes,
     attachment checklist, and requested duration/units are drafted.
5. **Submission/tracking assist**
   - Acceptance criterion: staff can submit through portal/fax/email assist and
     track status/more-info requests.

### Explicitly Out Of Scope

- Autonomous coverage decisions or denial decisions.
- Changing care plan, ordering treatment, or giving clinical advice.
- Full FHIR PAS implementation in 30 days.
- Deep EHR writeback, payer adjudication, claim submission, or appeals
  automation beyond packet support.
- Browser automation using shared credentials without explicit audit controls.
- Multi-specialty, all-payer support in v1.

### Week-By-Week Milestones

- **Week 1:** Pick one specialty/use case, define 3-5 payer policies, build
  templates, and collect 50 prior cases.
- **Week 2:** Build intake, evidence extraction, missing-document detection, and
  criteria mapping.
- **Week 3:** Generate packet, reviewer UI, audit log, and submission assist.
  Run shadow comparison against historic cases.
- **Week 4:** Pilot on live cases with human approval. Measure staff minutes,
  first-pass completeness, more-info requests, and status tracking.

**Dependencies:** sample cases, payer policies, chart-note exports, CPT/ICD
mapping, staff reviewer, HIPAA/security review, and submission process owner.

**Acceptance test:** For a selected payer/policy, the agent produces a complete
packet with cited chart evidence, missing-document flags, and human approval
before submission.

**Top risks:** HIPAA/PHI, stale payer criteria, wrong codes, missing evidence,
automation bias, and credential/session security for payer portals.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: Next.js + TypeScript case workbench and status board.
- Backend: Python FastAPI for intake, document extraction, policy mapping, and
  workflow APIs.
- Orchestration: explicit workflow graph for intake, evidence extraction,
  criteria mapping, packet generation, review, submission assist, and follow-up.
- Data: Postgres for cases, policy criteria, packet status, audit events,
  reviewer actions; object storage for chart notes/forms; vector index for
  payer policies and clinical criteria.
- Document AI: OCR/layout extraction for PDFs/faxes and structured extraction
  for codes, dates, diagnoses, medications, and clinical findings.
- Integrations: EHR export/manual upload first; optional clearinghouse, portal
  assist, fax/email, and FHIR APIs later.
- Security: HIPAA-aligned controls, BAA-ready hosting, encryption, RBAC,
  audit logs, minimum necessary PHI, and retention controls.

**Architecture:** The agent sits provider-side. It does not adjudicate
coverage. It creates a packet and follows status. Human staff approve
submission and handle exceptions.

**Critical design decisions:**

1. **One specialty first:** payer policies are too variable for broad launch.
2. **Portal/fax/email assist before full API:** CMS APIs matter, but a 30-day
   MVP must handle today's messy channels.
3. **Citations over summaries:** every clinical claim must cite chart evidence
   or payer policy.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/pa/intake` | Start a prior authorization case | Patient/payer/procedure payload, tenant ID | Case ID | Clinic admin token | Reject if key clinical fields are missing |
| GET | `/api/pa/cases/:caseId` | Fetch packet state and evidence | Case ID | Status, citations, pending items | RBAC session | 404 if case missing; 403 on tenant mismatch |
| POST | `/api/pa/cases/:caseId/generate-packet` | Build the submission packet | Case ID, policy version | Packet draft and completeness score | Staff role | Fail closed if chart evidence is insufficient |
| POST | `/api/pa/cases/:caseId/submit` | Assist submission to payer | Case ID, channel, reviewer approval | Submission receipt | Approved staff role | Block if approval or required attachments are missing |
| POST | `/api/webhooks/payer-status` | Receive status updates from portals/rails | Payer webhook payload | Ack + queued sync | Signed webhook secret | Retry transient failures; dedupe duplicate events |

### Folder / Module Structure

- `app/(console)/pa/` for case workbench, packet review, and status tracking.
- `app/api/pa/` for intake, packet generation, submission assist, and status APIs.
- `app/api/webhooks/` for payer status and transaction updates.
- `services/pa-agent/` for extraction, criteria mapping, and packet assembly.
- `services/connectors/ehr/` for chart export and manual upload normalization.
- `services/connectors/fax/`, `services/connectors/email/`, `services/connectors/payer-portal/` for messy-channel submission support.
- `lib/clinical/` for policy criteria, evidence citation, and packet templates.
- `tests/pa/` for PHI boundaries, evidence completeness, and submission regressions.

### Environment Variables

- `DATABASE_URL`: Postgres for cases, policy criteria, and audit records.
- `OBJECT_STORAGE_BUCKET`: storage for charts, forms, and packet snapshots.
- `REDIS_URL`: queue backend for packet assembly and follow-up jobs.
- `MODEL_ROUTER_API_KEY`: provider-router credential.
- `MODEL_ROUTER_BASE_URL`: model gateway endpoint.
- `EHR_EXPORT_TOKEN`: EHR export or manual-upload integration.
- `FAX_API_KEY`: fax submission support.
- `EMAIL_SMTP_HOST`: email submission support.
- `AVAILITY_API_KEY`: clearinghouse or payer-rail integration.
- `COVERMYMEDS_API_KEY`: submission rail integration where available.
- `SURESCRIPTS_API_KEY`: payer-status and rail integration where available.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: traces and metrics export.
- `SENTRY_DSN`: error tracking.

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Payer-side UM | Very high | Cohere/Anterior/EviCore sell to payers | BUY/INTEGRATE LATER | Provider wedge should not require payer-side control. |
| ePA transaction rail | High | CoverMyMeds/Surescripts/Availity/Waystar/Experian | HYBRID | Use available channels; do not rebuild clearinghouse in v1. |
| Evidence extraction | Medium | Generic document AI exists | BUILD | Criteria-specific chart mapping is core. |
| Packet generation | Medium | Some vendors provide workflow tools | BUILD | Complete packet is the wedge. |
| Status tracking | Medium | Portals/RCM tools partial | BUILD | Follow-up loop creates operational value. |
| FHIR PAS | High | Standards/API infrastructure emerging | DEFER | Important roadmap, too heavy for first 30 days. |

**Bottom line:** Build the provider-side packet copilot and status loop. Buy or
integrate transaction rails where available.

## 5. MVP ROI Business Case

**Current-state cost model:** staff time per PA, physician time, delayed care,
denials/rework, more-info requests, phone/fax/portal chasing, and patient
abandonment. AMA reports 40 PAs per physician per week and 13 hours weekly.

**Agentic MVP cost model:** policy ingestion, document extraction, packet
generation, reviewer queue, submission assist, tracking board, PHI-compliant
hosting, and audit storage.

**Pricing options:**

1. Fixed pilot for one specialty and 100 live cases.
2. Per completed packet with platform minimum.
3. Enterprise package by specialty/payer group plus support.

Use buyer-specific inputs where available. Default formulas:

```text
Current monthly PA admin cost =
  monthly PA volume * staff minutes per PA / 60 * loaded staff hourly cost
  + physician minutes per PA / 60 * loaded physician hourly cost
  + rework/denial follow-up cost

Agentic monthly cost =
  platform minimum + (completed packets * packet fee)
  + human review minutes / 60 * loaded staff hourly cost

Monthly value =
  current monthly PA admin cost avoided - agentic monthly cost

Payback period =
  pilot/build cost / monthly value
```

Illustrative assumptions, not universal claims:

- Loaded PA coordinator cost: `$35-$55/hour`.
- Physician review/escalation cost: buyer-specific; use only if physician time
  is actually reduced.
- Current staff time: use AMA's 13 hours weekly per physician as macro pain
  evidence, then replace with buyer-specific measured minutes per case.
- Pilot/build cost: examples below assume `$30K-$60K` for a focused specialty
  pilot with PHI controls.
- Packet fee target: `$8-$25` per completed packet depending volume and review
  requirements.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | 100 cases/mo, poor chart data, 20% staff-time reduction, `$45/hr` coordinator cost, high review overhead, `$30K` pilot | Slow | 12-24 months | Use as research pilot only. |
| Base | 300+ cases/mo, repetitive payer policies, 40% staff-time reduction, `$45/hr` coordinator cost, `$15/packet`, `$45K` pilot | Moderate | 4-8 months | Strong specialty practice wedge. |
| Upside | 1,000+ cases/mo, repetitive policies, 50%+ staff-time reduction, fewer more-info requests, `$12/packet`, `$60K` pilot | Fast | 2-4 months | Strong health-system/RCM case. |

**No-go condition:** If payer policies cannot be obtained, chart evidence is
unusable, or human review owner is absent, the MVP should not proceed.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Cohere Health | Payer UM | Policy digitization and UM platform | Enterprise implementation; payer-side orientation | Demo/sales-led; implementation cited | Cohere |
| Anterior | Clinical AI/PA | AI reviewer-assist and business case framing | Enterprise sales; not provider packet wedge only | Demo/business case | Anterior |
| CoverMyMeds | ePA | Pharmacy/ePA infrastructure | More transaction rail than full provider packet copilot | Sales-led | McKesson/CMM |
| Surescripts ePA | ePA network | Electronic prior authorization network and payer/provider connectivity | More transaction infrastructure than full packet copilot | Sales-led | Surescripts/category research |
| Availity | Provider-payer network | Eligibility, authorization, payer-provider transaction footprint | Broad portal/network workflow; not the narrow packet agent | Sales-led | Availity/category research |
| Waystar | RCM/clearinghouse | Revenue-cycle workflow footprint | Broad RCM; agentic packet depth is not the core wedge | Sales-led | Waystar/category research |
| Experian Health | RCM/PA workflow | Existing provider administrative workflow footprint | Enterprise RCM orientation | Sales-led | Experian/category research |
| Honey Health | Healthcare admin AI | Agentic admin positioning | Pricing not transparent publicly | ROI/pricing funnel | Honey |

**Direct threats:** Anterior and Honey Health for agentic admin; Cohere for
policy/UM automation. **Table stakes:** evidence extraction, policy mapping,
packet generation, tracking, audit. **Do not build:** autonomous adjudication,
full payer UM, or all-payer/all-specialty support. **Gaps:** provider-side
narrow wedge, messy-channel support, and full packet follow-up.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Intake | Order/chart/payer data uploaded | Case is created | Required fields extracted or flagged missing | Intake report |
| Criteria mapping | Payer policy loaded | Agent reviews chart | Evidence maps to criteria with citations | Criteria table |
| Packet draft | Required evidence exists | Agent generates packet | Form/letter/attachments are complete | Reviewer checklist |
| Missing info | Evidence is absent | Agent reviews case | Missing item is flagged with reason | Missing evidence report |
| Human review | Packet ready | Staff approves/edits | Submission cannot proceed without approval | Audit log |
| Status tracking | Submission recorded | Follow-up timer runs | More-info/denial/approval status captured | Status board |

**Edge cases:** duplicate patient/order, stale payer policy, wrong CPT/ICD,
illegible chart note, portal outage, fax failure, more-info request, appeal
trigger, urgent expedited case, and non-covered service.

## 8. Data Architecture Lite

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| Patient/order | EHR/export/manual | Case table | EHR | Upload/API | Required PHI/code fields |
| Chart evidence | PDF/chart note | Object storage + extracted spans | EHR/source doc | Upload | Citation and OCR confidence |
| Payer criteria | Policy docs | Versioned criteria store | Payer policy | Manual refresh | Effective date/version |
| Packet | Agent draft + reviewer edits | Packet table/object | Submitted packet | Per case | Human approval |
| Submission status | Portal/fax/email/clearinghouse | Status table | Payer/channel | Manual/API | Timestamp/proof |
| Audit | System events | Append-only log | Audit log | Append-only | User/action/source |

**Analytics questions:** Which payer policies cause most missing-info requests?
How much staff time is saved? Which case types are not suitable? What is
first-pass completeness? Where do denials cluster?

**Privacy/security:** PHI requires BAA, RBAC, audit trails, encryption, minimum
necessary access, retention controls, and incident response. Browser automation
requires delegated accounts, least privilege, and explicit session logs.

## 9. Deployment Sequencing

**Pre-deploy:** sign BAA/security review, confirm specialty, policy set, sample
cases, submission channel, and reviewer ownership.

**Staging:** use synthetic/sanitized cases. Test extraction, citations, missing
evidence, packet generation, and status tracking.

**Production:** start with human-reviewed packet drafts only. Enable submission
assist after staff validates packet quality. Do not automate clinical decisions.

**Smoke test:** create case, extract evidence, map criteria, generate packet,
approve, record submission, trigger follow-up timer, and verify audit trail.

**Rollback:** disable new case intake and submission assist, export packets and
audit, return to manual process.

## 10. Post-Launch Iteration Plan

**Metrics:** activation equals percent of eligible cases processed; retention
equals weekly staff use and new case volume; revenue signal equals paid pilot
extension or per-packet agreement.

**Week 1:** fix extraction and criteria mapping. No new payer/specialty.

**Week 2:** interview coordinators and physicians. Identify the top missing
evidence or rework driver.

**Week 3:** improve that driver or add one payer policy.

**Week 4:** measure staff minutes, first-pass completeness, and more-info rate.

**Pivot signals:** accuracy below clinical safety threshold, staff distrusts
packets, policies change too fast to maintain, or PHI/security review blocks
deployment.

## Source Notes

- CMS CMS-0057-F -
  https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f.
- AMA 2025 prior authorization survey -
  https://www.ama-assn.org/system/files/prior-authorization-survey.pdf.
- KFF prior authorization poll -
  https://www.kff.org/patient-consumer-protections/kff-health-tracking-poll-public-finds-prior-authorization-process-difficult-to-manage/.
- Cohere Health - https://www.coherehealth.com/utilization-management-suite.
- Anterior - https://www.anterior.com/prior-authorization-solution.
- Honey Health -
  https://www.honeyhealth.ai/platform/prior-authorization-management-5lwwb.
- HealthAdminBench - https://arxiv.org/abs/2604.09937.
- CHI-Bench - https://arxiv.org/abs/2605.16679.
- AI-Generated Prior Authorization Letters -
  https://arxiv.org/abs/2603.29366.
- Anterior fairness evaluation - https://arxiv.org/abs/2603.14631.
