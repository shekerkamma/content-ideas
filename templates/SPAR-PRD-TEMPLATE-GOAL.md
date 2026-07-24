# SPAR-PRD-TEMPLATE-GOAL

An interview-driven, goal-aligned PRD generator for work you'll run with Claude
Code `/goal`. Merges the **SPAR** structure (Situation · Purpose · Action ·
Result) with the **DBS Framework** (Direction · Blueprints · Solutions) from AI
Foundations — but instead of a static fill-in form, it **interviews you one
question at a time** and produces a PRD whose Success Criteria paste straight
after `/goal`.

**Why interview, not fill-in:** vague goals produce vague builds. The six
questions force specificity, and the DONE question turns the goal into
*verifiable checks* — the real alignment layer.

## Six topics → SPAR → DBS

| Interview topic | SPAR | DBS layer |
|---|---|---|
| SCOPE | Purpose (goal) | Direction |
| STACK | Situation | Blueprints |
| SURFACES | Result | Solutions |
| DATA | Situation + Result | Blueprints / Solutions |
| CONSTRAINTS | Purpose (non-goals) | Blueprints (rules) |
| DONE | Purpose + Result (success criteria) | Solutions (verification) |

---

## The prompt — paste into Claude to run standalone

```
You are helping me write a quick PRD for work I'll do with Claude Code using /goal.
The work might be a new build, a refactor, a bug fix, a script, or any other kind
of project. Interview me first, then write the PRD.

Rules:
- Ask me one question at a time. Wait for my answer before moving on.
- If my answer is vague or I skip something, push back and ask the sharper version.
- Adapt follow-up wording to the kind of project I'm describing (web app, API, CLI,
  script, data pipeline, refactor, etc.) but cover all six topics.
- Do not write the PRD until I've answered all six questions.
- When you have what you need, say "I have what you need" and produce the PRD.

Ask me these six questions, one at a time. Wording can adapt to my project type,
but each question must cover the topic listed:

1. SCOPE — "In one sentence, what are you trying to accomplish? Is this a new build,
   a change to existing code, or something else?"
2. STACK — "What tech stack, language, or tools are involved? If it's existing code
   and you're not sure, tell me and I'll check the repo."
3. SURFACES — "What are the concrete things that will exist or change when this is
   done? List them. Files, functions, API endpoints, CLI commands, pages, database
   tables, or anything else a person could point at."
4. DATA — "What inputs does this take and what outputs does it produce? Include
   anything stored, anything read from somewhere else, and the shape of the data
   if it matters."
5. CONSTRAINTS — "What must NOT change or break? For new builds, what are you
   explicitly cutting from v1? For existing code, what behavior must be preserved
   exactly?"
6. DONE — "How will we know this is finished? List every distinct thing that should
   be true when it works. For each one, tell me how I'd verify it — a command to
   run, a file to check, a behavior to test. The more specific, the better. Also:
   what seed data should exist so the verification is meaningful?"

After all six answers, produce the PRD in this exact structure:

# [Project Name] PRD
## One-Liner
## Stack
## Surfaces
## Data
## Constraints
## Success Criteria

The Success Criteria section must be a numbered list of discrete, verifiable checks
I can paste directly after /goal. Each check must: (a) state one thing that must be
true, and (b) name how Claude should prove it — a command output, a file dump, a
curl response, a test result, or a specific behavior demonstrated in the transcript.
End with a single sentence describing what seed data should exist before
verification runs. The whole section must be copy-pasteable as a /goal condition.

Start with question 1 now.
```

---

## Installed as a skill

This generator is installed at `.claude/skills/spar-prd-goal/`. Run it with
`/spar-prd-goal <project>` instead of pasting the prompt. A worked output example
lives in `.claude/skills/spar-prd-goal/references/template.md`.
