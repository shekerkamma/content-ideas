# Video Deck Validation: Brainstorm / Discovery Notes
Date: 2026-07-03 - Goal: Validate every slide in the AI Agents Are The New SaaS deck for content support, design quality, visible client language, and visual coverage.

## Structured context
- **Topic type**: deck validation
- **Topic string**: Slide-by-slide grill-me validation of `ai-agents-new-saas-video-deck-v8-validated-draft.pptx`
- **Entities**: AI Agents Are The New SaaS, Slang AI, Same Day, Excalidraw, branded PPTX workflow
- **Prospect/account**: n/a
- **Target buyer**: executive / client-facing deck audience
- **Verticals**: SaaS, AI agents, service workflows
- **Open decisions**: whether to rebuild v9 now or keep v8 as blocked draft -> user / builder

## Summary / key decisions

Validated deck:
`runs/2026-07-02-video-to-deck-rerun/ai-agents-new-saas-video-deck-v8-validated-draft.pptx`

Supporting artifacts reviewed:
- `runs/2026-07-02-video-to-deck-rerun/grill-me-validation-v8.md`
- `runs/2026-07-02-video-to-deck-rerun/ai-agents-new-saas-storyboard.md`
- `runs/2026-07-02-video-to-deck-rerun/ai-agents-new-saas-screen-change-coverage.md`
- `runs/2026-07-02-video-to-deck-rerun/ai-agents-new-saas-visual-inventory-v2.md`
- Real render contact sheets from `/tmp/video-deck-v8-render/contact_real_1.png` and `/tmp/video-deck-v8-render/contact_real_2.png`

Validation result: **blocked for client delivery**.

Why:
- The deck is structurally much better than earlier drafts: 15 slides, executive summary, conclusion, consistent branded layout, no timestamps, no YouTube references, and no hyperframe screenshots visible.
- Mechanical PPTX validation passes.
- However, five slides still expose internal/source wording by saying `transcript` on visible client slides.
- Most Excalidraw visuals are present, but they are dark, small, and partially illegible at slide scale.
- The visual inventory is mostly covered, but named examples such as Slang AI and Same Day are softened into generic categories, reducing proof value.
- The PPTX embeds rendered Excalidraw PNGs. The `.excalidraw` sources exist, but the diagram content is not editable inside PowerPoint itself.

## Mechanical QA

- Slide count: 15.
- PPTX XML validation: pass via `validate_pptx`.
- Real render: pass via LibreOffice -> PDF -> PyMuPDF PNGs.
- Embedded media: 12 PNG images.
- Slides with pictures: 1, 3-14.
- Slides without pictures: 2, 15.
- Internal-term scan:
  - `transcript` appears on slides 3, 7, 9, 10, and 13.
  - No visible hits for `excalidraw`, `youtube`, `hyperframe`, `synthesis`, `validation`, `audit`, `timestamp`, `codex`, or `claude`.

## Slide-by-slide grill validation

### Slide 1 - Cover
- **Content support**: Pass. The title and subtitle match the core video thesis.
- **Design**: Pass with caution. Strong executive cover, but the small dark inset is not readable as a visual proof element.
- **Body/content**: Pass. No internal process language.
- **Required fix**: Optional: either enlarge the inset or remove it; do not rely on it for communication.

### Slide 2 - Executive Summary
- **Content support**: Pass. The summary captures workflow choice, human shadowing, smallest useful agent, trust wrapper, and pilot path.
- **Design**: Pass. Dense but controlled; good BLUF / where-how-win structure.
- **Body/content**: Pass. Client-facing language is clean.
- **Required fix**: None.

### Slide 3 - Market Context
- **Content support**: Mostly pass. The labor-vs-software framing is transcript-backed.
- **Design**: Caution. The dark chart is visible but too small for detailed reading.
- **Body/content**: Fail. Visible text says "The transcript frames..." which is an internal source note.
- **Required fix**: Replace with client-facing wording such as "The core argument reframes software from helping teams do work to owning finished work outcomes."

### Slide 4 - Core Thesis
- **Content support**: Pass. "The product is the job" is directly supported.
- **Design**: Caution. Diagram is relevant but handwritten labels are small.
- **Body/content**: Pass. Clean client language.
- **Required fix**: Enlarge/redraw diagram labels for slide-scale readability.

### Slide 5 - Economics
- **Content support**: Pass. Labor comparison and junior employee / agency / headcount framing are supported.
- **Design**: Caution. Visual is useful but the table text is hard to read.
- **Body/content**: Pass.
- **Required fix**: Convert the comparison table into native PPT text or larger Excalidraw labels.

### Slide 6 - Examples
- **Content support**: Partial pass. The categories are supported, but the transcript examples Slang AI and Same Day are missing by name.
- **Design**: Caution. Visual is clean, but the category cards are generic.
- **Body/content**: Partial. Good takeaway, weak evidence specificity.
- **Required fix**: Add named example cards for Slang AI and Same Day, while keeping presenter/youtuber images excluded.

### Slide 7 - Workflow Selection
- **Content support**: Pass. The scorecard dimensions are transcript-backed.
- **Design**: Caution. The scorecard visual is relevant but small.
- **Body/content**: Fail. Visible text says "The transcript's selection rule..." which is internal/source language.
- **Required fix**: Replace with "The selection rule is direct: start where buyers already fund an employee, agency, receptionist, coordinator, or dispatcher."

### Slide 8 - Observation
- **Content support**: Pass. Shadowing 10-20 cases, checks, exceptions, and acceptance criteria are supported.
- **Design**: Caution. Diagram is on-topic but small.
- **Body/content**: Pass.
- **Required fix**: Increase contrast and label size in the diagram.

### Slide 9 - First Product
- **Content support**: Pass. Draft-and-approve, triage, coordinator, and bounded action are supported.
- **Design**: Caution. The four-step visual is useful but cramped.
- **Body/content**: Fail. Visible text says "The transcript says..."
- **Required fix**: Replace with "The first product should be smaller than the fully autonomous employee promise."

### Slide 10 - Workflow Architecture
- **Content support**: Pass. Predictable workflows before autonomy is supported.
- **Design**: Caution. Visual is clear at macro level, but labels are small.
- **Body/content**: Fail. Visible text says "The transcript cites..."
- **Required fix**: Replace with "Many agent products should start as predictable workflows before adding judgment-heavy autonomy."

### Slide 11 - Trust Wrapper
- **Content support**: Pass. Wrapper, logs, approvals, controls, handoffs, analytics, and evals are supported.
- **Design**: Caution. Visual is legible enough at high level, but smaller labels still need enlargement.
- **Body/content**: Pass.
- **Required fix**: Prefer larger visual labels or native PPT annotation callouts.

### Slide 12 - Commercialization
- **Content support**: Pass. Pilot like labor, setup plus monthly, and usage/outcome pricing are supported.
- **Design**: Caution. Diagram is relevant but sparse compared with the importance of the section.
- **Body/content**: Pass.
- **Required fix**: Add a clearer commercial model ladder: setup -> monthly -> usage/outcome.

### Slide 13 - Productization
- **Content support**: Pass with caution. This fixed the earlier unsupported moat framing, but it underplays the "own the workflow" section from the source.
- **Design**: Caution. Visual is fine but not distinctive enough from slide 12.
- **Body/content**: Fail. Visible text says "The transcript-supported productization path..."
- **Required fix**: Replace with client-facing wording and explicitly connect repeated work to workflow ownership.

### Slide 14 - 30-Day Plan
- **Content support**: Pass. The 30-day sequence and workflow teardown distribution are supported.
- **Design**: Caution. Strong slide title, but the five-week/day visual is too small for comfortable reading.
- **Body/content**: Pass.
- **Required fix**: Make the plan native PPT text or enlarge the visual.

### Slide 15 - Conclusion
- **Content support**: Pass. The next-move sequence matches the video argument.
- **Design**: Pass. Clean closing slide with clear four-step action path.
- **Body/content**: Pass.
- **Required fix**: None.

## Open flags

- Should v9 prioritize PowerPoint-native diagram editability, or is separate `.excalidraw` source plus rendered diagram acceptable? -> user
- Should named product examples be included as client-facing proof cards even when the source video used screenshots/logos? -> user / builder
- Should the deck move to Google Slides for visual iteration after v9 rebuild? -> user

## Recommended rebuild criteria for v9

1. Remove all visible uses of `transcript` from slides 3, 7, 9, 10, and 13.
2. Enlarge or redraw every Excalidraw visual so labels are readable in slide view.
3. Add named proof cards for Slang AI and Same Day on the examples slide.
4. Strengthen slide 13 to cover workflow ownership, not only productization.
5. Decide explicitly whether final diagrams must be PowerPoint-native editable shapes or whether delivered `.excalidraw` source files satisfy editability.
6. Re-render to PDF/PNG and repeat the slide-by-slide review before marking reviewed.

## V9 rebuild outcome

Reviewed deck:
`runs/2026-07-02-video-to-deck-rerun/ai-agents-new-saas-video-deck-v9-reviewed.pptx`

Builder:
`runs/2026-07-02-video-to-deck-rerun/build_video_deck_v9_reviewed.py`

Updated diagram source:
`runs/2026-07-02-video-to-deck-rerun/build_excalidraw_diagrams_v3.js`

Real render QA:
- PDF: `/tmp/video-deck-v9-render/ai-agents-new-saas-video-deck-v9-reviewed.pdf`
- Contact sheet 1: `/tmp/video-deck-v9-render/contact_real_1.png`
- Contact sheet 2: `/tmp/video-deck-v9-render/contact_real_2.png`

Fixes applied:
- Removed visible internal/source wording from slides 3, 7, 9, 10, and 13.
- Enlarged the visual frame across story slides.
- Added named proof examples, including Slang AI and Same Day, to slide 6.
- Reframed slide 13 around workflow ownership and productizing repeated work.
- Regenerated Excalidraw diagrams through the live local canvas.
- Rebuilt the PPTX as a reviewed artifact rather than a draft artifact.

V9 validation:
- Slide count: 15.
- PPTX XML validation: pass.
- Internal-term scan: pass for `excalidraw`, `youtube`, `hyperframe`,
  `transcript`, `synthesis`, `validation`, `source`, `audit`, `timestamp`,
  `markdown`, `grill`, `codex`, and `claude`.
- Real render: pass through LibreOffice -> PDF -> PyMuPDF PNG contact sheets.
- Embedded media: expected 12 diagram images.
- Client-facing structure: pass. Includes cover, executive summary, story slides,
  and conclusion.
- Visual coverage: pass with caveat. Meaningful visual beats are represented by
  recreated Excalidraw diagrams, while presenter-only frames remain excluded.

Residual caveat:
- The visible diagrams are rendered Excalidraw PNGs with separate `.excalidraw`
  source files. They are editable at the diagram-source layer, but not as native
  PowerPoint shapes inside the deck.
- Some hand-drawn labels remain less crisp than native PowerPoint text. The deck
  is acceptable as a reviewed Excalidraw-style deck. If the requirement is
  PowerPoint-native editability and maximum label crispness, run a v10 rebuild
  that converts the diagram labels and boxes into native PPT shapes.

Final status: **reviewed with editability caveat**.
