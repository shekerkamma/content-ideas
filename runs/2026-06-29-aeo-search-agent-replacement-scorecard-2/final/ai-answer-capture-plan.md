# AI Answer Capture Plan

- Run: `2026-06-29-aeo-search-agent-replacement-scorecard-2`
- Required independent captures: `20`
- Required engines: `4` (ChatGPT, Claude, Google AI Mode, Perplexity)
- Prompt coverage: `5` non-target-seeded prompts

## Evidence Rules

- Run each prompt exactly as written.
- Do not mention the target asset, scorecard, brand, page URL, or this workflow.
- Paste the full dated answer text and any visible citation/source URLs.
- If an engine shows no citations, leave citations empty and preserve the answer text.
- Do not synthesize, summarize, rewrite, or backfill answers.

## Capture Matrix

### act_001 - ChatGPT - aip_001

What software or workflow do teams usually use to handle ad & creative generation at scale, and where are AI agents realistically useful or not useful?

### act_002 - Claude - aip_001

What software or workflow do teams usually use to handle ad & creative generation at scale, and where are AI agents realistically useful or not useful?

### act_003 - Perplexity - aip_001

What software or workflow do teams usually use to handle ad & creative generation at scale, and where are AI agents realistically useful or not useful?

### act_004 - Google AI Mode - aip_001

What software or workflow do teams usually use to handle ad & creative generation at scale, and where are AI agents realistically useful or not useful?

### act_005 - ChatGPT - aip_002

What software or workflow do teams usually use to handle ai shopping / sales consultant, and where are AI agents realistically useful or not useful?

### act_006 - Claude - aip_002

What software or workflow do teams usually use to handle ai shopping / sales consultant, and where are AI agents realistically useful or not useful?

### act_007 - Perplexity - aip_002

What software or workflow do teams usually use to handle ai shopping / sales consultant, and where are AI agents realistically useful or not useful?

### act_008 - Google AI Mode - aip_002

What software or workflow do teams usually use to handle ai shopping / sales consultant, and where are AI agents realistically useful or not useful?

### act_009 - ChatGPT - aip_003

What software or workflow do teams usually use to handle conversational support, and where are AI agents realistically useful or not useful?

### act_010 - Claude - aip_003

What software or workflow do teams usually use to handle conversational support, and where are AI agents realistically useful or not useful?

### act_011 - Perplexity - aip_003

What software or workflow do teams usually use to handle conversational support, and where are AI agents realistically useful or not useful?

### act_012 - Google AI Mode - aip_003

What software or workflow do teams usually use to handle conversational support, and where are AI agents realistically useful or not useful?

### act_013 - ChatGPT - aip_004

What software or workflow do teams usually use to handle doc summarization & drafting, and where are AI agents realistically useful or not useful?

### act_014 - Claude - aip_004

What software or workflow do teams usually use to handle doc summarization & drafting, and where are AI agents realistically useful or not useful?

### act_015 - Perplexity - aip_004

What software or workflow do teams usually use to handle doc summarization & drafting, and where are AI agents realistically useful or not useful?

### act_016 - Google AI Mode - aip_004

What software or workflow do teams usually use to handle doc summarization & drafting, and where are AI agents realistically useful or not useful?

### act_017 - ChatGPT - aip_005

What software or workflow do teams usually use to handle legal research & drafting, and where are AI agents realistically useful or not useful?

### act_018 - Claude - aip_005

What software or workflow do teams usually use to handle legal research & drafting, and where are AI agents realistically useful or not useful?

### act_019 - Perplexity - aip_005

What software or workflow do teams usually use to handle legal research & drafting, and where are AI agents realistically useful or not useful?

### act_020 - Google AI Mode - aip_005

What software or workflow do teams usually use to handle legal research & drafting, and where are AI agents realistically useful or not useful?

## Ingest

Fill `stage_outputs/ai_live_capture_ingest_template.json` with the real answers.
Then ingest with the AEO live-capture workflow or transform each filled item into `aeo-live-capture` answers-json rows.
