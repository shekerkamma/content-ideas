# Bounded batch authoring and synthesis

## Why batching is mandatory

A long single generation loses evidence boundaries, repeats language, weakens later slides, drifts
from the narrative spine, and returns shallow or malformed envelopes. Batch authoring is a semantic
control, not merely a token workaround.

Use bounded batches whenever the deck has more than eight slides or the content contracts contain
multiple evidence blocks, counterarguments, decisions and design instructions.

## Default batch protocol

- Content-envelope batch size: maximum four slides.
- Design-envelope batch size: maximum four slides.
- Process batches sequentially in narrative order unless independent appendices can safely run in
  parallel.
- Give every batch the deck-level invariant packet plus local slide inputs.
- Give each batch the prior two titles/contracts and next two planned titles so transitions remain
  coherent.
- Require strict JSON matching the contract schema; prohibit commentary around the JSON.
- Allow a larger output budget when the batch must classify many source statements. Do not truncate
  evidence to satisfy an arbitrary response limit.

## Global invariant packet

Every batch receives the same frozen packet:

```text
audience and decision
BLUF and tension
authoritative slide sequence
evidence-status definitions
allowed-numbers list
metric/scoring definitions
Accenture analytical grammar
content and design schemas
review controls and Meta LOOP dispositions
template profile and design direction
visible-word and evidence-block limits
prohibited claims, patterns and internal terms
```

Hash or version this packet. All batch outputs must record its version. If a governing invariant
changes, identify and rerun every affected batch rather than silently mixing versions.

## Batch input

Each slide in the batch must include:

- slide ID, section and story role;
- predecessor and successor titles;
- mapped evidence rows and permitted numbers;
- applicable Grill-Me control IDs;
- Meta LOOP disposition and rewrite instructions;
- required analytical operation and candidate exhibit;
- content to preserve, cut, merge or move to notes/appendix;
- slide-specific acceptance tests.

Do not give a batch the entire unfiltered research corpus. Supply only mapped evidence plus the
global ledger locator for verification.

## Content batch prompt

Use the content-envelope prompt from `prompt-templates.md` and add:

```text
Batch ID: {batch_id}
Invariant version: {invariant_version}
Slides in this batch: {slide_ids}
Previous context: {previous_two_contracts}
Next planned titles: {next_two_titles}
Applicable review controls: {control_records}

Return one complete contract per requested slide. Do not omit fields, merge slides, renumber slides,
or introduce evidence not mapped to that slide. Keep every evidence block bounded and traceable.
```

## Design batch prompt

Run only after the corresponding content batch passes validation. Add:

```text
Treat each slide independently. Do not select a layout merely because another slide in the batch
uses it. Preserve comparable geometry only for explicitly comparable dossier pages. Each design
prompt must bind the slide's exact visual thesis, evidence statuses, comparison logic, decision and
review controls.
```

## Per-batch validation

Before accepting a batch, check:

- requested slide IDs equal returned slide IDs;
- no duplicates, omissions or renumbering;
- every required field is populated;
- 2–4 evidence blocks per substantive slide;
- every evidence ID exists and is allowed for that slide;
- every number appears in `allowed-numbers.yaml`;
- evidence statuses use the canonical vocabulary;
- every applicable review control is implemented or explicitly deferred;
- title, answer, counterargument, implication and decision are not paraphrases of one another;
- content and visible-word budgets are respected;
- no unsupported ranking or unbounded claim appears.

Reject and rerun only the failed batch with exact failed criteria. Do not regenerate passing batches.

## Cross-batch synthesis

After all batches pass, consolidate in authoritative slide order and run global checks:

1. slide count, unique IDs and sequence match the rewrite blueprint;
2. section transitions and title-only story are coherent;
3. duplicate titles, claims, evidence blocks and recommendations are identified;
4. parallel competitor pages use parallel grammar and like-for-like scopes;
5. evidence coverage and confidence are balanced across competitors;
6. every Grill-Me control has one implementation disposition;
7. every Meta LOOP rewrite instruction maps to a resulting contract;
8. owners, triggers, decisions and stop rules are complete;
9. appendix/core-story boundaries are respected;
10. content contracts and design contracts have one-to-one slide mapping.

Write a consolidation validation report. The consolidated file—not individual batch files—is the
only input accepted by the builder.

Run the bundled structural validator:

```bash
python3 skills/compound-competitor-analysis-pptx/scripts/validate_authoring_batches.py \
  <run> --manifest authoring/batch-manifest.json \
  --json-out authoring/validation/consolidation.json
```

## Batch output structure

```text
authoring/
  invariant-packet.json
  batch-manifest.json
  content/
    batch-001.json
    batch-002.json
  design/
    batch-001.json
    batch-002.json
  validation/
    batch-001-content.json
    batch-001-design.json
    consolidation.json
slide-content-contracts.json
slide-design-contracts.json
```

Store raw model output separately from validated normalized output when normalization is required.

## Failure conditions

Block build when:

- a batch is truncated or malformed;
- slide IDs are missing or duplicated;
- two batches use different invariant versions without an approved migration;
- evidence or numbers cannot be traced;
- consolidation overwrites richer contracts with shorter summaries;
- a global review finding is absent from every batch;
- the builder consumes batch fragments rather than the consolidated validated contracts.
