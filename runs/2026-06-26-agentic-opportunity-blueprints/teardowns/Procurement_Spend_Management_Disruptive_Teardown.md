---
status: reviewed
use_case: "Procurement & Spend Management"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Procurement & Spend Management Disruptive Competitor Teardown

## Market Frame
- Workflow: P2P automation, supplier onboarding, and spend management.
- Target buyer: procurement, finance, and AP teams.
- Existing spend category: procurement suites and supplier networks.
- Incumbent economic model: opaque enterprise pricing and six-figure implementation fees.
- Agentic wedge: overlay that chases documents, extracts vendor details, and resolves exceptions without becoming the ERP.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| SAP Ariba | Procurement suite | Enterprise procurement | Opaque enterprise | Supplier onboarding pain | ERP integration | Clunky UX |
| Coupa | Spend management | Enterprise procurement | Opaque enterprise | Rigid workflows | Strong network | Human middleware remains |

## Direct Threats
1. SAP Ariba and Coupa.

## Pricing Friction
- Six-figure setup and opaque pricing are common.
- Vendor onboarding still needs manual chasing.

## Onboarding And Workflow Friction
- Endless email chains for tax and banking details.
- Integrations fail and humans become middleware.

## What Not To Build
- Do not build a new ERP or financial system of record.

## What To Keep
- Existing ERP and supplier databases.

## Agentic Wedge
- Wedge statement: autonomous vendor chasing and document extraction on top of existing P2P systems.
- Why it wins: usage-based scaling with natural-language integration.
- Why now: procurement teams want less manual reconciliation.

## Blueprint Inputs
- Scope implication: one supplier onboarding flow.
- Architecture implication: document extraction plus workflow orchestration.
- Build-vs-buy implication: keep ERP and P2P backbone; build the agentic layer.
- ROI implication: lower onboarding labor and fewer manual interventions.
- QA/deployment implication: vendor data integrity and reconciliation are key.

## Source Notes
- Source teardown in `source/Procurement_Competitor_Teardown.md`.
