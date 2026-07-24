# Future Skill Chain Note: Agent-Native Decks

Use a controlled local skill chain for future agent-native deck creation. Exclude subscription-gated slide generators from the default pipeline.

Recommended chain:

1. `content-research` or `video-to-deck` for source ingestion and structured notes.
2. `ce-agent-native-architecture` for architecture vocabulary, components, and flows.
3. `presentation-content-writer` for self-contained slide narrative.
4. Equivalent image-generation path for a small number of high-quality hero or conceptual images when images add value:
   - Primary immediate option: OpenAI `image_gen`.
   - Optional later option: `ce-gemini-imagegen` / Nano Banana Pro only when quota is available.
5. `drawio` or Excalidraw-style diagram generation for architecture diagrams when editable diagrams are required.
6. `branded-pptx-deck` / `pptxkit` for final native PowerPoint generation, validation, preview, and delivery.

Decision rule:

- Use generated images only when they should carry mood, cover art, or a conceptual visual. They should not replace architecture block diagrams.
- Use `branded-pptx-deck` for final client-facing PowerPoint output and QA.
- Do not rely on generated decorative images for architecture slides. Core architecture visuals should be block diagrams with clear labels, large text, and no overlap.

Nano Banana Pro setup status:

- Skill present: `compound-engineering:ce-gemini-imagegen`.
- Dependency installed locally: `google-genai`.
- The skill expects `GEMINI_API_KEY`.
- This host currently exposes `GOOGLE_GENERATIVE_AI_API_KEY`; pass it as `GEMINI_API_KEY="$GOOGLE_GENERATIVE_AI_API_KEY"` when invoking the scripts.

Test result on 2026-06-12:

- `gemini-3-pro-image-preview` call reached the Gemini API but failed with `429 RESOURCE_EXHAUSTED`.
- `gemini-2.5-flash-image` fallback also reached the Gemini API but failed with `429 RESOURCE_EXHAUSTED`.
- Interpretation: the local skill pipe is wired, but the current Google project/key has zero available free-tier image-generation quota for these models.
- Required before production use: use a Gemini key/project with active billing or available image-generation quota.

Equivalent tool decision after quota failure:

- Use OpenAI `image_gen` for local cover/concept image generation when a visual asset is needed immediately.
- Use Draw.io or Excalidraw-style block diagrams for core architecture slides because precise labels, arrows, and no-overlap constraints matter more than visual flourish.
- Do not include subscription-gated slide generators in the default deck pipeline.

Known quality constraints from this run:

- Body text must be presentation-sized, not document-sized.
- Each slide needs a narrative description, not only bullets.
- Diagrams need a plain-English explanation beside or below the visual.
- Architecture diagrams should use building blocks, arrows, labels, and explicit flows.
- Final `.pptx` must pass XML validation and open in Windows PowerPoint without repair prompts.
