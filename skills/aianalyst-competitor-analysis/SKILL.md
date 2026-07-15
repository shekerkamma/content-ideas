---
name: aianalyst-competitor-analysis
description: "Use when the user wants competitor analysis run as an AI Analyst evidence-dataset workflow: competitive landscape, benchmarking, battlecards, market map, positioning analysis, consulting-firm comparisons, KPI/evidence-led differentiation, or client-ready PPTX/HTML outputs where sourced web evidence, internal datasets, metrics, confidence scoring, and AI Analyst dataset conventions must be used together."
---

# AI Analyst Competitor Analysis

Run competitor analysis as a data product: sources become an evidence dataset, metrics are defined before scoring, findings are validated like analysis outputs, and client artifacts are generated only after QA.

Use this skill when competitor work needs deeper quantitative/evidence handling than `competitor-analysis-pipeline` alone. Read [references/prompt-fit-checklist.md](references/prompt-fit-checklist.md) and [references/effective-competitor-analysis-prompt.md](references/effective-competitor-analysis-prompt.md) before framing the analytical question. Read [references/dataset-contract.md](references/dataset-contract.md) before building or revising the evidence ledger. Read [references/you-com-search-plan.md](references/you-com-search-plan.md) before running You.com discovery or livecrawl retrieval. Read [references/datapoint-extraction.md](references/datapoint-extraction.md) before extracting quantitative proof from crawled pages, PDFs, press releases, case studies, reviews, or internal datasets. Read [references/story-architect-pipeline.md](references/story-architect-pipeline.md) before building the PPTX or HTML storyboard. Read [references/genspark-slides-delivery.md](references/genspark-slides-delivery.md) before using hosted Genspark AI Slides. Read [references/final-client-delivery.md](references/final-client-delivery.md) before building the final branded PPTX, self-contained HTML, or GitHub Pages package. Read [references/quality-gates.md](references/quality-gates.md) before rendering or publishing client artifacts.

## Runtime Preamble

State that this run will use the AI Analyst competitor-analysis pipeline: recall, research-tool discipline, evidence ledger as dataset, metric definitions, source tieout, confidence scoring, story review, branded PPTX, interactive HTML, and publish/open QA.

## Required Outputs

Create or update a self-contained run folder:

```text
runs/<YYYY-MM-DD>-<target>-aianalyst-competitor-analysis/
├── inputs/
├── working/
├── outputs/
│   ├── evidence-ledger.csv
│   ├── evidence-ledger.md
│   ├── metric-definitions.md
│   ├── data-quality-report.md
│   ├── competitor-brief.md
│   ├── scoring-model.md
│   ├── story-architect-pack.md
│   ├── storyboard-qa.md
│   └── artifact-traceability.md
├── client-package/
│   ├── build_deck.py
│   ├── *-draft.pptx
│   ├── *-reviewed.pptx
│   ├── genspark-deck/
│   │   ├── deck.html
│   │   ├── theme.css
│   │   ├── deck.css
│   │   └── build/
│   ├── site/index.html
│   ├── pages/<slug>/index.html
│   ├── delivery-manifest.json
│   └── qa/
└── status.json
```

If the user is continuing an existing run, preserve its folder and add missing AI Analyst outputs instead of starting over.

## Workflow

1. **Frame the analytical question.**
   Convert the request into a decision question, audience, target company/product, competitor arenas, geography, timeframe, required artifacts, and success criteria. If the user asks for a minimum slide count, treat it as a hard requirement.
   First run the prompt-fit checklist. Then fill the effective competitor-analysis prompt from [references/effective-competitor-analysis-prompt.md](references/effective-competitor-analysis-prompt.md). If the user's prompt is a launch report, market report, generic vendor list, or oversized template, compress it into this competitor-analysis decision prompt before research or writing. Save the operating prompt in `inputs/operating-prompt.yaml` and, when the original prompt was changed, save `outputs/prompt-fit-review.md`.

2. **Run recall before new research.**
   Use GBrain/durable memory and repo-local prior runs first. Record recall status in `status.json` or run notes. If GBrain is unavailable, continue and document the fallback.

3. **Use research-tool order.**
   Do not begin with generic search. Prefer local artifacts, GBrain, `you-com-search` Level 2 livecrawl, You.com Level 1/3 as appropriate, Exa, Firecrawl/content-research/STORM, official sources, then generic search only for targeted verification or fallback. Use [references/you-com-search-plan.md](references/you-com-search-plan.md) for query templates, search logs, and livecrawl API naming. Save raw captures or JSON in `outputs/` or `working/`.

4. **Create the evidence dataset.**
   Treat every useful source claim as a row in `outputs/evidence-ledger.csv`. Use the schema in [references/dataset-contract.md](references/dataset-contract.md). The ledger must include competitor, arena, source URL, source type, metric family, metric value/unit when present, extracted claim, confidence, evidence strength, and storyboard use.

5. **Extract specific datapoints.**
   Use [references/datapoint-extraction.md](references/datapoint-extraction.md) to mine metrics from source captures. Extract hard numbers, implied metrics, benchmarks, named customer proof, pricing, funding, trust/compliance markers, distribution proof, integration depth, adoption/review counts, and time/ROI/support-productivity claims. Normalize units and keep the original claim text. Do not lose non-numeric but decision-relevant datapoints such as certifications, partner ecosystems, implementation model, buyer segment, or deployment constraints.

6. **Register dataset context when useful.**
   If the run will use AI Analyst-style analysis or repeated queries, create `.knowledge/datasets/<dataset_id>/` with `manifest.yaml`, `schema.md`, `quirks.md`, and `metrics/index.yaml`, or point to an existing active dataset. Never store credentials in dataset files.

7. **Define metrics before scoring.**
   Write `outputs/metric-definitions.md` for any metric used in charts, heatmaps, ranking, or recommendations. Include formula, numerator/denominator where relevant, unit of analysis, source columns, exclusions, limitations, and confidence basis.

8. **Run data quality and source tieout.**
   Produce `outputs/data-quality-report.md` with row counts, coverage by competitor, source type mix, metric-family coverage, missing values, duplicate claims, stale sources, primary-source share, vendor-published share, and evidence gaps. Halt or label `draft` if important claims are not source-backed.

9. **Build the scoring model.**
   Write `outputs/scoring-model.md` with the scoring rubric, weights, scale definitions, evidence inputs, sensitivity notes, and confidence labels. Score competitors on the same dimensions. Do not mix scored evidence with unsupported opinion.

10. **Synthesize the competitive answer.**
   Produce `outputs/competitor-brief.md` with:
   - executive answer
   - competitor arenas by buyer job
   - evidence-backed heatmap
   - quantified datapoints that drive the story
   - where the target wins
   - where incumbents can compress the position
   - proof gaps and recommended proof plan
   - compete/partner/attach/avoid guidance

11. **Run the story-architect pipeline.**
    Use [references/story-architect-pipeline.md](references/story-architect-pipeline.md) and the `story-architect` skill to create `outputs/story-architect-pack.md` before any deck/page build. The pack must contain BLUF, audience decision, tension, argument arc, slide spine, evidence map, datapoint promotion map, content cuts, rebuild instructions, and storyboard QA. Every proposed slide or HTML section must map to evidence rows, defined metrics, or clearly labeled interpretation.

12. **Use review gates.**
    Apply `grill-me` to structure, storyboard, content quality, scoring logic, and whether datapoints are actually reflected in the narrative. Re-run or amend the story-architect pack if grill-me changes the BLUF, argument arc, slide order, evidence map, or content cuts. Use AI Analyst validation concepts: source tieout, triangulation, guardrails, semantic validation, and close-the-loop follow-up plan.

13. **Run artifact readiness gates.**
    Use [references/quality-gates.md](references/quality-gates.md). Do not build PPTX/HTML until required analytical outputs exist, traceability is mapped, datapoint coverage is summarized, search-again triggers are resolved or explicitly waived, and the story-architect pack reflects the latest grill-me critique.

14. **Build client artifacts.**
    Use [references/final-client-delivery.md](references/final-client-delivery.md). When hosted generation is useful or requested, first use `genspark-slides` / Genspark AI Slides for deck generation, expansion, and recoverable editable project creation. Feed it the validated story-architect pack, evidence-led datapoints, final slide spine, allowed-number list, and banned unsupported datapoints; then recover/capture the generated slides, QA them, and keep the Genspark project URL as an upstream editable/reference artifact. If Genspark under-generates, request one expansion pass with specific missing sections. If unsupported datapoints remain after the first correction pass, stop regenerating and clean the recovered artifact deterministically using [references/genspark-slides-delivery.md](references/genspark-slides-delivery.md).

    Final delivery must then recreate/package the deck through `genspark-branded-deck` from owned `deck.html`, `theme.css`, and `deck.css`, using the evidence-clean story and recovered Genspark output only as reference. The final delivery PPTX must be editable: use the `genspark-branded-deck` hybrid-editable path at minimum, or `branded-pptx-deck` when fully native editable PowerPoint shapes/charts are required. Image-only PPTX exports are allowed only as QA/reference drafts, not final delivery. Do not stop at a hosted Genspark URL or recovered export when a client-ready final package is required. Build a self-contained interactive HTML report at `client-package/site/index.html` and, when a shareable URL is requested, stage/publish it through the GitHub Pages path. The datapoints and evidence rows must appear in main narrative sections, not only in appendix or notes.

15. **QA, publish, and manifest.**
    Run branded-deck render/contact-sheet QA, mandatory OfficeCLI QA for reviewed PPTX status, text-overflow checks, and Playwright HTML navigation checks. If OfficeCLI is unavailable or fails for environmental reasons, keep the PPTX status `draft` or `blocked` unless the user explicitly accepts an unreviewed deck. If publishing to GitHub Pages, push the final self-contained HTML and verify the live URL with a cache-busting query string. Write `client-package/delivery-manifest.json` with hosted Genspark URL when used, branded deck source path, PPTX path, slide count, local HTML path, public HTML URL, commit SHA when published, OfficeCLI result path/status, QA status, sync status, and artifact status.

## AI Analyst Rules

- Treat external research as data, not prose notes.
- Use the prompt-fit checklist to prevent overbroad launch-report prompts from driving competitor-analysis outputs. A long prompt can be kept as a QA checklist, but the operating prompt must center on the competitive decision.
- Use the effective competitor-analysis prompt as the default operating prompt, not a broad launch-report or generic market-map prompt.
- Use explicit dataset IDs, schemas, metric specs, row counts, and confidence labels.
- Preserve raw evidence enough to rerun or audit the analysis.
- Capture both numeric datapoints and structured qualitative datapoints; many competitor signals are binary, categorical, dated, or named-customer proof rather than pure metrics.
- Every client-facing slide and HTML section must trace to evidence rows, defined metrics, or explicitly labeled synthesis/interpretation.
- Use charts only when the underlying ledger has enough comparable rows.
- Prefer primary/current sources for volatile facts such as pricing, funding, leadership, product claims, and customer proof.
- Distinguish vendor-published proof, third-party proof, analyst proof, and internal/customer proof.
- If internal CRM/product/support data is supplied, connect it as a separate dataset and join only through explicit keys or documented assumptions.
- Do not claim precision from scraped/web evidence that the data cannot support.
- Supported numbers must be plugged into the deck/report with the correct source label and caveat; unsupported numbers must be removed or replaced with qualitative language.
- Do not repeatedly ask Genspark to regenerate slides to repair evidence issues. Use a bounded generation loop, then deterministic cleanup and QA.
- Final client delivery requires both a recreated branded PPTX through `genspark-branded-deck` and a self-contained HTML artifact unless the user explicitly scopes one artifact out.
- Hosted Genspark output is useful upstream, but it is not the complete final delivery package by itself.
- Final delivery slides must be editable and must use evidence-based numbers from upstream AI Analyst dataset artifacts: `evidence-ledger.csv`, `metric-definitions.md`, `data-quality-report.md`, `scoring-model.md`, `competitor-brief.md`, and `story-architect-pack.md`.
- Image-only slide exports are not acceptable final deliverables unless the user explicitly waives editability; keep them as drafts or QA references.

## Output Standards

Use explicit status:

- `draft`: generated but not fully validated
- `reviewed`: evidence dataset, story, deck, HTML, and QA checks passed
- `blocked`: required data, source access, or rendering path is unavailable

Final response must include:

- run folder
- evidence ledger row count
- PPTX path and slide count
- branded deck source path
- HTML local path and public URL when client-ready sharing was requested
- delivery manifest path
- QA status, including OfficeCLI status for PPTX
- review gates used
- top differentiated answer in 2-4 bullets

## Skill Relationships

### Dependencies

- `competitor-analysis-pipeline` for the broader client-ready competitor workflow
- `you-com-search` or equivalent specialist research tool for evidence collection
- `ai-analyst` conventions for dataset, metric, validation, and presentation discipline
- `grill-me` for pressure-testing
- `story-architect` for storyboard
- `genspark-slides` for Genspark AI Slides generation, recovered HTML, editable hosted project, and visual/export QA
- `genspark-branded-deck` for final branded PPTX recreation from owned HTML/CSS after evidence cleanup, using its hybrid-editable path for final delivery
- `branded-pptx-deck` when the client needs fully native PowerPoint shapes/charts or re-layoutable slides

### Handoffs

| Skill | Pattern | Handoff |
|---|---|---|
| `you-com-search` | upstream evidence retrieval | raw captures, `evidence-ledger.csv` |
| `ai-analyst/run-analysis` concepts | embedded analysis method | metric definitions, data quality report, scoring model |
| `grill-me` | review gate | structure/content/scoring critique |
| `story-architect` | mandatory narrative pipeline | BLUF, audience decision, tension, argument arc, slide spine, evidence map, content cuts, rebuild instructions |
| `genspark-slides` | upstream hosted slide generation/reference | Genspark project/viewer, recovered slide HTML, rendered references, QA notes |
| `genspark-branded-deck` | downstream final PPTX recreation | branded `deck.html`, `theme.css`, `deck.css`, contact-sheet QA, hybrid-editable `*-reviewed.pptx`; image exports only as draft/reference |
| `branded-pptx-deck` | alternate downstream PPTX rebuild | fully native/re-layoutable `*-reviewed.pptx` when explicitly required |
| `competitor-analysis-pipeline` | peer/base pipeline | publishing and delivery QA |

## Gotchas

- **Launch-report trap:** do not let sections such as supply chain, packaging design, generic launch tactics, or market-size theater distract from the competitive decision. Use them only if they directly affect the competitor analysis.
- **Volume trap:** a 12,000-18,000 word target can produce a worse answer when the decision requires a tight brief, battlecard, or proof plan. Prefer decision density over length.
- **Appendix trap:** evidence-led datapoints belong in the main storyline; an appendix can support, not carry, the argument.
- **Story-pipeline trap:** do not jump from evidence ledger to PPTX. Build and QA the story-architect pack first, then render artifacts from that slide spine.
- **Traceability trap:** do not ship slides or sections that cannot be traced to `claim_id`s, defined metrics, or labeled interpretation.
- **Extraction trap:** do not only extract `%` values. Funding, pricing, customer counts, integrations, certifications, named customers, review counts, deployment time, partner networks, and dated product launches are all competitor datapoints.
- **Metric trap:** do not chart or rank on an undefined metric.
- **Coverage trap:** a heatmap is misleading if some competitors have much better source coverage than others; label confidence or rebalance.
- **Vendor-proof trap:** case studies and vendor pages are useful but must be labeled as vendor-published unless independently verified.
- **Dataset trap:** do not use `.knowledge` files for secrets or raw credentials.
- **Generic-search trap:** generic web search is fallback/verification, not the starting point.
- **Genspark-regeneration trap:** repeated slide regeneration can introduce new unsupported metrics. Expand once when scope is thin, then patch recovered slide content deterministically.
- **Editable-export trap:** a local image-based PPTX export from Genspark capture is not the editable source of truth. The hosted Genspark project is editable unless a native PowerPoint rebuild is performed.
- **Unsupported-number trap:** do not leave supported numbers out and do not keep unsupported numbers in. Maintain an allowed-number list and scan visible slide text before delivery.
- **Final-package trap:** do not call the run delivered after a Genspark project or PPTX alone. Final delivery includes a recreated `genspark-branded-deck` PPTX plus self-contained HTML, with GitHub Pages publication when requested.
- **Image-deck trap:** do not deliver image-only slides as the final PPTX. Final client decks must be editable and must carry evidence-based numbers from the AI Analyst artifacts.
