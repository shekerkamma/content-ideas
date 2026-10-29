# 01 — Install the converter in two minutes

## What the converter does
Point it at a PDF; it reads the book chapter by chapter, pulls out the
frameworks, the decision rules and the mistakes the author says not to make,
and writes all of that into a skill Claude pulls off the shelf when the job
calls for it.

## Two installs, same result
Ask Claude Code directly:
> Install the book-to-skill skill from https://github.com/virgiliojr94/book-to-skill
> into my personal skills folder at ~/.claude/skills/ so it works in every project.

Or run it yourself:
```bash
npx skills add virgiliojr94/book-to-skill
```

## Decision rule — which skills folder
| Folder | What it means |
|---|---|
| `~/.claude/skills/` | Personal. Works in every project on the machine. |
| `.claude/skills/` in a project | Project only. Right when the book skills belong to that business. |

Default to personal unless the books are business-specific.

## Verification
Open a fresh Claude Code session and type `/book`. If `book-to-skill` appears in
autocomplete, it is installed. That is the whole setup.
