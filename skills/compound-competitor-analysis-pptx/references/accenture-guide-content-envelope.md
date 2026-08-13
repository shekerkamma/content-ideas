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

## Relationship to the source guide

The supplied guide is a prompt-pattern reference, not evidence and not the default brand template.
Its repeated page architecture is useful because it makes every method operational. This skill
adds the controls absent from a generic prompt card: evidence IDs/status, falsifier, reviewer
controls, batch boundaries, design regions, accessibility, and delivery gates.
