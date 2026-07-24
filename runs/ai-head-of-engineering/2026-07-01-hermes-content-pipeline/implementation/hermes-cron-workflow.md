# Hermes Cron Workflow - Content Pipeline V1

## Cron Name

`hermes-content-pipeline-daily`

## Schedule

Daily at `06:30` local time.

## Preconditions

- `YOU_API_KEY` is configured outside the repo.
- Hermes search backend is configured as `you`.
- `sources.yaml` exists.
- `pipeline-config.yaml` exists.
- Output root exists or can be created.
- No active lock file exists.

## Workflow

Hermes can execute the workflow by running:

```bash
python3 /home/shekerk/content-ideas/runs/ai-head-of-engineering/2026-07-01-hermes-content-pipeline/implementation/runner.py --live --output-root /home/shekerk/content-ideas/runs/hermes-content-pipeline
```

If live search is not ready, omit `--live` to run fixture mode and validate the artifact flow without API spend.

### 1. Acquire Lock

- Check `.locks/content-pipeline.lock`.
- If lock exists and is younger than 2 hours, stop and write skipped-run log.
- If lock exists and is stale, write warning and replace it.

### 2. Load Config

- Read `sources.yaml`.
- Read `pipeline-config.yaml`.
- Validate required fields.
- Confirm `mode: draft_only`.
- Confirm `approval_gates.publish_allowed: false`.

### 3. Scan Sources

For each enabled source cluster:

- Query the preferred search provider for recent source items.
- Use source URL/domain constraints where possible.
- Fetch or extract only enough content to classify and summarize.
- Normalize each item to `source-item.schema.json`.
- Deduplicate by canonical URL and title similarity.
- Stop at `daily_caps.source_items`.

### 4. Rank Topic Opportunities

- Group source items into topic clusters.
- Score clusters with the configured ranking weights.
- Write top clusters to `topic-clusters/YYYY-MM-DD/`.
- Include ranking reasons and source coverage.
- Stop at `daily_caps.topic_clusters`.

### 5. Generate Research Briefs

For top-ranked clusters:

- Use You.com search/livecrawl for current evidence.
- Prefer primary sources when available.
- Require at least `quality_gates.min_sources_per_brief` sources.
- Write markdown and JSON brief artifacts.
- Stop at `daily_caps.research_briefs`.

### 6. Generate Draft Package

For the top eligible brief:

- Draft one long-form article package.
- Generate LinkedIn, X, and newsletter variants.
- Build citation map.
- Mark status as `draft`.
- Write markdown and JSON artifacts.
- Stop at `daily_caps.draft_packages`.

### 7. Quality Checks

- Confirm every draft claim that needs support maps to citations.
- Confirm citations include URLs and fetched dates.
- Confirm output status is draft.
- Confirm no publish action was requested or available.

### 8. Memory Write-Back Candidates

- Write memory candidates for sources, entities, topics, and angles.
- Include provenance and confidence.
- Do not write low-confidence claims.
- If GBrain is unavailable, write local markdown candidates.

### 9. Run Log

- Write run summary.
- Record source counts, topic counts, brief counts, draft counts.
- Record model route and estimated spend.
- Record errors and skipped sources.

### 10. Release Lock

- Remove lock.
- If removal fails, write error summary.

## Failure Behavior

- Search provider unavailable: stop after writing a failed run log.
- Source extraction fails: skip source and continue.
- Brief has fewer than 3 valid sources: do not draft from it.
- Draft quality gate fails: write draft as `needs_revision`, not `approved`.
- Cost cap exceeded: stop after current artifact and write partial-run log.
- Publish attempt detected: block, write critical error, and stop.

## First Manual Test

Run the workflow once with:

- 3 source clusters
- 10 source items max
- 3 topic clusters max
- 1 research brief max
- 1 draft package max

Pass when one draft package and one business deliverable package land in the run folder with citations, variants, run log, and no publish action.
