# AI Knowledge Graphs vs Traditional RAG: Compilation-Based Retrieval for Enterprise Knowledge Management

## Executive Summary

Traditional Retrieval-Augmented Generation (RAG) systems retrieve document chunks via vector similarity at query time — fast to set up, but brittle under cross-document reasoning. Compilation-based approaches (exemplified by OpenKB and knowledge graph systems) treat ingestion as a first-class build step: the LLM synthesizes, cross-references, and structures knowledge at ingest time, producing a human-readable, queryable artifact. For enterprise knowledge management, the trade-offs between these paradigms are significant: RAG optimizes for breadth and speed of indexing; compilation-based systems optimize for depth and faithfulness of reasoning.

## Key Findings

### 1. The "Amnesia Problem" in Traditional RAG
Traditional RAG stores raw chunks as dense vectors and retrieves by cosine similarity at query time. This produces K-nearest neighbors that may individually be relevant but lack the cross-document reasoning needed for synthesis. Each query starts with no memory of previous queries or of how concepts relate across documents. Contradiction detection is absent — two conflicting passages may both be returned without any flagging.

### 2. Knowledge Graphs as a Retrieval Layer
Knowledge graphs (Neo4j, Amazon Neptune, Google's Knowledge Catalog) model entities and their relationships explicitly. Graph traversal enables multi-hop reasoning: "Who worked with Person X on Project Y?" can follow edges rather than relying on co-occurrence in a chunk. The limitation: building production-grade knowledge graphs requires significant schema design, ontology definition, and entity resolution work. They are better for structured domains (pharma, compliance, HR) than for fast-moving document corpora.

### 3. Compilation-Based Retrieval (OpenKB / PageIndex model)
OpenKB treats document ingestion as a compilation step: the LLM reads each document, generates a summary, identifies and updates concept pages, creates entity pages, and builds cross-references. The output is a Markdown wiki — human-readable, inspectable, and diffable. PageIndex enables vectorless retrieval: rather than embedding chunks, it indexes over the compiled wiki pages, which are already semantically structured. Key advantages:
- Cross-document contradictions flagged at compile time
- Synthesis reflects everything ingested, not random K-nearest chunks
- Build artifact is auditable by humans without specialized tooling

### 4. Hybrid Approaches
Production enterprise systems increasingly combine both paradigms. Microsoft GraphRAG (2024) extracts a local knowledge graph at index time, then uses graph-aware retrieval at query time. Amazon Bedrock Knowledge Bases supports both semantic (vector) and structured (graph) retrieval in the same pipeline. The compilation step adds latency and cost at ingest time but dramatically improves retrieval faithfulness for complex, multi-document queries.

### 5. Enterprise Fit Comparison

| Dimension | Traditional RAG | Knowledge Graph | Compilation (OpenKB) |
|---|---|---|---|
| Ingest speed | Fast | Slow (schema design) | Medium |
| Query faithfulness | Low (chunk retrieval) | High (structured) | High (compiled) |
| Cross-doc synthesis | Poor | Good (if modelled) | Excellent |
| Human-auditable | No | Partial | Yes |
| Setup complexity | Low | High | Medium |
| Best for | Broad document search | Structured domains | Dynamic, growing corpora |

### 6. The PageIndex Innovation
PageIndex (used by OpenKB) addresses the vectorless retrieval challenge: rather than embedding raw chunks, it indexes over compiled concept and entity pages which already contain synthesized, cross-referenced information. This reduces the semantic distance between the query and the retrieved unit — the page is about the concept, not just a passage that mentions it.

## Sources

1. Lewis et al. (2020) — "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Facebook AI Research)
2. Edge et al. (2024) — "From Local to Global: A Graph RAG Approach to Query-Focused Summarization" (Microsoft Research)
3. OpenKB documentation — VectifyAI, github.com/VectifyAI/OpenKB
4. Karpathy, A. — LinkedIn post on compilation-based retrieval (2024)
5. Amazon Web Services — "Knowledge Bases for Amazon Bedrock" technical documentation (2024)
6. Google Cloud — "Enterprise Knowledge Graph" and "Knowledge Catalog" documentation (2024)

## Open Questions

- At what corpus size does compilation latency become a blocking constraint vs. the faithfulness gains?
- How does GraphRAG's local/global community structure compare to OpenKB's flat concept+entity wiki structure for reasoning tasks?
- Can PageIndex be combined with sparse BM25 retrieval for hybrid search over the compiled wiki?
