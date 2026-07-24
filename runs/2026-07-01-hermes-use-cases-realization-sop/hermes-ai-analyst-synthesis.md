# Hermes Use Cases And Realization - AI Analyst Synthesis

Run: `runs/2026-07-01-hermes-use-cases-realization-sop`
Date: 2026-07-01
Status: validated qualitative synthesis for deck rendering

## Goal Contract

- Outcome: client-ready PPTX that explains Hermes use cases and realization as
  an SOP/spec-driven implementation document.
- Artifacts: synthesis markdown, PPTX builder script, reviewed PPTX, QA preview.
- Constraints: use `goal-loop-orchestrator`; wire `ai-analyst` before deck
  rendering; use branded PPTX workflow; do not hardcode secrets.
- Acceptance criteria: deck contains implementation SOP, use-case realization
  patterns, guardrails, source/tool order, data synthesis, rollout phases, and
  QA gates.
- Verification: source tieout, python builder compile, PPTX structural
  validation, preview contact sheet review.
- Research mode: source-grounded synthesis from workshop transcript, Hermes
  setup PDF, and repo Hermes notes. No generic web search used.
- Loop budget: 3 passes.
- Stop conditions: reviewed PPTX created, QA artifacts generated, or build
  blocker reported.

## Skill Chain

| Phase | Skill/action | Why | Input | Output | Verification |
|---|---|---|---|---|---|
| 1 | `goal-loop-orchestrator` | Define outcome, chain, gates | user request, local source files | goal contract, chain contract | chain has concrete handoffs |
| 2 | `ai-analyst` synthesis | Validate and structure source facts before rendering | transcript, setup PDF extract, existing Hermes use-case doc | this synthesis pack | source tieout and confidence labels |
| 3 | `branded-pptx-deck` | Build native editable client PPTX | synthesis pack | reviewed PPTX | `Deck.save()` validation and preview |

## Chain Contract

| Step | Skill/action | Consumes | Produces | Next consumer | Value test |
|---|---|---|---|---|---|
| 1 | `goal-loop-orchestrator` | user deck request | goal/chain contract | `ai-analyst` | clear acceptance criteria and SOP spine |
| 2 | `ai-analyst` | source docs and notes | validated synthesis | PPTX builder | deck content is grounded before design |
| 3 | `branded-pptx-deck` | validated synthesis | native PPTX + preview | user | client-ready editable deliverable |

## Source Tieout

| Claim | Source | Confidence | Deck use |
|---|---|---|---|
| Hermes is a personal-agent harness that gives a model access to local tools, files, shell, browser/search, schedules, and memory. | Workshop transcript and `docs/hermes-use-cases-and-realization.md` | High | operating thesis and architecture |
| You.com is recommended as the Hermes search API because `livecrawl` can combine search and full-page markdown extraction. | `Hermes Agent Setup - Google Docs.pdf`, pages 5-6 | High | search backend SOP |
| You.com Research API and Finance Research API are relevant for deep research and finance workflows. | Setup PDF, pages 6-7 | High | use-case/tool mapping |
| GBrain adds graph-like, git-backed, human-readable memory with background cleanup/dreaming. | Setup PDF, pages 7-8 | High | memory SOP |
| Smart contacts/entities combine email, calendar, Zoom, Twitter/X, LinkedIn, contacts, You.com enrichment, GBrain, and Obsidian visualization. | Setup PDF, pages 8-9 and transcript | High | use-case realization slide |
| Cost controls should use activity-dependent model selection: Sonnet default, Opus for meaningful code, Haiku for summarization/parsing. | Setup PDF, pages 9-10 | High | model routing controls |
| Scheduled processes include daily inefficiency scan, signal monitoring, data ingestion, and GBrain dreaming. | Setup PDF, page 10 and transcript | High | cron/SOP slide |
| Human approval should gate high-risk actions like publishing, investor emails, credential changes, and deletion. | Derived from transcript examples and implementation notes | Medium-high | controls and RACI |
| The workshop cited an operating setup with 18 cron jobs. | Setup PDF page 10 and transcript | High | proof point, not a target requirement |

## Synthesis Findings

1. Hermes should be sold and implemented as an always-on operating layer, not as
   another chat UI. The value comes from tool access, scheduled routines, memory,
   and current search wired into repeatable SOPs.
2. The implementation sequence matters: install and model provider first, then
   search, then memory, then low-risk read-only routines, then draft workflows,
   then approval-gated execution.
3. You.com is the preferred current-web layer for Hermes because it reduces
   multi-tool sprawl for search plus extraction and supports agentic research
   workloads.
4. GBrain is the durable memory layer. It should be treated as recall/write-back
   infrastructure, while client deliverables remain in repo/run files.
5. The strongest initial use cases are read-only or draft-only: daily brief,
   smart contacts, pre-call brief, investor/deal research, social/news signal
   monitoring, content research drafts, cost/health scans, and security audits.
6. Autonomy should be staged. Start with observe/summarize, advance to draft,
   then require approval before external side effects.
7. The agent needs an operating contract: source order, credential boundaries,
   model routing, schedule ownership, escalation rules, and acceptance criteria.

## Use-Case Taxonomy

| Use case | Trigger | Data sources | Hermes realization | Autonomy level | Primary guardrail |
|---|---|---|---|---|---|
| Daily executive brief | morning/afternoon cron | calendar, inbox, Slack/Teams, transcripts, GBrain | summarize priorities and deltas | read-only scheduled | cite sources; no sends |
| Smart contacts/entities | new meeting/contact or nightly enrichment | calendar, email, Zoom, LinkedIn, Twitter/X, contacts, You.com | enrich profiles and write entity notes | scheduled/event-triggered | provenance and freshness |
| Pre-call account briefing | calendar event | GBrain, web/news, company docs, CRM/email | meeting prep note with hooks, risks, questions | event-triggered draft | stale-source block |
| Investor/deal research | fundraise or prospect list | investor lists, prior investments, social/news, inbox | rank fit, draft hooks, queue outreach | draft-only | user sends messages |
| Signal monitoring | cron | web, news, social, forums, YouTube, Reddit | filter meaningful deltas and explain impact | read-only scheduled | noise threshold |
| Content pipeline | daily/weekly topic scan | YouTube creators, web/news, You.com Research, GBrain | rank topics, draft posts/promos | draft-only | editorial approval |
| Cost/model health | nightly cron | Hermes logs, API usage, model routes, cron status | scan inefficiency and runaway spend | operational scheduled | approval before risky fix |
| Security/permission audit | scheduled/manual | config, env, plugins, MCPs, credentials | least-privilege report and remediation queue | read-only/manual | no secret exposure |
| Lightweight app builder | user prompt | repo files, skills, terminal, browser checks | build small tools with verification | delegated manual | tests and worktree isolation |
| Knowledge compaction | nightly/weekend cron | notes, meetings, research, GBrain markdown | dedupe, link, and refactor memory | low-risk scheduled | git-backed review |

## SOP Implementation Phases

1. **Foundation**: install Hermes, choose local setup, connect model provider,
   enable desktop/CLI access, document owner and host machine.
2. **Search**: configure You.com as current-web backend; keep extraction fallback
   via Firecrawl/Exa if needed; store key outside repo.
3. **Memory**: install GBrain, connect Obsidian/vault, define recall/write-back
   rules, establish entity schema.
4. **Controls**: model routing, spend caps, permissions, credential inventory,
   audit cron, escalation rules.
5. **Read-only routines**: daily brief, pre-call brief, signal monitoring,
   contact enrichment reports.
6. **Draft workflows**: investor hooks, content drafts, CRM updates, meeting
   follow-ups.
7. **Approval-gated execution**: sends, publishes, external writes, deletion,
   credential/config changes.
8. **Run/Improve**: weekly QA, cron health, memory dreaming review, model
   routing review, use-case backlog prioritization.

## Acceptance Criteria For A Production Hermes Use Case

- Trigger is explicit: cron, calendar event, user command, folder drop, or API.
- Inputs are enumerated with owner, permissions, and freshness requirement.
- Search/memory order is specified: GBrain recall, You.com, specialist tools,
  then generic web fallback only if needed.
- Output artifact is named and stored in a known location.
- Autonomy level is declared: read-only, draft, approval-gated, or autonomous.
- Human approval rules are written for external side effects.
- Model routing and cost cap are defined.
- Verification checks are defined before the use case is called live.
- Failure mode is explicit: stale source, missing credential, blocked API,
  low-confidence result, runaway cost, or unqualified action.

## Deck Spine

1. Cover.
2. Executive SOP view.
3. Why Hermes is an operating layer.
4. Reference architecture.
5. Source/tool order.
6. You.com search backend spec.
7. GBrain memory spec.
8. Governance and autonomy ladder.
9. Implementation roadmap.
10. Use-case portfolio matrix.
11. Daily brief realization.
12. Smart contacts/entities realization.
13. Pre-call and investor/deal research realization.
14. Signal monitoring and content pipeline realization.
15. Cost/model health and security realization.
16. Lightweight app builder and knowledge compaction realization.
17. SOP templates and acceptance criteria.
18. Chain QA and operating cadence.
19. 30-day rollout plan.
20. Decision and next actions.

## Skill Chaining QA

- Skill/action just run: `ai-analyst` synthesis.
- Intended input consumed: workshop transcript, setup PDF extract, existing
  Hermes use-case doc.
- Actual input consumed: source extract files and `docs/hermes-use-cases-and-realization.md`.
- Intended output produced: validated synthesis and deck spine.
- Actual output produced: this synthesis pack.
- Downstream consumer: branded PPTX builder.
- Evidence the next step can use it: slide-by-slide deck spine, use-case
  taxonomy, acceptance criteria, and source tieout tables.
- Material progress toward acceptance criteria: content is grounded and
  structured before rendering.
- Duplication or overlap with prior pass: none; extends prior use-case note into
  SOP/deck-ready analysis.
- Missing dependency or skipped gate: no current-web lookup; not needed because
  user-provided sources are sufficient.
- Chain status: compound.
- Decision: continue to PPTX render.

## Optional Storm Research Gate

- Skill considered: `storm-research`.
- Decision: not required for this deck pass.
- Reason: `storm-research` is designed for fresh, multi-perspective external
  research with true subagent fan-out and citation verification. This deliverable
  is a client SOP/spec deck grounded primarily in user-provided workshop/setup
  materials and repo notes, so adding a degraded single-agent STORM pass would
  not improve the chain quality.
- Reroute rule: use `storm-research` in a follow-on pass if the deck needs an
  external market validation appendix, competitive benchmark, or citation-heavy
  briefing beyond the Hermes workshop/setup source set.
- Chain status: compound without STORM; optional future research expansion.
