# Skills Audit — 2026-07-12

Analyst: Fable (skills-analyst role). Re-run anytime with:
`python3 ~/.claude/skills/skills-analyst/scripts/audit.py --out /tmp/skills-audit.md`

## Scope & evidence base

- **8 skill roots** scanned: `~/.claude/skills` (master), `~/.codex/skills`,
  `~/.agents/skills`, `~/.gemini/skills`, repo `skills/`, repo `.claude/skills`,
  repo `.agents/skills`, plugin `plugins/content-ideas/skills`.
- **243 distinct skill names**; 104 present in more than one root; **27 diverged**
  duplicates at audit start (25 after fixes below).
- **Usage mined** from 56 Claude Code transcripts (2026-06-10 → 2026-07-12) and
  680 Codex history entries. Only **~41 skills have any recorded usage**.
- Caveat: transcript retention is limited, and inline-read frameworks
  (strategy-consulting's 21, solution-delivery's 13, etc.) never appear as
  Skill-tool calls. Zero-usage is a signal, not proof.

## How you actually use Claude (repeated work)

| Rank | Workflow | Evidence |
|---|---|---|
| 1 | **Video / URL ingestion → analysis** | `watch` 18×, `content-research`, most session openers are pasted links |
| 2 | **Session continuity** | `session-handoff` 14× — your single most-typed slash command |
| 3 | **Branded deck production** | `branded-pptx-deck` 12×, `marp` 7×, genspark, openkb-deck, `video-to-deck` |
| 4 | **Research → strategy → deal prep** | `strategy-consulting` 4×, `ai-strategy-brief`, `research-to-deck` 3×, pipeline-runner |
| 5 | **Cross-host skill porting/sync** | ≥4 sessions ("install in Antigravity", "port genspark skills to Claude Desktop", …) — had **no skill** until now |
| 6 | **Learning / brainstorming** | `grill-me` 4×, `learn-anything` 3× |

## Verdicts

### KEEP (used, healthy)

`watch`, `session-handoff`, `branded-pptx-deck`, `marp`, `grill-me`,
`strategy-consulting` (+ its 51 inline consulting frameworks — wired via
CLAUDE.md, invisible to usage mining by design), `firecrawl`,
`ai-use-cases-consultant`, `skill-builder`, `drawio`, `research-to-deck`,
`learn-anything`, `content-research`, `content-ideas`, `pipeline-runner`,
`graphify`, `ai-strategy-brief`, `video-to-deck`, `genspark-slides`,
`genspark-branded-deck`, `refero-design`, `exa-api`, `printing-press`,
`ikigai` / `ikigai-gamma-slidedeck`, and the full BuilderOS chain
(`idea-generator` → `idea-validator` → `product-planner` → `design-system` →
`build-mvp` / `spar-prd-goal` → `build-loop-*` → `launch-checklist`).

### FIX

**Done in this audit:**
- `branded-pptx-deck` (your #1 skill) — `~/.claude/skills` copy was a stale
  Jul-3 version missing the OfficeCLI QA gate; synced from repo (Jul-9).
- `video-to-deck` — same stale-copy problem; synced from repo.
- `~/.claude/scripts/officecli_qa.py` installed so the QA-gate reference
  resolves outside the repo.

**Also done in this audit (approved 2026-07-12):**
- `pipeline-runner` + `second-brain`: plugin copies were a version behind
  (v1.1.0 vs v1.2.0 with the last30days Stage 0.5) → resynced from repo;
  `python3 -m pytest -q` passes (73 tests).
- `docx` / `pdf` / `xlsx` / `excalidraw` / `genspark-branded-deck` / `plaid`:
  repo copies (Jul 2–9, newer) synced over stale globals.
- `ikigai` / `ikigai-gamma-slidedeck` / `openhands-niche-agency`: refactored
  global copies (template extracted to `templates/agents-md-template.md`)
  synced down to repo `.agents`, template dir included.
- `ai-head-of-engineering` family (×10): newer quoted-YAML frontmatter from
  repo `.agents` synced to repo + global.
- Every replaced file backed up to `~/.claude/skills-archive/2026-07-12/_replaced/`.
- **Not drift:** `skill-builder`, `storm-research`, `agentic-blueprint-pipeline`,
  `disruptive-teardown-pipeline` short copies are intentional Codex/OpenHands
  *discovery wrappers* pointing at a canonical copy — left as designed.
- Diverged duplicates after fixes: **27 → 4** (all four are the intentional wrappers).

**Backlog executed (second pass, approved 2026-07-12):**
- `goal-loop-orchestrator` 702→229L: strategy research policy, chaining-QA gate,
  and recipes/relationships/gotchas extracted to `references/` (repo + global).
- `office-hours`: top-level copy was a broken Antigravity port (Windows
  `%USERPROFILE%` paths, missing reference files). Replaced with a symlink to
  the canonical `gstack/office-hours`, reversed the Antigravity path rewrites
  there and in `gstack/plan-ceo-review`, extracted visual-exploration section
  (665→509L). Same symlink fix for top-level `plan-ceo-review`.
- `learn-anything` 554→481L: Step 5 sandbox mechanics → `reference/step5-sandbox.md`.
- `drawio` 526→352L: XML structure → `references/xml-structure.md` (Windows-side master).
- `content-ideas` 629→549L: research/memory policy + use-case realization
  structure → `references/`; contract-asserted phrases preserved in the pointer
  paragraphs; version stays 2.2.0; all three copies mirrored; pytest green.
- `graphify`, `refero-design`: left as-is (already progressive-disclosed /
  vendored upstream — slimming would cause upstream drift).
- **Merge executed:** `ai-head-of-engineering` 10 skills × 3 roots → 1
  orchestrator per root; the 9 roles now live in `references/roles/01–09-*.md`,
  run inline; single-role triggers folded into the orchestrator description;
  old dirs archived under `merged-ai-hoe/` in the archive.
- **Merges declined with cause:** `aeo-*` stage skills carry scripts invoked by
  path from `run_pipeline.py`, `goal-loop-orchestrator`, and `content-ideas` —
  consolidation would break script-path contracts. `openkb-deck-neon`/
  `-editorial` are vendored external OpenKB skills with distinct design-system
  content — merging creates upstream drift.
- **Hygiene:** 23 pre-existing dead symlinks removed from `~/.claude/skills`
  (targets in deleted `~/markdown-viewer-skills-audit/`); dangling
  `content-ideas-okf` entry removed from `.claude/settings.json`.
- Final numbers: **157 distinct skills** (from 243), diverged duplicates
  **4** (all intentional discovery wrappers), tests green.

**Remaining fix backlog:**
- **Bloat** (>500-line SKILL.md on *used* skills — extract `references/`):
  `goal-loop-orchestrator` (702L), `office-hours` (669L), `content-ideas` (629L),
  `learn-anything` (554L), `graphify` (541L), `refero-design` (538L),
  `drawio` (526L). Matches the existing skill-audit-backlog memory.

### MERGE

- `watch` + `watch-video` (+ `watch:watch` plugin alias) → one `watch`.
  Three near-identical video skills answer the same trigger.
- `ai-head-of-engineering` + its 9 sub-skills, duplicated across 3 roots
  (30 dirs, zero recorded usage) → 1 orchestrator + `references/` files.
- `aeo-*` (11 skills) → `aeo-orchestrator` + reference files for the stages.
- `openkb-deck-neon` + `openkb-deck-editorial` → one deck skill with a theme
  parameter.
- `vercel-*` (6 vendored guideline packs, zero usage) → one reference pack.

### DELETE / ARCHIVE — approved and executed 2026-07-12

71 items moved to `~/.claude/skills-archive/2026-07-12/` (see `MANIFEST.txt`
there for every path). `plaid` + `founders-build-stack` kept per user decision.
`watch-video` merged into `watch` (dir archived, host symlinks removed).
Repo-tracked removals (`content-ideas-okf`, `vercel-*`, `ponytail*`) now show
as deletions in `git status` on this branch — commit them with the branch.
Original groups as approved:

- **Group A, cruft:** `watch.bak-20260703023028`, `content-ideas-okf`
  (no SKILL.md), `imported/scaffold-exercises` dirs in claude/codex roots.
- **Group B, toy skills:** `time-skill`, `time-tokyo`, `weather-fetcher`,
  `weather-fetcher-tokyo`.
- **Group C, superseded:** `plaid` + `founders-build-stack` (CLAUDE.md:
  BuilderOS supersedes PLAID; keep only while in-flight PLAID builds exist),
  `watch-video` (after merge into `watch`).
- **Group D, unused gstack/broadside pack (~35 skills, many 1,000+ lines):**
  `autoplan`, `ship`, `land-and-deploy`, `plan-ceo-review`*, `plan-eng-review`,
  `plan-design-review`, `plan-devex-review`, `design-review`,
  `design-consultation`, `design-html`, `design-shotgun`, `devex-review`,
  `cso`, `qa`, `qa-only`, `canary`, `benchmark`, `retro`, `freeze`, `unfreeze`,
  `careful`, `cheat`, `checkpoint`, `guard`, `health`, `investigate`, `learn`,
  `browse`, `codex`, `pair-agent`, `document-release`, `setup-deploy`,
  `setup-browser-cookies`, `google-ads`, `dub`.
  (*`plan-ceo-review` and `office-hours` each used once — excluded from the
  archive list if you want to keep the gstack planning pair.)
- **Group E, unused vendored packs:** `ponytail` family (6), `vercel-*` (6).

Recommended action for C–E is **archive** to `~/.claude/skills-archive/2026-07-12/`
(reversible), not deletion.

## New this audit

- **`skills-analyst` skill** — the AI-systems-analyst role, installed at
  `~/.claude/skills/skills-analyst/` (master), symlinked into `.codex`,
  `.agents`, `.gemini` roots, vendored in repo `skills/skills-analyst/`.
  Bundles `scripts/audit.py` (stdlib-only) that regenerates the full
  inventory/usage/divergence report. Hard rule baked in: never delete
  without explicit confirmation.
