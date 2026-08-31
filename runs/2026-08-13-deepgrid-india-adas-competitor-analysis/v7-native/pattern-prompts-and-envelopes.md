# Seven patterns — prompt + content envelope each

Grammar borrowed from the supplied guide (`WHEN TO USE · WORKFLOW · KEY PROMPT ·
OUTPUT INCLUDES`). The patterns themselves are **derived from this deck's
content**, not imposed: each one exists because 73 slides were profiled and that
structure was actually found in them.

Each pattern below carries two operational things:

- a **KEY PROMPT** — copy-paste, bracketed variables, states the required ending
- a **CONTENT ENVELOPE** — the exact field schema the prompt must return

The envelope is what makes the pattern real. It differs per pattern by design,
because a different envelope is what forces a different exhibit. One envelope for
every slide is what produced 74 identical pages.

| Pattern | Slides | Envelope's distinguishing field | Exhibit it draws |
|---|---:|---|---|
| P1 Evidence Ladder | 21 | `rungs[].confidence` | rung width = confidence |
| P2 Threat × Arena | 11 | `matrix.cells[].rating` | cell colour + bar = rating |
| P3 Staged Move | 18 | `stages[].reversible` | numbered chain, arrows |
| P4 Bounded Argument | 18 | `positions[].stance` | three-column stance bar |
| P5 Dated Plan | 2 | `phases[].span_weeks` | timeline rail, spans to scale |
| P6 Cost Bridge | 2 | `steps[].value` + `verified` | waterfall, height = magnitude |
| P7 Confidence Register | 1 | `claims[].importance × evidence` | scored dot register |

Shared across every pattern (the spine that never varies):
`slide_id · kicker · action_title · analytical_question · executive_answer ·
counterargument · falsifier · implication · decision · owner · trigger ·
stop_or_escalate_rule · evidence_ids[] · speaker_notes`.

---

## P1 · EVIDENCE LADDER — 21 slides

**WHEN TO USE**
- A competitor or claim is described with mixed-quality evidence
- Leadership is treating a company statement as a verified fact
- The rating rests on what is *known* versus what is *asserted*

**WORKFLOW**
1. Split every statement into verified fact · attributed claim · qualified interpretation · insufficient evidence
2. Assign each a confidence, and say what artifact would raise it
3. Convert the weakest load-bearing rung into the decision

**KEY PROMPT**
> "Build an evidence ladder for [subject] as of [date] using only [evidence IDs].
> Produce four rungs ordered strongest to weakest. For each rung give the label,
> the statement in one sentence, its status (verified fact / attributed claim /
> qualified interpretation / insufficient evidence), a confidence between 0 and 1,
> and the named artifact that would raise it. Do not merge rungs of different
> status. End with the response decision, the owner, and the artifact that moves
> the rating."

**CONTENT ENVELOPE**
```json
{
  "pattern": "evidence-ladder",
  "observable_position": "one paragraph — what is visibly true",
  "rungs": [
    { "label": "≤40 chars",
      "text": "one sentence",
      "status": "verified fact | attributed claim | qualified interpretation | insufficient evidence",
      "confidence": 0.0,
      "raises_it": "named artifact, not a category",
      "evidence_ids": ["S00-00"] }
  ],
  "gap": "the artifact whose absence holds the rating"
}
```
Rules: exactly 4 rungs · descending `confidence` · at least one `insufficient
evidence` rung or the ladder is not doing its job.

---

## P2 · THREAT × ARENA MATRIX — 11 slides

**WHEN TO USE**
- A competitor's power differs by who is buying
- Effort is allocated by brand rather than by arena
- One threat rating is hiding where exposure actually sits

**WORKFLOW**
1. Fix the arenas and the control point each one rewards
2. Rate the competitor per arena against that control point, with the fact behind it
3. Name the arena to defend, the arena to concede, and the inversion signal

**KEY PROMPT**
> "Rate [competitor] across [arenas] on the control point each arena rewards. For
> every cell give a rating from HIGHEST / HIGH / MEDIUM-HIGH / MEDIUM /
> LOW-MEDIUM / LOW and the single fact behind it in under twelve words. Explain in
> one sentence why the rating changes between arenas — the mechanism, not a
> restatement. End with the arena to defend, the arena to concede, and the signal
> that would invert the ranking."

**CONTENT ENVELOPE**
```json
{
  "pattern": "threat-arena",
  "matrix": {
    "arenas": ["Government / PSU", "OEM / Tier-1", "Fleet / Mining"],
    "rows": [ { "dimension": "≤26 chars",
                "cells": [ { "rating": "HIGH", "note": "≤46 chars", "evidence_ids": ["S00-00"] } ] } ]
  },
  "variance_mechanism": "one sentence — why the rating moves between arenas",
  "defend": "arena", "concede": "arena",
  "inversion_signal": "the observable that would flip the ranking"
}
```
Rules: every cell needs a `rating` **and** a `note` · `variance_mechanism` must
name a mechanism, not repeat the ratings.

---

## P3 · STAGED MOVE — 18 slides

**WHEN TO USE**
- A bounded action is being proposed against a rival or partner
- The move must be testable and abandonable, not open-ended
- Sales or BD needs a sequence, not a feature comparison

**WORKFLOW**
1. State the rival's advantage as a mechanism
2. Design the narrowest sequence that tests it, marking what is reversible
3. Set the gate that escalates and the condition that abandons

**KEY PROMPT**
> "Design a bounded staged move for [company] against [competitor/opportunity].
> Give 3–4 stages in order. For each: a label of at most 30 characters, what
> happens in one sentence, whether it is reversible, and its cost or commitment
> level. The final stage must be a decision gate with an explicit escalate
> condition. State their advantage as a mechanism first. End with the abandonment
> rule — do not propose a feature-for-feature response."

**CONTENT ENVELOPE**
```json
{
  "pattern": "staged-move",
  "their_mechanism": "one sentence — why they currently win",
  "stages": [
    { "n": 1, "label": "≤30 chars", "text": "one sentence",
      "reversible": true, "commitment": "low | medium | high",
      "evidence_ids": ["S00-00"] }
  ],
  "escalate_when": "observable that increases commitment",
  "abandon_when": "condition that stops the move"
}
```
Rules: 3–4 stages · last stage `label` contains "decision gate" · at least one
stage `reversible: true` or the move is not bounded.

---

## P4 · BOUNDED ARGUMENT — 18 slides

**WHEN TO USE**
- The page carries an argument rather than a dataset
- A position must survive a hostile question
- No structured evidence exists — the reasoning *is* the exhibit

**WORKFLOW**
1. State the position, answer-first
2. Give the three stances a reader could take, and what each rests on
3. Close on the one that survives, and what would overturn it

**KEY PROMPT**
> "Argue [position] for [audience]. Give exactly three stances: the position
> taken, the strongest opposing stance, and the bounded middle. For each give the
> claim in one sentence and what it rests on. Mark which stance the evidence
> currently supports. Do not hedge the losing stances — state them at full
> strength. End with the decision, the owner, and the observable that would
> overturn the chosen stance."

**CONTENT ENVELOPE**
```json
{
  "pattern": "bounded-argument",
  "positions": [
    { "stance": "taken | opposing | bounded",
      "claim": "one sentence",
      "rests_on": "≤80 chars — the evidence or assumption beneath it",
      "supported": true,
      "evidence_ids": ["S00-00"] }
  ],
  "overturned_by": "the observable that would change the answer"
}
```
Rules: exactly 3 positions, one per `stance` · exactly one `supported: true` ·
`opposing` must be stated at full strength, never softened.

---

## P5 · DATED PLAN — 2 slides

**WHEN TO USE**
- Claims must become artifacts inside a fixed window
- Funding should release on evidence rather than on calendar
- Several workstreams are running without gates

**WORKFLOW**
1. Set the window and the artifact each phase must produce
2. Sequence so each phase unlocks the next
3. Attach a gate, an owner and a stop condition to every phase

**KEY PROMPT**
> "Build a [duration] plan for [company] that converts claims into reproducible
> artifacts. Give 3–5 phases. For each: the window as it would be written on a
> chart, its span in weeks, the artifact it must produce, the owner, and the gate
> that releases the next phase. Sequence so each phase unlocks the following one.
> End with the condition under which the plan stops rather than continues."

**CONTENT ENVELOPE**
```json
{
  "pattern": "dated-plan",
  "target_outcome": "what the window must deliver",
  "phases": [
    { "when": "Weeks 1–2", "span_weeks": 2, "label": "≤34 chars",
      "artifact": "the reproducible output", "owner": "role",
      "gate": "what releases the next phase" }
  ],
  "stops_if": "the condition that ends the plan"
}
```
Rules: `span_weeks` must be real — the rail draws phases to scale · every phase
needs an `artifact`, never an activity.

---

## P6 · COST BRIDGE — 2 slides

**WHEN TO USE**
- A cost advantage is claimed but not modelled
- Capital is requested against a projected unit price
- A die-level number is being compared to a system price

**WORKFLOW**
1. State today's delivered cost and what it includes
2. Bridge to the target through every element that must be carried
3. Gate the commitment on the model, not on the direction

**KEY PROMPT**
> "Build the cost bridge from [current] to [target] for [company]. Give each step
> as a label, a display amount, a numeric value for the bar height, and whether
> the magnitude is verified or directional. Carry every element that must be
> paid: NRE, yield, package, qualification, warranty, lifecycle. State explicitly
> whether a projected die price is comparable to a system price. End with the gate
> that must clear before capital is committed."

**CONTENT ENVELOPE**
```json
{
  "pattern": "cost-bridge",
  "steps": [
    { "label": "≤20 chars", "amount": "as displayed",
      "value": 0, "kind": "base | add | target", "verified": false }
  ],
  "comparability_rule": "one sentence on what may not be compared to what",
  "capital_gate": "what must clear before spend"
}
```
Rules: every step needs `verified` · if any step is `verified: false` the exhibit
prints a directional caveat — an unlabelled bar chart of unverified magnitudes is
the defect this pattern exists to prevent.

---

## P7 · CONFIDENCE REGISTER — 1 slide

**WHEN TO USE**
- Many claims of uneven quality must be prioritised for diligence
- The team needs to know what to purge from client-facing material
- Before a board review or an external pitch

**WORKFLOW**
1. List the load-bearing claims
2. Score each by importance and by evidence strength, on the same scale
3. Purge the low-evidence, high-importance ones and name the test

**KEY PROMPT**
> "Register the load-bearing claims behind [plan]. Score each on importance 1–3
> and evidence strength 1–3, using the same scale for all. Identify which are
> load-bearing — high importance, low evidence — and convert those into a purge
> list and a test plan with owners. End with the rule for what may appear in
> client-facing material."

**CONTENT ENVELOPE**
```json
{
  "pattern": "confidence-register",
  "claims": [
    { "claim": "≤120 chars", "importance": 3, "evidence": 1,
      "band": "high | medium | low-contested", "evidence_ids": ["S00-00"] }
  ],
  "purge_list": ["claims that may not be used externally"],
  "publication_rule": "what may appear in client-facing material"
}
```
Rules: `importance` and `evidence` are 1–3 integers · any claim with
`importance ≥ 2` and `evidence = 1` must appear in `purge_list`.

---

## How the three layers connect

```
PROMPT            →  produces  →  CONTENT ENVELOPE  →  draws  →  EXHIBIT
(what to ask)                    (typed fields)                (geometry that
                                                                encodes meaning)
```

A pattern is only real when all three exist. A prompt with no typed envelope
returns prose; a typed envelope with no exhibit returns boxes. Both failures
already happened in this run, which is why the envelopes above are schemas rather
than descriptions.
