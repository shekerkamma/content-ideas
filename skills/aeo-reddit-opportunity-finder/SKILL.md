---
name: aeo-reddit-opportunity-finder
description: Use when Reddit should become an AEO wedge/signal layer: find buyer-language threads, skepticism, competitor comparisons, and Reddit evidence that can update AEO prompts, validate semantic patterns, or identify source opportunities.
argument-hint: "[run-dir]"
permissions:
  file_read:
    - runs/
    - skills/aeo-reddit-opportunity-finder/
  file_write:
    - runs/
  shell:
    allowed_scripts:
      - scripts/find_opportunities.py
---

# aeo-reddit-opportunity-finder

Use Reddit as a signal layer for AEO. The goal is not automated posting. The
goal is to discover how buyers actually phrase doubts, comparisons, and
workflow pain so AEO prompts and pattern mining stop reflecting only our own
thesis.

## Runtime Preamble

Say: "Running `aeo-reddit-opportunity-finder`: I will treat Reddit as buyer
language and skepticism evidence, map threads to AEO prompts and semantic
patterns, and produce opportunity artifacts. I will not post or automate Reddit
engagement."

## Inputs

Run folder from `aeo-orchestrator` / `aeo-pattern-miner`.

Optional upstream evidence files inside the run:

- `stage_outputs/reddit_threads.jsonl`
- `stage_outputs/reddit_comments.jsonl`
- `stage_outputs/thread_data.json`

If Reddit evidence is not present, the script still produces a discovery plan
from the AEO prompt pack and pattern candidates.

## Workflow

1. Read:
   - `manifest.json`
   - `stage_outputs/queries.jsonl`
   - `normalized/pattern_candidates.jsonl` when present
   - `normalized/pattern_reviews.jsonl` when present
   - Reddit thread/comment evidence when present
2. Produce:
   - semantic Reddit probes by buyer job, objection, and decision context
   - candidate subreddits and semantic selection criteria
   - buyer-language signals from supplied Reddit evidence
   - prompt updates for AEO capture runs
   - source/opportunity recommendations
   - a handoff queue for `reddit-new-factcheck` and `reddit-seo-pipeline` when
     used through `aeo-evidence-sprint-loop`
3. Write:
   - `stage_outputs/reddit_semantic_probes.jsonl`
   - `normalized/reddit_buyer_language.jsonl`
   - `normalized/reddit_aeo_opportunities.jsonl`
   - `final/reddit-opportunity-report.md`

## Command

```bash
python3 skills/aeo-reddit-opportunity-finder/scripts/find_opportunities.py runs/<run-id>
```

## How It Fits

`AEO prompt pack -> Reddit semantic probes -> real Reddit evidence -> real AI-answer captures -> semantic pattern miner -> subagent review -> diagnostic/deck`

Reddit should improve the questions we ask AI systems and the patterns we test.
It should not be treated as proof by itself.

## Semantic Rule

Do not treat Reddit discovery as keyword search. Start with semantic probes:

- buyer job: what is the practitioner trying to accomplish?
- failure mode: where does current software or process break down?
- switching trigger: what would make them replace or renegotiate?
- skepticism: what claims would they challenge?
- comparison frame: what alternatives do they naturally compare?

Retrieval should use semantic search, `you-com-search`, agent/human screening,
or another research tool that can judge meaning. Prefer You.com over ordinary
WebSearch for candidate thread discovery when it is available. The evidence
decision is based on whether a thread semantically matches the probe, not
whether it matches the words. Do not accept threads from literal keyword hits
alone.

## Evidence Rules

- Reddit is buyer-language and skepticism evidence, not automatic truth.
- Do not claim demand or market size from a thread count.
- Do not recommend posting unless a human explicitly chooses to engage.
- Preserve thread URLs, comment IDs, scores, and quoted snippets when available.
- Map every opportunity to either a prompt update, pattern validation need, or
  source/citation opportunity.
- Treat You.com/Exa/search results as candidate retrieval only. Real Reddit
  evidence requires extracted thread/comment content and qualification.

## Relationship To Existing Reddit Skills

- `reddit-new-factcheck`: upstream validation gate for deciding whether a pain
  point, objection, comparison frame, or skepticism signal has qualified Reddit
  practitioner support.
- `reddit-seo-pipeline`: downstream extractor and manual strategy workflow when
  a specific Reddit thread URL is known. Use it to produce thread JSON and a
  human-reviewed engagement plan, never to post automatically.
- `aeo-pattern-miner`: downstream/upstream peer; Reddit creates buyer-language
  hypotheses, pattern miner checks AI-answer surfaces.

## Gotchas

- Do not use Reddit as an astroturfing workflow.
- Do not write promotional comments automatically.
- Do not overfit to generic AI subreddits. Prefer practitioner communities.
- Do not let Reddit replace real AI-answer captures; it sharpens them.
