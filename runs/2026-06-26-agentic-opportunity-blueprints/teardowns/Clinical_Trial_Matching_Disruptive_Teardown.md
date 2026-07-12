---
status: reviewed
use_case: "Clinical Trial Matching"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Clinical Trial Matching Disruptive Competitor Teardown

## Market Frame
- Workflow: match patient histories to trial inclusion/exclusion criteria and route to coordinators.
- Target buyer: clinical research ops, trial sponsors, and site coordinators.
- Existing spend category: CTMS, matching tools, and coordinator labor.
- Incumbent economic model: enterprise quotes and long rollout cycles.
- Agentic wedge: semantic matching layer that understands unstructured records without requiring a full CTMS rebuild.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| IQVIA CTM | CRO / trial management | Sponsors, sites | Enterprise custom quotes | Heavy deployment and integration | Scale and compliance | Expensive and slow |
| Medidata | Clinical cloud | Sponsors | Enterprise quotes | Implementation and validation | Platform breadth | Large rollout burden |
| Veeva Vault | Clinical suite | Sponsors | Enterprise pricing | Deep configuration | Regulated platform | Heavy deployment |
| Tempus AI | Matching / data platform | Oncology / research | Enterprise / sales-led | Data integration burden | Data-driven matching | Narrower domain focus |
| Antidote | Matching platform | Patients/sites | Sales-led | Matching and workflow setup | Specialized matching | Still workflow-heavy |
| OpenClinica | EDC/CTMS | Research ops | Enterprise / open-source mix | Validation and setup | Modern clinical tooling | Not enough on unstructured matching |

## Direct Threats
1. IQVIA and Medidata.
2. Veeva Vault and Tempus AI.

## Pricing Friction
- Enterprise custom quotes and services are common.
- Rollouts can run 6-12 months.

## Onboarding And Workflow Friction
- Matching relies on structured data and coordinators still read charts manually.
- UIs and deployment cycles are outdated and heavy.

## What Not To Build
- Do not build a full CTMS or EDC system.
- Do not pretend matching can ignore regulatory controls.

## What To Keep
- Existing CTMS, EHR, and sponsor workflows.
- Human review for eligibility edge cases.

## Agentic Wedge
- Wedge statement: ingest unstructured patient histories and match semantically against trial criteria.
- Why it wins: reduces manual screening cost and speeds enrollment.
- Why now: sponsors want lower CAC for trial recruitment.

## Blueprint Inputs
- Scope implication: one indication area and one trial cohort.
- Architecture implication: secure matching layer over clinical records.
- Build-vs-buy implication: keep the research ops stack; build the matcher.
- ROI implication: fewer screened-out patients and lower coordinator burden.
- QA/deployment implication: inclusion/exclusion test sets and audit logs are mandatory.

## Source Notes
- Source teardown in `source/Clinical_Trial_Matching_Competitor_Teardown.md`.
