# Accenture-style prompt envelope

This contract is derived from the supplied 24-slide reference guide
`assets/reference-decks/accenture-style-claude-guide-draft.pptx` (SHA-256
`961d4685f42c29709bb9582e10de2486c78c92cd82fe4596a3942d8317ccfd02`). The source repeats a useful
four-part teaching grammar on each method page:

1. **When to use** — decision context and trigger;
2. **Workflow** — three ordered analytical operations;
3. **Key prompt** — bounded instruction with named methods and required ending; and
4. **Output includes** — explicit artifact schema.

Preserve that grammar while strengthening it for evidence-controlled slide production.

## Content-envelope prompt

```text
SLIDE ID: [S##]
ARCHETYPE: [catalog ID]

WHEN TO USE THIS PAGE
- Audience decision: [decision this page enables]
- Trigger: [why it belongs in the story now]
- Dependency: [required prior page/evidence gate]

WORKFLOW
1. Frame one analytical question and define the comparison scope.
2. Resolve it using only [allowed evidence IDs], separating verified fact,
   attributed claim, qualified interpretation, and insufficient evidence.
3. Expose the mechanism, strongest counterargument/falsifier, and the resulting
   decision, owner, observable trigger, and stop/escalate rule.

KEY PROMPT
Build slide [S##] for [audience] to decide [decision]. Answer [analytical question].
Use [archetype] and compare on [buyer control points]. Use only [evidence IDs].
Write one assertion title and one executive answer. Show the causal/comparative/
temporal logic explicitly. Include the strongest counterargument or falsifier.
End with the implication, decision, owner, trigger, and stop/escalate rule.
Return the complete slide-content and slide-design contracts; do not render yet.

OUTPUT INCLUDES
- action_title
- analytical_question
- executive_answer
- evidence_blocks[] with status and evidence IDs
- logic.type and logic.mechanism
- counterargument and falsifier
- implication, decision, owner, trigger, stop_or_escalate_rule
- dominant_exhibit and archetype
- region-level design contract
- source notes, speaker notes, accessibility intent
- Grill-Me and Meta LOOP control IDs
```

## Competitor-profile specialization

```text
WHEN TO USE
- A named rival requires a decision-grade profile, not a company fact sheet.
- Leadership must choose contain, partner, monitor, or deprioritize by segment.

WORKFLOW
1. Normalize the competitor identity, segment scope, buyer, geography, and evidence date.
2. Compare threat by segment using field proof, procurement access, qualification,
   economics, service reach, and channel control; run sensitivity on weights.
3. Convert the result into a decision with falsifier, owner, verification trigger,
   and early-warning signals.

KEY PROMPT
Assess [competitor] against [company] in [segments/geography] as of [date]. Use only
[evidence IDs]. Separate fact, company claim, interpretation, and unknown. Explain why
the competitor can win, where the threat is bounded, what would change the rating, and
whether the correct response is contain, partner, monitor, or deprioritize. Return the
full content and design contracts for [slide IDs] only.

OUTPUT INCLUDES
- normalized profile and evidence horizon
- segment threat with scoring sensitivity
- buyer-control comparison
- messaging collision and counterclaim
- white-space mechanism and copy barrier
- response decision, owner, trigger, early-warning signal, falsifier
```

## Long-deck batching specialization

Prepend the envelope above to every authoring batch. Append:

```text
BOUNDARY
- Author slides [n–m] only; maximum four slides.
- Do not introduce claims, numbers, companies, or dates outside the allowed evidence list.
- Do not collapse required fields to fit a word limit; flag the slide for split instead.
- Keep parallel grammar with [comparison slide IDs].
- Stop when a load-bearing gap prevents a supported answer.
```

## One envelope per pattern, never one envelope per deck

The guide's real mechanism is easy to miss: **its OUTPUT INCLUDES list differs on
every page.** That is not formatting variety — a different output schema is what
forces a different exhibit. Applying one generic envelope to every slide produces
a deck where all pages carry the same fields, so all pages draw the same boxes.
Measured on one 74-slide build: 74/74 pages were prose-in-cards, 64/74 shared two
layout fingerprints, and zero analytical exhibits existed. Every lint gate passed.

The chain that fixes it has three links, and a pattern is only real when all
three exist:

```text
KEY PROMPT          →  CONTENT ENVELOPE       →  EXHIBIT
(what to ask)          (typed field schema)      (geometry encoding meaning)
```

A prompt with no typed envelope returns prose. A typed envelope with no exhibit
returns boxes. Give each pattern one distinguishing field and let the exhibit
render *that* field as geometry — rung width as confidence, cell colour as
rating, bar height as magnitude, phase width as span.

### Derive the patterns from the content, do not impose a taxonomy

Profile the slides first and let the pattern set fall out of what is actually
there. A taxonomy chosen up front distributes badly — one imposed 12-method
scheme put 20 slides in a catch-all and 1 slide in another method. Profiling the
same deck yielded seven patterns whose counts matched real structural families.

### Bind mechanically, and let the binder fail loudly

Project each slide's extracted evidence into its pattern's schema with a script,
then validate against that pattern's stated rules. Two rules that matter:

- **Never force a slide into a pattern its evidence cannot draw.** Fall back to
  the bounded-argument pattern — whose own "when to use" is *no structured
  evidence exists, the reasoning is the exhibit* — and record the reason in the
  bound artifact.
- **When a binding rule rejects real content, suspect the rule.** A rule
  requiring two or more rating rows rejected three valid pages; one competitor
  rated across three arenas is exactly the threat-matrix use case. Check whether
  the rule or the evidence is wrong before editing either.

### A deck of argued pages still needs a spine

Per-page rigour does not produce a narrative. Source order frequently splits a
subject across the deck — one competitor's evidence, threat map, recommended move
and falsifier landing at slides 20, 22, 21 and 59 — so the subject is never
argued in one place. Group by subject inside acts, and add the story layer the
argued pages cannot supply themselves: a storyboard page with act bands drawn to
page-count scale, a pyramid page, act dividers carrying each act's question, and
a hostile-question page. See `references/review-control-loop.md` for the review
chain that feeds it.

## Relationship to the source guide

The supplied guide is a prompt-pattern reference, not evidence and not the default brand template.
Its repeated page architecture is useful because it makes every method operational. This skill
adds the controls absent from a generic prompt card: evidence IDs/status, falsifier, reviewer
controls, batch boundaries, design regions, accessibility, and delivery gates.
