# OSINT Source Map & Methodology
- **Sources:** Reddit (r/salesforce, r/sales), Tropic, Vendr
- **Methodology:** Mined Reddit to reveal rep frustration with "glorified overlays" and aggressive, inaccurate data association. Sourced vendor pricing models from procurement trackers to understand the true Total Cost of Ownership (TCO) beyond list prices.

## Company Overview
- **Gong:** Enterprise scale. Positioned as the premier revenue intelligence and conversational AI platform.
- **Clari:** Enterprise scale. Positioned as a purpose-built revenue platform and forecasting engine.
- **People.ai:** Mid-to-enterprise. Positioned as an enterprise revenue intelligence and data capture tool.
- **Other Incumbents:** Salesforce Einstein Activity Capture (EAC), Dooly.

## Product Teardown
- **Top 3 Features:** Automatic email/calendar syncing, conversational intelligence (call recording/transcription), pipeline forecasting/deal health scores.
- **Pricing Tiers:** Opaque platform fees ($5k-$50k+) plus $1k-$1.6k per user/year for Gong. Clari often reaches six figures. High implementation costs.
- **Onboarding Friction:** Setting up sync rules, dealing with historical data, and managing the change management of reps adapting to a new interface.

## Where They Are Strong
- Providing pipeline visibility to sales leadership. High-quality transcriptions and conversational analytics.

## Where They Are Weak
- **Rep Adoption:** Often viewed as "extra work" or a "big brother" tool. 
- **Data Association:** Aggressive data association (EAC syncing emails to the wrong opportunities). Non-queryable data silos.

## Disruptive Strategy
- **Direct Threats:** Gong and Clari.
- **Table Stakes:** Email/calendar ingestion, call transcription, basic CRM updating.
- **What We Must NOT Do:** Do not build a massive forecasting dashboard for VPs. Focus entirely on zero-touch execution for the individual contributor.
- **3 Specific Gaps (The Agentic Wedge):**
  1. Fix the "garbage in" problem by deploying a discrete agent that listens to calls and natively updates standard Salesforce fields (MEDDPICC) without requiring a separate UI.
  2. Eliminate the massive platform access fee ($50k+) by offering a lightweight, API-first orchestration layer that writes directly to the system of record.
  3. Provide perfect contextual association (unlike EAC) using LLMs to accurately map activity to the correct opportunity, solving the data clutter complaint.
