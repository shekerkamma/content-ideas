---
name: karpathy-guidelines
description: Use when writing, reviewing, or refactoring any code to enforce: surface assumptions before coding, minimum code that solves the problem, surgical edits that touch only what's required, and verifiable success criteria. Always-on behavioral overlay during implementation work. Triggers on "karpathy", "apply karpathy", "coding guardrails", or any coding task in projects where this skill is loaded.
category: Code Quality & Review
license: MIT
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

## Skill Relationships

### Category
Code Quality & Review

### Dependencies
None — standalone behavioral overlay. No file inputs or outputs.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `claude-code-director` | Behavioral overlay | always-on during any implementation phase | — (modifies HOW coding runs, not what is produced) |
| `plaid` (Build phase) | Behavioral overlay | always-on when executing `docs/product-roadmap.md` tasks | — |
| `code-review` / `ce-code-review` | Domain cluster | sibling in the code quality domain; code-review assesses output, karpathy-guidelines governs process | — |
| `simplify` | Domain cluster | sibling; simplify cleans up after implementation, karpathy-guidelines prevents overcomplication during it | — |

### Runtime Preamble
This skill has no interactive invocation. It is an always-on overlay: whenever any implementation work runs in a project that has loaded karpathy-guidelines, these four rules govern how Claude codes — not as a checklist to recite, but as internalized behavior.

---

## Gotchas

- **This is a behavioral overlay, not a checklist:** Do not recite these rules to the user before every edit. Internalize them and code accordingly. If a rule is being violated in the current task, name the violation once and correct course.
- **"Simplicity first" does not mean "no error handling":** It means no error handling for impossible scenarios. Errors that can realistically occur must still be handled.
- **Surgical changes applies to edits, not new files:** When writing a new file from scratch, write it cleanly. The surgical rule governs changes to existing code — don't touch what you weren't asked to touch.
- **Goal-driven execution requires a stated plan for multi-step tasks:** For single-line fixes, stating a plan is overkill. Apply judgment — require explicit verification steps only when multiple things could go wrong independently.
- **Don't use this skill as a reason to slow down trivial tasks:** The guidelines say "for trivial tasks, use judgment." Asking for clarification on a one-liner typo fix is overhead, not caution.
