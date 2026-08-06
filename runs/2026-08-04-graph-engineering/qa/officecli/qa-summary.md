# Render QA summary

- Render path: OfficeCLI/officecli binary and repo-root `scripts/officecli_qa.py` were not
  available in this environment. Fallback used per skill instructions: Windows-side
  LibreOffice (`/mnt/c/Program Files/LibreOffice/program/soffice.exe`) headless
  `--convert-to pdf`, then rendered to per-slide PNGs at 110 DPI (PyMuPDF).
- `lint_pptx.py` (deterministic design-quality gate): **0 errors, 0 warnings** — see
  `qa/pptx-design-lint.json`. (First pass found 2 errors / 48 warnings — label
  contrast/size, 4 overlong titles causing wrap/overflow risk, two slides over the 80-word
  budget, a table-row/footnote overlap on slide 13, and 9 back-to-back visually identical
  layouts on slides 4-12; all fixed in `build_deck.py` — see git-free run history in that
  file's content — and confirmed clean on rebuild.)
- Real render pass (`qa/officecli/render/slide_01.png` … `slide_14.png`): all 14 slides
  visually inspected. No red overflow, no clipped text, no title/subtitle collisions, no
  overlapping boxes, footer + page number present on every slide, all 10 extracted
  evidence images render legibly with the webcam bubble cleanly masked and no title/body
  text clipped by the mask.
- Programmatic internal-term + timestamp scan across every text shape in the deck:
  **clean** — no `transcript`, `hyperframe`, `Excalidraw`, `YouTube`, `synthesis`, `audit`,
  `validation`, `Codex`, `Claude`, file paths, or `MM:SS` timestamps found in any
  client-facing slide text. (The source video's own "Startup Ideas Podcast" branding badge
  is visible inside the extracted evidence images themselves — baked into the presenter's
  original on-screen graphic — per the content-cuts decision in the story-architect pack,
  this is left as-is since it is part of the captured evidence pixels, not restated in any
  native slide text.)
- `presentation-evidence.json` + `slide-plan.json` + `graph-engineering-visual-spec.json`
  cross-validated together with `validate_presentation_contracts.py`: **valid**, no
  unresolved evidence references, no orphaned visuals.

## Delivery gate status

| Gate | Status |
|---|---|
| 0. Deck-context (deck-brief.md + deck-design.json) | Pass — validated |
| 1. Story (story-architect pack) | Pass — used directly, not a fallback |
| 2. Evidence (grill-me validation) | Pass — 14/14 claims challenged and resolved |
| 3. Capture-completeness + coverage | Pass — see graph-engineering-hyperframes.md (28/28 frames accounted for; `token-burner` used as the closest available substitute for the undocumented `scene-complete` mode — see run report) |
| 4. Client-language | Pass — programmatic scan clean |
| 5. Render | Pass — lint clean + real LibreOffice render inspected |
| 6. Editability | **Hybrid editable** |
| 7. Proof (named examples survive) | Pass — LangGraph, AutoGen GraphFlow, n8n, Make.com, Shopify worked example all preserved by name |
| 8. Generated-asset | Not applicable — no image-model assets used in this deck |

**Status: reviewed.**
