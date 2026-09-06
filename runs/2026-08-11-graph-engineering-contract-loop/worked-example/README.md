# Worked example: skill integrity audit

A real contract loop on real work — auditing all 315 skills in this repo for
defects that break invocation, routing, or cross-host portability.

Chosen because it clears the Stage 0 fit gate honestly:

1. **Being wrong costs more than tokens** — the mirror drift this run fixed sat
   undetected for three months.
2. **"Good" is writable** — six of the seven criteria are scripts.
3. **A script would partly do** — so rung 1 is a script, and only criterion 7
   needs judgment. That split is the point.
4. **Steps are separable** — each criterion is independent.

## Files

| File | Role |
|---|---|
| `check_skills.py` | The deterministic checker. One `--rule` per contract criterion. |
| `contract.md` | Frozen at `Status: AGREED`, 7 criteria, with the real disputes recorded. |
| `feature_list.json` | 7 items, binary status, each naming its `verified_by`. |
| `claude-progress.txt` | Run log. |
| `.claude/agents/auditor.md` | The critic — `Read, Grep, Glob, Bash`, no write access. |

## Run it

```bash
cd runs/2026-08-11-graph-engineering-contract-loop/worked-example

python3 check_skills.py                    # rung 1: the deterministic pass
python3 ../../../skills/graph-engineering/scripts/check_contract.py --dir .
python3 ../../../skills/graph-engineering/scripts/verify_state.py --dir .
```

Both gates pass. `check_skills.py` exits 1 with 34 real findings.

## Result

`FAIL (77)` → `FAIL (34)` → **`FAIL (14)`**, and the 14 are the waived
cosmetic class.

| Rule | Before | After | What happened |
|---|---|---|---|
| `frontmatter` | PASS | PASS | 315/315 have a closed YAML block |
| `mirror` | PASS | PASS | fixed earlier in this run; was 4 drifted |
| `bytecode` | FAIL (46) | PASS | all 46 were false — criterion rewritten |
| `dupes` | FAIL (3) | **PASS** | 3 real collisions fixed |
| `desc` | FAIL (14) | **PASS** | real number was 36; all restored |
| `name` | FAIL (17) | FAIL (14) | 3 fixed, 14 waived with reason |

### The collisions (fixed)

Two directories each declared one invocation name, so whichever loaded last
silently won:

```
'gstack'              declared by ['gstack', 'gstack-command']
'open-gstack-browser' declared by ['connect-chrome', 'open-gstack-browser']
'pp-hackernews'       declared by ['hackernews', 'pp-hackernews']
```

All three trace to commit `7f3d602`, which imported skills under both their
directory name and their declared name. Fixed by making each `name:` match its
directory — non-destructive, reversible, and both invocation paths still
resolve. Nothing was deleted.

### The descriptions (fixed, and the criterion was wrong twice)

The length check found **14** skills under 40 characters. The real number was
**36**: descriptions had been truncated to their first line, losing ~12,700
characters of routing information including every `Use when:` trigger list.

```yaml
# ~/gstack/canary/SKILL.md — the source
description: |
  Post-deploy canary monitoring. Watches the live app for console errors,
  performance regressions, and page failures using the browse daemon. Takes
  periodic screenshots, compares against pre-deploy baselines, and alerts
  on anomalies. Use when: "monitor deploy", "canary", "post-deploy check",
  "watch production", "verify deploy". (gstack)

# skills/canary/SKILL.md — what this repo had
description: Post-deploy canary monitoring. (gstack)
```

Restored 36 from `~/gstack/*/SKILL.md`. Three more — `context-save`, `ios-fix`,
`scrape` — have no upstream template and were written from their bodies and
`triggers:` metadata, each stating its discriminator against its nearest peer
(`/context-restore`, `/ios-qa`, `/automate`). All 315 parse as YAML.

**Where the truncation actually happened matters:**
`~/.claude/skills/canary/SKILL.md` is *already* truncated, so gstack's install
step flattened the folded blocks — not the port into this repo. The host
installs are still degraded, and that is where these skills actually get
invoked from. Out of scope per this contract, recorded in
`claude-progress.txt` as the next job.

**Second criterion defect:** `rule_desc` returned early on folded blocks. After
converting 36 skills to `description: >-`, it would have passed without
measuring anything. A criterion that stops measuring is indistinguishable from
one that got satisfied. Fixed to resolve folded blocks before checking length.

## The part worth reading: the loop caught a wrong criterion

The first version of the bytecode rule walked the filesystem for `__pycache__`
and reported **46 failures** — 60% of a 77-failure total. Every one was wrong.
`__pycache__/` and `*.pyc` are in `.gitignore`, and `git ls-files` returns zero
of them. The criterion was measuring the developer's working directory rather
than what ships.

A script cannot notice that about itself. It reported `FAIL (77)` with total
confidence and correct arithmetic. Rewriting the rule to ask git what is tracked
took the count from **77 → 34**.

This is the argument for the critic role, and it happened for real rather than
being staged. It is recorded in `contract.md` under Disputes, which is what that
section is for.

Two other criteria were weakened by the same review and are recorded there:

- **Criterion 3 is cosmetic for 14 of its 17 hits.** In Claude Code the `name:`
  field is the invocation name and the directory is not, so the `pp-*` family
  installed under unprefixed directories is harmless. Only the 3 that collide
  matter — and those are criterion 2. Criterion 3 became waivable per-skill.
- **Criterion 4 is a proxy, not a measure.** A 40-character threshold does not
  decide whether a description routes correctly; `canary` fails at 39
  characters, which is not meaningfully different from 40. It was kept as a
  cheap tripwire that finds candidates, and criterion 7 was added as the one
  that actually decides — judged by the auditor, not the script.

## Criterion 7 is still failing, on purpose

The description work is done for all 39 skills. Criterion 7 is still marked
`failing`, because its `verified_by` is the auditor and the auditor has not run.
The builder does the work; the builder does not get to pass it. Unverified is
failing — that is the contract's Grading clause, and marking it `passing` here
would be exactly the self-evaluation the whole pattern exists to prevent.

Run it in a Claude Code session from this directory:

```text
/goal Work through contract.md one criterion at a time.

For each: do the work, run its check, then hand off to the auditor subagent to
grade it against contract.md. Only mark an item passing when the auditor grades
it pass. If the auditor fails an item, fix exactly what it named and resubmit.

Update feature_list.json and claude-progress.txt after each item, and commit.
Stop when every criterion passes or after 15 attempts.
```

The critic was not run here. Spawning subagents needs the Agent tool, which was
not requested — so this example is verified through rung 1 and both gates, and
rung 2 is set up and handed over rather than claimed as done.
