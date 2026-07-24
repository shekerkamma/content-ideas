---
name: aeo-live-capture
description: Use when collecting real AI-answer captures for an existing AEO workflow run. Guides the user through asking generated queries in ChatGPT, Claude, Perplexity, Google AI Mode, Gemini, or Copilot, then writes raw answer text and answer_captures.jsonl without hand-editing JSON.
argument-hint: "[run-dir]"
permissions:
  file_read:
    - runs/
    - skills/aeo-orchestrator/
    - skills/aeo-live-capture/
  file_write:
    - runs/
    - /tmp/
  shell:
    allowed_scripts:
      - scripts/capture_answers.py
---

# aeo-live-capture

Collect real AI-answer evidence for an AEO audit. This skill does not scrape or
log into AI products. It turns manual answer collection into a controlled,
artifact-backed workflow.

## Runtime Preamble

Say: "Running `aeo-live-capture`: I will show the generated prompts, collect
pasted AI answers and citation URLs, write raw capture files, then re-render the
AEO audit. Manual captures are real evidence only if they were copied from an
actual AI/search surface."

## Workflow

1. Require a run directory created by `aeo-orchestrator`.
2. Read:
   - `manifest.json`
   - `inputs/config.json`
   - `stage_outputs/queries.jsonl`
3. Pick the highest-priority queries or the user-specified query ids.
4. For each query:
   - show the exact prompt
   - ask the user to run it in ChatGPT, Claude, Perplexity, Google AI Mode,
     Gemini, or Copilot
   - collect engine name
   - collect pasted answer text
   - collect cited URLs, if any
5. Write:
   - `stage_outputs/raw/cap_live_*.txt`
   - `stage_outputs/answer_captures.jsonl`
6. Recompute sources, entities, scores, recommendations, and final report.
7. Run `aeo-qa` validation.

## Commands

Interactive mode:

```bash
python3 skills/aeo-live-capture/scripts/capture_answers.py \
  runs/<run-id> \
  --interactive \
  --replace-non-live
```

Noninteractive ingest mode:

```bash
python3 skills/aeo-live-capture/scripts/capture_answers.py \
  runs/<run-id> \
  --answers-json /tmp/live-answers.json \
  --replace-non-live
```

`answers-json` shape:

```json
[
  {
    "query_id": "q_061",
    "engine": "ChatGPT",
    "answer": "Pasted answer text...",
    "citation_urls": ["https://example.com/source"]
  }
]
```

## Evidence Labels

Use `raw_metadata.collection_method = manual_live_capture` for pasted answers
copied from a real AI/search product.

Use `manual_placeholder`, `scorecard_seed`, or `research_synthesis` for anything
that is not a live AI answer. QA keeps those runs in `draft`.

## Skill Relationships

### Category
Data & Analysis

### Dependencies
- `aeo-orchestrator` - creates the run folder and query pack.
- `aeo-qa` - validates the updated run after capture.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `aeo-orchestrator` | Sequential upstream | always | `runs/<run-id>/stage_outputs/queries.jsonl` |
| `aeo-qa` | Sequential downstream | after captures are written | `qa/validation.json` |
| `playwright-cli` | Future optional peer | only if approved browser capture is added later | screenshots/raw text |

## Host Compatibility

Canonical source: `skills/aeo-live-capture/SKILL.md`.

Works in Claude Code, Codex, and OpenHands because all state moves through local
run files.

## Gotchas

- Do not call scorecard seeds or research summaries "live" evidence.
- Do not auto-post, auto-publish, or automate accounts.
- Do not overwrite raw captures unless `--replace-non-live` is being used to
  remove placeholders/seeds.
- If citation URLs are not visible in the engine, leave `citation_urls` empty
  and preserve the answer text.
