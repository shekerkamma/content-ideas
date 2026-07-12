# AI Code Assistant Research Memo

Research value: high. There is strong public evidence of crowded incumbents,
pricing instability, enterprise governance gaps, and an opening for a
security-first proprietary-codebase agent.

## Incumbents And Categories

Default platform incumbent: GitHub Copilot. Broad distribution through GitHub,
VS Code, Visual Studio, JetBrains, Neovim, CLI, GitHub.com, and agent workflows.
Copilot Enterprise indexes an organization's codebase for deeper context and
offers organization controls, IP indemnity, and no training on Business or
Enterprise data.

General agentic coding assistants: Anthropic Claude Code, OpenAI Codex, Cursor,
Devin/Windsurf. These compete on multi-file edits, terminal/IDE integration,
cloud agents, PR creation, test execution, and background work.

Enterprise-private coding platforms: Tabnine, Sourcegraph, Amazon Q Developer.
Tabnine differentiates on private deployment, VPC/on-prem/air-gapped options,
zero code retention, no training, license-safe usage, MCP governance, and
context engine. Sourcegraph emphasizes code search, deep search, batch changes,
MCP server access, self-hosting, single-tenant cloud, and codebase context for
humans and agents.

AI code review / governance layer: Qodo is close to the wedge, with agentic PR
review, rules, mined rules, cross-repo review, governance analytics, BYOK,
single-tenant SaaS, and on-prem/air-gapped enterprise.

## Pricing And Pricing Friction

- GitHub Copilot public individual plans: Pro `$10/month`, Pro+ `$39/month`,
  Max `$100/month`, with AI Credits consumed by chat, agent mode, code review,
  cloud agent, CLI, and apps.
- Copilot org pricing is reported as Business `$19/user/month` and Enterprise
  `$39/user/month`, with a June 1, 2026 move to token/AI-credit usage creating
  cost uncertainty for heavy agent users.
- Cursor: Individual `$20/month`, Teams `$40/user/month`, Enterprise custom.
  Enterprise gates pooled usage, invoice/PO billing, SCIM, repository/model/MCP
  access controls, audit logs, AI code tracking API, and controls for browser,
  network, and auto-run behavior.
- Devin/Windsurf: Pro `$20/month`, Max `$200/month`, Teams `$80/month` plus
  `$40/month` per full dev seat, Enterprise sales-led. Extra usage is purchased
  at API pricing and varies by task/model/complexity.
- Tabnine: Code Assistant `$39/user/month` annually; Agentic Platform
  `$59/user/month` annually. Unlimited usage applies when using customer's own
  LLM/on-prem/cloud endpoint; Tabnine-provided LLM access is provider cost plus
  handling fee.
- Sourcegraph Enterprise starts at `$16K`, includes AI credits, volume pricing,
  org-wide pooling, no monthly credit expiry, and rollover on renewal.
- Amazon Q Developer Pro is `$19/user/month`; Java upgrade transformation
  includes 4,000 LOC/month/user pooled, then `$0.003` per submitted LOC.
- Qodo Pro Team is `$30` with credit packs; Enterprise custom for 30+ users.

## Buyer Pain / Workflow Friction

- Trust gap: Stack Overflow 2025 says 84% of respondents use or plan to use AI
  in development, but 46% distrust AI output accuracy versus 33% who trust it;
  only 3.1% highly trust outputs.
- Complex-task gap: Stack Overflow reports only 4.4% say AI handles complex
  tasks very well.
- Enterprise system dependency: DORA 2025 says AI amplifies existing
  organizational strengths and weaknesses; returns come from improving the
  underlying system, not buying tools alone.
- Experienced-developer slowdown risk: METR's 2025 RCT found experienced
  open-source developers were 19% slower with AI tools despite expecting to be
  faster.
- Review burden: 2025 Copilot adoption research found more rework and shifted
  review burden onto experienced core developers.

## Disruptive Agentic Wedge

The best wedge is an enterprise codebase operations agent with governed,
local-context execution, not another autocomplete assistant.

Position it as a private-codebase productivity layer that attaches to existing
GitHub/GitLab/Bitbucket/Jira/CI, learns repo architecture and team standards,
and handles bounded internal workflows: onboarding maps, dependency tracing,
flaky test triage, migration PRs, test generation, security-remediation PRs,
release-note diffs, code-review prep, and breakage investigations.

Differentiation:

- Predictable pricing for bounded workflows, avoiding token shock.
- Repo-local or VPC deployment with no persistent code retention by default.
- Strong audit trail: retrieved file, command, prompt, model, diff, test, and
  approval logged.
- Context quality over model novelty: code graph, dependency map, ownership
  map, docs, ADRs, CI history, Jira tickets.
- Human-in-the-loop PRs only; no silent merges.
- Governance-native policy packs for secrets, PII, license risk, prompt
  injection, model routing, and allowed tools.

## 30-Day MVP Implications

Build a narrow wedge: AI onboarding + change-impact + PR-prep agent for one
proprietary repo.

MVP scope:

- Connect GitHub/GitLab repo read-only, then optional branch/PR write.
- Build repo index: symbols, imports, file ownership, docs, tests, CI config,
  recent PRs.
- Chat workflows: explain codebase, locate implementation, assess change
  impact, generate test plan, draft PR with tests.
- Agent workflows: create branch, modify files, run tests/lint, produce diff,
  summarize risk, open PR.
- Admin controls: repo allowlist, command allowlist, network off by default,
  secrets redaction, audit log, no-training promise.
- Pricing test: per-seat plus workflow quota, or per-repo fixed pilot fee.
- Buyer target: VP Eng / platform engineering / dev productivity teams at
  100-2,000 engineer companies with large proprietary monorepos or legacy
  services.

## Risks / Security / IP

- Code leakage and training risk: buyers will ask whether code, prompts,
  outputs, logs, and embeddings are retained or used for training.
- Prompt injection and tool poisoning: MCP and tool-using agents expose a real
  attack surface.
- Generated-code vulnerabilities: AI-attributed files have documented CWE risk;
  tests, static analysis, and human review are product features.
- License/IP ambiguity: buyers care about public-code matching, attribution,
  indemnity, and license contamination.
- Cost unpredictability: agentic workflows can run long and trigger expensive
  model/tool loops.
- Reliability/accountability: agents can make plausible but system-breaking
  edits; diffs, code owners, and approvals are required guardrails.

## Sources

- GitHub Copilot Plans & Pricing:
  https://github.com/features/copilot/plans
- ITPro, Copilot pricing changes:
  https://www.itpro.com/software/development/github-copilot-pricing-changes-usage-based-billing-explained
- Business Insider, Copilot token usage backlash:
  https://www.businessinsider.com/github-copilot-token-uage-pricing-change-reaction-2026-6
- Cursor Pricing: https://cursor.com/pricing
- Devin/Windsurf Pricing: https://devin.ai/pricing
- Tabnine Pricing: https://www.tabnine.com/pricing/
- Sourcegraph Pricing: https://sourcegraph.com/pricing
- Qodo Pricing: https://www.qodo.ai/pricing/
- Amazon Q Developer Pricing:
  https://aws.amazon.com/q/developer/pricing/
- Claude Code Docs: https://code.claude.com/docs/en/overview
- OpenAI Codex: https://openai.com/codex/
- OpenAI Enterprise Privacy:
  https://openai.com/enterprise-privacy/
- Stack Overflow Developer Survey 2025:
  https://survey.stackoverflow.co/2025/ai/
- DORA 2025:
  https://dora.dev/research/2025/dora-report/
- METR productivity RCT: https://arxiv.org/abs/2507.09089
- AI-assisted programming maintenance burden:
  https://arxiv.org/abs/2510.10165
- MCP prompt-injection paper:
  https://arxiv.org/abs/2603.21642
- AI-generated code vulnerability analysis:
  https://arxiv.org/abs/2510.26103
