---
name: present
description: Route any request to create, rebuild, edit, review, theme, export, or improve a presentation to the correct governed presentation workflow. Use for PowerPoint/PPTX, HTML slides, Genspark slides, Marp, source-deck rebuilds, speaker notes, accessibility, and client-ready presentation delivery.
---

# Present

Act as the single public entry point for presentation work. Select an existing engine; do
not create another presentation workflow.

## Route

| Request | Primary route |
|---|---|
| Client-ready native, editable PPTX | `branded-pptx-deck` |
| Inspect or make controlled edits to an existing PPTX | `pptx-toolkit` |
| Rebuild from PPTX, PDF, OneDrive, video, or slide images | `presentation-source-bundle` → selected builder |
| Browser-native HTML presentation | `presentation` |
| Hosted Genspark generation or recovery | `genspark-slides` → `genspark-branded-deck` |
| Markdown-driven technical slides | `marp` |
| Speaker notes, accessibility, theme, or export | Apply the matching presentation support stage to the selected engine |

Domain skills such as `research-to-deck`, `architecture-presentation`,
`analytics-to-comms`, and `gcc-roadmap` remain content/orchestration stages. Require them to
hand off through the shared contracts instead of inventing a renderer.

## Governed workflow

For any material deck build or redesign:

1. Select the output engine and state the editability mode.
2. Use `presentation-source-bundle` when a source presentation, URL, PDF, or video exists,
   producing `presentation-evidence.json`.
3. Use `pptx-design-quality` to create and validate `deck-brief.md`,
   `deck-design.json`, and `template-profile.json`. When `presentation-evidence.json`
   exists, derive a draft `template-profile.json` from it first with
   `derive_template_profile.py`, then tailor and validate — do not hand-author from the
   blank template when a reference deck is available.
4. Tailor `slide-plan.json` using archetype IDs from the design-quality catalog. When
   `presentation-evidence.json` exists, draft it first with `draft_slide_plan.py` instead
   of starting from the blank template.
5. Use `pptx-visual-spec` to create and validate `visual-spec.json`.
6. Build with the selected engine.
7. Run that engine's structural validation, design lint, real-render QA, and visual review.
8. Label the result `draft`, `reviewed`, or `blocked`; never promote without evidence.

## Routing rules

- Default client-facing deliverables to native editable PPTX.
- Treat HTML, Genspark, and Marp as deliberate output choices, not interchangeable
  implementations.
- Preserve exact-state source visuals when appearance is evidence; keep ordinary claims,
  data, titles, and feasible diagrams native and editable.
- Keep credentials and host-specific connector configuration outside the project.
- Do not expose internal tool names, source paths, validation labels, or production notes on
  client-facing slides.
- Do not ask users to manually chain support skills when the route can invoke them as stages.

## Required handoff

The standard governed handoff is:

```text
presentation-evidence.json  # source-derived work only
deck-brief.md
deck-design.json
template-profile.json
slide-plan.json
visual-spec.json
builder source
draft/reviewed presentation
qa/
```

If a selected engine cannot consume the relevant contracts, adapt the engine through a thin
adapter. Do not weaken or duplicate the contracts.

## Relationships

| Skill | Pattern | Handoff |
|---|---|---|
| `presentation-source-bundle` | Conditional upstream | `presentation-evidence.json` |
| `pptx-design-quality` | Mandatory design overlay | brief, design, template profile, lint evidence |
| `pptx-visual-spec` | Mandatory visual overlay | slide plan and visual specification |
| `branded-pptx-deck` | Native PPTX engine | editable `.pptx` |
| `pptx-toolkit` | Existing-PPTX modifier | controlled edited `.pptx` |
| `presentation` | HTML engine | HTML presentation |
| `genspark-slides` | Hosted source engine | `genspark-handoff.json` |
| `genspark-branded-deck` | Genspark downstream | governed PPTX/HTML output |
| `marp` | Markdown engine | HTML/PDF/PPTX with declared editability |
