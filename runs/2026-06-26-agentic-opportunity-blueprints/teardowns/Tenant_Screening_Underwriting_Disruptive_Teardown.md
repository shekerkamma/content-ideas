---
status: reviewed
use_case: "Tenant Screening & Underwriting"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Tenant Screening & Underwriting Disruptive Competitor Teardown

## Market Frame
- Workflow: analyze applicant documents and produce a lease decision draft.
- Target buyer: property managers and rental operators.
- Existing spend category: screening APIs and property management suites.
- Incumbent economic model: per-screen fees plus bundled subscriptions.
- Agentic wedge: explainable screening and exception handling layer that sits on top of existing FCRA-compliant data feeds.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| RealPage | Enterprise leasing | Large multifamily | Subscription + transactional fees | Compliance training and setup | Integrated funnel | Black-box risk |
| AppFolio | PMS / screening | Property managers | Built-in screening | Ecosystem setup | Integrated experience | Not always transparent |
| TransUnion SmartMove | Screening | Independent landlords | $25-$48/applicant | Application and dispute setup | Easy access | Black-box denials |

## Direct Threats
1. RealPage and AppFolio.
2. TransUnion SmartMove.

## Pricing Friction
- Per-screen and transactional fees are visible.
- Enterprise contracts hide the true cost.

## Onboarding And Workflow Friction
- False positives and opaque denials frustrate operators and applicants.
- Compliance training is required.

## What Not To Build
- Do not become a consumer reporting agency.

## What To Keep
- Existing screening data feeds and leasing systems.

## Agentic Wedge
- Wedge statement: explainable AI decisions plus proactive exception handling.
- Why it wins: reduces dispute friction and improves applicant transparency.
- Why now: operators want screening without black-box pain.

## Blueprint Inputs
- Scope implication: one applicant class and one screening flow.
- Architecture implication: orchestrated data feeds and explainable synthesis.
- Build-vs-buy implication: keep the CRA/data sources; build the reasoning layer.
- ROI implication: less manual review and faster applicant throughput.
- QA/deployment implication: FCRA compliance and appeal handling are critical.

## Source Notes
- Source teardown in `source/Use_Case_36_Competitor_Teardown.md`.
