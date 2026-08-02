---
name: evidence-led-competitor-pipeline
description: Orchestrate current-web ingestion, an AI Analyst evidence ledger, metric-first competitive scoring, decision-story review, and client-ready branded PPTX plus self-contained HTML delivery. Use when a competitor landscape, market map, battlecard, startup cohort, or company comparison must be repeatable, traceable, resumable, and pass evidence, PowerPoint, HTML, and manifest QA gates; especially when Printing Press/Firecrawl or You.com supplies research and `aianalyst-competitor-analysis` plus `competitor-analysis-pipeline` produce the deliverables.
---

# Evidence-Led Competitor Pipeline

Run a compound skillpipe whose stages have explicit owners, handoff artifacts, and stop
conditions. Keep business logic in the participating skills; this skill owns orchestration,
state, and gate enforcement.

## Runtime Preamble

State:

> I am using the evidence-led competitor pipeline: GBrain/local recall, Printing Press and
> You.com ingestion, AI Analyst evidence controls, story and strategy review, then branded
> PPTX/HTML build and QA. Printing Press is a data tap; it does not score competitors or
> produce the final client artifacts.

## Required Reading

- Read `references/skillpipe.json` before initializing or resuming a run.
- Read `references/handoff-contract.md` before changing stage order, waiving a gate, or
  promoting an artifact to `reviewed`.
- Read the complete `aianalyst-competitor-analysis` and
  `competitor-analysis-pipeline` instructions for the current host.
- When a PPTX is required, apply `pptx-visual-spec` and a direct branded deck skill.

## Operating Model

Use this fixed ownership model:

| Layer | Owner | Responsibility |
|---|---|---|
| Recall | GBrain or durable memory | Reuse prior company, vertical, and source knowledge |
| Data taps | `you-com-search` Level 2 and `pp-firecrawl` | Discover and capture current pages, structured content, and approved source assets |
| Evidence product | `aianalyst-competitor-analysis` | Ledger, metrics, quality, scoring, confidence, allowed numbers, traceability |
| Decision story | `story-architect`, grill/GStack lenses | BLUF, tension, argument arc, slide spine, proof gaps, recommendations |
| Client delivery | `competitor-analysis-pipeline` plus branded builders | Editable branded PPTX, self-contained HTML, publishing when requested |
| QA and state | This skillpipe | Gate checks, resumability, manifest, status, and sync |

Never let a data tap write scores or recommendations directly. Never let a rendering tool
invent or reinterpret evidence.

## Workflow

1. **Resume before creating.**
   Read `<run>/status.json`. Preserve an existing run and fill missing artifacts in place.
   Initialize only when the run has no status:

   ```bash
   python3 skills/evidence-led-competitor-pipeline/scripts/skillpipe.py init \
     <run> --target "<target>" --min-slides <count>
   ```

2. **Recall and inventory.**
   Record whether GBrain/memory was used. Inventory existing research, source captures,
   visual assets, decks, HTML, and QA results. Do not repeat current research already
   captured with source URLs and retrieval dates.

3. **Acquire evidence.**
   Use repo/local sources first, then You.com Level 2 livecrawl, then `pp-firecrawl` for
   full-page or site capture. Use Exa or primary sources for targeted discovery and generic
   search only as fallback. Save raw results under `working/` or `research/`; record every
   query/capture in `outputs/search-log.md`.

4. **Build the evidence product.**
   Invoke `aianalyst-competitor-analysis`. Create the evidence ledger at one row per sourced
   claim, define metrics before scoring, report coverage and source bias, build the scoring
   model, and create `allowed-numbers.yaml`. Label synthesis and confidence explicitly.

5. **Lock the story.**
   Create the story-architect pack only after evidence, metrics, data quality, and scoring
   exist. Apply grill/GStack review as lenses. Update the pack if the review changes the
   BLUF, order, evidence map, or promoted datapoints.

6. **Specify visuals.**
   Write and validate `<run>/visual-spec.json`. Keep claims, metrics, citations, logos, and
   product proof native or approved/extracted. Image generation may provide only
   non-evidentiary, text-free visual support.

7. **Build client artifacts.**
   Use `competitor-analysis-pipeline` and the configured branded PPTX workflow. Produce an
   editable `*-draft.pptx`, a self-contained `client-package/site/index.html`, and builder
   sources. Do not ship an image-only deck. Preserve the builder with the run.

8. **Validate and promote.**
   Run the skillpipe validator, PPTX structural/design/render/OfficeCLI QA, visible-number
   scan, editable-text-shape check, and Playwright/browser HTML QA. Write
   `outputs/sync-check.md` and `client-package/delivery-manifest.json`. Copy to a
   `*-reviewed.pptx` only after all required gates pass.

9. **Prove material change when a redesign was requested.**
   A successful rebuild is not proof of a successful redesign. Compare the previous and
   candidate PPTX with `scripts/compare_pptx.py`. When the user asked to rework, redesign,
   improve, or create a new deck from an existing one, require visible slide-level change:

   ```bash
   python3 skills/evidence-led-competitor-pipeline/scripts/compare_pptx.py \
     <previous.pptx> <candidate.pptx> \
     --require-material \
     --json-out <run>/client-package/qa/material-change.json
   ```

   Report slide-count change, same-position full-text matches, identical slide text found
   anywhere, changed slide positions, and editable-text-shape counts. A deck that only
   changes shared geometry, headers, metadata, or pipeline artifacts fails this gate.

10. **Close the loop.**
   Record reusable corrections in `outputs/run-learnings.md`, update the skill when the
   correction generalizes, and write durable findings back to GBrain when available.

## Commands

Show current stage:

```bash
python3 skills/evidence-led-competitor-pipeline/scripts/skillpipe.py status <run>
```

Validate one gate:

```bash
python3 skills/evidence-led-competitor-pipeline/scripts/skillpipe.py validate \
  <run> --stage evidence
```

Validate the complete pipeline:

```bash
python3 skills/evidence-led-competitor-pipeline/scripts/skillpipe.py validate \
  <run> --stage complete --json-out <run>/outputs/skillpipe-validation.json
```

The validator is intentionally dependency-free and checks artifact presence and status
contracts. It complements, but does not replace, semantic evidence review or visual QA.

## Status Rules

- `draft`: analysis or artifacts exist but at least one required final gate is incomplete.
- `reviewed`: evidence, story, editable PPTX, OfficeCLI, HTML, sync, and manifest gates pass.
- `blocked`: a required source, authority, tool, or render path is unavailable and no safe
  in-scope fallback exists.

Do not infer `reviewed` from a filename. Read the manifest, status, sync check, and QA
evidence.

## Skill Relationships

| Skill/tool | Pattern | Handoff |
|---|---|---|
| GBrain/memory | upstream | recall notes and prior source pointers |
| `you-com-search` | upstream data tap | raw Level 2 captures and search log |
| `pp-firecrawl` / `firecrawl-pp-cli` | upstream data tap | page/site captures and source assets |
| `aianalyst-competitor-analysis` | sequential core | evidence dataset and analytical controls |
| `competitor-analysis-pipeline` | sequential core | story, branded PPTX, HTML, publishing and QA |
| `pptx-visual-spec` | mandatory overlay | validated `visual-spec.json` |
| `branded-pptx-deck` or `genspark-branded-deck` | downstream builder | editable reviewed PPTX |
| `github-pages-publisher` | optional downstream | verified public HTML URL |

## Fail Conditions

Stop promotion to `reviewed` when:

- research notes exist but no evidence ledger exists;
- scores or charts use undefined metrics;
- source coverage is uneven but confidence is hidden;
- visible numbers are absent from `allowed-numbers.yaml`;
- the story pack does not map slides to evidence, scores, or labeled interpretation;
- the final deck is image-only or has zero editable text shapes;
- a requested rework/redesign has no material visible slide-level change;
- PPTX OfficeCLI/render QA is missing;
- HTML is missing, broken, or out of sync with the deck;
- the manifest or `status.json` disagrees with the actual files.
