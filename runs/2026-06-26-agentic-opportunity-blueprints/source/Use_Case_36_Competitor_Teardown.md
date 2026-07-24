# Tenant Screening & Underwriting - Competitor Teardown
## OSINT Source Map & Methodology
- **Sources Mined**: r/PropertyManagement, r/RealEstate
- **Query Strategy**: Researched 'Tenant screening software', 'RealPage', 'AppFolio', 'TransUnion SmartMove', and 'complaints'.
- **Rationale**: To identify points of friction for applicants and operators regarding algorithmic screening, false positives, and hidden costs.

## 1. Competitor Overview
- **RealPage (LeaseStar/Propertyware)**: Massive enterprise suite serving large multifamily portfolios. Heavily scrutinized for pricing algorithms.
- **AppFolio**: Comprehensive PMS with built-in screening capabilities.
- **TransUnion SmartMove**: Standalone, on-demand screening service targeting independent landlords.

## 2. Product Teardown
- **Top 3 Features**: Instant credit checks, automated criminal/eviction history, and integrated lease decisioning.
- **Pricing Tiers**: SmartMove charges $25-$48 per applicant. RealPage/Yardi use per-unit subscription fees plus transactional fees (~$10-$30 per check) hidden in enterprise contracts.
- **Onboarding Friction**: Significant compliance training required. Applicants face a 'black box' process with high fees.

## 3. Where They Are Strong
- **Stickiness**: Seamless integration with the leasing funnel. Once an applicant applies via AppFolio, the screening happens within the same ecosystem.

## 4. Where They Are Weak
- **Inaccuracy & 'Black Box' Denials**: Reddit is filled with complaints about automated tools missing crucial criminal records or erroneously denying tenants due to data errors.
- **Dispute Friction**: The manual review and dispute process is incredibly slow and opaque, putting landlords at liability risk.

## 5. The Disruptive Strategy
- **Top 2 Direct Threats**: RealPage and AppFolio.
- **Table Stakes**: FCRA compliance, instant credit/background pulls.
- **What We Must NOT Do**: Do not try to become a consumer reporting agency (CRA) from scratch. We must orchestrate existing data feeds.
- **The 3 Specific Gaps (Our Agentic Wedge)**:
  1. **Intelligent Document OCR**: Replace failing legacy income verification with an agent that understands edge-case pay stubs and bank statements flawlessly.
  2. **Explainable AI Decisions**: Provide landlords with a human-readable synthesis of *why* an applicant was flagged, rather than a black-box numerical score, mitigating dispute friction.
  3. **Automated Exception Handling**: When a flag occurs, the agent proactively and conversationally reaches out to the applicant to request clarifying documents, eliminating the PM's manual follow-up.
