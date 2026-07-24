---
status: reviewed
use_case: "Commission Dispute Resolution"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Commission Dispute Resolution Disruptive Competitor Teardown

## Market Frame
- Workflow: reconcile commission plans against closed-won data, explain payouts, and resolve disputes.
- Target buyer: sales ops, finance, and revops.
- Existing spend category: SPM suites and commission tooling.
- Incumbent economic model: per-user pricing plus significant implementation and maintenance.
- Agentic wedge: agent that reads comp PDFs and CRM data to resolve disputes without a giant SPM project.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| Xactly | SPM suite | Enterprise revops | $40-$60+/user/mo plus implementation fees | Complex rules and heavy setup | Strong enterprise scale | Admin burden and ticket dependency |
| CaptivateIQ | Commission platform | Mid-market / enterprise | ~$35-$55/user/mo plus implementation | Spreadsheet-like but still complex | Modern UX | Still requires manual configuration |
| Spiff | Commission platform | Mid-market | ~$75/user/mo plus implementation | Rule design and data loading | Salesforce adjacency | Admin overhead |
| Varicent / Performio | SPM | Enterprise | Sales-led | Specialized configuration | Enterprise control | Heavy implementation burden |

## Direct Threats
1. Xactly and CaptivateIQ.
2. Spiff, Varicent, and Performio.

## Pricing Friction
- License fees are only part of the cost.
- Implementation and maintenance can dwarf the software spend.
- Teams often need dedicated admins or engineers.

## Onboarding And Workflow Friction
- Rule builders are complicated and brittle.
- Reps and managers still ask why payouts were made.
- Minor plan changes often require vendor support.

## What Not To Build
- Do not create a standalone SPM platform.
- Do not require custom coding to change a bonus tier.

## What To Keep
- CRM source data, comp policy PDFs, and audit trails.
- Human approval for disputed or exceptional payouts.

## Agentic Wedge
- Wedge statement: reconcile comp plans and sales data in natural language and output an explanation or resolution.
- Why it wins: removes Excel labor and support tickets.
- Why now: mid-market teams want relief from enterprise SPM complexity.

## Blueprint Inputs
- Scope implication: one comp plan family and one sales data source.
- Architecture implication: policy document reader plus CRM reconciliation worker.
- Build-vs-buy implication: keep the source systems, build the dispute resolver.
- ROI implication: fewer disputes and lower admin cost.
- QA/deployment implication: payout traceability and calculation tests.

## Source Notes
- Source teardown in `source/Commission_Dispute_Resolution_Competitor_Teardown.md`.
