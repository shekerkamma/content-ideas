---
status: reviewed
use_case: "Enterprise Knowledge Search"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Enterprise Knowledge Search Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** internal knowledge, IT, and enablement leaders.

**Later ICPs:** support and employee-experience teams once one knowledge domain
proves the search-to-answer loop.

**Pain wedge:** enterprise knowledge is scattered across docs, wikis, tickets,
and chat.

**Incumbent weakness:** search tools return results, but users still need to
stitch together answers.

**Agentic disruption thesis:** search, synthesize, cite, and answer in one
workflow.

**Why now:** teams have too many systems of record and too little retrieval
quality.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

The score is inferred from enterprise search spend, content-rot complaints, and
the obvious friction in cross-silo retrieval.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** employees and support teams needing fast answers.

**Current workaround:** search boxes, Slack questions, and tribal knowledge.

**Switching reason:** faster answers and reduced context switching.

**Payment signal:** search, knowledge, and collaboration budgets.

**30-day reachability:** one knowledge domain and one source boundary can prove
value.

**Verdict: PROCEED, but keep the first domain narrow.**

## 2. The 30-Day Scope Definition

**Project name:** Answer Copilot

**Validated problem:** users need answers with citations, not just search
results.

**Target user:** employee or support agent.

**Core hypothesis:** the agent can answer a narrow class of questions with
cited sources.

### In Scope

1. **Native connectors**
   - Acceptance criterion: Drive, Slack, and Jira are indexed with permissions.
2. **Answer synthesis**
   - Acceptance criterion: the agent returns a concise answer with citations.
3. **Escalation / fallback**
   - Acceptance criterion: unresolved questions route to the correct source.

### Explicitly Out Of Scope

- Building another wiki or database.
- Manual content migration.
- Full company-wide search replacement in v1.
- Knowledge ownership by the agent.

### Week-By-Week Milestones

- **Week 1:** connect one knowledge domain and source boundary.
- **Week 2:** build connectors and permissions trimming.
- **Week 3:** synthesize answers with citations.
- **Week 4:** pilot with one support or employee workflow.

**Dependencies:** source connectors, RBAC, and a knowledge owner.

**Acceptance test:** a user gets a cited answer without manually jumping across
systems.

**Top risks:** permissions leakage, content rot, and weak relevance.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: search / answer console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for docs, tickets, and chat.
- Auth: SSO plus connector credentials.
- Database: Postgres for sources, answer logs, citations, and feedback.
- Observability: OpenTelemetry and search metrics.
- Hosting: cloud app with queue worker.

**Architecture:** connectors -> permission trim -> retrieve -> synthesize ->
cite -> answer / fallback. The agent should answer directly from the live data
layer.

**Critical design decisions:**

1. Do not build a new knowledge database.
2. Preserve document-level permissions.
3. Make citations mandatory for every answer.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/search/index` | index sources | source bundle | index status | service token | retry queue |
| POST | `/api/search/answer` | answer a question | question, source scope | cited answer | session JWT | fallback to search |
| POST | `/api/search/feedback` | capture response quality | answer_id, rating | ack | session JWT | 400 on invalid id |

### Folder / Module Structure

- `app/search/`
- `app/api/search/`
- `services/connectors/`
- `services/retrieve/`
- `workers/indexing/`
- `lib/rbac/`

### Environment Variables

- `CONNECTOR_TOKEN`
- `VECTOR_STORE_URL`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `SSO_JWT_SECRET`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Search connectors | medium | Glean / Coveo / Guru expensive | BUY / HYBRID | existing connectors help |
| Answer synthesis | medium | search tools still return results | BUILD | core wedge |
| Citation / fallback | medium | manual stitching is the pain | BUILD | high leverage |

**Bottom line:** buy connector breadth where possible and build answer
synthesis.

## 5. MVP ROI Business Case

**Current-state cost model:** search time, Slack interruptions, and content
maintenance.

**Agentic MVP cost model:** connector ingestion, model usage, storage, and
support.

**Pricing options:**

1. Per domain.
2. Consumption-based access.
3. Enterprise package with connectors and analytics.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | content rot persists | 12-18 months | month 14+ | needs governance |
| Base | one domain, cited answers | 6-9 months | month 8-12 | strong fit |
| Upside | multiple teams adopt | 3-5 months | month 4-6 | strong leverage |

**Formulas**

```text
Monthly value =
  search time saved + fewer Slack interrupts + support deflection
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if permissions cannot be trimmed correctly, do not ship.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Glean | workplace search | strong modern UX | per-seat cost and integrations | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/EnterpriseKnowledgeSearch_Competitor_Teardown.md` |
| Coveo | enterprise search | scale and governance | heavy implementation | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/EnterpriseKnowledgeSearch_Competitor_Teardown.md` |
| Guru | knowledge management | system of record for policies | content rot / admin burden | per-seat | `runs/2026-06-26-agentic-opportunity-blueprints/source/EnterpriseKnowledgeSearch_Competitor_Teardown.md` |
| Elastic Enterprise Search | developer-focused | customizable | engineering-heavy | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/EnterpriseKnowledgeSearch_Competitor_Teardown.md` |

**Direct threats:** Glean and Coveo.

**What not to build:** another wiki or database.

**Agentic wedge:** kill the per-seat tax, eliminate content rot, and deploy via
one-click connectors.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| answer with citations | question arrives | agent runs | cited answer returned | replay test |
| permissions trim | confidential doc exists | search runs | unauthorized user does not see it | access test |
| fallback | answer unknown | search runs | user gets the right source path | scenario test |

### Edge Cases

- Empty domain.
- Permission denied.
- Stale content.
- Duplicate answers.
- Search source outage.
- Tenant isolation.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| docs | Drive / wiki | document store | source system | batch / realtime | checksum |
| tickets | help desk | ticket table | help desk | realtime | RBAC trim |
| chats | Slack | chat store | Slack | realtime | access policy |
| answers | agent | answer log | agent | realtime | citation required |

**Retention and deletion:** retain answer logs and citations, delete transient
prompts after retention, and keep source lineage.

**Privacy/security:** strict permissions trimming, tenant isolation, and no
surface of confidential docs to unauthorized users.

**Analytics questions:** which domains have the most unanswered questions and
which sources generate the most stale answers?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one domain, one connector set, RBAC policy, rollback
flag.

**Staging:** index-only, then answer-only.

**Production sequence:** one domain, one workflow, one owner.

**Smoke test:** one answer with citations and permission trimming.

**Rollback:** disable answer synthesis and fall back to indexed search.

**Observability:**

- Logs: source, question, citation, access outcome.
- Metrics: answer rate, citation rate, fallback rate.
- Alerts: permission leak, connector failure, content rot spike.
- Dashboards: unanswered questions and stale content hotspots.

## 10. Post-Launch Iteration Plan

**Metrics:** time to answer, repeat use, and search deflection.

**Week-by-week:**

- Week 1: expand one more source boundary.
- Week 2: improve citation quality.
- Week 3: add better permissions trimming.
- Week 4: package for adjacent teams.

**Pivot signals:** keep it domain-specific if breadth hurts quality, tighten
connector scope if permission leaks appear, and treat content rot as a source
governance problem.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/EnterpriseKnowledgeSearch_Competitor_Teardown.md` - enterprise-search incumbent map and answer-synthesis wedge.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Enterprise_Knowledge_Search_Disruptive_Teardown.md` - upstream teardown dossier for the enterprise-search wedge.
- Official reference points reviewed: Glean, Coveo, Elastic, Guru, and Microsoft Search product pages.
