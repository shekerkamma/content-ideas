---
name: goal-loop-orchestrator
description: >
  Use when the user wants to refine a goal, choose or chain multiple skills,
  run a compound workflow, execute looping skill passes, or continue until
  acceptance criteria are met. Works across Claude Code and Codex by using
  local skills first, external skill discovery only when needed, explicit
  handoffs, verification checks, and stop conditions.
category: Business Automation
license: MIT
---

# Goal Loop Orchestrator

Turn a vague goal into a verified outcome by refining the goal, selecting the
right skill chain, executing in loops, and stopping only when acceptance
criteria are met or a real blocker is reached.

This is not a replacement for domain skills. It is the controller that decides
which skill to use next, what each pass must produce, and whether the result is
good enough to stop.

## Core Loop

```text
Refine Goal -> Select Skill Chain -> Execute Pass -> Verify -> Improve -> Repeat -> Stop
```

## Reference files (read on demand, not up front)

- `references/strategy-research-policy.md` — REQUIRED before any market, moat,
  wedge, competitive, investment, or pipeline-strategy goal. Research order
  (GBrain → You.com → Exa → Firecrawl → Reddit semantic chain → subagents →
  primary sources), evidence bar, and the Reddit Semantic Evidence Checklist.
- `references/chaining-qa.md` — the Skill Chaining QA gate: chain contract,
  pass-level checks, broken-chain patterns, reroute rules. Run after every pass.
- `references/recipes-relationships-gotchas.md` — reusable recipes, example
  invocation, full skill-relationships table, and the complete gotchas list.

## Operating Rules

1. **Goal first, skills second.** Do not search for or load skills until the
   goal has a clear outcome, artifacts, constraints, acceptance criteria, and
   stop conditions.
2. **Use local skills before external discovery.** Inventory available local
   skills first; search the external ecosystem only for uncovered phases.
3. **Load progressively.** Read only the skill needed for the current phase.
4. **Use real-data research for strategy.** For moat, market, wedge,
   investment, competitive, pipeline, or strategy work, follow
   `references/strategy-research-policy.md`. Generic search is fallback/source
   discovery only, never the evidence base.
5. **Use `ai-analyst` upstream for data synthesis.** Any quantitative question,
   metric, chart, KPI, trend, forecast, cohort, funnel, segmentation, or
   opportunity sizing routes through `ai-analyst` before strategy, narrative,
   or deck rendering.
6. **Use client-ready PPTX skills for decks.** Slide deck, executive deck,
   board deck, PowerPoint, client-ready presentation → `branded-pptx-deck`
   after upstream validation. No ad hoc slides.
7. **Every pass needs a handoff.** Each pass must leave enough context for the
   next pass to continue without re-asking or guessing.
8. **Verification gates completion.** Generation is not completion.
9. **Loops are bounded.** Every run has a loop budget and a hard stop.
10. **Ask before installing external skills.** No remote skills, plugins,
    packages, or global files without explicit user approval.

## Step 1: Refine the Goal Contract

```markdown
## Goal Contract
- Outcome:
- Artifacts:
- Constraints:
- Acceptance criteria:
- Verification:
- Research mode:
- Loop budget:
- Stop conditions:
- Known inputs:
- Missing inputs:
```

Inspect files, repo state, docs, and prior artifacts before asking the user.
Ask only when a missing answer materially changes the workflow and cannot be
inferred safely. For vague requests, propose a recommended contract and let the
user correct it.

Loop budget: default 3 passes; 5 for complex multi-artifact workflows; 1 when
the user asks only for review, advice, or a plan. The budget is total passes
for the whole goal. Exceed it only with user approval after explaining why.

## Step 2: Inventory Skills

Look in host-appropriate roots, metadata first (`name`, `description`, routing
section), full bodies only for candidates matching the next phase:

- Repo-local shared skills: `skills/*/SKILL.md` (preferred — travels with the project)
- Generic project skills: `.agents/skills/*/SKILL.md`
- Claude Code project skills: `.claude/skills/*/SKILL.md`
- Codex global: `~/.codex/skills/*/SKILL.md` · Claude global: `~/.claude/skills/*/SKILL.md`

When installed globally, resolve helper skill paths in this order: repo-local
`skills/<name>/` → `~/.claude/skills/<name>/` → `~/.codex/skills/<name>/` →
`/home/shekerk/content-ideas/skills/<name>/`. If a helper path is missing,
record it and use the next location.

## Step 3: Build the Skill Chain

```markdown
## Skill Chain
| Phase | Skill/action | Why | Input | Output | Verification |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
```

Typical phases: discovery/recall → research → data synthesis → strategy →
product → design → implementation → QA → packaging → memory write-back.
Use the smallest chain that can satisfy the goal.

### Mandatory Skill Routing Matrix

If a trigger matches, insert the required skill unless unavailable; if
unavailable, record the blocker and downgrade the output rather than silently
skipping the route.

| Trigger | Required skill/action | Position | Required handoff |
|---|---|---|---|
| Goal is vague, risky, high-leverage, or needs pressure testing | `grill-me` | Upstream / peer before execution | clarified assumptions, objections, decision notes |
| Any data question, analytical request, metric inquiry, visualization request, quantitative claim, trend, forecast, KPI, cohort, funnel, segmentation, opportunity sizing, or data-backed synthesis | `ai-analyst` via `ask-question` | Upstream before strategy, narrative, or deck | validated findings, source tieout, confidence, charts/tables when applicable |
| Market, moat, wedge, competitive, investment, or pipeline strategy | Strategy research policy (see reference) | Upstream evidence collection | source pack, confidence labels, primary-source tieout, research mode |
| Exa-capable source discovery needed | `exa-api` or Exa MCP | Research discovery before generic search | semantic discovery JSON, source list, rejected leads |
| Important pages need ingestion | `firecrawl` / `firecrawl-pp-cli` | After source discovery | full-page captures with URL, date, status, live/blocked state |
| Buyer pain, skepticism, switching trigger, comparison frame, or workflow language depends on Reddit | `aeo-reddit-opportunity-finder -> reddit-new-factcheck` plus retrieval route | Before accepting buyer-language claims | semantic probes, claim pack, evidence pack, rejection/human-review notes |
| Specific Reddit thread URLs are known | `reddit-seo-pipeline` | Reddit retrieval before factcheck | thread JSON/comment extraction |
| User asks for slide deck, PowerPoint, executive deck, board deck, or client-ready presentation | `branded-pptx-deck` | Downstream after upstream validation | branded PPTX, preview/QA artifacts, deck status |
| User asks for product idea, PRD, roadmap, launch, design, or build plan | BuilderOS chain (`product-planner` etc.; `plaid` only for legacy in-flight builds) | Product planning phase | `docs/prd.md`, roadmap/design docs |
| User asks for coding, review, refactor, or implementation | `karpathy-guidelines` | Implementation/review overlay | explicit assumptions, surgical change plan, verification commands |
| Browser/UI behavior must be verified | `playwright-cli` | QA / verification | screenshots, traces, test output |

Default compound chains:

- Analytical strategy: `ai-analyst -> Strategy Research Policy -> strategy synthesis`.
- Analytical deck: `ai-analyst -> strategy/narrative if needed -> branded-pptx-deck`.
- Market wedge with buyer pain: `GBrain/prior recall -> you-com-search -> exa-api -> firecrawl -> Reddit semantic chain -> ai-analyst validation -> strategy synthesis`.
- Product build: `grill-me if needed -> product-planner -> karpathy-guidelines -> implementation -> verification`.

### Handoff to Claude Code `/goal`

When the execution phase runs as a Claude Code `/goal` (instead of this skill
looping inline), render the Goal Contract as the 5-part loop-engineering prompt:

```
/goal

TASK: [Outcome, phrased as the verb — what to do]
WHY: [who it's for / why it matters — Fable uses this context on long runs]
OUTCOME: [Artifacts — the exact finished result]
CONSTRAINTS: [Constraints + "Stop after N turns." from the loop budget]
VERIFICATION: [Acceptance criteria + Verification, each check naming its proof]
```

- Never hand off without a turn cap in CONSTRAINTS — map it from the loop budget.
- Qualitative acceptance criteria must route through a grader skill with a
  numeric threshold ("loop until `officecli-qa` reports no issues", "score ≥ 8/10")
  so `/goal` can self-verify instead of stopping early or looping blind.
- Recurring re-check goals (monitor → evaluate → adjust → wait, e.g. A/B test
  rounds) belong in `/loop` or a scheduled routine, not an unbounded `/goal`.
- Ops: `/goal` alone = status; `/goal clear` = stop early.

## Step 3.5: Skill Chaining QA Gate

Before executing a chain, and after every loop pass, run the gate in
`references/chaining-qa.md`: fill the Chain Contract, run the pass-level
chaining check, classify the pass (`compound` / `isolated` / `duplicate` /
`blocked` / `reroute`), and apply the reroute rules. A step with no concrete
input, output, downstream consumer, and value test gets removed.

## Step 4: Execute Looping Passes

For each pass: inspect state and previous handoff → select next skill/action →
read its instructions fully → execute → write/update artifacts → verify →
produce a handoff → run the chaining QA gate → decide (stop / continue /
reroute / refine / ask).

```markdown
## Loop State
- Pass:
- Max passes:
- Acceptance criteria met:
- Verification status:
- Material change since previous pass:
- Stop / continue decision:
- Reason:
```

If a pass produces no material change toward the acceptance criteria, stop or
ask. Do not run another pass with the same inputs and same plan.

```markdown
## Handoff
- Phase completed:
- Skill/action used:
- Inputs consumed:
- Artifacts created/changed:
- Decisions made:
- Evidence/checks:
- Open flags:
- Recommended next pass:
```

## Step 5: Verification

Match verification to the work: code → build/lint/tests/typecheck; UI →
browser run + screenshots; research → primary-source citation trail; strategy →
research-grade source mix per the policy reference; data → `ai-analyst`
validation + source tieout; decks → `branded-pptx-deck` QA gates and explicit
`draft`/`reviewed`/`blocked` status; skill creation → frontmatter validity,
trigger clarity, progressive disclosure, host compatibility.

If verification cannot run, explain exactly why and record residual risk.

## Step 6: External Skill Discovery

Only after local inventory shows a gap. Check source reputation, adoption,
repo activity, phase fit, and overlap with local skills. Present candidates as
options with install commands. Ask before installing.

## Stop Conditions

Stop when: acceptance criteria met and verified · loop budget reached · a pass
produced no material change · the next pass would repeat the same action with
the same inputs · remaining improvements are polish only · the same blocker
repeated · the user changes/cancels the goal · continuing would require
installing, purchasing, authenticating, or modifying external/global state
without approval. When stopping on budget/no-progress/polish, report what is
complete, what remains, and what approval or input would justify another pass.

## Key Gotchas (full list in references/recipes-relationships-gotchas.md)

- Do not start with skill search; refine the goal first.
- Do not treat a chain plan as execution.
- Do not mark done without verification; name residual risk if checks can't run.
- Do not validate strategy or Reddit claims with generic search — follow the
  strategy-research-policy reference or label the output `hypothesis`.
- Do not hand-roll data synthesis (`ai-analyst` first) or ad hoc decks
  (`branded-pptx-deck` + QA gates).
- Do not loop past the budget or install external skills silently.

### Runtime Preamble

When this skill triggers, say briefly: "I'll refine the goal first, then run
the smallest skill chain needed and loop until the acceptance criteria are met
or a real blocker appears."
