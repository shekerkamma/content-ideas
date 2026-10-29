---
name: ss
description: 'Grab the most recent N screenshots from the user''s screenshot folder and act on them. Use when the user types /ss, /ss [N], or /ss [N] [action]. Actions: explain, fix, remix, compare, transcribe, infographic, diff, or freeform intent. Default N is 1, default action is explain. This is how the user "speaks visually" to Claude Code. Do NOT invoke when the user mentions "screenshot" or "ss" in conversation without the literal /ss prefix.'
allowed-tools:
- Bash
- Read
- Edit
- Write
- Grep
- Glob
---

# /ss — Visual input shortcut

The user takes a screenshot, types `/ss [N] [action]`, and you load the most recent N screenshots from their screenshot folder and act on them. This is the user's primary way of giving Claude visual context.

## Configuration (edit if path changes)

- **Screenshot folder:** `/mnt/c/Users/sheke/OneDrive/Pictures/Screenshots`
- **Filename pattern:** `Screenshot YYYY-MM-DD HHMMSS.png` (contains spaces)
- **Default count:** 1
- **Default action:** `explain`

## Argument parsing

The user's message after `/ss` is the args string. Parse as follows:

1. If the first whitespace-delimited token is a positive integer → that is **N**. The remaining tokens are the **action**.
2. If the first token is the literal word `diff` → set N=2, action=`compare`.
3. Otherwise → N=1, action is the entire args string.
4. If args is empty → N=1, action=`explain`.

Examples of parsing:

| Input | N | Action |
|---|---|---|
| `/ss` | 1 | `explain` |
| `/ss 3` | 3 | `explain` |
| `/ss fix` | 1 | `fix` |
| `/ss 3 infographic` | 3 | `infographic` |
| `/ss diff` | 2 | `compare` |
| `/ss 2 do this for our hero section` | 2 | `do this for our hero section` |

## Loading screenshots

After parsing N, run this Bash command to list the N most recent PNGs, newest first:

```bash
ls -t "/mnt/c/Users/sheke/OneDrive/Pictures/Screenshots"/*.png 2>/dev/null | head -N
```

Substitute the actual N value. Then use the **Read** tool on each path returned (Read handles PNGs as images for vision input).

If the listing is empty, tell the user the screenshot folder appears empty and ask them to take a screenshot first. Do not silently proceed.

## Action vocabulary

These verbs get specific handling. Anything not matched is treated as freeform intent with the screenshots as context.

### `explain`
Describe what's in the screenshot(s) concretely. Transcribe key text. Name UI elements. No flowery language. If multiple screenshots, summarize each in turn, then synthesize.

### `fix`
Treat the screenshot as a bug report.
- If the image shows an error message or stack trace → identify the error, locate the relevant file in the current project, propose and apply the fix.
- If the image shows a UI defect (overlapping text, broken layout, misaligned elements) → find the component in the current project, fix it, and explain what changed.
- If we are not in a code project (no git repo, no recognizable source tree) → explain the bug and suggest a fix; do not invent a project context.

When CWD is a git repo, run `git status` and skim the recent diff *before* searching the codebase — the bug is usually in code the user just touched.

### `remix` or `do this`
The user saw something they liked online or elsewhere and wants to recreate or adapt it for their own context. Extract the essential pattern (visual, structural, or rhetorical), then adapt it to fit what you know about the user's current goals or project. Produce concrete output (code, copy, plan) rather than abstract advice.

### `compare`
Requires N >= 2. Diff the screenshots: what changed, what stayed the same, what's better/worse. Most useful for before/after UI iteration. If N == 1, ask the user what they want to compare against.

### `transcribe`
Faithfully extract all visible text. No interpretation, no rewriting. Preserve structure (lists stay lists, tables stay tables) using markdown.

### `infographic`
Requires N >= 2 ideally. Synthesize the content of the screenshots into a single unified visual artifact. Output an HTML file (single file, inline CSS, no external assets) that the user can open in a browser. Save it to the current working directory as `infographic-<timestamp>.html` and tell the user the path.

### Freeform (default fallback)
Treat the action text as a literal instruction from the user. Use the screenshots as visual context for that instruction. Do not over-interpret — if they say "make this blue", they mean make the thing in the screenshot blue, not "discover what 'blue' might metaphorically mean".

## When NOT to invoke this skill

- The user mentions "screenshot" or "ss" in regular conversation without typing the literal `/ss` prefix.
- The user asks Claude to take a screenshot of something (this skill *reads* screenshots, it does not capture them).
- The user wants to work with images that are not in the configured screenshot folder — in that case, ask them to drag the file into the chat or give an explicit path.

## Output style

- After loading the screenshot(s), open with one short sentence naming what you see ("Loaded 3 screenshots showing a Stripe pricing page, a Linear dashboard, and a Notion workspace") so the user knows the right files were picked up.
- Then execute the action.
- Keep responses tight. The user is using `/ss` for speed; long preambles defeat the point.
