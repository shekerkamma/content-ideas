# /design video brief — client-ready deck

10 slides from Brendan Jowett, *"Master NEW /design Claude Skill In 10 Minutes!"*
(youtube.com/watch?v=IHPcOvVU4PM, 12:26).

**Read off frames, not captions.** The first cut used `watch --detail transcript`
— zero frames — and was correspondingly thin. See `frame-evidence.md`: the
captions carried roughly a sixth of the substance, and the default download is
640×360 at which none of the on-screen text is legible. Every figure on a content
slide (file names, line counts, version ids, hex values) came off a 1080p frame.

Built with **artifact-tool presentation JSX** per `vault-presales-pptx-pipeline`'s
PowerPoint Rule — 310 native shapes, 176 text boxes, **0 pictures, 0 media parts**.
Zero flattened slides.

## Chain

```
watch --detail transcript   212 caption segments — used to LOCATE the moments
yt-dlp -f 299 + ffmpeg      12 targeted 1080p frames at those moments
frame-evidence.md           what the frames carried that the captions could not
story-architect method      story-pack.md — BLUF, tension, arc, spine, cuts
slide-plan.json             schema-valid spine, 0 errors
build_deck.mjs              artifact-tool JSX + deck-kit + deck-grid
kit-spec.mjs                type scale corrected to the design system (see below)
```

The transcript's job is to find the moments worth a frame. It is not the evidence.

## The defect that made every earlier cut look bland

`assets/deck-kit.mjs` sets its type in artifact-tool **pixels** but uses the design
system's **point** numbers as those pixel values. artifact-tool is 1px = 0.75pt, so:

| Role | Spec pt | Spec px | Kit px | Renders at |
|---|---|---|---|---|
| Slide title | 24–30 | 32–40 | 30 | **22.5pt** |
| Body | 12–14 | 16–19 | 13 | **9.75pt** |
| Card heading | 12–16 | 16–21 | 15 | **11.25pt** |
| Kicker | 8–10 | 11–13 | 10 | **7.5pt** |
| Footer | 7–8 | 9–11 | 9 | **6.75pt** |

Every role lands under floor; the whole deck renders about a quarter too small.
This is the exact trap `references/artifact-tool-presentation-jsx.md` documents —
*"reading those numbers as pixels shrinks the whole deck by a third and is the single
fastest way to ship a deck that looks wrong at a glance"* — and the kit falls into it.

`kit-spec.mjs` re-cuts `header` / `footer` / `card` / `kpi` / `table` / `chain` / `rail`
at `PX(pt) = pt / 0.75`, keeping the kit's geometry and primitives. Effect on lint:

```
TEXT_TOO_SMALL       33 → 0
SLIDE_MISSING_TITLE   8 → 1     (the linter needs ≥24pt to see a title at all)
total warnings       70 → 29
```

**This belongs upstream in `deck-kit.mjs`.** Every deck built from the kit carries it.

## Gates

| Gate | Bar | Result |
|---|---|---|
| Canvas | 13.333 × 7.5 in | pass |
| No flattened slides | 0 pictures | **0 pictures, 0 media parts** |
| Native objects | shapes + text frames | 310 shapes · 176 text boxes |
| Speaker notes | present | 10/10 |
| `pptx-toolkit validate` | valid | pass |
| **OfficeCLI** | `passed`, issues 0 | **passed · 0 issues** |
| Contact sheet | reviewed by eye | pass — artifact-tool renders + OfficeCLI's independent HTML render |
| Internal-term scan | clean | clean |
| Number scan | every figure traceable | pass |

29 lint warnings remain, all characterised:

- **`TEXT_LOW_CONTRAST` ×16** — the design system's own cyan kicker (`#00B4D8` on white)
  is 2.46:1 against a 4.5:1 floor, and the kit reproduces it in `header()`/`kpi()`.
  A spec-level defect, not a deck defect. Worth amending in the vault document.
- **`SLIDE_WORD_COUNT` ×7 / `SLIDE_SHAPE_COUNT` ×4** — a `chain()` is one *major* object
  built from many shapes; the design system budgets major objects, the linter counts
  shapes.
- **`SLIDE_MISSING_TITLE` ×1** — slide 6, the pivot, has no title band by design.

## Caveats

- Georgia/Arial are the design system's documented fallbacks, applied deliberately.
  Linux renders show sans titles; Windows PowerPoint resolves Georgia.
- No native PowerPoint contact sheet — OfficeCLI produced the HTML one; PowerPoint COM
  was occupied. The HTML render is independent of artifact-tool, so it is the real
  cross-check.
