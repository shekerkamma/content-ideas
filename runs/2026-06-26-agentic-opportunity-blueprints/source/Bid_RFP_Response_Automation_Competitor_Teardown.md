# OSINT Source Map & Methodology
- **Sources:** Reddit (r/sales, r/Proposal), Sifthub, AutoRFP.ai
- **Methodology:** Targeted Reddit to uncover raw user sentiment on "shelfware" risks and onboarding friction. Used third-party pricing aggregators since exact pricing for RFP tools is deliberately hidden behind enterprise sales walls to force qualification calls.

## Company Overview
- **Loopio:** Mid-to-large enterprise scale. Positioned as an RFP response and knowledge management platform.
- **Responsive (formerly RFPIO):** Large enterprise scale. Positioned as a strategic response management platform.
- **Other Incumbents:** Qvidian, Ombud, Proposal Software.

## Product Teardown
- **Top 3 Features:** Centralized content library, AI-assisted answer suggestions (matching Q&A), workflow approvals & collaboration.
- **Pricing Tiers:** Custom enterprise quotes. Loopio typically starts at ~$20k/year for base plans (e.g., 10 seats); Responsive ranges $7k-$28k+ depending on features and AI modules. Both use heavy per-seat models and charge extra for crucial CRM integrations.
- **Onboarding Friction:** Massive heavy lifting required. Users complain about the painful process of cleaning up existing policies and building the "single source of truth."

## Where They Are Strong
- Sticky workflow approval engines for large teams. Robust integrations for enterprise ecosystems (if you pay for the add-ons).

## Where They Are Weak
- **Maintenance Burden:** Libraries get stale quickly, rendering the AI useless. Often becomes "shelfware" without a dedicated manager.
- **Weak AI Matching:** Their legacy AI matching requires significant human intervention and struggles to draft complete responses from scratch.

## Disruptive Strategy
- **Direct Threats:** Loopio and Responsive.
- **Table Stakes:** Chrome extension/easy access, MS Word/Excel parsing, basic content search.
- **What We Must NOT Do:** Do not force the user to build and manually maintain a new centralized knowledge base. We should dynamically ingest existing Google Drive/Confluence/Notion docs.
- **3 Specific Gaps (The Agentic Wedge):**
  1. Eliminate the "library maintenance" tax via real-time ingestion of existing company assets.
  2. Subvert the $20k entry cost with a usage-based or lighter per-seat model that scales easily for small teams.
  3. Replace manual matching with advanced generative AI that drafts the full response, rather than just suggesting a snippet that needs heavy editing.
