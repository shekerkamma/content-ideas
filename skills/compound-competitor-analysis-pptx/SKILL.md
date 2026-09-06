---
name: compound-competitor-analysis-pptx
description: Run a compound competitor-analysis-to-client-PowerPoint pipeline spanning GBrain recall, current-source acquisition, AI Analyst evidence controls, scoring, Story Architect, Grill-Me, Meta LOOP, bounded batch authoring, Accenture analytical grammar, per-slide design contracts, native editable PPTX construction, and OfficeCLI plus Microsoft PowerPoint QA. Use for competitor landscapes, threat assessments, battlecards, market maps, diligence dossiers, strategic counter-moves, or deep-research competitor decks that must be traceable and client-ready.
---

# Compound competitor analysis PPTX

Produce a decision-grade presentation system, not a collection of formatted pages. Preserve
research depth in the evidence layer while making each visible slide communicate one analytical
argument through geometry, comparison, causality, sequence, qualification, or decision logic.

## Required skill chain

Use the following stages in order. Announce each material skill action to the user.

1. `GBrain Recall` when available and the company, market, person, or use case may have appeared
   before. Do not replace local deliverable artifacts with GBrain.
2. Research/discovery skill appropriate to the task. Prefer primary and current sources. Write a
   local evidence ledger and distinguish verified facts, company claims, interpretations, and gaps.
3. `presentation-source-bundle` for every supplied PPTX, PDF, webpage, or source presentation.
4. `ai-analyst` or domain analysis skill for metrics, comparisons, scoring, and evidence quality.
5. `story-architect` for BLUF, narrative spine, section logic, counterarguments, and asks.
6. `grill-me` for load-bearing slide-by-slide questions and recommended answers.
7. `meta-loop` when its capability gate passes, to independently classify grill findings, resolve
   conflicts, and approve a rewrite blueprint. Never call a single-model rewrite Meta LOOP.
8. `llm-council` only when a genuine high-stakes strategy/design tradeoff remains after the grill;
   it does not replace evidence verification or Meta LOOP integration.
9. `pptx-design-quality` and `pptx-visual-spec` for deck-wide and per-region design contracts.
10. `branded-pptx-deck` for a new native deck; `pptx-toolkit` only for explicitly surgical edits.
11. `officecli` for validation, issue scanning, HTML snapshots, and native Microsoft PowerPoint render
   QA on Windows.

For competitor-analysis decks, do not invoke this presentation stage directly from raw research.
Read and apply [competitor-analysis-wiring.md](references/competitor-analysis-wiring.md). The default
entry point is `evidence-led-competitor-pipeline`; `aianalyst-competitor-analysis` owns the analytical
data product; `competitor-analysis-pipeline` owns the broader client package; this skill owns the
evidence-to-slide and design-to-PPTX contract.

For multi-skill builds, write and validate `skill-application-manifest.json` using the visible
skill-application contract in `skills/present/references/visible-skill-application-contract.md`.

## Read these references

- Read [workflow.md](references/workflow.md) before starting any material build.
- Read [contracts.md](references/contracts.md) before authoring `slide-plan.json` or design specs.
- Read [accenture-analytical-grammar.md](references/accenture-analytical-grammar.md) before writing
  slide titles, executive answers, comparisons, or recommendations.
- Read [prompt-templates.md](references/prompt-templates.md) before generating slide-level content or
  design prompts.
- Read [design-system.md](references/design-system.md) before implementing layouts.
- Read [officecli-qa.md](references/officecli-qa.md) before promotion or delivery.
- Read [competitor-analysis-wiring.md](references/competitor-analysis-wiring.md) whenever the deck is
  a competitor landscape, benchmark, battlecard, threat assessment, market map, or diligence pack.
- Read [review-control-loop.md](references/review-control-loop.md) before invoking grill-me,
  meta-loop, or an LLM council and before regenerating slide contracts from review findings.
- Read [batch-authoring.md](references/batch-authoring.md) before generating more than eight slide
  content or design envelopes.
- Read [completeness-gates.md](references/completeness-gates.md) before evidence lock and again before
  reviewed promotion.
- Read [example-library.md](references/example-library.md) before drafting prompts or selecting slide
  archetypes. Copy and tailor an example; never treat example claims or numbers as evidence.
- Read [accenture-guide-content-envelope.md](references/accenture-guide-content-envelope.md) before
  writing batch prompts or slide content envelopes. It distills the supplied 24-slide prompt guide
  into a portable competitor-analysis contract.
- Read [v14-native-archetype-contract.md](references/v14-native-archetype-contract.md) before
  selecting or rebuilding DeepGrid competitor slide layouts. The v14 native deck is the design
  authority when it is supplied or named.

## Non-negotiable artifacts

Material builds require these files in the run directory before rendering:

```text
presentation-evidence.json       # source-derived work
evidence-ledger.csv              # claim-level source and status
deck-brief.md
deck-design.json
template-profile.json
slide-plan.json
visual-spec.json
slide-content-contracts.json     # one complete content envelope per slide
slide-design-contracts.json      # one visual/layout prompt per slide
skill-application-manifest.json  # multi-skill builds
claim-slide-traceability.json    # claim/control → contract → rendered region
client-package/delivery-manifest.json
builder source
qa/
```

Copy the templates in `assets/contracts/`, tailor them, and validate them. Do not claim a skill was
applied because it was invoked; its output must visibly affect slide content or design.

For competitor work, initialize the run-stage graph from
`assets/contracts/competitor-skillpipe.template.json`; do not skip directly from raw captures to
slide authoring.

Initialize review artifacts from `assets/contracts/grill-ledger.template.json` and
`assets/contracts/meta-loop-rewrite-blueprint.template.json`. Slide contracts must cite the review
control IDs they implement.

For long decks, initialize `assets/contracts/authoring-batch-manifest.template.json`. Author content
envelopes in bounded batches of no more than four slides, then consolidate and validate globally.
Never ask one prompt to write an entire deep-research deck.

Use `examples/prompts/sample-prompts.md` for invocation patterns,
`examples/completed-contracts/` for filled contract syntax, and
`examples/review-control-traces/` for the required Grill-Me → Meta LOOP → visible-change chain.
Use `assets/slide-archetypes/archetype-catalog.json` to select a governed composition and inspect
`assets/slide-archetypes/deepgrid-v14-native-archetypes-draft.pptx` for the intended visual outcome.
The native example preserves the reviewed DeepGrid v14 master/theme and nine editable design
families while replacing client claims with synthetic content. It is the design authority; do not
create an independent neutral template when v14 is in scope.

The user-supplied guide is preserved byte-for-byte at
`assets/reference-decks/accenture-style-claude-guide-draft.pptx`. Use it as a prompt-envelope and
composition reference only. Do not present it as the client template and do not copy its visible
claims into a deliverable.

## Build rules

- Use the branded template resolved from `BRANDED_PPTX_TEMPLATE`, or the configured branded fallback.
- For supplied reference decks, derive `template-profile.json` from the source and preserve brand
  geometry, typography, color, footer, motif, and composition rules.
- Keep titles, claims, data, diagrams, captions, and citations native/editable when feasible.
- Use exact extracted pixels only when appearance itself is evidence. Never redraw an exact UI,
  source figure, certification, or supplied artwork.
- Use image models only for text-free, non-evidentiary organic imagery. Never generate logos,
  charts, slide text, product proof, people, facilities, or certifications as evidence.
- Put complete sources, caveats, and discarded detail in notes or appendix. Do not shrink a report
  into boxes.
- Never overwrite the source deck. Keep a reproducible builder beside the deliverable.
- Preserve speaker notes and accessibility reading order/alt text. A slide is not complete when its
  visible content is clean but its notes, citations, or accessibility contract is missing.
- Run entity normalization, source-freshness, comparison-scope, allowed-number, internal-term,
  material-change, and delivery-sync gates defined in `completeness-gates.md`.

## Per-slide gate

Every slide must have:

1. one action title that states the answer;
2. one analytical question;
3. one executive answer;
4. evidence blocks with IDs and evidence statuses;
5. explicit comparison, causal, temporal, qualification, or decision logic;
6. strongest counterargument or falsifier;
7. implication, decision, owner, and observable trigger;
8. one dominant analytical exhibit;
9. a design prompt defining grid, focal point, reading flow, encoding, density, hierarchy, and
   prohibited patterns;
10. source notes and speaker notes.

Reject any slide that is only prose arranged into cards. Reject any graphic whose geometry does not
encode meaning. Reject any conclusion that outruns its evidence status.

## Accenture analytical grammar

Apply these rules visibly:

- BLUF: lead with the decision or implication, then prove it.
- Titles are complete assertions, not topics.
- Each page answers a single executive question.
- Compare on buyer-relevant control points, not feature catalogues.
- Separate fact, attributed claim, qualified interpretation, and insufficient evidence.
- State the causal mechanism connecting evidence to implication.
- Make counterarguments and falsifiers visible, not hidden in notes.
- End each section with a decision, owner, trigger, and stop/escalate rule.
- Use parallel grammar across comparable competitor pages.

## Status gates

Use matching filename suffixes:

- `*-draft.pptx`: contracts or build exist, but required QA is incomplete.
- `*-reviewed.pptx`: every required contract validates; structural and design lint is clean; OfficeCLI
  validation and issue scan report zero; all slides were inspected in contact sheets; and a native
  Microsoft PowerPoint render was inspected when the host supports it.
- `blocked`: a required evidence, branded-template, editability, or real-render path is unavailable.

Run the bundled validator:

```bash
python3 skills/compound-competitor-analysis-pptx/scripts/validate_run.py \
  <run-dir> --competitor --reviewed
```

Validate the bundled example library after changing prompts, contracts, or archetypes:

```bash
python3 skills/compound-competitor-analysis-pptx/scripts/validate_examples.py \
  skills/compound-competitor-analysis-pptx
```

Run OfficeCLI QA:

```bash
python3 skills/compound-competitor-analysis-pptx/scripts/officecli_qa.py \
  <deck-draft.pptx> --out <run-dir>/qa/officecli --required
```

On WSL with Windows OfficeCLI and PowerPoint installed, add:

```bash
python3 skills/compound-competitor-analysis-pptx/scripts/officecli_qa.py \
  <deck-draft.pptx> --out <run-dir>/qa/officecli --required --native-windows
```

Only promote after reading the generated `qa-summary.md` and inspecting every contact sheet.

## Competitor-analysis relationships

| Skill | Pattern | Condition | Handoff |
|---|---|---|---|
| `evidence-led-competitor-pipeline` | Orchestrator upstream | default for traceable competitor work | run state, evidence/story gates, manifest |
| `competitor-analysis-pipeline` | Peer upstream | broader competitor package and HTML required | research dossier, story pack, client-package contract |
| `aianalyst-competitor-analysis` | Sequential upstream | evidence, metrics, scoring, confidence required | ledger, metric definitions, quality report, scoring model, allowed numbers |
| `enterprise-ai-competitor-landscape` | Optional upstream | 100–150 company Enterprise AI universe | normalized company universe and market-map analysis |
| `investor-competitive-dossier` | Optional upstream | investor/startup diligence use case | investment thesis, cohort dossier, diligence gaps |
| `story-architect` | Sequential upstream | always after evidence lock | BLUF, slide spine, evidence map, content cuts |
| `grill-me` | Amplifier upstream | always before design lock | question/answer ledger and atomic visible-change controls |
| `meta-loop` | Sequential integration | 3+ independent review/classification subtasks and capability gate passes | verified finding ledger, dispositions, final rewrite blueprint |
| `llm-council` | Optional decision review | genuine high-stakes tradeoff remains after grill/meta-loop | recommendation, dissent, first action |
| `pptx-visual-spec` | Mandatory peer | every build | validated region routing and provenance |
| `branded-pptx-deck` | Sequential downstream | fully native client PPTX | editable draft/reviewed deck and builder |
| `competitor-analysis-pipeline` | Sequential downstream | HTML/battlecard/public client package required | synchronized HTML, deck, manifest |
| `officecli` | QA downstream | every reviewed PPTX | validation, issue report, HTML/native contact sheets |
| GBrain Write-back | Knowledge downstream | durable findings likely to recur | sourced reusable findings, never deliverables |
