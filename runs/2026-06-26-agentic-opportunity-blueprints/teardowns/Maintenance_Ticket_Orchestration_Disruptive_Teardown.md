---
status: reviewed
use_case: "Maintenance Ticket Orchestration"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Maintenance Ticket Orchestration Disruptive Competitor Teardown

## Market Frame
- Workflow: receive tenant complaints, diagnose, dispatch vendors, and follow up on work orders.
- Target buyer: property management and facilities teams.
- Existing spend category: PMS and maintenance tracking tools.
- Incumbent economic model: per-unit or per-month SaaS pricing.
- Agentic wedge: vendor-native communication layer that follows through until the job closes.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| AppFolio | PMS | Property managers | ~$280/mo+ | Vendor adoption friction | Portal ownership | Over-complicated modules |
| Buildium | PMS | Smaller portfolios | ~$62/mo + unit fees | Setup and call center add-ons | Broad fit | Still needs manual dispatch |
| Property Meld | Maintenance platform | Property managers | ~$1.60/unit/mo | Vendor portal friction | Specialization | Portal dependency |

## Direct Threats
1. AppFolio and Property Meld.
2. Buildium for smaller portfolios.

## Pricing Friction
- Per-unit and add-on pricing stacks up.
- Vendors and managers still bear the real operating cost.

## Onboarding And Workflow Friction
- Vendors refuse to adopt portals.
- Tickets fall through the cracks.

## What Not To Build
- Do not force vendors into a new app or portal.

## What To Keep
- Existing PMS and tenant portal systems.

## Agentic Wedge
- Wedge statement: SMS/email-native dispatcher with photo analysis and follow-up.
- Why it wins: bypasses vendor portal adoption friction.
- Why now: property managers need closer to zero-touch resolution.

## Blueprint Inputs
- Scope implication: one maintenance category and one portfolio type.
- Architecture implication: multimodal triage plus vendor-native follow-up.
- Build-vs-buy implication: keep the PMS; build the orchestration agent.
- ROI implication: fewer ticket fall-throughs and lower dispatch labor.
- QA/deployment implication: vendor follow-up and issue classification tests are key.

## Source Notes
- Source teardown in `source/Use_Case_35_Competitor_Teardown.md`.
