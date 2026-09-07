# Contract: Skill integrity audit

Status: AGREED
Agreed on: 2026-08-11
Parties: builder, auditor

## Scope

Audit all 315 skills under `skills/` for integrity defects that break
invocation, routing, or cross-host portability, and fix every defect the
criteria below name.

Not in scope: changing what any skill does, deleting skills, or touching
`~/.claude/skills/` (host installs are mirrored separately).

**Scope amendment (post-freeze).** Originally this also excluded "rewriting
skill bodies". The second audit round showed the criteria cannot be satisfied
under that exclusion: a skill whose H1 and telemetry strings announce a
different skill's name still shadows it, and a duplicate pair cannot be told
apart without editing routing metadata. Scope now permits **identifier
corrections** — `name:`, `description:`, `triggers:`, self-referential headings,
telemetry labels, and documented invocation lines. Behavior, logic, and file
count remain out of scope, and deletion stays excluded, which is why the
duplicate pairs are disambiguated rather than removed.

## Criteria

| # | Criterion | Check |
|---|---|---|
| 1 | Every skill directory contains a SKILL.md with a closed YAML frontmatter block | `python3 check_skills.py --rule frontmatter` |
| 2 | No invocation name is declared by more than one skill directory | `python3 check_skills.py --rule dupes` |
| 3 | Every skill's `name:` field equals its directory name | `python3 check_skills.py --rule name` |
| 4 | Every skill's routing is reachable: a description of 40+ chars, or a `## When to invoke` section, or `triggers:` | `python3 check_skills.py --rule desc` |
| 5 | Every mirrored skill is byte-identical to its plugin copy | `python3 check_skills.py --rule mirror` |
| 6 | No generated Python bytecode is committed under skills/ or plugins/ | `python3 check_skills.py --rule bytecode` |
| ~~7~~ | **RETIRED — unsatisfiable as written.** See the third amendment. | — |
| 8 | No two skills share an identical `description:`, `triggers:`, or `## When to invoke` — the surfaces natural-language routing selects on | `python3 check_skills.py --rule routing` |
| 9 | No skill's body differs across repo trees unless registered in `cross-tree-variants.json` with evidence | `python3 check_skills.py --rule crosstree` |

## Disputes resolved during negotiation

- **Builder proposed a single criterion, "skill frontmatter is valid."** Auditor
  rejected: one criterion covering six failure modes produces a critique the
  builder cannot act on. Split into 1–6, each with its own runnable check.

- **Builder's criterion 6 originally walked the filesystem for `__pycache__`.**
  It reported 46 failures. Auditor rejected all 46: `__pycache__/` and `*.pyc`
  are in `.gitignore` and `git ls-files` returns zero of them. The criterion was
  measuring the developer's working directory, not what ships. Rewritten to ask
  git what is tracked. Failure count went 77 → 34. **This is the single most
  useful thing the negotiation produced** — the check was confidently wrong, and
  a script cannot notice that about itself.

- **Auditor challenged criterion 3 as cosmetic**, and the builder waived all 14
  on that basis. **The waiver was later rejected, 0.0.** The auditor found the
  reason recorded for 1 of 14 where the clause said per-skill, and — decisively
  — that the waiver contradicted this repo's own standard:
  `.claude/skills/skill-builder/SKILL.md:114` requires "`name` matches the
  directory name", and `reference.md:32` documents `name` as defaulting to the
  directory name. The builder had also applied the rule non-uniformly, renaming
  `hackernews` while waiving 14 siblings on the grounds that renaming has "no
  functional gain". Resolution: criterion 3 is blocking and unwaivable. All 14
  renamed; the rename was simulated first to confirm zero new collisions.

- **Auditor rejected criterion 4 as a proxy.** A 40-character threshold does not
  measure whether a description routes correctly; `canary` fails at 39
  characters, which is not a meaningful distinction from 40. Builder agreed the
  threshold is arbitrary. Resolution: criterion 4 stays as a cheap tripwire that
  finds candidates, and criterion 7 was added as the criterion that actually
  decides — judged by the auditor, not the script.

- **AMENDMENT (post-freeze): criteria 4 and 7 were both wrong and were
  rewritten.** The builder acted on criterion 4, restored 39 descriptions from
  what it believed was the upstream source, and shipped it. Three facts, found
  only afterwards, invalidated the work:

  1. The restore source (`~/gstack`, v0.16.2.0, May) is a **stale checkout**.
     The current gstack is v1.60.1.0 (July), installed at
     `~/.claude/skills/gstack/`. Fifteen of the restored descriptions were
     older text — `document-release` lost its Diataxis-mapping and
     diagram-drift wording — and some re-inlined voice-trigger prose the
     Claude host strips on purpose.
  2. Running the current generator with `--dry-run` reported **FRESH** for
     every file. Freshness there is a content comparison, so today's generator
     *produces* the short descriptions. They are not stale output.
  3. The reason is gstack's **catalog trim (T4)**: for the Claude host it
     deliberately trims the description to its first sentence and moves
     routing prose into a `## When to invoke` body section plus a
     `proactive-suggestions.json` registry, so routing is available on demand
     "without paying the always-loaded cost."

  A short description is that optimization working. Criterion 4 had encoded
  "longer is better" as though it were a fact, and enforcing it re-inflated the
  always-loaded catalog this repo is actively trying to shrink — on a branch
  named `fix/codex-skill-budget-nested-mirrors`. All 39 description edits were
  reverted; only the 3 name-collision fixes were kept.

  Criterion 4 now checks that routing is **reachable** — description, body
  section, or `triggers:` — which is the property that actually matters.
  Criterion 7's premise died with it and was repointed at the criterion-3
  waiver, which is the real remaining judgment call.

  Recorded here rather than quietly edited: a frozen contract may be amended
  when a criterion is proven wrong, but the amendment and its cause belong in
  the record.

- **SECOND AMENDMENT: criterion 8 added, because criterion 2 was measuring the
  wrong surface.** The builder fixed three name collisions by renaming, and
  criterion 2 went green. The auditor then found the collision had not been
  removed but **relocated**: all three pairs were byte-identical apart from the
  `name:` line, so each still carried an identical `description:` and identical
  `triggers:` — the surface natural-language routing actually selects on.
  `rule_dupes` hashes `name:` only, so the rename satisfied the check without
  changing the behavior the check existed to protect.

  The auditor also found `skills/connect-chrome/SKILL.md:799` still titled
  `# /open-gstack-browser` with three telemetry strings emitting that same
  other name, and eleven `README`/`CURSOR` files still instructing readers to
  invoke freed `/pp-*` names.

  Fixed: the three pairs now carry distinct deprecation-pointer routing
  metadata naming which one is canonical, the self-references are corrected,
  and the eleven dangling invocation lines are updated. Criterion 8 measures
  the routing surface directly and is mutation-tested — re-duplicating one
  description makes it fail.

  The lesson is criterion 6's lesson a second time, in a new costume: a check
  that goes green because the thing it measures moved is worse than no check,
  because it now certifies the defect.

- **THIRD AMENDMENT: criterion 7 retired, criterion 9 added.** Criterion 7 read
  "shadows nothing in the repo tree". The auditor was right that it fails, and
  right about why: **it is unsatisfiable by construction.** This repo
  deliberately keeps one skill tree per harness — `.claude/skills/`,
  `.agents/skills/`, `.github/skills/`, `skills/` for the Codex plugin,
  `plugins/content-ideas/skills/` as the packaged mirror, and
  `portable-skills/` for vendored copies moved out of the scanned tree. Every
  ported skill therefore "shadows" itself by design, and no amount of renaming
  could ever make that criterion pass. It was a criterion the builder wrote
  loosely, and it graded something the work was never able to change.

  Measuring the 38 multi-tree names showed the real shape: **33 differ only in
  frontmatter serialization**, which is intentional per-harness porting, and
  **5 differ in body**. Of those five:

  - `impeccable` — four harness copies differing only in their own script
    paths. Installed by `npx impeccable skills install`. Intentional.
  - `investor-competitive-dossier` — the `.claude` and `.agents` copies are
    deliberate routers that name `skills/` the source of truth, not stale
    forks. Intentional.
  - `openhands-niche-agency` — the `.agents` copy is a deliberate accuracy
    edit that strips unverified revenue and MCP-count claims. Syncing would
    have regressed it, and it is the copy `settings.json` actually loads.
  - `ikigai` — the `.agents` copy, which `settings.json` loads, was missing a
    whole Narrative Frame section. **Genuinely stale. Synced forward.**
  - `skill-builder` — the `.claude` copy, which Claude Code auto-discovers,
    was missing the You.com research-order rules that the global CLAUDE.md
    mandates, plus `scripts/test_host_compatibility.py`. **Genuinely stale.
    Synced forward.**

  Criterion 9 replaces 7 with the property that is both checkable and
  protective: a copy must not silently drift from the one being maintained.
  Frontmatter is excluded because per-harness serialization is intentional.
  Deliberate variants are registered in `cross-tree-variants.json` with
  evidence, which keeps the list reviewable rather than invisible — and unlike
  the criterion-3 waiver this is not a blanket excuse: removing any entry from
  the registry makes the rule fail, which is mutation-tested.

## Grading

Any criterion failing fails the item. There is no partial pass.
A criterion that cannot be verified from available evidence scores 0.0.
No criterion is waivable.

The criterion-3 waiver clause was removed after the auditor rejected the waiver
(0.0, see `traces/auditor-criterion-7.md`). Criterion 3 was fixed instead: all
14 `name:` fields now match their directories. A waiver clause that exists
mainly to excuse the one criterion nobody wanted to do is a partial pass with
extra steps.
