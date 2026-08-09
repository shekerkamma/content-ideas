---
name: enterprise-ai-competitor-landscape
description: Build a sourced Enterprise AI competitor landscape across 100-150 companies. Use this when asked for Enterprise AI market maps, Gartner-style quadrants, funding analysis, pricing analysis, SWOT, white-space analysis, competitive threat analysis, or strategic recommendations across AI company categories.
metadata:
  legacy-frontmatter:
    triggers:
    - competitor landscape
    - enterprise ai companies
    - enterprise ai market map
    - gartner magic quadrant
    - funding analysis
    - pricing analysis
    - ai competitive analysis
---

# Enterprise AI Competitor Landscape

## Goal

Produce a sourced market-intelligence pack for 100-150 Enterprise AI companies, classified by category and converted into executive-ready strategy artifacts.

This is not a quick competitor list. Treat it as a research pipeline.

## Required Inputs

- Scope: global or region-specific.
- Time horizon: current snapshot or trend over a defined period.
- Audience: founder, investor, enterprise buyer, consultant, or internal strategy team.
- Output format: markdown report, spreadsheet/CSV, PPTX deck, or all three.

If these are missing and the user asks for a full run, make reasonable defaults:

- Scope: global Enterprise AI.
- Time horizon: current as of today.
- Audience: strategy/market-facing executive.
- Output: markdown report plus CSV-ready company table; PPTX only if requested.

## Source Rules

Funding, pricing, headcount, company status, and category positioning are current facts. Verify them with web research before finalizing.

Use primary or high-quality sources where available:

- Company websites and pricing pages.
- Product documentation.
- SEC filings or investor relations for public companies.
- Crunchbase, PitchBook, Dealroom, CB Insights, or public funding announcements.
- Reputable tech/business media for funding and strategic moves.
- GitHub/docs for developer platform claims.

Do not fabricate missing pricing, funding, or headcount. Use `not public`, `unverified`, or `estimate` with source notes.

## Company Categories

Classify each company into one primary category and optional secondary categories:

- Foundation Models
- Infrastructure
- Agent Frameworks
- Enterprise Platforms
- AI Development Platforms
- AI Operations
- Vertical AI
- Knowledge Management
- Developer Platforms
- Observability
- Security
- Governance
- AI Consulting
- Managed Services

## Output Artifacts

Create the artifacts listed in [references/output-schema.md](references/output-schema.md).

Minimum deliverables:

1. Company universe table.
2. Category-level market map.
3. Gartner-style quadrant view.
4. Funding analysis.
5. Pricing analysis.
6. Category SWOT.
7. White-space analysis.
8. Competitive threat analysis.
9. Strategic recommendations.

## Research Workflow

1. Define scope and assumptions.
2. Build the initial company universe of 100-150 companies.
3. De-duplicate companies and normalize names.
4. Classify each company by primary and secondary category.
5. Collect sourced fields:
   - URL
   - category
   - positioning
   - product type
   - target buyer
   - funding/stage
   - approximate headcount when source-backed
   - pricing model
   - deployment model
   - moat
   - risks
6. Score companies for Gartner-style placement:
   - ability to execute
   - completeness of vision
   - enterprise readiness
   - developer traction
   - pricing transparency
   - integration depth
   - governance/security maturity
7. Build category-level analysis.
8. Identify white space and strategic recommendations.
9. Validate claims and mark confidence per section.

## Gartner-Style Quadrant Rules

Use "Gartner-style" or "quadrant-style" unless the output is explicitly not for publication. Do not claim it is an official Gartner Magic Quadrant.

Axes:

- X-axis: Completeness of vision.
- Y-axis: Ability to execute.

Quadrants:

- Leaders
- Visionaries
- Challengers
- Niche Players

Every placement needs a short rationale. If evidence is weak, mark placement as provisional.

## Pricing Analysis Rules

Separate pricing into:

- Public transparent pricing.
- Usage-based pricing.
- Seat-based pricing.
- Platform/enterprise custom pricing.
- Services/managed delivery pricing.
- Not public.

Never infer exact enterprise pricing from absence of public pricing. Use pricing model and qualitative pricing transparency score instead.

## Funding Analysis Rules

For private companies, record:

- latest known round
- date
- amount if public
- known investors if public
- total funding if source-backed

For public companies, use public-company status and relevant market position instead of startup funding round.

## QA Gates

Before final delivery:

- Confirm company count is within 100-150.
- Confirm every company has a primary category.
- Confirm every funding/pricing claim has a source or is explicitly marked unavailable.
- Confirm no inactive/wound-down company is presented as active without caveat.
- Confirm Gartner-style quadrants are labeled unofficial.
- Confirm strategic recommendations are tied to evidence, not generic AI hype.

## Failure Modes

Stop and report if:

- Current web research is unavailable.
- Fewer than 100 relevant companies can be sourced.
- Source quality is too weak for funding/pricing claims.
- The user asks for exact private-company data that is not public.

## Suggested Run Folder

Write runs to:

`runs/YYYY-MM-DD-enterprise-ai-competitor-landscape/`

Recommended structure:

```text
source/
working/
outputs/
outputs/company-universe.csv
outputs/market-map.md
outputs/quadrant-analysis.md
outputs/funding-analysis.md
outputs/pricing-analysis.md
outputs/swot.md
outputs/white-space.md
outputs/competitive-threats.md
outputs/strategic-recommendations.md
```
## Shared PPTX Visual Contract

Any PowerPoint output from this workflow must use the `pptx-visual-spec` behavioral overlay.
Create and validate `<run>/visual-spec.json` after evidence/story approval and pass it to the
selected direct deck builder. Competitive data, rankings, company claims, and logos may not
route to an image model.
