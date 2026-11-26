# Motion ads: a Claude skill for motion graphics and product ads

A skill that teaches Claude to make motion graphics and product ads in three levels, from a finished ad built with nothing but code to photoreal product footage joined into one continuous camera move.

It is the written-down version of what was learned building three finished ads for the tutorial "Claude Just Changed Motion Graphics Forever!": the steps, the rules, the prompts, the scripts, and the mistakes.

![A numbered storyboard for a 16-second code-only ad](examples/storyboard-eink-display.jpg)

*The storyboard for the Level 1 example, made with this skill's template. Spec ad for the TRMNL e-ink display, made for a tutorial. Not affiliated with TRMNL.*

## What it does

Every job follows four steps:

1. **Assets.** The logo file, product photos and screenshots, in one sorted folder.
2. **Storyboard.** A numbered board, approved before anything is built.
3. **Build.** Code, footage, or generated shots, depending on the level.
4. **Sound.** Music, voice and effects placed on the picture's own beats.

Claude does the work and stops for a decision at the storyboard. It reviews its own frames, measures its own sound, and tells you what it could not check.

## The three levels

| Level | What it makes | What it needs |
|---|---|---|
| **1. Code only** | Motion graphics and ads for screens, apps, logos and simple devices, as a web page rendered to 4K video, with sound made by code | Claude Code, Node 22+, Chrome, ffmpeg, Python. No paid tools |
| **2. Real footage** | Raw footage cut down to a tight promo, with code-built graphics over it, an AI voiceover and AI music | The above, plus a Higgsfield account (our example used 15 credits) |
| **3. Photoreal product** | Photoreal product footage from keyframe stills and first-frame/last-frame video shots, joined into one camera move | The above, plus more credits (our example used about 790, with about 330 in the final cut) |

## Install

### Claude Code

```bash
git clone https://github.com/Samin12/claude-ads-skill ~/.claude/skills/motion-ads
```

Start a new session. The skill is named `motion-ads` and loads by itself when you ask for an ad or a motion graphic. To use it in one project only, clone it into that project's `.claude/skills/motion-ads` instead.

The scripts use `ffmpeg`, Python 3.9+ with `numpy` and `Pillow` (one script also uses `scipy`), and Node 22+ with Chrome for rendering. Claude will set up what is missing inside your project and ask before installing anything else.

### claude.ai and the Claude desktop app

1. Download `motion-ads.zip` from the [latest release](https://github.com/Samin12/claude-ads-skill/releases/latest).
2. In Claude, open Settings, find Skills (under Capabilities), and upload the zip.

In claude.ai the skill gives Claude the method, the rules and the prompt templates. The scripts that render and mix video need a computer with ffmpeg and Chrome, so run those levels in Claude Code or the desktop app's Code tab.

## How to use it

Make a folder, put your logo, product photos and screenshots in it, open Claude Code in that folder, and paste:

```text
Use the motion-ads skill. I want a 15-second ad for the product in this folder.
Start with Level 1 (code only). Sort my assets, tell me if anything is missing or too low-resolution,
then give me a numbered storyboard and stop so I can approve it.
```

Approve the storyboard or ask for changes, and Claude builds it, reviews it, and adds sound. For Levels 2 and 3, connect Higgsfield first (on higgsfield.ai: MCP, then "Add Higgsfield to Claude") and tell Claude your credit budget.

To follow the style of a video you like, put the file in the folder and say "reverse-engineer this video's style and write me the prompt for my product". Claude takes the reference apart, writes the prompt, and shows it to you before using it.

## The rules it works to

1. Use the actual logo, photos and screens. Quality in is quality out.
2. Storyboard first, approved before any build.
3. Each shot physically becomes the next one. Cross-dissolves are banned.
4. The subject stays dead centre.
5. Something is always moving.
6. Sound only where something moves, exactly on the beat.
7. One folder, sorted.
8. Text slides up inside a mask. No bounce.
9. Copy a style, never a video.
10. Write the prompt before the picture (meta-prompting).
11. Blend the person in: join the ad's last frame to their first.

## What is inside

```
SKILL.md                 the procedure Claude follows
references/              a guide per level, prompt templates, sound design, Higgsfield setup,
                         the storyboard, checks, honesty rules
templates/               the storyboard page and a starter page for code-built motion
scripts/                 14 tools: render a page to video, review sheets, join shots, cut footage,
                         make and mix sound, master, study a reference video, log credits
examples/                a storyboard and review sheet from one of our builds
```

Every script explains itself:

```bash
python3 scripts/mix_sound.py --help
node scripts/render_page.mjs --help
```

![A review sheet: one frame a second of the finished ad](examples/review-sheet-eink-display.jpg)

*A review sheet. Claude cannot watch a video play, so it reads frames like these before showing you anything.*

## Honest work

The skill labels spec ads, refuses to invent logos or product text, uses only facts that are in your footage for a voiceover, and will not generate a real person's face unless that person asked for it. It does not post or upload anything. See `references/honesty.md`.

## Credits

- Made by [Samin Yasar](https://github.com/Samin12) with Claude.
- Inspired by [Rourke's video](https://youtu.be/cDb-wPq0Iyk) on making motion graphics with Claude.
- The example images show a spec ad for the TRMNL e-ink display. TRMNL's name, logo and screens belong to TRMNL, which has no connection to this project.

## Licence

MIT, for the skill's text and code. See [LICENSE](LICENSE). Product names, logos and screens that appear in the example images belong to their owners.
