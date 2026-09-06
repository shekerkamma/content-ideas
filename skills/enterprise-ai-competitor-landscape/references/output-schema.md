# Output Schema

## Company Universe Table

Required columns:

| Column | Meaning |
|---|---|
| company | Normalized company name |
| url | Official website |
| primary_category | One category from the skill taxonomy |
| secondary_categories | Optional additional categories |
| positioning | One-sentence market positioning |
| target_buyer | Primary buyer/user |
| product_type | Platform, API, app, infra, service, etc. |
| funding_stage | Public, bootstrapped, seed, Series A, etc. |
| latest_funding | Amount/date if public |
| headcount | Source-backed estimate or `not verified` |
| pricing_model | Seat, usage, enterprise custom, open source, services, etc. |
| public_pricing | yes/no/partial |
| deployment_model | SaaS, VPC, self-hosted, API, hybrid |
| enterprise_readiness | high/medium/low with rationale |
| moat | Why the company may defend its position |
| risk | Main vulnerability |
| sources | URLs or source IDs |
| confidence | high/medium/low |

## Market Map

For each category:

- category definition
- representative companies
- buyer problem
- maturity level
- consolidation pressure
- likely winners
- likely losers

## Quadrant Analysis

For each category or for the whole market:

- quadrant name
- companies in quadrant
- placement rationale
- confidence

Use unofficial Gartner-style language.

## Funding Analysis

Required sections:

- funding concentration by category
- most-funded companies
- underfunded but strategically important companies
- public-company incumbents vs startups
- funding momentum
- investor pattern notes

## Pricing Analysis

Required sections:

- pricing model by category
- transparent vs opaque pricing
- enterprise custom pricing zones
- usage-based pricing risks
- buyer friction created by pricing
- disruptive pricing opportunities

## SWOT

Create SWOT at category level, not only company level:

- strengths
- weaknesses
- opportunities
- threats

## White Space

For each white-space opportunity:

- unmet buyer problem
- why incumbents underserve it
- category adjacency
- target buyer
- recommended wedge
- build difficulty
- go-to-market difficulty
- proof needed

## Competitive Threat Analysis

Threat types:

- incumbent platform expansion
- foundation model commoditization
- open-source substitution
- cloud-provider bundling
- vertical SaaS embedding AI
- consulting/services capture
- governance/security blocker

## Strategic Recommendations

Each recommendation must include:

- recommendation
- rationale
- target category
- target buyer
- what to build or avoid
- proof milestone
- risk
- confidence
