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

Two checks. Paths are relative to `~`, not to the repo — resolving them from the
wrong root produces false positives, which is how the first pass mis-reported
four working skills as broken.

```bash
# every declared SKILL.md path resolves
for p in $(grep -oE '`~?/?[A-Za-z0-9._/-]*SKILL\.md`' ~/.claude/CLAUDE.md | tr -d '`' | sort -u); do
  f="${p/#\~/$HOME}"; case "$f" in /*) ;; *) f="$HOME/$f";; esac
  [ -e "$f" ] || echo "MISSING: $p"
done

# every /trigger resolves to a skill somewhere
for t in $(grep -oE 'When the user types `/[a-z0-9-]+`' ~/.claude/CLAUDE.md \
           | grep -oE '/[a-z0-9-]+' | tr -d '/' | sort -u); do
  find -L ~/.claude/skills/$t ~/content-ideas/skills/$t \
       ~/content-ideas/.claude/skills/$t \
       ~/content-ideas.local/skill-framework/.agents/skills/$t ~/.claude/commands \
       -maxdepth 2 \( -name SKILL.md -o -name "$t.md" \) 2>/dev/null | head -1 \
    | grep -q . || echo "DEAD TRIGGER: /$t"
done
```

**A directory is not a skill.** `find -type f` does not follow symlinks, so a
working symlinked skill counts as zero files. That mistake produced a "61 empty
directories" finding that was entirely an artifact; 325 of those resolved fine.
Test with `-e` or `find -L`.
