---
status: reviewed
use_case: "Legacy-IT Modernization (NL→SAP)"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Legacy-IT Modernization (NL->SAP) Disruptive Competitor Teardown

## Market Frame
- Workflow: expose legacy ERP and mainframe functionality through natural language and automate modernization tasks.
- Target buyer: enterprise IT transformation and SAP teams.
- Existing spend category: consulting firms, iPaaS, and migration software.
- Incumbent economic model: multi-million-dollar consulting engagements.
- Agentic wedge: NL overlay and code translation layer that avoids full-system replacement.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| Accenture / PwC / Deloitte | Consulting | Enterprise IT | Multi-million engagements | Readiness assessments and roadmaps | Deep enterprise context | Human middleware |
| SAP Signavio | Process mining | SAP teams | Sales-led / hidden | Process mapping complexity | Strong process visibility | Heavy project work |
| Boomi | iPaaS | Integration teams | Consumption / node pricing | Integration setup | Connector ecosystem | Not a migration brain |
| SNP Group | SAP transformation | SAP teams | Sales-led | Data transformation complexity | SAP focus | Services-heavy |
| Panaya | Change intelligence | SAP teams | Sales-led | Readiness and test setup | Change analysis | Still a project-heavy tool |

## Direct Threats
1. Big 4 consultancies and Boomi.
2. SAP Signavio, SNP, and Panaya.

## Pricing Friction
- Consulting engagements are expensive and slow.
- Software pricing is often hidden behind sales calls.

## Onboarding And Workflow Friction
- Readiness assessments can take months.
- Custom ABAP/COBOL debt creates migration drag.

## What Not To Build
- Do not replace SAP as the system of record.

## What To Keep
- SAP and existing legacy systems.

## Agentic Wedge
- Wedge statement: use NL over legacy systems and automatically translate legacy logic into modern services.
- Why it wins: immediate value without a giant migration.
- Why now: enterprises are stuck between old systems and expensive consulting.

## Blueprint Inputs
- Scope implication: one legacy workflow or SAP module.
- Architecture implication: read-only overlay plus code translation assistance.
- Build-vs-buy implication: keep the system of record; build the modernization assistant.
- ROI implication: reduced consulting spend and faster process discovery.
- QA/deployment implication: compatibility and data governance are essential.

## Source Notes
- Source teardown in `source/Legacy_IT_modernization_Competitor_Teardown.md`.
