# Motion design — DeepGrid SKU Explainer

## Where the grammar comes from

Deepgrid's own product simulators (`refs/*.html`) all animate the same idea: a
signal propagates through a chain and the console fills in behind it. Their
keyframes are `march`, `pktrun`, `radarPing`, `detPulse`, `rungIn`, `swFront/
swLeft/swRight`, `towerGlow`, `coverBreath`.

The deck reuses that grammar rather than inventing one: **bands build top to
bottom, and inside a band the columns wipe left to right.** A four-card row
fills the way a signal runs the chain.

## Pipeline

```
officecli query <deck> shape --json      # stable @id paths + resolved geometry
  -> plan_motion.py   -> motion-plan.json
  -> apply_motion.py  -> batch.json
  -> officecli batch  -> animated deck (Windows-side path only)
  -> lint_motion.py   -> independent XML read-back
```

`plan_motion.py` derives everything from geometry, so it needs no cooperation
from the builder and survives a rebuild: shapes cluster into bands by `y`, then
into columns by horizontal overlap.

## The rule that shapes the whole plan

**One perceived step per band, not per column.** Inside a band every shape is
`withPrevious`; the left-to-right stagger comes from `delay` (110 ms per
column), not from `trigger`. So a row of four cards is one click and one
motion, and a seven-column signal chain runs across 770 ms as a single step.

Getting this wrong is what the first two attempts did — one step per column
blew the budget on every slide, and the collapse that fixed the count destroyed
exactly the left-to-right motion that was the point.

## `max_build_steps_per_slide` counts nodes, not steps

`lint_motion.py`'s `_build_steps` appends one entry per `cTn` carrying a
`presetClass` — that is one entry per animated **shape**. The name says steps.
On this deck the two readings differ by an order of magnitude: 487 perceived
steps versus 2,602 nodes, and the densest slide is 5 steps but 120 nodes.

The cap in `motion-config.json` is therefore set as a node ceiling (128) with
the reason recorded in the file, and the real click budget (8) is enforced
upstream in `plan_motion.py`. Raising a cap silently because a gate went red is
how a gate stops measuring anything; the number and its meaning are written
down together.

## Verification

- `officecli` self-report is **not** proof — its `get` reads the resident's
  memory. Proof is the on-disk md5 changing (`0cb3d71…` → `5f827b5…`) plus
  `lint_motion.py` reading the transition and `<p:timing>` XML straight out of
  the package.
- The gate is demonstrably live: the smoke run animated slide 1 only, and the
  linter reported 80 `MOTION_TRANSITION_MISSING` warnings for slides 2–81.
  A clean run on a fully animated deck means something only because that
  negative control fired first.
- No `exit` effects anywhere, so the resting state is the complete slide and
  every static gate still applies: `overflow_scan` 0, `verify_deck` PASS,
  `pptx_toolkit validate` valid, OfficeCLI 0 issues.

## Embedding the simulators

Four of Deepgrid's own HTML simulators are embedded as playable clips, one per
F slide: `ddrive` (23), `forklift` (17), `yard` (55), `sentinel` (74).

`media/capture_sim.mjs` drives each page in Chromium over WSLg and records it,
stepping through every scenario the console offers. Two things it has to do:

- **Click through the DOM, not through Playwright's actionability wait.** These
  consoles paint confidentiality watermarks and intro panels that intercept
  pointer events, so `page.click()` times out on a button that is perfectly
  clickable from script. `page.evaluate(s => document.querySelector(s).click())`
  works every time.
- **Re-encode to H.264 + a silent AAC track.** Playwright records VP8 in WebM,
  which PowerPoint will accept and then show as a black rectangle.

**The seat is declared by the builder, not guessed by the attacher.** The build
writes `<deck>-video-seats.json` naming the exact rect it left empty behind each
frame. `plan_motion.py` reads it to *exclude* those shapes (an embedded clip has
no build, so anything animating under it would wipe in behind something already
on screen), and `attach_media.py` reads the same file to *fill* them. One
source of truth, so the clip lands inside its frame rather than near it.

Order matters: **media first, then motion.** The plan is derived from a shape
query, so it has to see the final slide.

### Checking that the clips are really in the package

`zipfile` on the `.pptx` — but note the parts land at top-level
`media/mediadata*.mp4`, **not** `ppt/media/`. A first check that filtered on
`'/media/' in name` returned **0 mp4s on a deck that had four**, because that
leading slash matches neither path. The file had grown from 0.55 MB to 20.8 MB,
which is what said the check was wrong rather than the deck. Same failure class
as the occlusion gate that measured an empty population.
