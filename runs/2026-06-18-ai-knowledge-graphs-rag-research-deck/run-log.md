# research-to-deck run log
date: 2026-06-18
topic: AI Knowledge Graphs vs Traditional RAG: The Case for Compilation-Based Retrieval
style: neon (Aurora Glass)
kb: /home/shekerk/test-kb

## Stage results
- Stage 1 Research:  ✓ ai-knowledge-graphs-rag-research.md (~750 words, 6 sources)
- Stage 2 Compile:   ✓ compiled into test-kb wiki (gemini/gemini-2.5-flash, LITELLM_DROP_PARAMS=True)
- Stage 3 Synthesis: ✓ ai-knowledge-graphs-rag-synthesis.md (5 questions answered)
- Stage 4 Deck:      ✓ 10 slides, style=neon — openkb-deck-neon (Aurora Glass)
- Stage 5 QA:        ✓ no patches needed (openkb-html-critic — all 5 checks passed)
- Stage 6 PPTX:      skipped (--pptx flag not set)

## Deliverables
- Research brief: runs/2026-06-18-ai-knowledge-graphs-rag-research-deck/ai-knowledge-graphs-rag-research.md
- Synthesis:      runs/2026-06-18-ai-knowledge-graphs-rag-research-deck/ai-knowledge-graphs-rag-synthesis.md
- Deck (draft):   runs/2026-06-18-ai-knowledge-graphs-rag-research-deck/ai-knowledge-graphs-rag-deck-draft.html
- Deck (final):   runs/2026-06-18-ai-knowledge-graphs-rag-research-deck/ai-knowledge-graphs-rag-deck.html

## Slide sequence
1. cover   — "RAG Has an Amnesia Problem"
2. thesis  — Three paradigms (query time / schema time / ingest time)
3. compare — Vector RAG vs Compilation Model
4. data    — "0" cross-references built by traditional RAG
5. chapter — Chapter 02: Knowledge Graphs vs Vector Search
6. compare — Knowledge Graphs vs Vector Search
7. thesis  — "The page IS the concept" (PageIndex)
8. compare — GraphRAG vs Compilation Model
9. quote   — "Synthesis reflects everything the system has consumed"
10. closing — "Build. Compile. Know."

## Notes
- KB patch required for Gemini compatibility: LITELLM_DROP_PARAMS=True + _cached_text() provider guard
  (patched in /home/shekerk/OpenKB, pushed to shekerkamma/OpenKB)
- OKF v0.1 conformance: all wiki pages now emit title/tags/timestamp frontmatter
