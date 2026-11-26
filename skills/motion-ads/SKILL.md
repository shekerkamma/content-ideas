---
name: motion-ads
description: Make premium motion graphics and product ads in three levels. Level 1 is code only (HTML, canvas, three.js rendered to video, with sound made by code). Level 2 edits real footage and adds code-built graphics, an AI voiceover and AI music through Higgsfield. Level 3 makes photoreal product ads from keyframe stills and first-frame/last-frame video shots joined into one continuous camera move. Use this whenever someone asks for a product ad, promo, launch video, motion graphic, animated logo or title, SaaS or app demo animation, event recap or trailer, "an Apple-style ad", a spec ad, or wants to recreate the style of a video they like, even if they do not say "motion graphics". Also use it to add sound design to a silent video, to storyboard an ad, or to blend a person into the end of an ad.
---

# Motion ads

Make an ad the way a small studio would: gather the real ingredients, agree a storyboard, build it, then add sound. The person directs. You do the work and show it at each gate.

Every job follows the same four steps at every level. Do them in order, and stop where it says stop.

## The four steps

### 1. Assets

Put everything in one project folder, sorted, before any creative work.

```
project/
  assets/     real logo files, product photos, screenshots, footage, SOURCES.md
  refs/       videos or stills whose style is being followed (optional)
  storyboard/ the board and its frames
  build/      pages, keyframes, shots, prompts
  sound/      music, voice, effects, cue sheet
  out/        review sheets, drafts, the final file
  credits.json, credits.md    (only when paid models are used)
```

- Ask for, or fetch, the **real** things: the logo as a vector file, product photos from several angles, the real screens of the app. Never draw a logo or a product from memory.
- Check the resolution of everything. Low-resolution input gives a fake-looking result.
- Write where each file came from in `assets/SOURCES.md`.
- If something essential is missing, say so now and ask for it. Do not fake it.

### 2. Storyboard, then stop

Make a numbered storyboard and **stop for approval before building anything**. A storyboard costs seconds; a rebuilt animation costs minutes and credits.

- 6 to 8 shots for a 12 to 20 second piece.
- Each shot says: what is on screen, what moves, **how this shot becomes the next one**, and what you hear.
- Use `templates/storyboard.html` (fill in a `board.js` next to it) and render it to one image with `scripts/render_page.mjs`.
- Read `references/storyboard.md` for the fields and for what to ask the person.

Show the board. Wait for "approved" or for changes. Only skip the wait if the person has clearly said to run straight through.

### 3. Build

Choose the level from what the job needs. Read that level's guide before you start.

| Level | Use it when | Made with | Guide |
|---|---|---|---|
| 1. Code only | Flat or simple 3D subjects: screens, apps, logos, devices with simple shapes, charts, type | A time-driven web page rendered to video. No generators, nothing paid | `references/level-1-code.md` |
| 2. Real footage | There is real footage to cut down and dress | A cut list, code-built graphics over the footage, AI voice and music | `references/level-2-footage.md` |
| 3. Photoreal product | Metal, glass, skin, liquid, fabric: anything code makes look like plastic | Keyframe stills, then video shots from one keyframe to the next, joined | `references/level-3-product.md` |

If the subject needs real light on real materials, do not try it in code. Say so and go to Level 3.

Build a quick draft first, review it frame by frame, fix what is wrong, and only then make the full-size version and show it.

### 4. Sound

Only after the picture is approved. Sound follows the picture's beats by name, so a re-timed picture re-times its sound.

- Level 1: make the sounds with code (`scripts/make_sounds.py`). The person can also drop their own music or effects into `sound/`.
- Levels 2 and 3: generate music at the exact length, and only the few effects the picture earns.
- Mix from one cue sheet (`scripts/mix_sound.py`), then master (`scripts/master_audio.py`).
- Read `references/sound-design.md` first. The short version: music leads, never repeat one whoosh on every move, and use the real rate for anything mechanical.

## The rules

These came out of building three finished ads. Apply them without being asked, and say which one you are applying when you push back on a request.

1. **Real assets.** Quality in is quality out. Real logo files, real photos, real screens, used pixel for pixel. No invented logos, products or text.
2. **Storyboard first.** Numbered, approved before any build.
3. **Transform, never dissolve.** Each shot physically becomes the next. For every join ask: *what could this shape become?* A logo opens into a window onto the footage. The ink of one screen travels to form the next. One camera keeps moving through the join. No cross-dissolves, no fades between separate shots.
4. **Dead centre.** The subject stays on the centre of the frame and everything changes around that one point, so the eye never hunts.
5. **Always moving.** Something moves in every frame, even on a hold: a slow orbit, a drifting background, a light sweep. Fast first, then a long settle. Never a dead stop.
6. **Sound by design.** A sound only where something visibly moves. Sounds sit exactly on the picture's beats.
7. **One folder, sorted.** Everything the job needs lives in the project folder, organised, so any step can be redone.
8. **Text slides up.** Each word slides up into place inside a mask, one after the other, blurred to sharp. No bounce, no scale pops, no letters fading in one by one. Few words at a time.
9. **Copy a style, not a video.** To follow a reference, take it apart first (`scripts/study_video.py`), write its style down in words, and apply that to the new subject. Never reuse its footage, logo, music or wording.
10. **Write the prompt before the picture.** For generated stills and video, write a long, exact prompt from the references first, show it, and let the person edit it. That prompt is the point of reference for every later shot.
11. **Blend the person in.** To hand an ad off to a real person on camera, end the ad on a frame they can match, then join the ad's last frame to their first frame.

Plus three that keep the work honest:

- **One light, shallow focus.** One key light, the background out of focus, the subject sharp at every angle.
- **Label spec work.** If it uses a brand you do not own, it is a spec ad: say so on screen or in the notes, and never present it as official. See `references/honesty.md`.
- **Say what you could not check.** You cannot hear and cannot watch playback. Report what you measured, and ask the person to watch it once with sound.

## Quality checks before you show anything

Read `references/checks.md` for the full list. The ones that catch the most:

- **Frame review.** `scripts/frame_sheet.py` puts frames on one image. Read it. Then look at single frames at full size for sharpness, small text and shimmer: a sheet hides small faults.
- **Zoom into the delivered file, not the preview.** Faults invisible at 1080p show at 4K.
- **Hidden cuts and joins.** `scripts/find_jumps.py --joins` on every generated clip.
- **Against the real thing.** Put the result next to the real product photo: proportions, logo position, every character of text.
- **Sound on picture.** The mixer prints how far each cue landed from its beat. It should be 0 ms.
- **Loudness.** About -14 LUFS integrated and at most -1 dB true peak for YouTube. The last half second quiet.

## Higgsfield (Levels 2 and 3)

Read `references/higgsfield.md` before the first paid job. In short:

- **Connect it.** In Claude: add the Higgsfield connector (on higgsfield.ai open MCP, then "Add Higgsfield to Claude"). In a terminal: the `higgsfield` CLI after `higgsfield auth login`. Use whichever is present.
- **What worked for us.** Keyframes: `nano_banana_pro`. Shots that must join: `kling4_0` with a first frame and a last frame. Music: `elevenlabs_music_v2_5`. Effects: `mirelo_text_to_audio`. Voice: `elevenlabs_v4`. Models change: check what is available, and test the hero shot on two or three before committing.
- **Money.** Agree a credit budget first. Quote every job before running it, log it (`scripts/credit_log.py`), and stop and ask before going over. Check the account's charges after the first job on any model you have not used: one quote was four times too low.

## Following a reference, meta-prompting, blending someone in

Read `references/style-and-meta-prompting.md`. It covers the reverse-engineer pass, how to turn it into the prompt that drives the whole job, and how to join an ad to a person's camera shot.

## What is in this skill

| Path | What it is for |
|---|---|
| `references/level-1-code.md` | Code-only ads: the page contract, transforms, the notes that fixed real problems |
| `references/level-2-footage.md` | Cutting footage, graphics over it, voice, music |
| `references/level-3-product.md` | Keyframes, first/last-frame shots, joins, upscaling, what failed and why |
| `references/storyboard.md` | The storyboard fields and the approval gate |
| `references/prompt-templates.md` | Prompt blocks for stills, video, music, effects and voice, ready to fill in |
| `references/sound-design.md` | How to build the sound and the mistakes to avoid |
| `references/higgsfield.md` | Setup, models, commands, credit logging |
| `references/style-and-meta-prompting.md` | Reverse-engineering a video, meta-prompting, blending yourself in |
| `references/checks.md` | The full review list |
| `references/honesty.md` | Spec-ad labels, real assets, people and likeness |
| `templates/storyboard.html` | The storyboard page |
| `templates/ad-page.html` | A starter page for code-built motion |
| `scripts/` | Tools. Each one explains itself with `--help` |
| `examples/` | A real storyboard and review sheet from one of our builds |

### Scripts

| Script | Does |
|---|---|
| `render_page.mjs` | Renders a time-driven web page to video, stills or a transparent overlay. Needs Node 22+, Chrome, ffmpeg. No packages |
| `frame_sheet.py` | Frames of a video, or a folder of stills, on one labelled sheet |
| `find_jumps.py` | Finds hidden cuts in generated clips and checks that clips meet at their joins |
| `join_shots.py` | Joins first/last-frame shots into one continuous move, re-timed so the camera never stops at a join |
| `cut_footage.py` | Cuts footage to a cut list: speed, crop, freeze, slow motion |
| `ink_morph.py` | Pairs the pixels of two flat images so one can re-form into the other |
| `make_sounds.py` | Makes a free sound kit with code |
| `tick_bed.py` | Builds a steady mechanical bed at an exact rate from recorded beats |
| `split_takes.py` | Splits one voiceover take into its lines |
| `mix_sound.py` | Mixes music, voice and effects from one cue sheet, on the picture's beats |
| `master_audio.py` | Masters to a loudness target and measures the result |
| `study_video.py` | Takes a reference video apart: cuts, shot lengths, motion, colour, loudness, tempo |
| `credit_log.py` | Logs paid jobs against a budget |
| `hf_submit.sh` | Submits a Higgsfield CLI job with a quote, a stall retry and a download |

Paths such as `scripts/...`, `templates/...` and `references/...` are inside this skill's folder, not the project. Run a script by its full path there, and write its output into the project.

The Python scripts need Python 3.9+ with `numpy` and `Pillow` (`ink_morph.py` also needs `scipy`), and `ffmpeg` on the path. If they are missing, make a virtual environment inside the project and install them there. Ask before installing anything system-wide.

## Reporting back

When you hand over, give: the file path, its size, length and frame rate, what each step cost in time and credits, what you checked and how, and what you could not check. List known flaws with their timecodes. Keep the rejected takes; do not delete anything.

## On this machine (local adoption notes)

Upstream: `github.com/Samin12/claude-ads-skill` (MIT, licence kept). Installed 2026-11-26 from the pack zip; the body above is upstream, unchanged.

- **Chrome.** No system Chrome on WSL. Set `CHROME=$HOME/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome` before `render_page.mjs`. Chromium crashes inside the Claude Code Bash sandbox, so run renders unsandboxed.
- **Speed.** Software rendering: about 0.56 s a frame at 1080p (6 s took 101 s). Draft at 1080p, and render 4K or heavy three.js on the Windows GPU (see the animate GPU notes) or with `--gpu`.
- **Python.** Use `~/.venvs/motion-ads/bin/python` for every script (numpy, Pillow, scipy). Node 24 and ffmpeg are on PATH.
- **Higgsfield.** The claude.ai Higgsfield connector (`mcp__claude_ai_Higgsfield__*`) is already connected; there is no `higgsfield` CLI, so `hf_submit.sh` does not apply. Still quote every job (`estimate_*_cost`) and log it with `credit_log.py`.
- **Neighbours.** `hyperframes` is the house video engine (captions, Kokoro voice, registry blocks); `animate` makes stylised canvas explainers; `motion-graphics-prompt` writes prompts for claude.ai chat. Use this skill for ads and promos, and its rules (transform not dissolve, slide-up text, sound on beats) in the others.
- **Prompt library.** The pack's numbered prompts (0, 1.1–1.6, 2.1–2.6, Tips 9–10, 3.1–3.12, credit budget) are in `~/content-ideas/vendor/motion-ads-prompts/` (gitignored: the prompts have no licence). `README.md` there maps each prompt to its step. Give them when the person asks for a prompt to paste; the rules above already apply them.
- **Learned on the DG32 build (2026-11-26).** In 9:16, set the vertical fov from the 16:9 one (`2·atan(tan15°·H/W)`) so subjects keep their size, then push full-panel shots further out. Keep coplanar faces ≥0.015 apart and the near plane ≥0.3, or long shots z-fight. Swap a shrinking textured card to a flat body only at dot size, or it flashes as a coloured rectangle.
