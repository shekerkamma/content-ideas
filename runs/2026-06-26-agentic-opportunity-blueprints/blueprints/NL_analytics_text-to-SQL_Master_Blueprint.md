---
status: reviewed
use_case: "NL Analytics (text-to-SQL)"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence: high
---

# NL Analytics (text-to-SQL) Master Implementation Blueprint

## Executive Positioning
- Target buyer: business teams, analytics leaders, and data platform owners.
- Pain wedge: users wait for dashboards for simple questions.
- Incumbent weakness: BI tools are seat-heavy and require analyst help.
- Agentic disruption thesis: translate natural language into validated SQL and return answers directly.
- Why now: warehouse access is standard, but query generation remains the bottleneck.

## 1. Problem-Solution Fit Diagnostic
Score 27/30
- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

Evidence:
- Who has the problem: teams asking ad hoc questions of the warehouse.
- Last-time/recency evidence: BI tooling remains expensive and slow.
- Current workaround: dashboard requests and analyst tickets.
- Switching reason: faster answers and reduced BI seat cost.
- Payment signal: BI licenses and analyst time.
- 30-day reachability: one warehouse and one semantic layer can prove the wedge.

Verdict: PROCEED

## 2. 30-Day Scope Definition
- Project name: Warehouse Query Copilot
- Validated problem: users need answers, not dashboards.
- Target user: business user or analyst.
- Core hypothesis: the agent can generate valid read-only SQL and explain ambiguous terms.

In scope:
1. Schema extraction and metadata tagging.
2. Text-to-SQL query generation.
3. Slack/Teams bot response.

Explicitly out of scope:
- Replacing the warehouse.
- Write queries in v1.
- Dashboard studio replacement.

Week-by-week milestones:
- Week 1: schema extraction and tagging.
- Week 2: query generation and tuning.
- Week 3: sanitization and visualization.
- Week 4: bot deployment.

Dependencies:
- warehouse access, semantic layer, and SSO.

Acceptance test:
- natural language questions convert into valid SQL and return correct results.

Top 3 risks + mitigations:
- ambiguous metrics - semantic layer
- query safety - read-only service account
- poor accuracy - clarification prompts

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend: Slack/Teams bot and lightweight web UI.
- Backend: Python service.
- Agent orchestration: LlamaIndex or LangChain.
- Retrieval/data layer: warehouse metadata plus semantic dictionary.
- Auth: read-only service account with row-level security.
- Database: warehouse plus Postgres for logs.
- Observability: query success and latency metrics.
- Hosting: secure cloud service.

Architecture:
- System boundary: ask -> translate -> validate -> query -> answer.
- Runtime topology: chat bot -> SQL generation -> database execute -> response.
- Core agent loop: interpret question, disambiguate terms, generate SQL, run read-only, explain result.
- Human-in-the-loop points: ambiguous definitions and query failures.
- Integration endpoints: Snowflake/BigQuery/Redshift, Slack/Teams, semantic layer.
- Failure handling: ambiguous questions trigger clarification before query.

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|
| questions | user asks | id, tenant_id, user_id, question, ts | tenant_id, ts | tenant-scoped |
| sql_runs | generated SQL | id, question_id, sql, status, hash | question_id, status | read-only |
| answers | response output | id, question_id, summary, result_ref | question_id | immutable |
| glossary | metric definitions | id, term, definition, owner | term | versioned |

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | /api/questions | ask question | natural language | question_id | user auth | 400 on invalid input |
| POST | /api/questions/{id}/sql | generate SQL | question_id | sql | service auth | clarification if ambiguous |
| POST | /api/questions/{id}/run | run query | sql | data | service auth | 403 on write attempt |

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|
| warehouse | inbound/outbound | read-only query | service account | deny by default |
| semantic layer | inbound | metric definitions | service token | version fallback |
| chat bot | outbound | answer and chart | bot token | fallback to text |

Folder/module structure:
- `app/(console)/analytics/`
- `app/api/questions/`
- `services/parse/`
- `services/translate/`
- `services/validate/`
- `services/answer/`

Environment variables:
- `WAREHOUSE_URL`
- `READONLY_SERVICE_ACCOUNT`
- `SEMANTIC_LAYER_PATH`
- `BOT_TOKEN`
- `LLM_API_KEY`

Critical design decisions:
1. Read-only and RLS because data safety is critical.
2. Semantic layer because metric ambiguity causes errors.
3. Chat interface because users want answers now.

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| text-to-SQL copilot | moderate | BI seats are expensive | BUILD | seat reduction is the wedge |
| warehouse | low | existing | BUY | keep SoR |
| semantic layer | low | existing if present | BUY/REUSE | prevents ambiguity |

Bottom line:
- Annual SaaS spend if buying: BI seats and reporting tools.
- One-time MVP build estimate: $40k-$80k equivalent effort.
- Recommended split: buy warehouse/semantic layer, build query copilot.
- Payback period: under 12 months if BI requests fall.

## 5. MVP ROI Business Case
Current-state cost model:
- Software: BI seats.
- Labor: analyst and data team time.
- Services/admin: dashboard maintenance.
- Error/rework: slow answers and bad definitions.

Agentic MVP cost model:
- Build: one SQL generation and answer pipeline.
- Monthly run: query and model usage.
- Maintenance: glossary and tuning.

Pricing options:
1. Low-risk pilot: one team.
2. Usage/outcome model: per question.
3. Enterprise package: copilot plus governance.

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Base | 1-2 hours saved/week | 6-10 months | month 8-12 | standard |
| Upside | strong adoption | 3-6 months | month 4-6 | high volume |
| Downside | low accuracy | 12-18 months | month 14+ | narrow scope |

No-go condition: if metrics definitions cannot be standardized, the agent will be mistrusted.

## 6. Competitor Product Teardown
Competitor map:
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Tableau | BI | mature | dashboard-heavy | enterprise / seat-based | `source/NL_Analytics_Competitor_Teardown.md` |
| Looker | BI | warehouse-native governance | analyst-heavy | enterprise sales-led | `source/NL_Analytics_Competitor_Teardown.md` |
| Sisense | BI | embedded analytics | seat/capacity cost | enterprise sales-led | `source/NL_Analytics_Competitor_Teardown.md` |
| Domo | BI | business-user friendly | credit-based cost | enterprise sales-led | `source/NL_Analytics_Competitor_Teardown.md` |
| Power BI | BI | broad adoption | still dashboard centric | bundled / seat-based | `source/NL_Analytics_Competitor_Teardown.md` |

Direct threats: Tableau and Looker. Table stakes: governance, access controls, zero hallucinations in SQL. Things not to build: a new warehouse or storage engine. Gaps: collapsing the interface, destroying per-seat licensing, eliminating spaghetti logic.

## 7. Acceptance Criteria + Test Plan
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| business question | user asks | translate runs | SQL generated | benchmark |
| ambiguous metric | vague request | translate runs | clarification asked | negative test |
| read-only query | SQL ready | run starts | correct result returned | integration test |

Edge cases:
- empty state
- query failure
- write query blocked
- slow dependency
- duplicate question idempotent
- row-level security enforced

## 8. Data Architecture Lite
Data domains:
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| schema | warehouse | catalog table | warehouse | batch | metadata tags |
| questions | user | question log | bot | realtime | redaction |
| sql runs | agent | run table | agent | realtime | read-only check |
| answers | system | answer table | system | realtime | audit trail |

Retention and deletion:
- Data retained: question logs and query lineage.
- Data deleted: ephemeral prompts and transient query drafts.
- Audit retained: SQL, results, and reviewer notes.

Analytics questions:
1. Which questions are answered without analyst help?
2. Which terms are most ambiguous?
3. What is the cost per successful answer?

Privacy/security:
- Warehouse data may contain sensitive commercial or customer information; use tenant isolation, read-only service accounts, and row-level security.

## 9. Deployment Sequencing
Pre-deploy checklist:
- confirm warehouse access
- confirm semantic definitions
- confirm read-only policy

Staging:
- run benchmark question set
- verify SQL safety and clarification prompts

Production sequence:
- start in read-only mode, then answer-only, then optional chart rendering
- expand team by team

Smoke test:
- ask, translate, run, answer

Rollback:
- disable query execution and keep answer drafts only

Observability:
- Logs: prompt, SQL, result, and version.
- Metrics: accuracy, latency, clarification rate.
- Alerts: query failures and write-block attempts.
- Dashboards: usage, cost, and answer quality.

## 10. Post-Launch Iteration Plan
Metrics:
- Activation: percent of questions answered.
- Retention: weekly usage and repeat asks.
- Revenue/willingness-to-pay: pilot extension or per-question commitment.

Week-by-week:
- Week 1: fix schema tagging.
- Week 2: improve translation accuracy.
- Week 3: tune ambiguity prompts.
- Week 4: measure analyst time saved.

Pivot signals:
- if metric definitions cannot be standardized or users do not trust SQL, narrow to guided analytics only.

## Source Notes
- `runs/2026-06-26-agentic-opportunity-blueprints/source/NL_Analytics_Competitor_Teardown.md` - internal teardown and incumbent mapping.
- `source/Agent_Use_Cases_Phase1.md` - use-case scorecard and scope.
- `source/original-10-skill-stack.txt` - prompt lineage.
- Tableau homepage - https://www.tableau.com/ - accessed 2026-06-26 - BI and analytics platform positioning.
- Tableau pricing - https://www.tableau.com/pricing - accessed 2026-06-26 - creator/viewer pricing and packaging.
- Looker homepage - https://cloud.google.com/looker - accessed 2026-06-26 - warehouse-native BI and embedded analytics positioning.
- Power BI homepage - https://www.microsoft.com/en-us/power-platform/products/power-bi/ - accessed 2026-06-26 - BI, semantic modeling, and Copilot positioning.
- Sisense homepage - https://www.sisense.com/ - accessed 2026-06-26 - embedded analytics and BI reference.
- Domo homepage - https://www.domo.com/ - accessed 2026-06-26 - governed data and analytics reference.
- Alteryx homepage - https://www.alteryx.com/ - accessed 2026-06-26 - analytics prep and workflow reference.
