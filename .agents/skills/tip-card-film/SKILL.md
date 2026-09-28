---
name: tip-card-film
description: Use when a recorded talking-head video needs on-screen graphics at the moments it makes a point — "add tip cards to my video", "make motion graphics for this recording", "cut this into titled segments", "picture-in-picture explainer", "transcript to motion graphics", "animate the key moments". Builds a HyperFrames project where, for each card, the camera blurs and shrinks into a rounded picture-in-picture while a titled card (with a screenshot or a typed prompt box) builds beside it, then reverses; styled entirely from your design tokens. Renders to MP4 with the camera's own audio.
license: MIT
metadata:
  category: Video production
  version: '1.0'
  cost-tier: 'Sonnet to choose the moments from a transcript; building and rendering are scripts (no model).'
---

# Tip-card films

A reusable cut for explainer videos: talk to camera, and at each point worth showing, the shot slides into
a picture-in-picture while a card states the point. The choreography is a well-worn pattern (RoboNuggets'
"25 Claude Design tricks" video runs about thirty of these); the look is yours, because every colour and
font comes from the spec's tokens. It is the transcript-to-motion-graphics tip made repeatable.

## Workflow

1. **Record** the talking-head video.
2. **Get a word-timed transcript** (the `watch` skill, or Whisper) and choose the moments: one card per point,
   at least 1.5 s long (in, hold, out), not overlapping. Use the words' timestamps; a card should land on
   the word that makes the point.
3. **Write `spec.json`** beside the video (format below). Colours and fonts come from the site's design
   tokens (`design-tokens`, DESIGN.md); screenshots come from your own work (`design-os` finds them).
4. **Build, check, render:**

```bash
S=<this skill's directory>/scripts
python3 $S/build_tip_film.py spec.json film-project
cd film-project
hyperframes check                            # 0 errors; layout, motion and contrast audits must show samples
hyperframes render --output film.mp4
```

5. **Verify the MP4**, not only the render log: duration equals the camera's, an audio stream exists, and
   a frame from each card shows the card (see "Measured").

## spec.json

```json
{
  "title": "Five design tricks",
  "camera": "talk.mp4",
  "width": 1920, "height": 1080,
  "tokens": {"bg": "#f4f1ea", "ink": "#1d1f21", "ink2": "#5e646a", "accent": "#b4622a",
             "surface": "#1b1d1f", "surface_ink": "#f2efe8",
             "font_display": "Newsreader, serif", "font_text": "Inter, sans-serif"},
  "fonts": [{"family": "Newsreader", "file": "fonts/Newsreader.woff2", "weight": "400 700"},
            {"family": "Inter", "file": "fonts/Inter.woff2", "weight": "400 700"}],
  "cards": [
    {"start": 12.4, "end": 17.8, "title": "Grab a font", "subtitle": "one that fits the brand", "image": "shots/fonts.png"},
    {"start": 21.0, "end": 26.0, "title": "Ask for SVG", "subtitle": "editable and animatable",
     "prompt": "Make the icons and the diagram as SVG, not raster."}
  ]
}
```

- A card shows an `image`, a `prompt` (a dark prompt box whose text types itself in), or neither.
- Paths are relative to the spec and are copied into the project's `assets/`.
- The builder refuses a bad spec with `BLOCKED` and every problem listed: overlapping or too-short cards,
  a card past the end of the video, a missing file, or a named font without a local file.

## Measured

A 12 s synthetic camera (moving test pattern and a 440 Hz tone), two cards, 1280×720, CLI 0.8.81:
`hyperframes check` passed (0 errors; 0 layout issues across 9 samples; 5/5 text checks WCAG AA); the render
took 3 min 27 s on software GPU and produced 12.0 s of video with audio (mean −21 dB). Against the source:

| Phase | Frame vs camera (mean abs. diff.) | PiP vs shrunken camera |
|---|---|---|
| before / between / after cards | 6–10 (encode noise) | 124–138 (no PiP) |
| during each card | 128–141 (card on screen) | **~10** (camera is in the PiP) |

That comparison is the verification to repeat on a real film: a render that "succeeds" with the camera
stuck full-frame would pass every log line and fail this table.

## Judgment rules

- **Tokens, not taste.** Colours and fonts come from the brand's tokens; never hand-pick new ones for a film.
- **Ship the fonts.** A generic family resolves to whatever the render machine has installed: `serif` came
  out sans-serif here. For any look that matters, list the font files in `fonts`.
- **One point per card, landed on the word.** A card that arrives before the sentence reads as a slide
  deck; one that arrives after reads as a correction.
- **Real screenshots over mock-ups.** A card is evidence; use your own work (design-os), not generated
  stand-ins.

## Gotchas

- **Use the `hyperframes` you can see.** Here `npx hyperframes@0.8.74 check` failed with "Missing browser
  script layout-audit.browser.js" while that file sat in its package; the global install (0.8.81) ran every
  audit. When `check` reports `0 sample(s)` or `0/0 text checks`, nothing was measured: fix the CLI before
  trusting it.
- `check` warns `nested_structure_needs_subcomposition` for each card. That concerns Studio's timeline
  display (one row per element), not the render; cards stay in `index.html` so the camera and the card
  animate on one timeline.
- The camera `<video>` is muted and its sound is a separate `<audio id="cam-audio">` on the same file, as
  HyperFrames requires; a render without that `id` is silent.
- Rendering is slow on software GPU (about 17 s per second of 720p here). Render a short spec first.

## Skill Relationships

| Skill | Pattern | Handoff |
|---|---|---|
| `watch` | Upstream | word-timed transcript to choose card moments |
| `design-tokens` | Upstream | the `tokens` block |
| `design-os` | Upstream | finds the screenshots for `image` cards |
| `hyperframes`, `hyperframes-core`, `hyperframes-cli` | Dependency | the composition contract, `check`, `render` |
| `narrated-deck-film` | Peer | narrated slide films; this one starts from a camera recording |

## Host Compatibility

Stdlib Python plus ffmpeg/ffprobe; rendering needs Node 22+ and the `hyperframes` CLI. Works in Claude
Code, Codex, DeepSeek Harness and OpenHands; on Windows run `python`. Canonical at `skills/tip-card-film/`,
byte-identical mirror at `.agents/skills/tip-card-film/`.
