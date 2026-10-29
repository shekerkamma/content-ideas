---
name: narrated-deck-film
description: Use when an existing slide deck must become a narrated presentation film with a cloned or branded voice — investor briefs, pre-sales decks, board readouts, use-case walkthroughs. Triggers on "turn this deck into a video", "narrated deck", "investor pitch video", "voiceover for these slides", "deck to film with my voice". Narration comes from an authored corpus and is gated against reciting the slides; runtime is derived from measured speech; structural slides missing from the source deck (executive summary, act dividers, conclusion) are authored in the deck's own design system. Not for turning a video into slides (use video-to-deck) and not for per-use-case films built from scratch (use use-case-film).
license: MIT
metadata:
  category: Media Production
  version: '1.0'
  compatibility: Python 3 stdlib plus ffmpeg/ffprobe and a Chromium binary. ElevenLabs for voice. Claude Code, Codex CLI, or any host reading agent Markdown.
  legacy-frontmatter:
    argument-hint: "<film-config.json>"
    user-invocable: true
---

# Narrated Deck Film

A deck plus an authored narration corpus becomes a 1080p film whose runtime is
decided by the speech, not by a template.

The chain is: **authored narration → gate → measured speech → measured
timings → composition → render → gate.** Timing flows one way. No duration is
hand-typed and none is measured twice.

## When to invoke

- "turn this deck into a video", "narrated version of this deck"
- An investor or pre-sales deck that must travel without a presenter
- An existing narrated cut that reads as slide-reading and needs rebuilding

Do **not** use to summarise a video into slides, or to build a film that has
no source deck.

## Workflow

1. **Find the narration corpus before writing one.** Authored narration
   usually already exists on disk. Regenerating it from extracted slide text
   is the most expensive mistake this pipeline can make — see the judgment
   rules.
2. **Gate the narration** — `scripts/check_narration.py <narration.json>
   --deck <slides.pptx|slide-text.txt>`. Blocks on recitation and on internal
   markers. Fix the writing, never the threshold. When the narration lives in a
   story pack (`## 9. Narration`, which is also the deck's speaker notes), rewrite
   flagged lines there with `scripts/rewrite_narration.py`: it gates the merged
   text and refuses to write while any slide is flagged.
3. **Storyboard the missing structure.** Run `story-architect`. Decks written
   for reading almost always lack a front executive summary, act dividers, and
   a closing synthesis — a reader can flip, a film viewer cannot.
4. **Author those slides** — `scripts/render_slides.py <spec.json> --out <dir>`,
   in the host deck's own tokens and typeface.
5. **Voice it** — `scripts/synth_narration.py <config.json>`. Budget-preflighted,
   resumable, request-stitched. `--dry-run` costs nothing. With no cloned voice,
   voice locally with Kokoro (setup in `use-case-film`), then bring off-band
   slides to pace with `scripts/tune_slide_speeds.py <report>` and voice again;
   gate the second pass.
6. **Compose** — `scripts/build_film.py <config.json>`. One segment per slide,
   each bounded by its measured narration.
7. **Gate delivery** — `scripts/verify_film.py <config.json>`.

## Judgment rules

Editable policy. Tune here, never inside the step instructions.

- **Narration is synthesis, never recitation.** A voice track assembled from
  slide text passes every audio and video check ever written — right length,
  right voice, present — and is worthless in front of a buyer. The reader can
  already read the slide. Say what it *means*. Measured: two authored corpora
  in this repo scored 27% and 32% mean trigram echo against their own decks
  before rewriting, and 9% after.
- **Lead with the assertion, not the headline.** If the narration's first
  clause restates the slide title, the slide and the voice are doing one job
  between them instead of two.
- **Never voice what only a reader needs.** Slide numbers and ids, the
  confidentiality footer, registration numbers, contact details, version
  annotations, and "in plain terms" analogy blocks. These are reading aids;
  spoken, they are padding at best and a leak at worst.
- **Runtime is an output, not an input.** Never target a duration. Write the
  beats the material justifies, measure the speech, let the film be as long as
  it is.
- **Pace is a measurement, not a preference.** Compute words ÷ summed audio
  duration. Around 150 wpm reads as considered; 190+ reads as rushed and is
  the single most common defect in a generated narration. Correct it with the
  provider's speed control and re-measure — do not cut the writing to fix it.
- **One voicing per slide id, not per deck ordering.** Decks shipped in
  several orders are one narration set and several `slide_order` lists.
  Re-voicing a permutation is a pure duplicate charge.
- **A cloned voice is the one honest reason to pay for TTS.** It cannot be
  produced locally. Everything else — budget, resume, stitching — exists so
  that paying for it once is enough.
- **Motion must not cover content.** Prefer a full-frame `insert` over a
  corner `pip`. A dense deck has no free corner, and an overlay on one hides
  live text while looking deliberate.

## Verification discipline

Every gate below exists because its absence once produced a green run over a
broken artifact.

- **Preflight the budget before spending any of it.** Discovering a quota
  ceiling at slide N leaves N−1 slides paid for and no usable film.
- **A gate whose population came back empty is worse than no gate**, because
  it now certifies the defect. `check_narration.py` blocks — rather than
  passing — when the deck yields no text, or when narration keys and deck keys
  do not intersect. Both happened here: a flattened-image `.pptx` parsed to
  zero slides and the check reported CLEAN.
- **Prove the typeface against a control.** A page whose webfont fails to load
  renders in the fallback and looks fine. `render_slides.py` measures the
  family against serif and blocks on equal widths. Related: Chromium here does
  not resolve fontconfig families at all, so fonts must be embedded as data
  URIs — and the probe must wait on `document.fonts.ready`, or it measures the
  fallback during the `font-display: block` period and reports a false failure.
- **Prove motion against a static control, not a threshold.** Compare the same
  0.5 s delta inside the insert window against a still slide in the same film.
- **Audio presence is not audio content.** Compare `mean_volume` against
  generated silence (`anullsrc` reads ≈ −91 dB), not against a hand-picked dB.
- **Retry only what is retryable.** Retrying a 401 or 422 eight times hides it
  and returns `None`, which the next stage then treats as a file.
- **Assert on every structural string replace.** A no-op replace is
  indistinguishable from success. One here silently did nothing and the
  rendered slide looked plausible.
- **Never `pkill -f <pattern>` from a shell whose own command line contains
  that pattern.** It matches its parent and kills the caller (exit 144).
  Match on a pid via `ps -eo pid,args | awk`.

## Scripts

| Script | Does |
|---|---|
| `scripts/check_narration.py` | Gates narration for recitation, internal markers, and assertion |
| `scripts/rewrite_narration.py` | Rewrites story-pack narration lines, gated in memory first; refuses to write while flagged |
| `scripts/tune_slide_speeds.py` | Per-slide TTS speeds that bring every slide to the target pace, from a measured report |
| `scripts/synth_narration.py` | Budget-preflighted, resumable, request-stitched TTS; emits the duration manifest |
| `scripts/render_slides.py` | Authors executive-summary / divider / conclusion slides in the deck's tokens |
| `scripts/build_film.py` | One measured segment per slide, Ken Burns plus optional motion insert, concat |
| `scripts/verify_film.py` | Duration, streams, silence control, motion control, slide coverage |

## Config

```jsonc
{
  "voice_id": "...", "model_id": "eleven_multilingual_v2",
  "voice_settings": { "stability": 0.40, "similarity_boost": 0.88,
                      "style": 0.35, "use_speaker_boost": true, "speed": 0.85 },
  "narration": "narration/deck.json",       // authored, one entry per slide id
  "slides_dir": "slides/DECK",
  "slide_pattern": "p-{slide:02d}.png",
  "slide_files": { "exec": "slides/NEW/exec.png" },   // named structural slides
  "slide_order": ["1", "exec", "2", "3"],            // ordering lives here only
  "audio_dir": "...", "work_dir": "...",
  "tail_padding": 0.9, "zoom_max": 1.08,
  "motion": { "source": "video/capture.webm",
              "cues": [ { "slide": "7", "mode": "insert",
                          "start_frac": 0.25, "seconds": 10 } ] },
  "output": "exports/film.mp4"
}
```

## Setup

`ELEVENLABS_API_KEY` in the environment — never in a config file, a script, or
a commit. Set it in `~/.bashrc` and mirror it into
`.claude/settings.local.json`'s `env` block, per the repo's two-layer pattern.
`DECK_CHROMIUM` pins a Chromium binary when the bundled path is absent.
