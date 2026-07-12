# Use Case One-Pager - Hermes Content Pipeline

## Clear-Cut Use Case

Hermes monitors curated AI/operator source clusters, ranks the best content opportunities, creates a source-grounded research brief, drafts an article package, and queues it for human editorial review.

## Buyer / Operator Problem

The operator cannot manually track every useful source, identify which topics matter, research each angle, and produce consistent business-facing content at the speed the market moves.

## Core Value

Reduce content production from manual source scanning and blank-page drafting to a daily queue of ranked, sourced, review-ready content packages.

## 30-Day MVP

Hermes can:

- scan 10-20 curated sources daily
- cluster and rank content opportunities
- create sourced research briefs
- draft long-form article packages
- generate LinkedIn, X, and newsletter variants
- write durable topic/source memory to GBrain or local markdown
- log cost and run health
- require human approval before anything is published

## Explicitly Not In V1

- auto-publishing
- full CMS dashboard
- multi-channel scheduler
- paid ad creative generation
- full traffic attribution
- autonomous editorial judgment

## Solution Components

| Component | Role |
|---|---|
| Hermes | agent harness and scheduled workflow runner |
| You.com | current web search and enrichment |
| Firecrawl/Exa | fallback extraction where already wired |
| GBrain/Obsidian | durable memory for sources, topics, entities, and angles |
| Markdown/JSON queues | inspectable system of record for drafts and decisions |
| Model routing | cheap extraction, standard drafting, expensive reasoning only when needed |
| Editorial approval gate | prevents uncontrolled publishing |

## Build Decision

Build the workflow logic: source config, ranking, brief schema, draft package, approval queue, memory write-back, and cost controls.

Buy or reuse commodity capabilities: search, extraction, LLM inference, memory substrate, and scheduling.

## Feasibility

- Estimated effort: 124-196 hours
- Target 30-day cut: keep v1 under 160 hours by deferring dashboard, CMS publishing, multi-channel scheduling, and full analytics
- AI fit: 23/30 because the work is structured, source-checkable, asynchronous, and draft-only

## Launch Gate

Launch only after the smoke test proves:

- source scan works
- top opportunities are ranked with reasons
- research brief cites sources
- draft package is marked as draft
- rejected drafts are not reused as approved
- memory write-back preserves provenance
- no publish action occurs

## Success Metric

Within the first week of use, the pipeline should produce at least 3 review-ready content packages from real source clusters, with each package requiring editorial refinement rather than ground-up manual drafting.

