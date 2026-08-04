# Visible skill-application contract

Use this contract when a deck invokes multiple content, story, design, visual, editing, or QA
skills. Invocation logs and intermediate files prove execution—not visible impact.

## Required gates

1. **Content impact:** `presentation-content-writer` must change visible slide articulation, not
   only notes. Map every slide to its key message and derived visible structure. Notes cannot carry
   a required claim or caveat.
2. **Direction impact:** Impeccable must compare at least three materially distinct directions or
   structures on at least three representative slides. Record the selection and four or more
   concrete differences from the incumbent world. Recoloring plus isolated diagrams is not enough.
3. **Visual-system impact:** Apply at least three reusable archetypes or one signature grammar to
   at least 60% of slides. Preserve exact source evidence and ship editable deterministic sources.
4. **Editing-layer impact:** `pptx-toolkit` operations count only at their intended layer. Native
   notes are valuable, but are not visible design improvement.
5. **QA boundary:** OfficeCLI, lint, and package checks prove technical cleanliness. Reviewed
   promotion also requires a real render and independent content/design review.

## Manifest and validator

Write `<run>/skill-application-manifest.json` with stage status, proper layer, outputs, impact;
content visible/notes counts; direction candidates, representative slides, selection and material
differences; visual archetypes, coverage, source-evidence slides and editable sources; and QA gates.

```bash
python3 skills/present/scripts/validate_skill_application.py \
  <run>/skill-application-manifest.json --check-files
```

A missing or superficial stage keeps the deck `draft` or `blocked`. Never compensate by describing
the skill more strongly in the delivery message.
