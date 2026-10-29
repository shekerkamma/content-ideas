---
name: watch-video
description: Bridge to Claude/Codex global `/watch` video analysis for YouTube or local videos. Use when Codex needs upstream frame-aware video notes, sampled video frames, subtitles/transcript, timestamped markdown reports, or visual moments before content research, Genspark AI Slides generation, deck creation, or client-ready presentation workflows.
---

# Watch Video

Use this skill to run the existing Claude/Codex `/watch` implementation as an upstream video-analysis step.

## What It Does

The upstream `/watch` skill:

- downloads video/subtitles with `yt-dlp`
- reads metadata with `ffprobe`
- extracts frames/audio with `ffmpeg`
- prefers native captions
- can fall back to Groq/OpenAI Whisper when configured
- writes a markdown report to stdout
- writes extracted frames under the chosen output directory

It is not a browser session and does not call a vision model by itself.

## Default Chain

For video-to-deck work:

```text
watch-video
→ vault-content-research-pipeline or content brief
→ Genspark AI Slides (`_create_slide`) preview
→ genspark-slides HTML capture
→ /ce-doc-review
→ presentations:Presentations editable rebuild
```

## Run

Use the bundled wrapper:

```bash
python scripts/run_watch.py "<youtube-url-or-local-video>" --out-dir "<run-dir>" --no-whisper
```

Useful options:

```bash
python scripts/run_watch.py "<source>" --out-dir "<run-dir>" --max-frames 80 --resolution 512 --start 00:00 --end 10:00 --no-whisper
python scripts/run_watch.py "<source>" --out-dir "<run-dir>" --whisper groq
```

The wrapper writes:

- `<run-dir>/report.md`
- `<run-dir>/watch/` frame and media artifacts

## Upstream Location

The default implementation is the sibling repository skill:

`../watch`

If the path changes, set:

`WATCH_SKILL_DIR=/path/to/skills/watch`

## Guardrails

- Run `setup.py --check` before the first watch run when possible.
- For videos over 10 minutes, use `--start` and `--end` or expect sparse frame coverage.
- Use `--no-whisper` when native captions are enough or API keys are unavailable.
- If the user wants a deck, save the report in the task workspace and feed it into `genspark-slides` / Presentations.
- Do not claim frame-by-frame exhaustive review unless the frame interval and coverage support it.
