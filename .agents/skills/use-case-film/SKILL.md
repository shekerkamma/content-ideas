---
name: use-case-film
description: Use when a set of use cases, product lines, or regulatory obligations must become long-form narrated films — one film per use case, minutes not seconds. Triggers on "film per use case", "comprehensive use-case video", "explainer film for each", "narrated walkthrough of each use case", "turn Part III into films". Derives every card duration from measured narration audio, synthesises speech locally with no API or quota, and gates delivery on a claim-evidence pass plus a silence-control audio check. Not for short social ads (use video-to-deck or an ad pipeline) and not for turning one video into slides (use video-to-deck).
license: MIT
metadata:
  category: Media Production
  version: '1.0'
  compatibility: Python 3 stdlib plus kokoro-onnx/soundfile for local TTS. Node 22+ and FFmpeg for render. Claude Code, Codex CLI, Codex desktop, or any host reading agent Markdown.
---

# Use-Case Film

One comprehensive narrated film per use case, built so the runtime is decided by
what there is to say rather than by a template.

The pipeline is: **source of record → beats → local speech → measured timings →
composition → render → gate.** Timing flows one way only. Nothing is hand-typed.

## When to invoke

- "a film for each use case", "comprehensive per-use-case video"
- A portfolio, product ladder, or regulatory matrix that needs one film per entry
- An existing short cut that reads as thin and needs real length

Do **not** use for 15–60s social ads, or to summarise one video into slides.

## Workflow

1. **Locate the source of record.** Search the repo before generating anything.
   A corpus of authored narration, briefs, or analyses usually already exists;
   paraphrasing a web page when a 6,000-word authored script is on disk is the
   most expensive mistake this pipeline can make.
2. **Extract the use cases.** If the source is a single-page app, the section
   may render only on click — dump `document.body.innerText` *after* navigating,
   and confirm each use case appears with its detail, not just its row.
3. **Write beats.** Each film: rule → challenge → what is supplied → the
   boundary (what is *not* supplied) → the numbers → who is in the room → the
   gate that proves it → the risk → next action. One `vo` string per beat.
4. **Synthesise per beat** — `scripts/tts_beats.py`. Local, unlimited.
5. **Measure** — `scripts/measure_beats.py` reads each WAV and emits the
   manifest. This is the only place durations are decided.
6. **Compose** — `scripts/build_film.py` renders HTML with `data-start` /
   `data-duration` taken from the manifest.
7. **Render and mux**, then **gate** — `scripts/verify_films.py`.

## Judgment rules

Editable policy. Tune here, never inside the step instructions.

- **Runtime is an output, not an input.** Never target a duration. Write the
  beats the material justifies, measure the speech, and let the film be as long
  as it is. A film cut to fit a number reads as thin because it is.
- **Every film names its own risk out loud.** A use case whose weakness is
  absent from its film is marketing, and marketing not backed by a measured
  result is exactly what a serious source will have told you not to fund.
- **A claim marked REQUIRES VERIFICATION never enters a film.** Advertising is
  the worst place for an unverified claim: it is public and it reaches buyers.
  Exclude it and record the exclusion in the film's brief.
- **State the boundary.** Where the subject supplies part of a system, spend a
  card on what it does *not* supply. This is what makes a film usable in front
  of the integrator who owns the rest.
- **Cheapest voice that clears the quality bar.** Local neural TTS first
  (Kokoro), platform TTS second (SAPI/`say`), a paid API never by default. A
  daily-capped API is disqualified for long-form by arithmetic: 58 beats does
  not fit in 10 requests.
- **Prefer a source's own framing over a summary of it.** Where a product card
  and a detailed section disagree, the detailed section is usually the one that
  survived review.

## Verification discipline

Every gate below exists because its absence once produced a green run over a
broken artifact.

- **A duration that matches the manifest is the proof the chain held.** Compare
  rendered duration to the manifest, not to intent.
- **Audio presence is not audio content.** Measure `mean_volume` and compare
  against a generated silent control (`anullsrc` reads ≈ −91 dB). A stream that
  exists can still be silence.
- **Never copy a render that is still being written.** ffprobe the duration
  before copying to a delivery path; a partial mux is a valid file that stops
  short.
- **`ffmpeg -v error` suppresses `silencedetect` output.** Any check parsing
  silencedetect must not pass it, or it will report zero silences on audio full
  of them.
- **Never wait on `pgrep -f <pattern>` when the launching command line contains
  that pattern.** It matches its own parent and waits forever. Match on a pid,
  or on `ps -eo args | grep '[r]ender'`.
- **Read exit codes before a pipe, not after.** `cmd | tail` reports `tail`'s
  status; an install can "succeed" while nothing installed.

## Scripts

| Script | Does |
|---|---|
| `scripts/tts_beats.py` | One WAV per beat via local Kokoro; loads the model once |
| `scripts/measure_beats.py` | Reads every WAV, emits `film-manifest.json` |
| `scripts/build_film.py` | Beats + manifest → composition HTML + assembled narration |
| `scripts/verify_films.py` | Duration/stream/level gate with a silence control |

## Setup

```bash
uv venv ~/.venvs/kokoro --python 3.12
uv pip install --python ~/.venvs/kokoro/bin/python kokoro-onnx soundfile
# model + voices (~325MB + 28MB) — resumable, do NOT wrap in a short timeout
curl -L -C - -o ~/.cache/hyperframes/tts/models/kokoro-v1.0.onnx \
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
```

Verify the model is byte-complete before use; a truncated ONNX fails opaquely.
