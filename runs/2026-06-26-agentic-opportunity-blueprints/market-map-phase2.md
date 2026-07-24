# Phase 2 Market Map

Date: 2026-06-26

This matrix covers the phase-2 use cases from the dashboard. The detailed teardown method is the same as phase 1: name the incumbents, expose pricing/onboarding friction, and define the agentic wedge.

| Use case | Incumbent category | Direct threats | Pricing friction | Agentic wedge |
|---|---|---|---|---|
| Freight Quote & Routing Agent | Freight brokers / TMS | Freight marketplaces, TMS, procurement tools | Broker commission, platform fees, services-heavy contracts | Automate quote, negotiate, and book across carriers |
| Customs & Bill of Lading Extraction | Customs docs / IDP | OCR, customs brokers, ERP capture tools | Per-document capture fees and manual exception handling | Extract multi-language shipping docs directly into ERP |
| Inventory Forecasting & Re-routing | Supply chain planning / TMS | Planning suites, routing optimizers, control tower tools | Enterprise suite pricing and implementation | Re-route shipments from weather, delays, and demand shifts |
| Supplier Dispute Resolution | AP automation / P2P | AP tools, invoice automation, procurement suites | Module pricing, implementation, and exception labor | Match invoice/PO/receipt and resolve disputes autonomously |
| Prior Authorization Agent | PA / clearinghouse / RCM | CoverMyMeds, Surescripts, Availity, payer portals | Sales-led rails, portal toil, and services burden | Finish the packet, submit, and track to disposition |
| Claim Denial Management | Denial management / appeals | RCM suites, appeals tooling, payer portals | Services-heavy and transaction-based pricing | Draft appeals with cited evidence from denial codes and chart notes |
| Patient Intake & Triage | Intake / symptom-check tools | Patient access suites, triage tools, chatbot intake | Seat/module pricing and clinical workflow setup | Capture symptoms and pre-populate clinical workflow |
| Clinical Trial Matching | Trial matching / recruitment tools | CTMS, EHR search, recruitment services | Services and enterprise integration burden | Match patient histories to trial criteria automatically |
| Commercial Lease Abstraction | Lease abstraction / CRE tooling | Yardi/AppFolio modules, legal ops tooling | Per-seat or services-based pricing | Extract terms, CAM charges, and renewal dates into systems |
| Maintenance Ticket Orchestration | Property maintenance / FSM | Work order platforms, vendor management tools | Module pricing and multi-vendor setup | Diagnose, route, and schedule work orders end to end |
| Tenant Screening & Underwriting | Tenant screening / underwriting | Screening APIs, rental platforms, manual review teams | Per-screen fees and add-on compliance checks | Auto-analyze docs and render a lease decision draft |
| HOA Compliance & Violations | HOA management / compliance | HOA software, manual notices, legal ops | Module pricing and notice workflows | Ingest photos/rules and draft violations and escalations |
| KYC/AML Onboarding Agent | KYC/AML / CLM | Persona, Sumsub, Alloy, ComplyAdvantage, Fenergo | Per-verification plus sales-led enterprise pricing | Normalize evidence and produce auditable case memos |
| Loan Origination Underwriting | Mortgage underwriting / LOS | LOS suites, document AI, manual underwriters | Per-loan or enterprise pricing, services burden | Extract financials and draft pre-approval support |
| Portfolio Rebalancing Reporting | Wealth reporting / client comms | Portfolio reporting tools, advisor tech | Seat and enterprise pricing | Generate personalized portfolio narratives from raw data |
| Audit & Tax Document Synthesis | Audit prep / tax workflow | Tax prep tools, document synthesis, bookkeeping | Services-heavy, seasonal labor costs | Turn receipts and PDFs into audit-ready schedules |
| Bid & RFP Response Automation | Proposal / RFP tools | RFP software, knowledge bases, proposal teams | Seat plus services and content ops | Draft answers from historic wins and source content |
| Commission Dispute Resolution | Commission management / sales ops | Commission platforms, finance ops | Module pricing and manual dispute work | Reconcile compensation rules against CRM source data |
| CRM Data Hygiene & Auto-Logging | Conversation intelligence / CRM hygiene | Sales enablement, CRM automation, call recording | Seat and add-on pricing | Auto-fill CRM fields and next steps from call data |
| Deal Desk Pricing Approvals | CPQ / deal desk | CPQ suites, pricing governance tools | Seat/module pricing and approval workflow setup | Check margin, discount, and policy before approval |
| Vendor Catalog Enrichment | PIM / product content | PIM, content syndication, merchandising tools | Seat and data-enrichment pricing | Rewrite supplier specs into sellable product listings |
| Dynamic Competitor Pricing Agent | Repricing / ecommerce pricing | Repricing tools, marketplace intelligence | Per-SKU and enterprise pricing | Scrape rivals and adjust price to protect floor margin |
| Influencer Campaign Orchestration | Influencer marketing platforms | Creator tools, outreach CRMs, agencies | Seat, campaign, and services pricing | Scout, negotiate, track, and execute campaigns autonomously |
| Returns & Refund Triage | CX returns / reverse logistics | Returns platforms, support tools, warehouse workflows | Per-return or module pricing | Review request, verify policy, and process refund/exchange |
| Retail Inventory Reconciliation | Inventory control / ERP recon | WMS/ERP tools, spreadsheet reconciliation | Enterprise software plus manual ops | Reconcile POS vs warehouse and trigger reorder actions |

## Market-Mapping Takeaway

Phase 2 follows the same pattern as phase 1:

- If the incumbent is a transaction rail, the wedge is the reasoning layer above it.
- If the incumbent is a module inside a suite, the wedge is a narrow workflow that exposes the module's operational drag.
- If the incumbent is a services team, the wedge is to compress the handoff and turn the work into an auditable workflow.

