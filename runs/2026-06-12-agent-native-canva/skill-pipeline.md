# Reusable Skill Pipeline

This run converged on a better deck-build chain than the earlier ad hoc flow.

## Default Chain

1. `content-research` or `video-to-deck` for source ingestion and structured notes.
2. `compound-engineering:ce-agent-native-architecture` for the architecture and workflow framing.
3. `presentation-content-writer` for slide-by-slide narrative and action titles.
4. `drawio` or Excalidraw-style diagram generation for architecture visuals.
5. `branded-pptx-deck` / `pptxkit` for final native PowerPoint generation and validation.
6. `presentation-exporter` for PDF or image export when a portable review artifact is needed.

## Usage Rules

- Do not include Genspark or other subscription-gated slide generators in the default pipeline.
- Use OpenAI `image_gen` only for selective cover or conceptual imagery when the deck genuinely benefits from it.
- Keep architecture slides as labeled block diagrams, not decorative AI art.
- Make the slide narrative self-explanatory before rendering the deck.
- Validate the PPTX structurally before delivery.
- Review rendered contact sheets before copying to Windows Desktop.

## Observations From This Run

- The skill chain worked better than the earlier single-script flow.
- Narrative quality improved once the content writer and architecture framing were used before rendering.
- Diagram quality improved when the deck relied on explicit blocks and labels instead of generic generated images.
- The deck still needs a human visual QA pass on the cover whenever the layout changes.

## Reuse Note

For future decks, start with the source research and narrative skills, then move into branded PPTX rendering only after the storyboard is stable.
