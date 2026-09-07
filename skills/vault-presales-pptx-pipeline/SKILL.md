---
name: vault-presales-pptx-pipeline
description: Use when the deliverable is a CLIENT-READY PowerPoint deck — pre-sales decks, use-case realization decks, implementation or solution-architecture slides, solution-on-a-page, executive one-pagers, Genspark-sourced deck upgrades, rebuilding a supplied reference deck properly, fixing structural issues as part of a material client-ready redesign, or POC Factory assets. Triggers on "/vault-presales-pptx-pipeline", "client-ready deck", "custom pptx", "client-ready pptx", "pre-sales deck", "use-case realization deck", "solution-on-a-page", "rebuild this deck", "upgrade this deck", "update this deck", "modify this deck", "contextualize this deck", "customize this deck", "adapt this deck", "refresh this deck", "improve this deck", "enhance this deck", "rebrand this deck", "make this deck client-ready", "fix this deck and make it client-ready", or "deck from this reference". Treat broad update, modification, contextualization, adaptation, improvement, or branding requests as FULL NATIVE
  REBUILDS, not in-place edits. St
metadata:
  legacy-frontmatter:
    trigger: /vault-presales-pptx-pipeline
    argument-hint: '[what deck — e.g. ''rebuild the DeepGrid IM client-ready'', ''use-case realization deck from UC-08'', ''solution-on-a-page for <account>'']'
    category: Business Automation
---

# Vault Pre-Sales PPTX Pipeline

Build deck-ready source packets from the wiki, then produce a client-ready PPTX with **artifact-tool presentation JSX** (see `## PowerPoint Rule`). If the source is YouTube/video, run `watch-video` first to create frame-aware notes. If the user wants Genspark to create preview slides, call the Genspark AI Slides app next, then run `genspark-slides` to capture the generated HTML and visual references. If the app tool is not exposed, use `tool_search` for `Genspark AI Slides create presentation slides` before asking the user to enable a connector. If the source is already a Genspark agent/viewer link or recovered Genspark slide HTML, start at `genspark-slides`.

## Runtime Preamble

At invocation, surface this to the user:

> "Running `/vault-presales-pptx-pipeline` — the **client-ready** path: native editable
> PowerPoint objects, zero flattened slides, on the Client-Ready PPTX Design System.
>
> 1. **Did you provide a reference deck?** If so it *is* the storyline — I'll extract and
>    first inventory and structurally validate it, then follow its arc rather than invent
>    one (Rule 0). The source file remains unchanged. An update, modification, contextualization,
>    adaptation, or improvement request means a new native rebuild—not an in-place patch.
> 2. **Is the content ready?** If not, chain upstream first: `/content-research`,
>    `/ai-strategy-brief`, `/ai-analyst`, `/aianalyst-competitor-analysis`.
> 3. **Deck type?** use-case-realization · implementation-plan · solution-architecture ·
>    solution-on-a-page · presales-pipeline · poc-factory-offer · genspark-upgrade.
>
> Alternatives: `/branded-pptx-deck` (branded template, outside this design system) ·
> `/genspark-branded-deck` (fast visual, flattened — not client-ready) · `/marp` (markdown)."

**Then, before writing anything:** read `references/storyboard-method.md`, then
`references/artifact-tool-presentation-jsx.md`, and start from `assets/deck-kit.mjs`.

## Rebuild-by-Default Rule

When a user supplies an existing deck and broadly asks to **update, modify, contextualize,
customize, adapt, refresh, improve, enhance, rebrand, upgrade, or fix the deck**, rebuild it
as a new native presentation. Do not preserve or reuse the source slide coordinates, text-box
geometry, broken layouts, or visual defects. Treat the source as storyline, content, evidence,
and approved assets only; reflow every slide through the design-system grid.

Use `pptx-toolkit` alone only when the user explicitly constrains the request to named surgical
operations—such as correcting a specific typo, updating a specified note, or moving/removing
specified slides—and explicitly wants the existing layout preserved. If a request mixes a
surgical edit with contextualization, branding, visual improvement, narrative change, or
client-ready output, the full rebuild wins. Do not ask the user to choose when these broad
rebuild verbs are present.

## Pipe

0. **If the user supplied a reference PPTX, preserve it and run structural intake FIRST.**
   Use `pptx-toolkit inspect` to save `<run>/source-inventory.json`, then
   `pptx-toolkit validate` to confirm package relationships and slide structure. Record
   duplicated or suspicious slides, shape/text inventory, notes/comments presence, and
   unsupported complex parts. Never overwrite the incoming file.
0.1. **Extract the supplied deck's storyline and follow it.** It is the storyboard — do not
   invent an arc. Structural defects in the source are evidence to repair, not reasons to
   discard the intended narrative. See `references/storyboard-method.md` (Rule 0).
1. Start from one or more wiki notes: use cases, architecture, projects, research, tasks.
2. If the source is YouTube/video, run `watch-video` and preserve the report plus frame folder.
3. If the user wants Genspark preview slides, call the Genspark AI Slides app `_create_slide`, then run `genspark-slides` against the generated viewer.
4. If the source is an existing Genspark deck, run `genspark-slides` and preserve the recovered HTML plus PNG references.
5. Generate a deck packet with `scripts/generate_deck_packet.py` when starting from vault notes, or create an equivalent packet from recovered watch/Genspark sources.
6. Review the packet for story, proof objects, brand fit, and missing inputs.
6.4. **Visual sourcing gate — runs first, per visual region.** Apply the shared
   `pptx-visual-spec` contract, mirrored locally in
   `references/visual-sourcing-rules.md`. Exact-state evidence routes to EXTRACT before
   ordinary data/claims route to NATIVE; new deterministic graphics route to AUTHOR by type;
   only text-free organic imagery may route to an image model. Write and validate
   `<run>/visual-spec.json` against `references/visual-spec-schema.json`.
6.5. **Auto visual pass — MANDATORY, runs every build, never waits to be asked.** Classify
   each slide's visual need from its content and act. **The user does not request images; the
   build decides.** See `## Auto Visual Pass` below. Layout of native objects is derived from
   the grid in `references/layout-spec.md` / `assets/deck-grid.mjs`, never hand-typed pixels.
7. Build the editable PPTX from the reviewed packet with **artifact-tool presentation JSX** — see `## PowerPoint Rule` and read `references/artifact-tool-presentation-jsx.md` first.
7.5. **Run the structural output gate.** Run `pptx-toolkit validate` on the exported draft.
   This catches broken package relationships and slide-structure defects; it does not replace
   rendering QA.
7.6. **Run the visual output gate.** Run OfficeCLI with `--required`, review its issue report,
   render every slide, inspect a contact sheet, and scan for internal-only language. Keep the
   filename at `*-draft.pptx` until both structural and visual gates pass; then promote a copy
   to `*-reviewed.pptx`. Use `blocked` when a required gate cannot run.
8. Store reviewed PPTX files in `Decks/outputs/`.
8.5. **Resolve delivery and open requests to the reviewed artifact.** If the user says
   "open it," "show me the deck," or "open the folder" after a build, select the newest
   `*-reviewed.pptx` for the active run, verify that the delivered copy matches it, and open
   that file or its containing folder. Never present the source deck or a draft as the rebuilt
   result.
9. Link the reviewed deck from source project/use-case notes, `Pre-Sales/`, daily note, and relevant MOCs.

## Delivery and Open Contract

- Treat the supplied PPTX as immutable source material, never as the completed deliverable.
- Treat `*-draft.pptx` as an internal review artifact. Open it only when the user explicitly
  asks to inspect the draft, and label it as unreviewed.
- Treat `*-reviewed.pptx` as the default target for "open it," "show me," "deliver it," and
  "open the Windows folder."
- Before opening a delivered copy, verify that it exists and matches the reviewed run artifact
  by hash or byte-for-byte comparison.
- If no reviewed artifact exists yet, say so plainly. Do not open the original deck in a way
  that implies the rebuild is complete.
- When a Windows destination is requested, copy only the reviewed artifact, verify the copy,
  then open Explorer with that file selected.

## Existing-PPTX Structural Routing

`vault-presales-pptx-pipeline` owns the orchestration. Broad deck-change requests rebuild by
default; route out only when the user explicitly constrains the task to surgical operations:

| Finding / requested change | Route | Required finish |
|---|---|---|
| Explicitly named typo/text correction, note update, slide reorder/removal, or safe OOXML inspection **with the existing layout preserved** | `pptx-toolkit` only | toolkit validation + OfficeCLI render QA |
| Broken package relationships or unreadable PPTX | `pptx-toolkit` diagnosis; repair only supported operations, otherwise mark `blocked` | reopen/validate + OfficeCLI |
| Update, modify, contextualize, customize, adapt, refresh, improve, enhance, rebrand, upgrade, or broadly fix an existing deck | **this pipeline**; rebuild every slide with artifact-tool JSX | toolkit validation + visual-spec + OfficeCLI |
| Branding, narrative, layout, architecture, charts, visual assets, or client-ready quality changes | **this pipeline**; use source inventory and Rule 0, rebuild with artifact-tool JSX | toolkit validation + visual-spec + OfficeCLI |
| Existing branded-template deck outside the Client-Ready PPTX Design System | `branded-pptx-deck`, with `pptx-toolkit` at intake/output boundaries | branded workflow QA |

Structural validation proves that the PPTX package is coherent. It does **not** prove that
text fits, contrast is readable, shapes do not collide, or the deck looks client-ready; those
remain render-review responsibilities.

## Related deck skills — when to route out

| Skill | Use it when | Output |
|---|---|---|
| **this pipeline** | The deliverable is **client-ready** and governed by `Client-Ready PPTX Design System` | **100% native objects, zero flattened slides** (artifact-tool JSX) |
| `pptx-toolkit` | Existing-file inventory or an explicitly named surgical operation that preserves the current layout | structurally validated native `.pptx` draft |
| `genspark-branded-deck` | Fast, pixel-perfect **visual** deck; gradients/glass/custom diagrams that native shapes can't easily do; credit-free | Image-per-slide, or hybrid (text boxes over a **flattened** design background) — **not client-ready under the design system** |
| `genspark-slides` | You want Genspark's **AI** to draft the content, then recover its HTML | Generated slides → HTML recovery → rebuild here |
| `branded-pptx-deck` | Native shapes/charts on the **branded template**, outside this design system | python-pptx native |

**The dividing line is the design system's editability rule** — *"Do not flatten full
slides into images for the client-ready output."* `genspark-branded-deck`'s hybrid
flattens layouts (only the text is live), so it cannot satisfy that rule no matter how
good it looks. Use it for speed and visual fidelity; use this pipeline for the
client-ready deliverable.

Chain: `genspark-slides` (AI drafts) → recover HTML → **this pipeline** (rebuild native, client-ready).

## Deck Types

- `use-case-realization`: problem -> target state -> AI workflow -> implementation roadmap -> metrics.
- `implementation-plan`: phases, workstreams, integrations, data, risks, timeline.
- `solution-architecture`: system map, data flow, integration points, deployment model.
- `solution-on-a-page`: one-slide executive summary with business outcome, architecture, metrics, and pilot.
- `presales-pipeline`: account/use-case pipeline, stage, next action, blockers, assets needed.
- `poc-factory-offer`: repeatable POC asset, buyer value, demo scope, build plan, proof.
- `genspark-upgrade`: generate Genspark preview slides when needed -> recover Genspark slide HTML -> critique story and design -> rebuild as editable, branded, client-ready PPTX.

## Required Source Grounding

Every deck packet must include:
- source notes,
- target audience,
- business problem,
- solution claim,
- proof objects,
- implementation path,
- metrics,
- risks,
- missing inputs,
- backlinks.

## PowerPoint Rule

For actual PPTX generation, use artifact-tool presentation JSX. Do not generate final PPTX with Python or direct OOXML edits.

**→ Read `references/artifact-tool-presentation-jsx.md` before building.** It carries the
import block, the API surface, the style grammar, the 190 geometry names, the export/QA
calls, and the traps. Without it you will lose an hour rediscovering them.

**From WSL / Claude Code:** the library lives in the Codex runtime cache and ships a
**Windows-native** `skia-canvas`, so a direct import fails with
`skia.node: invalid ELF header`. Use the one-time Linux port at
`~/.local/artifact-tool-linux` (build steps in the reference). Once ported, the whole
pipeline runs on WSL node — no Windows interop, no Codex CLI needed.

Fast visual copies from `genspark-slides` may be image-based PPTX files. Label them clearly as image-based. Client-ready outputs must be rebuilt with editable slide objects through artifact-tool presentation JSX.

### Images are allowed. Flattened slides are not.

**"Zero flattened slides" is not "zero images."** The design system bans replacing a slide's
*structure* with a picture. It does not ban a picture placed **inside** an otherwise native
slide. A cover image, a product photograph, a screenshot, or a conceptual illustration sitting
in a frame while the title, body, callouts, and citations remain live text is fully compliant.
The reference builders show `0 pictures` because those decks had no photographic requirement —
that is a property of the content, **not a target to hit**.

The line to hold:

| Belongs to native objects — always | May be an image asset |
|---|---|
| Titles, body, callouts, captions, citations | Real product/facility/prototype photographs |
| Architecture, data flows, process diagrams | Application screenshots, source documents |
| Charts, tables, KPI tiles, comparisons, timelines | Approved client artwork and brand assets |
| Claims/data authored for the deck; exact-state source evidence is the sourcing-gate exception | Covers, visual metaphors, conceptual illustration |

**Never send text to an image model.** Any glyph routes to HTML/SVG → screenshot. Generated
assets must be text-free by construction — image models produce typos that are plausible at a
glance and survive review.

**Route via `ai-graphics`** (`~/.claude/skills/ai-graphics/`), which owns raster execution.
HTML/SVG screenshot is deterministic and remains the default for text-bearing assets. For an
eligible text-free organic region, Codex hosts use built-in `image_gen` through the signed-in
ChatGPT/Codex subscription; Claude Code may use the authenticated Codex bridge. OmniRoute is
an explicit provider adapter only and its quota does not govern built-in image generation.
Only a successful real render proves availability.

Generated imagery is **never** client proof, never a stand-in for missing product evidence,
never a real person or facility, and never a source for logos or certifications. Record the
prompt and label the asset as generated. Full policy: `references/visual-tool-routing.md`.

## Auto Visual Pass

**This is automatic. The user never asks for images — the build classifies every slide and
acts.** Run this as pipe step 6.5, once per slide, before building that slide. It is not a
separate deliverable and it is not optional polish; it is part of what "build the deck" means.

For each slide, read its content and assign exactly one visual verdict:

| Slide content | Verdict | Action — automatic |
|---|---|---|
| Numbers, comparison, KPI, table, ranking | **NATIVE** | Build with `deck-kit.mjs` shapes/charts. **No image** — native is the contract. |
| Architecture, data flow, process, timeline, system map | **NATIVE** | Build with kit rails/chains/shape-charts. **No image** — a redrawn diagram is native, not a picture. |
| Real product, facility, prototype, screenshot, or an approved client/brand asset is *named in the packet* | **PLACE ASSET** | Retrieve and place it. If it is named but not supplied, add to `missing inputs` — **never fabricate it**. |
| Section divider, cover, chapter, or a conceptual/ambient slide with **no data and little text** that would read as bare | **GENERATE** | Auto-produce a **text-free** organic image (metaphor/texture/scene) and place it behind live text. This is the only verdict that calls an image model. |
| Dense text/bullets, exec summary, decision, next steps | **NONE** | No visual. Do not decorate a content slide with a stock image. |

**The GENERATE path, executed automatically:**

1. Write a **text-free** image spec from the slide's theme (the deck's palette, no glyphs — any
   letter is a defect). Never send the slide's title or copy to the model.
2. In Codex hosts, call built-in `image_gen`; in Claude Code, use the installed authenticated
   Codex bridge when that subscription route is intended. Place the PNG in a declared fixed
   slot and keep title/subtitle as **live text boxes on top**.
3. If the actual render fails, do not block the deck: use a native typographic treatment or
   deterministic SVG motif and retain the prompt/spec for a later rerender. Provider-adapter
   status is consulted only when the user explicitly selected that adapter.

**Why the default is NATIVE, not "generate an image."** In this pipeline a screenshot or a
generated picture becomes a **flattened region**; native objects are the editability contract.
So automatic image generation fires narrowly — covers and ambient/section slides — precisely
where native has nothing to express and a text-free image adds real value. Everything with a
number, a claim, or a diagram is auto-built native. This is why the reference decks show `0
pictures`: their content was all data, so the auto pass correctly generated nothing. A deck with
a cover or a section metaphor would legitimately carry a few.

**Never** let the auto pass invent evidence, a real person/facility, a logo, or a chart. Those
verdicts are PLACE ASSET (retrieve) or NATIVE (build) — never GENERATE.

**Do not substitute `pptxkit` / python-pptx for a final client deck.** It is the correct
builder for `branded-pptx-deck`, but it is not this pipeline's method. The rule exists to
guarantee the `Client-Ready PPTX Design System` editability contract: native objects, and
**no flattened slides**.

### Reference builders

| Deck | Builder | Result |
|---|---|---|
| Design-system test (7 slides) | `Decks/_work/design-system-test/build_test_deck.mjs` | 246 editable objects; validated 2026-07-16 |
| Deepgrid competitor/diligence (20 slides) | `runs/2026-07-16-deepgrid-client-ready-pptx/build_deck.mjs` (content-ideas repo) | 690 shapes · 442 text boxes · **0 pictures** · OfficeCLI passed / 0 issues |
| Context Layer concept-explainer (**50 slides, with images**) | `runs/2026-07-18-context-layer-client-ready-pptx/build_deck_v2.mjs` (content-ideas repo) | native shapes/text + **14 images placed** (7 extracted blog figures + 7 text-free OpenAI dividers) · `C.image({dataUrl})` per §5c of the build reference · OfficeCLI passed / 0 issues — the reference for **images inside native slides** |

## References

- **`references/storyboard-method.md`: WHERE THE STORYLINE COMES FROM** — Rule 0 (a supplied
  reference deck *is* the storyboard), how to extract it, the reusable IM arc, arc-integrity
  checks, the `genspark-upgrade` correction pattern, and slide-language rules. **Read this
  before writing a single title.**
- **`assets/deck-kit.mjs`: THE BUILD KIT** — import-and-go helpers (content-fitting cards,
  proportion bars, shape-charts, timeline rails, process chains) with every gotcha solved.
  Start here; write only slide content.
- **`references/artifact-tool-presentation-jsx.md`: THE BUILD METHOD** — import block (incl. the
  WSL Linux port), API surface, `textStyle`/`stroke` grammar, all 190 geometry names,
  export + QA calls, mandatory gate table, and the traps. **Read this before building.**
- `references/deck-types.md`: slide patterns by deck type.
- `references/presales-story.md`: story spine and proof object rules.
- `references/visual-tool-routing.md`: which design tool for which artifact.
- **`references/visual-sourcing-rules.md`: WHERE EACH GRAPHIC COMES FROM** — the per-slide
  NATIVE / EXTRACT / AUTHOR gate. If a reference image exists, recreate it EXACTLY (extract +
  place, never reconstruct); if not, AUTHOR by type (HTML/CSS boxes · SVG geometry · React
  components). Codifying artwork that already exists is banned — it drifts from the original.
- **`references/layout-spec.md` + `assets/deck-grid.mjs`: LAYOUT AS SPECIFICATION** — the
  12-column grid + named bands + templates. Native placement is DERIVED (`cx/span/cols/rows`),
  never hand-typed. Also carries the graphic/slide background-match rule.
- `assets/*.md`: packet templates.
- Design system: `Knowledge/Presentation Design/Client-Ready PPTX Design System.md` — canvas,
  type, colour, L01–L16 layouts, density budget, quality gate.

---

## Skill Relationships

### Category
Business Automation

### Dependencies
Required for this skill to work:
- **`@oai/artifact-tool`** — the mandated builder. On WSL, requires the one-time Linux port
  at `~/.local/artifact-tool-linux` (`references/artifact-tool-presentation-jsx.md` §1).
  Without it every build fails with `skia.node: invalid ELF header`.
- **`assets/deck-kit.mjs`** — the helper library (content-fitting cards, proportion bars,
  shape-charts, rails, chains). Start here; do not rewrite it.
- **`Client-Ready PPTX Design System`** — `Knowledge/Presentation Design/`. The visual contract.
- **`scripts/generate_deck_packet.py`** — packet generator. Defaults `--vault .`; pass
  `--vault /mnt/c/Users/sheke/Documents/hyundai-ai-vault` when running from another project.
- `ai-graphics` — the raster route, when a slide needs a picture. Its scripts live in **that
  skill, not this one**: `~/.claude/skills/ai-graphics/scripts/html_to_png.mjs` (default, free,
  deterministic), built-in Codex `image_gen` for eligible text-free imagery, and
  `omniroute_image.py` only for explicit provider-adapter use. Not required for a
  text-and-shapes deck; required the moment a raster asset is in scope.
- `pptx-visual-spec` — mandatory behavioral overlay; the local sourcing rules and schema are
  synchronized mirrors of its canonical contract.
- `pptx-toolkit` — mandatory structural intake/output gate for existing PPTX work. Use the
  content-ideas implementation at
  `python3 <content-ideas>/skills/pptx-toolkit/scripts/pptx_toolkit.py`. It inventories,
  performs supported surgical edits, and validates package structure; it is not the final
  client-deck builder.
- `officecli` — final QA gate. The script lives in the **content-ideas repo**, not this skill:
  `python3 <content-ideas>/scripts/officecli_qa.py <pptx> --out <run>/qa/officecli --required`.
  Mandatory before naming anything `*-reviewed.pptx`.

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `aianalyst-competitor-analysis` | Sequential upstream | competitor/diligence evidence needed | `outputs/evidence-ledger.csv`, `scoring-model.md` |
| `content-research` | Sequential upstream | URLs/repos/docs to ingest | research notes |
| `ai-analyst` | Sequential upstream | validated quant findings | analysis JSON / charts |
| `ai-strategy-brief` | Sequential upstream | 1-page exec brief as source | brief markdown |
| `story-architect` | **Amplifier — always** | any deck needs a spine before building | `outputs/story-architect-pack.md` |
| `pptx-toolkit` | Structural gate / surgical alternative | an existing PPTX is supplied or a draft was exported | `source-inventory.json`, structurally validated `.pptx` |
| `pptx-visual-spec` | Behavioral overlay | every visual and PPTX build | `<run>/visual-spec.json` |
| `ai-graphics` | Amplifier | a slide needs a raster asset — cover, illustration, or any structured visual native shapes can't carry | `.png` + reusable `.html` template |
| `watch-video` | Sequential upstream | source is YouTube/video | frame-aware report |
| `genspark-slides` | Sequential upstream | Genspark's AI should draft first | recovered slide HTML + PNG refs |
| `genspark-branded-deck` | Alternative / Peer | fast pixel-perfect visual deck; **flattens layouts — not client-ready** | image/hybrid `.pptx` |
| `branded-pptx-deck` | Alternative / Peer | branded template outside this design system | native `.pptx` (pptxkit) |
| `marp` | Alternative / Peer | markdown-source slides | `.md` → html/pptx |
| `officecli-qa` | Amplifier downstream | final render QA gate (script in the content-ideas repo) | `qa/officecli/qa-summary.md` |
| `/ce-doc-review` | Amplifier | high-stakes review before delivery | review notes |

### Full chain
existing PPTX → `pptx-toolkit` intake → `story-architect` →
**`vault-presales-pptx-pipeline`** → `pptx-toolkit` output validation →
`officecli-qa` → `Decks/outputs/`

For non-PPTX sources, begin at the relevant research/source stage instead of the toolkit.

## Host Compatibility

### Target Hosts
- **Claude Code** — yes. Globally available via `~/.claude/skills/vault-presales-pptx-pipeline`
  (symlink → the vault canonical). Fires from any project.
- **Codex / OpenAI** — yes, via `~/.codex/skills/vault-presales-pptx-pipeline` (symlink).
- **OpenHands / .agents hosts** — yes, via `~/.agents/skills/…` (symlink) or the vault's own
  `.agents/skills/vault-presales-pptx-pipeline/`.
- **Gemini CLI** — yes, via `~/.gemini/skills/…` (symlink).

### Canonical Source
`hyundai-ai-vault/.claude/skills/vault-presales-pptx-pipeline/` is the source of truth.
`.agents/skills/…` in the vault is a mirrored copy — **edit the canonical, then sync both**.
All four global host roots are symlinks to the canonical: one master, N symlinks, zero drift.

### Tool Mapping
- Claude `Read`/`Grep`/`Glob` → Codex shell reads + `rg`
- Claude `Edit`/`MultiEdit` → Codex `apply_patch`
- Claude `Bash` → Codex shell (`node build.mjs`, `python3 scripts/officecli_qa.py`)
- Claude `AskUserQuestion` → numbered choices in chat

## Gotchas

- **Rule 0 is not optional.** A supplied reference deck IS the storyline. Inventing an arc
  cost four rebuild rounds on 2026-07-16; visual/density/jargon fixes did not help because
  the defect was structural. `references/storyboard-method.md`.
- **A clean package is not a clean slide.** `pptx-toolkit validate` checks relationships and
  structure; OfficeCLI plus a real render checks overflow, collisions, clipping, contrast,
  and visual quality. Both gates are mandatory for existing-PPTX work.
- **Do not overwrite the supplied deck.** Preserve it as the immutable source; write
  `*-draft.pptx`, then create `*-reviewed.pptx` only after all gates pass.
- **"Open it" means the reviewed output.** Never open the source deck or an unreviewed draft
  as though it were the rebuilt deliverable. Verify the delivered copy before launching it.
- **Broad change verbs mean rebuild.** Update, modify, contextualize, customize, adapt,
  refresh, improve, enhance, rebrand, upgrade, or broadly fix an existing deck by rebuilding
  it natively. Never inherit a source deck's broken coordinates just because it is editable.
- **`skia.node: invalid ELF header`** → you imported the Windows artifact-tool from WSL.
  Use the Linux port. This is the #1 blocker and it looks like the tool "doesn't exist".
- **Do not substitute `pptxkit`/python-pptx for a final client deck.** It's correct for
  `branded-pptx-deck`; it is not this pipeline's method.
- **Never pass a fixed card height.** `card(x,y,w,'auto',…)`. Fixed heights = 40–50% dead
  air = the deck reads as junk. Density is correctness, not taste.
- **`flowChartTerminator` renders as a bare rule** — use `flowChartAlternateProcess`.
- **`rail()` on a dark slide needs `{dark:true}`** or labels fail the 4.5:1 contrast rule.
- **Montage export is broken in the WSL port** (page 1 only) — build contact sheets from
  per-slide PNGs with PIL.
- **`0 pictures` is not a quality target.** It is what the DeepGrid decks happened to need. A
  cover photo or illustration inside a native slide is compliant — only *flattened slides* are
  banned. Do not redraw a photograph as shapes to protect a number.
- **A green provider preflight does not mean an image will render.** It proves reachability,
  not quota. Built-in Codex image generation is separate from OmniRoute; confirm whichever
  selected route with a real render.
- **Fonts:** DM Serif Display/Questrial are absent on Linux. The kit sets the design system's
  documented fallbacks (Georgia/Arial) deliberately. Local renders showing sans titles is a
  render artifact, not a defect — Windows PowerPoint resolves Georgia.
- **Banned-number scans throw false positives.** A corrected figure legitimately appears
  inside its own disavowal, and real filed quarters ("Q4 2024") hit fabricated-date regexes.
  **Print surrounding text before calling anything a defect.**
- **File locked in PowerPoint** → "Permission denied" on copy. Write a NEW filename; never
  claim delivery succeeded without checking the copy's exit status.
- **Status honestly:** `*-draft.pptx` until OfficeCLI passes + contact sheet reviewed +
  internal-term scan clean; only then `*-reviewed.pptx`. `blocked` if a required path is gone.
