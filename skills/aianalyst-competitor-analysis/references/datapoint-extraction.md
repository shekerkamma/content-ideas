# Datapoint Extraction Guide

Use this guide when turning crawled competitor research into structured evidence rows. The goal is not just to collect quotes; the goal is to extract comparable datapoints that can support scoring, charts, battlecards, proof gaps, and narrative claims.

## Extraction Passes

Run extraction in four passes over each raw source:

1. **Entity pass:** identify company/product, customer names, partners, systems, integrations, analysts, regions, industries, buyer personas, and source owner.
2. **Metric pass:** extract numeric or measurable claims with units, baselines, dates, and comparison language.
3. **Capability pass:** extract categorical proof such as features, certifications, deployment model, AI agent capability, integrations, workflow coverage, and governance.
4. **Story pass:** tag each useful claim to a storyboard use: heatmap, threat priority, battlecard, proof gap, datapoints slide, roadmap, pricing, consulting/SI implications, or recommendation.

Do not stop at the first useful fact from a source. A single case study or pricing page can produce many evidence rows.

## Datapoint Families

### ROI / Financial

Extract:

- cost savings, revenue lift, payback period, ROI %, TCO, implementation cost, subscription price, services cost, seat price, platform fee, contract size, ARR, valuation, funding, headcount, customer count
- language such as `saved`, `reduced cost`, `ROI`, `payback`, `revenue`, `pipeline`, `profit`, `cost to serve`, `lower TCO`

Normalize:

- percentages as numeric percent
- money with currency and period when stated
- funding rounds with amount, date, lead investor, and round type
- pricing with unit such as user/month, tenant/month, implementation fee, annual platform fee

Reject or label low confidence:

- vague `significant savings` without amount
- unverifiable market-size claims without source basis

### Time / Velocity

Extract:

- onboarding time, implementation duration, time-to-value, deployment time, go-live time, resolution time, cycle time, setup time, configuration time, migration duration
- language such as `faster`, `same day`, `weeks to days`, `reduced from`, `accelerated`, `time-to-value`

Normalize:

- convert days/weeks/months to a canonical unit when useful
- preserve before/after values and baseline when stated
- separate absolute duration from percentage improvement

### Support Productivity

Extract:

- ticket deflection, response time, resolution time, support volume, self-service rate, CSAT/NPS, onboarding support load, implementation manager capacity, customer success workload
- language such as `tickets`, `support`, `deflection`, `response`, `resolution`, `self-serve`, `CSAT`, `NPS`

Normalize:

- percentages as percent
- response/resolution times in hours or days
- customer/team capacity as counts

### Trust / Compliance / Enterprise Readiness

Extract:

- SOC 2, ISO 27001, HIPAA, GDPR, SSO/SAML, SCIM, RBAC, audit logs, data residency, encryption, private cloud, VPC, on-prem, security reviews, procurement fit
- customer logos and enterprise brands when they indicate trust, but label as logo proof rather than performance proof

Normalize:

- binary certifications as `metric_value=1`, `metric_unit=binary`, `metric_name=<certification>`
- dated certification or trust-page claim when date is available

### AI / Automation

Extract:

- AI agents, copilots, workflow automation, browser automation, RPA, generated playbooks, knowledge graphs, LLM integration, autonomous setup/configuration, validation loops, human-in-the-loop controls
- language such as `agent`, `AI`, `automation`, `copilot`, `workflow`, `orchestration`, `knowledge graph`, `auto-configure`, `validate`

Normalize:

- classify as `assistive`, `workflow automation`, `agentic execution`, or `governed automation`
- record whether proof is demo/claim, case study, docs, or production customer evidence

### Quality / Risk

Extract:

- error reduction, compliance error reduction, rework reduction, implementation accuracy, SLA, uptime, auditability, QA, rollback, governance, exception handling
- language such as `error`, `risk`, `quality`, `audit`, `accuracy`, `compliance`, `rework`, `SLA`, `uptime`

Normalize:

- keep both risk type and affected workflow
- mark whether claim is measured, procedural, or feature-based

### Distribution / Market Presence

Extract:

- funding, investors, acquisition, parent company, partner ecosystem, marketplace listings, integration count, app store reviews, G2 reviews, analyst mentions, community footprint, geographic presence, customer segments

Normalize:

- review counts as counts plus source/date
- ratings as score plus scale
- integrations as count when stated, or categorical list when not
- analyst placement as category/year/source

### Pricing / Packaging

Extract:

- public tiers, seat pricing, minimum contracts, free trials, enterprise packaging, add-ons, usage-based fees, implementation fees, services dependencies

Normalize:

- price, currency, billing period, unit, and whether public/list/custom
- distinguish software fee from professional-services/implementation fee

### Consulting / SI Benchmark

Extract:

- Accenture/BCG/Deloitte/McKinsey/IBM positioning, transformation offers, implementation accelerators, AI delivery factories, managed services, industry playbooks, ecosystem partnerships, productivity claims

Normalize:

- classify as `buyer expectation`, `services substitute`, `partner threat`, or `route-to-market force`
- do not compare consulting claims as if they are SaaS product metrics unless the source supports it

## Extraction Cues

Search each source for:

```text
%, percent, x, times, faster, slower, reduced, increased, saved, cut, improved,
days, weeks, months, hours, minutes, same day, time-to-value, onboarding,
implementation, go-live, support, tickets, response, resolution, CSAT, NPS,
ROI, payback, cost, revenue, pricing, tier, user/month, annual, ARR, funding,
Series, valuation, customers, users, seats, integrations, partners, SOC 2,
ISO, HIPAA, GDPR, SSO, RBAC, audit, AI, agent, automation, workflow, copilot
```

Use semantic extraction too: many useful datapoints do not contain obvious metric words.

## Normalization Rules

- Preserve the original text in `claim_text`.
- Store extracted numeric value in `metric_value` only when the source gives a number or a direct calculation from stated numbers is trivial and documented.
- Put the original unit in `metric_unit`; add normalized units in `notes` when converted.
- Keep `baseline` and `comparison` separate from the metric value.
- Use `published_at` for the source publication date and `retrieved_at` for crawl date.
- If a claim has multiple metrics, create multiple rows with the same source URL and different `claim_id`s.
- If the same claim appears in several syndicated sources, keep the strongest/original source and mark duplicates in `notes`.

## Confidence Rules

High confidence:

- official source with a specific measurable claim
- public filing or audited/report source
- internal dataset with clear grain and source tieout
- trust/compliance page for a binary certification

Medium confidence:

- vendor-published case study with named customer and specific metric
- credible analyst/review source with clear date and category
- pricing page with public tiers but custom enterprise caveats

Low confidence:

- undated claim
- vague marketing claim
- scraped snippet without full source context
- user review without sample size/context
- unsupported third-party summary

## Rejection Rules

Do not extract as a datapoint:

- adjectives without evidence: `best`, `leading`, `seamless`, `robust`
- unsourced claims copied from another page
- estimates that cannot be traced to a source
- duplicate quotes unless they add a new metric/source type
- irrelevant SEO boilerplate

Keep rejected-but-interesting items in `working/rejected-datapoints.md` when they explain a research gap.

## Promotion To Story

Promote a datapoint into the main PPTX/HTML storyline when it meets at least one condition:

- differentiates the target from a competitor arena
- changes a score or threat priority
- quantifies a buyer pain, outcome, or proof gap
- reveals incumbent compression risk
- supports a recommended roadmap/proof plan
- represents a missing datapoint that buyers will ask for

Do not hide promoted datapoints only in an appendix. They should appear in heatmaps, evidence coverage slides, battlecards, datapoints tabs, charts, or recommendation sections.

## Required Datapoint Summary

Every run should produce a summary table with:

| Summary | Required View |
|---|---|
| Total evidence rows | Count of all ledger rows |
| Numeric evidence rows | Rows with `metric_value` |
| Rows by metric family | ROI, time, support, trust, AI, quality, distribution, pricing |
| Rows by competitor | Coverage balance |
| High-confidence rows | Proof suitable for main claims |
| Vendor-published rows | Bias indicator |
| Primary-source rows | Source quality indicator |
| Story-promoted rows | Rows used in PPTX/HTML |
| Missing datapoints | Gaps to search again |

If the user says the datapoints are not reflected, rerun this summary and compare `story-promoted rows` against actual PPTX/HTML content before revising.
