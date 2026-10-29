---
name: design-os
description: Use when someone wants to find, browse or reuse their own visual work — "find that orange logo I made", "show me every dashboard we designed", "search my generated images", "what did we render last month", "build me a design library", "design OS", "more like this". Indexes folders of finished designs (HTML), generated images and videos, embeds each one with Gemini Embedding 2 so words find pictures, and serves a local gallery with semantic search, "more like this", type filters and a copy-path button for handing an asset to Claude.
license: MIT
metadata:
  category: Design tooling
  version: '1.0'
  cost-tier: 'Haiku to run: the agent starts two commands. Embedding is Gemini Embedding 2 on the free AI Studio key (about one call per new file, cached forever by content hash).'
---

# Design OS

Everything you finish or generate lands in some folder and is never found again. This indexes those folders
once, describes nothing by hand, and lets you search by what is *in* the pictures: a burger, a dark
dashboard, an orange logo. It is the piece of RoboNuggets' "design operating system" tip that this setup
did not have; recall of text and entities stays with GBrain and `search.py`.

## Run it

```bash
S=<this skill's directory>/scripts
python3 $S/design_os.py index ~/Pictures/generated runs/ deepgrid-v2/public --limit 200
python3 $S/design_os.py serve            # http://127.0.0.1:8793
python3 $S/design_os.py search "orange logo on white" --top 10
```

- **What it indexes:** images (png, jpg, webp, gif), videos (mp4, webm, mov; a poster frame via ffmpeg) and
  HTML designs (title and visible text; add `--screenshots` for a rendered thumbnail through Playwright).
  `node_modules`, `.git` and dot-folders are skipped.
- **Incremental:** re-running skips unchanged files (path, size, mtime) and never re-embeds known content
  (content hash). Files deleted from an indexed folder drop out of the index.
- **Free-tier friendly:** `--limit` caps new embeddings per run (default 200). A quota, key or network error
  stops embedding cleanly, keeps everything done so far, and reports the rest as pending; run again later
  to continue. `--no-embed` indexes and thumbnails only; names and titles stay searchable.
- **The gallery:** search by content, filter Images / Videos / Designs, **More like this** (image to image,
  no API call), **Copy path** to paste an asset into a Claude chat, and the thumbnail opens the file.
  Results are laid out row by row in rank order at every width.
- **State:** `$DESIGN_OS_HOME`, default `~/.local/share/design-os` (`%LOCALAPPDATA%\design-os` on Windows):
  `index.json`, `vectors.bin` (float32, 3072 per item) and `thumbs/`.

## Measured

On the 217 scene frames of the RoboNuggets video (files named `frame_0001.jpg`…, so names could not help):
all 217 embedded in 4 min 11 s with no quota error; a second run embedded 0.
Blind queries against scenes whose content was known from the contact sheets:

| Query | Expected | Top result |
|---|---|---|
| perfume bottle on a dark product page | 11:57 | 11:57 |
| world map with photos of people | 00:28–00:30 | 00:31, 00:29, 00:29 |
| orange and yellow abstract shapes | 13:20 | 13:21 ×3 |
| a burger on a plate | 12:52–12:56 | **rank 11** |
| a grid of burger photos in an image gallery app | 12:52–12:56 | **ranks 2 and 3** |

The burger rows are the usage rule below, measured.

## Judgment rules

- **Describe the whole picture, not only the object in it.** Each file is embedded as one image. A small
  subject inside a busy frame ranks low for its own name (rank 11 above) and high for a description of the
  whole screen (rank 2). Search the way you would caption the image.
- **Index what you made, not the internet.** Point it at your outputs (renders, runs, generated-image
  folders, finished sites); a downloaded stock library drowns your own work.
- **Mind the free tier.** Keep `--limit` at the level your key allows per day and let repeated runs finish
  the backlog; never raise it to force a large folder through in one go.
- **Copy the path, not the file.** The gallery hands Claude a path to read; it never uploads assets anywhere.

## Gotchas

- `serve` reads `gallery.html` at start-up: restart it after editing the page.
- Without Pillow, images larger than 4 MB get no thumbnail (small originals serve as their own); install
  Pillow in the Python you run it with for thumbnails of everything.
- Semantic search needs `GOOGLE_GENERATIVE_AI_API_KEY` (or `GEMINI_API_KEY`) for the query too; without it
  the search box falls back to names and titles, and says nothing about it beyond fewer results.
- Embedding uses `scripts/gemini_embed.py` in this repo; run the skill from a content-ideas checkout, or put
  that folder on `PYTHONPATH`.

## Skill Relationships

| Skill | Pattern | Handoff |
|---|---|---|
| `gemini-embed` | Dependency | `embed(text=…, image_path=…)` |
| `ai-graphics`, `hyperframes`, `watch` | Upstream | their output folders are what you index |
| `refero-design` | Complement | external references; Design OS is your own work |
| GBrain, `search.py` | Peer | text, entity and conversation recall; Design OS is visual |

## Host Compatibility

Stdlib Python (Pillow optional), ffmpeg for video posters, Node + Playwright only for `--screenshots`.
Works in Claude Code, Codex, DeepSeek Harness and OpenHands; on Windows run `python`. Canonical at
`skills/design-os/`, byte-identical mirror at `.agents/skills/design-os/`. Tests (`tests/test_design_os.py`)
use a deterministic fake embedder, so they check indexing, caching, quota handling, ranking and file serving
without an API key; visual similarity itself was measured with the live model as above.
