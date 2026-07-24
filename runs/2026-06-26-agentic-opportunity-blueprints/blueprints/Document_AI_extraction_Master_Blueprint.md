---
status: reviewed
use_case: "Document AI Extraction"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence: high
---

# Document AI Extraction Master Implementation Blueprint

## Executive Positioning
- Target buyer: AP, ops, and back-office leaders processing invoices, forms, and contracts.
- Pain wedge: manual keying is slow, and template OCR misses nuance.
- Incumbent weakness: OCR suites are rigid and page-centric.
- Agentic disruption thesis: extract structured data from messy documents and route it to the system of record.
- Why now: large-context models plus OCR pipelines can outperform template-only capture on messy docs.

## 1. Problem-Solution Fit Diagnostic
Score 27/30
- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

Evidence:
- Who has the problem: AP, operations, logistics, and legal ops teams.
- Last-time/recency evidence: document processing happens continuously.
- Current workaround: manual keying and spreadsheets.
- Switching reason: lower keying cost and fewer errors.
- Payment signal: OCR and document processing software budgets.
- 30-day reachability: one document class and one destination system can prove the wedge.

Verdict: PROCEED

## 2. 30-Day Scope Definition
- Project name: Doc Extract Copilot
- Validated problem: documents need structured fields, not text blobs.
- Target user: operations analyst or AP clerk.
- Core hypothesis: the agent can extract fields and route exceptions without manual data entry.

In scope:
1. Document ingest.
2. Field extraction.
3. Exception queue.

Explicitly out of scope:
- Full BPM suite.
- Document storage replacement.
- Autonomous financial posting without review.

Week-by-week milestones:
- Week 1: OCR and upload.
- Week 2: extraction schema and confidence rules.
- Week 3: exception UI.
- Week 4: connect to one system of record.

Dependencies:
- document types, destination system, and review workflow ownership.

Acceptance test:
- structured fields are extracted accurately on a test corpus with exception handling.

Top 3 risks + mitigations:
- OCR errors - fallback parsing
- template variation - confidence thresholds
- bad writes - review gate

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend: validation UI built in Next.js.
- Backend: Python FastAPI.
- Agent orchestration: extraction pipeline plus LLM vision assist.
- Retrieval/data layer: object store + Postgres.
- Auth: SSO and service credentials.
- Database: Postgres for documents, fields, exceptions, and downstream writes.
- Observability: OCR quality and extraction metrics.
- Hosting: secure cloud environment or buyer VPC.

Architecture:
- System boundary: ingest -> OCR -> extract -> validate -> push.
- Runtime topology: file upload -> text extraction -> field mapping -> exception queue.
- Core agent loop: identify document type, pull fields, confidence gate, send downstream.
- Human-in-the-loop points: low-confidence fields and unsupported forms.
- Integration endpoints: storage, ERP/CRM/AP systems, review UI.
- Failure handling: if extraction is weak, mark the field unresolved rather than guessing.

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|
| documents | source files | id, tenant_id, doc_type, uri, hash | tenant_id, doc_type | tenant-scoped |
| fields | extracted output | id, doc_id, field_name, value, confidence | doc_id, field_name | approval gated |
| exceptions | review items | id, doc_id, reason, status | doc_id, status | audit tracked |
| writes | downstream updates | id, doc_id, system_ref, status | doc_id | immutable |

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | /api/documents | upload doc | file | doc_id | user auth | 400 on invalid file |
| POST | /api/documents/{id}/extract | extract fields | doc_id | fields | service auth | partial with exceptions |
| POST | /api/documents/{id}/push | push downstream | doc_id | status | service auth | queue on outage |

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|
| storage | inbound | doc upload | service token | retry and hash check |
| ERP/CRM/AP | outbound | structured fields | API token | queue if unavailable |
| review UI | outbound | exception review | app auth | preserve state |

Folder/module structure:
- `app/(console)/docs/`
- `app/api/documents/`
- `services/ocr/`
- `services/extract/`
- `services/validate/`
- `services/push/`

Environment variables:
- `DOC_BUCKET`
- `TARGET_API_TOKEN`
- `OCR_PROVIDER_KEY`
- `EXCEPTION_THRESHOLD`
- `REVIEW_ROLE`

Critical design decisions:
1. Field confidence and exception queue because silence is dangerous.
2. Keep destination systems because the agent is a worker, not the system of record.
3. Support one document class first, then expand only after the first class is stable.

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| document extraction | moderate | OCR suites are rigid and costly | BUILD | messy-doc handling is the wedge |
| downstream system | low | already installed | BUY | keep SoR |
| storage | low | commodity | BUY/REUSE | no need to replace |

Bottom line:
- Annual SaaS spend if buying: OCR and document AI tools.
- One-time MVP build estimate: $40k-$80k equivalent effort.
- Recommended split: buy storage and destination systems, build extraction worker.
- Payback period: under 12 months if manual keying falls.

## 5. MVP ROI Business Case
Current-state cost model:
- Software: OCR/document tools.
- Labor: manual keying time.
- Services/admin: QA and corrections.
- Error/rework: downstream data errors.

Agentic MVP cost model:
- Build: one extraction pipeline.
- Monthly run: OCR and model usage.
- Maintenance: schema and form updates.

Pricing options:
1. Low-risk pilot: one document class.
2. Usage/outcome model: per document extracted.
3. Enterprise package: extraction plus workflow.

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Base | fewer manual keying hours | 6-10 months | month 8-12 | standard |
| Upside | high document volume | 3-6 months | month 4-6 | strong fit |
| Downside | messy scans | 12-18 months | month 14+ | needs human review |

No-go condition: if document quality is too poor, the product becomes a cleanup tool only.

## 6. Competitor Product Teardown
Competitor map:
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| ABBYY | IDP/OCR | established enterprise capture | template-bound and expensive | page/capacity based | `source/DocumentAI_Competitor_Teardown.md` |
| Kofax | capture | legacy enterprise footprint | heavy setup and maintenance | enterprise sales-led | `source/DocumentAI_Competitor_Teardown.md` |
| IBM Datacap | capture | legacy integration | rigid capture workflows | enterprise sales-led | `source/DocumentAI_Competitor_Teardown.md` |
| Ephesoft | capture | document workflow history | setup and tuning burden | sales-led | `source/DocumentAI_Competitor_Teardown.md` |

Direct threats: ABBYY and Kofax. Table stakes: structured output, confidence scores, secure handling. Things not to build: ERP replacement or downstream system replacement. Gaps: zero-template extraction, instant onboarding, and handling unstructured chaos.

## 7. Acceptance Criteria + Test Plan
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| extraction | scanned doc | pipeline runs | fields captured | fixture test |
| low confidence | ambiguous field | pipeline runs | exception created | negative test |
| push | approved fields | push runs | destination updated | integration test |

Edge cases:
- empty state
- OCR failure
- unsupported file rejected
- slow dependency
- duplicate doc idempotent
- tenant isolation

## 8. Data Architecture Lite
Data domains:
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| docs | upload | blob store | source | realtime | hash check |
| fields | agent | field table | agent | realtime | confidence threshold |
| exceptions | agent | exception table | review | realtime | approval state |
| writes | system | write table | destination | realtime | status check |

Retention and deletion:
- Data retained: extraction metadata and audit logs.
- Data deleted: transient OCR intermediates after retention.
- Audit retained: field lineage, confidence, and approval trail.

Analytics questions:
1. Which document classes have the most exceptions?
2. Which fields fail most often?
3. What is the cost per extracted document?

Privacy/security:
- Documents often contain PII/financial data; enforce tenant isolation, encryption, minimum necessary access, and retention limits.

## 9. Deployment Sequencing
Pre-deploy checklist:
- confirm document class
- confirm downstream system
- confirm review owner

Staging:
- run on a test corpus
- verify confidence thresholds and exceptions

Production sequence:
- start with draft extraction and exception routing only
- expand downstream writes after accuracy stabilizes

Smoke test:
- upload, extract, review, push

Rollback:
- disable downstream writes, preserve audit

Observability:
- Logs: file hash, OCR pass, extraction version.
- Metrics: field accuracy, exception rate, latency.
- Alerts: OCR failure and confidence drops.
- Dashboards: doc classes, exceptions, and downstream writes.

## 10. Post-Launch Iteration Plan
Metrics:
- Activation: percent of docs extracted.
- Retention: weekly analyst usage and repeat upload volume.
- Revenue/willingness-to-pay: paid pilot extension or per-document contract.

Week-by-week:
- Week 1: fix OCR and schema gaps.
- Week 2: improve confidence thresholds.
- Week 3: add one document class.
- Week 4: measure manual keying reduction.

Pivot signals:
- if document quality is consistently poor or exception volume is too high, narrow to cleanup and routing.

## Source Notes
- `runs/2026-06-26-agentic-opportunity-blueprints/source/DocumentAI_Competitor_Teardown.md` - internal teardown and incumbent mapping.
- `source/Agent_Use_Cases_Phase1.md` - use-case scorecard and scope.
- `source/original-10-skill-stack.txt` - prompt lineage.
- Google Cloud Document AI - https://cloud.google.com/document-ai - accessed 2026-06-26 - developer-facing document parsing and extraction platform.
- Amazon Textract - https://aws.amazon.com/textract/ - accessed 2026-06-26 - OCR and structured extraction reference.
- Azure Document Intelligence - https://azure.microsoft.com/en-us/products/ai-foundry/tools/document-intelligence - accessed 2026-06-26 - document intelligence and extraction reference.
- ABBYY - https://www.abbyy.com/ - accessed 2026-06-26 - incumbent IDP/OCR reference.
