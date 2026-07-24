---
status: reviewed
use_case: "AI Shopping / Sales Consultant"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Guided Selling / CPQ Disruptive Competitor Teardown

## Market Frame
- Workflow: configure products, guide quotes, and generate pricing artifacts.
- Target buyer: sales ops, revenue ops, and commerce teams.
- Existing spend category: CPQ and guided-selling tools.
- Incumbent economic model: per-seat licensing plus SI-heavy implementations.
- Agentic wedge: conversational quoting engine that computes from pricing logic without a massive visual rules builder.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| Salesforce CPQ / Revenue Cloud | CPQ | Enterprise sales ops | Seat + SI contracts | Massive migration effort | CRM integration | Over-architected |
| Conga CPQ | CPQ | Enterprise sales ops | Enterprise pricing | Complex configuration | Quote generation | Heavy implementation |
| Oracle CPQ | CPQ | Enterprise sales ops | Enterprise pricing | Custom contracts | Pricing governance | Rigid workflow |
| DealHub | CPQ / deal room | Mid-market/enterprise | Per-user pricing | Expensive at scale | Agile deal room | Still admin heavy |

## Direct Threats
1. Salesforce CPQ and DealHub.
2. Conga and Oracle CPQ.

## Pricing Friction
- Multi-year contracts and SI costs are common.
- Pricing logic changes require admins or consultants.

## Onboarding And Workflow Friction
- Quote calculations can be slow.
- Reps abandon the tool and use spreadsheets.

## What Not To Build
- Do not build a massive visual rule-builder.

## What To Keep
- CRM, catalog, and pricing logic sources.

## Agentic Wedge
- Wedge statement: reps describe the deal in natural language and the agent generates the quote.
- Why it wins: destroys SI implementation drag and admin bottlenecks.
- Why now: sales teams want speed without CPQ fatigue.

## Blueprint Inputs
- Scope implication: one product catalog and one pricing motion.
- Architecture implication: pricing logic interpreter plus PDF output.
- Build-vs-buy implication: keep pricing source systems; build conversational orchestration.
- ROI implication: less deal friction and lower admin cost.
- QA/deployment implication: margin guardrails and pricing accuracy matter.

## Source Notes
- Source teardown in `source/GuidedSelling_CPQ_Competitor_Teardown.md`.
