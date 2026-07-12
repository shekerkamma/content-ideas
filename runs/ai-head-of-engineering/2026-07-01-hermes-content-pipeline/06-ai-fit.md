# 06 - AI Use-Case Validator

## Use Case

Use AI to rank content opportunities, synthesize source-grounded research briefs, generate draft articles, and create promotional variants for human review.

## AI Fit Score

| Axis | Score | Reasoning |
|---|---:|---|
| Task structure | 4/5 | Inputs and outputs can be strongly templated. |
| Output verifiability | 4/5 | Claims can be checked against source URLs and citations. |
| Failure tolerance | 4/5 | Draft-only workflow means humans catch failures before publishing. |
| Cost per call | 3/5 | Deep research and drafting can become expensive without caps. |
| Latency tolerance | 5/5 | Scheduled background workflow can wait minutes. |
| Hallucination risk | 3/5 | Risk is real, but source-grounding and review reduce blast radius. |

Total: 23/30

## Recommended Pattern

Use **LLM + tools + retrieval**, not a free-running agent loop for every item.

- Tools: source fetch, You.com search/livecrawl, queue read/write, cost log, memory write-back.
- Retrieval: use GBrain/local memory for prior topic angles, entities, and source history.
- LLM: use structured prompts for ranking, brief synthesis, article drafting, and variants.
- Agent loop: reserve for top-ranked topics where multi-step research is justified.

## Model Recommendation

- Default: Sonnet-class model for ranking, briefing, and drafting.
- Cheap extraction/classification: Haiku-class model.
- Expensive reasoning pass: Opus-class model only for high-value briefs or final editorial critique.

Planning cost target:

- Triage/source ranking: low-cost path, budget-capped per daily run.
- Full article package: allow higher spend, but cap number of packages per day.
- Production pricing must be checked against current provider pricing before launch.

## Failure Modes

1. The pipeline ranks noisy topics because the source cluster is poorly chosen.
2. Drafts contain plausible but unsupported claims.
3. The system over-produces content that matches keywords but not business strategy.
4. Costs increase silently because scheduled runs expand source volume.
5. Memory write-back pollutes durable context with low-quality summaries.

## Minimum Eval Set

- 20 historical source items manually labeled as good/bad opportunities.
- 10 ranked topic outputs reviewed by the operator.
- 5 research briefs checked for source support.
- 3 draft articles edited and scored for voice, accuracy, and usefulness.
- 1 end-to-end daily run under the configured cost cap.

