# Review control loop: Grill-Me → Meta LOOP → slide contracts

## Canonical chain

```text
current deck + evidence/story contracts
→ grill-me questions and recommended answers
→ grill-ledger.json with atomic controls
→ meta-loop independent classification and verification
→ verified-findings-ledger.json + final-rewrite-blueprint.json
→ updated story-architect pack
→ regenerated slide-content and slide-design contracts
→ native rebuild + material-change comparison + OfficeCLI QA
```

A review transcript is not implementation. Every finding must become a testable visible-change
control and trace through the rendered slide.

## Grill-Me input and frontier

Provide the rendered deck/contact sheets, evidence ledger, story pack, existing slide contracts,
user critique, and deck-wide statistics. Ask one load-bearing question at a time and include a
recommended answer. If the user delegates answers, answer from evidence and record the assumption.

Grill these frontiers:

1. audience decision and BLUF;
2. inclusion, exclusion and slide count;
3. evidence sufficiency and overclaims;
4. competitor scope and comparison basis;
5. narrative sequence and section logic;
6. per-slide content envelope;
7. analytical exhibit and visual metaphor;
8. density, hierarchy, typography and whitespace;
9. counterarguments and falsifiers;
10. decision, owner, trigger and stop rule;
11. appendix/core-story boundary;
12. QA and reviewed-promotion standard.

## Grill ledger

Convert each agreed answer into an atomic control:

```json
{
  "control_id": "G-001",
  "question": "What single decision must the deck enable?",
  "answer": "Approve a bounded perception-layer attach strategy.",
  "recommended_answer": "...",
  "answer_source": "user-confirmed | self-answered | evidence-derived",
  "applies_to": {"scope": "deck | section | slide", "slide_ids": [1, 2]},
  "layer": "story | content | evidence | design | QA",
  "required_visible_change": "Rewrite title and decision rail",
  "acceptance_test": "Title-only read reproduces the bounded decision",
  "evidence_ids": ["E-001"],
  "status": "open"
}
```

Controls must be atomic, assigned to one implementation layer, and testable. Notes-only changes do
not satisfy visible content or design controls.

Normalize an existing slide-level grill review with:

```bash
python3 skills/compound-competitor-analysis-pptx/scripts/normalize_grill_review.py \
  <run>/outputs/grill-me-slide-review.json <run>/grill-ledger.json
```

## Meta LOOP integration

Use `meta-loop` only when its required Claude aggregator and Codex worker capability gate passes.
Follow its attribution and verification-ledger rules. Use isolated non-overlapping worker briefs:

- W1: story and sequence controls;
- W2: claim-by-claim evidence classification;
- W3: slide content-envelope controls;
- W4: slide design/layout controls;
- W5: QA and promotion controls.

Verify every worker result against the actual evidence/deck and assign `PASS`, `FIX`, or `ESCALATE`.
The aggregator resolves duplicates, contradictions, precedence and scope, returning `SHIP`,
`CONDITIONAL`, or `BLOCK`.

If the capability gate fails, run a clearly labeled bounded fallback. Do not claim Meta LOOP,
multi-model independence, worker verification, or aggregator approval.

## Consolidated finding and blueprint

Every consolidated finding records source grill control IDs, slide/section scope, evidence,
confidence, defect type, current-state evidence, required visible change, disposition, target layer,
owner, acceptance test, worker verdict, and aggregator disposition.

The rewrite blueprint defines:

- authoritative core and appendix sequences;
- slide-level `rewrite`, `merge`, `move-to-appendix`, `retain`, `remove`, or `research-first` status;
- control IDs implemented by each slide;
- content and design rewrite instructions;
- evidence and counterargument requirements;
- merge/move/remove map preserving slide-count commitments;
- material-change expectations;
- unresolved research/user blockers.

Regenerate the story pack whenever the blueprint changes BLUF, order, slide role, evidence map, or
content cuts. Then regenerate both slide contracts. Do not merely reorder the old deck or place
review findings in speaker notes.

## Optional LLM Council

Use `llm-council` only for a remaining high-stakes choice: attach versus full-system ambition,
partner versus compete, preserve versus compress a long deck, or competing design directions. Feed
it the evidence, grill controls and verified Meta LOOP conflicts. Convert the chairman's selected
recommendation and dissent into new controls; never paste council prose directly into slides.

## Visible implementation gate

Maintain this trace:

```text
control ID → target slide → changed contract field → built shape/region → rendered evidence
```

Reject the pass when a control changes only notes, old/new slides remain materially identical, slide
contracts omit control IDs, the user's criticism recurs in the contact sheet, the builder ignores the
blueprint, or a deck-wide visual control affects fewer than 60% of applicable slides.
