---
name: spar-prd-goal
description: Use when the user wants a quick, goal-aligned PRD for a single unit of work they'll run with Claude Code `/goal` — a new build, refactor, bug fix, script, or one task off a BuilderOS `docs/product-roadmap.md`. Interviews the user one question at a time (six topics), then writes a PRD whose Success Criteria are copy-pasteable as a `/goal` condition. The per-task layer that sits BETWEEN BuilderOS product-planner (macro roadmap) and build-mvp / build-loop (execution). Triggers on "/spar-prd-goal", "SPAR brief", "SPAR PRD", "write a PRD for /goal", "spec this roadmap task for /goal", "give Claude a target to hit". Grounded in SPAR (Situation·Purpose·Action·Result) × the DBS Framework (Direction·Blueprints·Solutions).
argument-hint: [project name or one-line goal]
---

## What This Skill Does

Interviews the user, then writes a **quick PRD** for work they'll do with Claude
Code using `/goal`. The PRD's **Success Criteria** section is built to be pasted
directly after `/goal` — every check names how Claude must prove it.

This is the goal-alignment engine: the six interview topics map onto **SPAR**
(Situation · Purpose · Action · Result), which maps onto the **DBS Framework**
(Direction · Blueprints · Solutions). The DONE topic + Success Criteria are the
measurable target — "give Claude something to hit," made verifiable.

Interview script and PRD output structure: [references/template.md](references/template.md).

## Mapping (why the six topics cover everything)

| Interview topic | SPAR | DBS layer |
|---|---|---|
| SCOPE | Purpose (goal) | Direction |
| STACK | Situation | Blueprints |
| SURFACES | Result (what exists/changes) | Solutions |
| DATA | Situation + Result | Blueprints / Solutions |
| CONSTRAINTS | Purpose (non-goals) | Blueprints (rules) |
| DONE | Purpose + Result (success criteria) | Solutions (verification) |

## Chains with (BuilderOS pipeline)

This skill is the **per-task layer** in the BuilderOS build pipeline:

```
idea-generator → idea-validator → product-planner → design-system → build-mvp / build-loop-*
                                        │                                   ▲
                                        ▼ docs/product-roadmap.md            │
                                   [pick one task] → spar-prd-goal → /goal ──┘
```

- **Upstream:** `product-planner` writes `docs/product-roadmap.md` (checkboxed
  tasks). Take ONE roadmap task as this skill's input instead of a cold prompt —
  pre-fill SCOPE/STACK/SURFACES from `docs/prd.md` and `docs/product-roadmap.md`
  if they exist.
- **Downstream:** hand the PRD's Success Criteria to Claude Code `/goal`, then run
  `build-loop-claude-code` (or `-codex` / `-cursor`) to build → review → test →
  fix that task until the criteria pass.
- Use `build-mvp` instead when the user wants the WHOLE roadmap built at once;
  use `spar-prd-goal` when they want a single task specced with a verifiable
  `/goal` target first.

---

## Workflow — run the interview, then write the PRD

Say this to the user, then begin:

> You are helping me write a quick PRD for work I'll do with Claude Code using
> `/goal`. The work might be a new build, a refactor, a bug fix, a script, or any
> other kind of project. Interview me first, then write the PRD.

### Interview rules
- Ask **one question at a time**. Wait for the answer before moving on.
- If an answer is vague or a topic is skipped, **push back** and ask the sharper
  version.
- Adapt follow-up wording to the project type (web app, API, CLI, script, data
  pipeline, refactor, etc.) but cover **all six** topics.
- Do **not** write the PRD until all six questions are answered.
- When you have enough, say **"I have what you need"** and produce the PRD.

### The six questions (ask one at a time; wording adapts, topic must not change)

1. **SCOPE** — "In one sentence, what are you trying to accomplish? Is this a new
   build, a change to existing code, or something else?"
2. **STACK** — "What tech stack, language, or tools are involved? If it's existing
   code and you're not sure, tell me and I'll check the repo."
3. **SURFACES** — "What are the concrete things that will exist or change when
   this is done? List them — files, functions, API endpoints, CLI commands,
   pages, database tables, anything a person could point at."
4. **DATA** — "What inputs does this take and what outputs does it produce?
   Include anything stored, anything read from elsewhere, and the shape of the
   data if it matters."
5. **CONSTRAINTS** — "What must NOT change or break? For new builds, what are you
   explicitly cutting from v1? For existing code, what behavior must be preserved
   exactly?"
6. **DONE** — "How will we know this is finished? List every distinct thing that
   should be true when it works. For each, tell me how I'd verify it — a command
   to run, a file to check, a behavior to test. The more specific, the better.
   Also: what seed data should exist so the verification is meaningful?"

### Output — produce the PRD in this exact structure

```
# [Project Name] PRD
## One-Liner
## Stack
## Surfaces
## Data
## Constraints
## Success Criteria
```

**Success Criteria** must be a numbered list of discrete, verifiable checks the
user can paste directly after `/goal`. Each check must:
(a) state one thing that must be true, and
(b) name how Claude should prove it — a command output, a file dump, a curl
    response, a test result, or a specific behavior demonstrated in the transcript.

End the section with a single sentence describing what **seed data** should exist
before verification runs. The whole section must be copy-pasteable as a `/goal`
condition.

---

## Rules
- One question at a time. Never batch the interview.
- No PRD until all six topics are answered — push back on vague answers.
- Success Criteria must be verifiable, not aspirational. Every check names its proof.
- Keep it tight: verdict-first, numbers over adjectives (see `~/.claude/skills/voice.md`).
