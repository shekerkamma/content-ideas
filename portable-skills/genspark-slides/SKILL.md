---
name: genspark-slides
description: Orchestrate Genspark AI Slides generation, authenticated recovery, and the compound handoff into `genspark-branded-deck` or a native PPTX builder. Use for Genspark AI slide creation, Genspark project/viewer URLs, `/api/files/s/...` HTML recovery, Genspark exports, Genspark-to-branded-deck requests, or Genspark decks that must become branded, editable, executive, pitch-ready, or client-ready PowerPoint.
---

# Genspark Slides

Use Genspark AI Slides as the fast preview generator, treat the generated viewer as
the source of truth for recovery, then continue into the requested delivery builder.
Do not stop at a hosted project or flattened export when the user asks for branding,
editability, or client-ready PowerPoint.

## Canonical Contract

Read and follow the installed sibling contract at
`../pptx-visual-spec/references/genspark-video-deck-contract.md` (repo source:
`skills/pptx-visual-spec/references/genspark-video-deck-contract.md`). It is the
source of truth for evidence inputs, rich prompt context, slide-count policy,
same-project expansion, headed Playwright recovery, credit classification,
editability labels, handoff schema, QA status, and host adapters. Validate the
handoff with `pptx-visual-spec/scripts/validate_genspark_handoff.py`.

> **On WSL:** read `references/wsl-execution-blockers.md` before launching a
> browser. Re-test the current boundary; do not reuse a historical conclusion.
> Prefer the Genspark connector for generation. Use a Windows-authenticated browser
> lane for gated viewer recovery, and WSL Chromium only for public viewers/local
> rendering.

## Compound Delivery Contract

Treat `genspark-slides` and `genspark-branded-deck` as sequential stages:

```text
validated story/brief
→ Genspark AI Slides connector (optional ideation/generation)
→ genspark-slides recovery and reference QA
→ genspark-branded-deck owned HTML/CSS branded rebuild
→ branded-pptx-deck or vault-presales-pptx-pipeline when fully native/client-ready
→ OfficeCLI QA and reviewed delivery
```

Use these routes:

| User outcome | Required route |
|---|---|
| Genspark preview/project only | Generate and retain project URL; recover only when requested |
| Fast visual PPTX | Recover and package image slides; label `draft` or `reviewed-image` |
| Branded or reskinned deck | Always hand off to `genspark-branded-deck` |
| Hybrid-editable PowerPoint | `genspark-branded-deck` hybrid path |
| Fully native/client-ready PowerPoint | Use recovered content and branded references, then rebuild through `branded-pptx-deck` or `vault-presales-pptx-pipeline` |

When the selected builder is `vault-presales-pptx-pipeline`, use the reusable
mapping contract at
`../../../genspark-branded-deck/references/genspark-to-vault-native.md`. The
Genspark deck remains the Rule-0 storyline and design reference; Vault owns the
grid, native object model, design-system conformance, and final QA.

Write `<run>/genspark-handoff.json` before the branded stage using the canonical
`pptx-visual-spec/references/genspark-handoff-template.json`. It includes:

- `project_url` and `viewer_url` when available
- source slide count and requested slide count
- recovered HTML and render directories
- validated content/story source paths
- brand source or token path
- requested editability: `image`, `hybrid`, or `native`
- blocked/omitted pages and the reason
- final builder and QA status

If hosted generation fails because of access, credits, authentication, or bot
protection, record the failure and continue directly to `genspark-branded-deck`.
Hosted failure is not a delivery stop when validated source content exists.
Use `blocked_credit_limit` only when the UI/API explicitly reports credit or
quota exhaustion. Slow generation, remaining task batches, a generic quota asset,
or anonymous-viewer console noise is not credit evidence.

Use `references/prompt-routing.md` as the trigger and acceptance matrix for
generation, recovery, branding, contextualization, editability, and fallback
requests.

## Preview-First Chain

When the user wants a new deck, preview, or first-pass slide concept:

1. If the source is a YouTube/video URL and the user wants visual grounding, run `watch-video` first to create a timestamped report and extracted frames.
2. Ensure the Genspark AI Slides app tool is available.
   - If `mcp__codex_apps__genspark_ai_slides._create_slide` is already exposed, use it.
   - If it is not exposed, use `tool_search` for `Genspark AI Slides create presentation slides`.
   - Only ask the user to enable/install a connector if tool discovery cannot expose Genspark AI Slides.
3. Call `_create_slide` with clear requirements: topic, audience, evidence-driven
   count policy, structure, tone, visual direction, and the complete upstream
   context packet—not merely summarized `watch-video` findings.
4. Wait for or open the returned project/view URL.
5. Use this skill to recover the generated slide HTML from the Genspark viewer.
6. Confirm evidence coverage before treating slide count as complete.
   - For video sources, require a scene-complete hyperframe manifest, timestamped
     transcript evidence, and a slide-to-evidence coverage matrix in the prompt.
   - Never impose a maximum slide count merely for neatness. Treat a requested
     count as a minimum or planning estimate unless the user explicitly states a
     hard maximum.
   - If any meaningful story beat or distinct screen state is omitted or
     overcrowded, update the same project with an explicit expansion request.
     Continue expanding until coverage is complete; count alone is not a pass.
7. Render the HTML to PNG references and package a fast visual PPTX if requested.
8. Write `genspark-handoff.json` and continue into `genspark-branded-deck` for
   branding. Route fully native/client-ready output onward to `branded-pptx-deck`
   or `vault-presales-pptx-pipeline`.

When the user already provides a Genspark URL, skip generation and start with HTML recovery.

## Rich Context Gate For Video Sources

Do not send Genspark a short outline derived from a video. Before `_create_slide`,
write `<run>/genspark-context-packet.md` containing:

- audience decision, BLUF, tension, and argument arc;
- transcript section summaries with timestamps and claim status;
- the scene-complete hyperframe count and maximum time gap;
- every meaningful screen group, representative frame, observed UI state, and
  disposition;
- a slide-to-evidence coverage matrix with action title, content, visual state,
  caveat, and speaker implication;
- sensitive values and unsupported claims that must be excluded;
- design tokens and the downstream editability route.

Paste the substantive packet into the connector `requirements`; a local file
path alone is not context for the remote generator. If the connector accepts
only text, encode the visual observations in text and keep frames for downstream
recovery/native rebuilding. Hyperframes are still essential: they determine
what screens exist, what the prompt must describe, and what the final deck must
prove.

The context packet is a blocking gate. `genspark-brief.md` may summarize it for
humans but must never replace it in the connector call.

## Core Workflow

1. Open the Genspark agent or viewer URL with the authenticated Windows browser
   lane. Use local WSL Chromium only for a public viewer.
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

In Codex Desktop, use the exposed Genspark connector for generation. For local
capture, run Node with the workspace Playwright dependency or the bundled Node
runtime supplied by the host.

Use **headed Chromium first** for connector-generated project recovery. A
successful connector call runs on a remote service and does not prove that the
local WSL resolver can open the returned project URL. If headed Chromium reports
`ERR_NAME_NOT_RESOLVED` while public DNS-over-HTTPS resolves the hostname, rerun
the same headed capture with `--doh-template`; do not declare the hosted deck
blocked from a shell `curl` failure alone.

```bash
node scripts/capture_genspark_slides.mjs --url "<genspark-url>" --out "<workspace>/genspark-source" --headed
node scripts/render_package_genspark_slides.mjs --html-dir "<workspace>/genspark-source/html" --out-pptx "<output>.pptx" --title "Deck Title"
```

WSL resolver recovery, after a headed run reproduces `ERR_NAME_NOT_RESOLVED`:

```bash
node scripts/capture_genspark_slides.mjs \
  --url "<genspark-url>" \
  --out "<workspace>/genspark-source" \
  --headed \
  --doh-template "https://dns.google/dns-query{?dns}"
```

If that Chromium build still reports `ERR_NAME_NOT_RESOLVED`, take a current IP
from the successful DNS-over-HTTPS answer and scope the mapping to this browser
process (never copy a stale IP from documentation):

```bash
node scripts/capture_genspark_slides.mjs \
  --url "<genspark-url>" \
  --out "<workspace>/genspark-source" \
  --headed \
  --host-resolver-rules "MAP www.genspark.ai <current-ip>, EXCLUDE localhost"
```

Use `--min-slides <n>` when the user requested a minimum count; treat a failure as a retry/quality signal, not a fatal pipeline collapse.

If a public viewer is accessible and Playwright cannot launch its bundled browser,
pass a local Chrome path:

```bash
node scripts/capture_genspark_slides.mjs --url "<genspark-url>" --out "<workspace>/genspark-source" --chrome "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" --headed
```

If the viewer redirects to Google/Genspark sign-in, do not attempt Google login in
an automated WSL browser. Use the Windows-authenticated Chrome DevTools/extension
lane. A dedicated persistent capture profile is acceptable only when the browser
and its encrypted cookie store remain on the same OS:

```bash
node scripts/capture_genspark_slides.mjs \
  --url "<genspark-viewer-url>" \
  --out "<workspace>/genspark-source" \
  --chrome "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
  --headed \
  --user-data-dir "C:/Users/<windows-user>/.codex/genspark-browser-profile" \
  --auth-wait-ms 300000
```

After that succeeds, reuse the same `--user-data-dir` without needing another sign-in. This is the preferred recovery path for gated or unstable Genspark viewer access.

If Chromium fails with a sandbox-host/`Operation not permitted` error or the host
blocks GUI launch, rerun the same command through the host's approved headed or
unsandboxed execution path. Do not convert that browser-runtime failure into a
Genspark, DNS, or credit diagnosis.

## Brand-Ready Upgrade

Do not stop at image packaging when the user asks for an editable, executive, branded, client-ready, or pitch-ready deck.

Inside Sheker's vault, use the compound chain before final PPTX build:

```text
watch-video (for YouTube/video sources)
→
Genspark AI Slides app (`_create_slide`)
→ genspark-slides
→ genspark-branded-deck
→ vault-presales-pptx-pipeline
→ OfficeCLI QA
```

If a Genspark deck already exists, start at `genspark-slides`:

```text
genspark-slides
→ genspark-branded-deck
→ vault-presales-pptx-pipeline
→ OfficeCLI QA
```

For a fully native rebuild:

1. Treat recovered HTML as the source deck.
2. Treat rendered PNGs as visual references.
3. Extract slide text and proof objects from HTML.
4. Build a claim spine and design system.
5. Rebuild slides with editable shapes, text, diagrams, and charts.
6. Preserve factual content unless the user asks for rewriting.
7. Use source visuals only as references unless the user explicitly accepts an image-based deck.

When working inside Sheker's vault, save final PPTX files in `Decks/` unless the user names another output folder.

## Quality Gates

- Confirm the slide count from the captured endpoints and validate the coverage
  matrix row by row.
- If Genspark under-generates or compresses several required states into an
  illegible summary, update the same project with an explicit expansion request.
  Do not accept a short deck merely because its endpoint count is internally
  consistent.
- Inspect a contact sheet before delivery.
- State whether the PPTX is image-based or fully editable.
- If the viewer is gated and the Windows-authenticated lane is unavailable, ask
  the user to open/share the deck or provide exported HTML/PPTX.
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
