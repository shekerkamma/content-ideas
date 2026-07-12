# 04 - Build vs Buy Auditor

## Recommendation Summary

Buy or reuse commodity infrastructure. Build the workflow logic that makes the content pipeline specific: source selection, ranking rubric, brief format, editorial gates, and memory write-back.

| Feature | Decision | 3-Year Cost Direction | Reasoning |
|---|---|---|---|
| Search/current web grounding | BUY | API spend, variable | You.com should be configured as preferred search; building search is wasteful. |
| Full-page extraction fallback | BUY/REUSE | API spend, variable | Use Firecrawl/Exa only where You.com extraction is insufficient. |
| Source cluster configuration | BUILD | Low dev + maintenance | Differentiated because it captures editorial strategy. |
| Source monitoring | HYBRID | Moderate | Use existing APIs/RSS/search where possible; build normalization and scoring. |
| Topic ranking | BUILD | Moderate | This is the pipeline's judgment layer and should reflect business priorities. |
| Research brief generation | HYBRID | API spend + prompt maintenance | Buy model/search calls; build brief schema and source discipline. |
| Draft article generation | HYBRID | API spend + prompt maintenance | Buy model inference; build voice, structure, and review controls. |
| Editorial queue | BUILD | Low | Markdown queue is simple and avoids SaaS workflow lock-in. |
| CMS publishing | DEFER/BUY LATER | Depends on CMS | Publishing is high-risk and not needed in v1. |
| Analytics | HYBRID | Low initially | Build run quality logs; buy traffic analytics later. |
| Memory write-back | REUSE | Low/moderate | Use GBrain/Obsidian-style memory rather than building a memory system now. |
| Cost/security monitoring | BUILD | Low/moderate | Guardrails need to be specific to this Hermes setup. |

## Integration Burden Flags

- CMS integrations can consume a week or more once credentials, previews, formatting, and rollback are included.
- Social APIs add policy and account-risk concerns; keep promotional outputs as drafts.
- Vendor pricing must be validated before production because model/search costs change and depend heavily on volume.

## Build / Buy Boundary

Build:
- Ranking rubric
- Research brief schema
- Draft package format
- Editorial queue
- Approval gates
- Cost and provenance logs

Buy / reuse:
- Search
- Extraction
- LLM inference
- Memory substrate
- Basic scheduling/runtime

