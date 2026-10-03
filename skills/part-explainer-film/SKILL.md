---
name: part-explainer-film
description: Use when a product part with a draw.io architecture diagram and a story-architect storyboard must become a short narrated explainer film (45-90 s) in the Founder Voice, with a camera that walks the real diagram beat by beat. Triggers on "explainer film for SKU-3", "make the part explainers", "animate the architecture diagram with narration", "one-minute film per product page". Not for an existing slide deck (use narrated-deck-film), not for adding motion over an already narrated film (use film-motion-overlay), not for a social carousel (use storyboard-to-carousel).
license: MIT
metadata:
  category: Media Production
  version: '1.0'
  cost-tier: Sonnet executes it; the narration step needs judgment, every other step is a script. ElevenLabs is paid per character; Kokoro is free.
  compatibility: Python 3 stdlib, ffmpeg/ffprobe, Node 20+ with playwright and a Chromium build. Groq Whisper for the transcript gate. Claude Code, Codex CLI, or any host reading agent Markdown.
  legacy-frontmatter:
    argument-hint: "<part-slug> e.g. sku-3"
    user-invocable: true
---

# Part Explainer Film

A storyboard and the part's own architecture diagram become a narrated film: an opening on the
problem, one scene per storyboard beat with the camera on that beat's zones, and a close on what is
still unproven. The diagram is the real draw.io SVG from the site, never a redraw.

The chain runs one way: **storyboard → scenes → authored narration → script gate → voice → voice gate
→ frames → film → delivery gate.** Durations are decided once, by the measured voice.

## Inputs (DeepGrid v6 paths; pass others for another site)

| Input | Where |
|---|---|
| Storyboard | `content-ideas/runs/2026-10-03-arch-storyboards/<slug>.json` (headline, lead, beats with marks + zones, closing) |
| Diagram source + SVG | `deepgrid-dr-silicon-v6/public/downloads/<slug>-architecture.drawio`, `public/diagrams/<slug>-architecture.svg` |
| Product page text (value authority) | the part's record in `app/product-pages-data.ts` plus `<slug>.sections.json`, saved as `page-text.txt` |
| Design system | `deepgrid-dr-silicon-v6/design-system/` (tokens.json + fonts; the approved DeepGrid Semi system) |
| Wordmark | `public/brand/deepgrid-semi-wordmark.png` |

Run folder: `content-ideas/runs/<date>-part-explainers/<slug>/`. Scripts are in `scripts/`.

## Workflow

1. **Locate the zones.** `locate_zones.py <drawio> <svg> --out zones.json`. It measures the drawio-to-SVG
   offset from the zone boxes themselves and blocks if fewer than two agree.
2. **Scaffold scenes.** `scaffold_scenes.py <storyboard> --zones zones.json --kicker "SKU-3 · HI-REL PMIC" --out scenes.json`.
   It refuses to overwrite an existing scenes.json, which may hold authored narration.
3. **Author every `label` and `narration`.** This is the one judgment step. Follow `references/voice.md`:
   2-6 on-screen words, narration written for the ear, an assertion per scene, numerals only from the
   storyboard or page, emotion tags only at the arc points, pauses from punctuation.
4. **Gate the script.** `gate_script.py scenes.json --page-text page-text.txt` (0 clean, 2 findings).
   Fix the writing, never the thresholds.
5. **Voice it.** `voice.py scenes.json --provider elevenlabs --page-text page-text.txt --dry-run` first
   (budget preflight, nothing spent), then without `--dry-run`. `--provider kokoro` is the free
   placeholder. `ELEVENLABS_API_KEY` must be in the environment. For Kokoro, open the pauses on every
   scene (step 6), gate, and if the pace is off run `tune_kokoro.py scenes.json` (per-scene speed from
   the measured pace, clamped 0.85-1.15), then voice, pace and gate once more. `runs/2026-10-03-part-explainers/batch.sh`
   is the worked batch for nine parts.
6. **Gate the voice.** `measure_voice.py scenes.json`: per-scene pace, longest pause, transcript match.
   A scene the voice rushed gets `extend_pauses.py scenes.json --scene <id>` (opens the gaps the voice
   left at script punctuation to the Holt lengths; never stretches speech), then gate again. A
   transcript difference that is the transcriber, not the voice, is waived in scenes.json with a reason.
7. **Render frames.** `node render_frames.mjs <run> --svg <svg> --ds <design-system> --wordmark <png>`.
   Blocks if a design-system font fails to load. Look at a contact sheet of hold and mid-move frames.
8. **Build.** `build_film.py <run> --out <slug>-explainer` → `out/<slug>-explainer.mp4`, `.vtt`, `-poster.jpg`.
9. **Gate delivery.** `verify_film.py <run> --out <slug>-explainer`. Then look at frames pulled from
   the delivered MP4, not from the renderer.
10. **Integrate** (once the pilot is approved): copy MP4, VTT and poster to the site's
    `public/media/explainers/`, place the player at the top of "Inside the part" with the VTT as a
    `<track>`, no autoplay with sound, then run `e2e-qa-review`.

## Judgment rules

Editable policy. Tune here, never inside the step instructions.

- **Voice: `eleven_v3`, Founder Voice `xqmZGpVMlMzAiUYMY0NQ`, stability 0.5, similarity 0.8.** Chosen
  on 2026-10-03 from five measured takes (`runs/2026-10-03-founder-voice-sample/DECISION.md`). Kokoro
  `bm_george` is the placeholder when the ElevenLabs quota is short, never the delivered voice.
- **Holt delivery.** 140-155 spoken wpm for the film; pauses 0.25-0.45 s at a comma, 0.55-0.85 s at a
  full stop, 1.0-1.3 s at a transition; nothing over 1.6 s. Emotion is performed by the model
  (`[thoughtful]` open, `[serious]` on what is unproven, `[confident]` close), never faked by
  stretching audio or speaking stage directions.
- **One idea per scene; the label names it, the narration says what it means.** Narration that echoes
  its beat body over 35% of trigrams is recitation.
- **Every number on screen or spoken is on the product page or storyboard.** The page wins over any
  annex. No market figures, no "certified" or "compliant"; standards are "designed toward".
- **Runtime is an output.** Write what the beats need, measure the voice; the gate's 45-90 s band is a
  warning that the writing is too thin or too long, not a target to pad to.
- **Captions ship as a track, not burned in.** The lower frame is the diagram; text over it would
  hide what is being explained.
- **Motion: one camera move per scene, then stillness.** The move carries the eye from the last
  beat's zones to this one; the hold does not drift. Labels never sit on the diagram.

## Verification discipline (what each gate caught on the SKU-3 pilot)

- **v3 rejects request stitching.** `previous_text`/`next_text`/`previous_request_ids` return HTTP 400
  on `eleven_v3`. `narrated-deck-film/scripts/synth_narration.py` now skips them for v3.
- **Shorter sentences did not slow a rushed close** (198 → 203 wpm, longest pause 0.26 s). Opening the
  voice's own gaps to Holt lengths did (161 wpm, film 152 wpm), with no re-voice and no stretched speech.
- **Whisper word times absorb trailing silence.** Pauses are measured with silencedetect; word times
  only locate boundaries. Inside a boundary window take the longest gap: the nearest was a 0.07 s
  breath inside a word.
- **Transcript caches are keyed by audio file**, so a paced or re-voiced take is heard again.
- **The font check measured fallbacks** until faces were loaded explicitly: an unused face falls back
  to the default font, which differs in width from sans-serif and monospace and passed.
- **Kokoro at speed 1.0 ran 123-174 wpm across one film's scenes.** Opening the pauses alone left the
  film at 156; one per-scene tuning pass brought it to 151 with every scene inside tolerance.
- **Caches are keyed by audio content**, not file name: a re-voiced Kokoro scene keeps its name, and a
  name-keyed transcript would have matched the new audio against the old words.
- **The transcriber writes some numbers as digits and others as words, and splits compounds**
  ("busload"). The gate compares numbers as digits and ignores pure word-spacing differences, printing each.
- **When two transcription models agree on a different word** ("key erase" heard as "key arrays",
  "bills" as "builds"), rewrite the phrase: the listener will mishear it too. Waive only connected-speech elisions.
- **Diagram names carry HTML escapes and double spaces** ("Sensing &amp; math", "Flight control  ·  hard
  real-time"), and a bus is a dark bar, not a zone box; the locator and scaffold handle all three.
- **The delivery gate flagged a static opening** (move delta 0.06 against a still hold). The film now
  enters with a settle from a wider view. Motion is proven against the hold of the same scene.

## Gotchas

- **Never author narration from the beat body.** The gate's echo check exists because it is the
  cheapest mistake to make and it sounds fine.
- **Never print the ElevenLabs key.** On this machine it is read at runtime from the DeepGrid batch
  script on D: (see the `elevenlabs-key-and-founder-voice` memory); report only its length.
- **Check the budget before every batch.** The meter lags; the dry run reads it live.
- **A storyboard zone name must match the diagram label exactly** (`Pre-regulator · synchronous buck`);
  scaffold blocks with the list of real names when it does not.
- **Reading-path markers are edge labels** with no box in the .drawio; the renderer finds them in the SVG.

## Skill Relationships

### Category
Media Production (Business Automation with sub-skill dependencies)

### Dependencies
- `narrated-deck-film`: its `synth_narration.py` voices ElevenLabs runs (budget preflight, resume).
- `use-case-film`: its `tts_beats.py` voices the Kokoro placeholder.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `story-architect` | Prerequisite | always; the storyboard is its output | `runs/2026-10-03-arch-storyboards/<slug>.json` |
| `architecture-to-everything` | Sequential upstream | the diagram and guide | `public/downloads/<slug>-architecture.drawio`, SVG |
| `narrated-deck-film` | Alternative / Peer, and dependency | a slide deck instead of a diagram | `work/synth.json` |
| `film-motion-overlay` | Domain cluster | motion over an existing narrated film | — |
| `storyboard-to-carousel` | Parallel / Complement | same storyboard, social output | — |
| `e2e-qa-review` | Sequential downstream | after site integration | `qa/` |

### Runtime Preamble
"I'll build the explainer from the part's storyboard and its real architecture diagram. Has
story-architect produced the storyboard? Voice is the Founder Voice on eleven_v3; I check the
ElevenLabs budget before spending and fall back to Kokoro as a placeholder. For a slide deck use
narrated-deck-film instead."

## Host Compatibility

- Canonical source: `content-ideas/skills/part-explainer-film/`; byte-identical mirror in
  `.agents/skills/part-explainer-film/` (Codex, DeepSeek Harness, OpenHands); Claude Code reaches it via
  the `~/.claude/skills/part-explainer-film` symlink.
- Scripts are stdlib Python and Node ESM; on Windows use `python` for `python3`.
- Claude `AskUserQuestion` maps to one plain question; nothing in the chain needs subagents.
