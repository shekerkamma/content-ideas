---
name: excel-ingest
description: >-
  Convert an Excel workbook into analysis-ready CSVs before any profiling or analysis runs.
  Invoke as /excel-ingest. Trigger on ".xlsx", ".xls", "spreadsheet", "workbook", "analyze this
  Excel file", "which sheet", "the header is wrong", or any analysis request whose data arrives
  as a workbook rather than a CSV. Detects the real header row, names every sheet, and refuses
  to pick between two plausible data sheets.
---

# Excel Ingest

Read and follow the complete canonical skill at
`../../../skills/ai-analyst/excel-ingest/SKILL.md`. Run its script from the repo checkout at
`skills/ai-analyst/excel-ingest/scripts/excel_ingest.py`. Treat `skills/ai-analyst/excel-ingest/`
as the source of truth; do not add workflow logic to this wrapper.

One caution from real use: the tool assumes one table per sheet. On hand-built report sheets that
stack several tables, run `--list` first and read each table by its label instead of converting the
whole sheet.
