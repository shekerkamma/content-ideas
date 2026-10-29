# Host config snapshots

`~/.claude/CLAUDE.md` is the global instruction file every Claude Code session on
this machine loads. It is **not** tracked by any repo, so a machine rebuild loses
it along with every routing decision recorded in it.

`global-CLAUDE.md` here is a snapshot, not a live copy. Nothing reads it. Refresh
it after editing the real file:

```bash
cp ~/.claude/CLAUDE.md docs/host-config/global-CLAUDE.md
```

## Why the snapshot exists

On 2026-09-09 an audit of every path and trigger declared in that file found
routes pointing at skills that did not exist:

| Route | Was | Now |
|---|---|---|
| `/claude-md-auditor` | existed nowhere | `/rule-rewriter` |
| `/skill-distiller` | existed nowhere | `/skills-analyst` then `/skill-builder` |
| `/landing-page-gen` | existed nowhere | removed |
| `/vertical-scorer` | existed nowhere | removed |
| `/openkb-deck-editorial` | existed nowhere | removed |
| `/code-reviewer` | directory with references but no SKILL.md | removed |
| `deep-research`, `technical-writer` | wrong root | `~/content-ideas.local/skill-framework/.agents/skills/` |
| `openkb`, `openkb-deck-neon`, `openkb-html-critic` | `OpenKB/skills/` (empty dir) | `~/content-ideas/skills/` |
| `second-brain`, `ai-strategy-brief`, `ai-strategy-researcher` | wrong path | corrected |

After the pass: **46 declared paths, 0 missing, 0 dead triggers.**

## How to re-run that audit

```bash
python3 scripts/check_routes.py ~/.claude/CLAUDE.md    # 0 clean, 1 blocked, 2 findings
python3 scripts/check_routes.py CLAUDE.md AGENTS.md ~/.claude/CLAUDE.md
```

`scripts/check_routes.py` replaces the shell one-liners this file used to carry.
It checks two things per instruction file: that every `` `path/SKILL.md` ``
backtick-quoted path resolves, and that every ``When the user types `/x` ``
trigger reaches a skill in one of the known roots. `tests/test_route_integrity.py`
holds it honest against `tests/fixtures/routes/broken-CLAUDE.md`, a fixture with
four deliberate defects and one working route.

Where `check_skills.py` validates the skills themselves, this validates the
instructions that point at them — the failure mode nothing else catches.

## Two traps the script encodes

Both produced wrong answers on the first manual pass:

- **Declared paths resolve from `~`, not from the repo root.** Resolving them
  from the repo reported four working skills as broken.
- **`find -type f` does not follow symlinks**, so a symlinked skill counts as
  zero files. That produced a "61 empty directories" finding that was entirely
  an artifact: 325 of them resolved fine. The script uses `Path.exists()`, which
  follows, and a test asserts it never shells out to `find`.
