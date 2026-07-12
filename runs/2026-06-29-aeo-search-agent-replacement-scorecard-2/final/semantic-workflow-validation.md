# Semantic Workflow Validation

## Verdict

The corrected AEO workflow is workflow-ready, not evidence-ready.

It now has the right operating shape:

- semantic evidence units instead of keyword-hit pattern claims
- low confidence for target-seeded captures
- subagent review before pattern promotion
- Reddit as semantic buyer-signal discovery, not keyword search
- explicit warnings against treating weak evidence as market truth

## Checks Passed

- `skills/aeo-pattern-miner/scripts/mine_patterns.py` compiles.
- `skills/aeo-reddit-opportunity-finder/scripts/find_opportunities.py` compiles.
- Pattern mining regenerates:
  - `normalized/capture_units.jsonl`
  - `normalized/semantic_clusters.jsonl`
  - `normalized/pattern_candidates.jsonl`
  - `working/subagent-review-brief.md`
  - `final/pattern-discovery-audit.json`
  - `final/pattern-mining-report.md`
- Reddit opportunity finder regenerates:
  - `stage_outputs/reddit_semantic_probes.jsonl`
  - `normalized/reddit_buyer_language.jsonl`
  - `normalized/reddit_aeo_opportunities.jsonl`
  - `final/reddit-opportunity-report.md`
- `pattern-discovery-audit.json` reports `uses_keyword_pattern_matching: false`.
- Current pattern candidates remain low confidence because all supporting evidence units are target-seeded.
- Subagent reviews reject or downgrade the current candidates instead of validating them.
- Reddit probes are semantic and include selection/retrieval rules requiring semantic fit.

## Checks Failed Or Not Yet Evidence-Ready

- No real Reddit thread evidence is loaded: `reddit_buyer_language.jsonl` has zero rows.
- No independent real AI-answer capture set exists for pattern promotion.
- The run is still based on two manual captures that cite the target domain.
- The AEO prompt pack still needs category-specific competitor cleanup before a full evidence sprint.

## Business Interpretation

This workflow now protects against false confidence. It can be used to run a real wedge validation sprint, but it should not yet produce external claims, a polished deck, or a buyer-facing market report.

## Next Validation Sprint

1. Select 5-8 clean semantic Reddit probes.
2. Collect semantically matched Reddit threads with URLs, snippets, scores, and subreddit context.
3. Convert Reddit buyer language into non-target-seeded AI-answer prompts.
4. Capture 20-30 dated answers across ChatGPT, Claude, Perplexity, and Google AI Mode.
5. Rerun semantic pattern mining.
6. Send evidence units to adversarial and product subagent reviewers.
7. Promote only patterns that survive evidence and review gates.
