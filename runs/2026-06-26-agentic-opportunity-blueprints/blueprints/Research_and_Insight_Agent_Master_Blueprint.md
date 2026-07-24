---
status: reviewed
use_case: "Research and Insight Agent"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Research and Insight Agent Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** strategy, product, and research teams.

**Later ICPs:** adjacent planning teams once one corpus proves the brief loop.

**Pain wedge:** teams need a synthesized briefing, not another search box.

**Incumbent weakness:** research tools store notes but do not create decision-
ready briefs.

**Agentic disruption thesis:** synthesize a question into a structured insight
memo from approved sources.

**Why now:** market-research tools are expensive, and general copilots are not
source-governed.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 26/30**

The score is inferred from recurring research work, expensive portals, and the
manual synthesis bottleneck.

- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 9/10

**Who has the problem:** teams doing recurring competitive or market research.

**Current workaround:** manual note synthesis and slide writing.

**Switching reason:** faster brief generation and fewer manual steps.

**Payment signal:** research tools and analyst hours.

**30-day reachability:** one corpus and one brief template can prove the wedge.

**Verdict: PROCEED, but keep the corpus governed.**

## 2. The 30-Day Scope Definition

**Project name:** Insight Brief Copilot

**Validated problem:** research has to become an answer, not just notes.

**Target user:** analyst or strategist.

**Core hypothesis:** the agent can synthesize a brief with citations and
takeaways.

### In Scope

1. **Corpus ingest**
   - Acceptance criterion: approved sources are loaded and indexed.
2. **Synthesis**
   - Acceptance criterion: the agent produces a decision-ready memo.
3. **Brief template**
   - Acceptance criterion: the output follows the requested structure.

### Explicitly Out Of Scope

- Proprietary data vendor.
- Survey collection engine.
- Uncited synthesis.
- Unbounded open-web research in v1.

### Week-By-Week Milestones

- **Week 1:** ingest one corpus and one brief template.
- **Week 2:** build citations and source trimming.
- **Week 3:** synthesize the memo.
- **Week 4:** pilot with one strategy or research team.

**Dependencies:** approved corpus, source policy, and reviewer.

**Acceptance test:** a user can ask a question and receive a cited memo with
takeaways.

**Top risks:** source drift, weak citation mapping, and noisy briefs.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: memo workspace.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for corpus and notes.
- Auth: SSO plus source-system permissions.
- Database: Postgres for sources, memos, citations, feedback.
- Observability: OpenTelemetry and brief quality logs.
- Hosting: cloud app with queue worker.

**Architecture:** approved corpus -> retrieve -> synthesize -> cite -> brief.
The agent is a synthesis layer on top of approved sources.

**Critical design decisions:**

1. Do not become a proprietary data vendor.
2. Keep exact citation mapping mandatory.
3. Keep the corpus governed and source-governed.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/research/index` | index sources | corpus bundle | index status | service token | retry queue |
| POST | `/api/research/brief` | synthesize memo | question, corpus scope | insight brief | session JWT | fallback to outline |
| POST | `/api/research/feedback` | capture brief quality | brief_id, rating | ack | session JWT | 400 on invalid id |

### Folder / Module Structure

- `app/research/`
- `app/api/research/`
- `services/index/`
- `services/synthesize/`
- `workers/briefs/`
- `lib/citations/`

### Environment Variables

- `CORPUS_TOKEN`
- `VECTOR_STORE_URL`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `SSO_JWT_SECRET`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Research portals | high | AlphaSense / Qualtrics expensive | BUY / REUSE | not the wedge |
| Brief synthesis | medium | human synthesis is the pain | BUILD | core wedge |
| Citation mapping | medium | required for trust | BUILD | high leverage |

**Bottom line:** reuse approved corpora and build synthesis.

## 5. MVP ROI Business Case

**Current-state cost model:** analyst hours, research-tool seats, and brief
assembly.

**Agentic MVP cost model:** ingest, model usage, citations, review, and storage.

**Pricing options:**

1. Fixed pilot.
2. Per brief.
3. Enterprise research package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | narrow corpus | 12-18 months | month 14+ | learning only |
| Base | faster brief generation | 6-9 months | month 8-12 | strong fit |
| Upside | democratized insight access | 3-5 months | month 4-6 | strong leverage |

**Formulas**

```text
Monthly value =
  analyst time saved + brief turnaround reduced + seat cost avoided
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if citations cannot be mapped exactly, keep the output as
research notes only.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| AlphaSense | market intelligence | premium search | expensive per seat | $15k-$60k / seat cited | `runs/2026-06-26-agentic-opportunity-blueprints/source/Research_Insight_Competitor_Teardown.md` |
| Qualtrics | XM | data corpora | admin burden | $20k-$100k+ enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Research_Insight_Competitor_Teardown.md` |
| Gartner / Forrester | research portals | authority | paywalled / seat-gated | per-seat portal | `runs/2026-06-26-agentic-opportunity-blueprints/source/Research_Insight_Competitor_Teardown.md` |
| Medallia | XM | feedback data | synthesis bottleneck | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Research_Insight_Competitor_Teardown.md` |

**Direct threats:** AlphaSense and Qualtrics.

**What not to build:** a proprietary data vendor or survey engine.

**Agentic wedge:** automated synthesis, democratized seats, and cross-silo
context.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| brief synthesis | corpus loaded | agent runs | memo with citations returned | replay test |
| citation mapping | source question asked | agent runs | source links are exact | citation test |
| template fit | brief requested | synthesis runs | output matches structure | review test |

### Edge Cases

- Empty corpus.
- Conflicting sources.
- Weak citation.
- Large document set.
- Source outage.
- Tenant isolation.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| corpus | approved sources | document store | source system | batch / realtime | checksum |
| memos | agent | memo table | agent | realtime | citation required |
| citations | retrieval | citation table | source refs | realtime | exact mapping |
| feedback | reviewers | feedback table | reviewers | realtime | immutable log |

**Retention and deletion:** retain memo lineage and citations, delete
transient prompts after retention, and keep source scope controls.

**Privacy/security:** source-governed corpus and tenant isolation.

**Analytics questions:** which question types create the most synthesis edits
and which source classes produce the most weak citations?

## 9. Deployment Sequencing

**Pre-deploy checklist:** corpus approved, template chosen, reviewer assigned,
rollback flag.

**Staging:** index-only, then brief-only.

**Production sequence:** one corpus, one template, one review path.

**Smoke test:** ask one question and verify citations.

**Rollback:** disable synthesis and fall back to notes-only mode.

**Observability:**

- Logs: source, retrieval, citation, brief.
- Metrics: brief turnaround, citation rate, edit rate.
- Alerts: citation mismatch, source drift, corpus outage.
- Dashboards: unanswered questions and weak-source hotspots.

## 10. Post-Launch Iteration Plan

**Metrics:** brief turnaround, repeat use, and edit rate.

**Week-by-week:**

- Week 1: add a second corpus boundary.
- Week 2: improve citation quality.
- Week 3: tighten template fidelity.
- Week 4: package for adjacent teams.

**Pivot signals:** keep it source-governed if weak citations appear, and
expand only when the corpus and template stay stable.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Research_Insight_Disruptive_Teardown.md` - upstream teardown dossier for the research/insight wedge.
- Official reference points reviewed: AlphaSense, Qualtrics, SurveyMonkey, and Gong product pages.
- `runs/2026-06-26-agentic-opportunity-blueprints/source/Research_Insight_Competitor_Teardown.md` - market-research incumbent map and synthesis wedge.
