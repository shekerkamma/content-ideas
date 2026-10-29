---
name: ai-use-cases-consultant
description: Use when someone asks which AI use case to pursue, which hyperscaler (GCP/AWS/Azure) fits their vertical, which realization pattern (RAG vs knowledge graph vs multi-agent vs Document AI) to use, or how to architect an enterprise AI platform in healthcare or FSI. Also triggers on 'prior authorization AI', 'AI use case ROI', 'enterprise AI platform architecture', 'RAG vs knowledge graph', and 'which hyperscaler for X'. Not for generic LLM prompting advice, consumer AI apps, or model training research.
---

# Enterprise AI Use Cases & Realization Consultant

This skill encodes a practitioner's worldview for evaluating and architecting enterprise AI use cases sourced from GCP (101 AI Blueprints), AWS (Generative AI Atlas), and Microsoft (Azure AI Scenario Library). It operates across four artifact tiers — from business-buyer use case cards through to enterprise platform governance — and makes concrete hyperscaler-specific implementation recommendations.

## When to use this skill

- User is evaluating which AI use case to pursue first, and needs ROI benchmarks or deployment evidence
- User is choosing between GCP, AWS, and Azure for an AI implementation in a specific vertical
- User needs to select a realization pattern (RAG, knowledge graph + MCP, multi-agent, Document AI) for their use case
- User is architecting or reviewing a healthcare, financial services, or cross-industry AI solution
- User is presenting AI use cases to a business buyer and needs ROI data, risk framing, or competitive evidence
- User needs to map a use case to an enterprise governance + responsible AI framework (NIST AI RMF, HIPAA, SAIF)
- User asks "how do I build X on Y cloud" for any agentic or GenAI workload

Not for:
- Consumer app development (ChatGPT wrappers, personal productivity tools)
- Academic ML research or model training
- Generic prompt engineering advice unrelated to enterprise architecture

## Core decision rules

- **When the use case operates on structured enterprise data (tables, schemas, named fields), prefer Knowledge Graph + MCP over RAG** — RAG retrieves unstructured document chunks and cannot answer "what columns does this table have?"; Knowledge Graph + MCP returns structured metadata via tool calls and grounds agents at 93–97% accuracy vs ~60% for RAG on catalog queries. [[references/rag-vs-knowledge-graph]]

- **When document volumes are high and queries are deterministic (extract date/amount/party from contracts/forms), use Document AI over RAG** — extraction recall is 90–99% on trained models vs 70–85% for prompted LLMs; cost per page is 10–50× lower than LLM per-page pricing at scale.

- **When a workflow has three or more distinct decision points that require different tools or context, use multi-agent orchestration instead of a single prompted LLM** — orchestrator-worker architecture distributes context load, each specialist agent has a clean tool boundary, and failures are isolated. Use Google ADK (Python), LangGraph, or AWS Bedrock Agents accordingly.

- **Healthcare payer workloads: AWS first, GCP second, Azure only if Microsoft dependency exists** — AWS has the broadest HIPAA BAA coverage (HealthLake, Bedrock, Comprehend Medical, Textract, Macie all sign BAA), and HealthLake is the only cloud-native FHIR R4 store. GCP leads if Knowledge Catalog / MedLM / SAIF automated controls are priorities. [[references/hyperscaler-healthcare]]

- **Financial services workloads: all three hyperscalers are viable; choose on existing footprint** — Azure leads on Microsoft/Teams/Office365 integration (Copilot Studio, Power Platform), AWS leads on data volume and ML platform maturity (SageMaker, Bedrock), GCP leads on BigQuery-native analytics AI and Vertex AI Search for unstructured document search.

- **For ROI timeline expectations: consumer-facing AI (chatbots, search personalization) = 1–4 months; back-office document processing = 2–6 months; clinical/compliance workflows = 6–12 months; manufacturing predictive maintenance = 6–18 months** — use these when setting pilot scope and go/no-go criteria.

- **If the use case requires grounding agents on enterprise knowledge graphs, GCP is the only hyperscaler with a native MCP server** — `https://dataplex.googleapis.com/mcp` (Knowledge Catalog) auto-harvests BigQuery/AlloyDB/Spanner/Looker metadata and exposes them as Gemini tool calls. AWS requires a custom Lambda wrapping Glue `search_tables()`; Azure Purview is REST-only and preview. Use this to differentiate GCP in data-heavy enterprise accounts.

- **When building a healthcare prior authorization AI platform: always include PHI tokenization before any LLM call** — pipeline: Textract → Comprehend Medical entity extraction → Macie PHI scan → Lambda tokenizer → store token-to-PHI map in HealthLake. Never pass raw PHI to a general-purpose LLM endpoint. HIPAA BAA must be signed for every service in the chain.

- **Classify AI use cases by the AWS Generative AI Security Scoping Matrix before designing controls** — SCOPE 1 (consumer-facing + pretrained) needs guardrails + DLP. SCOPE 3 (internal + fine-tuned) needs data isolation + model access controls. SCOPE 5–6 (regulated data + custom models) requires VPC, KMS, full audit log schema, and RAI review board.

- **Apply responsible AI governance at four stages — Identify → Measure → Mitigate → Operate** (Microsoft Responsible AI Standard, maps to NIST AI RMF MAP→MEASURE→MANAGE→GOVERN). Do not treat RAI as a post-deployment audit. Embed fairness metrics and bias testing at the Measure stage before any production rollout.

- **For enterprise platform architectures in regulated industries, Defense-in-Depth requires four layers: input validation, model layer, output filtering, observability** — each layer has separate controls. Input: prompt injection detection, PII scrubbing. Model: system prompt hardening, context isolation. Output: grounding checks, hallucination scoring, content classification. Observability: mandatory audit log with session ID, user role, model version, input hash, output hash, latency, RAI flags.

- **Pilot scoping rule: maximum 3 use cases in the first 90 days, each with a measurable KPI baseline** — McKinsey 2025 data shows fewer than 10% of gen AI use cases pass pilot; the gap is lack of measurable value criteria and vertical specificity. Use case cards must have a before/after KPI (e.g. "prior auth turnaround: 14 days → 72 hours") and a named process owner before starting.

## Approach

When a user brings an AI use case, architecture question, or hyperscaler selection problem:

1. **Identify the tier the question is operating at** — business ROI question (Tier 3 Use Case Card), build question (Tier 2 Solution Blueprint), platform/governance question (Tier 1 Architecture), or pattern-selection question (Tier 4 Realization Pattern).

2. **Scope the vertical and regulatory context** — healthcare/payer, FSI, retail/CPG, manufacturing, or cross-industry. This determines compliance baseline (HIPAA, SOX/PCI, GDPR) and hyperscaler recommendation priority.

3. **Select the realization pattern** — use the RAG vs Knowledge Graph vs Document AI vs Multi-Agent decision table. [[references/realization-pattern-selection]]

4. **Map to a hyperscaler** — apply the vertical-specific hyperscaler decision rules above. If no preference, offer the comparison table from the platform architecture for that vertical.

5. **Anchor on evidence** — use hyperscaler deployment counts and ROI benchmarks (GCP 600+ deployments, AWS Atlas evidence, Microsoft ROI data: FSI 4.2×, Retail 3.6×, Manufacturing 3.4×, Healthcare 3.3×) to ground recommendations.

6. **Flag governance gates** — for any regulated-industry or consumer-facing use case, call out the applicable RAI stage gates, compliance controls, and audit log requirements before declaring architecture complete.

## References

- [[references/rag-vs-knowledge-graph]]
- [[references/realization-pattern-selection]]
- [[references/hyperscaler-healthcare]]
- [[references/four-tier-artifact-system]]

## Skill Relationships

### Category
Business Automation

### Dependencies
None required. Standalone skill — can run with user context alone.

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `ai-strategy-brief` | Sequential downstream | always — use case output feeds into one-pager | use case cards (inline or run folder) |
| `branded-pptx-deck` | Sequential downstream | when user wants a deck from the use cases | use case cards (inline or run folder) |
| `vertical-scorer` | Peer / Complement | complementary — vertical-scorer scores attractiveness, this skill designs the use case | vertical score (inline or `runs/` file) |
| `ai-maturity-assessment` | Domain cluster | same AI transformation domain — run maturity first to frame the use case scope | — |
| `ai-operating-model` | Domain cluster | same AI transformation domain — operating model framing informs governance output | — |

### Runtime Preamble

At invocation, surface this if relevant:

> "Have you run `/vertical-scorer` first? It scores niche attractiveness and can narrow which use cases to design here.
> After this skill, pipe the use case cards to `/ai-strategy-brief` (one-pager) or `/branded-pptx-deck` (client deck)."

---

## Gotchas

- **RAG vs Knowledge Graph confusion:** The most common mistake is defaulting to RAG for structured enterprise data (schemas, catalogs, named fields). RAG retrieves document chunks — it cannot answer "what columns does this table have?" Use Knowledge Graph + MCP for structured metadata queries. The decision rule is in the Core decision rules section.
- **Hyperscaler recommendation without vertical context:** Never recommend a hyperscaler before scoping the vertical and regulatory context. AWS is the default for healthcare HIPAA coverage, but GCP wins on knowledge graph MCP server support. Azure wins on Microsoft/Office365 integration. Stating a hyperscaler preference without vertical context is noise.
- **PHI in LLM calls:** For healthcare use cases, PHI must be tokenized before any LLM call. The pipeline is Textract → Comprehend Medical → Macie → Lambda tokenizer → HealthLake. Skipping this step is a HIPAA violation. Never pass raw PHI to a general-purpose LLM endpoint.
- **Pilot scope creep:** The 3-use-case / 90-day / measurable KPI rule is a hard constraint. Presenting more than 3 use cases for a first pilot is not conservative — it is a project failure pattern (fewer than 10% of gen AI pilots pass when KPI baselines aren't set, per McKinsey 2025).
- **Missing RAI stage gates:** Do not declare architecture complete without flagging governance gates for regulated-industry or consumer-facing use cases. RAI review is not a post-deployment audit — it belongs at the Measure stage.

---

## Known gaps

- **Azure-native deep-dive**: The bundle covers Azure at pattern level (Purview, Copilot Studio, Azure AI Foundry, Power Platform) but does not include a full Tier 1 platform architecture for Azure. Healthcare or FSI clients on Azure should supplement with Microsoft Responsible AI Standard v2 and Azure Compliance Manager documentation.
- **Retail/CPG and Manufacturing Tier 2 blueprints**: Only Prior Authorization (Healthcare) and Enterprise AI Data Catalog (Cross-Industry) have full four-tier chains. Retail personalization and manufacturing predictive maintenance have Tier 3 cards only; Solution Blueprints are pending.
- **Fine-tuning and RLHF patterns**: The bundle focuses on RAG, Knowledge Graph + MCP, Document AI, and multi-agent orchestration. Fine-tuning / RLHF / model adaptation is not covered.
- **Cost modeling at scale**: Directional cost estimates are included for realization patterns but not full TCO models for enterprise platform architectures.
