---
name: storyboard-to-carousel
description: Use when a part storyboard (story-architect output with beats tied to a draw.io architecture diagram) should become a LinkedIn document carousel: 1080x1350 slides plus one PDF, in the DeepGrid Semi design system. Triggers on "LinkedIn carousel for SKU-3", "carousel from the storyboard", "make the part carousels", "social version of the explainer". Not for a narrated film (use part-explainer-film), not for a slide deck (use branded-pptx-deck or vault-presales-pptx-pipeline), not for one-off social cards or infographics (use ai-graphics).
license: MIT
metadata:
  category: Media Production
  version: '1.0'
  cost-tier: Sonnet executes it; writing the 25-word bodies is the judgment step, every other step is a script. No paid API.
  compatibility: Python 3 stdlib, Node 20+ with playwright and a Chromium build. Claude Code, Codex CLI, or any host reading agent Markdown.
  legacy-frontmatter:
    argument-hint: "<part-slug> e.g. sku-3"
    user-invocable: true
---

# Storyboard to Carousel

The same storyboard that drives a part's explainer film becomes a carousel a reader pages through in
a feed: a cover with the headline, one slide per beat (the assertion, the real diagram cropped to that
beat's zones, one sentence on what it means), the honest close, and a call to action with the page link.

## Inputs

As `part-explainer-film`: the storyboard JSON, the diagram `.drawio` + SVG, the product page text, the
design system (`deepgrid-dr-silicon-v6/design-system/`) and the wordmark. Run folder:
`content-ideas/runs/<date>-carousels/<slug>/`.

## Workflow

1. **Zones.** `python3 ../part-explainer-film/scripts/locate_zones.py <drawio> <svg> --out zones.json`
   (or copy `zones.json` from the part's explainer run).
2. **Scaffold.** `scripts/scaffold_carousel.py <storyboard> --zones zones.json --kicker "SKU-3 · HI-REL PMIC" --url <page> --out carousel.json`.
3. **Author** every `body` (and the CTA `title`). One sentence for a reader in a feed, at most 25
   words, what the block means for their board. Titles stay the storyboard's assertions.
4. **Gate.** `scripts/gate_carousel.py carousel.json --page-text page-text.txt` (0 clean, 2 findings).
5. **Render.** `node scripts/render_carousel.mjs <run> --svg <svg> --ds <design-system> --wordmark <png>`
   → `out/<part>-NN.png` and `out/<part>-carousel.pdf`. Blocks on a missing font or any overflowing text.
6. **Look** at a contact sheet of every slide at feed size (about 430 px wide). Fix, re-render, stop
   after one confirmation round.

## Judgment rules

Editable policy. Tune here, never inside the step instructions.

- **One idea per slide, 25 words at most.** A carousel is read at thumb speed; the title carries the
  claim, the body says why a board designer cares.
- **The real diagram, cropped, never redrawn.** The crop stays inside the diagram (no blank paper past
  its edge); the beat's zones keep full strength, the rest dims under ink, a copper frame marks them.
- **Every number is on the product page or storyboard.** No market figures, no "certified" or
  "compliant"; standards are "designed toward". Every slide footer says pre-silicon.
- **Copper is the one accent; teal only for a safe state.** Ink ground, Newsreader titles, Inter body,
  JetBrains Mono kickers, as the approved design system says.
- **Close on what is unproven, then the ask.** The CTA names what to bring and links the product page.

## Verification discipline (SKU-3 pilot)

- Negative control: a body with a dash, "certified", "unparalleled" and an invented 47 V, plus a
  120-character title, gave 5 findings and exit 2; rendering it blocked on the title overflowing by 64 px.
- The first render left ~250 px empty under every body and shrank a two-zone beat to unreadable; the
  diagram card is now 660 px tall. Crops ran past the diagram's edge; they are now clamped inside it.

## Gotchas

- **LinkedIn takes the PDF**, not the PNGs, for a document carousel; the PNGs are for review and other channels.
- **A storyboard zone name must match the diagram label exactly**; scaffold blocks with the real names.
- **Never paste the beat body**; the gate's echo check flags over 40 % trigram overlap.

## Skill Relationships

### Category
Media Production

### Dependencies
- `part-explainer-film`: its `locate_zones.py` (called by path, not copied).

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `story-architect` | Prerequisite | always | `runs/2026-10-03-arch-storyboards/<slug>.json` |
| `part-explainer-film` | Parallel / Complement | same storyboard, film output | `zones.json`, `page-text.txt` |
| `ai-graphics` | Alternative / Peer | a single social card or infographic | — |
| `social-media-team` | Sequential downstream | scheduling and posting | `out/<part>-carousel.pdf` |

### Runtime Preamble
"I'll build the carousel from the part's storyboard and its real diagram: cover, one slide per beat,
the honest close, a call to action. You get PNGs to review and the PDF LinkedIn takes."

## Host Compatibility

- Canonical source `content-ideas/skills/storyboard-to-carousel/`; mirror `.agents/skills/storyboard-to-carousel/`;
  Claude Code via the `~/.claude/skills/storyboard-to-carousel` symlink.
- Stdlib Python and Node ESM; on Windows use `python` for `python3`.
