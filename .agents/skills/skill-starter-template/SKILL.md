---
name: skill-starter-template
description: >
  Reusable starter template for building a new project-specific skill after
  the workflow has already been validated manually. Use this when you want to
  scaffold a narrow, testable OpenHands-style skill with explicit steps,
  review gates, scripts, and references.
triggers:
  - new skill
  - build skill
  - skill template
  - scaffold skill
---

# skill-starter-template

Use this as the base structure for any new skill in this repo.

Do not keep this skill as the final implementation. Copy this folder, rename it
to the real skill name, then replace the placeholders with the actual workflow.

## When To Use

Use this template when:
- the workflow has already been run manually at least once
- the task is repeated and multi-step
- the output format is stable enough to encode
- you know what should be automated versus reviewed manually

Do not use this template when:
- the process is still exploratory
- the scope is too broad
- the workflow has not been validated manually yet

## Required Inputs

Before turning this into a real skill, define:
- the exact job the skill owns
- the inputs it needs every run
- the output path or artifact it must produce
- the source rules it must follow
- the review gates it must stop at
- whether it is project-only or reusable across repos

## Build Workflow

### 1. Rename the skill

Rename this folder from `skill-starter-template` to the real skill name.

Update frontmatter:
- `name`
- `description`
- `triggers`

Make the description specific enough that the agent can tell when to load it.

### 2. Replace the placeholders

Replace every bracketed placeholder in this file:
- `<task>`
- `<inputs>`
- `<sources>`
- `<output>`
- `<review gate>`
- `<failure mode>`

If a placeholder survives, the skill is not ready.

### 3. Move mechanics into scripts

If part of the workflow is deterministic, put it in `scripts/`.

Examples:
- parsing files
- transforming data
- validating output
- running repeatable commands
- packaging artifacts

Keep judgment-heavy rules in this file.

### 4. Add local references

Put stable supporting context in `references/`.

Examples:
- output schema
- domain notes
- style guide
- QA checklist
- source shortlist

The skill should point to those files explicitly instead of pasting everything
inline.

### 5. Define the execution path

Every real skill should eventually specify a concrete sequence like this:

1. Read the required local context.
2. Validate that required inputs exist.
3. Gather the minimum approved external sources.
4. Run local scripts if needed.
5. Produce the output artifact.
6. Stop at the review gate.
7. Finalize only after verification.

Replace that generic sequence with the actual workflow for `<task>`.

## Real Skill Skeleton

Copy and edit this section for the real skill:

### Goal

Automate `<task>` so the user gets `<output>`.

### Inputs

- `<input 1>`
- `<input 2>`
- `<input 3>`

### Do

1. Read `<local file or context>`.
2. Confirm `<precondition>`.
3. Use only `<approved sources or tools>`.
4. Run `scripts/<script-name>` if `<condition>`.
5. Produce `<artifact>` at `<path>`.
6. Present `<review gate>` before any irreversible action.

### Do Not

- invent missing inputs
- skip source verification
- write outputs outside the approved location
- bypass the review gate
- continue silently after `<failure mode>`

### Success Criteria

The skill is successful when:
- `<artifact>` exists
- `<quality bar>` is met
- `<review step>` is completed

### Failure Handling

If `<blocking condition>` happens:
- stop
- explain what is missing
- say exactly what input or state is needed next

## Testing Checklist

Before treating the real skill as usable:
- run it on a fresh example
- confirm the order of operations is correct
- confirm output location is correct
- confirm the review gate triggers at the right point
- confirm at least one edge case is handled
- confirm the description and triggers are not too broad

## Resources

- Script placeholder: [scripts/README.md](./scripts/README.md)
- Reference placeholder: [references/README.md](./references/README.md)
- Playbook: [docs/skill-building-playbook.md](/home/shekerk/content-ideas/docs/skill-building-playbook.md)
