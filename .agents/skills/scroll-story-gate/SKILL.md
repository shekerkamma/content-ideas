---
name: scroll-story-gate
description: Use before generating any asset for a scroll-scrubbed page — validates the storyboard while changes are still free. Triggers on "check the storyboard", "review the scroll plan before generating", "visual story table", "am I ready to generate", "scroll pacing plan". Enforces that scroll distance is budgeted independently of clip duration, that text-bearing beats have room to be read, that every cross-clip seam declares which frame feeds which, and that no credibility claim is invented. Provider-agnostic — it gates the plan, never the vendor. Not a scroll-page builder (use scroll-craft) and not a video renderer.
license: MIT
metadata:
  category: Media Production
  version: '1.0'
  compatibility: Python 3 stdlib only. No network, no provider, no API key. Runs on Claude Code, Codex CLI, Codex desktop, or any host reading agent Markdown.
---

# Scroll Story Gate

A scroll-scrubbed page fails in ways that only appear after you have paid for the
footage: a transition with no room to breathe, copy that scrolls past before it
can be read, two clips that do not meet at the seam. Every one of those is
visible in the plan.

This gate reads the plan and refuses the ones that will fail. It is the cheapest
step in the pipeline and the only one that runs before the money.

## When to invoke

- A Visual Story / storyboard table exists and generation has not started
- Re-planning after a seam or a pacing problem showed up on a render
- Reviewing someone else's scroll plan before approving spend

Pair with `scroll-craft`, which owns the build, the engine and the encode. This
skill owns only the go/no-go before generation.

## The plan format

A storyboard is a JSON file. One entry per beat, in scroll order.

```json
[
  {"id":"01-open","kind":"scene","visual":"Subject established, camera static",
   "copy":"Hero heading + primary action","vh":1.5,"clip":"a","clip_seconds":6},
  {"id":"02-travel","kind":"transition","visual":"Origin exits, subject alone in frame",
   "copy":null,"copy_waived":"No copy - let the motion lead","vh":2.0,
   "clip":"a","clip_seconds":6},
  {"id":"03-arrive","kind":"scene","visual":"Destination enters, subject settles",
   "copy":"Outcome heading, closing action","vh":1.5,"clip":"b","clip_seconds":6,
   "continues_from":{"clip":"a","frame":"last"}}
]
```

`vh` is scroll distance in viewport heights. `clip_seconds` is footage length.
**They are independent numbers and the gate enforces that they are treated as
such** — a 6-second clip can span 5vh of scroll or 1vh, and stretching a handful
of frames across a long scroll does not make the playback smooth.

## Run it

```bash
python3 scripts/check_story.py storyboard.json          # 0 clean, 1 blocked, 2 findings
python3 scripts/check_story.py storyboard.json --plan   # also emit the generation order
```

## Judgment rules

Editable policy. Tune the numbers here; the script reads them from this file's
defaults only as a starting point.

- **Scroll distance is budgeted, never inherited from clip length.** A beat that
  sets `vh` proportional to `clip_seconds` is not a plan, it is a default.
- **Text needs travel.** A beat carrying copy gets at least `MIN_COPY_VH` (1.0)
  of scroll, because a heading that enters and leaves inside half a viewport
  height is never read. A beat with no copy must say so explicitly via
  `copy_waived` rather than leaving the field empty — silence is indistinguishable
  from an oversight.
- **A transition is a beat, not a gap.** If the story moves between settings, the
  move gets its own row with its own `vh`. Two scenes touching directly is a cut,
  and a cut inside a scrub reads as a glitch.
- **Every seam declares its frame.** A clip that continues another states
  `continues_from`. Longer scroll distance cannot change what is visible in the
  source frames, so a seam that was never planned cannot be fixed by pacing.
- **Credibility claims are quoted or absent.** Testimonials, customers, awards,
  addresses, years in business and project counts are flagged unless marked
  `sourced: true`. Inventing them is the one failure a render will never catch.
- **Total scroll is stated, not accumulated by accident.** The gate reports the
  sum so the page length is a decision.

## What this gate does not do

It does not judge whether the story is good, choose a provider, estimate cost, or
verify a render. Pacing remains **unverified** until someone scrolls the built
page — say that plainly rather than reporting a smooth result from a clean plan.

## Provider independence

The gate names no vendor and needs no key. It emits a generation *order* —
which clips to make, in what sequence, and which frame each one inherits — and
any provider can execute it. Where two clips share a seam, the order guarantees
the parent is produced and inspected before its child is requested.
