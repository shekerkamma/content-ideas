# KYC/AML Onboarding Agent Research Memo

Research value: high. The market is mature, crowded, and already moving toward
agentic compliance, but pricing opacity and workflow fragmentation leave a
credible wedge for a narrow onboarding-review agent.

## Incumbents And Categories

Identity verification / KYC APIs: Persona, Sumsub, Veriff, Trulioo, iDenfy,
Onfido/Entrust, Jumio. These focus on ID document verification, liveness,
biometrics, database checks, proof of address, reusable KYC, and watchlist
add-ons.

Identity decisioning / orchestration: Alloy, Socure, Sardine. These vendors sit
above raw checks, combining rules, risk signals, vendor routing, case
management, fraud graphing, and lifecycle monitoring.

AML screening / financial crime platforms: ComplyAdvantage, Unit21, NICE
Actimize, Feedzai, Oracle FCCM, Fenergo, Napier, Refinitiv/LSEG, Moody's Grid,
Dow Jones Risk & Compliance.

KYB / business onboarding specialists: Arva AI, Middesk, Detected, FullCircl,
Creditsafe, Dun & Bradstreet, Trulioo Business Verification. Arva is a sharp
agentic competitor, claiming AI agents for screening, KYB/KYC, and transaction
monitoring.

Bank core / CLM incumbents: Fenergo, Pega, Salesforce FSC, nCino, Appian,
ServiceNow, and internal bank workflows.

## Pricing / Pricing Friction Evidence

Public pricing exists mainly for lower-end IDV and AML screening; enterprise
onboarding remains opaque.

- Persona Essential starts at `$250/month`, minimum 12-month term. Growth and
  Enterprise are sales-led, with advanced KYB, Graph, marketplace apps, custom
  redaction, permissions, data residency, SAR features, and bespoke automations
  gated into higher plans.
- Sumsub Basic is `$1.35/verification` with `$149` minimum monthly commitment;
  Compliance is `$1.85/verification` with `$299` minimum monthly commitment and
  includes AML screening, ongoing AML monitoring, and proof of address.
  Enterprise is sales-led.
- Veriff Essential is `$0.80/verification` with `$49/month` minimum; Plus is
  `$1.39/verification` with `$99/month` minimum; Premium is
  `$1.89/verification` with `$209/month` minimum. PEP/sanctions screening adds
  `$0.64/verification`; ongoing monitoring adds `$0.09/verification`.
- ComplyAdvantage Starter begins at `$99/month` for monitored entities up to
  2,000; Enterprise is sales-led.
- iDenfy add-on pricing shows manual review, PEP/sanctions, proof of address,
  and enterprise-volume verification add-ons.
- Alloy, Socure, Trulioo, Sardine, and Arva largely push demo/contact-sales for
  full platforms, signaling enterprise procurement and integration friction.

## Buyer Pain / Workflow Friction

Regulators require risk-based CDD, ongoing monitoring, beneficial ownership
verification, SAR decisioning, alert management, and auditability. FFIEC's
BSA/AML manual makes clear that banks need procedures for customer risk
profiles, ongoing monitoring, beneficial ownership updates, alert management,
SAR decisions, and documented conclusions.

Operational pain clusters around:

- Manual investigation load: alert management requires internal/external
  research tools, adequate staffing, escalation, and documented conclusions.
- Fragmented evidence: onboarding pulls from IDV, sanctions, adverse media,
  corporate registries, beneficial ownership, transaction expectations, CRM,
  and core banking systems.
- False positives and review queues: vendor claims from ComplyAdvantage and
  Arva reveal the buying pain around routine alert resolution and L1 review
  volume.
- Conversion versus risk tradeoff: Alloy and Socure frame onboarding around
  approving more good customers while reducing friction and manual review.

## Disruptive Agentic Wedge

The strongest wedge is a CDD/EDD review copilot that turns messy onboarding
evidence into an auditable decision packet, not another raw KYC API.

Position it as an overlay that sits on top of Persona, Sumsub, Veriff, Alloy,
and ComplyAdvantage outputs and performs:

- Evidence ingestion from KYC vendors, CRM, registry docs, sanctions/adverse
  media hits, beneficial ownership forms, and analyst notes.
- Policy-specific review against the institution's SOP, risk matrix, prohibited
  industries, geography rules, and escalation thresholds.
- Discrepancy detection across documents, UBO forms, public registries,
  websites, addresses, names, and watchlist matches.
- Explainable recommendation: approve, request info, EDD, reject, or escalate.
- Generated audit packet with evidence table, risk rationale, open questions,
  timestamps, source links, and analyst override controls.

## 30-Day MVP Implications

Narrow MVP: business onboarding / KYB plus individual beneficial-owner CDD
review for fintechs, sponsor banks, payments, or lending platforms.

Build scope:

- Inputs: CSV/API upload, vendor webhooks from Persona/Sumsub/Veriff, PDF
  incorporation docs, UBO certification, sanctions/adverse-media hit exports,
  customer questionnaire, website URL.
- Core agent loop: classify entity, extract fields, compare documents to
  structured form, screen names via configured provider/export, run
  adverse-media/web research if allowed, score against policy, produce decision
  memo.
- Human-in-loop: reviewer queue, approve/escalate/request-more-info buttons,
  required rationale, override logging.
- Auditability: immutable case timeline, source snapshots, prompt/version log,
  evidence citations, rule IDs, confidence bands.
- Integrations: start with one IDV/KYB provider export plus CRM/CSV rather than
  deep bank-core integration.
- Success metric: reduce L1 review time per case by 50%+, increase
  straight-through processing for low/medium-risk cases, and preserve human
  approval for final decisions.

## Risks / Regulatory / Security

- Regulatory defensibility: FFIEC expects documented processes, staff
  responsibility, escalation, SAR decisioning, and customer-risk profile logic.
- Beneficial ownership accuracy: the agent can detect reliability issues, but
  false accusations or missed discrepancies create regulatory risk.
- Model risk management: Fed/OCC SR 11-7 requires validation, governance,
  monitoring, and independent challenge for material model use.
- Privacy/data handling: KYC data includes sensitive PII, biometrics, government
  IDs, addresses, ownership data, and adverse-media evidence.
- Hallucination/source integrity: adverse-media research must cite sources,
  preserve snapshots, and distinguish exact from fuzzy matches.
- Vendor dependence: use licensed screening/IDV providers; do not become the
  regulated screening source of truth on day one.
- FCRA boundaries: keep use-case boundaries clear for credit, employment,
  housing, insurance, and adverse-action workflows.

## Sources

- Persona pricing: https://withpersona.com/pricing
- Persona platform: https://withpersona.com/
- Sumsub pricing: https://sumsub.com/pricing/
- Veriff pricing: https://www.veriff.com/pricing
- ComplyAdvantage pricing: https://complyadvantage.com/pricing/
- ComplyAdvantage platform: https://complyadvantage.com/
- Alloy platform: https://www.alloy.com/
- Socure platform: https://www.socure.com/
- Trulioo platform: https://www.trulioo.com/
- Sardine platform: https://www.sardine.ai/
- Arva AI platform: https://arva.ai/
- FFIEC BSA/AML Manual, CDD:
  https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/02
- FFIEC BSA/AML Manual, Beneficial Ownership:
  https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/03
- FFIEC BSA/AML Manual, Suspicious Activity Reporting:
  https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04
- Federal Reserve/OCC SR 11-7 Model Risk Management:
  https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm
