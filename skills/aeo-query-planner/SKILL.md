---
name: aeo-query-planner
description: Use when turning a brand, market, competitors, topics, or buyer objective into AEO query clusters for AI-search visibility audits.
argument-hint: "[brand/topic/config]"
---

# aeo-query-planner

Create the prompt/query pack for an AEO audit. Output structured query records,
not prose-only suggestions.

## Source / Tool Order

Use wired search dependencies if the query plan needs current market language:

1. Read the supplied brand/topic/config and local AEO artifacts.
2. Run GBrain recall when available for prior prompts, competitors, and buyer
   language.
3. Use `you-com-search`, Hermes `web.search_backend: you`, or equivalent
   You.com wrapper for current buyer-language, competitor, and category
   discovery.
4. Use Exa for semantic/source discovery and Firecrawl for full-page capture
   after candidate URLs are known.
5. Use generic WebSearch/search_web only if the dependency chain is unavailable
   or returns no useful signal.

## Required Query Clusters

Cover as many as fit the scope:

1. `category` - best tools/vendors/platforms in the category.
2. `comparison` - target brand versus competitors.
3. `alternatives` - alternatives to named competitors.
4. `problem` - buyer pain or workflow query.
5. `selection` - "which should I choose" decision prompt.
6. `pricing` - pricing/value prompt when relevant.

Each query must include:

- `query_id`
- `cluster`
- `persona`
- `intent`
- `query`
- `priority`

## Output

Write query records to:

`runs/<run-id>/stage_outputs/queries.jsonl`

## Skill Relationships

### Category
Data & Analysis

### Dependencies
None.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `aeo-orchestrator` | Sequential downstream | always | `stage_outputs/queries.jsonl` |
| `content-ideas` | Sequential upstream | when topics come from content research | selected topic list |

## Host Compatibility

Canonical source: `skills/aeo-query-planner/SKILL.md`.

## Gotchas

- Do not create only branded queries. Non-branded and competitor prompts expose
  where the brand loses recommendations.
- Do not overfit to SEO keywords. Buyer-language prompts are more useful than
  keyword variants.
