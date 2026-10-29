---
name: aeo-orchestrator
description: Use when running a portable AI-search/AEO visibility audit for one brand, domain, competitor set, and prompt pack. Orchestrates query planning, answer capture ingestion, entity extraction, visibility scoring, recommendation generation, QA, and final report rendering across Claude Code and Codex.
argument-hint: "[config.json|--sample]"
permissions:
  file_read:
    - runs/
    - skills/aeo-orchestrator/
  file_write:
    - runs/
    - /tmp/
  shell:
    allowed_scripts:
      - scripts/run_pipeline.py
      - scripts/validate_contracts.py
---

# aeo-orchestrator

Run a reproducible AEO evidence pipeline. This is a workflow kit, not a
dashboard, rank tracker, or autonomous publisher.

The orchestrator owns state, contracts, validation, and final status. Leaf
skills own judgment-heavy stages. Scripts own deterministic mechanics.

## Runtime Preamble

Say: "Running `aeo-orchestrator`: I will create a file-backed AEO audit run,
preserve raw captures, validate artifact contracts, and produce Markdown/CSV
evidence. I will not auto-publish or claim guaranteed AI-search rankings."

## Source / Tool Order

Use wired research/search dependencies before generic web search:

1. Read repo-local config, prior run files, and referenced skill files.
2. Run GBrain recall when available for the brand, competitors, topics, and
   prior AEO runs.
3. Use `you-com-search`, Hermes `web.search_backend: you`, or an equivalent
   You.com wrapper for current-web discovery, livecrawl, research, or finance
   research when the audit needs external source discovery.
4. Use Exa for semantic/source discovery and Firecrawl for full-page capture
   after candidate URLs are known.
5. Use specialist MCPs/plugins for the source class when available, such as
   GitHub, Google Drive, Microsoft Learn, browser/Reddit tools, or official
   docs connectors.
6. Use generic WebSearch/search_web only when the above routes are unavailable
   or return no useful signal, and label the evidence as fallback-sourced.

## Inputs

Accept either:

- `$ARGUMENTS = --sample` for a smoke-test sample run.
- Path to a JSON config file.
- If no argument is provided, ask for a config path or permission to run
  `--sample`.

Config shape:

```json
{
  "target_brand": "ExampleCo",
  "domain": "example.com",
  "competitors": ["CompetitorA", "CompetitorB"],
  "market": "US",
  "language": "en",
  "objective": "Find where AI answers recommend competitors instead of us.",
  "topics": ["enterprise AI search optimization", "AEO platform"],
  "engines": ["manual"],
  "manual_captures": [
    {
      "query": "best enterprise AI search optimization platforms",
      "engine": "manual",
      "answer": "CompetitorA is often recommended...",
      "citation_urls": ["https://competitora.com/"]
    }
  ]
}
```

## Workflow

1. Resolve the skill directory and script paths.
2. Run the pipeline:

```bash
python3 skills/aeo-orchestrator/scripts/run_pipeline.py --config "$ARGUMENTS"
```

For smoke test:

```bash
python3 skills/aeo-orchestrator/scripts/run_pipeline.py --sample
```

3. Validate contracts:

```bash
python3 skills/aeo-orchestrator/scripts/validate_contracts.py runs/<run-id>
```

4. Report the final artifact paths:
   - `final/aeo-audit.md`
   - `final/evidence.csv`
   - `normalized/visibility_scores.json`
   - `normalized/recommendations.jsonl`
5. When the business question is "what patterns are AI answers surfacing?",
   hand the reviewed run to `aeo-pattern-miner`:

```bash
python3 skills/aeo-pattern-miner/scripts/mine_patterns.py runs/<run-id>
```

6. When Reddit should become the wedge/signal layer, hand the same run to
   `aeo-reddit-opportunity-finder`:

```bash
python3 skills/aeo-reddit-opportunity-finder/scripts/find_opportunities.py runs/<run-id>
```

## Artifact Contract

Read `references/contracts.md` before changing schemas. The non-negotiable
contract files are:

- `manifest.json`
- `stage_outputs/queries.jsonl`
- `stage_outputs/sources.jsonl`
- `stage_outputs/answer_captures.jsonl`
- `normalized/entities.jsonl`
- `normalized/visibility_scores.json`
- `normalized/recommendations.jsonl`
- `qa/validation.json`
- `final/aeo-audit.md`
- `final/evidence.csv`

## Validation Gates

The run is `reviewed` only when:

- target brand, market, objective, and prompt pack exist
- each query has `query_id`, `cluster`, `persona`, `intent`, `query`, and
  `priority`
- every answer capture maps to a query
- raw answer text exists on disk
- every recommendation cites at least one existing evidence id
- validation passes with no hard errors

If any hard gate fails, keep status `blocked` or `draft`.

## Skill Relationships

### Category
Business Automation

### Dependencies
- `aeo-query-planner` - planning rubric for query clusters.
- `aeo-answer-capture` - ingestion rules for manual/API/browser captures.
- `aeo-live-capture` - guided workflow for pasted real AI-answer captures.
- `aeo-entity-extractor` - extraction rules for brands, citations, and claims.
- `aeo-gap-analyzer` - recommendation rules.
- `aeo-qa` - final grounding and contract gate.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `content-ideas` | Sequential upstream | when topics or buyer language come from trend research | `feed-data.json` or selected topic list |
| `aeo-live-capture` | Sequential downstream | when seed/placeholder captures need real AI-answer evidence | `stage_outputs/answer_captures.jsonl` |
| `reddit-new-factcheck` | Sequential upstream | when Reddit evidence is needed | `reddit-evidence-pack.json` |
| `reddit-seo-pipeline` | Sequential upstream | when Reddit thread opportunities are part of the audit | `thread_data.json` |
| `aeo-reddit-opportunity-finder` | Sequential downstream | when Reddit should sharpen prompts, objections, and pattern evidence | `final/reddit-opportunity-report.md` |
| `enterprise-ai-competitor-landscape` | Sequential upstream | when competitor universe needs sourcing | company table or report |
| `second-brain` | Amplifier | after durable findings need wiki/write-back | `final/aeo-audit.md` |
| `branded-pptx-deck` | Sequential downstream | only after QA passes and a deck is requested | `final/aeo-audit.md` |
| `aeo-pattern-miner` | Sequential downstream | when AEO should discover recurring market patterns | `final/pattern-mining-report.md` |

### Runtime Preamble
This orchestrator composes existing research skills when their artifacts are
available, but the run folder remains the system of record. GBrain/second-brain
are memory layers, not deliverable storage.

## Host Compatibility

### Target Hosts
- Claude Code: yes - use this repo-local skill or mirror as a thin wrapper.
- Codex/OpenAI: yes - canonical path `skills/aeo-orchestrator/SKILL.md`.
- OpenHands: yes - use the same files and scripts.

### Canonical Source
`skills/aeo-orchestrator/SKILL.md`

## Gotchas

- Never overwrite raw capture text on retry. Add a new capture id instead.
- Do not claim "ranking" certainty. Treat visibility scores as observed
  evidence from dated captures.
- Do not auto-publish content, comments, or site changes.
- Do not make unsupported recommendations. Every recommendation needs evidence
  ids resolving to a capture or source.
