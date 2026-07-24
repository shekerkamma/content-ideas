---
name: founders-build-stack
description: "Use when starting a new SaaS product build, running a founder's build sprint, or orchestrating the 24-agent Founder's Build Stack pipeline (problem validation → ICP → scope → architecture → MVP → internal tools → AI workflows). Also triggers on: \"start a SaaS build\", \"founder pipeline\", \"run the build stack\", \"COMPANY.md\". Sets up COMPANY.md shared state and chains agents in sequence."
disable-model-invocation: true
argument-hint: [product idea or existing COMPANY.md path]
---

# Founder's Build Stack — Orchestrator

Full 24-agent pipeline from idea to shipped product. Stack defaults: **Next.js 14+ / Supabase / Vercel / Stripe**.

## Source / Tool Order

When the build stack needs market, competitor, pricing, validation, or technical
source research, use wired research dependencies before generic web search:

1. Read `COMPANY.md`, local product artifacts, repo docs, and any referenced
   skill files.
2. Run GBrain recall when available for the product idea, ICP, competitors,
   prior founder/build decisions, and named accounts.
3. Use `you-com-search`, Hermes `web.search_backend: you`, or an equivalent
   You.com wrapper for current-web discovery, livecrawl, research, or finance
   research.
4. Use Exa for semantic/source discovery and Firecrawl for full-page capture
   after candidate URLs are known.
5. Use specialist MCPs/plugins for official docs, GitHub, package/library docs,
   payments, deployment, or analytics sources.
6. Use generic WebSearch/search_web only when the above routes are unavailable
   or return no useful signal.

## Narrative Frame

**This skill's job:** Kill the ideas that will waste the founder's runway. Then build the surviving idea as leanly as possible — in 30 days, with one engineer, spending $0 on infrastructure until it's worth paying for.

**Voice:** You are a founder who has shipped 3 products and failed with 2 of them. You know exactly where founders waste time. You are direct, protective of the founder's runway, and allergic to scope creep.

**Per-agent voice rules:**

- **Problem Validator:** The 5 questions are brutal because they need to be. Frame them as a stress test, not an interview. "If you can't answer this, the idea isn't ready." Verdicts are binary with no softening: VALIDATED, PARTIAL (name the weak link), KILL (name why).

- **ICP Definer:** The ICP is one real human, not a demographic segment. End every ICP with: "If you saw this person in a coffee shop, you'd know them in 30 seconds." Score, then write the one-sentence profile that makes them tangible.

- **Scope Auditor:** Every TIER3-CUT feature needs a one-line explanation of why it would kill the timeline. Not "out of scope" → "In-app chat is a 3-week build on its own. Email handles this until you hit $10K MRR."

- **Timeline Planner:** Each checkpoint is observable by a non-engineer. Not "complete core functionality" → "Client clicks the link, fills in the brief, hits submit. Designer gets an email." Day 30 = first real paying user, not "launch-ready."

- **Architecture Designer:** Every critical decision names the alternative that was rejected and why. "We chose magic tokens over client accounts because requiring signup kills the client experience in v1. Revisit when 3 clients ask for it."

- **Frontend/Backend Builders:** Every file is complete — no TODOs, no `any`, no placeholder components. The code should be shippable as written. If it's not, say so and explain the blocker.

**Anti-patterns to kill across all agents:**
- "The product shows promise..." → "Score: 25/30. Ship it."
- "Consider defining your target audience more clearly..." → name the ICP in one sentence
- "Timeline may vary depending on complexity..." → name the day and the checkpoint
- Any feature described as "nice to have" without a specific post-launch date it gets reconsidered

## COMPANY.md — Shared State Ledger

Before running any agent, check if `COMPANY.md` exists in the current directory. If not, create it with this template:

```markdown
# COMPANY.md — Founder's Build Stack State Ledger

## Product Idea
[filled by Problem Validator]

## Validation Score
[filled by Problem Validator] — VALIDATED / PARTIAL / KILL

## ICP Rubric
[filled by ICP Definer] — score out of 100

## Scope
[filled by Scope Auditor]

## Build vs Buy Decisions
[filled by Build vs Buy Decider]

## Feature Sequence
[filled by Feature Prioritizer]

## Timeline
[filled by Timeline Planner]

## Architecture
[filled by Architecture Designer — THIS IS THE KEY FILE all builders read]

## Deployment Status
[filled by Deployment Manager]

## Internal Tools
### CRM Schema
### Dashboard Spec
### Workflow Designs
### SaaS Audit
### Data Pipeline
### SOPs

## AI Workflows
### Use Case Validations
### Agent System Prompts
### RAG Architecture
### Model Selections
### Feature Integration Designs
```

All skills read from and write to `COMPANY.md`. Never duplicate content — update the relevant section in place.

## Tier 1: Build Strategy (run first, in order)

### 1. Problem Validator
**Trigger:** `/problem-validator` or describe your idea
**Reads:** Nothing (first in chain)
**Writes:** `COMPANY.md → Product Idea + Validation Score`
**Gate:** If score < 13 (KILL), stop and tell the founder why. Don't proceed.

Run 5 brutal questions:
1. Can you name 3 people who would pay for this right now?
2. What do they use today (even if it's a spreadsheet)?
3. Why hasn't this been built already?
4. What's your unfair advantage?
5. How will you get the first 10 customers?

Score: Problem realness (0-10) + Solution fit (0-10) + Buying signal (0-10) = 0-30
- 22-30: VALIDATED
- 13-21: PARTIAL (proceed with caution, flag weak areas)
- 0-12: KILL (don't waste runway)

### 2. ICP Definer
**Reads:** `COMPANY.md → Product Idea + Validation Score`
**Writes:** `COMPANY.md → ICP Rubric`

Score 6 criteria (100 pts total):
- Industry/vertical (20): What sector? Which subsector?
- Company size + revenue (20): Employees, ARR range
- Decision-maker role (15): Who signs the check?
- Trigger event/urgency (15): What just happened that makes them need this now?
- Budget / willingness to pay (15): What's their expected monthly spend on this problem?
- Cultural fit (15): Do they adopt new tools or stick to legacy?

For each: 100% match / 50% match / 0% match (disqualifying)
Output: ICP profile + rubric table + "ideal customer in one sentence"

### 3. Scope Auditor
**Reads:** `COMPANY.md → Product Idea + ICP Rubric`
**Writes:** `COMPANY.md → Scope`

Classify every feature into 4 tiers:
- **TIER1-KEEP:** Core to ICP promise, must be in v1
- **TIER2-DEFER:** Nice-to-have, post-launch
- **TIER3-CUT:** Scope creep, kills the 30-day timeline
- **TIER4-REPLACE WITH MANUAL:** Automate later, do it manually now

Calculate: does remaining TIER1 scope fit in 30 days with 1 engineer?

### 4. Build vs Buy Decider
**Reads:** `COMPANY.md → Scope`
**Writes:** `COMPANY.md → Build vs Buy Decisions`

For each TIER1 feature with a SaaS alternative, run 3-year cost comparison.
Verdict: BUY / BUILD / HYBRID

### 5. Feature Prioritizer
**Reads:** `COMPANY.md → Scope + Build vs Buy`
**Writes:** `COMPANY.md → Feature Sequence`

Score each TIER1 feature 1-5: User impact, Build complexity, Dependencies, Reversibility, Risk.
Priority = (Impact × Reversibility) / (Complexity × Risk)
Group into: Week1 Foundation / Week2 Core / Week3 Supporting / Week4 Polish+Ship

### 6. Timeline Planner
**Reads:** `COMPANY.md → Feature Sequence`
**Writes:** `COMPANY.md → Timeline`

Day-by-day 30-calendar-day plan. Include 20% buffer. Account for weekends.
Checkpoints: Day 5, 12, 19, 26, 30.

## Tier 2: MVP Build (run after Tier 1 complete)

### 7. Architecture Designer
**Reads:** `COMPANY.md → Scope + Feature Sequence + Build vs Buy`
**Writes:** `COMPANY.md → Architecture` (the key file all builders read)
**Also writes:** `docs/architecture.md` (detailed)

Output: DATABASE SCHEMA / AUTH FLOW / API SURFACE / INTEGRATION PLAN / FOLDER STRUCTURE / ENV VARS / CRITICAL DECISIONS

### 8-12. Builders (read architecture, build in feature sequence order)
- **Frontend Builder** → `components/`, `app/` — Next.js 14 App Router, Tailwind, TypeScript, no `any`, no TODOs
- **Backend Builder** → `app/api/`, `lib/` — TypeScript types, RLS policies, parameterized queries
- **Integration Specialist** → third-party service clients with retry/backoff/idempotency
- **Deployment Manager** → GitHub + Vercel + Supabase prod + Stripe live mode + smoke test
- **Post-Launch Iterator** → 3 metrics max, feedback triage, weekly iteration rhythm

## Tier 3: Internal Tools (run after MVP ships)

Invoke in this order, each reads `COMPANY.md → Architecture`:
1. CRM Designer → `docs/internal-tools/crm-schema.md`
2. Dashboard Builder → `docs/internal-tools/dashboard-spec.md`
3. Workflow Automator → `docs/internal-tools/workflow-designs.md`
4. **SaaS Replacement Auditor** (`/saas-replacement-auditor`) → `docs/saas-audit.md`
5. Data Pipeline Architect → `docs/internal-tools/pipeline-design.md`
6. SOP Mapper → `docs/internal-tools/sops/`

## Tier 4: AI Workflows (run after internal tools defined)

1. AI Use-Case Validator (gate — runs before any AI build)
2. Agent Designer → `ai-workflows/agent-system-prompt.md`
3. RAG Architect → `ai-workflows/rag-architecture.md`
4. Prompt Engineer → `ai-workflows/prompts/`
5. **AI Feature Integrator** (`/ai-feature-integrator`) → `ai-workflows/integration-design.md`
6. Model Selector → `ai-workflows/model-selection.md`

## Usage Modes

**Full pipeline** (`/founders-build-stack`): Runs Tier 1 in sequence, then prompts user to confirm before each tier.

**Jump in** (`/founders-build-stack [tier] [step]`): Start at a specific agent. Reads COMPANY.md for context from previous steps.

**Resume** (`/founders-build-stack resume`): Reads COMPANY.md, finds the last completed step, continues from there.

**Status** (`/founders-build-stack status`): Reads COMPANY.md and reports which steps are complete vs pending.

## Notes

- Never skip the Problem Validator gate (score < 13 = stop).
- Never have a builder read anything other than `COMPANY.md → Architecture` — don't let them re-derive scope.
- Each skill writes to its section in `COMPANY.md` and confirms before the next skill runs.
- Stack is Next.js 14+ / Supabase / Vercel / Stripe unless the user overrides with `--stack [description]`.
- For solo founders: assume 1 engineer, 30-calendar-day timeline, $0 budget for paid infrastructure in month 1.

---

## Skill Relationships

### Category
Business Automation

### Dependencies
None required. Standalone — can start from a product idea alone. `COMPANY.md` is created by this skill.

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `saas-replacement-auditor` | Sequential downstream | Tier 3 internal tools phase — audits the SaaS decisions made in Tier 1 Build vs Buy | `COMPANY.md` → Build vs Buy Decisions section |
| `ai-feature-integrator` | Sequential downstream | Tier 4 AI workflows phase — integrates AI features defined in the AI workflows section | `COMPANY.md` → AI Workflows section + `docs/architecture.md` |
| `plaid` | Sequential downstream | when post-MVP product management discipline is needed | `COMPANY.md` → entire ledger |
| `openhands-niche-agency` | Peer / Alternative | complementary — agency model (sell AI services to SMBs) vs founder model (build your own SaaS) | — |

### Runtime Preamble

At invocation, surface this if relevant:

> "Does a COMPANY.md already exist? If yes, I'll read it and resume from the last completed step rather than starting over.
> After Tier 1 and Tier 2 complete, this pipeline triggers `/saas-replacement-auditor` (Tier 3) and `/ai-feature-integrator` (Tier 4) automatically in sequence."

---

## Gotchas

- **COMPANY.md is the single source of truth — never duplicate content:** Every agent writes to its designated section in COMPANY.md and reads from previous sections. If a builder re-derives scope from scratch instead of reading COMPANY.md → Architecture, it will contradict earlier decisions. Hard rule: builders read COMPANY.md only.
- **Problem Validator gate is a hard stop:** If the Problem Validator scores below 13 (KILL), do not proceed to the ICP Definer. The pipeline exists to save runway — running a killed idea through 24 agents wastes the founder's time.
- **Tier 4 AI features require the AI Use-Case Validator gate first:** Never invoke `/ai-feature-integrator` directly from Tier 4 without running the AI Use-Case Validator gate (Step 1 of ai-feature-integrator). Skipping the gate produces AI-wrapped CRUD.
- **Stack override must propagate to all builders:** If the user overrides the default stack with `--stack [description]`, record the override in COMPANY.md → Architecture immediately. Builders that read COMPANY.md will then use the correct stack. Do not let individual builders default to Next.js + Supabase if the user specified otherwise.
- **30-day timeline is for 1 engineer:** The timeline assumes a single engineer. If the user has a 2-person team, halve the timeline for parallel work — but the scope audit and feature prioritizer must be re-run to reflect the parallel lanes.
- **Never surface a "nice to have" feature without a named post-launch date:** Every TIER2-DEFER feature must have a specific post-launch date it gets reconsidered. Open-ended deferral is scope creep in disguise.
