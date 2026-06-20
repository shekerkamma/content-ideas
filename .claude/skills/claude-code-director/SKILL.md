---
name: claude-code-director
description: Use when starting any Claude Code task, automation, or build — apply the Director Framework (Plan First, Manage Context, Verify The Work, Build The System). Encodes the Cole Medin methodology. Trigger phrases: "director mode", "apply the director framework", "plan this properly", "stop vibe coding", "how should I approach this build", "set up a PLAN.md".
argument-hint: [task or project description]
disable-model-invocation: true
---

# Claude Code Director Framework
*Cole Medin × Nate Herk — "How to Build Effective Claude Code Agents in 2026"*

You are not a vibe coder. You are the **director** of your coding agents — the one who sets intent, reviews output, and evolves the system. This skill runs the 4-pillar framework that moves first-pass accuracy from 65% to 92%+.

## Task

$ARGUMENTS

---

## Skill Chains

**Upstream — what feeds INTO this skill:**

| Skill | When to use it first | What it hands off |
|---|---|---|
| `grill-me` | Task is fuzzy — you're not sure what you're building | `brainstorms/{date}-{slug}.md` — read the Structured context block to pre-fill PLAN.md without re-asking |
| `plaid` (Plan phase) | Task is a product feature in a PLAID product arc | `vision.json` + `docs/prd.md` + `docs/product-roadmap.md` — pre-fill PLAN.md sections 1–4 |
| `content-research` / `deep-research` | Task requires domain, competitive, or tech stack research before planning | Second brain notes + research brief → Codebase Analysis context in PLAN.md |

**During execution — behavioral reference:**

| Skill | Role |
|---|---|
| `karpathy-guidelines` | Load as a live behavior reference for any coding work: think before coding, minimum viable solution, surgical edits, goal-driven verification loop. Reinforces Pillars 1 and 3. |

**Downstream — what this skill feeds INTO:**

| Skill | When | What to hand off |
|---|---|---|
| `code-reviewer` | Pillar 3 "Review" step — after tests pass, before marking done | Git diff or list of changed files |
| `skill-builder` | Pillar 4 staircase top rung — when evolution checklist says "make this a skill" | One-paragraph description of the workflow pattern to encode |
| `plaid` (Build phase) | Task is a PLAID product feature | Mark the roadmap checkbox complete in `docs/product-roadmap.md`, then offer `/plaid build` to continue the product arc |

---

## PILLAR 1 — PLAN FIRST

> "You spend more time planning than you actually do building."

The instinct is to jump straight into building. Resist it. An agent with a clear PLAN.md outperforms an agent with a vague prompt every time — because it gets the scope, the order, and the constraints right before a single file is touched.

**Before any implementation, create a PLAN.md with these 6 sections:**

1. **Goal + Success Criteria** — What are we building? What does "done" look like in one crisp sentence?
2. **Codebase Analysis** — What files, directories, APIs, or systems are involved? Use a subagent (Explore type) to map this if the codebase is unfamiliar.
3. **Integration Points** — What existing code/services/workflows will we touch or connect to?
4. **Task Rules** — Conventions to follow. Hard constraints. What NOT to do.
5. **Granular Task List** — Numbered steps, each small enough to complete in one session or one subagent handoff. No "implement the feature" — break it down.
6. **Validation Strategy** — How will you prove it's actually working? Specific commands, checks, or test scenarios.

**Action — before writing a single line of code:**
- If a `grill-me` brainstorm file exists for this task, read it and extract the Structured context block — pre-fill PLAN.md from it instead of re-asking covered questions
- If a PLAID PRD exists (`docs/prd.md`, `vision.json`), read those files and pre-fill sections 1–4 from them
- Otherwise, use AskUserQuestion to pull out all 6 sections one at a time
- If the codebase is unfamiliar, spawn an Explore subagent to map relevant files first
- Don't start implementing until the user confirms the plan

**Pro tip:** If domain or tech stack research is needed before planning, run `/content-research` or `/deep-research` first, then come back. Their notes become your Codebase Analysis context.

**Coding behavior reference:** For any implementation work, load `karpathy-guidelines` as a live behavioral reference — think before coding, simplest solution, surgical edits, goal-driven verification.

---

## PILLAR 2 — MANAGE CONTEXT

> "Attention is scarce. The dumb zone is real."

Every model has a context ceiling after which quality degrades — not obviously, but silently. It starts missing things it knew 50K tokens ago. This is the dumb zone.

**Dumb Zone Thresholds (approximate):**
- Opus 4.8: ~250K tokens
- Opus 4.7: ~200K tokens
- Sonnet 4.6: ~100–125K tokens

**6 Strategies to Stay Sharp:**

1. **Separate sessions** — Break large tasks into phases. Use the RALF loop (below) for multi-session work.
2. **Prime first, not everything** — Load only what's needed for this phase. Don't front-load the whole repo.
3. **Specialized primes** — Skills load on-demand (their descriptions stay in context; full content only loads when invoked). Use this architecture for your own workflows.
4. **On-demand context** — Let the agent discover files when needed rather than pre-loading everything up front.
5. **Git log as memory** — Commit messages carry context across sessions. Write them to be discovered.
6. **Subagents for research** — Delegate investigation to subagents to keep the main context lean.

**Warning signs you've hit the dumb zone:**
- Agent ignores things it knew earlier in the session
- Code quality degrades mid-task
- It stops using skills it should know

**RALF Loop** (for tasks spanning 3+ sessions):
```
Planner (Session 1) → PLAN.md
    ↓
Implementer (Session 2) → reads PLAN.md, executes, writes Execution Report
    ↓
Validator (Session 3) → reads Plan + Report, verifies, closes out
```
Each role gets a fresh context loaded with only what it needs.

**Action:** Before a long session, decide explicitly: what goes in the context up front vs. what gets discovered during execution? If nearing the dumb zone, write a handoff document and start a fresh session.

---

## PILLAR 3 — VERIFY THE WORK

> "Prove to me it's actually done and working."

The difference between 65% and 92% first-pass accuracy is a verification harness. Without it, agents report success when they've technically completed steps — not when the output actually works.

**Verification Pipeline:**
```
Auto-checks → Rules/Lint → Tests → [FAIL → Fix → Re-run] → Review → Real-world check → Ship
```

**For this task, define:**
- What commands run automatically to check correctness? (lint, test, build)
- Can the agent spin up the app/service and test it as a user would?
- For non-code tasks: can output be rendered, previewed, or read visually?
- What edge cases should be tested intentionally?

**The Key Question:** *"How could this go wrong?"*
Build test scenarios around those failure modes. If something breaks, fix it and **re-run the full verification** — don't assume the fix resolved the root cause.

**Useful tools for verification:**
- Playwright for browser automation
- Screenshot → Claude image analysis for visual checks
- CLI output parsing for correctness checks
- Rendering HTML/data + visual review

**Action:** Before finalizing the plan, write the Validation Strategy in PLAN.md Section 6. The agent must complete verification before reporting done. "It ran without errors" is not verification.

**Chain:** After auto-checks and tests pass, invoke `/code-reviewer` on the diff as the "Review" step before shipping.

---

## PILLAR 4 — BUILD THE SYSTEM

> "Every bug is a permanent upgrade."

This is the most important pillar — and the one most people skip. Instead of patching a bug and moving on, treat every failure as a signal about a gap in your system. Fix the system, not just the instance.

**The Staircase (each level raises the floor permanently):**
```
Bug → Rule (CLAUDE.md) → Document → Command → Skill
```

- **Rule:** Add a line to CLAUDE.md so the agent never makes this mistake again
- **Document:** Write a reference doc if the failure revealed missing knowledge
- **Command:** If you fixed it with a bash command, make that command repeatable
- **Skill:** If the fix was a workflow, encode it as a skill for future invocations

**System Evolution Checklist** (run after every session):
- [ ] Did anything go wrong or surprise you?
- [ ] Should a new CLAUDE.md rule prevent that mistake system-wide?
- [ ] Should a new document guide future work in this area?
- [ ] Should this workflow become a reusable skill? → if yes, invoke `/skill-builder [workflow description]`
- [ ] Does this failure reveal a gap in the verification harness?
- [ ] Did anything work better than expected? (Save that too — don't only save corrections)
- [ ] If this was a PLAID product task: mark the roadmap checkbox in `docs/product-roadmap.md`, then offer `/plaid build` to continue

**Security mindset:** Assume that anything the agent can read or touch, it will — even if you never asked it to. Use hooks for guardrails, not prompts. Prompts can be overridden by context; hooks cannot.

---

## Output Format

After running through all 4 pillars interactively with the user, produce:

### 1. PLAN.md

Save to the project root (or path specified in `$ARGUMENTS`):

```markdown
# PLAN.md — [Task Name]
*Generated: [date]*

## Goal + Success Criteria
[One sentence. What does done look like?]

## Codebase Analysis
[Files, directories, services, APIs involved]

## Integration Points
[What existing code/workflows we'll touch]

## Task Rules
- [Constraint or convention]
- [DO NOT: ...]
- [Always: ...]

## Task List
- [ ] 1. [step — specific and small enough for one session]
- [ ] 2. [step]
- [ ] 3. [step]
...

## Validation Strategy
[Specific commands, checks, or scenarios that must pass before task is "done"]
```

### 2. Context Budget Note

Flag explicitly if the task is large enough to require:
- RALF loop (3+ implementation sessions)
- Session splitting with handoff documents
- Subagent delegation for research phases

### 3. Verification Harness

List the specific commands or checks that must pass before the task is complete. Format:
```
Verification gates:
1. [command or check]
2. [command or check]
...
```

### 4. System Evolution Note

One sentence on what rule, document, command, or skill to add after this task completes.

---

## Notes

- Run through all 4 pillars **before** any implementation begins.
- If `$ARGUMENTS` is empty, ask what the user is building before proceeding.
- For large tasks (3+ implementation sessions), recommend RALF loop explicitly.
- Security: surface any MCP servers, file system access, or external API calls that need scoping. Use hooks for hard guardrails.
- Do NOT start implementing until PLAN.md is confirmed by the user.
- After implementation: always run the System Evolution Checklist. Record wins as well as failures.
- The goal is a system that gets smarter with every run — not a single task completed.

---

## Route to next skill

After PLAN.md is confirmed and the task is complete, present this menu:

| # | Option | When |
|---|---|---|
| 1 | `/code-reviewer` | Verification passed — review the diff before shipping |
| 2 | `/skill-builder [workflow]` | Evolution checklist says "make this a skill" |
| 3 | `/plaid build` | Task is part of a PLAID product — mark roadmap and continue |
| 4 | `/grill-me [next task]` | Next task is fuzzy — need discovery before planning |
| 5 | `/content-research` or `/deep-research` | More domain/tech research needed before next PLAN.md |

Present as: "Task complete. Where next?" with the relevant options from the table above (omit ones that don't apply to this task).
