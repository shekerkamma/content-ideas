---
name: cheat
description: |
  Maintain a project-scoped running cheat sheet that grows across sessions.
  Use when the user types /cheat (show), or /cheat <anything> (smart edit:
  append a note, start a new section, refactor, search, or freeform edit —
  Claude interprets intent from the args). The cheat sheet lives at
  ~/.claude/projects/<encoded-cwd>/CHEATSHEET.md and is project-scoped, so
  switching projects switches sheets automatically. Do NOT invoke when the
  user mentions "cheat sheet" in conversation without the literal /cheat prefix.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
---

# /cheat — Running cheat sheet for the current project

A growing, project-scoped knowledge file the user updates as they learn. Built for the kind of structured-learning workflow where each study session adds a few facts and the cheat sheet eventually replaces re-reading source files.

## File location (computed at runtime)

The cheat sheet lives at a path derived from the user's current working directory:

```bash
CHEAT_PATH="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')/CHEATSHEET.md"
```

Always resolve this path freshly for each invocation — never hardcode. This makes the skill auto-adapt when the user `cd`s to a different project.

If the parent directory does not exist, create it: `mkdir -p "$(dirname "$CHEAT_PATH")"`.

If the file does not exist, create it with this seed content:

```markdown
# Cheat Sheet — <project name from basename of pwd>

> Append-only knowledge file. Maintained by the `/cheat` skill.

## Active section
```

## Argument modes

The user's message after `/cheat` is the args string. Decide what to do based on its content:

### No args (`/cheat`)
Read the file and display it as-is. If the file is empty or only has the seed template, say so and suggest the user add their first entry with `/cheat add <something>`.

### Args present (`/cheat <anything>`)
Interpret the args as a smart edit instruction. The user is **not** speaking a strict command vocabulary — they are stating intent in plain language. Map their intent to one of these operations:

| Intent signal in args | Operation |
|---|---|
| Starts with `add `, `note `, `+`, or just a fact | **Append** as a bullet under the most recent `##` section |
| Starts with `new `, `section `, `## `, or names a new topic | **New section**: add `## <title>` and continue appending under it |
| Starts with `session `, `Session ` followed by a number | **New section** titled `## Session <N> — <inferred or asked title>` |
| Starts with `refactor`, `reorganize`, `dedupe`, `clean up` | **Refactor**: read the whole file, group related bullets, dedupe, tighten language. Preserve every distinct fact. |
| Starts with `search `, `find `, `what do I know about ` | **Search**: grep the file for the topic; report matches with section context. Do not edit. |
| Starts with `remove `, `delete `, `clear ` | **Remove**: identify the matching content, confirm with the user before deleting if ambiguous, then edit out. |
| Anything else | **Freeform edit**: read the file, interpret the user's instruction as best you can, make the edit, and show what changed. |

## Operation rules

1. **Read before write.** Always Read the current cheat sheet before editing. Edit, do not Write-overwrite, unless refactoring the whole file.
2. **Append to the most recent section by default.** Sections accumulate from top (oldest) to bottom (newest). New bullets join the bottom-most `##` section.
3. **One bullet per fact.** Don't pack multiple facts into one bullet. If the user gives a multi-fact note, split it.
4. **Keep bullets terse.** Cheat sheets exist for fast scanning. If a bullet is more than ~25 words, suggest splitting it.
5. **Preserve facts on refactor.** Refactoring may regroup, rename sections, dedupe duplicates, and tighten language — but it must not silently lose any distinct fact. If two bullets are similar but distinguishable, keep both. If truly duplicate, keep one.
6. **Show what changed.** After every edit (not on show or search), end with a short summary: which section was touched, what was added/changed, and the new bullet count.

## Output style

- For show: print the file content. No preamble.
- For edits: one short confirmation sentence + a snippet of the changed lines.
- For search: matches grouped by section, no editorializing.
- Never re-explain the cheat sheet's purpose to the user — they know.

## When NOT to invoke this skill

- The user says "cheat sheet" or "cheat" in normal conversation without the literal `/cheat` prefix.
- The user wants to edit a different file (a real project doc, a README, etc.) — even if they call it a "cheat sheet". This skill manages exactly one file per project.

## Examples

| Input | Behavior |
|---|---|
| `/cheat` | Show file |
| `/cheat add daemon writes SQLite to .od/app.sqlite` | Append bullet to current section |
| `/cheat session 2 — Tourist` | Start `## Session 2 — Tourist` section |
| `/cheat refactor` | Reorganize, dedupe, tighten |
| `/cheat what do I know about contracts` | Search and report |
| `/cheat remove the bullet about NEXT_PORT` | Find and delete that bullet |
| `/cheat the daemon detects agents by scanning PATH` | Freeform → append as fact |
