# Canonical PPTX Visual-Sourcing Rules

This is the single visual-routing specification for PowerPoint-producing skills. It is
derived from the `vault-presales-pptx-pipeline` gate, with ambiguity removed around exact
screen evidence, structured data, authored graphics, and host-native image generation.

Apply it to each **visual region**. A slide may combine multiple routes: for example, a
generated text-free photograph, native headline and KPIs, and an extracted source figure.

## Decision Order

```text
1. Is exact appearance/state itself evidence or an explicit fidelity requirement?
   YES -> EXTRACT exact supplied/source pixels. Never redraw.
   NO  -> continue.

2. Is there an approved real asset whose identity matters?
   YES -> PLACE ASSET unchanged or perform an explicitly authorized edit.
   NO  -> continue.

3. Does the region communicate data, a claim, text, comparison, architecture,
   process, timeline, or other structured meaning?
   YES -> NATIVE when PowerPoint editability is feasible.
          Otherwise AUTHOR deterministically by type and place the render.
   NO  -> continue.

4. Is a new organic/editorial/ambient visual materially useful?
   YES -> IMAGE MODEL, text-free and non-evidentiary.
   NO  -> NONE. Do not decorate by default.
```

## Routes

| Route | Use when | Required output |
|---|---|---|
| `extract` | Exact UI state, screenshot, source figure, or supplied artwork must survive faithfully | High-DPI crop/asset plus source locator |
| `place-asset` | Approved logo, photograph, product asset, brand artwork, or supplied media is already available | Original asset plus provenance/rights record |
| `native` | Data, claims, text, charts, tables, KPIs, comparisons, architecture, flows, timelines, and editable diagrams | PowerPoint-native objects |
| `author-html` | New boxes-and-labels, grids, swimlanes, cards, or layout-driven diagrams need a reusable raster asset | `.html` plus rendered `.png` |
| `author-svg` | New parameterized geometry, circuits, radial/isometric figures, or coordinate-driven artwork | `.svg` or generator plus rendered `.png` |
| `author-react` | Existing/reusable component-driven visual needs static placement | `.jsx/.tsx` or static HTML plus rendered `.png` |
| `image-model` | New text-free organic scene, editorial illustration, texture, or visual metaphor | Prompt plus generated `.png` |
| `none` | A visual adds no explanatory value | Explicit reason; no decorative filler |

`author-*` assets are deterministic authored graphics, not image-model generations.

## Exact Extraction

Use `extract` before reconstruction when exact appearance is the point: application UI,
terminal output, code editor state, whiteboard/figure supplied as a reference, or a specific
screen in a video. This route may contain text because the text is part of authentic source
evidence; the ban on model-rendered text does not apply to real extracted pixels.

1. Render PDF/deck sources at 200-220 DPI or use the highest-resolution supplied asset.
2. Crop the intended region and auto-trim against a corner-sampled background.
3. Pad in the sampled background color; record dimensions, page/frame/time, and crop bounds.
4. Place without distortion using `contain` or a planned `cover` crop.
5. Match the slide/surface background so the asset does not look pasted on.
6. Keep slide title, caption, citation, callouts, and footer native and editable.
7. Do not redraw an exact reference into HTML/SVG merely to claim editability.

When a supplied chart/table is only a source for its data and exact artwork is not required,
route the information to `native` instead. The deciding question is whether pixels/state or
the underlying information is the required evidence.

## Native Versus Authored Structured Graphics

Use `native` when the final PowerPoint must support normal editing and the visual can be
expressed clearly with slide primitives. This is the default for claims and structured
business content.

Use an `author-*` route when the deliverable explicitly needs a reusable image asset, when
the geometry exceeds PowerPoint primitives, or when a reference-less visual must be rendered
consistently across surfaces. Select by structure:

- HTML/CSS: layout, cards, labels, grids, swimlanes, comparisons.
- SVG: true geometry, coordinate math, circuits, isometric/radial figures.
- React: existing component systems or stateful widgets rendered to a static state.

Render through `~/.claude/skills/ai-graphics/scripts/html_to_png.mjs`. Ship the editable
source beside the PNG. Every glyph remains code-rendered and deterministic.

## Image-Model Route

Image generation is narrow and automatic only when a text-free organic visual adds material
value, typically a cover, section image, conceptual scene, or editorial illustration.

### Execution precedence

Read `skills/image-generation-router/SKILL.md` before executing `image-model` records.

1. Respect an explicit provider request. OpenAI/imagegen selects the built-in route;
   Gemini/Nano Banana/CLIProxyAPI selects the local Gemini adapter. Never substitute a
   Flash image model when the user requested Nano Banana Pro.
2. Without an explicit provider, use the built-in `image_gen` route first. In Codex it uses
   the signed-in ChatGPT/Codex subscription and is independent of provider-adapter quotas.
   In Claude Code, use the installed Codex bridge only when intentionally routing through
   that subscription: `generate_with_codex_cli.py` -> `codex exec` -> built-in `image_gen`.
3. If the built-in route is unavailable, disclose the failure and probe CLIProxyAPI. Use
   Gemini only when authenticated `GET /v1/models` reports the requested/selected image
   model; never rely on a stale model table.
4. Use OmniRoute/provider adapters only when the user explicitly requests that separate
   route or model control. Its status never blocks built-in OpenAI or CLIProxyAPI Gemini.

### Non-negotiable constraints

- Text-free by construction. Any accidental glyph, logo, watermark, or signature is a defect.
- Never generated as proof, a real product/facility/person, a certification, a logo, or a
  source for technical/quantitative claims.
- Do not send slide copy, labels, or numbers to the image model.
- Keep all claims and typography in native objects or deterministic authored code.
- Record the prompt, execution path, authentication mode, orchestration model, requested
  engine, and resolved engine. `resolved_engine` is `null` when the tool does not expose it.
- Inspect the actual image and the placed slide crop. Tool reachability alone is not QA.

## Precedence and Exceptions

1. User-supplied exact evidence and approved assets outrank generated alternatives.
2. Deck-specific rules may require more native editability, but cannot authorize redrawing
   exact evidence, model-rendered text, fabricated proof, or missing provenance.
3. Image-per-slide skills may flatten the final layout only when that output mode is explicit.
   Their source visuals still follow this routing contract, and image models still cannot
   render slide text or claims.
4. A reference deck supplies the storyline and design evidence; it does not require every
   page to become a screenshot. Apply the exact-state versus underlying-information test.

## Required Visual Specification

Every meaningful visual region records:

- stable ID, slide IDs, purpose, artifact type, evidence status, route, and reason;
- source locator or approved asset provenance when applicable;
- asset and editable-source paths;
- prompt and execution metadata for generated imagery;
- placement slot, fit, crop/background decisions;
- QA results for visual inspection, legibility, crop, background, text safety,
  evidence separation, and provenance.

Validate against `visual-spec-schema.json` before build and before `reviewed` promotion.

## Reviewed Gate

- Every meaningful visual has a route or explicit `none` reason.
- Exact references were extracted, not approximated.
- Data/claims remain native or deterministic, never image-model output.
- Generated images are text-free and non-evidentiary.
- Graphic and surface backgrounds match.
- All placed images were inspected in a real Office render.
- OfficeCLI issues = 0 for reviewed PPTX output.
- No full-slide flattening unless the chosen skill explicitly declares that output mode.
