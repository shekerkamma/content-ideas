# Graph engineering: the contract loop

Research run, 2026-08-11. Deliverable: `skills/graph-engineering/`.

## What was ingested

| Source | Form | Capture |
|---|---|---|
| Dapta / Josue Hernandez, "Graph Engineering: The Contract Loop" | Notion, 8 pages (hub + 7 steps) | `sources/notion-guide-8-pages.md` |
| Anthropic, "Build Agents That Run for Hours" — Ash Prabaker & Andrew Wilson, AI Engineer conf, 1:15:40 | Video, native captions | `sources/anthropic-workshop-transcript.md` |

Notion pages are client-rendered; `WebFetch` returns only the JS shell. Firecrawl
with `--wait-for 6000` renders them. Three code blocks on Step 5 lazy-load and
needed `--wait-for 25000` on a second pass — worth remembering for any Notion
capture where code blocks come back as `Loading Plain Text code…`.

The workshop transcript is deduped from rolling captions (each caption line
repeats the tail of the previous one). Naive line-dedup leaves ~135 KB of
duplication; longest-suffix-prefix overlap matching gets it to 77 KB.

## Where the two sources disagree

The walkthrough is accurate on everything checkable against Anthropic's pages,
but it compresses the architecture in two ways that matter for implementation:

1. **It presents two roles. There are three.** Planner, generator, evaluator —
   a PM / IC / QA structure with a context window each. The planner writes a
   deliberately *high-level* spec and is then kept out of the loop. It does not
   plan granular technical details, because an error there cascades and
   magnifies across every downstream sprint, and it does not get to intervene
   mid-run to re-litigate whether a feature is possible. The spec is re-injected
   as a reference point instead.

2. **It omits the critic-isolation constraint.** Anthropic tried giving the
   evaluator the generator's context and backed it out: it "muddies the two
   model streams" and makes it easier for the model to kid itself that
   something works. The critic judges output only and says "this is an issue";
   the builder reflects on its own work and finds the fix. This is the single
   easiest thing to get wrong when implementing the pattern, because feeding
   the critic more context feels like an obvious improvement.

Both are encoded in the skill — see Stage 2 and Stage 3 of `SKILL.md`, and the
`## Gotchas` section.

## The load-bearing claims, with sources

| Claim | Figure | Source |
|---|---|---|
| Code merged at Anthropic authored by Claude | >80%, as of May 2026 | Anthropic, *When AI Builds Itself* |
| Multi-agent token cost | ~15× a chat turn | Anthropic, *Multi-Agent Research System* |
| Single agent with tools | ~4× a chat turn | same |
| Reference harness run | ~6 hours, ~$200 | workshop |
| Simplified harness after model upgrade | ~half the cost, better output | workshop |
| Contract criteria for one app | 27 | workshop + walkthrough |
| Judge rubric starting test cases | ~20 | Anthropic, *Multi-Agent Research System* |

The widely-circulated "80% of Anthropic engineers use self-improving loops" is a
corruption of the first row — a statistic about *code*, not people. The
percentage changes every time it recirculates, which is the tell. Not used.

Andrew Ng's HumanEval numbers (95.1% for GPT-3.5 in a loop vs 67.0% for GPT-4
single-pass) are from a Sequoia talk, not Anthropic, and are illustration only.

## What shipped

`skills/graph-engineering/` — one skill, four working scripts, mirrored
byte-identical to `plugins/content-ideas/skills/graph-engineering/`.

```
SKILL.md                      6 stages: fit gate → state layer → critic →
                              contract → loop → trace tuning → deletion
scripts/init_loop.py          scaffolds the 4 artifacts + auditor + git repo
scripts/check_contract.py     gates the contract: AGREED status, every
                              criterion has a Check, hedge-word detection
scripts/verify_state.py       binary status, verified_by present, next item
scripts/collate_traces.py     trace review packet for the tuning loop
assets/auditor.md             critic subagent — Read/Grep/Glob/Bash, no write
assets/contract-template.md   scope, criteria table, disputes, grading
references/patterns.md        the 5 patterns + cost table + when to skip
references/rubrics.md         taste rubric + judge rubric + calibration
references/sources.md         every figure traced to a first-party page
```

Verified: all four scripts exercised end to end (scaffold → reject placeholder
state → reject DRAFT contract → accept a filled contract → flag a vague one →
collate traces). Clean on all three `skill-builder` audits.

## Pre-existing test failures — diagnosed and fixed

`tests/test_plugin_contract.py` had three failures on branch
`fix/codex-skill-budget-nested-mirrors` before this run. One root cause, three
symptoms.

**Cause:** commit `7f3d602` ("Port Claude and Codex skills for cloud use") ran a
frontmatter normalizer over **199** `SKILL.md` files under `skills/`. Claude
Code's skill spec only permits a fixed set of top-level frontmatter keys, so the
normalizer moved `version`, `argument-hint`, and `user-invocable` under
`metadata.legacy-frontmatter:` and unfolded the `description: >` blocks. It ran
over **zero** files under `plugins/`, and it did not update the contract test,
which still read the old locations.

| Failing test | Symptom |
|---|---|
| `test_versions_match_across_manifests` | `_skill_version()` regex required a top-level, double-quoted `version:` — now nested and bare |
| `test_user_invocable` | regex anchored `user-invocable:` to column 0 — now indented two levels |
| `test_repo_marketplace_packages_every_shared_skill` | `plugins/` still held pre-normalization copies |

**Fix applied:**

- Re-mirrored the four drifted files canonical → plugin (`content-ideas`,
  `pipeline-runner`, `second-brain`, `karpathy-guidelines`; `plaid` had not
  drifted).
- Relaxed both regexes to accept either frontmatter position, with a comment
  explaining why the keys moved. The version *values* were never wrong — all
  four manifests and the skill agreed on `2.3.0`; only the location changed.

The normalization was deliberate and correct — it makes the skills spec
compliant — so the tests were brought to the new layout rather than reverting
199 files. `CLAUDE.md` now records the canonical layout and requires any future
normalizer pass to cover `plugins/` in the same commit.

**Result:** 151 passed, 1 skipped. `graph-engineering` is now genuinely enforced
in `PACKAGED_SKILLS` rather than shadowed by an earlier failure.

## Open threads

- The critic gets real leverage only when it can *use* the output rather than
  read about it. For non-browser work that means the `verified_by` command has
  to actually execute the thing — this repo has no worked non-browser example
  yet.
- `meta-loop` and `graph-engineering` overlap conceptually but not in shape.
  Worth revisiting whether meta-loop's worker briefs should adopt the
  contract-negotiation stage.
