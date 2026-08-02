# Deck brief

## Audience

The repo maintainer (sheke), reviewing what got installed and wired into this
project's own skill set this session. Already fluent in the codebase; needs
the "what changed and why it's trustworthy" read, not an intro to PowerPoint QA.

## Decision

Confirm the Impeccable install + design-qa-detect.sh wiring actually works
end-to-end, and that the PPTX/HTML boundary (lint_pptx.py vs Impeccable) is
correctly scoped — this deck IS the test artifact for that gate.

## Narrative promise

We installed a real, upstream, 53.8k-star deterministic design-QA tool,
wired it into two existing skills that already referenced it by name but
never had it, and it caught a real defect on the first run — including in
this very deck's own export.

## Voice and tone

Direct, evidence-led, technical. No marketing language. Every claim traces to
a command we actually ran and a result we actually saw this session.

## Anti-references

Generic AI dashboard look, cards nested inside cards, purple-to-blue gradient
backgrounds, decorative glow without semantic purpose, icon-tile-above-heading
stacks — the exact clichés Impeccable's own detector catalogs and this deck
must not exhibit.

## Evidence and editability

Every number and finding in this deck (side-tab count, rule count, version
numbers) must match what the actual tool runs in this session produced.
Marp PPTX export is image-per-slide (flattened, not editable) — acceptable
here since this is an internal status/test artifact, not a client deliverable.

## Success criteria

- The slide-title sequence tells the argument by itself.
- Each slide carries one main message and structured supporting evidence.
- The reviewed deck passes context, visual-spec, structural, design-lint, and render QA.
