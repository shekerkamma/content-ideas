# Worked example: Claude Code Code Mode A/B (2026-11-24)

The run that produced this skill. The post below passed `check_post.py`; the carousel is
`code-mode-carousel.html` in this folder (the filled editorial template). The user rejected
earlier versions of both, so every failure is recorded here.

## Result table

| Arm | Conversation tokens (`/context` Messages) | Time | Correct |
|---|---|---|---|
| Normal | 34.4k | 38 s | 5/5 |
| Code Mode | 18k | 67 s | 5/5 |

Setup: 24 Markdown notes, 5 planted broken links, Opus 5.5, same prompt, one run each.

## Draft

I turned on Claude Code's new Code Mode and ran the same job twice.

It used 48% fewer tokens. It also took 1.8 times as long.

The job was to find 5 broken links I had planted across 24 Markdown notes. Same model, same prompt.

The only change was Code Mode. Claude writes a small script that makes its tool calls, instead of reading every result back into the conversation.

Normal session: 34.4k tokens, 38 seconds.
Code Mode: 18k tokens, 67 seconds.
Both found all 5 links.

The bigger savings you've seen quoted (99%, 73%, 37%) come from Cloudflare, Datadog and a different Anthropic API feature. None of them measured Claude Code.

Speed isn't the only cost. A Code Mode session loses Remote Control, Claude in Chrome, computer use and the desktop app, and it only resumes with Code Mode on.

So I don't run it by default. I start it per job, for long searches across many files, where my usage limit matters more than the wait. The one-line launcher is on the last slide.

One run on one task proves very little. Test it on your own work before you change your setup.

#ClaudeCode #AIEngineering #DeveloperTools

## Rejected versions

- **Carousel v1:** near-black + terracotta + monospace cards. "The pdf file looks horrible."
  Also printed via `page.pdf()`, so the text became Type 3 glyphs.
- **Carousel v2:** bone canvas, light grey type, orange pixel-square unit charts. "Looks like the pdf
  generated does not look professional at all." Replaced by the editorial report the user picked
  from three mockups (`code-mode-carousel.html` here).
- **Post v1–v3:** outline of "2. Setup → …", arrows, a pasted bash function, an 👉 emoji and a
  "Tried Code Mode yet?" closer. "Does not look good at all."
