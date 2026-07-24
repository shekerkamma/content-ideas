---
status: reviewed
use_case: "Doc Summarization / Drafting"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Doc Summarization / Drafting Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** ops, legal, and knowledge-work teams that need summaries and
first drafts from messy source docs.

**Later ICPs:** adjacent analyst and coordinator teams once one document class
proves the summary-to-draft loop.

**Pain wedge:** teams need a summary and a useful next draft, but the source
docs are dense and time-consuming to read.

**Incumbent weakness:** generic summarizers miss task-specific structure and
citations.

**Agentic disruption thesis:** ingest a doc set, summarize with citations, and
draft the next artifact.

**Why now:** long-context models can handle more of the source in one pass.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 26/30**

The score is inferred from repeated drafting work, document overload, and the
need for source-grounded summaries.

- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 9/10

**Who has the problem:** knowledge workers with dense docs and repetitive
drafting.

**Current workaround:** manual reading, copy / paste, and templates.

**Switching reason:** faster comprehension and first-draft generation.

**Payment signal:** productivity software and labor time.

**30-day reachability:** one document type and one target draft can prove the
wedge.

**Verdict: PROCEED, but keep the task shape explicit.**

## 2. The 30-Day Scope Definition

**Project name:** Doc Summarize + Draft Copilot

**Validated problem:** teams need a fast summary plus a useful next draft.

**Target user:** analyst, associate, or coordinator.

**Core hypothesis:** the agent can produce a source-grounded summary and a
draft artifact.

### In Scope

1. **Document ingest**
   - Acceptance criterion: one document set is indexed and chunked.
2. **Summarization**
   - Acceptance criterion: the agent produces a cited summary.
3. **Draft generation**
   - Acceptance criterion: the agent generates the next artifact from the
     summary.

### Explicitly Out Of Scope

- General-purpose writing assistant.
- Replacing the source repository.
- Full legal review automation.
- Unbounded document corpus in v1.

### Week-By-Week Milestones

- **Week 1:** ingest one document type and define draft template.
- **Week 2:** build cited summarization.
- **Week 3:** draft the next artifact.
- **Week 4:** pilot with one workflow and review edits.

**Dependencies:** source docs, template, and reviewer.

**Acceptance test:** a user can go from raw docs to a usable draft in one
session.

**Top risks:** weak citations, hallucinated structure, and doc variability.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: drafting workspace.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for doc chunks.
- Auth: SSO plus document access control.
- Database: Postgres for documents, summaries, drafts, and feedback.
- Observability: OpenTelemetry and document lineage.
- Hosting: cloud app with queue worker.

**Architecture:** doc ingest -> chunking -> summarize -> draft -> review. The
agent uses the summary to produce a task-specific draft.

**Critical design decisions:**

1. Keep source docs and drafts linked by citations.
2. Make the draft template explicit for each workflow.
3. Keep human review in the loop.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/docs/ingest` | ingest docs | file bundle | ack | service token | retry queue |
| POST | `/api/docs/summarize` | summarize docs | doc_set_id | cited summary | service token | fallback to outline |
| POST | `/api/docs/draft` | draft next artifact | summary_id, template | draft artifact | service token | fallback to summary only |

### Folder / Module Structure

- `app/docs/`
- `app/api/docs/`
- `services/ingest/`
- `services/summarize/`
- `services/draft/`
- `lib/templates/`

### Environment Variables

- `DOC_SOURCE_TOKEN`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `EXPORT_BUCKET`
- `SSO_JWT_SECRET`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Document repository | low | already exists | BUY | source of truth already exists |
| Summarization | medium | generic tools miss structure | BUILD | core wedge |
| Draft generation | medium | copy / paste burden | BUILD | high leverage |

**Bottom line:** reuse the document source and build the summarization / draft
layer.

## 5. MVP ROI Business Case

**Current-state cost model:** reading time, drafting time, and template churn.

**Agentic MVP cost model:** ingest, model usage, review, and storage.

**Pricing options:**

1. Fixed pilot.
2. Per document set.
3. Enterprise productivity bundle.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low document repeatability | 12-18 months | month 14+ | narrower use |
| Base | one doc class, cited summary | 6-9 months | month 8-12 | strong fit |
| Upside | repeated drafting workflow | 3-5 months | month 4-6 | strong leverage |

**Formulas**

```text
Monthly value =
  reading time saved + drafting time saved + rework reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if the documents are too heterogeneous to cite reliably,
stay in summary-only mode.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Qvidian | RFP / proposal | workflow depth | admin burden | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/DocSummarizationDrafting_Competitor_Teardown.md` |
| Seismic | sales enablement | content management | modular and expensive | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/DocSummarizationDrafting_Competitor_Teardown.md` |
| Highspot | sales enablement | analytics and tracking | heavy pricing | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/DocSummarizationDrafting_Competitor_Teardown.md` |
| Conga | document generation | Salesforce integration | setup complexity | module / seat pricing | `runs/2026-06-26-agentic-opportunity-blueprints/source/DocSummarizationDrafting_Competitor_Teardown.md` |

**Direct threats:** Conga and Qvidian.

**What not to build:** a new CRM or content library.

**Agentic wedge:** summarize with citations, then draft the next artifact
directly from source docs and CRM context.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| cited summary | doc set loaded | summarize runs | citations present | replay test |
| next draft | summary ready | draft runs | artifact follows template | diff test |
| missing source | doc missing | draft runs | user sees limitation | negative test |

### Edge Cases

- Conflicting source docs.
- Missing citations.
- Draft template absent.
- Large doc set.
- Invalid upload.
- Tenant isolation.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| docs | source repository | document store | source system | batch / realtime | checksum |
| summaries | agent | summary table | agent | realtime | citation required |
| drafts | agent | draft table | agent | realtime | template validation |
| feedback | reviewer | feedback table | reviewer | realtime | immutable log |

**Retention and deletion:** retain citations and draft lineage, delete
transient prompts after retention, and keep source / summary mapping.

**Privacy/security:** document access control and tenant isolation.

**Analytics questions:** which document classes need the most drafting
correction and which sources create the most weak citations?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one document type, draft template, reviewer path,
rollback flag.

**Staging:** summarization-only, then draft mode.

**Production sequence:** one workflow, one owner, one review queue.

**Smoke test:** one summary and one draft generated from the same doc set.

**Rollback:** disable draft generation and keep summary-only mode.

**Observability:**

- Logs: doc set, citation, summary, draft version.
- Metrics: summary quality, draft edit rate, time saved.
- Alerts: missing citations, template failure, upload failure.
- Dashboards: workflow completion and edit hotspots.

## 10. Post-Launch Iteration Plan

**Metrics:** time saved, repeat use, and review edit rate.

**Week-by-week:**

- Week 1: add another document type.
- Week 2: improve citation quality.
- Week 3: tighten draft templates.
- Week 4: package for adjacent workflows.

**Pivot signals:** keep it summary-only if citations fail, constrain templates
if structure drifts, and add more workflow specificity if the product is used
as generic summarization.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Doc_Summarization_Drafting_Disruptive_Teardown.md` - upstream teardown dossier for the summarization/drafting wedge.
- Official reference points reviewed: Notion, Microsoft Copilot, Google Gemini, Grammarly, and Writer product pages.
- `runs/2026-06-26-agentic-opportunity-blueprints/source/DocSummarizationDrafting_Competitor_Teardown.md` - proposal/document incumbent map and summary-to-draft wedge.
