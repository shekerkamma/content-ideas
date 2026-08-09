# Realization Pattern Selection Guide

## The four patterns

### 1. RAG (Retrieval Augmented Generation)
**Signal:** Unstructured documents. Query is "tell me about X" or "what does policy Y say."
**Best for:** Enterprise search, meeting summarization, policy Q&A, RFP response generation, contract review assistance.
**Maturity:** Highest — production at scale across all hyperscalers.
**ROI timeline:** 1–4 months.
**Stack:** Embedding model + vector DB (Pinecone / Weaviate / pgvector / Vertex AI Matching Engine) + LLM.

### 2. Document AI (Structured Extraction)
**Signal:** High-volume documents with predictable structure (forms, invoices, contracts, medical records, insurance claims).
**Best for:** Claims processing, KYC document extraction, mortgage/lease review, prior authorization form parsing.
**Maturity:** High — GCP Document AI (70+ specialized processors), AWS Textract, Azure Form Recognizer.
**ROI timeline:** 2–6 months.
**Stack:** Purpose-built extraction model (not LLM-first) + output validation + downstream workflow.
**Key metric:** Extraction recall 90–99% on trained models; 70–85% on prompted LLMs.

### 3. Multi-Agent Orchestration
**Signal:** Workflow has 3+ decision points requiring different tools, data sources, or role separations.
**Best for:** Prior authorization (intake → clinical review → determination → notification), loan underwriting, complex supply chain ops.
**Maturity:** Emerging but production-ready in FS and healthcare verticals.
**ROI timeline:** 6–12 months (higher integration cost).
**Stack:** Orchestrator agent (ADK / LangGraph / Bedrock Agents) + specialist subagents with scoped tools + human-in-loop escalation point.
**Rule:** Each subagent should have exactly one role and a clean tool boundary. Avoid "mega-agents" with 10+ tools.

### 4. Knowledge Graph + MCP
**Signal:** Agents need structured metadata from enterprise data catalogs, API catalogs, or knowledge bases.
**Best for:** AI-assisted data stewardship, enterprise data catalog navigation, schema-aware code generation, grounded analytics agents.
**Maturity:** Emerging — GCP native, AWS/Azure require custom wrappers.
**ROI timeline:** 2–6 weeks for bootstrapping; ongoing value from day-one metadata grounding.
**Stack:** Enterprise catalog (GCP Knowledge Catalog / AWS Glue / Azure Purview) + MCP server + agent with MCPToolset.

## Decision flowchart

```
Is the source structured metadata (tables, schemas, lineage)?
  YES → Knowledge Graph + MCP
  NO ↓

Is the source high-volume structured documents (forms, invoices)?
  YES → Document AI
  NO ↓

Does the workflow have 3+ distinct decision stages with different tools?
  YES → Multi-Agent Orchestration
  NO → RAG
```

## Pattern combinations (common)

| Use case | Primary | Supporting |
|---|---|---|
| Prior authorization | Multi-Agent | Document AI (form parsing) + RAG (policy lookup) |
| Enterprise search | RAG | — |
| Data catalog AI | Knowledge Graph + MCP | RAG (for enriching descriptions) |
| KYC onboarding | Document AI | Multi-Agent (orchestrator) |
| Code assistant (enterprise) | RAG | Knowledge Graph + MCP (for API/schema grounding) |

## Anti-pattern: LLM for deterministic extraction
Using a prompted LLM (GPT / Claude / Gemini) as the primary extraction engine for high-volume structured forms is an anti-pattern at scale. Cost per page is 10–50× higher than a trained Document AI model, and recall is 15–25 percentage points lower. Reserve LLMs for post-extraction enrichment, summarization, or edge-case handling — not bulk extraction.
