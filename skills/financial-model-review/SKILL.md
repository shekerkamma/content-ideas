---
name: financial-model-review
version: 0.1.0
description: Use when someone shares a spreadsheet financial or business model — startup plan, investor model, segment build-up, budget, P&L, unit-economics workbook — and wants it analysed, sanity-checked, pressure-tested for red flags, prepared for diligence or an investment committee, reconciled against a pitch deck or information memorandum, or turned into a decision memo or deck. Produces an evidence-graded analysis report behind a blocking arithmetic-integrity gate. Triggers on "analyse this model", "review this financial model", "business analysis of this spreadsheet", "check these numbers", "is this plan credible", "diligence this". Chains `ai-analyst` for the analysis itself and `strategy-consulting` for the business case.
---

# Financial Model Review

Produce a decision product about a model, not a description of it. A model is a
set of claims; this pipeline separates what the workbook *computes* from what it
*asserts*, and grades both.

State at invocation:

> Running the financial-model-review compound pipeline: extraction, deterministic
> integrity gate, driver teardown, external benchmark, adversarial review, and a
> graded analysis report.

## Non-negotiables

1. **Never interpret before the integrity gate passes or every break is
   explained.** A narrative built on broken arithmetic is worse than no
   narrative — it launders the error into a decision.
2. **Never retype numbers by hand from a screenshot or a partial read.** Extract
   with the script. Transcription errors are indistinguishable from model errors
   in the final report.
3. **Separate model-internal findings from world-facing findings.** "The
   arithmetic breaks in FY28" and "89% gross margin on a hardware kit is not
   achievable" are different claims with different evidence standards. Label
   every finding with which kind it is.
4. **Grade every judgement.** Use `Verified` (re-derived from the file),
   `Benchmarked` (checked against a cited external source), or `Judgement`
   (analyst opinion, no external proof). No ungraded assertions in the report.
5. **A model with no formulas is a finding, not a convenience.** Hardcoded
   workbooks carry no auditable calculation chain — say so prominently.

## Required reading

- [references/analysis-contract.md](references/analysis-contract.md) — run layout,
  finding schema, grading rules, report structure. Read before starting.
- [references/model-integrity-checks.md](references/model-integrity-checks.md) —
  the standard identity set, plausibility bands, and the questions that separate
  an aggressive plan from an incoherent one. Read before Stage 3.
- Read the complete instructions for `ai-analyst` before Stage 4, and for
  `strategy-consulting` before Stages 4–7.

## Relationship to `ai-analyst`

`ai-analyst` is the analytical engine for Stages 4–7 — it owns question framing,
hypothesis testing, opportunity sizing, forecasting, charting, storyboarding, and
deck creation, and this skill must not reimplement any of them.

What this skill adds is everything upstream of that handoff, which `ai-analyst`
does not cover:

- **Spreadsheet ingestion.** `ai-analyst` connects to CSV, DuckDB, Postgres,
  BigQuery, and Snowflake — not `.xlsx`. `scripts/sheets_to_csv.py` bridges that
  gap.
- **Accounting-identity validation.** `ai-analyst`'s validation stack (source
  tieout, semantic validation, triangulation) is built for product-analytics
  datasets. It does not know that EBT − Tax must equal Net Income. The Stage 3
  gate does.
- **Cross-document reconciliation and evidence grading** for claims about the
  world rather than about the dataset.

Integration rules:

- **`ask-question` is the mandatory entry point.** `guardrails`, `triangulation`,
  and `semantic-validation` are embedded in `ask-question` / `run-analysis` and
  must not be invoked separately — their own skill files say so.
- Connect the tidy CSVs as a **CSV dataset**. Do not assume DuckDB is available;
  it frequently is not.
- Pass the Stage 3 integrity results into the business context so `ai-analyst`
  never re-derives a figure this pipeline has already flagged as broken.

## Pipeline

### 1. Frame and recall
Establish one run root: `runs/<YYYY-MM-DD>-<subject>-model-review/`.
Name the **decision** the analysis serves (invest / approve budget / renegotiate /
correct before circulation) and the **audience**. The decision determines depth;
without one, this becomes trivia.

Run GBrain semantic recall for the company, sector, prior model versions, and any
past corrections. Record recall status even when empty.

### 2. Extract
```bash
python3 scripts/extract_workbook.py MODEL.xlsx > outputs/extract.md
python3 scripts/extract_workbook.py MODEL.xlsx --json outputs/extract.json
```
Stdlib only — deliberately does not depend on openpyxl, which is often broken or
absent on these hosts. Reports formulas alongside cached values, and flags a
workbook that contains no formulas at all.

Inventory every sheet: what it claims to be, what it feeds, and any prose note
the author wrote. Author notes are claims and get tested like any other.

### 3. Integrity gate (blocking)
Build a spec of period-indexed series and the identities they must satisfy, then:
```bash
python3 scripts/check_model_integrity.py outputs/spec.json --json outputs/integrity.json
```
Exit code 1 means at least one identity broke beyond tolerance. Set tolerance to
the model's own rounding unit (typically 0.01–0.02 for figures carried to two
decimals) so rounding drift never masquerades as an error — and an error never
hides behind "it's just rounding".

Cover at minimum the identities in `references/model-integrity-checks.md`, plus
every cross-sheet total the workbook claims ties out. Where the author asserts a
reconciliation in prose ("totals reconcile exactly"), test that assertion
literally.

**Do not proceed until each break is either corrected or explained in writing.**

### 4. Hand off to `ai-analyst`
Flatten the workbook to tidy CSV and connect it as a dataset:
```bash
python3 scripts/sheets_to_csv.py MODEL.xlsx --outdir data/<subject>/ --single tidy-all.csv
```
Output is one row per observation with `sheet, section, block, line_item, period,
column, value`. `section` and `block` both matter: a model that reports revenue
and gross profit in the same sheet will repeat `ADAS` as a line item under two
different sections, and merging them corrupts every downstream ratio.

Then drive the analysis through `ai-analyst`'s `ask-question` entry point —
segment contribution, growth decomposition, margin bridges, sensitivity, and
opportunity sizing. Supply the Stage 3 findings as business context.

Any sheet the flattener skips (typically a text comparison or reconciliation tab)
is not queryable and must be reviewed by reading it directly — it is usually the
sheet with the highest finding density.

### 5. Driver teardown
Decompose the top line to the smallest driver the model exposes — usually
units × price × attach rate. Then, per driver, ask what must be true in the world
for it to hold, and how that requirement scales.

Apply `strategy-consulting`
`skills/03-strategic-choice-and-economics/business-case-builder.md` for the
economics and `skills/02-market-and-competitive-intelligence/profit-pool-analysis.md`
where the model implies capturing a share of an existing pool.

Attend specifically to margin *trajectory*: a rising gross margin is a claim
about learning curves, mix shift, or pricing power, and the model must say which.
Run the margin bridge in `references/model-integrity-checks.md` to establish
which one actually drives it — the narrative defense and the arithmetic often
disagree. Flat multi-year ASPs in a market with real price erosion is a claim too.

**When the model is a forward plan supporting a raise**, read Tier 3b before
writing any finding. Every figure is an assumption, so "aggressive" is not a
defect — the tests are whether growth decomposes into checkable drivers, whether
per-segment rates are genuinely bottom-up, and whether each rate converts to a
physical unit someone can falsify. Severity is ranked by what the finding costs
in diligence, not by accounting tidiness.

### 6. External benchmark
Take the handful of drivers the case actually rests on and check them against
the world. Use `exa-api` or `you-com-search` for discovery, primary sources for
confirmation. Benchmark comparable-company gross margins, ASP trends, sales-cycle
length, and market size. Every benchmark gets a citation; uncited comparisons stay
`Judgement`.

### 7. Adversarial review
Run `grilling` against the three findings that would most change the decision.
For a genuinely contested call — a valuation, a go/no-go — escalate to
`llm-council`. The purpose is to find the strongest argument *against* your own
read before an outside reviewer does.

Then apply `strategy-consulting`
`skills/05-risk-performance-and-value-governance/risk-and-mitigation.md` to turn
surviving concerns into a register with owners and triggers.

### 8. Report
Write the decision memo per
`skills/06-alignment-and-executive-communication/decision-memo.md`. Structure and
finding schema are specified in the analysis contract. Lead with the decision and
the findings that drive it — never with a tour of the sheets.

For a deck, route through `present`; client-facing PPTX must follow the repo's
branded-template and QA gates. Charts follow `dataviz`.

### 9. Write back
Persist durable findings to GBrain: the company, the model version reviewed, each
break found, and each benchmark established. The next version of this model
should start from these corrections, not rediscover them.

## Skill Relationships

### Category
Data & Analysis

### Dependencies
- `scripts/extract_workbook.py` — stdlib `.xlsx` reader; required, since openpyxl is
  frequently broken or absent on these hosts
- `scripts/check_model_integrity.py` — the blocking Stage 3 gate
- `scripts/sheets_to_csv.py` — tidy-CSV bridge into `ai-analyst`
- `references/analysis-contract.md` — run layout, finding schema, grading rules
- `references/model-integrity-checks.md` — identity set and plausibility bands

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `ai-analyst` | Sequential downstream | always — owns framing, sizing, forecasting, charting, decks from Stage 4 | `data/<subject>/tidy-all.csv` + integrity findings as business context |
| `strategy-consulting` | Sequential downstream | always — business case, profit pool, risk register, decision memo | `outputs/findings.md` |
| `grilling` | Sequential downstream | when findings drive a contested decision | top three findings |
| `llm-council` | Alternative / Peer | escalation from `grilling` for genuinely contested calls | the decision under review |
| `investor-competitive-dossier` | Alternative / Peer | that skill reviews a *market*; this one reviews a *model* — pair them for diligence | `outputs/decision-memo.md` |
| `present` | Sequential downstream | optional — when the deliverable is a deck | `outputs/decision-memo.md` |
| `officecli` | Alternative / Peer | when the task is editing or proofreading a workbook rather than reviewing its logic | the workbook |

### Runtime Preamble

At invocation, say:
- "Running /financial-model-review — extraction, integrity gate, then analysis."
- After Stage 2: how many sheets extracted, and whether the workbook contains formulas.
- After Stage 3: the gate result, stated as breaks vs rounding drift. If any break
  is unexplained, say analysis is blocked rather than continuing quietly.
- If external benchmarking is skipped: "World-facing findings are Judgement-grade only."

---

## Gotchas

- **A `.xlsx` with no formulas is a values dump, not a model.** You cannot audit a
  calculation chain that isn't in the file. Report it, and treat the upstream
  source model as the real artifact under review.
- **Do not let rounding drift and real breaks share a sentence.** Set tolerance to
  the model's own precision. Reporting ±0.01 as a finding burns the credibility
  you need for the ±2.29 one.
- **A break whose magnitude equals another figure in the model is a structural
  error, not a typo.** Prior-year losses landing in a current-year row are the
  common case — look before calling it a rounding artifact.
- **`ai-analyst` cannot open `.xlsx`.** Always melt to CSV first, and never assume
  DuckDB is installed — the CSV connector is the reliable path.
- **Never invoke `guardrails`, `triangulation`, or `semantic-validation`
  directly.** They are embedded in `ai-analyst`'s `ask-question` / `run-analysis`
  entry points and their own files say not to call them separately.
- **Sheets the flattener skips are not sheets you can ignore.** Reconciliation and
  comparison tabs have no period columns, so they never reach the CSV — and they
  routinely carry the highest-materiality findings in the whole workbook.
- **Line-item names repeat across sections.** Melt on `section` + `block` +
  `line_item`, never `line_item` alone, or revenue and gross profit for the same
  segment silently merge into one series.
- **The workbook's own reconciliation tab is a claim, not a source of truth.**
  Test its assertions — including prose ones like "totals reconcile exactly".
- **Absence of a cash-flow statement is a gap to report, not a shortfall to
  compute.** Say what cannot be concluded instead of inferring it.

---

## Reporting the run

State which stages ran, which were skipped and why, the integrity gate result,
and the grade mix of the findings. If external benchmarking was skipped, say the
world-facing findings are `Judgement` only, and do not present them as validated.
