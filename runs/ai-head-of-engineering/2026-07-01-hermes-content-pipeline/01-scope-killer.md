# 01 - Scope Killer

## Core Moment Of Value

The operator receives a ranked content opportunity with a sourced research brief, a draft article, and promotional variants ready for editorial review without manually scanning source feeds.

## Feature Decisions

| Feature | Score | Decision | Reasoning |
|---|---:|---|---|
| Curated source cluster configuration | 9 | KEEP | Required to define what Hermes monitors. |
| Scheduled source monitoring | 8 | KEEP | Core to the always-on content pipeline. |
| You.com-backed current web search | 8 | KEEP | Required for fresh evidence and source discovery. |
| Topic clustering and ranking | 8 | KEEP | Converts noise into prioritized content opportunities. |
| Source-grounded research brief | 8 | KEEP | Creates defensible input for writing. |
| Draft long-form article | 7 | KEEP | Produces the main content asset. |
| SEO/AEO structure pass | 7 | KEEP | Aligns output to discovery goals without needing a separate CMS. |
| Promotional variants | 6 | KEEP | Useful if limited to LinkedIn/X/email snippets, not ad-scale generation. |
| Human editorial queue | 8 | KEEP | Required guardrail before publish. |
| GBrain memory write-back | 7 | KEEP | Builds durable topic/source/entity knowledge. |
| Cost and token logging | 8 | KEEP | Prevents runaway scheduled spending. |
| Auto-publish to CMS | 3 | DEFER | Too risky for v1; editorial approval must stay mandatory. |
| Full CMS dashboard | 4 | DEFER | Nice to have; markdown/Obsidian queue is enough for v1. |
| Hundreds of dynamic ad creatives | 2 | CUT | Not needed for first content pipeline value. |
| Multi-channel scheduler | 4 | DEFER | Useful later but adds platform permissions and risk. |
| Full analytics attribution | 4 | DEFER | Track simple status and links first. |
| Competitor-wide market intelligence portal | 3 | DEFER | Broader than content drafting. |
| Automated brand voice training | 4 | DEFER | Start with a documented style profile and eval set. |

## 80/20 Keep List

1. Source monitoring
2. Topic clustering and ranking
3. Source-grounded research brief
4. Draft article package
5. Editorial queue with approval gates

## One-Line MVP Statement

In 30 days, Hermes can monitor curated content sources, rank the best content opportunities, generate a sourced draft package, and queue it for human editorial approval.

## Founder-Favorite Features Cut Or Deferred Anyway

- Auto-publishing: deferred because one hallucinated or off-brand article can damage trust.
- Full CMS/dashboard: deferred because file-based review proves workflow value faster.
- Large-scale ad creative generation: cut because the first risk is topic quality, not creative volume.

