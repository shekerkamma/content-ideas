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

1. **Zones and blocks.** `python3 ../part-explainer-film/scripts/locate_zones.py <drawio> <svg> --out zones.json`,
   then `scripts/zone_blocks.py <drawio> --zones zones.json` (adds each zone's blocks, so a beat redraws
   them natively instead of pasting the diagram).
2. **Scaffold.** `scripts/scaffold_carousel.py <storyboard> --zones zones.json --kicker "SKU-3 · HI-REL PMIC" --url <page> --out carousel.json`.
3. **Author** every `body` (and the CTA `title`), each beat's `stat` (`{"value", "label"}`: the one figure a
   reader keeps, from the page), and exactly three `items` on the close (open questions) and on the CTA
   (what to bring). One sentence per body, at most 25 words; items at most 14. Titles stay the storyboard's
   assertions.
4. **Gate.** `scripts/gate_carousel.py carousel.json --page-text page-text.txt` (0 clean, 2 findings).
5. **Render.** `node scripts/render_carousel.mjs <run> --ds <design-system> --wordmark <png>`
   → `out/<part>-NN.png`, `out/<part>-carousel.pdf` and the editable `out/<part>-carousel.html`. Blocks on a
   missing font or any overflowing text.
6. **Look** at a contact sheet of every slide at feed size (about 430 px wide). Fix, re-render, stop
   after one confirmation round.

## Judgment rules

Editable policy. Tune here, never inside the step instructions.

- **One idea per slide, 25 words at most.** A carousel is read at thumb speed; the title carries the
  claim, the body says why a board designer cares.
- **Redraw, never paste.** A pasted draw.io crop put 5-px labels on a phone and read as a screenshot; the
  first version was rejected as unprofessional for it. A beat redraws its zone's real blocks as tiles
  (names the beat mentions first, each name once), and the SIGNAL-CHAIN RAIL draws the part's zones along
  every slide's base with the active zone in copper: the diagram and the progress bar in one element.
- **A focal point on every slide.** Each beat leads with one hero figure in copper; the cover with a hook
  and a numbered zone map; the close with three numbered open questions; the CTA with three things to bring.
  Four archetypes, never one template repeated.
- **Every number is on the product page or storyboard.** No market figures, no "certified" or
  "compliant"; standards are "designed toward". Every slide footer says pre-silicon.
- **Copper is the one accent; teal only for a safe state.** Ink ground, Newsreader titles, Inter body,
  JetBrains Mono kickers, as the approved design system says.
- **Close on what is unproven, then the ask.** The CTA names what to bring and links the product page.

## Verification discipline (SKU-3 pilot)

- Negative control: a body with a dash, "certified", "unparalleled" and an invented 47 V, plus a
  120-character title, gave 5 findings and exit 2; rendering it blocked on the title overflowing by 64 px.
- v1 (pasted, cropped diagram) was rejected. v2 visual rounds caught: a stat label orphaned beside its
  figure (moved under it), a fault beat showing the wrong four blocks (named blocks now rank first),
  close and CTA slides a fifth empty (lists spread to the rail), duplicate tiles where four rails share
  names (de-duplicated), a rail label clipped mid-word at eight zones (dense size), and the package frame
  listed as a zone (containers are skipped). zone_blocks.py first required a line break before a block's
  sub-line and silently dropped half the DG32-LITE blocks; it accepts a dot too.

Tests: `tests/test_storyboard_to_carousel.py` (both block formats, a block that fills its zone, copy-gate
defects in the hero figure and the lists).

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
