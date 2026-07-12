---
status: reviewed
use_case: "Enterprise Knowledge Search"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Enterprise Knowledge Search Disruptive Competitor Teardown

## Market Frame
- Workflow: search across company knowledge, answer questions, and synthesize live context.
- Target buyer: internal ops, knowledge management, and IT/productivity teams.
- Existing spend category: enterprise search and knowledge management tools.
- Incumbent economic model: per-seat licenses and enterprise commitments.
- Agentic wedge: synthesis layer that sits on top of existing silos and answers dynamically.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| Coveo | Enterprise search | Enterprise IT | Opaque enterprise pricing | Heavy integration | Strong search scale | Expensive and complex |
| Sinequa | Enterprise search | Large enterprise | Sales-led | Deep governance setup | Complex-environment fit | Heavy implementation |
| Guru | Knowledge mgmt | Mid-market / enterprise | Per-seat / sales-led | Content curation and upkeep | Useful policy/wiki layer | Content rot |
| Glean | Workplace search | Enterprise | $50-$75+/user/month, large annual deals | 100+ seats and integration work | Strong modern search UX | Per-seat tax and setup cost |
| Elastic Enterprise Search | Search platform | Engineering teams | Enterprise / custom | Requires engineering resources | Highly customizable | Not zero-setup |

## Direct Threats
1. Glean and Coveo.
2. Sinequa and Guru.

## Pricing Friction
- Per-seat pricing gates access and discourages company-wide use.
- Annual contracts and minimum seats are common.

## Onboarding And Workflow Friction
- Integration complexity is high.
- Manual curation causes content rot.

## What Not To Build
- Do not build another wiki or database.

## What To Keep
- Existing Drive, Slack, Jira, and policy sources.

## Agentic Wedge
- Wedge statement: synthesize answers from live data without forcing a migration.
- Why it wins: removes content rot and kills seat gating.
- Why now: buyers want all-company access, not a licenseed search silo.

## Blueprint Inputs
- Scope implication: one knowledge domain and one connector set.
- Architecture implication: semantic graph over existing silos.
- Build-vs-buy implication: buy the source systems, build the synthesis layer.
- ROI implication: lower per-seat spend and less admin curation.
- QA/deployment implication: security trimming and connector health are essential.

## Source Notes
- Source teardown in `source/EnterpriseKnowledgeSearch_Competitor_Teardown.md`.
