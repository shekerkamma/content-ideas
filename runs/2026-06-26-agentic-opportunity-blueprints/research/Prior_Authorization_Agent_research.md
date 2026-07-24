# Prior Authorization Agent Research Memo

Research value: high. Prior authorization has strong public pain evidence,
clear regulatory forcing functions, and an active vendor field, but pricing is
mostly opaque.

## Incumbent Competitors And Categories

- Payer-side utilization management platforms: Cohere Health, Anterior, EviCore,
  HealthHelp/WNS, Carelon and other benefit-management vendors. These sell to
  health plans and delegated UM entities, emphasizing clinical review
  automation, policy digitization, reviewer assist, and real-time approvals.
- Provider-side prior-auth/ePA workflow tools: CoverMyMeds/McKesson,
  Surescripts ePA, Availity, Waystar, PriorAuthNow/Rhyme, Experian Health,
  clearinghouse/RCM platforms. These sit closer to eligibility, order intake,
  EHR workflows, payer portals, and claim/revenue cycle operations.
- Agentic/back-office healthcare AI entrants: Honey Health, SmarterDx,
  Anterior-style clinical AI, and denial/appeals tools such as Counterforce
  Health. These frame the problem as end-to-end administrative work.
- Standards/infrastructure layer: CMS-0057-F, HL7 FHIR, Da Vinci CRD/DTR/PAS,
  payer APIs, and X12 278 coexistence.

## Pricing / Pricing-Friction Evidence

- Public SKU pricing is largely absent for major prior-auth vendors. Cohere,
  Anterior, Honey, and similar enterprise vendors route buyers to demo,
  consultation, or personalized ROI flows.
- Honey has a public ROI & Pricing link, but no simple crawlable pricing. That
  is buyer-friction evidence.
- Cohere states a typical full implementation is within 6 months, implying
  enterprise deployment and services-heavy pricing.
- Anterior offers business-case validation with sample work and maximum of 10
  hours buyer time, pointing to enterprise ROI selling.
- Economic pain anchors pricing: AMA's 2025 survey says practices average 40
  prior authorizations per physician per week, spend 13 hours weekly, and 40%
  of physicians have staff working exclusively on PA.

## Buyer Pain / Workflow Friction

- AMA's 2025 survey of 1,000 physicians reports 95% say PA delays care, 79% say
  PA can lead to treatment abandonment, 92% say PA negatively affects outcomes,
  and 26% report PA has led to a serious adverse event.
- AMA also reports 94% say PA increases physician burnout, 74% say denials
  increased over five years, and 63%/62% find it difficult to determine whether
  drug/service PA is required.
- KFF's July 2025 poll found 51% of insured adults had needed PA in the prior
  two years; among them, 47% found the process difficult, 48% experienced delay,
  and 43% experienced denial.
- CMS identified the same friction structurally: its final rule requires
  impacted payers to expose APIs that identify documentation requirements,
  support PA request/response, return denial reasons, and publish metrics.

## Disruptive Agentic Wedge

Best wedge: provider-side PA copilot that finishes the whole packet and follows
it until disposition, initially for one high-volume specialty.

The opportunity is not just writing a medical necessity letter. 2026 research
found LLM letters can be clinically strong but miss administrative scaffolding
such as billing codes, requested authorization duration, and follow-up plans.

The constrained agent:

- Detects PA requirement from order, payer, CPT/HCPCS/NDC, plan, and clinical
  context.
- Pulls chart evidence from EHR/files/faxes.
- Maps evidence to payer criteria and generates a submission checklist.
- Produces a complete packet: form fields, codes, clinical notes, attachments,
  letter, requested duration/units/site of care.
- Submits through portal, fax, email, clearinghouse, or FHIR API.
- Tracks status, handles more-information requests, and escalates exceptions.
- Never denies or changes care; it prepares, submits, tracks, and recommends
  approval-supporting evidence for human review.

## 30-Day MVP Implications

Build narrow. Pick one specialty and transaction class, such as outpatient
imaging, cardiology procedures, MSK, DME, or specialty drugs.

MVP scope:

- Intake: CSV/manual order upload plus PDF/chart-note upload; optional
  lightweight EHR export rather than deep integration.
- Rules: start with 3-5 payer policies and structured criteria templates.
- Evidence extraction: diagnosis, CPT/ICD/NPI/member/payer fields; identify
  missing documentation.
- Packet generation: payer-specific form, medical necessity letter, attachment
  bundle, audit trail.
- Human review queue: approve/edit before submission.
- Submission: initially portal/fax/email assist; do not require full FHIR PAS
  integration in 30 days.
- Tracking: status board, next-action timer, evidence of submission,
  denial/more-info reason capture.
- Metrics: cycle time, staff minutes saved, first-pass completeness, requests
  needing human intervention, approval/denial outcome.

Avoid claiming full autonomous prior-auth adjudication. Current benchmarks show
long-horizon healthcare admin agents remain unreliable: HealthAdminBench's best
computer-use agent completed only 36.3% of tasks end to end; CHI-Bench's best
agent resolved 28.0%.

## Risks / Regulatory / Security

- HIPAA/PHI: BAA, access controls, audit logs, minimum necessary data, encrypted
  storage/transit, vendor risk review.
- Clinical safety: hallucinated criteria, missing contraindications, wrong
  codes, stale payer policy, inappropriate automation bias.
- Denial/coverage risk: the agent should not deny, delay, or modify care. Keep
  human signoff and route uncertain cases.
- Fairness: automated PA models need error-rate monitoring across demographic
  groups.
- Regulatory deadlines: CMS-0057-F requires operational PA provisions beginning
  Jan. 1, 2026, denial reasons regardless of request method, 72-hour expedited
  and 7-calendar-day standard decision timeframes for many impacted payers,
  annual public metrics, and Prior Authorization APIs beginning Jan. 1, 2027.
- Workflow security: browser automation over payer portals creates credential,
  session, and auditability issues; prefer delegated accounts, explicit logs,
  and least-privilege credentials.

## Sources

- CMS, Interoperability and Prior Authorization Final Rule CMS-0057-F:
  https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-prior-authorization-final-rule-cms-0057-f
- AMA, 2025 AMA prior authorization physician survey:
  https://www.ama-assn.org/system/files/prior-authorization-survey.pdf
- KFF, Public Finds Prior Authorization Process Difficult to Manage:
  https://www.kff.org/patient-consumer-protections/kff-health-tracking-poll-public-finds-prior-authorization-process-difficult-to-manage/
- Cohere Health utilization management:
  https://www.coherehealth.com/utilization-management-suite
- Anterior prior authorization:
  https://www.anterior.com/prior-authorization-solution
- Honey Health prior authorization:
  https://www.honeyhealth.ai/platform/prior-authorization-management-5lwwb
- HealthAdminBench: https://arxiv.org/abs/2604.09937
- CHI-Bench: https://arxiv.org/abs/2605.16679
- AI-Generated Prior Authorization Letters:
  https://arxiv.org/abs/2603.29366
- Anterior fairness evaluation:
  https://arxiv.org/abs/2603.14631
