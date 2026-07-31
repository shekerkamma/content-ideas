# Verbatim recovery — turning a live Genspark deck into local slide files

**Load this when:** the user supplies a Genspark deck URL and wants that deck as
a PPTX ("convert", "make it editable", "faithful"), rather than a new deck built
from its content.

## Why verbatim is the default

Re-authoring a deck the user already approved destroys content and layout they
chose. A 37-slide source rebuilt as your own 43-slide arc is a different
document, however good it looks. Reproduce first; improve only when asked.

## Do not scrape the agent page

The `genspark.ai/agents?id=…` page body contains the **generation prompt and the
agent's task log** — not the slides. Extracting it yields a plausible-looking
brief that is not the deck. The viewer also virtualises: only ~10 slide iframes
are mounted at any time, so harvesting `iframe.contentDocument` returns a partial
deck. Use the data API.

## Recovery procedure

Run through Windows Chrome (`mcp__chrome-devtools-windows__*`) — Genspark needs
the authenticated session, which WSL Chromium does not have.

1. **Find the endpoint.** `list_network_requests` with
   `resourceTypes: ["fetch","xhr","document"]` →
   `GET /api/project/slide_data?project_id=<id>&is_edit_mode=false&deck=<deck>`

2. **Inspect the shape before pulling it.** Return a probe (key names, array
   lengths, string *lengths*) rather than the payload — a 37-slide deck is
   ~450 KB and will flood context.

   ```
   data.meta_data.canvas        -> { width: 1920, height: 1080 }
   data.meta_data.page_num      -> 37
   data.meta_data.asset_oids    -> { "chrome.css": "<sha>" }
   data.file_contents[]         -> { index, filename, content /* full slide HTML */ }
   ```

3. **Write it to disk, not through context.** `evaluate_script` accepts a
   `filePath`. Absolute paths outside the MCP's workspace roots are rejected;
   a bare filename works and lands in Windows `%TEMP%`, readable from WSL at
   `/mnt/c/Users/<user>/AppData/Local/Temp/<name>.json`.

4. **Fetch the shared stylesheet** — it is the deck's whole design system
   (palette, type roles, type scale):
   `/api/slides_git/projects/<id>/decks/<deck>/assets/chrome.css`

5. **Split to files:** `slides/NN-<filename>.html` plus `chrome.css`.

6. **Wrap, do not rewrite.** Each file contains a
   `<div class="slide-container" style="width:1920px;height:1080px;…">`. Wrap
   each in `<section class="slide">`, link `chrome.css`, add the standard
   `window.__deck` export hook and the `body.export-bg` rule. Nothing else.

## Retarget the pipeline to a 1920 stage

The bundled scripts assume a 1280×720 stage. Genspark decks are 1920×1080:

| Where | 1280 stage | 1920 stage |
|---|---|---|
| `render*.mjs` viewport | `1280×720 @ dsf 2` | `1920×1080 @ dsf 4/3` (both → 2560×1440) |
| `build_editable_pptx.py` | `IN_PER_PX = 13.333/1280` | `13.333/1920` |
| `build_editable_pptx.py` | `PT_PER_PX = 0.75` | `0.5` |

Absolute per-object positioning is an *advantage* for the hybrid export: every
text node already has an explicit, generous bbox, so PowerPoint re-wrap is rare.

## Fonts

`chrome.css` `@import`s Google Fonts. Playwright fetches them at render time, but
`build_editable_pptx.py` names fonts for the native text boxes. Install the real
families locally so renders and QA are accurate, capture a font `role`
(display / body / mono) in `render_hybrid.mjs`, and map role → family in the
builder. Ship the font files beside the deck and say plainly that a machine
without them will substitute.

## Inherited defects

A faithful reproduction reproduces the source's layout bugs. Fixed-height title
boxes are the common one: a long title wraps and prints over its subtitle. Fix
surgically and say what you changed —

- widen the title box into unused margin before touching type size;
- otherwise auto-fit *only* overflowing boxes, measured after
  `document.fonts.ready` and gated so the renderer cannot screenshot a pre-fit
  frame.

Do not re-flow the slide.
