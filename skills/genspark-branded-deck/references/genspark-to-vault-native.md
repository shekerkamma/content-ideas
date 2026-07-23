# Genspark-to-Vault native design handoff

Use this contract when Genspark provides a strong concept or visual direction but
the final presentation must satisfy the Client-Ready PPTX Design System.

## Division of responsibility

| Layer | Genspark contributes | Vault contributes |
|---|---|---|
| Story | Slide order, action-title candidates, visual metaphors | Executive arc check, evidence discipline, density decisions |
| Design | Mood, semantic color roles, archetype inspiration | 12-column grid, L01–L16 layouts, typography, contrast, spacing |
| Content | Draft wording and grouping | Source-grounded claims, concise copy, speaker notes |
| Build | Recovered HTML and PNG references | Native artifact-tool JSX objects; zero flattened layouts |
| QA | Reference contact sheet | Structural validation, OfficeCLI, real render, internal-term scan |

## Required handoff files

Keep these together in the run folder:

- `genspark-handoff.json`
- recovered `genspark-source/html/`
- rendered Genspark reference slides
- `GENSPARK-DESIGN-SPEC.md` or equivalent token/archetype notes
- validated story source and `story-architect-pack.md`
- `visual-spec-native.json`
- native builder script and QA evidence

## Token translation

Translate roles, not literal colors. The Client-Ready design system remains the
delivery authority.

| Genspark role | Vault-native role |
|---|---|
| Dark control-surface field | Midnight technical, cover, ask, or close slide |
| Pale primary text | White on dark; Slate on light |
| Control / subject accent | Cyan by default; use red or amber only for tension/risk |
| Execution / active state | Teal or verified success green |
| Intelligence / model layer | Pale blue or cyan |
| Caution / prerequisite | Amber |
| Dense background grid, glow, glass | Remove; replace with clean alignment, rules, and whitespace |

Use one dominant accent per slide. Do not preserve decorative gradients, glow,
glass, or a full-deck dark treatment merely because the Genspark reference used
them.

## Archetype translation

| Genspark pattern | Vault-native layout |
|---|---|
| Thesis cover | L01 cover or L02 executive thesis |
| Problem/capability card grid | L03 positioning or L05 pillars |
| Node-and-arrow architecture | L04 process, L07 architecture, or L08 technical deep dive |
| Three-step setup/adoption sequence | L04 process or L11 roadmap |
| Two-mode comparison | L10 competitive/comparison |
| Role/profile catalog | L09 product/service matrix |
| Final recommendation | L14 ask/next step |

## Native rebuild rules

1. Treat the Genspark slide list as the reference storyline under Rule 0.
2. Rebuild every title, card, table, diagram, timeline, and chart as a native
   artifact-tool JSX object placed from `deck-grid.mjs`.
3. Images are allowed only as authentic evidence or approved assets inside a
   native slide; a rendered Genspark slide is never the final background.
4. Preserve semantic meaning, not source coordinates.
5. Apply the automatic visual verdict per slide: `NATIVE`, `PLACE ASSET`,
   `GENERATE`, or `NONE`. Genspark reference art does not bypass this gate.
6. Keep the hybrid Genspark build as a prototype/reference artifact and label it
   honestly. Promote only the Vault-native output to `*-reviewed.pptx`.

## Acceptance criteria

- Slide order remains traceable to the recovered Genspark deck.
- `visual-spec-native.json` validates with `output_mode: native`.
- Zero full-slide pictures and no flattened layout backgrounds.
- All claims, labels, flows, cards, and timelines are editable.
- Structural validation passes.
- OfficeCLI reports `passed` with zero issues.
- Real-render contact sheet is visually clean.
- Visible text contains no internal tool names, paths, or production labels.
