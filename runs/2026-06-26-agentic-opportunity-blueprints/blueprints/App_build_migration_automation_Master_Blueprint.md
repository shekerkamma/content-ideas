---
status: reviewed
use_case: "App Build and Migration Automation"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence: high
---

# App Build and Migration Automation Master Implementation Blueprint

## Executive Positioning
- Target buyer: engineering leaders and platform teams.
- Pain wedge: migrations consume expensive engineering time on boilerplate.
- Incumbent weakness: low-code and migration tools fail on custom edge cases.
- Agentic disruption thesis: parse the codebase, translate patterns, keep tests green, and preserve ejectability.
- Why now: teams want modernization without multi-quarter rewrite projects.

## 1. Problem-Solution Fit Diagnostic
Score 27/30
- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

Evidence:
- Who has the problem: teams moving frameworks or platforms.
- Last-time/recency evidence: code-generation agents are widely used now.
- Current workaround: manual rewrite and integration work.
- Switching reason: reduce boilerplate and migration cost.
- Payment signal: engineering time and modernization budgets.
- 30-day reachability: one module and one migration target can prove the wedge.

Verdict: PROCEED

## 2. 30-Day Scope Definition
- Project name: Migration Copilot
- Validated problem: app migration is repetitive and tedious.
- Target user: engineer or platform team.
- Core hypothesis: the agent can migrate isolated code paths and generate passing tests.

In scope:
1. AST analysis and code mapping.
2. Automated transpilation and test generation.
3. Pilot module migration.

Explicitly out of scope:
- Full architecture rewrite.
- Autonomous production deploys without review.
- Unknown business logic automation without flagging.

Week-by-week milestones:
- Week 1: AST parsing and analysis.
- Week 2: source-target mapping.
- Week 3: transpilation and tests.
- Week 4: pilot migration.

Dependencies:
- repo access, CI pipeline, and target framework conventions.

Acceptance test:
- a module migrates and passes generated tests.

Top 3 risks + mitigations:
- hidden business logic - human review gate
- test gaps - generate and run tests
- merge conflicts - isolate changes

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend: migration review UI.
- Backend: TypeScript/Python service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: repo index and AST store.
- Auth: Git provider SSO.
- Database: Postgres for migration jobs and diffs.
- Observability: test pass rate and diff tracking.
- Hosting: ephemeral containers in CI.

Architecture:
- System boundary: repo ingest -> analyze -> transform -> test -> review.
- Runtime topology: codebase clone -> AST parse -> transform -> test -> PR.
- Core agent loop: inspect code, map patterns, rewrite modules, run tests, flag ambiguity.
- Human-in-the-loop points: unclear business logic and PR review.
- Integration endpoints: Git repos, CI/CD, issue tracker.
- Failure handling: if tests fail, the agent narrows scope and retries.

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|
| jobs | migration jobs | id, tenant_id, repo, target | tenant_id, repo | tenant-scoped |
| modules | code modules | id, job_id, path, language, status | job_id, status | access scoped |
| diffs | transform output | id, module_id, patch, result | module_id | audit tracked |
| tests | generated tests | id, module_id, name, status | module_id, status | immutable |

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | /api/jobs | create migration job | repo, target | job_id | user auth | 400 on invalid target |
| POST | /api/jobs/{id}/run | run migration | job_id | results | service auth | partial on unknown code |
| POST | /api/jobs/{id}/review | reviewer action | approve/reject | ack | user auth | 409 if stale |

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|
| git repo | inbound/outbound | code and PRs | OAuth | retry and branch isolation |
| CI/CD | outbound | tests and builds | service token | stop on test fail |
| issue tracker | outbound | migration notes | API token | queue if down |

Folder/module structure:
- `app/(console)/migration/`
- `app/api/jobs/`
- `services/analyze/`
- `services/transform/`
- `services/test/`
- `services/review/`

Environment variables:
- `GIT_OAUTH_TOKEN`
- `TARGET_FRAMEWORK`
- `CI_BASE_URL`
- `JOB_BUCKET`
- `LLM_API_KEY`

Critical design decisions:
1. AST-first because syntax-aware transformations are safer.
2. Tests as gate because code must compile and run.
3. Human review for ambiguous business logic because the model cannot guess intent reliably.

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| migration copilot | moderate | low-code tools fail on edge cases | BUILD | edge-case handling is the wedge |
| source repo | low | existing | BUY | keep SoR |
| CI | low | existing | BUY/REUSE | use current pipeline |

Bottom line:
- Annual SaaS spend if buying: migration tools and integrators.
- One-time MVP build estimate: $60k-$120k equivalent effort.
- Recommended split: buy source/CI, build migration worker.
- Payback period: under 12 months if migration time drops.

## 5. MVP ROI Business Case
Current-state cost model:
- Software: migration tools.
- Labor: engineer time.
- Services/admin: consulting.
- Error/rework: failed rewrites and merge conflicts.

Agentic MVP cost model:
- Build: transform and test pipeline.
- Monthly run: repo analysis and LLM usage.
- Maintenance: target updates and rule tuning.

Pricing options:
1. Low-risk pilot: one module.
2. Usage/outcome model: per migrated module.
3. Enterprise package: migration plus CI automation.

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Base | 80% boilerplate saved | 6-10 months | month 8-12 | conservative |
| Upside | multiple modules | 3-6 months | month 4-6 | strong fit |
| Downside | complex legacy code | 12-18 months | month 14+ | keep narrow |

No-go condition: if the repo cannot be safely analyzed, the tool should stay advisory only.

## 6. Competitor Product Teardown
Competitor map:
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| OutSystems | low-code | enterprise governance | proprietary runtime | enterprise sales-led | `source/App_build_migration_automation_Competitor_Teardown.md` |
| Mendix | low-code | enterprise scale | heavyweight learning curve | enterprise sales-led | `source/App_build_migration_automation_Competitor_Teardown.md` |
| Appian | BPM | workflow depth | proprietary lock-in | enterprise sales-led | `source/App_build_migration_automation_Competitor_Teardown.md` |
| Pega | automation | scale and governance | costly and complex | enterprise sales-led | `source/App_build_migration_automation_Competitor_Teardown.md` |
| Oracle APEX | low-code | DB centric | limited ejectability | enterprise sales-led | `source/App_build_migration_automation_Competitor_Teardown.md` |

Direct threats: OutSystems and Appian. Table stakes: RBAC, security, fast deployment. Things not to build: another proprietary visual flowchart language. Gaps: standard output, prompt-to-app, and no specialized certs.

## 7. Acceptance Criteria + Test Plan
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| module migration | source module | transform runs | target module compiles | test suite |
| ambiguous logic | undocumented block | run starts | human review queued | negative test |
| stateful component | complex code | transform runs | tests pass | integration test |

Edge cases:
- empty repo
- parser failure
- unsupported framework
- queued job
- duplicate migration idempotent
- repo isolation

## 8. Data Architecture Lite
Data domains:
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| repo code | git | repo index | repo | batch | checksum |
| transforms | agent | diff table | agent | realtime | lint + tests |
| tests | agent | test table | agent | realtime | pass/fail |
| reviews | engineer | review table | engineer | realtime | immutable log |

Retention and deletion:
- Data retained: diffs, tests, and review trail.
- Data deleted: ephemeral workspaces and transient prompts.
- Audit retained: commands, patches, and reviewer decisions.

Analytics questions:
1. Which module types migrate cleanly?
2. Which transforms fail tests most often?
3. What is the cost per migrated module?

Privacy/security:
- Code and prompts are sensitive IP; enforce repo isolation, least privilege, secret redaction, and no-training settings.

## 9. Deployment Sequencing
Pre-deploy checklist:
- confirm repo access
- confirm target framework
- confirm CI command list

Staging:
- run on a sandbox branch
- verify compile and test output

Production sequence:
- start read-only, then branch-only, then draft PRs
- no merge or deploy autonomy

Smoke test:
- analyze, transform, test, open draft PR

Rollback:
- revoke permissions and preserve audit trail

Observability:
- Logs: prompts, commands, diffs, and tests.
- Metrics: test pass rate, diff size, rollback rate.
- Alerts: unsafe commands and failing builds.
- Dashboards: migration jobs and time saved.

## 10. Post-Launch Iteration Plan
Metrics:
- Activation: weekly workflows run.
- Retention: repeat use and reviewer acceptance.
- Revenue/willingness-to-pay: paid pilot or per-module pricing.

Week-by-week:
- Week 1: fix index gaps.
- Week 2: improve transform quality.
- Week 3: deepen test generation.
- Week 4: measure PR acceptance.

Pivot signals:
- if developers distrust output or tests fail too often, narrow to migration assist only.

## Source Notes
- `runs/2026-06-26-agentic-opportunity-blueprints/source/App_build_migration_automation_Competitor_Teardown.md` - internal teardown and incumbent mapping.
- `source/Agent_Use_Cases_Phase1.md` - use-case scorecard and scope.
- `source/original-10-skill-stack.txt` - prompt lineage.
- OutSystems - https://www.outsystems.com/ - accessed 2026-06-26 - enterprise AI development platform positioning.
- OutSystems Pricing - https://www.outsystems.com/pricing-and-editions - accessed 2026-06-26 - custom quote pricing and app/user scale model.
- Mendix - https://www.mendix.com/ - accessed 2026-06-26 - agentic enterprise and low-code platform positioning.
- Mendix Pricing - https://www.mendix.com/pricing/ - accessed 2026-06-26 - tiered pricing with app-level entry point.
- Appian - https://www.appian.com/ - accessed 2026-06-26 - process orchestration and low-code platform positioning.
- Appian Pricing - https://appian.com/products/pricing - accessed 2026-06-26 - pricing and plans entry point.
- Pega Platform - https://www.pega.com/products/platform - accessed 2026-06-26 - enterprise low-code and workflow platform positioning.
- Oracle APEX Pricing - https://www.oracle.com/application-development/apex/pricing/ - accessed 2026-06-26 - APEX cloud price list and developer services.
