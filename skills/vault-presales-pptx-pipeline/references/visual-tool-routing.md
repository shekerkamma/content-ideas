# Visual Tool Routing

Select tools from the artifact requirement. Do not route every visual task to Figma or any other single vendor.

## Evidence-First Order

1. Supplied client assets, screenshots, product photographs, templates, and brand kits.
2. Approved assets retrieved from connected repositories such as Google Drive, Google Slides, SharePoint, Box, or Figma.
3. Native editable Presentations objects for charts, tables, diagrams, timelines, and architecture.
4. Purpose-built design tools for UI concepts, wireframes, product design, design systems, or web companions.
5. AI-generated raster imagery when authentic evidence is unavailable and the visual is illustrative.
6. Licensed public imagery found through web image search, with source and usage rights recorded.

## Requirement-to-Tool Map

| Requirement | Preferred tools | Use when | PPTX handling |
|---|---|---|---|
| Final client-ready PowerPoint | Codex Presentations / artifact-tool | The deliverable is a `.pptx` | Build titles, text, shapes, diagrams, tables, and charts as editable slide objects. |
| Website or published interactive companion | Framer | The work is primarily a website, CMS experience, or publishable interactive page | Export approved screenshots or diagrams only when they support the deck; keep the web artifact separate. |
| High-craft interface or multidisciplinary design | Figma | A craft designer needs precise layout, components, motion, shaders, or a familiar collaborative canvas | Retrieve approved frames/assets through the connector when available; rebuild slide structure natively. |
| Agent-native product design | Paper or MagicPath | Codex, Claude Code, or Cursor should design alongside the user on a shared canvas | Use for product flows and UI concepts; export selected evidence, not flattened slide layouts. |
| Accessible design generation for non-designers | Google Stitch or Claude Design | Rapid high-quality concepts are needed without deep design-tool expertise | Use outputs as concepts or evidence; validate brand fit and rebuild editable slide content. |
| Design-system source of truth | Google Stitch | The task requires reusable design tokens or a `design.md`-style specification | Translate validated tokens into the deck design specification and presentation theme. |
| Budget-conscious visual design | Open Design or MagicPath | Cost and bring-your-own-agent support are key constraints | Confirm export quality and rights before using outputs in a client deck. |
| Rapid wireframes and user journeys | UX Pilot | A PRD must become wireframes, screens, or an end-to-end journey quickly | Use wireframes as product evidence; annotate the journey with native slide objects. |
| Branded presentation concepts | Canva | A branded Canva presentation or fast visual exploration is explicitly wanted | Treat Canva as an optional creation surface; export or rebuild according to editability requirements. |
| AI slide preview or inspiration | Genspark Slides | Fast preview slides are needed before a higher-quality rebuild | Recover the visual reference, critique it, then rebuild the client-ready deck with Presentations. |
| New illustrative raster image | OpenAI image generation | A cover, visual metaphor, neutral industry scene, or conceptual illustration is needed | Record the prompt and label the asset as generated; avoid using it as business evidence. |
| Edit a supplied raster image | OpenAI image editing | Remove, extend, restyle, or adapt an image with user authorization | Preserve the original and record the edit request. |
| Public image discovery | Web image search | No approved asset exists and a real-world image is necessary | Open the source page, verify licensing and provenance, and record the URL. |
| Approved repository retrieval | Google Drive/Slides, SharePoint, Box, Figma | Client-approved logos, templates, product imagery, or screenshots already exist | Use the connected source instead of searching or generating replacements. |

## Current Capability Check

Read `design-tools-runtime.yaml` before promising or invoking a design tool. Its status values are the production gate.

- **Ready for write work:** Codex Presentations, Google Slides, Canva, MagicPath, **HTML/SVG → screenshot**, Google Drive, and web image search.
- **HTML/SVG → screenshot is the default raster route**, not a fallback. Any visual carrying
  text belongs here: it is free, deterministic, re-renders without limit, and ships an
  editable `.html` beside the `.png`. Run it via the `ai-graphics` skill
  (`scripts/html_to_png.mjs`). Reach for an image model only for organic or illustrative
  regions that contain no glyphs.
- **Codex built-in image generation is ready and separate from provider adapters.** In Codex
  hosts, use built-in `image_gen` through the signed-in ChatGPT/Codex subscription for eligible
  text-free organic imagery. OmniRoute route health applies only when that adapter is explicitly
  selected. Only a real render proves the selected execution path.
  - **From Claude Code / WSL, drive it through the `codex` CLI bridge** (verified 2026-07-18,
    `codex-cli 0.144.4`; this is the OpenAI route when OmniRoute's `:20128` images route is
    down, which it was):
    ```bash
    codex exec --dangerously-bypass-approvals-and-sandbox \
    "Use your built-in image generation tool to create ONE 16:9 image and save it to the EXACT
    path /abs/out.png. CRITICAL: absolutely NO text/letters/numbers. Concept: <text-free scene>.
    Save one PNG to /abs/out.png and confirm it exists."
    ```
    Codex writes to `~/.codex/generated_images/<id>/*.png` then copies to your path. No API key
    (uses the subscription). **Timeouts:** ~60–120 s per image; generate **one image per
    `codex exec`** (batching 4 in a session overran) and give the shell ≥ 300 s — the default
    2-min cap kills it mid-render. On-palette prompt that worked: *"premium tech-keynote 3D
    render, deep navy #0A1628, glowing cyan #00B4D8 + teal #0A9396, no text."*
- **Figma is limited:** authentication works, but the verified Vokal organization seat is `View`. Use it for accessible references and inspection only until an edit-capable seat is verified.
- **MagicPath is ready:** CLI 2.6.0 is authenticated and can access the user's projects through the bundled `pnpm dlx` fallback.
- **Genspark Slides is available but not write-tested:** use it only after an explicit preview request and successful connector response.
- **Browser-only and not configured for production writes:** Framer, Paper, Google Stitch, Claude Design, Open Design, and UX Pilot.

Use only a `ready` tool for production writes. Re-run the relevant identity, permission, or CLI check before upgrading any other status.

Do not claim that a named tool was used unless its connector, browser session, CLI, or API actually ran. If the strongest tool is unavailable, use the nearest ready option or ask for access only when the difference materially affects the result.

## PPTX Routing Rules

### Use native slide objects for

- architecture and data flows;
- process diagrams and roadmaps;
- charts, tables, KPI tiles, and comparisons;
- titles, body text, callouts, captions, and citations;
- reusable slide components and layout structure.

### Use image assets for

- real product, facility, prototype, and workflow photographs;
- application screenshots and source documents;
- approved client artwork;
- generated cover or conceptual illustrations;
- visual evidence that would lose meaning if redrawn.

### Do not use generated images as

- proof of client results;
- a substitute for missing product evidence;
- a representation of real employees or facilities;
- a technical architecture or quantitative chart;
- a source for logos, certifications, or regulatory claims;
- a reliable way to render substantial text.

## Selection Procedure

For every visual requirement, record:

1. Artifact type: photograph, UI, wireframe, diagram, chart, design system, web page, or slide.
2. Evidence status: authentic, approved, illustrative, generated, or public-source.
3. Editability requirement: native object, editable source file, or acceptable raster evidence.
4. Delivery surface: PPTX, web, collaborative canvas, or image asset.
5. Access path: installed connector, browser, CLI, API, local file, or unavailable.
6. Rights and provenance: owner, URL, license, prompt, or supplied-file path.
7. Selected tool and fallback.

## Practical Defaults

- A client supplies screenshots and a logo: retrieve and use those assets; do not regenerate them.
- A slide needs a system architecture: build it natively in Presentations.
- A deck needs a product UI concept: use MagicPath, Paper, Figma, Stitch, or UX Pilot according to access and fidelity needs, then place selected screens as evidence.
- A deck needs a cinematic cover with no authentic image: use image generation and record the prompt.
- A request is actually a publishable website: route the primary artifact to Framer and produce a separate PPTX only if needed.
- A request needs fast slide inspiration: use Genspark or Canva, then apply the editable-output rule.

## Source

- User-supplied selection summary derived from [Design tools reference video](https://www.youtube.com/watch?v=6OpWU-HrsuQ), especially 08:05 and 19:40–21:16.
- Verified on 2026-07-16 with the native Windows `/watch` skill using YouTube captions filtered to 07:30–21:30.
- Reviewed pinned frames at 08:05, 19:40, 20:01, 20:26, 20:33, 20:47, 20:51, and 21:16. Working evidence is stored in `Decks/_work/design-tool-routing-video-native/`.
