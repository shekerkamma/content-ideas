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

Use this loop for compound work such as product builds, research-to-deck
pipelines, code implementation, strategy briefs, audits, launches, and other
tasks where one skill is not enough.

## Operating Rules

1. **Goal first, skills second.** Do not search for or load skills until the
   goal has a clear outcome, artifacts, constraints, acceptance criteria, and
   stop conditions.
2. **Use local skills before external discovery.** Inventory available local
   skills first. Search the external ecosystem only when local skills do not
   cover a required phase.
3. **Load progressively.** Read only the skill needed for the current phase.
   Do not load every plausible skill up front.
4. **Use real-data research for strategy.** For moat, market, wedge,
   investment, competitive, pipeline, or strategy work, the default is not a
   lightweight scan. Probe for and use You.com, Reddit evidence tools, Exa,
   Firecrawl, durable memory, specialist research skills, primary sources, and
   deep-research subagents where available. Generic search is fallback/source
   discovery only, never the evidence base.
5. **Use `ai-analyst` upstream for data synthesis.** For any quantitative
   question, metric, dataset, chart, KPI, trend, forecast, cohort, funnel,
   segmentation, opportunity sizing, or data-backed synthesis, route through
   `ai-analyst` before strategy, narrative, or deck rendering.
6. **Use client-ready PPTX skills for decks.** When the user asks for a slide
   deck, executive deck, board deck, PowerPoint, or client-ready presentation,
   route to `branded-pptx-deck` after upstream validation. Do not create ad hoc
   slides or unreviewed deck artifacts.
7. **Every pass needs a handoff.** Each skill/action pass must leave enough
   context for the next pass to continue without re-asking or guessing.
8. **Verification gates completion.** Generation is not completion. Stop only
   after checking the result against the acceptance criteria and running the
   available verification steps.
9. **Loops are bounded.** Every run must have a loop budget and a hard stop.
   Do not continue just because the output could be improved.
10. **Ask before installing external skills.** Do not install remote skills,
   plugins, packages, or global files without explicit user approval.

## Step 1: Refine the Goal Contract

Convert the user's request into a short goal contract:

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

If missing information can be discovered from files, repo state, docs, or prior
artifacts, inspect those before asking the user. Ask only when a missing answer
materially changes the workflow and cannot be inferred safely.

For vague requests, propose a recommended contract and let the user correct it.
For direct execution requests, proceed with the best reasonable contract.

Set a loop budget in the contract:

- Default: 3 passes for ordinary tasks.
- Use 5 passes for complex multi-artifact workflows.
- Use 1 pass when the user asks only for review, advice, or a plan.
- Treat the budget as total passes for the whole goal, not passes per skill.
- Exceed the budget only after telling the user why another pass is needed and
  receiving approval.

## Step 2: Inventory Skills

Look for available skills in host-appropriate roots:

- Repo-local shared skills: `skills/*/SKILL.md`
- Generic project skills: `.agents/skills/*/SKILL.md`
- Claude Code project skills: `.claude/skills/*/SKILL.md`
- Codex global skills: `~/.codex/skills/*/SKILL.md`
- Claude global skills: `~/.claude/skills/*/SKILL.md`

Prefer repo-local skills when they exist because they travel with the project
and work across Claude Code and Codex.

When inventorying, read metadata first: `name`, `description`, and any routing
section. Load full skill bodies only for candidates that match the next phase.

When this skill is installed globally, resolve helper skill paths in this order:

1. Repo-local `skills/<skill-name>/...` under the current project.
2. Global Claude Code `~/.claude/skills/<skill-name>/...`.
3. Global Codex `~/.codex/skills/<skill-name>/...`.
4. This repo's shared skill root: `/home/shekerk/content-ideas/skills/<skill-name>/...`.

Do not assume relative `skills/...` paths exist when Claude Code is launched
from another project. If a helper path is missing, record the missing path and
use the next available location.

## Step 3: Build the Skill Chain

Create a chain plan before execution:

```markdown
## Skill Chain
| Phase | Skill/action | Why | Input | Output | Verification |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
```

Typical phases:

- Discovery / recall
- Research / evidence collection
- Data synthesis / validation
- Strategy / synthesis
- Product / requirements
- Design / UX
- Implementation
- QA / review
- Packaging / delivery
- Memory / write-back

Do not force every phase. Use the smallest chain that can satisfy the goal.

Mandatory routing:

- Data or analytical synthesis: insert `ai-analyst` upstream. Its `ask-question`
  entry point is the mandatory route for analytical questions, and its validated
  findings/charts become the handoff artifact for downstream strategy or decks.
- Client-ready deck or PowerPoint output: insert `branded-pptx-deck` as the
  render stage. The deck must be built from validated upstream content, use the
  branded PPTX workflow, and pass PPTX QA before being called final.
- If the user asks for both analysis and a deck, the default chain is:
  `ai-analyst -> strategy/narrative skill if needed -> branded-pptx-deck`.

### Mandatory Skill Routing Matrix

Use this matrix before finalizing the skill chain. If a trigger matches, insert
the required skill in the listed position unless the skill is unavailable; if it
is unavailable, record the blocker and downgrade the output rather than silently
skipping the route.

| Trigger | Required skill/action | Position | Required handoff |
|---|---|---|---|
| Goal is vague, risky, high-leverage, or needs pressure testing | `grill-me` | Upstream / peer before execution | clarified assumptions, objections, decision notes |
| Any data question, analytical request, metric inquiry, visualization request, quantitative claim, trend, forecast, KPI, cohort, funnel, segmentation, opportunity sizing, or data-backed synthesis | `ai-analyst` via `ask-question` | Upstream before strategy, narrative, or deck | validated findings, source tieout, confidence, charts/tables when applicable |
| Market, moat, wedge, competitive, investment, or pipeline strategy | Strategy research policy | Upstream evidence collection | source pack, confidence labels, primary-source tieout, research mode |
| Exa-capable source discovery needed | `exa-api` or Exa MCP | Research discovery before generic search | semantic discovery JSON, source list, rejected leads |
| Important pages need ingestion | `firecrawl` / `firecrawl-pp-cli` | After source discovery | full-page captures with URL, date, status, live/blocked state |
| Buyer pain, skepticism, switching trigger, comparison frame, or workflow language depends on Reddit | `aeo-reddit-opportunity-finder -> reddit-new-factcheck` plus retrieval route | Before accepting buyer-language claims | semantic probes, claim pack, evidence pack, rejection/human-review notes |
| Specific Reddit thread URLs are known | `reddit-seo-pipeline` | Reddit retrieval before factcheck | thread JSON/comment extraction |
| User asks for slide deck, PowerPoint, executive deck, board deck, or client-ready presentation | `branded-pptx-deck` | Downstream after upstream validation | branded PPTX, preview/QA artifacts, deck status |
| User asks for product idea, PRD, roadmap, launch, design, or build plan | `plaid` | Product planning phase | `vision.json`, `docs/prd.md`, roadmap/design docs |
| User asks for coding, review, refactor, or implementation | `karpathy-guidelines` | Implementation/review overlay | explicit assumptions, surgical change plan, verification commands |
| Browser/UI behavior must be verified | `playwright-cli` | QA / verification | screenshots, traces, test output |

Default compound chains:

- Analytical strategy: `ai-analyst -> Strategy Research Policy -> strategy synthesis`.
- Analytical deck: `ai-analyst -> strategy/narrative if needed -> branded-pptx-deck`.
- Market wedge with buyer pain: `GBrain/prior recall -> you-com-search -> exa-api -> firecrawl -> Reddit semantic chain -> ai-analyst validation -> strategy synthesis`.
- Product build: `grill-me if needed -> plaid -> karpathy-guidelines -> implementation -> verification`.

## Step 3.5: Skill Chaining QA Gate

Before executing a chain, and after every loop pass, verify that the selected
skills are compounding toward the goal instead of running as isolated motions.

### Chain Contract

For every skill/action in the chain, define:

```markdown
## Chain Contract
| Step | Skill/action | Consumes | Produces | Next consumer | Value test |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
```

Definitions:

- `Consumes`: the exact artifact, source pack, decision, file, URL list, prior
  run output, or user input the skill must use.
- `Produces`: the exact artifact, evidence, decision, file, or state change the
  skill must leave behind.
- `Next consumer`: the downstream skill/action that will use the output.
- `Value test`: the observable reason this step moves the goal closer to the
  acceptance criteria.

If a step has no concrete input, no concrete output, no downstream consumer,
and no value test, remove it from the chain or mark it as optional/advisory.

### Pass-Level Chaining Check

After each skill/action pass, answer these checks before continuing:

```markdown
## Skill Chaining QA
- Skill/action just run:
- Intended input consumed:
- Actual input consumed:
- Intended output produced:
- Actual output produced:
- Downstream consumer:
- Evidence the next step can use it:
- Material progress toward acceptance criteria:
- Duplication or overlap with prior pass:
- Missing dependency or skipped gate:
- Chain status: compound / isolated / duplicate / blocked / reroute
- Decision: continue / revise chain / stop / ask user
```

Use these statuses:

- `compound`: output was consumed or is ready for the named downstream consumer,
  and the goal measurably advanced.
- `isolated`: the skill completed but produced no useful handoff or no
  downstream step can consume it.
- `duplicate`: the skill repeated prior work without adding materially better
  evidence, decisions, implementation, or verification.
- `blocked`: the skill could not run or could not produce the required handoff.
- `reroute`: the selected skill was the wrong tool for the phase; revise the
  chain before continuing.

### Broken Chain Patterns

Stop and revise the chain when any of these appear:

- A skill produces output that no later skill reads.
- A downstream skill ignores the upstream artifact and starts from scratch.
- Two skills perform the same discovery, research, synthesis, or QA without a
  distinct role.
- A skill only restates the goal or produces advice when the chain needs an
  artifact, evidence pack, decision, implementation, or verification.
- A skill succeeds operationally but does not move any acceptance criterion.
- Evidence discovery is treated as validation without the required qualifying
  skill, such as Reddit discovery without `reddit-new-factcheck`.
- Deck, strategy, PRD, or implementation work begins before required upstream
  evidence or planning gates are satisfied.
- Generic WebSearch/search_web bypasses wired search dependencies when
  You.com, Exa, Firecrawl, or specialist tools are available.
- A loop continues after a pass produced no material change.

### Reroute Rules

If a pass is `isolated`, `duplicate`, or `reroute`:

1. Stop the current chain before starting another skill.
2. Identify the missing handoff or wrong assumption.
3. Rewrite the Chain Contract for the remaining steps.
4. Remove any skill that has no concrete value test.
5. Continue only if the revised chain has a named next consumer and verification
   path.

If a pass is `blocked`, try one local fallback that preserves the same handoff
contract. If the same blocker repeats, stop and report the blocker rather than
running unrelated skills.

## Strategy Research Policy

Use this policy when the goal involves market maps, moats, wedges, competitive
strategy, investment theses, pipeline strategy, buyer pain, or strategic options.

Default mode is `validated-research`. A run may switch to `hypothesis` only
when required tools are unavailable/blocked or the user explicitly asks for a
fast scan. Record the mode in the goal contract and final handoff.

Research order:

1. Durable memory / prior work: GBrain, repo run artifacts, brainstorms, prior
   strategy briefs, pipeline outputs.
2. Specialist local skills: `strategy-consulting`, `disruptive-teardown-pipeline`,
   `saas-gap-analyzer`, `content-ideas` strategy mode, `pipeline-runner`, or the
   closest project-specific research skill.
3. Capability probe: before external research, check which research routes are
   available in the host:
   - CLI: `command -v exa`, `command -v firecrawl-pp-cli`,
     `command -v firecrawl`, `command -v reddit`, plus repo scripts such as
     `skills/you-com-search/scripts/search.py`,
     `skills/exa-api/scripts/exa_search.sh`,
     `skills/aeo-reddit-opportunity-finder/scripts/find_opportunities.py`,
     `skills/reddit-new-factcheck/scripts/*`, and
     `skills/reddit-seo-pipeline/scripts/*`.
   - MCP/plugin: Exa (`mcp__claude_ai_Exa__web_search_exa` or equivalent),
     Firecrawl (`mcp__firecrawl__*` or `/firecrawl`), Hermes
     `web.search_backend: you`, Reddit/browser research plugins, and
     host-provided tool discovery.
   - Subagents: Claude `Task`, Codex-discovered multi-agent tools, MCP
     subagent servers, or another available host-provided multi-agent route.
4. You.com: use `you-com-search`, Hermes `web.search_backend: you`, or an
   equivalent You.com API wrapper before generic WebSearch for broad current
   web discovery, livecrawl, research, or finance research. Treat You.com
   output as candidate source material unless the API returned full cited
   research output.
5. Exa: use Exa or an equivalent semantic search tool for source discovery when
   available. Prefer it over generic web search for competitors, categories,
   buyer-language pages, forums, docs, and market signals. In this repo, if no
   Exa MCP tool is exposed, use `exa-api/scripts/exa_search.sh` from the
   resolved helper skill path when `EXA_API_KEY` is set.
6. Firecrawl: use Firecrawl or an equivalent crawler/reader to ingest important
   pages discovered by Exa, especially vendor pricing, docs, support pages,
   changelogs, review pages, and forum threads. In this repo, prefer
   `firecrawl-pp-cli` through `skills/firecrawl/SKILL.md`; if the CLI is
   installed but sandbox networking blocks the API, request escalation or mark
   Firecrawl blocked.
7. Reddit evidence: when buyer pain, skepticism, switching triggers, comparison
   frames, or workflow language matter, use the repo's custom Reddit skill
   chain. Do not substitute simple web search or an Exa `site:reddit.com` query
   for this chain.
   - First run `aeo-reddit-opportunity-finder` to create semantic Reddit probes
     by buyer job, software failure, switching trigger, skepticism, comparison
     frame, and pattern validation. The probes define what meaning to retrieve;
     they are not evidence.
   - Then use the best available Reddit retrieval route: supplied thread URLs
     with `reddit-seo-pipeline`, logged-in Reddit/browser research,
     `you-com-search` or Exa as Reddit discovery assistants, ScrapeCreators, or
     `reddit-new-factcheck/scripts/old_reddit_evidence.py`.
   - Then run `reddit-new-factcheck` as the qualification gate against focused
     claims. Raw Reddit search output, raw old.reddit HTML, and raw thread JSON
     are discovery only.
   - Accept Reddit evidence only when it passes semantic qualification:
     relevant subreddit/source context, matching buyer/practitioner persona,
     matching workflow language, and a concrete pain, workaround, objection,
     switching trigger, comparison frame, or adoption signal.
   - Reject keyword-only matches, generic AI chatter, off-topic subreddits,
     company-name-only mentions, and broad/noisy threads even if a script marks
     them as weak support. Add a human-review note when rejection depends on
     judgment.
   - If the custom Reddit skills are unavailable or no qualified Reddit evidence
     is found, record `no qualified Reddit evidence` and keep the claim as a
     validation gap. Do not present buyer pain as Reddit-validated.
7. Subagents: for deep research, spawn focused research subagents when the host
   supports them. Use parallel subagents for independent questions such as:
   incumbent/pricing map, Reddit/buyer-pain mining, regulatory/procurement
   risk, and workflow/job-post evidence. Do not duplicate the same task across
   agents.
8. Primary sources: vendor docs, pricing pages, SEC filings, official blogs,
   regulatory filings, public datasets, court/agency documents, GitHub repos,
   customer docs, implementation guides.
9. Community and buyer-language evidence: Reddit, forums, review sites,
   customer interviews, job posts, support docs, changelogs. Use these to prove
   pain, not as the only market map.
10. Generic web search: fallback only for source discovery or when richer tools
   are unavailable. It cannot by itself satisfy strategy evidence requirements.
   If generic search is used because better tools are unavailable, switch the
   run to `hypothesis` mode and say why.

Minimum evidence bar for `validated-research` strategy:

- GBrain/prior-artifact recall attempted or completed.
- Specialist local skill selected for the strategy shape.
- Exa/semantic discovery used when available.
- Firecrawl/full-page ingestion used for important discovered pages when
  available.
- Reddit/community/operator evidence used through the custom semantic Reddit
  chain when buyer pain, switching triggers, skepticism, comparison frames, or
  workflow language are part of the claim. If the chain returns no qualified
  evidence, the run may still validate market/pricing facts from primary
  sources, but buyer-language Reddit validation remains open.
- At least one primary source backs each hard company, pricing, regulatory,
  funding, product, or date claim.
- Subagents spawned for deep research when the host supports them and the
  research has independent streams worth parallelizing.

Subagent prompt requirements:

- Scope one research question only.
- Name the target industry, buyer, workflow, and geography.
- State required source types and banned source types.
- Require exact URLs, dates/access dates, source category, confidence, and
  extracted evidence snippets.
- Require rejected leads and why they were rejected.
- Require a concise answer plus a source table, not a narrative essay.
- Treat subagent outputs as leads. The main agent must reconcile conflicts,
  verify important claims, and decide final confidence.

For moat or wedge recommendations, require at least one of:

- direct buyer/user pain evidence,
- incumbent pricing/onboarding/workflow friction,
- regulatory or procurement forcing function,
- workflow evidence from docs, support pages, reviews, forums, or job posts,
- credible proof of budget or existing spend category.

If the evidence is only vendor marketing pages, generic search results, or
unscreened community chatter, the output is `hypothesis` mode, not validated
strategy.

If You.com, Exa, Firecrawl, Reddit tools, and subagents are all unavailable, either ask
whether to proceed with a hypothesis-level scan or produce a research plan with
the exact tools/data needed. Do not present the result as a validated strategy.

### Reddit Semantic Evidence Checklist

Use this checklist whenever a strategy claim depends on buyer/operator language,
skepticism, switching behavior, workflow pain, or comparison frames:

1. Create a focused claim document. Include only the claims Reddit can validate;
   keep market-size, pricing, date, funding, and regulatory claims in the
   primary-source track.
2. Create or reuse an AEO-style run folder with:
   - `manifest.json`
   - `stage_outputs/queries.jsonl`
   - optional `normalized/pattern_candidates.jsonl`
   - optional `normalized/pattern_reviews.jsonl`
3. Run `aeo-reddit-opportunity-finder` to generate semantic probes:

   ```bash
   python3 skills/aeo-reddit-opportunity-finder/scripts/find_opportunities.py runs/<run-id>
   ```

4. Run `reddit-new-factcheck` to prepare focused claims:

   ```bash
   python3 skills/reddit-new-factcheck/scripts/prepare_factcheck.py \
     --input <focused-claims.md> \
     --topic "<topic>" \
     --out-dir runs/<reddit-factcheck-run>
   ```

5. Retrieve Reddit evidence with known thread URLs, `reddit-seo-pipeline`,
   logged-in Reddit/browser research, ScrapeCreators, or the fallback collector:

   ```bash
   python3 skills/reddit-new-factcheck/scripts/old_reddit_evidence.py \
     --claim-pack runs/<reddit-factcheck-run>/claim-pack.json \
     --out-dir runs/<reddit-factcheck-run>/reddit-evidence-raw
   ```

6. Score retrieved Reddit JSON through `reddit-new-factcheck`.
7. Review accepted evidence manually. Reject false positives when the subreddit,
   persona, workflow, or pain signal is off-topic. Record rejections in a
   `human-review.md` or equivalent artifact.
8. Report one of these statuses:
   - `qualified Reddit support`
   - `weak qualified Reddit support`
   - `contradicted by Reddit evidence`
   - `no qualified Reddit evidence`
   - `primary-source required`

Never use Reddit thread counts, raw keyword hits, generic search snippets, or
off-topic weak matches as proof of demand.

## Step 4: Execute Looping Passes

For each loop pass:

1. Inspect current state and previous handoff.
2. Select the next skill or direct action.
3. Read the required skill instructions fully before acting.
4. Execute the phase.
5. Write or update artifacts.
6. Verify phase output.
7. Produce a handoff.
8. Run the Skill Chaining QA gate.
9. Decide: stop, continue, reroute, refine, or ask.

Track loop state explicitly:

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

Use this handoff shape:

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

Match verification to the work:

- Code: build, lint, tests, typecheck, relevant smoke test.
- UI: browser run, screenshots, responsive checks, visual overlap checks.
- Research: current sources, primary-source preference, citation trail.
- Strategy: research-grade source mix, buyer pain proof, incumbent friction,
  counterarguments, decision clarity, and confidence level.
- Data synthesis: `ai-analyst` validation, source tieout, metric definition,
  confidence scoring, and chart quality review when charts are produced.
- Decks: `branded-pptx-deck`, branded template/toolkit, upstream validation,
  text overflow/collision checks, preview review, and explicit
  `draft`/`reviewed`/`blocked` status.
- Data: schema validation, sample rows, edge cases, reproducibility.
- Skill creation: frontmatter validity, trigger clarity, progressive disclosure,
  host compatibility, and a realistic example invocation.

If verification cannot run, explain exactly why and record residual risk.

## Step 6: External Skill Discovery

Use external skill discovery only after local inventory shows a gap.

Candidate quality checks:

- Source reputation.
- Install count or visible adoption.
- Repository activity.
- Fit to the current phase.
- Overlap with existing local skills.
- Whether the skill adds instructions, scripts, or assets that are truly needed.

Present external candidates as options with install commands. Ask before
installing. If the user declines, continue with local/general capability.

## Stop Conditions

Stop the loop when one of these is true:

- Acceptance criteria are met and verification has passed.
- The loop budget has been reached.
- A pass produced no material change toward the acceptance criteria.
- The next pass would repeat the same skill/action with the same inputs.
- The remaining improvements are merely polish and not required by the
  acceptance criteria.
- The same blocker has repeated and no meaningful progress is possible without
  user input or an external state change.
- The user changes or cancels the goal.
- Continuing would require installing, purchasing, authenticating, or modifying
  external/global state without approval.

When stopping because of budget, no-progress, or polish-only improvements,
report what is complete, what remains, and what specific user approval or new
input would justify another pass.

## Reusable Recipes

When a workflow is likely to recur, capture the chain as a reusable recipe in
the final response or a local artifact if the user asks.

Example recipe format:

```markdown
## Recipe: Research-to-Deck
1. Recall / prior context -> notes
2. Research -> source pack
3. Strategy synthesis -> brief
4. Branded deck -> draft
5. Deck QA -> reviewed deliverable
6. Write-back -> durable memory
```

## Example Invocation

Sample user prompt:

```text
I have a rough idea for an AI support triage tool. Refine the goal, pick the
right skills, and get me to a verified PRD plus build plan.
```

Expected behavior:

```markdown
## Goal Contract
- Outcome: verified PRD and build plan for an AI support triage tool
- Artifacts: `vision.json`, `docs/prd.md`, `docs/product-roadmap.md`
- Constraints: use local repo skills first; no external installs without approval
- Acceptance criteria: PRD covers users, workflows, data, risks, MVP scope, and roadmap
- Verification: validate PLAID outputs and check roadmap tasks are actionable
- Loop budget: 3 total passes
- Stop conditions: validated artifacts exist, budget reached, or missing product input blocks progress

## Skill Chain
| Phase | Skill/action | Why | Input | Output | Verification |
|---|---|---|---|---|---|
| 1 | `plaid` plan | Product idea -> PRD/roadmap | rough idea | `vision.json`, docs | schema/doc validation |
| 2 | `karpathy-guidelines` overlay | Keep build plan surgical and verifiable | PRD/roadmap | tightened roadmap | acceptance criteria check |
| 3 | direct review | Confirm completeness | generated docs | final handoff | residual risk list |

## Loop State
- Pass: 1
- Max passes: 3
- Acceptance criteria met: no
- Verification status: pending product artifact generation
- Material change since previous pass: goal contract and chain selected
- Stop / continue decision: continue
- Reason: artifacts do not exist yet
```

## Skill Relationships

### Category
Business Automation

### Dependencies
None required. Optional external discovery may use `npx skills`, web research,
or host-provided tool discovery when available, but only after local skills are
insufficient and user approval is obtained for installs.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `grill-me` | Upstream / peer | when the goal needs deep discovery or stress-testing | `brainstorms/{date}-{slug}.md` |
| `ai-analyst` | Required upstream | for any data question, quantitative synthesis, metric, chart, forecast, segmentation, funnel, cohort, or opportunity sizing | validated findings, analysis JSON, chart PNGs, confidence/validation notes |
| `strategy-consulting` / strategy research policy | Research/synthesis | when the goal involves market maps, moats, wedges, competitive strategy, investment thesis, or pipeline strategy | source-backed strategy brief, confidence labels, research mode |
| `you-com-search` | Research discovery | when current web search, livecrawl, research, finance research, or Reddit/forum candidate URL discovery is needed | You.com result JSON, candidate source URLs, cited research output |
| `exa-api` | Research discovery | when semantic source discovery, competitor discovery, buyer-language page discovery, docs, forums, or market signals are needed | Exa discovery JSON, source candidates, rejected leads |
| `firecrawl` | Research ingestion | when important pages need full-page capture after discovery | Firecrawl JSON/markdown captures with status/source metadata |
| `plaid` | Sequential downstream | when the refined goal is a product idea, PRD, roadmap, design, launch, or build | `vision.json`, `docs/*.md` |
| `karpathy-guidelines` | Behavioral overlay | during coding, review, or refactoring passes | verification-oriented implementation plan |
| `content-ideas` | Sequential downstream | when the goal is social/content research or idea generation | dated research feed |
| `aeo-reddit-opportunity-finder` | Required upstream for Reddit validation | when buyer-language, skepticism, switching, workflow pain, or comparison-frame evidence is needed from Reddit | semantic Reddit probes and opportunity report |
| `reddit-new-factcheck` | Required qualification gate for Reddit validation | after semantic probes or thread discovery produce candidate Reddit sources | claim pack, evidence pack, fact-check report, rejection notes |
| `reddit-seo-pipeline` | Reddit extraction helper | when specific Reddit thread URLs are known | thread JSON and extracted comments |
| `branded-pptx-deck` | Required downstream | when the output is a slide deck, PowerPoint, executive deck, board deck, or client-ready presentation | reviewed PPTX and QA artifacts |
| `playwright-cli` | Verification downstream | when browser/UI validation is needed | screenshots, traces, test output |

### Runtime Preamble
When this skill triggers, say briefly: "I’ll refine the goal first, then run the
smallest skill chain needed and loop until the acceptance criteria are met or a
real blocker appears."

## Gotchas

- **Do not start with skill search.** A skill chain selected before the goal is
  refined usually optimizes for tools instead of outcomes.
- **Do not load all candidate skills.** Metadata first, full instructions only
  when the phase needs that skill.
- **Do not treat a chain plan as execution.** The loop must actually run the
  selected phases unless the user asked only for a plan.
- **Do not mark done without verification.** If checks are unavailable, say so
  and name the residual risk.
- **Do not validate strategy with simple search.** For moat, wedge, market, and
  pipeline work, generic web search can find leads but cannot by itself prove
  buyer pain or defensibility. Use You.com/specialist research routes first or
  label the output as a hypothesis.
- **Do not choose hypothesis mode for convenience.** For strategy work,
  `validated-research` is the default. Use `hypothesis` only when tools are
  unavailable/blocked or the user explicitly asks for a fast scan.
- **Do not hand-roll data synthesis.** If the work involves metrics, datasets,
  charts, quantitative findings, trends, cohorts, funnels, forecasts, or
  opportunity sizing, route through `ai-analyst` first and use its validated
  findings as the handoff.
- **Do not make ad hoc decks.** If the user asks for slides, PowerPoint,
  executive/board deck, or client-ready presentation, route to
  `branded-pptx-deck` and its QA gates. Do not present a deck as final without
  branded PPTX validation and preview review.
- **Do not skip the capability probe.** For strategy research, explicitly check
  for You.com, Reddit, Exa, Firecrawl, and subagent routes before falling back.
  Missing tools are a limitation to report, not a reason to pretend the
  evidence is stronger than it is.
- **Do not use simple search as Reddit validation.** Reddit claims must go
  through semantic probes, focused claims, retrieval, qualification, and human
  review when needed. Raw Exa `site:reddit.com` hits, old.reddit search output,
  or script weak-support false positives are not qualified evidence.
- **Do not accept off-topic Reddit rows.** If subreddit/source context,
  practitioner persona, workflow language, or concrete pain/objection/switching
  signal is missing, reject the row and report `no qualified Reddit evidence`.
- **Do not loop forever.** Respect the loop budget. Stop on no-progress,
  repeated actions, or polish-only remaining work.
- **Do not install external skills silently.** Discovery can be automatic;
  installation requires approval.
- **Do not let handoffs get vague.** Each handoff must say what changed, where
  the artifact is, what was verified, and what remains open.
