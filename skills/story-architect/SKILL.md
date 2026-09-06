---
name: story-architect
description: Use before building decks, briefs, or narrative deliverables when raw research, transcripts, notes, or analysis need to become an executive storyboard. Produces BLUF, tension, argument arc, slide spine, evidence map, speaker implication, and rebuild decisions so downstream deck builders do not dump notes or frames onto slides.
metadata:
  legacy-frontmatter:
    user_invocable: true
---

# Story Architect

Turn raw material into a client-ready narrative spine before any deck is built.
Use this when a deliverable needs storyline, synthesis, slide sequencing, or
executive articulation.

## Inputs

Accept any combination of:
- Transcript or notes
- Research pack
- Frame/visual inventory
- Existing draft deck or outline
- User critique of a weak deck

## Required Output

Create a story pack markdown or JSON artifact with these sections:

1. **BLUF** — the one-sentence answer the deck must land.
2. **Audience decision** — what the reader should believe, decide, or do.
3. **Tension** — why this matters now; what breaks if the audience does nothing.
4. **Argument arc** — 5-8 ordered beats: context -> tension -> proof -> implication -> action.
5. **Slide spine** — one row per slide:
   - slide title as an assertion
   - role in the story
   - transcript/research evidence
   - visual treatment
   - speaker implication / takeaway
6. **Evidence map** — claims grouped as direct evidence, fair synthesis, or interpretation.
7. **Content cuts** — what should be excluded from the client deck and why.
8. **Rebuild instructions** — exact changes for the downstream deck builder.

## Rules

- Do not let the deck become a transcript summary, screenshot gallery, or note dump.
- Every slide must advance the argument, not merely label a topic.
- Use source-specific examples when the source provides them.
- Executive summary and conclusion are mandatory for client decks.
- Keep internal production language out of client-facing slide text.
- If a claim is only interpretation, soften it or move it to speaker notes/run artifacts.
- If the source contains demos, each demo needs: setup, observed finding, implication, and action.
- If visuals are reconstructed, specify whether they should be PPT-native, Excalidraw-source, SVG/HTML intermediate, or non-editable render.

## Quality Gate

Before handing off to PPTX rendering, answer:

- Does each slide have a reason to exist?
- Can a reader understand the story without seeing the raw source?
- Are the examples specific enough to prove the claim?
- Is there a clear decision or next action?
- Are there any unsupported claims, internal terms, or visible timestamps?
