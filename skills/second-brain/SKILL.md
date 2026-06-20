---
name: second-brain
description: >
  Use when someone says "build my second brain", "set up a knowledge base", "add to my wiki",
  "compile my notes", or wants to bootstrap and maintain a markdown-first repo following the
  raw/ → wiki/ → archive/ OpenKB-style pattern. Orchestrates content-research note intake,
  wiki compilation, and optional graphify export.
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

---

## Skill Relationships

### Category
Business Automation

### Dependencies
- `bootstrap_second_brain.sh` script at `<skill-dir>/scripts/` — required for first-time repo setup
- `references/simplebrain-pattern.md` — read before making structural changes (checked into the skill dir)

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `content-research` | Sequential upstream | always — content-research produces raw notes that second-brain ingests into raw/ | `raw/<topic>.md` or Obsidian vault notes |
| `graphify` | Sequential downstream | optional — after wiki compilation, graphify turns the wiki into a knowledge graph | `wiki/*.md` |
| `openkb` | Alternative / Peer | openkb uses compiled KB + vector search; second-brain is the raw → wiki maintenance layer that feeds it | `wiki/` tree |

### Runtime Preamble

At invocation, say:
- "Running /second-brain — markdown knowledge base. Structure: raw/ → wiki/ → archive/."
- If a named repo is specified (e.g., `hyundai-ai-vault`): "Using that path as the target."
- If no path given: "Defaulting to `second-brain/` in the current directory."
- After compilation: "Want me to export the wiki to a knowledge graph with /graphify?"

---

## Gotchas

- **Never delete from `raw/` or `archive/`.** Move only. These directories are the audit trail.
- **Read the existing wiki entry before writing.** Merge, do not overwrite. Blind overwrites lose prior context.
- **Do not make Obsidian a dependency.** The folder must work as plain markdown — no vault-only features.
- **Archived files are immutable.** Once a raw file lands in `archive/`, do not edit it — create a new wiki entry instead.
- **One topic per wiki file.** Combining topics makes semantic retrieval worse. Split early, not later.
