---
name: film-motion-overlay
description: Use when an existing narrated slide film (a deck voiced into an MP4, holding each slide still for 20-40 s) needs motion without touching its sound or captions — "add motion to the DG32 films", "the films are static slides", "animate the narrated deck video", "spotlight what the narration is talking about". Each caption cue moves a gentle camera to the slide region the sentence is about; audio and subtitles are copied bit for bit and proven so. Not for a film that is already motion graphics (measure first), not for making a new film from a storyboard (use part-explainer-film) or from a deck (use narrated-deck-film).
license: MIT
metadata:
  category: Media Production
  version: '1.0'
  cost-tier: Haiku or Sonnet executes it; every step is a script. No paid API. The one judgment is reading the contact frames.
  compatibility: Python 3 stdlib, ffmpeg/ffprobe, Node 20+ with playwright and a Chromium build. Tesseract only for the no-deck fallback. Claude Code, Codex CLI, or any host reading agent Markdown.
  legacy-frontmatter:
    argument-hint: "<film.mp4> with its -film.json, .vtt and the source deck's inspect.ndjson + frames"
    user-invocable: true
---

# Film Motion Overlay

A narrated deck film keeps its voice, captions and slide order; only the picture changes. At each
caption cue the camera eases toward the part of the slide the sentence is about, the rest of the
slide dims a little, and the region is outlined in the deck's own accent. Then it holds still.

## First, measure whether the film needs it

```bash
python3 scripts/motion_profile.py <film.mp4>     # share of still time, longest still run
```

Measured on the six DG32 films (2026-10-03): five were 96-97 % still with holds of 31-33 s (these
need it); the fault-path film was 15 % still with no hold over 1 s. It is already motion graphics, and
an overlay would fight its own animation. Skip any film under ~60 % still.

## Inputs

| Input | Where (DG32) |
|---|---|
| Film, captions, segment times | `runs/2026-09-13-dg32-*-package/**/video/<slug>.mp4`, `.vtt`, `<slug>-film.json` (byte-identical to the site's `public/media/<slug>.mp4`; check the md5) |
| Slide geometry (exact) | the deck's artifact-tool `<deck>.pptx.inspect.ndjson` (every text box and shape, 1280x720 stage) |
| Clean slide frames | `frames/slide-NN.png` from the deck export (rendered from these, never from decoded video) |
| No deck? | `scripts/ocr_regions.py --frames <dir> --out ocr.inspect.ndjson` writes the same shape by OCR |

## Workflow

1. **Plan.** `plan_overlay.py --film film.mp4 --film-json f.json --vtt f.vtt --inspect deck.inspect.ndjson --out plan.json`.
   `--film` measures the slide cuts from the film itself (`find_cuts.py`), which the build record does not
   give exactly: on DG32-LITE architecture the real cuts ran up to 0.13 s after film.json by slide 13.
   Read the printed matches. A cue matches the text box sharing the most distinctive words and
   numbers (spoken numbers are normalised: "thirty-two hundred" finds "3,242"), grown to the card that
   contains it. Title and footer boxes are never targets; unmatched cues keep the last framing.
2. **Render.** `node render_overlay.mjs <run> --plan plan.json --slides <frames-dir> [--accent #0077A3]`.
3. **Build.** `build_overlay.py <run> --original film.mp4 --out out/<slug>.mp4`. Frame-exact span
   boundaries pinned to the original's frame count; audio and subtitle streams copied.
4. **Verify.** `verify_overlay.py <run> --original film.mp4 --new out/<slug>.mp4`. Then pull frames
   from the delivered file (before, mid-move and hold on two slides) and look at them.
5. **Replace on the site** only after approval: the new MP4 at the same path; the `.vtt` and poster
   are unchanged because the timing and first frame are unchanged. Run `e2e-qa-review` on `/resources/videos`.

## Judgment rules

Editable policy. Tune here, never inside the step instructions.

- **The sound is the film.** Audio packets, decoded audio and subtitle text must be identical to the
  original. Any edit that needs the audio changed belongs in a re-voice, not here.
- **Move only for a reason.** One move per cue whose sentence names something on the slide; a cue
  that names nothing, or the same region again, keeps the framing. No drift, no idle motion.
- **Gentle.** Push at most 1.12x, 0.8 s ease, dim the rest by 22 % ink. A film is watched for
  minutes; a strong move every few seconds tires the eye.
- **The headline stays whole.** A push that would crop the slide title gives up zoom, then pans only
  as far as the title allows. Footer and source line may leave the frame during a push.
- **The deck's accent, not ours.** These decks are navy and teal; the outline is the deck's darker
  cyan (`#0077A3`, 3:1 on white). The site's copper belongs to the new explainers.
- **Deck geometry before OCR.** OCR (layout-grouped) agreed with exact deck geometry on 32 of 35 cues;
  use it only when no deck exists, and read the plan it produces.

## Verification discipline (what each gate caught on the 2DOM datasheet pilot)

- **A film already in motion was in the plan as "static slides".** Measure stillness first.
- **Per-span frame rounding drifted 3 frames (0.1 s) over 9 slides.** Span edges are now pinned to
  the original's total frame count.
- **A fixed motion floor flagged a real spotlight** (0.78 against a still 0.00, where the card was too
  large to push into). Motion is judged against the original at the same moment: at least 4x it and 0.4.
- **Negative control:** the untouched original checked against itself gives 28 findings and exits 2,
  so a clean overlay result is not an empty population passing.
- **Build records drift from the encoded film** (+0.13 s by slide 13): the still control then sat in the
  original's fade-in and four real moves failed. Boundaries are now measured; the rebuilt cuts match the
  original's within one frame. A first cut detector used absolute darkness and fired every 2 s on a dark
  navy title slide; it now looks for a dip relative to both neighbours.
- **A 1.12x push cropped "Same pins" to "e pins".** The headline band is now a constraint on every framing.
- **Tesseract paragraphs run across a row of cards** (17/35 agreement). Splitting lines at wide gaps
  and stacking only overlapping runs raised it to 32/35.

## Gotchas

- **OCR is installed, off PATH:** `content-ideas/.tools/tesseract/bin/tesseract` (5.3.4). `TESSERACT`
  overrides. Stirling PDF on :8090 also OCRs PDFs. Do not report OCR as missing from a PATH check.
- **Confirm the film on the site is the build you are reading** (md5) before trusting its film.json.
- **`frames/slide-NN.png` must be the export the film was cut from**; compare one against a decoded
  frame (mean difference ~1 is encoding noise; 0.7 between two frames of one hold is the noise floor).
- **The original fades in and out over 0.25 s at every cut.** The first frame of a span is grey by design.

## Skill Relationships

### Category
Media Production

### Dependencies
None. Reads the build records `narrated-deck-film` (or the DG32 `make_film.py`) left behind.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `narrated-deck-film` | Sequential upstream | the film and its records came from it | `video/<slug>-film.json`, `.vtt`, `frames/` |
| `part-explainer-film` | Domain cluster | new explainer from a storyboard | — |
| `hyperframes` | Alternative / Peer | a film that should be rebuilt as motion graphics, not overlaid | — |
| `e2e-qa-review` | Sequential downstream | after replacing a film on the site | `qa/` |

### Runtime Preamble
"I'll measure how still the film is first; if it is already moving, I'll stop. Otherwise each caption
cue gets a gentle move to the slide region it talks about, and I'll prove the audio and captions are
bit-identical to the original."

## Host Compatibility

- Canonical source `content-ideas/skills/film-motion-overlay/`; mirror `.agents/skills/film-motion-overlay/`;
  Claude Code via the `~/.claude/skills/film-motion-overlay` symlink.
- Stdlib Python and Node ESM; on Windows use `python` for `python3`. No subagents needed.
