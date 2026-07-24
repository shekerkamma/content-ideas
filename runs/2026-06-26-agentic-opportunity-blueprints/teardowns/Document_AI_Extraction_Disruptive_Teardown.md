---
status: reviewed
use_case: "Document AI / Extraction"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Document AI / Extraction Disruptive Competitor Teardown

## Market Frame
- Workflow: extract structured data from invoices, forms, contracts, and messy email attachments.
- Target buyer: operations, finance, and document-processing teams.
- Existing spend category: OCR and IDP platforms.
- Incumbent economic model: page or volume pricing plus services-heavy setup.
- Agentic wedge: LLM-based extraction that understands meaning, not pixel zones.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| ABBYY | OCR/IDP | Enterprise ops | Page/capacity licensing | Template setup and add-ons | High-speed batch processing | Template hell |
| Kofax | Capture | Enterprise ops | Custom enterprise pricing | Rule building and language packs | Legacy integration | Heavy implementation |
| Ephesoft | Capture | Enterprise ops | Enterprise pricing | Configuration and maintenance | Capture workflows | Rigid layouts |
| IBM Datacap | OCR/IDP | Enterprise ops | Enterprise pricing | Specialist setup | Enterprise footprint | Old-school extraction |
| Automation Anywhere | Document automation | Enterprise ops | Enterprise pricing | Automation configuration | RPA adjacency | Not semantic by default |

## Direct Threats
1. ABBYY and Kofax.
2. Ephesoft and IBM Datacap.

## Pricing Friction
- Volume pricing and services are expensive.
- Add-ons like language packs raise TCO.

## Onboarding And Workflow Friction
- Template shifts break extraction.
- New document types need specialist rules.

## What Not To Build
- Do not become the ERP or downstream system of record.

## What To Keep
- Existing ERP/ECM systems.

## Agentic Wedge
- Wedge statement: extract data from messy documents without templates.
- Why it wins: kills setup costs and handles unstructured chaos.
- Why now: businesses want faster onboarding of new document types.

## Blueprint Inputs
- Scope implication: one document class or workflow.
- Architecture implication: secure upload plus deterministic JSON output.
- Build-vs-buy implication: buy the downstream system, build the extraction layer.
- ROI implication: lower services cost and faster time to value.
- QA/deployment implication: confidence scores and edge-case regression tests are mandatory.

## Source Notes
- Source teardown in `source/DocumentAI_Competitor_Teardown.md`.
