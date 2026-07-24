---
name: aeo-evidence-sprint-loop
description: Use when running the full real-evidence loop for AEO: refresh Reddit semantic probes, ingest Reddit buyer evidence, generate non-target-seeded AI-answer prompts, rerun semantic pattern mining, and report evidence gates until the workflow is evidence-ready.
argument-hint: "[run-dir]"
permissions:
  file_read:
    - runs/
    - skills/aeo-evidence-sprint-loop/
    - skills/aeo-reddit-opportunity-finder/
    - skills/aeo-pattern-miner/
  file_write:
    - runs/
  shell:
    allowed_scripts:
      - scripts/run_loop.py
      - scripts/auto_capture_matrix.py
      - scripts/ingest_capture_matrix.py
      - ../aeo-reddit-opportunity-finder/scripts/find_opportunities.py
      - ../aeo-pattern-miner/scripts/mine_patterns.py
---

# aeo-evidence-sprint-loop

Run the AEO evidence sprint as a loop, not a static plan.

The loop composes existing skills:

1. `aeo-reddit-opportunity-finder` refreshes semantic buyer-signal probes.
2. `reddit-new-factcheck` qualifies whether Reddit evidence actually supports
   the semantic pain, objection, or comparison frame.
3. `reddit-seo-pipeline` extracts and analyzes known high-value thread URLs for
   manual strategy only; it must not post to Reddit.
4. Reddit evidence, when present, is normalized into buyer-language signals.
5. Non-target-seeded AI-answer prompts are generated from buyer jobs,
   objections, switching triggers, and comparison frames.
6. `aeo-pattern-miner` reruns semantic pattern mining.
7. Evidence gates decide whether the run is still `workflow_ready`,
   `evidence_collecting`, or `evidence_ready`.

## Runtime Preamble

Say: "Running `aeo-evidence-sprint-loop`: I will loop through Reddit semantic
probes, AI prompt generation, semantic pattern mining, and evidence gates. I
will not claim evidence-readiness until real Reddit evidence and independent
AI-answer captures exist."

## Command

```bash
python3 skills/aeo-evidence-sprint-loop/scripts/run_loop.py runs/<run-id>
```

## Inputs

Required:

- `manifest.json`
- `stage_outputs/queries.jsonl`

Optional but needed for evidence-ready status:

- `stage_outputs/reddit_threads.jsonl`
- `stage_outputs/reddit_comments.jsonl`
- `stage_outputs/answer_captures.jsonl` with independent real AI-answer captures

## Outputs

- `stage_outputs/ai_answer_prompt_pack.jsonl`
- `stage_outputs/ai_answer_capture_matrix.jsonl`
- `stage_outputs/ai_live_capture_ingest_template.json`
- `stage_outputs/reddit_skill_queue.jsonl`
- `final/ai-answer-capture-plan.md`
- `final/reddit-skill-loop-brief.md`
- `final/real-evidence-sprint-plan.md`
- `qa/evidence_sprint_status.json`

The loop also refreshes upstream/downstream artifacts:

- `stage_outputs/reddit_semantic_probes.jsonl`
- `normalized/reddit_buyer_language.jsonl`
- `normalized/reddit_aeo_opportunities.jsonl`
- `final/reddit-opportunity-report.md`
- `normalized/capture_units.jsonl`
- `normalized/semantic_clusters.jsonl`
- `normalized/pattern_candidates.jsonl`
- `final/pattern-mining-report.md`

## Reddit Skill Loop

Use the generated Reddit queue as the bridge between AEO pattern discovery and
existing Reddit skills:

1. `reddit-new-factcheck`: run first for queue items whose goal is to validate
   a pain point, objection, comparison frame, or skepticism signal against real
   Reddit practitioner evidence.
2. `reddit-seo-pipeline`: run only after a specific Reddit URL is known and the
   goal is thread extraction or manual engagement strategy. Never automate
   posting.
3. Write skill-derived thread/comment exports back into the same run folder as
   `stage_outputs/reddit_threads.jsonl`, `stage_outputs/reddit_comments.jsonl`,
   or per-thread JSON files that can be normalized.

The queue is not evidence. It is a retrieval worklist. A Reddit item becomes
evidence only after it passes the qualification gate from `reddit-new-factcheck`:
matching subreddit/source context, matching practitioner persona, matching
workflow language, and concrete pain, workaround, objection, adoption signal, or
comparison.

## Evidence Gates

`evidence_ready` requires all of:

- at least 5 real Reddit buyer-language rows
- at least 20 independent real AI-answer captures
- at least 3 independent answer engines
- no promoted high/medium pattern that relies on target-seeded evidence
- at least one pattern candidate with reviewer acceptance or a pending review
  package ready for subagents

Until then the run remains an internal workflow/evidence sprint.

## AI Capture Ingest

To fill the capture matrix from official APIs where credentials are present:

```bash
python3 skills/aeo-evidence-sprint-loop/scripts/auto_capture_matrix.py \
  runs/<run-id> \
  --engines "ChatGPT,Claude,Perplexity,Google AI Mode"
```

This does not scrape logged-in consumer products. It calls provider APIs only
when the relevant keys exist:

- `OPENAI_API_KEY` for `ChatGPT`
- `ANTHROPIC_API_KEY` for `Claude`
- `PERPLEXITY_API_KEY` or `PPLX_API_KEY` for `Perplexity`
- `GOOGLE_GENERATIVE_AI_API_KEY`, `GEMINI_API_KEY`, or `GOOGLE_API_KEY` for
  `Google AI Mode` / Gemini API captures

API captures are labeled with `capture_status = captured_api` and
`api_capture_note`. Treat them as model API evidence, not proof of the exact
consumer UI result.

After real answers are pasted into
`stage_outputs/ai_live_capture_ingest_template.json`, validate and ingest them
through `aeo-live-capture`:

```bash
python3 skills/aeo-evidence-sprint-loop/scripts/ingest_capture_matrix.py \
  runs/<run-id>
```

The ingest script requires:

- at least 20 filled answers
- at least 3 engines
- `query_id`, `engine`, `captured_at`, and verbatim `answer` for every row
- no target asset or scorecard mention in the prompt or captured answer

It writes `stage_outputs/ai_live_answers_for_ingest.json`, invokes
`aeo-live-capture`, then reruns the evidence loop.

## Gotchas

- Do not generate target-seeded prompts that mention the Agent Replacement
  Scorecard.
- Do not treat generated Reddit semantic probes as Reddit evidence.
- Do not treat manual test captures as market evidence.
- Do not mark the run evidence-ready because scripts pass.
