---
name: genspark-slides
description: Generate preview slides with Genspark AI Slides, then recover, recreate, and upgrade Genspark AI slide decks from shared Genspark agent/viewer links. Use when Codex needs to call Genspark AI Slides for a first-pass preview deck, inspect a Genspark presentation URL, capture `/api/files/s/...` slide HTML endpoints, save the full slide HTML source, render 16:9 references, package a visual PPTX/PDF, or hand the recovered HTML into the Presentations skill for brand-ready, client-ready, or editable slide rebuilds.
---

# Genspark Slides

Use Genspark AI Slides as the fast preview generator, then treat the generated viewer as the source of truth for HTML recovery.

> **On WSL / Claude Code: read `references/wsl-execution-blockers.md` FIRST.**
> Generation is blocked here by Cloudflare bot-check (headless), an unauthenticated
> session (headed), and OS-bound cookie encryption (copied Windows profile) — all
> rooted in WSL interop being off (`/proc/sys/fs/binfmt_misc/WSLInterop` missing).
> Check that file before spending time on browser launches. If generation is blocked,
> the two working alternatives are: (1) have the user generate in their own Windows
> browser and hand over the project URL, or (2) skip Genspark and author `deck.html`
> directly for `genspark-branded-deck`.

## Preview-First Chain

When the user wants a new deck, preview, or first-pass slide concept:

1. If the source is a YouTube/video URL and the user wants visual grounding, run `watch-video` first to create a timestamped report and extracted frames.
2. Ensure the Genspark AI Slides app tool is available.
   - If `mcp__codex_apps__genspark_ai_slides._create_slide` is already exposed, use it.
   - If it is not exposed, use `tool_search` for `Genspark AI Slides create presentation slides`.
   - Only ask the user to enable/install a connector if tool discovery cannot expose Genspark AI Slides.
3. Call `_create_slide` with clear requirements: topic, audience, slide count, structure, tone, visual direction, and any `watch-video` findings.
4. Wait for or open the returned project/view URL.
5. Use this skill to recover the generated slide HTML from the Genspark viewer.
6. Confirm the captured slide count meets the requested count.
   - If under target, update the same Genspark project once with an explicit expansion request.
   - If it is still under target, report Genspark under-generation and continue with `presentations:Presentations` for the full deck when the user needs the requested count.
7. Render the HTML to PNG references and package a fast visual PPTX if requested.
8. For client-ready work, chain into `/ce-doc-review` and `presentations:Presentations`.

When the user already provides a Genspark URL, skip generation and start with HTML recovery.

## Core Workflow

1. Open the Genspark agent or viewer URL with Browser.
2. Click `View` if the page starts in the conversation wrapper.
3. Watch network requests for `/api/files/s/<id>?pageIndex=<n>&scale=<s>`.
4. Download each endpoint at `scale=1`; these often return full slide HTML, not images.
5. Save one `slide-XX.html` file per page.
6. Render each HTML slide at `1280x720` into PNG references.
7. Create the requested output:
   - For fast recreation: package rendered PNGs into a widescreen PPTX.
   - For editable/client-ready work: use the recovered HTML and PNG references as source input for the `presentations:Presentations` skill.

## Scripts

Use these scripts when the page is accessible from local Chrome/Playwright.

In Codex Desktop, call `load_workspace_dependencies` first and run Node with the returned bundled Node executable. Set `NODE_PATH` to include the returned bundled `node_modules` folder and its `.pnpm/node_modules` folder when package resolution needs it.

```bash
node scripts/capture_genspark_slides.mjs --url "<genspark-url>" --out "<workspace>/genspark-source" --headed
node scripts/render_package_genspark_slides.mjs --html-dir "<workspace>/genspark-source/html" --out-pptx "<output>.pptx" --title "Deck Title"
```

Use `--min-slides <n>` when the user requested a minimum count; treat a failure as a retry/quality signal, not a fatal pipeline collapse.

If Playwright cannot launch its bundled browser, pass a local Chrome path:

```bash
node scripts/capture_genspark_slides.mjs --url "<genspark-url>" --out "<workspace>/genspark-source" --chrome "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" --headed
```

If the Genspark viewer redirects to Google/Genspark sign-in, use a persistent capture profile once and have the user complete sign-in in the opened browser window:

```bash
node scripts/capture_genspark_slides.mjs \
  --url "<genspark-viewer-url>" \
  --out "<workspace>/genspark-source" \
  --chrome "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
  --headed \
  --user-data-dir "C:/Users/sheke/.codex/genspark-browser-profile" \
  --auth-wait-ms 300000
```

After that succeeds, reuse the same `--user-data-dir` without needing another sign-in. This is the preferred recovery path for gated or unstable Genspark viewer access.

## Brand-Ready Upgrade

Do not stop at image packaging when the user asks for an editable, executive, branded, client-ready, or pitch-ready deck.

Inside Sheker's vault, chain through Compound Engineering before final PPTX build:

```text
watch-video (for YouTube/video sources)
→
Genspark AI Slides app (`_create_slide`)
→ genspark-slides
→ /ce-doc-review
→ presentations:Presentations
→ vault-presales-pptx-pipeline
→ /ce-compound
```

If a Genspark deck already exists, start at `genspark-slides`:

```text
genspark-slides
→ /ce-doc-review
→ presentations:Presentations
→ vault-presales-pptx-pipeline
→ /ce-compound
```

Then use `presentations:Presentations`:

1. Treat recovered HTML as the source deck.
2. Treat rendered PNGs as visual references.
3. Extract slide text and proof objects from HTML.
4. Build a claim spine and design system.
5. Rebuild slides with editable shapes, text, diagrams, and charts.
6. Preserve factual content unless the user asks for rewriting.
7. Use source visuals only as references unless the user explicitly accepts an image-based deck.

When working inside Sheker's vault, save final PPTX files in `Decks/` unless the user names another output folder.

## Quality Gates

- Confirm the slide count from the captured endpoints.
- If Genspark under-generates, retry expansion once and then state the gap clearly.
- Inspect a contact sheet before delivery.
- State whether the PPTX is image-based or fully editable.
- If the viewer is gated, ask the user to open/share the deck or provide exported HTML/PPTX.
- Do not fabricate missing slides; record gaps by page index.

## Images And Visuals

Recovered Genspark renders remain reference assets. Any new raster region follows the shared
visual spec and executes through `ai-graphics`: deterministic HTML/SVG for structured or
text-bearing work, and built-in Codex `image_gen` only for eligible text-free organic imagery.
Provider-adapter status applies only when explicitly selected; inspect every actual render.

## Shared PPTX Visual Contract

Genspark generation and recovered HTML are upstream reference surfaces. Before packaging or
rebuilding a final PPTX, apply `pptx-visual-spec`, create and validate
`<run>/visual-spec.json`, and classify every recovered region. Exact Genspark references may
be extracted for a faithful visual draft; client-ready/native rebuilds route underlying
claims and structure through the selected direct builder. Genspark-generated imagery is not
automatically evidence and does not bypass prompt/provenance rules.
