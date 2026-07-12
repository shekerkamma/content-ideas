# OSINT Source Map & Methodology
- **Sources:** Reddit (r/sales, r/SalesOperations), Visdum, CaptivateIQ, Prospeo
- **Methodology:** Reviewed Reddit to expose the "Excel dilemma" and administrative nightmares of maintaining legacy commission software. Checked pricing benchmarks to quantify the heavy implementation and professional services costs hidden from public view.

## Company Overview
- **Xactly:** Enterprise behemoth. Positioned as an end-to-end SPM (Sales Performance Management) suite.
- **CaptivateIQ:** Mid-market to enterprise. Positioned as a flexible, spreadsheet-like commission platform.
- **Spiff:** Mid-market (now acquired by Salesforce). Positioned as a modern, real-time visibility tool.
- **Other Incumbents:** Varicent, Performio.

## Product Teardown
- **Top 3 Features:** Complex tiered rule builders, ASC 606 compliance reporting, rep visibility dashboards.
- **Pricing Tiers:** Xactly is $40-$60+/user/mo; Spiff ~$75/user/mo; CaptivateIQ ~$35-$55/user/mo. **Crucially, there are massive implementation fees** ranging from $2.5k to $150k+.
- **Onboarding Friction:** Described as "dumpster fire" configuration processes. Often requires scoping out "absurdly detailed" rules and even hiring dedicated engineers to maintain the system.

## Where They Are Strong
- Handling highly complex, multi-currency, multi-tiered enterprise comp plans at scale. Audit compliance.

## Where They Are Weak
- **Usability for Admins:** Heavy reliance on vendor support tickets for minor plan changes. Constant data downloading/uploading workarounds.

## Disruptive Strategy
- **Direct Threats:** Xactly and Spiff.
- **Table Stakes:** Salesforce/CRM integration, transparent rep payout views, audit trails.
- **What We Must NOT Do:** Do not build a standalone SPM platform requiring custom coding to change a bonus tier.
- **3 Specific Gaps (The Agentic Wedge):**
  1. Bypass the $50k+ implementation fee with an autonomous agent that directly reads the compensation PDF and Salesforce closed-won data to reconcile disputes.
  2. Eliminate support tickets by enabling natural language queries for sales reps to understand exactly why they were paid a certain amount.
  3. Target the mid-market where teams are desperate to leave Excel but cannot afford Xactly's professional services burden.
