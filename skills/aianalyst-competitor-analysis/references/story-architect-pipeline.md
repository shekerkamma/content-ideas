# Story Architect Pipeline For Competitor Analysis

Use this pipeline after the evidence ledger, metric definitions, data-quality report, scoring model, and competitor brief exist. It is mandatory before building client PPTX or HTML artifacts.

## Inputs

Read:

- `outputs/evidence-ledger.csv`
- `outputs/evidence-ledger.md` when present
- `outputs/metric-definitions.md`
- `outputs/data-quality-report.md`
- `outputs/scoring-model.md`
- `outputs/competitor-brief.md`
- `outputs/allowed-numbers.yaml` when deck/HTML will contain visible numbers
- user requirements such as slide count, audience, brand, publish target, and critique

Do not build a story from memory when these files exist. The story pack must be traceable to them.

## Required Artifact

Write `outputs/story-architect-pack.md` with these sections:

1. **BLUF**
   One sentence that answers the executive question. It should say what the target should do or believe, not just describe the category.

2. **Audience Decision**
   The decision the reader should make: invest, compete, reposition, partner, de-risk, fund proof, change roadmap, or brief sales/product teams.

3. **Tension**
   Why the decision matters now. Name the external force, buyer expectation, incumbent compression risk, proof gap, or market timing.

4. **Argument Arc**
   Five to eight ordered beats:
   - context
   - analytical method
   - evidence coverage
   - market/arena structure
   - heatmap or score result
   - differentiation and compression risk
   - strategic choices
   - proof plan / next action

5. **Slide Spine**
   One row per proposed slide or HTML section:

   | # | Assertion title | Role in story | Evidence rows | Metric(s) | Visual treatment | Speaker implication |
   |---|---|---|---|---|---|---|

   Rules:
   - Titles must be assertions, not labels.
   - Each row must cite evidence `claim_id`s, metric names, or `interpretation` with confidence.
   - Datapoint-heavy slides must name which datapoint families they carry.
   - Breathing/setup slides are allowed, but their role must be explicit.

6. **Evidence Map**
   Group claims as:
   - direct evidence: sourced row supports the claim directly
   - fair synthesis: several rows support a summarized pattern
   - interpretation: analyst judgment based on evidence, must be softened
   - unsupported: cut, search again, or mark as assumption

7. **Datapoint Promotion Map**
   List which extracted datapoints will appear in the main artifacts.

   | Datapoint / claim_id | Main artifact location | Why it matters | Confidence |
   |---|---|---|---|

   At minimum, promote:
   - top target proof points
   - top competitor threat datapoints
   - evidence coverage summary
   - one quantified or structured proof point per major arena where available
   - missing datapoints that change confidence or next-step recommendations

8. **Content Cuts**
   Explicitly name what should not go into client-facing slides:
   - weak or duplicate claims
   - raw tool notes
   - unsupported market adjectives
   - appendix-only evidence that does not change the argument
   - internal file paths or process terms unless the user asks for an audit appendix

9. **Rebuild Instructions**
   Concrete instructions for the PPTX/HTML builder:
   - section order
   - slide count target
   - chart/table treatments
   - evidence/datapoint slides to include in the main flow
   - Genspark Slides prompt inputs when hosted editable delivery is required
   - allowed-number list with required caveats for every visible quantitative claim
   - requirement that final visible deck/HTML numbers must come from `outputs/allowed-numbers.yaml`
   - banned unsupported datapoint families, such as ROI, market size, pricing, ARR, growth, implementation cost, or arbitrary competitor percentages when not sourced
   - `genspark-branded-deck` recreation instructions: deck source path, target theme, hybrid-editable or native-PowerPoint path, contact-sheet QA expectations
   - self-contained HTML instructions: required sections, interactions, local path, GitHub Pages publish path, and URL verification requirement
   - required PPTX output name and reviewed/draft status
   - required HTML local path and publish URL target
   - what to avoid
   - QA checks that must pass

10. **Storyboard QA**
    Answer:
   - Does every slide have a reason to exist?
   - Does the first substantive slide answer the executive question?
   - Are datapoints reflected in the main story, not only appendix/supporting material?
   - Does every chart or score trace to a defined metric?
   - Are weak-confidence claims labeled or removed?
   - Can a reader understand the recommendation without reading raw sources?

## Competitor Story Patterns

Choose the pattern that best fits the decision.

### Positioning Strategy

Use when the target needs to clarify differentiation:

1. BLUF / recommendation
2. Buyer job and category confusion
3. Competitor arenas
4. Evidence coverage and confidence
5. Heatmap
6. Where target wins
7. Where incumbents compress
8. Proof gaps
9. Roadmap / actions

### Sales Battlecard

Use when field teams need objections and counters:

1. Executive answer
2. Buyer trigger events
3. Threat ranking
4. Arena-by-arena battlecards
5. Proof points and caveats
6. Objection handling
7. Discovery questions
8. Proof-plan asks

### Investor / Board Narrative

Use when the output supports funding or strategy:

1. Category thesis
2. Why now
3. Competitive map
4. Evidence-backed differentiation
5. Distribution and incumbent risk
6. Proof quality and gaps
7. Strategic options
8. Next-quarter proof plan

### Consulting / SI Comparison

Use when Accenture, BCG, Deloitte, IBM, McKinsey, or SIs shape buyer expectations:

1. Buyer expectation created by consulting/SI offers
2. Product vs service-delivery comparison
3. Proof and trust gap
4. Partner/compete/attach choice
5. How the target should position against services-led transformation

## Fail Conditions

Do not proceed to PPTX/HTML build if:

- there is no BLUF
- the slide spine is topic labels instead of assertions
- evidence rows do not map to slides
- datapoint promotion is missing
- allowed-number guidance is missing when a generated deck is required
- `outputs/allowed-numbers.yaml` is missing while visible numbers are planned
- final branded deck recreation instructions are missing when PPTX is required
- self-contained HTML instructions are missing when client-ready delivery is required
- the deck would be vendor-by-vendor chronology instead of a decision story
- the recommendation does not follow from evidence, scoring, and proof gaps
