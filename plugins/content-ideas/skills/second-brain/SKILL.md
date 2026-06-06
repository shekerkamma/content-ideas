---
name: second-brain
description: Bootstrap and maintain a SimpleBrain-style personal wiki repo for Codex and Claude. Use when the user wants a second brain, wiki repo, raw-to-wiki workflow, or a Codex-compatible alternative to an Obsidian-only setup.
---

# Second Brain

Build or normalize a markdown-first second-brain repo modeled on the
`BuildGreatProducts/SimpleBrain` pattern:

- `raw/` for captured inputs
- `wiki/` for clean AI-written notes
- `projects/` for active work
- `archive/` for processed raw inputs

This skill is for a knowledge repo, not a software project.

Read `references/simplebrain-pattern.md` before making structural changes.

## Workflow

1. Detect the target second-brain path.
   - Prefer an explicit path from the user.
   - If the user names a repo such as `hyundai-ai-vault`, use that path.
   - Otherwise choose a repo-local folder such as `second-brain/`.
2. If the repo does not exist, bootstrap it with:

```bash
bash "<skill-dir>/scripts/bootstrap_second_brain.sh" "<target-path>"
```

3. Ensure the core layout exists:
   - `raw/`
   - `wiki/`
   - `projects/`
   - `archive/`
4. Ensure the core control files exist:
   - `README.md`
   - `AGENTS.md`
   - `CLAUDE.md`
   - `translate.md`
   - `.gitignore`
5. Keep the repo markdown-first and git-friendly.
6. When translating raw notes:
   - read the existing wiki entry first if one exists
   - merge instead of overwriting blindly
   - move processed raw files into `archive/`
   - never edit archived files after they land there

## Rules

- Treat the second brain as the system of record for durable knowledge notes.
- Do not make Obsidian a requirement. The folder should work as plain markdown.
- `AGENTS.md` is the Codex entrypoint. `CLAUDE.md` is kept in sync for Claude.
- Never delete from `raw/` or `archive/`; move only.
- Prefer one topic per wiki file with kebab-case filenames.
- Preserve user phrasing when it carries signal; do not flatten everything into generic prose.
