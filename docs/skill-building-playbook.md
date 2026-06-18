# Skill-Building Playbook

This is a reusable approach for building any new skill in this repo or in an OpenHands-style workspace.

It combines:
- the six-step workflow from Brandon's video `Claude Code Skills: Automate Everything You Do`
- the practical host setup ideas from `/mnt/c/Users/sheke/Downloads/cheat-sheet.md`
- the OpenHands skill model from `docs.openhands.dev` and `github.com/OpenHands/OpenHands`

## Outcome

The goal is not "write a markdown file."

The goal is:
1. Pick a task worth automating.
2. Run it manually with the agent once.
3. Capture your preferences and edge cases.
4. Turn that learned workflow into an on-demand skill.
5. Test it, iterate it, and only then share it.

## The Core Rule

Do not start by writing the skill.

Start by running the task manually with the agent and giving feedback step by step. The skill should be a compressed version of a workflow you already validated.

This is the main point from the video, and it is the most important one.

## The 7-Stage Method

### 1. Choose the right task

A task is a good skill candidate if it is:
- repeated
- opinionated
- multi-step
- easy to judge as right or wrong
- likely to benefit from scripts, references, or tool rules

Good examples:
- release prep
- research brief creation
- transcript cleanup
- PR review
- pipeline QA

Bad examples:
- one-off brainstorming
- vague strategy work with no stable output format
- tasks where you still do not know your own process

### 2. Run the task manually first

Open a normal session and do the work manually with the agent.

Tell it:
- the goal
- the output you want
- the order of operations
- your preferences for tone, format, tools, and review points

While it works, correct it aggressively:
- "Do this first."
- "Use this source, not that source."
- "Summarize before editing."
- "Ask before publishing."
- "Use this file path."

This creates the raw material for the skill.

### 3. Extract the stable workflow

After the manual run, write down:
- inputs the task needs every time
- fixed sequence of steps
- important decision points
- tool preferences
- stop conditions
- review gates
- common failure modes

If the workflow is not stable yet, do not build the skill. Run the task manually again later.

### 4. Define the skill contract

Before writing `SKILL.md`, answer these questions:
- What exact task does this skill own?
- When should it trigger?
- What should it explicitly not do?
- What files, scripts, or references does it need?
- Is it project-specific or reusable across projects?
- What counts as success?

Keep the scope narrow. One skill should do one job well.

### 5. Implement it in the OpenHands-compatible structure

Use the progressive-disclosure layout:

```text
.agents/
  skills/
    my-skill/
      SKILL.md
      scripts/
      references/
      assets/
```

OpenHands guidance:
- keep always-on repo rules in `AGENTS.md`
- keep optional skills in `.agents/skills/<skill-name>/SKILL.md`
- use one folder per skill
- add scripts and references beside the skill instead of bloating the prompt

For this repo, also keep Codex/Claude portability in mind.

### 6. Train the skill by answering its questions

The video's practical pattern is right:
- ask the agent to turn the validated workflow into a skill
- answer its clarifying questions
- constrain scope tightly
- review the resulting plan before accepting it

Typical questions to resolve:
- project-only or global?
- what inputs are required?
- what order is mandatory?
- what should happen automatically versus only after confirmation?
- where should outputs go?
- what sources are allowed?

This is where most skill quality is won or lost.

### 7. Test, iterate, then roll out

Run the new skill on a fresh example.

Look for:
- wrong execution order
- missing prerequisites
- vague instructions
- poor defaults
- edge cases
- failure to stop for review

Then update the skill. Treat it like training a new employee:
- first run proves the outline
- second run exposes edge cases
- third run should feel reliable

Only share it after that.

## Host Setup Requirements

From the cheat sheet, the highest-value setup for skill work is:
- terminal-first workflow configured properly
- `.claude/settings.json` or equivalent host settings for speed
- MCP servers for current docs, databases, or external systems
- hooks only when they improve reliability, not just because they are possible

Recommended supporting config areas:
- settings for model, status line, and auto-approval of safe reads
- MCP config for tool-backed tasks
- hooks for validation or notification after long runs

Do not put environment setup instructions inside every skill if they are really host-level concerns. Put those in repo docs or `AGENTS.md` and keep the skill focused on task execution.

## What Goes In `SKILL.md`

`SKILL.md` should contain:
- name
- short description
- optional triggers if keyword activation matters
- the exact workflow
- tool and source rules
- required review gates
- links to local scripts and references

Minimal starter example:

```md
---
name: my-skill
description: Use when the user needs X done for Y output.
triggers:
  - keyword-one
  - keyword-two
---

# My Skill

## Use when
- The user needs X
- The repo context is Y

## Do
1. Read the required local context first.
2. Gather the minimum external sources needed.
3. Run the supporting script if present.
4. Produce the output in the required format.
5. Verify the result before finishing.

## Do not
- Skip source verification.
- Invent missing inputs.
- Write deliverables outside the approved locations.

## Resources
- Script: `scripts/run_task.py`
- Reference: `references/domain-notes.md`
```

## What Goes In Scripts vs Prompt

Put logic in `scripts/` when:
- the step is deterministic
- it is verbose or repetitive
- it transforms data
- it validates output
- it talks to a tool or API in a fixed way

Keep it in prompt instructions when:
- it is judgment-heavy
- it depends on human taste
- it is a policy rule
- it is a review checklist

Rule of thumb: prose for judgment, scripts for mechanics.

## Trigger Design

Use triggers only when they are genuinely distinctive.

Good triggers:
- specific domain terms
- named workflows
- project-specific nouns

Bad triggers:
- broad words like `review`, `code`, or `help`

If the task should be invoked mainly by the agent or by explicit mention, keep the description clear and do not rely on weak trigger words.

## Review Checklist

Before calling a skill ready, verify:
- the scope is narrow and obvious
- the order of operations is explicit
- required inputs are named
- output paths are explicit
- external source rules are explicit
- review gates are explicit
- scripts and references exist
- the skill works on a fresh example
- at least one known edge case is handled

## Repo-Specific Guidance

For this repo:
- keep durable repo rules in `AGENTS.md` and `CLAUDE.md`
- use local files as the system of record for deliverables
- prefer official/current sources for implementation details
- use OpenHands docs and repo as source of truth when the skill touches agent behavior, microagents, or workflow orchestration

OpenHands references:
- `https://docs.openhands.dev/overview/skills`
- `https://docs.openhands.dev/overview/skills/keyword`
- `https://docs.openhands.dev/sdk/guides/skill`

## Copy-Paste Prompt To Build A New Skill

Use this after you have already completed one manual run:

```text
We just completed a manual run of this workflow. Turn it into a project-specific skill.

Goal:
- Automate: <task>
- Output: <deliverable>
- Scope: <project-only or reusable>

Requirements:
- Ask clarifying questions before writing the skill if anything is ambiguous.
- Keep the skill narrow.
- Use OpenHands-style structure with one folder per skill.
- Put deterministic logic in scripts, not in long prompt prose.
- Include explicit review gates, output paths, and failure conditions.
- Prefer local references and official sources.

Then propose:
1. skill name
2. trigger strategy
3. folder structure
4. `SKILL.md` outline
5. supporting scripts/references to add
6. test plan
```

## Short Version

The practical loop is:
1. Do the task manually with the agent.
2. Correct it until the workflow is good.
3. Distill the stable process.
4. Encode it as a narrow skill with scripts and references.
5. Test on a fresh case.
6. Update for edge cases.
7. Roll it out only after it behaves reliably.
