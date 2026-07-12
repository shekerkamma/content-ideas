---
status: reviewed
use_case: "AI Code Assistant"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: medium-high
  competitor: high
  pricing: high
  implementation: medium-high
---

# AI Code Assistant Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** VP Engineering or Head of Platform Engineering at a regulated
or legacy-heavy software organization with 100-2,000 engineers, large
proprietary repos, high review burden, and an existing AI coding tool budget.

**Later ICPs:** broader developer productivity teams after a governed repo-
operations wedge proves time saved, reviewer acceptance, and security controls
in one high-context repo.

**Pain wedge:** Developers have access to powerful coding assistants, but
enterprise teams still struggle with local architecture context, trust, review
burden, IP/security controls, and unpredictable usage-based agent costs.

**Incumbent weakness:** GitHub Copilot, Cursor, Claude Code, OpenAI Codex,
Devin/Windsurf, Tabnine, Sourcegraph, Amazon Q Developer, and Qodo all push the
category forward. The gap is not generic code generation; it is governed
codebase operations for a specific enterprise repo.

**Agentic disruption thesis:** Build a private-codebase operations agent that
attaches to GitHub/GitLab/Jira/CI, learns repo architecture and team standards,
and handles bounded workflows: onboarding, change-impact analysis, PR prep,
test plan generation, flaky-test triage, migration diffs, and security
remediation drafts.

**Why now:** AI coding adoption is high, but public research shows trust and
complex-task gaps. Pricing is also shifting toward usage credits/tokens, making
enterprise cost predictability a positioning wedge.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 24/30**

This score is inferred from public adoption/trust research, pricing evidence,
and competitor analysis. It should be confirmed with at least three VP Eng,
platform engineering, or security buyers before being used as a validated sales
claim.

- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 7/10

**Who has the problem:** Platform engineering leaders, dev productivity teams,
staff/principal engineers, security teams, and engineering managers onboarding
developers into complex proprietary systems.

**Last-time/recency evidence:** Developers face codebase navigation and change
impact questions daily. Stack Overflow 2025 reports broad AI usage/planning but
low trust in AI output. DORA 2025 frames AI as an amplifier of existing
organizational systems, not a magic productivity layer.

**Current workaround:** Generic AI coding tools, internal docs, code search,
Slack questions, staff engineer office hours, manual PR review, CI spelunking,
and tribal knowledge.

**Switching reason:** A repo-specific operations agent can be priced and
governed around bounded workflows rather than generic seat/token consumption.

**Payment signal:** GitHub Copilot, Cursor, Tabnine, Sourcegraph, Amazon Q,
Qodo, and Devin/Windsurf all publish pricing or enterprise packaging. The
market is already budgeted; dissatisfaction centers on trust, context, security,
and cost predictability.

**30-day reachability:** Medium-high. Target buyers are identifiable by
engineering size, monorepo/legacy stack, platform engineering investment, and
security posture.

**Verdict: PROCEED, but avoid generic assistant positioning.** The wedge must be
workflow-specific and governance-native.

## 2. The 30-Day Scope Definition

**Project name:** Repo Operations Agent

**Validated problem:** Generic coding assistants help with snippets, but
enterprise teams need trusted repo-specific answers, change-impact analysis, and
PR prep with audit controls.

**Target user:** Platform engineering or dev productivity team at a 100-2,000
engineer company with proprietary repos.

**Core hypothesis:** A governed agent connected to one repo can reduce onboarding
and PR-prep time by answering architecture questions, tracing dependencies, and
drafting safe changes with tests.

### In Scope

1. **Repo indexing**
   - Acceptance criterion: agent indexes symbols, imports, docs, tests, CI
     config, ownership, and recent PR metadata for one repo.
2. **Architecture Q&A**
   - Acceptance criterion: answers cite files, symbols, docs, or PRs and admit
     uncertainty when context is missing.
3. **Change-impact analysis**
   - Acceptance criterion: given a proposed change, agent lists impacted files,
     tests, owners, risks, and rollout notes.
4. **PR-prep workflow**
   - Acceptance criterion: agent can create branch/diff in approved workspace,
     run allowed tests/lint, and open a draft PR or patch for review.
5. **Governance controls**
   - Acceptance criterion: admin can configure repo allowlist, command
     allowlist, network policy, model routing, secrets redaction, and audit log.

### Explicitly Out Of Scope

- General IDE autocomplete replacement.
- Silent merge or deploy.
- Unbounded terminal/network access.
- Training on customer code.
- Full multi-repo enterprise search in v1.
- Autonomous security patching in production branches.
- Legal/license final determinations.
- Replacing human code review.

### Week-By-Week Milestones

- **Week 1:** Connect one repo read-only, build code graph/index, ingest docs,
  and define approved workflows.
- **Week 2:** Ship architecture Q&A and change-impact analysis with citations.
- **Week 3:** Add branch/diff/test execution in sandbox with command allowlist
  and audit logs.
- **Week 4:** Pilot PR-prep workflow with 3-5 real tasks and measure review
  quality, test pass rate, and time saved.

**Dependencies:** GitHub/GitLab access, repo owner, CI command list, coding
standards, secrets policy, test environment, and security review.

**Acceptance test:** For a real task, agent explains relevant code, drafts a
change, runs approved tests, opens a draft PR, and logs every source, command,
model, diff, and approval.

**Top risks:** code leakage, prompt injection, tool poisoning, insecure diffs,
license/IP concerns, and cost unpredictability.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: Next.js + TypeScript admin console, workflow history, PR review
  prep, and audit viewer.
- Backend: Python FastAPI or TypeScript service for repo indexing, agent
  orchestration, and Git provider webhooks.
- Agent runtime: containerized sandbox per task with explicit command allowlist,
  network disabled by default, and ephemeral workspace.
- Retrieval/index: tree-sitter symbol parsing, ripgrep/code search, embeddings
  for docs/comments, code graph for imports/dependencies, and PR/CI history.
- Database: Postgres for repos, indexes, workflow runs, audit logs, policies,
  command results, and cost tracking.
- Integrations: GitHub/GitLab/Bitbucket, Jira/Linear, CI provider, SSO, secrets
  scanner, SAST, dependency scanner.
- Model layer: model router with no-training enterprise settings and option for
  buyer VPC/self-hosted models where required.

**Architecture:** The agent operates in a forked workspace. It can read indexed
repo context, generate a plan, modify files in a branch, run approved commands,
and create a draft PR. It cannot merge, deploy, exfiltrate secrets, or access
unapproved network targets.

**Critical design decisions:**

1. **Workflow agent, not autocomplete:** avoids competing head-on with Copilot
   and Cursor.
2. **Context quality before model novelty:** value comes from code graph,
   ownership, docs, ADRs, CI, and PR history.
3. **Audit-first execution:** every file, prompt, model, command, test, diff,
   and approval is recorded.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/repos/index` | Start or refresh repository indexing | Repo URL, provider, tenant ID | Index job ID | Org admin token | Reject if repo access is missing |
| GET | `/api/repos/:repoId/context` | Return code graph and indexed context | Repo ID | Symbols, deps, docs, policy state | RBAC session | 404 if repo not indexed |
| POST | `/api/workflows/plan` | Draft a safe implementation plan | Repo ID, task brief, branch target | Plan steps and risk flags | User session + repo access | Fail closed if policy pack is absent |
| POST | `/api/workflows/run` | Execute approved sandbox task | Plan ID, command allowlist, branch target | Run ID and diff summary | Maintainer or reviewer role | Abort on disallowed command or network access |
| POST | `/api/github/webhook` | Receive PR, push, and check events | Webhook payload | Ack + queued job | GitHub app signature | 401 on signature mismatch; retry on transient errors |

### Folder / Module Structure

- `app/(console)/repos/` for repo selection, context, and run history.
- `app/api/repos/` for indexing and context APIs.
- `app/api/workflows/` for plan generation, sandbox execution, and approvals.
- `app/api/github/` for webhook ingestion and status callbacks.
- `services/indexer/` for tree-sitter parsing, ripgrep search, and embeddings.
- `services/agent/` for planning, tool-use policy, and PR drafting.
- `workers/sandbox/` for ephemeral execution and command capture.
- `lib/git/` for provider adapters and branch operations.
- `lib/security/` for allowlists, secret scanning, and policy packs.
- `tests/code-assistant/` for command gating, data-boundary, and regression tests.

### Environment Variables

- `DATABASE_URL`: Postgres for repos, runs, policies, and audit logs.
- `REDIS_URL`: queue backend for indexing and sandbox jobs.
- `GITHUB_APP_ID`: GitHub App identifier.
- `GITHUB_APP_PRIVATE_KEY`: GitHub App signing key.
- `GITHUB_WEBHOOK_SECRET`: webhook verification secret.
- `MODEL_ROUTER_API_KEY`: provider-router credential.
- `MODEL_ROUTER_BASE_URL`: model gateway endpoint.
- `SANDBOX_IMAGE`: container image for isolated execution.
- `ALLOWED_COMMANDS`: allowlist used by the sandbox policy.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: traces and metrics export.
- `SENTRY_DSN`: error tracking and crash capture.

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Generic autocomplete/chat | High to match incumbents | Copilot/Cursor/Claude Code/Codex already strong | BUY/DO NOT BUILD | Not the wedge. |
| Repo-specific code graph | Medium | Sourcegraph/Tabnine have context engines | BUILD/HYBRID | Use OSS parsing/search but tailor to workflows. |
| Governed sandbox execution | Medium-High | Incumbents vary on controls | BUILD | Enterprise trust depends on execution policy. |
| PR-prep workflow | Medium | Codex/Claude/Devin support PR workflows | BUILD | Differentiate on buyer-specific controls and pricing. |
| Security/license policy packs | Medium | Qodo/Tabnine/Amazon market governance | HYBRID | Integrate scanners; build workflow gating. |
| Cost tracking | Low-Medium | Usage credits/tokens create uncertainty | BUILD | Predictability is a positioning wedge. |

**Bottom line:** Do not build another assistant. Build the governed internal
workflow layer for proprietary codebase operations.

## 5. MVP ROI Business Case

**Current-state cost model:** developer onboarding time, staff engineer
interruptions, manual change-impact analysis, PR rework, flaky-test triage,
security remediation cycles, and token/seat spend across generic AI tools.

**Agentic MVP cost model:** repo indexing, sandbox execution, model/API usage,
storage, CI usage, security controls, and platform maintenance.

**Pricing options:**

1. Fixed pilot for one repo and 3 workflows.
2. Per-repo monthly package with workflow quota.
3. Enterprise package with VPC/self-hosting, SSO, audit, and policy packs.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | Small/simple repo, 20 target developers, 2 hours/dev/mo saved, `$110/hr` loaded engineering cost, `$35K` pilot | Slow | 12-24 months | Not worth custom wedge. |
| Base | 100 target developers, 4 hours/dev/mo saved across onboarding/PR prep, `$125/hr` loaded cost, `$60K` pilot, `$6K/mo` run cost | Moderate | 4-8 months | Strong platform engineering case. |
| Upside | 300+ target developers, repeatable migrations/security fixes, 6+ hours/dev/mo or staff-engineer interrupt reduction, `$90K` pilot, `$12K/mo` run cost | Fast | 2-4 months | Strong enterprise case. |

**No-go condition:** If buyer cannot provide repo access, test commands, or
security policy, the agent cannot demonstrate trustworthy execution.

Use buyer-specific inputs where available. Default formulas:

```text
Current monthly workflow cost =
  target developers * hours spent on repo navigation/PR prep/rework per month
  * loaded engineering hourly cost
  + staff engineer interruption cost

Agentic monthly cost =
  platform/run cost + model/CI usage + residual review time

Monthly value =
  engineering time avoided + reduced rework/interruption cost - agentic monthly cost

Payback period =
  pilot/build cost / monthly value
```

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| GitHub Copilot | Default incumbent | Distribution, IDE/GitHub integration | Usage-credit uncertainty and generic context limits | Pro `$10`, Pro+ `$39`, Max `$100`; org pricing reported | GitHub, ITPro |
| Claude Code | Agentic coding CLI/IDE | Strong codebase reading, editing, command execution, and agent workflows | Not a buyer-specific governed platform by itself | Product/enterprise terms vary | Anthropic docs |
| OpenAI Codex | Cloud coding agent | Parallel worktrees, PRs, refactors, tests, review workflows | Needs enterprise governance and repo-specific controls for regulated buyers | Product/enterprise packaging | OpenAI |
| Cursor | IDE agent | Developer UX and agent mode | Enterprise controls/custom pricing; usage overage | `$20 individual`, `$40/team user`, enterprise custom | Cursor |
| Devin/Windsurf | Agentic coding | Background tasks and PR workflows | Cost varies by task/model complexity | Pro/Max/Team/Enterprise pricing | Devin |
| Tabnine | Private enterprise AI | VPC/on-prem/air-gapped and no-training positioning | Higher enterprise platform cost | `$39-$59/user/month` annually | Tabnine |
| Sourcegraph | Code search/context | Search, batch changes, enterprise context | Enterprise platform spend | Enterprise starts around `$16K` | Sourcegraph |
| Amazon Q Developer | AWS-native | AWS controls and transformation | Best for AWS-centric buyers | Pro `$19/user/month`; LOC overage | AWS |
| Qodo | Review/governance | PR review and rules | Enterprise custom for large teams | Pro Team `$30` plus credits | Qodo |

**Direct threats:** GitHub Copilot Enterprise, Cursor Enterprise, Sourcegraph,
Tabnine, and Qodo. **Table stakes:** repo indexing, citations, sandboxed edits,
tests, PR creation, audit. **Do not build:** generic autocomplete. **Gaps:**
predictable workflow pricing, local governance, and repo-specific operational
workflows.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Repo index | Repo connected | Index job runs | Symbols/docs/tests/owners are searchable | Index report |
| Architecture Q&A | Developer asks where X lives | Agent answers | Answer cites files/symbols and confidence | Citation log |
| Change impact | Proposed change given | Agent analyzes | Impacted files/tests/owners/risks listed | Impact report |
| PR prep | Task approved | Agent edits branch | Diff created and tests/lint run | Draft PR and command log |
| Security guard | Secret or unsafe command appears | Agent acts | Secret redacted or command blocked | Policy event |
| Audit trail | Workflow completes | Auditor opens run | Sources, prompts, model, commands, diff, cost visible | Audit view |

**Edge cases:** huge repo, generated code, failing tests, missing docs, circular
dependencies, secret in source, prompt injection in repo files, untrusted MCP
server, ambiguous ownership, and flaky CI.

## 8. Data Architecture Lite

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| Code files | Git provider | Index + ephemeral checkout | Git | Webhook/scheduled | Commit SHA |
| Symbols/deps | Parser/indexer | Code graph | Derived from Git | Reindex | Parser confidence |
| Docs/ADRs | Repo/wiki/docs | Vector/doc index | Repo/docs | Reindex | Source citation |
| PR/CI history | Git/CI APIs | Metadata tables | Git/CI | API | Run IDs |
| Agent runs | Runtime | Audit log | Agent platform | Append-only | Prompt/model/command |
| Diffs | Branch/patch | Git branch + audit | Git | Per run | Human review |

**Analytics questions:** Which workflows save time? Which repos produce
low-confidence answers? Which commands fail? What is cost per PR-prep workflow?
How often do reviewers reject agent diffs?

**Privacy/security:** code, prompts, embeddings, logs, and outputs are sensitive
IP. Require no-training settings, retention controls, encryption, tenant
isolation, secret redaction, command/network allowlists, SSO, audit logs, and
option for VPC/self-hosting.

## 9. Deployment Sequencing

**Pre-deploy:** confirm repo, access scopes, no-training/data retention terms,
command allowlist, network policy, CI budget, and security review.

**Staging:** index a non-critical repo or sandbox branch. Test Q&A, impact
analysis, patch generation, test execution, and prompt-injection cases.

**Production:** start read-only. Enable branch/PR write only for approved tasks.
No merges or deploys. Expand workflows after reviewer trust is established.

**Smoke test:** ask architecture question, run impact analysis, draft small
change, run tests, open draft PR, and verify audit/cost logs.

**Rollback:** revoke app permissions, disable workflow runs, preserve audit,
delete embeddings/cache per retention policy, and close draft branches.

## 10. Post-Launch Iteration Plan

**Metrics:** activation equals weekly workflows run by target developers;
retention equals repeat use and reviewer acceptance; revenue signal equals
paid per-repo/platform pilot.

**Week 1:** fix index gaps, citations, and command failures. No new repo.

**Week 2:** interview developers/reviewers. Identify the workflow with highest
trust and time-saved signal.

**Week 3:** deepen that workflow, such as change-impact or test-plan quality.

**Week 4:** measure PR acceptance, review comments, test pass rate, and saved
staff-engineer time.

**Pivot signals:** developers distrust output, security blocks code retention,
reviewers reject most diffs, or costs are unpredictable versus value.

## Source Notes

- GitHub Copilot Plans - https://github.com/features/copilot/plans - accessed 2026-06-26 - Copilot plan and credit pricing.
- ITPro Copilot pricing changes -
  https://www.itpro.com/software/development/github-copilot-pricing-changes-usage-based-billing-explained.
- Business Insider Copilot pricing backlash -
  https://www.businessinsider.com/github-copilot-token-uage-pricing-change-reaction-2026-6.
- Cursor Pricing - https://cursor.com/pricing.
- Devin/Windsurf Pricing - https://devin.ai/pricing.
- Tabnine Pricing - https://www.tabnine.com/pricing/.
- Sourcegraph Pricing - https://sourcegraph.com/pricing.
- Qodo Pricing - https://www.qodo.ai/pricing/.
- Amazon Q Developer Pricing - https://aws.amazon.com/q/developer/pricing/.
- Claude Code Docs - https://code.claude.com/docs/en/overview.
- OpenAI Codex - https://openai.com/codex/.
- OpenAI Enterprise Privacy - https://openai.com/enterprise-privacy/.
- Stack Overflow Developer Survey 2025 - https://survey.stackoverflow.co/2025/ai/.
- DORA 2025 - https://dora.dev/research/2025/dora-report/.
- METR productivity RCT - https://arxiv.org/abs/2507.09089.
- AI-assisted programming maintenance burden -
  https://arxiv.org/abs/2510.10165.
- MCP prompt-injection paper - https://arxiv.org/abs/2603.21642.
- AI-generated code vulnerability analysis - https://arxiv.org/abs/2510.26103.
