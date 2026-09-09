# Provenance: the causal and experimentation port

## What was ported, and from where

Upstream is `github.com/ai-analyst-lab/ai-analyst-plugin` (MIT, Shane Butler,
AI Analyst Lab) — the **AI Analyst Plus** plugin for Claude Cowork, v1.0.0,
first commit 2026-08-26. `skills/ai-analyst/LICENSE` already carries that
copyright: this repo's `ai-analyst` was itself converted from an earlier,
pre-rehome revision of the same project, committed here as `7f3d602` on
2026-08-09. This port is therefore a **partial catch-up**, not a new adoption.

Ported on 2026-08-30:

| Landed at | From upstream | Contents |
|---|---|---|
| `causal/` | `skills/causal/` | SKILL.md + `scripts/causal_stats/` (8 modules) |
| `srm-check/` | `skills/srm-check/` | SKILL.md + `scripts/srm.py` |
| `reliability/` | `skills/reliability/` | SKILL.md + `scripts/reliability_stats.py` |
| `design-experiment/scripts/experiment_stats/` | `skills/experiment/scripts/` | 9 modules, folded into the existing skill |
| `agents/` (10 files) | `agents/` | 5 causal, `confound-scanner`, 4 experiment |

## What was deliberately NOT ported

- **The 14 name-shared skills** (`archaeology`, `close-the-loop`,
  `compare-datasets`, `connect-data`, `data-quality-check`, `forecast`,
  `guardrails`, `knowledge-bootstrap`, `log-correction`, `patterns`,
  `question-framing`, `tracking-gaps`, `triangulation`,
  `visualization-patterns`). This repo already owns that workflow, adapted for
  Claude Code. Re-porting would overwrite a Claude-Code-shaped tree with a
  Cowork-shaped one.
- **`agents/experiment-designer.md`.** Ours is 16,624 bytes against upstream's
  16,032 and is already wired into the registry with a `hypothesis` dependency.
  Keeping ours removed the only agent name collision in the port.
- **Cowork host plumbing** — `notion-ingest`, `setup-notion`,
  `google-slides-export`, `google-doc-export`, and upstream's `connect-data`
  (which routes through Cowork connectors we do not have). Per this repo's
  evidence-ranking rule: these exist because of upstream's host, not because
  they transfer.
- **Five drifted helpers.** `forecast_helpers.py` (+5,591 bytes upstream),
  `structural_validator.py` (+4,369), `data_helpers.py` (+4,191),
  `schema_profiler.py` (+833), `deep_profiler.py` (−8). We are behind upstream
  on all five, but our copies were adapted for Claude Code, so reconciling them
  needs a real diff review rather than an overwrite. **Open, not resolved.**

## Why adapted rather than installed

`claudex-loop` is installed rather than vendored because it makes no claim on
this repo's instruction surface. This plugin does: 14 of its 47 skill names
collide with `ai-analyst`'s sub-skills, `experiment-designer` collides in
`agents/`, and upstream's own README warns it already competes with Anthropic's
Data Analyst plugin for the same tasks. Installing it would make that a
three-way routing collision — exactly what `check_skills.py`'s `dupes` and
`routing` rules exist to catch.

## Verification performed

Run against a throwaway uv venv (pandas 3.0.5, numpy 2.4.6, scipy 1.17.1,
statsmodels 0.15.0, scikit-learn 1.9.0) — none of these are installed in
`~/.venvs/data`, which has pandas and numpy only.

- Both libraries import: 13 public functions from `causal_stats`, 23 from
  `experiment_stats`.
- `did_basic` recovered a **planted** treatment effect of 5.0 as 4.758,
  95% CI [3.39, 6.13] — the interval contains the truth. Known-answer test, not
  a smoke test.
- `srm_check([5000,5000])` → `PASS`; `srm_check([5200,4800])` → `BLOCK`,
  chi2 = 16.00, p = 6.3e-5.
- `power_proportion(0.10, 0.10)` → 14,745 per arm, the standard textbook figure
  for 10% → 11% at alpha 0.05 / power 0.80.
- `proportion_test(1000, 10000, 1100, 10000)` → p = 0.0211, significant.

`tests/test_ai_analyst_causal.py` pins these; it guards with
`pytest.importorskip`, so the suite stays green on a machine without scipy.

## One defect found in the port itself

The first pass generated each CONTRACT block mechanically, assigning
`source: agent:<first dependency>` to whichever input happened to come first. That
made `causal-report-generator` claim its `CAUSAL_QUESTION` came from the assumption
checker — a user input attributed to an agent. The registry validator did **not**
catch it: it checks that `depends_on` names resolve and that the DAG is acyclic, not
that an input's declared producer actually produces it. Every source is now named
individually, and the registry generator asserts that each `agent:X` source appears
in that agent's `depends_on`. Same class as the gates already documented in
`CLAUDE.md`: a check that passes because it never measured the thing.

## Dependencies this port adds

`causal_stats` needs **statsmodels** and, for propensity matching,
**scikit-learn** — neither is currently installed anywhere on this machine.
`experiment_stats` needs **scipy**, also absent. The skills are inert without
them and say so; nothing else in the repo imports them, and the
`content-ideas` runtime remains stdlib-only.

---

# Addendum: `excel-ingest` is repo-original, not ported

`skills/ai-analyst/excel-ingest/` (2026-08-30) has **no upstream counterpart**.
Upstream carries no Excel handling at all: across all 47 plugin skills the only
`.xlsx` reference is `read_source_direct` in the tie-out helper, a bare
`pd.read_excel(path)`. So this skill is original work in this repo and is not
covered by the upstream MIT attribution above — though it lives inside a tree
that is.

**The defect it addresses is silent, which is why it needed a skill rather than
a line of code.** Measured on a workbook with a title row, a subtitle, a blank
row and a merged `A1:E1`:

| | rows | first column |
|---|---|---|
| `pd.read_excel(path)` | **303** | `ACME Trading — Confidential` |
| `/excel-ingest` | 300 | `order_date` |

The naive read raises nothing. `tests/test_ai_analyst_excel_ingest.py` pins the
broken behaviour explicitly (`test_naive_read_is_actually_broken`) so the fixture
cannot quietly stop reproducing it — the failure this skill exists for would
otherwise become invisible the moment the fixture drifts.

`helpers/data_helpers.py` `read_table` now raises and points here when handed a
workbook. It deliberately does **not** read Excel itself: doing so would move the
silent failure deeper into the stack, into a function that has no sheet or
header-row semantics to reason with.

**Not mirrored — and that is a live defect, not a design choice.**
`portable-skills/ai-analyst/helpers/data_helpers.py` still has the old error
path and that tree has no `excel-ingest/`. See the correction below.

## Verification performed

- 9/9 tests pass with pandas + openpyxl; all 9 skip cleanly without them.
- Refusal paths exercised directly: two data-shaped sheets → refuses and names
  both; `--sheet Q2` then succeeds; a workbook with no sheet over 15 rows →
  refuses; `.xls` → refuses, naming the missing `xlrd` engine.
- End to end on the messy fixture: `/excel-ingest` → `list_tables` discovers
  `acme_sales__sales` → `read_table` returns (300, 5) → `profile_completeness`
  all COMPLETE, `profile_distributions` revenue skew −0.073,
  `profile_anomalies` 4 found.

---

# Correction (2026-08-30): portable-skills IS a loaded tree

Both this port and the causal port above were carried out on the stated belief
that `portable-skills/` is an unloaded vendored archive, so mirroring was
skipped. **That belief was false.**

```
~/.claude/skills/ai-analyst -> ../../content-ideas/portable-skills/ai-analyst
~/.codex/skills/ai-analyst  -> ../../content-ideas/portable-skills/ai-analyst
```

Both host symlinks (dated 2026-08-14) point at `portable-skills/`, so that is the
copy Claude Code and Codex actually load. The belief came from
`scripts/cross-tree-variants.json`, whose pre-existing `ai-analyst/run-analysis`
entry cited a grep of `.claude/settings.json`, `.codex-plugin/plugin.json` and
`.claude-plugin/plugin.json` returning nothing. That grep was accurate; the
inference was not. **The tree is reached by symlink, not by manifest**, which no
manifest grep can see. All three `ai-analyst*` entries now carry corrected
evidence.

Consequences, measured:

| | loaded (`portable-skills/`) | maintained (`skills/`) |
|---|---|---|
| sub-skills | 39 | 43 |
| agents | **directory absent** | 28 |
| `validate_agent_registry.py` | **absent** | present |
| SKILL.md advertises | 39 skills / 18 agents | 43 skills / 28 agents |

So the running skill has no causal inference, no experiment statistics, no
`excel-ingest`, no agents directory, and **no DAG preflight gate** — the gate
this repo added specifically to fail fast on an incomplete registry.

`skills/ai-analyst` is a strict superset: `diff -rq` reports nothing present only
in `portable-skills/` except a `__pycache__` directory. Repointing the two host
symlinks at `skills/ai-analyst` therefore loses nothing and restores the gate.

**The generalisable rule:** a manifest grep proves a tree is not referenced by a
manifest. It does not prove the tree is unloaded. Check the host skill
directories for symlinks before concluding a copy is dead — `ls -l`, not `grep`.

