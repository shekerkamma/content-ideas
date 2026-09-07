# AEO Workflow Kit Contracts

All stages exchange local artifacts. JSONL is used for record streams; JSON is
used for manifests and summaries; Markdown/CSV are human-facing outputs.

## Run Layout

```text
runs/YYYY-MM-DD-aeo-search-<slug>/
  manifest.json
  inputs/
  stage_outputs/
    raw/
    queries.jsonl
    sources.jsonl
    answer_captures.jsonl
  normalized/
    entities.jsonl
    visibility_scores.json
    recommendations.jsonl
  qa/
    validation.json
  final/
    aeo-audit.md
    evidence.csv
```

## manifest.json

Required fields:

- `run_id`
- `created_at`
- `target_brand`
- `domain`
- `competitors`
- `market`
- `language`
- `objective`
- `engines`
- `stage_status`
- `artifact_paths`
- `validation_status`
- `status`

## queries.jsonl

Required fields:

- `query_id`
- `cluster`
- `persona`
- `intent`
- `query`
- `priority`

## sources.jsonl

Required fields:

- `source_id`
- `url`
- `domain`
- `source_type`
- `is_primary`
- `retrieved_at`
- `freshness_status`

## answer_captures.jsonl

Required fields:

- `capture_id`
- `query_id`
- `engine`
- `captured_at`
- `answer_text_path`
- `citation_urls`
- `raw_metadata`

## entities.jsonl

Required fields:

- `entity_id`
- `name`
- `entity_type`
- `aliases`
- `source_capture_ids`
- `evidence_ids`

## visibility_scores.json

Required fields:

- `target_brand`
- `competitors`
- `summary`
- `by_query`
- `by_entity`

## recommendations.jsonl

Required fields:

- `recommendation_id`
- `priority`
- `theme`
- `action`
- `evidence_ids`
- `expected_impact`
- `effort`
- `confidence`

## Status Values

- `draft`: artifacts exist but evidence is incomplete or sample/manual.
- `reviewed`: validation passes and enough real evidence exists.
- `blocked`: hard gate failed.

Sample runs must stay `draft`.
