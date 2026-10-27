---
name: excel-ingest
description: >-
  Convert an Excel workbook into analysis-ready CSVs before any profiling or analysis runs.
  Invoke as /excel-ingest. Trigger on ".xlsx", ".xls", "spreadsheet", "workbook", "analyze this
  Excel file", "which sheet", "the header is wrong", or any analysis request whose data arrives
  as a workbook rather than a CSV. Detects the real header row, names every sheet, and refuses
  to pick between two plausible data sheets.
---

# Skill: /excel-ingest — Excel to analysis-ready CSV

## Purpose

The ai-analyst pipeline is DataFrame-first: once a sheet is loaded correctly, every profiler
and agent runs on it unchanged. The weak link is the file-to-frame step, and it fails in the
worst possible way — quietly.

A bare `pd.read_excel(path)` on a normal business export produces this:

```
read_source_direct("acme_sales.xlsx") -> (303, 5)
columns: ['ACME Trading — Confidential', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']
```

Three banner rows became data, the company name became a column, and **nothing raised**.
A profiler downstream reports five all-object columns and the analysis proceeds on garbage.
This skill exists so that never reaches an agent.

## When to Use

- Any analysis whose input is `.xlsx` / `.xlsm` — run this **before** `/explore-data`,
  `/deep-profile`, or `/analyst`.
- `read_table` raised "is an Excel workbook, not a CSV".
- The columns look like a report title, or the row count is a few higher than expected.

## Invocation

`scripts/excel_ingest.py` sits next to this file. Resolve it relative to this SKILL.md —
the skill is reachable both as a top-level skill (`~/.claude/skills/excel-ingest`, a symlink)
and as an `ai-analyst` sub-skill, so a repo-root-relative path is wrong in one of the two.

```bash
SKILL_DIR=$(dirname "$(readlink -f <path to this SKILL.md>)")   # or the repo path below
python3 "$SKILL_DIR/scripts/excel_ingest.py" <workbook> --list
python3 "$SKILL_DIR/scripts/excel_ingest.py" <workbook> --sheet Sales --out-dir <data_dir>
python3 "$SKILL_DIR/scripts/excel_ingest.py" <workbook> --all-sheets --out-dir <data_dir>
```

From a `content-ideas` checkout that path is
`skills/ai-analyst/excel-ingest/scripts/excel_ingest.py`.

`--header-row N` overrides detection when you can see the right row and the tool cannot.

## Instructions

### Step 1: Inspect before converting

Always run `--list` first and show the user what is in the workbook:

```json
{"sheet": "Sales",   "total_rows": 304, "header_row": 3, "header_confidence": "high",
 "data_rows": 300, "looks_like": "data",    "merged_ranges": ["A1:E1"]}
{"sheet": "Summary", "total_rows": 5,   "header_row": 0, "header_confidence": "high",
 "data_rows": 4,   "looks_like": "summary", "merged_ranges": []}
```

Read three fields before going further:

- **`header_confidence: low`** — detection fell back to row 0 without evidence. Show the first
  rows to the user and confirm the header before converting. Do not proceed silently.
- **`merged_ranges` non-empty** — a hand-built report, not a system export. Merged cells leave
  `NaN` in every cell but the top-left. This skill *reports* them and never repairs them:
  forward-filling a merged label is a judgment about what the author meant.
- **`looks_like`** — `summary` means a pivot or total block. Analyzing it and calling it the
  data is the single most expensive mistake in this step.

### Step 2: Choose the sheet — do not guess

With exactly one data-shaped sheet, conversion is automatic. With more than one, the tool
**refuses**:

```
ERROR: Multiple sheets look like data tables: Q1(60 rows), Q2(60 rows).
       Pass --sheet to choose — this step does not guess.
```

Ask the user which sheet, or convert with `--all-sheets` and analyze them as separate tables.
Never pick the larger one on the user's behalf.

### Step 3: Convert into the data directory

Write CSVs into the working folder's data directory so `read_table` and `list_tables` find
them. Files land as `<workbook>__<sheet>.csv`, e.g. `acme_sales__sales.csv`.

### Step 4: Report what changed, then hand off

State the header row used, the resulting shape, and any unnamed columns that survived. Then
continue into `/deep-profile` or `/analyst` against the CSV — everything downstream is
unchanged.

## Judgment rules

- **Silence is the failure mode, not an error.** `pd.read_excel` succeeds on a broken read.
  Treat a plausible-looking frame from a workbook as unverified until the header row is named.
- **Never guess between sheets.** A summary sheet analyzed as data produces confident,
  well-formatted, wrong findings — the most expensive kind.
- **Report merged cells; never repair them.** Filling them encodes an assumption about the
  author's intent that belongs to the user.
- **Row count is the cheapest check available.** Banner rows inflate it. If the user says
  "about 300 orders" and the frame has 303, the header row is wrong.
- **Legacy `.xls` is refused, not approximated.** It needs the `xlrd` engine, which is not
  installed. Ask for a re-save as `.xlsx` rather than silently trying another parser.

## Dependencies

`pandas` and `openpyxl` (present in `~/.venvs/data`). `.xls` additionally needs `xlrd`,
which is **not** installed — the tool detects this and says so rather than failing obscurely.

## Related

- `/explore-data`, `/deep-profile` — run after this, on the CSV.
- `/srm-check` — if the converted sheet carries a variant column, that gate runs first.
- `helpers/data_helpers.py` `read_table` — raises and points here when handed a workbook.
