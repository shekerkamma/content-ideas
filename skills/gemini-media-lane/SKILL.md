---
name: gemini-media-lane
description: 'Use when the user invokes /gemini-media-lane to make media with Google''s gemini-api CLI: a 10-second teaser from a film (Gemini watches it, Omni animates a still, TTS narrates), launch or background music (Lyria), a banner or social image with exact text, or Deep Research running in the background while a landing page is built from gemini-api media only. Paid Gemini API key; states the cost before each recipe and verifies every output.'
argument-hint: '<teaser|music|banner|research-page> [source file, topic or brief]'
disable-model-invocation: true
license: MIT
metadata:
  category: Library / API Reference
  source: 'Surya Kunju, "Gemini API CLI + Claude Code" (youtube.com/watch?v=iC5v56h3R7E); github.com/google-gemini/gemini-api-cli v0.4.4; pilot run runs/2026-10-26-gemini-api-cli-pilot/'
  cost-tier: Sonnet
permissions:
  env:
    - GEMINI_API_KEY            # or GOOGLE_GENERATIVE_AI_API_KEY; Windows keeps it in Credential Manager
  network:
    - https://generativelanguage.googleapis.com
  file_read:
    - runs/
  file_write:
    - runs/
  shell:
    allowed_scripts:
      - scripts/check_media.py
      - scripts/dr_extract.py
      - scripts/make_card.py
---

# Gemini Media Lane

Four recipes that copy the gemini-api CLI video's demos, each proven on DeepGrid material on
2026-10-26 (`runs/2026-10-26-gemini-api-cli-pilot/`). The agent plans and checks; `gemini-api`
makes the media. One command per asset, no hand-written API code.

| Recipe | Video | What comes out | Typical cost (Oct 2026) |
|---|---|---|---|
| `teaser` | 0:48 | 10 s MP4: animated still + narration | about USD 0.40 (Omni 360p about USD 0.34) |
| `music` | 4:45 | ~3 min stereo MP3 | cents per track |
| `banner` | 5:03 | card with exact text: Gemini art + real HTML text | about USD 0.15 (one art image) |
| `research-page` | 6:17 | Deep Research report + landing page (image, loop, voice, music) | about USD 2–4 (USD 1–3 research) |

Prices come from Google's docs plus a third-party rate list. Re-check them when a recipe is used
after 2026-11-30, when several Gemini rates double. AI Studio's usage page is the real bill.

## Workflow

Input: `$ARGUMENTS`, a recipe name plus a source (film path, topic, brief). Ask if either is missing.

1. **Preflight.** Run `gemini-api version` (expect 0.4.4) and `gemini-api whoami` (an api-key source
   must be set; never print the key). If either fails, stop and see `troubleshoot.md`.
2. **Cost line.** Tell the user the recipe's estimate from the table, and wait if the user has not
   already approved spend in this conversation.
3. **Run folder.** Write everything under `runs/<YYYY-MM-DD>-gemini-media-<slug>/`. Always pass
   `--out`, and never let a command write into the repo root.
4. **Dry run first** for any new command shape: `--dry-run -o json` shows the request with the key
   redacted.
5. **Run the recipe** from `references/recipes.md` (exact commands, flags and sequencing).
6. **Verify** with `scripts/check_media.py` and by looking at the result (see Output checks).
   Fix and re-run only the failed asset.
7. **Report** what was made, where, what each check showed, and the cost estimate.

### Recipe outlines (details in `references/recipes.md`)

- **teaser.** `analyze` the film for a one-sentence teaser line and a thumbnail time, then view
  that frame yourself. If it's mid-transition, pick a sharper one from a contact sheet. `video -i
  still.png --resolution 360p` makes the clip; `tts` makes the line; ffmpeg mixes the narration
  over the clip's ambience at 1 s, 10 s total. Transcribe it back to confirm the words.
- **music.** `music "<mood> background music for <use>" --out <dir>/name`. Check the duration
  and loudness, and that there are no silent gaps.
- **banner.** Gemini makes the art; code sets the words. Generate **text-free** art with `image
  "<brief>. No text, no letters, no numbers, no logos anywhere."` (`--aspect-ratio 1:1` for the
  square layout, `16:9` for landscape; `--image-size 2K`), look at it, then run `scripts/make_card.py
  --layout square|landscape --art art.jpg --title "..." --tagline "..." --out <run>`. It checks the
  art is text-free, fills `templates/card-<layout>.html` (Poppins), renders with ai-graphics
  `html_to_png.mjs` (1080×1080 or 1200×627) and OCRs the text region. The model-drawn-text route
  (text in the image prompt) is only on request; it misspelled and re-lettered text in testing.
- **research-page.** Start `agent run --agent deep-research-preview-04-2026 --background
  --stream=false --jq '.id'`. Poll `agent status` once a minute in a background job. Meanwhile build
  the page assets with `image`, `video`, `tts` and `music`, and write the HTML around them. When it
  completes, `scripts/dr_extract.py` joins the report parts and saves the charts; render the
  report, then list the findings and which figures are vendor-sourced.

## Output checks

| Asset | Check | Pass |
|---|---|---|
| WAV | `check_media.py wav f.wav` | one RIFF header, size field = file − 8, readable |
| MP3/MP4 | `check_media.py av f` | expected duration, audio present, mean > −30 dB, no >2 s silence |
| Spoken line | `transcribe --format text --out f.txt` | words match the script |
| Card text | `make_card.py` (runs `check_media.py ocr --region`) | every expected line read exactly |
| Art slot | `check_media.py textfree art.jpg` + look at it | no confident 2+ letter words; no cut-off letter at an edge |
| Omni clip | look at a 1 fps contact sheet | product text not re-lettered where it matters |
| Research | `dr_extract.py` | report starts at its `#` title; charts saved; sources listed |

## Judgment rules

Editable policy. Change these lines, not the workflow.

- Copy the reference first: the four recipes are the scope; extra tests come after, labelled as extra.
- State the cost before every paid call that the user has not already approved in this conversation.
- Generate images, never edit screenshots or diagrams that carry text; for an addition, generate the
  element alone and composite it with code.
- Default video resolution: 360p for teasers; 720p+ only on request, with its price stated first.
- Banner text is HTML, never model-drawn, unless the user asks for model-drawn text.
- Banner art is generated text-free; do not crop art out of an image that has text (a cut-off letter
  slips past OCR).
- Image size: `--image-size 2K`; 1K garbles small text.
- Image text counts only if OCR reads it exactly; eyeballing is not a check.
- Omni output is a social teaser, not a product shot, when it redraws product markings.
- Facts in narration and pages come from the user's source; the model's line may paraphrase only
  wording the source already shows (on screen or in the script).
- Deep Research: standard agent by default; Max (USD 3–7) only on request. Poll once a minute; stop
  after 30 minutes and report.
- Deep Research findings are leads, not facts: carry the report's own vendor-marketing flags, and say
  nothing was checked against primary sources unless it was.
- Narration voice: Gemini TTS for drafts and briefings; shipped film narration stays on the user's
  Founder Voice / Kokoro route.

## Gotchas

- **Drift from the reference:** this skill exists because a pilot tested screenshot editing (never
  in the video) and skipped the real demos. Run the recipe asked for.
- **`transcribe` without `--out`** writes `transcript-*.md` into the current folder.
- **`analyze` has no `--stream` flag** (exit 2). `generate`, `agent run` and `agent status` need
  `--stream=false` for JSON.
- **Unsupported aspect ratios** return 400 `invalid_request` (16:10 is not allowed; use 16:9, 3:2 or 21:9).
- **No real transparency:** "transparent background" draws a checkerboard into a JPEG, and
  `--output-mime-type image/png` returns `invalid_request`. Cut the element out by colour.
- **Lyria content filter:** a plain prompt can return `content_blocked` with no reason ("…no
  vocals" did). Simplify the wording once; don't loop.
- **Deep Research output is split:** the report spans several `model_output` text parts, so
  take only the longest and you lose the start. Use `dr_extract.py`.
- **Real usage runs above Google's "typical":** one run used 948k input tokens (9% cached) against
  the docs' ~250k.
- **Gemini's thumbnail pick can land mid-transition.** Always look at the frame.
- **The Pro plan does not pay for this:** Google AI Pro covers the AI Studio website only; the
  CLI bills the API key, and Pro's monthly Cloud credits apply first.
- **Dollar sign before a digit in this file:** Claude Code replaces a dollar sign followed by a number
  with the invocation's arguments (positional placeholders), so a price written that way turns into an argument.
  Write prices as "USD 0.15".
- **"Any letter" is not an art-slot check:** OCR reports 31–50 letter-like fragments on clean chip art,
  so `textfree` counts only confident words of 2+ letters. A lone letter cut off at a crop edge passes
  it (tested), which is why the art is generated text-free and you still look at it.
- **Old Node corrupts renders on the Windows drive:** the system Node v18 wrote a 512 KiB non-PNG
  when the output sat on `/mnt/c` (fine on the WSL disk). `make_card.py` prefers nvm's newest Node,
  and fails if the render isn't a real PNG instead of OCR-ing garbage.
- **Hyphenated titles wrap at the hyphen:** the templates set `white-space:nowrap` on the title; keep
  titles short enough for the layout (9 characters fit both at the template sizes).
- **O vs 0 in squared fonts:** Tesseract reads a squared "O" as a zero. Ask for "a rounded sans-serif
  where O is a perfect circle" and OCR with `--region`. The model also tends to add a full stop.
- **Shell cwd:** finish back at the repo root, or the proof-of-done hook runs pytest in a test-less
  folder (exit 5).

See `troubleshoot.md` for error-by-error fixes.

## Skill Relationships

### Category
Library / API Reference

### Dependencies
- `gemini-api` CLI v0.4.4 on PATH (`~/.local/bin` on WSL, `C:\Users\sheke\.local\bin` on Windows).
- `ai-graphics` (`~/.claude/skills/ai-graphics/scripts/html_to_png.mjs` + Playwright) for banner renders;
  on Windows `make_card.py` runs it through `wsl.exe` (override with `AI_GRAPHICS_HTML_TO_PNG`).
  Poppins installed (the templates fall back to system-ui without it).
- ffmpeg/ffprobe; Tesseract for OCR. `check_media.py` finds it on its own: `TESSERACT_BIN`, then the
  repo-local `.tools/tesseract/bin/tesseract`, then PATH, then Program Files. On Windows with none of
  those, it runs the WSL repo build through `wsl.exe` (override the path with `WSL_TESSERACT`).

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `watch` / `watch-video` | Sequential upstream | study a reference video before copying it | `report.md` + frames |
| `ai-graphics` | Dependency (banner) + Peer | banner renders through its `html_to_png.mjs`; use the full skill for diagrams, dense infographics or edits to existing images | `card-<layout>.html` → `.png` |
| `pptx-design-quality` (`narrate_clips.py`) | Domain cluster | deck clip narration; already defaults to `gemini-api tts` | `<out-dir>/*.mp4` |
| `deep-research` | Alternative / Peer | Claude-run research with its own sourcing rules | brief file |
| `part-explainer-film` / `animate` | Sequential upstream | the film a teaser is cut from | film MP4 |
| `e2e-qa-review` | Prerequisite / Gate | a research-page landing page that will ship | QA report |
| `verifier` | Prerequisite / Gate before "done" | non-trivial claims | VERDICT line |

### Runtime Preamble
"Using gemini-media-lane (paid Gemini key). Recipe: <name>, estimate: <cost>. For text-heavy
graphics or edits to an existing image, /ai-graphics fits better. For Claude-run research,
/deep-research. To study a reference video first, /watch."

## Host Compatibility

### Target Hosts
- Claude Code: yes — `~/.claude/skills/gemini-media-lane` symlinks to `skills/gemini-media-lane/`.
- Codex/OpenAI: yes — `.agents/skills/gemini-media-lane/` (byte-identical copy).
- OpenHands / DSH: yes — `.agents/skills/gemini-media-lane/`.

### Canonical Source
`skills/gemini-media-lane/`. `.agents/skills/gemini-media-lane/` is a byte-identical copy
(`check_skills.py --rule crosstree`).

### Tool Mapping
- `disable-model-invocation` is Claude-only; on other hosts the cost line in step 2 is the guard.
- `AskUserQuestion` → a concise chat question.
- Background polling (`run_in_background`) → a detached shell loop writing `dr-poll.log`.
- Reading images to check frames → any host's image viewer; OCR stays the text check.

### Source / Tool Order
1. This file, then `references/recipes.md` and `troubleshoot.md`.
2. The user's local source files (films, scripts, narration JSON) and prior run folders.
3. `gemini-api --help`, `--usage` and `--schema`: the binary describes itself.
4. Official docs at ai.google.dev for prices and model changes, via Exa before generic web search.
