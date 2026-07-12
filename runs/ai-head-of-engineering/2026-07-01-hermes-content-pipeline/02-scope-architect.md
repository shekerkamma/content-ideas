# 02 - 30-Day Scope Architect

## In Scope

- Configure 10-20 curated source targets across YouTube/news/blogs/docs/social-ish sources where available.
- Scheduled daily source scan.
- Normalize source items into a simple JSON/markdown queue.
- Topic clustering and ranking based on relevance, freshness, business fit, and content angle.
- You.com search/livecrawl for current web enrichment and source-backed research.
- Research brief generation with citations/source URLs.
- Draft long-form article package.
- Generate three lightweight promotional variants: LinkedIn post, X thread outline, and email/newsletter blurb.
- Editorial queue in markdown/Obsidian-compatible files.
- GBrain write-back for durable topics, sources, entities, and prior angles.
- Cost logging, model-route logging, and daily run summary.

## Out Of Scope

- Automatic publishing to a live blog or CMS.
- Multi-user editorial workflow.
- Full visual dashboard.
- Paid ad creative factory.
- Full SEO analytics attribution.
- Automated image/video generation.
- Scraping sites that block automated access.
- Comment engagement automation.
- Lead capture and nurture automation.

## Milestones

### Week 1 - Foundation

- Define audience, voice, and source clusters.
- Create run folder structure and queue schemas.
- Configure search provider and memory write-back contract.
- Build a manual "scan -> queue" workflow.

### Week 2 - Core Pipeline

- Add scheduled source monitoring.
- Add ranking model and scoring rules.
- Generate research briefs from top-ranked topics.
- Store brief artifacts with source provenance.

### Week 3 - Drafting And Review

- Add article draft generation.
- Add SEO/AEO structure pass.
- Add promotional variant generation.
- Add editorial queue and approve/reject status.

### Week 4 - Hardening And Launch

- Add cost caps and run summaries.
- Add source freshness checks.
- Run smoke tests on 10 sample topics.
- Launch as draft-only workflow.

## Decisions Owed By Friday

- Target audience: founders, enterprise buyers, AI operators, or a narrower segment.
- Primary content format: blog, LinkedIn narrative, newsletter, or research brief.
- Source cluster list.
- Brand voice and "do not write like this" examples.
- Approval owner.
- Daily cost ceiling.

## Assumptions

- Hermes can run scheduled jobs locally or on an always-on machine.
- You.com API is configured outside the repo.
- GBrain/Obsidian-style memory is available or can be approximated with local markdown until wired.
- Human editor reviews every draft before publish.
- The first workflow values quality and provenance over volume.

## Definition Of Done

- 20 source items are ingested from configured sources.
- Top 5 opportunities are ranked with visible reasons.
- 3 research briefs are generated with source URLs.
- 3 draft article packages are produced.
- Each draft has LinkedIn, X, and newsletter variants.
- All outputs land in the editorial queue.
- GBrain write-back or local memory write-back succeeds for topics and sources.
- Daily run cost is logged.
- No content is published automatically.

