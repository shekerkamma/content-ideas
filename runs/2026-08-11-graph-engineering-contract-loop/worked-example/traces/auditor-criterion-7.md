# Auditor verdict — criterion 7

Run: 2026-08-11. Independent subagent. Given the contract and the outputs only;
not given the builder's reasoning, per the skill's critic-isolation rule.

VERDICT: fail
CRITERION 7: 0.0

## Findings (all verified against the repo, all upheld)

1. **The waiver reason is recorded for 1 of 14 skills.** The Grading clause says
   "per-skill". `claude-progress.txt` records one blanket entry reading
   "archive-is/pp-archive-is etc." — 13 of 14 have zero recorded reason.
   `feature_list.json` asserted "Reason recorded", true only for `archive-is`.

2. **The waiver's premise contradicts this repo's own standard.**
   `.claude/skills/skill-builder/SKILL.md:114` requires "`name` matches the
   directory name", and `.claude/skills/skill-builder/reference.md:32` documents
   `name` as optional, **defaulting to the directory name**. The waiver
   overrode a documented in-repo standard without citing or arguing against it.
   It also assumed one addressing surface where there are two: `name:` drives
   the `/slash-command`, while the Skill-tool roster addresses by directory.
   Each of the 14 is split across two names.

3. **"Shadows nothing" is false in the tree criterion 7 names.**
   `~/.claude/skills/hackernews/SKILL.md:2` and
   `~/.claude/skills/pp-hackernews/SKILL.md:2` both declare `pp-hackernews`.
   The builder fixed this in the repo only, and its own log deferred the host
   tree as "the next job".

4. **The waiver was applied non-uniformly to its own family.** The builder
   renamed `hackernews` — a 15th member of the same `pp-*` family — while
   waiving the other 14 on the grounds that renaming has "no functional gain".
   The result is two roster entries for the same tool with byte-identical
   `description:` lines.

## What the auditor verified as sound

- Uniqueness within `skills/`: 0 collisions across 315 skills.
- Uniqueness within `~/.claude/skills/` for the 14 waived names: clean.
- No router breakage: grepped every `.json`/`.md`/`.py`/`.sh`/`.toml` outside
  the skills' own directories. No manifest, command, or settings file
  references any of the 14.

## Out-of-scope observations

1. `feature_list.json` items 4 and 7 were stale against the amended contract.
2. `claude-progress.txt` narrated the reverted criterion-4 work as FIXED with
   no revert entry.
3. All 14 differ from their host installs beyond `name:` (nested
   `legacy-frontmatter:`); `~/.codex/skills/` holds both copies under identical
   declared names, so in Codex one silently wins. No criterion measures
   cross-tree drift — `--rule mirror` covers only the 6 in `MIRRORED`.
4. `skills/hackernews/SKILL.md` is an uncommitted working-tree edit, so
   criterion 2 passes only in the working directory — the same class of error
   the negotiation caught in criterion 6.
