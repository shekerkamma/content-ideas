# Analysis Contract

Binding rules for run layout, findings, grading, and report structure.

## Run layout

```
runs/<YYYY-MM-DD>-<subject>-model-review/
  inputs/
    <original workbook copy>        # never edit the source in place
    operating-prompt.yaml           # decision, audience, scope, deadline
  outputs/
    extract.md                      # human-readable workbook dump
    extract.json                    # structured dump
    spec.json                       # integrity spec (series + identities)
    integrity.txt                   # gate output, verbatim
    integrity.json                  # gate findings
    benchmark-log.md                # every external query, source, and result
    findings.md                     # graded finding register
    decision-memo.md                # the deliverable
  status.json                       # stages run, skipped, blocked
```

Copy the source workbook into `inputs/` before anything else. Analysis never
mutates the artifact under review.

## Finding schema

Every finding carries all seven fields. A finding missing any of them is not
ready to report.

| Field | Meaning |
|---|---|
| `id` | `F-01`, stable across revisions of the memo |
| `class` | `model-internal` or `world-facing` |
| `grade` | `Verified`, `Benchmarked`, or `Judgement` |
| `claim` | One sentence, falsifiable, no hedging |
| `evidence` | Cell reference / re-derived arithmetic / cited source |
| `materiality` | What it changes, quantified where possible |
| `action` | Correct, disclose, investigate, or accept |

## Grading

**Verified** — re-derived from the file itself. Arithmetic breaks, failed
cross-sheet ties, internal contradictions between a prose note and the numbers.
The strongest grade: it needs no outside agreement to hold.

**Benchmarked** — checked against a cited external source. Requires the source,
its date, and why the comparison is apt. A comparable that is not actually
comparable is a `Judgement` wearing a citation.

**Judgement** — analyst opinion. Legitimate and often the most valuable part of
the review, but it must be labelled so a reader can discount it. Never let a
`Judgement` inherit the authority of a `Verified` finding by sitting next to one
unlabelled.

## Materiality

Distinguish three tiers, and never inflate:

- **Blocking** — changes the decision. An arithmetic break in a headline figure,
  a driver that cannot hold, a reconciliation that fails against a document
  already circulated to third parties.
- **Material** — changes the magnitude but not the direction.
- **Noise** — rounding, presentation, labelling. Report in an annex; do not spend
  the reader's attention on it.

Rounding drift within the model's own precision is **noise by definition**. Say
so explicitly rather than listing it as a finding — a report that treats ±0.01
as a discovery loses credibility for the findings that matter.

## Report structure

1. **Decision and recommendation** — first, in full, before any methodology.
2. **What would have to be true** — the two or three load-bearing assumptions.
3. **Blocking findings** — each with evidence and required action.
4. **Material findings** — grouped by driver, not by sheet.
5. **What the model does well** — genuine strengths, stated plainly. A review
   that finds only faults reads as adversarial and gets discounted wholesale.
6. **Risk register** — owners and triggers.
7. **Annex** — integrity gate output verbatim, benchmark log, noise-tier items.

## Prohibited

- Presenting a model summary as an analysis. Restating the numbers is not review.
- Interpreting past an unexplained integrity break.
- Ungraded world-facing claims.
- Quoting a figure that appears in more than one sheet without stating which
  sheet it came from, when the sheets disagree.
- Recommending a decision the requested scope does not support. If the workbook
  has no cash-flow statement, the review cannot opine on funding adequacy — say
  what is missing instead of inferring it.
