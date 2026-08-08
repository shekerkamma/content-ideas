---
name: skill-hygiene
description: Sweep the whole skill library through three gates — intact, earned, lean — and rewrite what fails.
disable-model-invocation: true
---

# Skill Hygiene

A **sweep** across every skill on the machine. Each skill passes three **gates**, in
order, and exits the sweep in exactly one state. The gates are existing skills; this
document owns only their order, their handoffs, and the bar for done.

| Gate | Asks | Run |
|---|---|---|
| **intact** | Are the bytes still there? | `skill-doctor` |
| **earned** | Is it used, single-copy, and distinct? | `skills-analyst` |
| **lean** | Does it repay its context load? | `writing-for-agents` |

Failures at **earned** or **lean** go to `skill-builder` for the rewrite.

## The order is load-bearing

Run **intact** first. `skills-analyst` classifies a skill with no usage signal and no
clear trigger as DELETE/ARCHIVE — which is exactly how a zero-filled `SKILL.md` reads.
Judged before repair, recoverable skills get archived as dead. On 2026-08-08 that
distinction was worth 14 files, nine of them recoverable from git history alone.

Run **lean** last. Pruning prose inside a skill that gate two is about to merge or
archive is work thrown away.

## Sweep

### 1. Intact

Invoke `skill-doctor`. Restore every live file that has a donor; name every one that
does not, with the reason.

Done when a re-scan reports zero fixable live files.

### 2. Earned

Invoke `skills-analyst`. It classifies each skill KEEP / FIX / MERGE / DELETE and
carries its own evidence and confirmation rules — including that deletions are always
confirmed by the human first.

Feed it the gate-one result: a skill repaired this run is newly readable, so classify it
on its restored content, not on the emptiness that preceded it.

Done when every skill in the library carries a verdict.

### 3. Lean

For each KEEP and FIX survivor, read `writing-for-agents` and apply it: context-pointer
wording, the two loads, the information hierarchy, leading words, and the pruning tests
(single source of truth, relevance, no-ops).

Judge the **description** hardest — it is always-loaded on every turn, whether or not
the skill fires. A skill that only ever fires by hand costs nothing as a user-invoked
skill; see `SKILL-MECHANICS.md` for that trade.

Done when every survivor has been read against those tests and either passes or carries
a named defect.

### 4. Rewrite

Invoke `skill-builder` on each skill carrying a defect from gate two or three. Preserve
each skill's canonical location and its host copies; this repo keeps `skills/` canonical
and mirrors byte-identical wrappers into `.claude/skills/` and `.agents/skills/`.

Done when every defect is closed or explicitly deferred with a reason.

## Report

Every skill in the library ends in one state:

- **kept** — passed all three gates
- **rewritten** — failed a gate, fixed this run
- **recovered** — restored at gate one
- **archived** — human confirmed removal
- **deferred** — defect named, fix postponed, reason recorded

State the count per bucket. A skill missing from all five means the sweep is incomplete.
