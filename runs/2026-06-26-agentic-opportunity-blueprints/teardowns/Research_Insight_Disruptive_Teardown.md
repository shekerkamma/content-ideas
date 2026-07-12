---
status: reviewed
use_case: "Research & Insight Agent"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Research & Insight Agent Disruptive Competitor Teardown

## Market Frame
- Workflow: synthesize market/customer research into executive briefings.
- Target buyer: strategy, product, and research teams.
- Existing spend category: research tooling and premium data portals.
- Incumbent economic model: per-seat licensing and expensive portals.
- Agentic wedge: synthesis engine that democratizes insights without requiring a research seat.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| Qualtrics | XM / research | Enterprises | $20k-$100k+/yr | Admin-heavy setup | Proprietary VoC data | Synthesis bottleneck |
| AlphaSense | Market intelligence | Analysts | $15k-$60k/user/yr | Expensive and heavy | Huge licensed corpus | Seat scarcity |
| Gartner / Forrester | Analyst portals | Execs | Per-seat portal access | Procurement-heavy | Brand authority | CYA-style access |
| SurveyMonkey Enterprise | Survey tooling | Teams | Enterprise pricing | Ops and admin work | Survey capture | Not a synthesis engine |
| Medallia | Experience management | Enterprises | Enterprise pricing | Platform management | Historical customer data | License scarcity |

## Direct Threats
1. AlphaSense and Qualtrics.
2. Gartner/Forrester portals and Medallia.

## Pricing Friction
- Seats are expensive and scarce.
- Feature additions are often paywalled.

## Onboarding And Workflow Friction
- Administrators maintain logic and integrations.
- Analysts still need to synthesize and format findings manually.

## What Not To Build
- Do not become a proprietary data vendor or survey engine.

## What To Keep
- Existing source corpora and research data.

## Agentic Wedge
- Wedge statement: read the source corpus and output a ready-to-present briefing.
- Why it wins: removes the synthesis bottleneck and democratizes access.
- Why now: teams want faster, broader access to insights.

## Blueprint Inputs
- Scope implication: one research corpus and one briefing format.
- Architecture implication: synthesis engine over existing corpora.
- Build-vs-buy implication: keep the corpus sources; build the synthesis layer.
- ROI implication: less analyst time and lower portal spend.
- QA/deployment implication: exact citation mapping and zero hallucination are mandatory.

## Source Notes
- Source teardown in `source/Research_Insight_Competitor_Teardown.md`.
