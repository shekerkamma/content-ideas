# Real Evidence Sprint Loop

- Run: `2026-06-29-aeo-search-agent-replacement-scorecard-2`
- Loop status: `evidence_collecting`

## Gate Status

- PASS: `reddit_buyer_language_min_5`
- TODO: `independent_ai_answer_captures_min_20`
- TODO: `independent_answer_engines_min_3`
- PASS: `no_promoted_target_seeded_patterns`
- PASS: `review_acceptance_or_package_ready`
- PASS: `prompt_pack_ready`

## Counts

- reddit_buyer_language_rows: 88
- ai_answer_prompt_rows: 8
- answer_captures: 12
- manual_live_captures: 12
- independent_ai_answer_captures: 10
- independent_answer_engines: 2
- target_seeded_capture_ids: 2
- pattern_candidates: 9
- accepted_pattern_reviews: 0

## AI Answer Prompt Pack

### aip_001 - job_to_be_done

What software or workflow do teams usually use to handle ad & creative generation at scale, and where are AI agents realistically useful or not useful?

- Source probe: `rsp_163`
- Required engines: ChatGPT, Claude, Perplexity, Google AI Mode

### aip_002 - job_to_be_done

What software or workflow do teams usually use to handle ai shopping / sales consultant, and where are AI agents realistically useful or not useful?

- Source probe: `rsp_030`
- Required engines: ChatGPT, Claude, Perplexity, Google AI Mode

### aip_003 - job_to_be_done

What software or workflow do teams usually use to handle conversational support, and where are AI agents realistically useful or not useful?

- Source probe: `rsp_001`
- Required engines: ChatGPT, Claude, Perplexity, Google AI Mode

### aip_004 - job_to_be_done

What software or workflow do teams usually use to handle doc summarization & drafting, and where are AI agents realistically useful or not useful?

- Source probe: `rsp_114`
- Required engines: ChatGPT, Claude, Perplexity, Google AI Mode

### aip_005 - job_to_be_done

What software or workflow do teams usually use to handle legal research & drafting, and where are AI agents realistically useful or not useful?

- Source probe: `rsp_143`
- Required engines: ChatGPT, Claude, Perplexity, Google AI Mode

### aip_006 - job_to_be_done

What software or workflow do teams usually use to handle messaging-channel chatbot, and where are AI agents realistically useful or not useful?

- Source probe: `rsp_085`
- Required engines: ChatGPT, Claude, Perplexity, Google AI Mode

### aip_007 - job_to_be_done

What software or workflow do teams usually use to handle personalized marketing content, and where are AI agents realistically useful or not useful?

- Source probe: `rsp_184`
- Required engines: ChatGPT, Claude, Perplexity, Google AI Mode

### aip_008 - job_to_be_done

What software or workflow do teams usually use to handle travel & booking planner, and where are AI agents realistically useful or not useful?

- Source probe: `rsp_058`
- Required engines: ChatGPT, Claude, Perplexity, Google AI Mode

## Reddit Skill Queue

- `rsq_001` -> `reddit-new-factcheck`: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around ad & creative generation at scale?
- `rsq_002` -> `reddit-new-factcheck`: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around ai shopping / sales consultant?
- `rsq_003` -> `reddit-new-factcheck`: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around conversational support?
- `rsq_004` -> `reddit-new-factcheck`: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around doc summarization & drafting?
- `rsq_005` -> `reddit-new-factcheck`: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around legal research & drafting?
- `rsq_006` -> `reddit-new-factcheck`: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around messaging-channel chatbot?
- `rsq_007` -> `reddit-new-factcheck`: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around personalized marketing content?
- `rsq_008` -> `reddit-new-factcheck`: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around travel & booking planner?
- plus 4 additional queue items in `stage_outputs/reddit_skill_queue.jsonl`

## AI Answer Capture Matrix

- Capture tasks: 20
- File: `stage_outputs/ai_answer_capture_matrix.jsonl`
- Ingest template: `stage_outputs/ai_live_capture_ingest_template.json`
- Instructions: `final/ai-answer-capture-plan.md`

## Next Loop

1. Use `final/reddit-skill-loop-brief.md` and `stage_outputs/reddit_skill_queue.jsonl` to collect real Reddit thread/comment evidence.
2. Load real Reddit threads/comments into `stage_outputs/reddit_threads.jsonl` or `stage_outputs/reddit_comments.jsonl`.
3. Capture the matrix answers from ChatGPT, Claude, Perplexity, and Google AI Mode.
4. Add captures through `aeo-live-capture`.
5. Rerun this loop until gates pass.
