# Synthesis: AI Knowledge Graphs vs Traditional RAG

## Q1 — Core difference between traditional RAG and compilation-based retrieval

Traditional RAG retrieves document chunks at query time via vector similarity (K-nearest neighbors). It suffers from the "Amnesia Problem": no cross-document memory, no contradiction detection, poor synthesis faithfulness.

Compilation-based retrieval (OpenKB) treats ingestion as a first-class build step. An LLM synthesizes all documents into a human-readable Markdown wiki — summaries, concept pages, entity pages, cross-references (wikilinks). Contradictions are flagged at compile time. Every query draws on the full compiled corpus, not random chunks.

## Q2 — Knowledge graphs vs vector search for enterprise use cases

Knowledge graphs explicitly model entities and relationships, enabling multi-hop reasoning ("Who worked with X on Project Y?"). Higher query faithfulness, better cross-document synthesis, partial auditability. Trade-off: slow ingest, high setup complexity (schema design, ontology, entity resolution). Better for structured, static domains (pharma, compliance, HR).

Vector search is fast to set up and broad in coverage but lacks the relationship structure for complex synthesis. Best for breadth, not depth.

## Q3 — How PageIndex enables vectorless retrieval

PageIndex indexes over compiled wiki pages (concept and entity pages) rather than raw chunk embeddings. Because each page is already semantically structured and synthesized, the retrieved unit IS the concept — not a passage that mentions it. This reduces the semantic distance between query and result and removes the dependency on vector infrastructure entirely for long-form content.

## Q4 — GraphRAG vs OpenKB

Microsoft GraphRAG (2024) extracts local knowledge graphs at index time and uses graph-aware retrieval at query time. Local/global community structure. Hybrid: graph + vector.

OpenKB: flat wiki structure, upfront compilation step, fully human-readable artifacts, vectorless (PageIndex). No schema design required. Better for dynamic, growing corpora. GraphRAG better for domains with strong pre-existing ontologies.

## Q5 — Best approach for cross-document synthesis

Compilation-based retrieval (OpenKB model) wins for cross-document synthesis:
- Holistic synthesis at ingest time, not patchwork at query time
- Contradiction flagging built in
- High query faithfulness across multi-document queries
- Human-auditable, inspectable, diffable artifacts
- Vectorless retrieval via PageIndex

Knowledge graphs are strong for structured/static domains. Traditional RAG is best only for broad, shallow search over large undifferentiated corpora.
