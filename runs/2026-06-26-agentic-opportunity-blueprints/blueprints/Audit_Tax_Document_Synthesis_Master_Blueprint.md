---
status: reviewed
use_case: "Audit and Tax Document Synthesis"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence: high
---

# Audit and Tax Document Synthesis Master Implementation Blueprint

## Executive Positioning
- Target buyer: accounting, tax, and audit teams.
- Pain wedge: receipt and document triage is still a manual shoebox problem.
- Incumbent weakness: OCR and expense tools capture data, but tax schedules still need synthesis.
- Agentic disruption thesis: extract, categorize, and route documents into audit-ready structures.
- Why now: seasonal workload and labor cost make automation valuable.

## 1. Problem-Solution Fit Diagnostic
Score 28/30
- Problem realness: 10/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

Evidence:
- Who has the problem: tax professionals and auditors.
- Last-time/recency evidence: OCR and AP automation tools are common.
- Current workaround: manual sorting and spreadsheet entry.
- Switching reason: lower per-document cost and faster prep.
- Payment signal: accounting software and seasonal labor.
- 30-day reachability: one document class and one schedule mapping can prove the wedge.

Verdict: PROCEED

## 2. 30-Day Scope Definition
- Project name: Tax Doc Copilot
- Validated problem: receipts and PDFs need structured tax outputs.
- Target user: accountant or tax preparer.
- Core hypothesis: the agent can classify docs and map them to tax categories with review.

In scope:
1. PDF/receipt ingest.
2. Field extraction and category mapping.
3. HITL queue for illegible docs.

Explicitly out of scope:
- Replacing tax software.
- Final filing or tax advice.
- Full bookkeeping suite.

Week-by-week milestones:
- Week 1: cloud infra and parsing.
- Week 2: extraction and Pydantic structuring.
- Week 3: review UI.
- Week 4: historical parallel run and production deployment.

Dependencies:
- intake bucket, category map, and review workflow.

Acceptance test:
- standard receipts map to categories with high accuracy and exceptions are routed.

Top 3 risks + mitigations:
- illegible docs - HITL queue
- category drift - versioned tax map
- PII risk - masking and encryption

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend: review dashboard.
- Backend: Python FastAPI.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres plus blob store.
- Auth: accounting SSO.
- Database: Postgres for docs, categories, and audit.
- Observability: confidence and throughput metrics.
- Hosting: AWS ECS or similar secure backend.

Architecture:
- System boundary: intake -> extract -> classify -> review -> export.
- Runtime topology: PDF bucket -> EventBridge trigger -> agent -> encrypted DB.
- Core agent loop: extract data, classify, map schedule, flag low confidence.
- Human-in-the-loop points: illegible docs and uncommon categories.
- Integration endpoints: S3, tax schedules, accounting export.
- Failure handling: if extraction fails, route to review instead of guessing.

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|
| documents | source files | id, tenant_id, uri, hash, doc_type | tenant_id, doc_type | tenant-scoped |
| extracted_fields | parsed data | id, doc_id, field, value, confidence | doc_id, field | encrypted |
| classifications | tax mapping | id, doc_id, category, confidence | doc_id, category | reviewer gated |
| reviews | HITL queue | id, doc_id, reviewer, status | doc_id, status | immutable |

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | /api/documents | upload docs | file | doc_id | user auth | 400 on invalid file |
| POST | /api/documents/{id}/classify | classify | doc_id | categories | service auth | partial with review |
| POST | /api/documents/{id}/review | review item | decision | ack | user auth | 409 if stale |

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|
| S3/bucket | inbound | document intake | service token | retry and hash |
| accounting export | outbound | schedule payload | API token | queue if failed |
| review UI | outbound | HITL task | app auth | preserve state |

Folder/module structure:
- `app/api/`
- `services/ingest/`
- `services/extract/`
- `services/classify/`
- `services/review/`

Environment variables:
- `DOC_BUCKET`
- `EXPORT_API_TOKEN`
- `REVIEW_ROLE`
- `CATEGORY_MAP_PATH`
- `LLM_API_KEY`

Critical design decisions:
1. Versioned category map because tax rules change.
2. HITL for illegible docs because uncertainty must not be hidden.
3. Blob intake and encrypted DB because PII is sensitive.

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| document synthesis | moderate | OCR/RPA is brittle | Build | tax mapping is the wedge |
| accounting export | low | existing | Buy/Reuse | keep system of record |
| storage | low | existing | Buy/Reuse | use secure blobs |

Bottom line:
- Annual SaaS spend if buying: OCR and tax prep tools.
- One-time MVP build estimate: $40k-$80k equivalent effort.
- Recommended split: buy export/storage, build synthesis worker.
- Payback period: under 12 months if seasonal labor falls.

## 5. MVP ROI Business Case
Current-state cost model:
- Software: OCR and tax tools.
- Labor: seasonal staff time.
- Services/admin: manual sorting.
- Error/rework: miscategorized docs.

Agentic MVP cost model:
- Build: one ingest/classify pipeline.
- Monthly run: OCR and model usage.
- Maintenance: tax map updates.

Pricing options:
1. Low-risk pilot: one category set.
2. Usage/outcome model: per document.
3. Enterprise package: synthesis plus audit trail.

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Base | 96% cost reduction per doc | 6-10 months | month 8-12 | standard |
| Upside | big seasonal volume | 3-6 months | month 4-6 | strong fit |
| Downside | messy docs | 12-18 months | month 14+ | more review |

No-go condition: if category mappings cannot be versioned, the output is too risky.

## 6. Competitor Product Teardown
Competitor map:
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| ABBYY | OCR | established | rigid | enterprise | product page |
| Expensify | expense capture | easy | not tax-ready | seat-based | product page |
| legacy RPA | automation | flexible | breaks on format change | services | market standard |

Direct threats:
- OCR
- expense capture
- RPA

Table-stakes features to copy:
- extraction
- category mapping
- review queue

Things not to build:
- tax software replacement
- bookkeeping suite
- filing automation

Three exploitable gaps:
- shoebox triage
- category versioning
- PII handling

## 7. Acceptance Criteria + Test Plan
Feature test plan:
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| receipt ingest | standard receipt | pipeline runs | fields extracted | fixture test |
| illegible doc | blurry image | pipeline runs | review queued | negative test |
| category map | doc set | classify runs | correct schedule set | human baseline |

Edge cases:
- Empty state: no docs uploaded.
- Error state: unreadable file rejected.
- Invalid input: unsupported format.
- Slow dependency: queue remains pending.
- Concurrent action: duplicate doc idempotent.
- Auth/data boundary: tenant isolation.

## 8. Data Architecture Lite
Data domains:
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| documents | upload | blob store | source | realtime | hash check |
| fields | agent | field table | agent | realtime | confidence threshold |
| classifications | agent | class table | tax map | versioned | review state |
| reviews | accountant | review table | reviewer | realtime | immutable log |

Retention and deletion:
- Data retained: approved classifications and audit trail.
- Data deleted: transient prompts and temp OCR artifacts.
- Audit retained: document lineage.

Analytics questions:
1. Which document types most often require manual review?

Privacy/security:
- PII masking
- encrypted storage
- review only for low confidence

## 9. Deployment Sequencing
Pre-deploy checklist:
- bucket ready
- category map loaded
- review UI approved

Staging:
- historical parallel run.

Production sequence:
- shadow -> review-only -> live classification.

Smoke test:
- one receipt maps correctly.

Rollback:
- disable classification and keep manual review.

Observability:
- Logs: doc, field, category, review.
- Metrics: extraction accuracy, queue time, throughput.
- Alerts: OCR failure, category miss, export error.
- Dashboards: by document class.

## 10. Post-Launch Iteration Plan
Metrics:
- Activation: docs processed.
- Retention: repeat seasonal use.
- Revenue/willingness-to-pay: hours saved and cost reduced.

Week-by-week:
- Week 1: add more doc types.
- Week 2: improve category mapping.
- Week 3: add reconciliation.
- Week 4: expand to bank statement matching.

Pivot signals:
- if docs are too messy, narrow to receipts only
- if review queue is too large, keep assistive
- if tax map changes often, increase version control

## Source Notes
- ABBYY - https://www.abbyy.com/ - accessed 2026-06-26 - OCR backdrop.
- Expensify - https://www.expensify.com/ - accessed 2026-06-26 - expense capture backdrop.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Audit_Tax_Document_Synthesis_Disruptive_Teardown.md` - incumbent map and document synthesis wedge.
- CCH ProSystem fx - https://www.wolterskluwer.com/en/solutions/cch-prosystem-fx - accessed 2026-06-26 - integrated tax and accounting software reference.
- Intuit homepage - https://www.intuit.com/ - accessed 2026-06-26 - tax and accounting ecosystem backdrop.
- Drake Software homepage - https://www.drakesoftware.com/ - accessed 2026-06-26 - tax preparer software reference.
- GruntWorx homepage - https://www.gruntworx.com/ - accessed 2026-06-26 - cloud tax workflow and workpaper automation reference.
- These incumbents reinforce that the wedge is document synthesis and workpaper prep, not a tax engine or filing product.
