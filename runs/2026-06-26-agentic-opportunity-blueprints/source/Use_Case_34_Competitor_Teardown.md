# Commercial Lease Abstraction - Competitor Teardown
## OSINT Source Map & Methodology
- **Sources Mined**: r/CommercialRealEstate, r/RealEstateTechnology, Web search for pricing.
- **Query Strategy**: Targeted legacy incumbents (Yardi, MRI Software, Visual Lease) combined with 'lease abstraction', 'pricing', and 'complaints'.
- **Rationale**: To identify the true human-in-the-loop bottlenecks and pricing friction points hidden behind enterprise sales walls, proving the need for a pure AI agentic approach.

## 1. Competitor Overview
- **Yardi (Smart Lease)**: Massive enterprise property management suite. Valued in the billions. Positions itself as the all-in-one system of record.
- **MRI Software (Contract Intelligence)**: Large enterprise PropTech incumbent scaling through acquisitions (e.g., Leverton AI). Focused on ASC 842 / IFRS 16 compliance.
- **Visual Lease**: Specialized enterprise lease accounting and administration platform. Mid-market to large enterprise focus.

## 2. Product Teardown
- **Top 3 Features**: Embedded database management, automated critical date tracking, and compliance reporting.
- **Pricing Tiers**: Custom enterprise pricing hidden behind sales walls. Typically requires high initial implementation fees + tiered scaling based on modules. Newer pure-play tools charge $15-$20 per lease, exposing the bloated enterprise models.
- **Onboarding Friction**: 'Garbage in, garbage out' mentality. Highly dependent on accurate manual data input and legacy system migration.

## 3. Where They Are Strong
- **Stickiness**: They own the core database and system of record. Integrating deeply with rent rolls and general ledgers makes them incredibly difficult to rip out.

## 4. Where They Are Weak
- **Bloat & Manual Workflows**: Redditors constantly complain about complex historical leases. The tools still require significant human oversight (a 'human-in-the-loop') to verify complex amortized TIs and reimbursement structures.
- **Integration Friction**: Extracting data from these monolithic systems to use in agile underwriting tools remains a pain point.

## 5. The Disruptive Strategy
- **Top 2 Direct Threats**: Yardi and MRI Software.
- **Table Stakes**: Accurate extraction of rent schedules, critical dates, and standard lease clauses.
- **What We Must NOT Do**: Do not build a new lease database or property management system. We must act purely as an intelligence layer that sits on top of Yardi/MRI.
- **The 3 Specific Gaps (Our Agentic Wedge)**:
  1. **Instant, Zero-Touch Abstraction**: Eliminate the expensive 'human review' phase by offering provably accurate, context-aware abstraction.
  2. **Transactional Pricing**: Destroy the custom enterprise quoting model by offering transparent, per-document pricing.
  3. **Seamless API Injection**: Bypass their clunky UI by injecting extracted terms directly into their existing database, becoming the invisible workforce.
