---
name: experiment-to-linkedin
description: Use when a measured A/B test or before/after experiment (two runs, real numbers, a correctness check) should become a LinkedIn post plus a carousel PDF — "turn my test results into a LinkedIn post", "make a carousel of these A/B numbers", "post my benchmark on LinkedIn", "experiment to LinkedIn". Writes the post under anti-slop rules and renders a 6-slide 1080x1350 carousel from a bundled HTML template, reviewed page by page. Not for posts without measured results (use vault-content-ideas-pipeline), or for DeepGrid part storyboards (use storyboard-to-carousel).
argument-hint: "<results: file, folder, or pasted numbers> [--out <run-dir>]"
---

# Experiment → LinkedIn post + carousel

Turns one measured comparison into two finished pieces that say the same thing in the same order:
a LinkedIn post (paste-ready text) and a 6-slide carousel PDF to attach as a document. The carousel
uses an editorial-report design: white page, serif headlines that state each finding, real bar
charts with a source line, ruled tables.

**Cost tier:** Sonnet-class can run it end to end. Rendering is free and local (Playwright +
chromium). No image model, no paid API. Writing the post is the only judgment-heavy step.

Proven on: Claude Code Code Mode A/B, 2026-11-24 (`examples/code-mode.md`).

## Inputs

- **The result table** (required): for each arm (A = baseline, B = change) the measured numbers
  and a correctness score against a known answer. Example: tokens 34.4k vs 18k, time 38 s vs 67 s,
  5/5 vs 5/5.
- **The setup** (required): what was run, how many times, what was held constant.
- **Context claims** (optional): numbers others quote about the same thing, with their real source.
- **Run dir** (`--out`, default `$CONTENT_HOME/research/<slug>/`, `CONTENT_HOME` defaults to
  `~/Documents/Content`). Never the cwd.

If any number lacks a source (a log, a `/context` readout, a timer), stop and ask. Do not round
it into existence.

## Workflow

1. **Build the claim ledger.** Write `<run>/claims.md`: every number that will appear, its
   source, and a one-line caveat (sample size, single run, which tool measured it). Mark quoted
   third-party figures with who measured them and on what. This is the only place numbers come from.
2. **Pick the verdict.** One sentence that holds both the gain and the cost, e.g. "half the
   tokens, almost twice the time". It becomes slide 1 and the post's first line.
3. **Write the post** → `<run>/linkedin-post-draft.md`. Load `anti-slop` first, then follow
   [references/post-rules.md](references/post-rules.md). File shape: `## Hook Options` (3),
   `## Draft` (paste-ready), `## Source Notes`, `## Repurpose`.
4. **Check the post:**
   `python3 scripts/check_post.py <run>/linkedin-post-draft.md` and fix every FAIL.
5. **Fill the carousel.** Copy `assets/template.html` to `<run>/carousel/carousel.html` and
   replace every `[[placeholder]]`, including the chart numbers (`--max`, `--v`, tick labels). Slide plan and design rules:
   [references/carousel-design.md](references/carousel-design.md). Keep the slide order identical
   to the post.
6. **Render at 2x:**
   `node scripts/render.mjs <run>/carousel/carousel.html <run>/carousel`
   → `slide-01.png` … (2160x2700).
7. **Look at every slide** at full size (Read each PNG). Fix wrapped bar values, misaligned bars, bar
   lengths that don't match the numbers, one-word last lines; re-render. No cap on these passes, they're free.
8. **Build the PDF from the reviewed PNGs:**
   `node scripts/build_pdf.mjs <run>/carousel` → `carousel.pdf`.
9. **Look at the PDF pages** (`pdftoppm -r 30 -png` → contact sheet → Read). The PDF must match
   the PNGs page for page.
10. **Deliver.** Open the post and the PDF for the user (`code <path>`; on WSL also
    `explorer.exe "$(wslpath -w <path>)"`). State status `reviewed` only if steps 4, 7 and 9 ran.

## Outputs

```
<run>/
  claims.md                   # number → source → caveat
  linkedin-post-draft.md      # Hook Options / Draft / Source Notes / Repurpose
  carousel/
    carousel.html             # editable source
    slide-01.png … slide-06.png   # 2160x2700
    carousel.pdf              # image-only, 1080x1350 pages
```

## Judgment rules

Editable policy. Tune here, not in the steps.

- **Six slides** by default: hook, setup, metric A, metric B, the catch, your setup/verdict.
  Drop to five if there is only one metric; never pad to six.
- **One idea per slide.** Each headline states the finding; one `<em>` span carries the accent.
- **Bar charts** for every metric: grey baseline, red change, axis from 0 to a round `--max` just
  above the largest value, and a source line naming where the number was read.
- **Post length** 100–200 words; hook must land in the first 210 characters.
- **Single runs are reported as single runs**, in the post and on a slide footer. Never imply a
  benchmark.
- **Third-party numbers** appear only with who measured them, and only to say they aren't yours.
- **No code in the post body.** Code goes on a carousel slide.
- **Text contrast:** body `#3A3A3A` and labels `#6B6B6B` on white (both above 4.5:1).

## Gotchas

- **Don't restyle on your own.** Two designs were rejected: near-black + terracotta + monospace
  cards ("looks horrible"), then a bone canvas with orange pixel-square charts ("does not look
  professional at all"). The user picked the editorial report from three mockups. If a restyle is
  ever needed, show 2–3 mockups and let the user choose; don't guess a fourth time.
- **Never `page.pdf()` the HTML.** Text becomes Type 3 glyphs that look bad in Windows viewers.
  The PDF is built from the reviewed PNGs only.
- **Pillow's PDF writer fails here** (no JPEG encoder). Use `build_pdf.mjs`.
- **Freehand posts get rejected.** An outline of "2. Setup → …", arrows, a pasted bash function,
  an emoji pointer, and a "Tried it yet?" closer all read as slide notes or AI.
- **1,300 characters is not the "see more" line.** LinkedIn cuts at ~210 characters / 2–3 lines.
- **`brand_context/voice-profile.md` is a stock template** (web-scraping persona). Use its
  LinkedIn format rules, not its catchphrases. Ask for the user's real voice if voice matters.
- **`text-wrap: balance`** is on headlines and the callout to stop one-word last lines. Check it
  still holds after copy edits.
- **Bar rows:** `.lab`, `.bar` use `flex-shrink:0` and `.val` uses `nowrap`. Without them a long bar
  squeezes its label and the value wraps ("67 / s"), which happened in the first editorial render.
- **Playwright lookup:** scripts resolve `playwright` from `$PLAYWRIGHT_ROOT`, then the cwd, then
  the repo root. Set `PLAYWRIGHT_ROOT=~/content-ideas` if it says "Cannot find module".

## Skill Relationships

### Category
Business Automation

### Dependencies
- `anti-slop` — writing filter for the post (step 3).
- Playwright with a chromium build, already in the content-ideas repo `node_modules`.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `watch` | Sequential upstream | when the experiment was prompted by a video claim | `<run>/report.md` |
| `watch-video` | Sequential upstream | same, via the wrapper that writes `report.md` into the run dir | `<run>/report.md` |
| `anti-slop` | Behavioral overlay | always, step 3 | — |
| `ai-graphics` | Alternative / Peer | a one-off graphic, or design mockups if a restyle is asked for | design spec + HTML |
| `vault-content-ideas-pipeline` | Alternative / Peer | post with no measured experiment; vault note shape | `Content/LinkedIn/*.md` |
| `storyboard-to-carousel` | Alternative / Peer | DeepGrid part storyboards in the DeepGrid design system | — |
| `review-draft` | Amplifier | optional voice check if a real brand voice exists | draft md |

### Runtime Preamble
"I'll turn your measured results into a LinkedIn post and a 6-slide carousel. I need each
number's source first. No source, no number. If you have no measured result yet, use
`vault-content-ideas-pipeline` instead."

## Host Compatibility

### Target Hosts
- Claude Code: yes, via the content-ideas plugin (`skills/experiment-to-linkedin/`).
- Codex/OpenAI: yes, via `.codex-plugin/plugin.json` (`"skills": "./skills/"`).
- OpenHands: yes if `skills/` is mounted; scripts need node + playwright.

### Canonical Source
`skills/experiment-to-linkedin/` in the content-ideas repo.

### Tool Mapping
- Claude `Read` of PNGs (visual review) → any host's image-view tool; if none, report the
  carousel as unreviewed and do not call it `reviewed`.
- Claude `AskUserQuestion` → a plain chat question.
- `code` / `explorer.exe` open steps are WSL conveniences; on other hosts print the absolute paths.

### Source / Tool Order
1. This SKILL.md, the references, and the user's result files.
2. The run's own logs for every number (claims ledger).
3. Official docs only to verify context claims quoted in the post.
