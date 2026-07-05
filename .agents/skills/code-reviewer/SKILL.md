---
name: code-reviewer
description: >
  Review code changes for bugs, regressions, security issues, performance
  problems, and missing tests. Use when the user asks for a review, PR review,
  diff review, security audit, or wants to know what is risky in a change.
triggers:
  - code review
  - review this
  - review this diff
  - review this pr
  - pr review
  - security audit
  - audit this change
---

# code-reviewer

Review code changes as a reviewer, not as an implementer.

The goal is to identify issues that materially affect correctness, safety,
reliability, or maintainability. Do not default to style nits or speculative
refactors.

## When To Use

Use this skill when:
- the user asks for a review
- the user asks for PR feedback
- the user wants risk analysis on a code change
- the user wants a security or regression audit

Do not use this skill when:
- the user is asking you to implement a change directly
- the task is exploratory design without concrete code
- the user wants a rewrite rather than a review

## Review Standard

Prioritize:
1. correctness bugs
2. behavioral regressions
3. security issues
4. data loss or integrity risks
5. performance problems with real impact
6. missing or insufficient test coverage
7. maintainability issues only when they create real delivery risk

Deprioritize:
- formatting
- naming nits without impact
- subjective style opinions
- architecture rewrites not required by the change

## Required Workflow

### 1. Scope the review surface

Determine what is being reviewed:
- a PR
- a commit range
- a patch
- one or more local files

If a diff exists, review the diff first. Expand to surrounding files only when
needed to understand behavior.

### 2. Load local instructions

Read repo-specific guidance before judging the change:
- `AGENTS.md`
- `CLAUDE.md`
- any nearby instructions relevant to the changed area

Apply repository rules, but do not confuse repo conventions with defect
severity.

### 3. Understand intent before criticism

Infer:
- what the change is trying to do
- what user-visible behavior changed
- what assumptions the change makes
- what could break if those assumptions are wrong

Do not report an issue until you can explain the failure mode concretely.

### 4. Inspect by risk category

Review in this order:

#### Correctness

Look for:
- wrong conditionals
- bad state transitions
- broken edge-case handling
- ordering bugs
- stale references
- incorrect return values
- API contract mismatches

#### Regression Risk

Look for:
- behavior changes not covered by tests
- changed defaults
- removed validation
- partial migrations
- backwards-compatibility breaks

#### Security

Look for:
- injection risks
- auth or permission bypasses
- secret exposure
- unsafe deserialization
- path traversal
- missing input validation at trust boundaries

#### Performance

Look for:
- accidental N+1 work
- repeated expensive calls
- unnecessary allocations
- unbounded loops or scans
- excessive network or disk churn

Only raise these when the impact is credible, not hypothetical.

#### Testing

Look for:
- no test for new behavior
- no regression test for a bug fix
- no edge-case coverage
- tests that assert implementation details but miss behavior

### 5. Validate evidence

Every finding must have:
- a concrete problem
- why it matters
- where it occurs
- the likely consequence

If you cannot explain the consequence, do not present it as a finding.

### 6. Keep findings scoped

A finding should describe one issue, not a blended paragraph of several ideas.

If multiple files contribute to the same bug, explain the shared failure mode
once and cite the most relevant locations.

## Output Format

Present findings first.

Order them by severity:
- critical
- high
- medium

For each finding include:
- short title
- file reference
- why it is a problem
- likely impact

After findings, include:
- open questions or assumptions
- brief change summary only if useful

If there are no findings, say so explicitly and mention any residual risks or
testing gaps.

## File References

When possible, cite local file paths with line references.

Examples:
- [app.py](/abs/path/app.py:42)
- [src/reviewer.ts](/abs/path/src/reviewer.ts:118)

Prefer precise references over vague file mentions.

## Review Guardrails

Do not:
- propose fixes unless they help clarify the bug
- bury the real issue under long prose
- pad the review with generic praise
- invent line numbers
- treat missing context as proof of a defect

Do:
- stay concrete
- state assumptions when needed
- call out missing tests when they materially matter
- say "no findings" when that is the honest result

## Quick Checklist

Before finalizing the review, confirm:
- findings come before summary
- findings are severity-ordered
- each finding includes a concrete impact
- file references are present where possible
- style-only comments did not crowd out real risks
- missing tests were noted when relevant

## Reference

Detailed review checklist: [references/review-checklist.md](./references/review-checklist.md)
