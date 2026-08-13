# Example library

Use examples to constrain output shape without importing synthetic facts into a client deck.

## Routing

| Need | Read or copy | Required adaptation |
|---|---|---|
| Start a run | `examples/prompts/sample-prompts.md` | target, decision, audience, evidence horizon, slide count, template path |
| Build a content envelope | `references/accenture-guide-content-envelope.md` | adapt When to use → Workflow → Key prompt → Output includes to the slide-level evidence contract |
| Write a slide envelope | `examples/completed-contracts/` | evidence IDs, status, falsifier, implication, owner, trigger |
| Integrate review | `examples/review-control-traces/grill-to-meta-loop.json` | atomic control IDs and rendered-region traceability |
| Select a layout | `assets/slide-archetypes/archetype-catalog.json` | analytical relationship, density, hierarchy, visual provenance |
| Inspect intended finish | `assets/slide-archetypes/final-design-examples.html` | apply the client template profile; do not copy the neutral example skin |
| Review all archetypes at a glance | `assets/slide-archetypes/final-design-examples.png` | inspect hierarchy, density, and comparative consistency before authoring |
| Audit the chain | `examples/golden-path/README.md` | reproduce every artifact in the current run directory |

The byte-identical supplied reference deck is stored at
`assets/reference-decks/accenture-style-claude-guide-draft.pptx`. Its SHA-256 is
`961d4685f42c29709bb9582e10de2486c78c92cd82fe4596a3942d8317ccfd02`.
The normalized 24-slide source bundle is stored in `examples/reference-source/` and must remain
hash-linked to the reference asset.

## Rules

- Treat every company, number, date, source ID, and score in the examples as synthetic.
- Copy structure, field completeness, parallel grammar, and visual logic—not the example wording.
- Select an archetype because it encodes the required relationship. Never rotate layouts merely for variety.
- Keep the client template authoritative for typography, palette, footer, motif, and spacing.
- Reject a prompt that asks one model call to author more than four deep-research slide envelopes.
- Validate examples with `scripts/validate_examples.py` after any edit.
