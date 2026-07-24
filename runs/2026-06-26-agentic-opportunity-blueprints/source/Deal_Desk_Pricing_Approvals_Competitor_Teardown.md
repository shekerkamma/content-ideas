# OSINT Source Map & Methodology
- **Sources:** Reddit (r/Quote_to_Cash, r/SalesOperations), RevenueWizards, CloudQ
- **Methodology:** Analyzed Reddit to uncover "implementation burnout" and the friction between sales and deal desk teams. Evaluated market data to quantify the ratio of software licensing costs to consulting/implementation fees.

## Company Overview
- **Salesforce CPQ (Revenue Cloud):** Enterprise standard. Positioned as the native quoting and billing engine for Salesforce.
- **Conga CPQ:** Enterprise scale. Positioned as a robust multi-channel quoting solution.
- **DealHub:** Mid-market to Enterprise. Positioned as an agile CPQ and deal room platform.
- **Other Incumbents:** Oracle CPQ, PROS.

## Product Teardown
- **Top 3 Features:** Product configuration bundles, margin guardrails/discount approvals, automated document/quote generation.
- **Pricing Tiers:** $75-$300+/user/month. However, implementation costs are the real barrier, ranging from tens to hundreds of thousands of dollars, often requiring 10-20% annual maintenance budgets.
- **Onboarding Friction:** Over-engineering. Projects fail because they attempt to hardcode decades of messy, manual business rules into rigid software workflows.

## Where They Are Strong
- Enforcing strict margin guardrails. Handling massive, complex product catalogs with thousands of SKUs and dependencies.

## Where They Are Weak
- **Agility:** Approvals often bounce randomly between departments. The systems require specialized, certified administrators to make even simple catalog changes.

## Disruptive Strategy
- **Direct Threats:** Salesforce CPQ and DealHub.
- **Table Stakes:** PDF quote generation, basic discount tiering, CRM integration.
- **What We Must NOT Do:** Do not attempt to rip-and-replace the core ERP product catalog or build a rigid rules engine.
- **3 Specific Gaps (The Agentic Wedge):**
  1. Replace the heavy "Control Layer" with an agile "Orchestration Layer"—an agent that manages exceptions via Slack, reading historical margin data to autonomously approve or route deals.
  2. Subvert the massive implementation consulting fees by using an LLM to dynamically interpret custom quote requests rather than requiring hardcoded bundle rules.
  3. Alleviate the CPQ administrator bottleneck by allowing sales ops to update pricing logic using natural language prompts instead of complex formula fields.
