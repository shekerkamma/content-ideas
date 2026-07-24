---
name: officecli-qa
description: Run optional OfficeCLI validation and render QA for Office deliverables (.docx, .xlsx, .pptx). Use as a downstream QA gate after generating or editing Word, Excel, or PowerPoint files, especially before marking a deck or report reviewed.
category: Business Automation
---

# officecli-qa

Use this skill as the shared OfficeCLI gate for Office deliverables. It does not
replace the artifact-specific builder. It adds a consistent headless
`validate -> issues -> html -> screenshot` check so agents can inspect what a
human will open.

## When To Use

- After building or editing `.pptx`, `.docx`, or `.xlsx` files.
- Before marking a PowerPoint deck `reviewed`.
- Before delivering Word reports with tables, images, headers, tracked changes,
  or page-sensitive formatting.
- Before delivering Excel dashboards, pivots, charts, or formula-heavy models.

Do not use this as the primary PDF engine. For PDFs, use the `pdf` skill and use
OfficeCLI only on the Office source artifact before PDF export or as a source
comparison aid.

## Command

From the repo root:

```bash
python3 scripts/officecli_qa.py <artifact.docx|artifact.xlsx|artifact.pptx> --out <run>/qa/officecli
```

Install OfficeCLI when missing:

```bash
curl -fsSL https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.sh | bash
officecli --version
```

The helper writes:

```text
<run>/qa/officecli/
  validate.json
  issues.json
  html.json
  screenshot.json
  qa-summary.md
  render/<artifact>.png
  <artifact>.html
```

If `officecli` is not installed, the helper exits successfully by default and
writes `Status: skipped`. Use `--required` only when OfficeCLI QA is mandatory
for the run.

## Status Rules

- `passed`: all OfficeCLI commands returned zero.
- `partial`: validation, issue scan, and HTML render ran, but screenshot render
  was blocked by managed-sandbox browser permissions. This is expected in some
  Codex sandbox runs where Chromium fails with `Operation canceled`,
  `Operation not permitted`, `setsockopt`, or `crashpad`.
- `failed`: one or more OfficeCLI commands returned non-zero; inspect the JSON
  command records and fix the artifact or fall back to the artifact-specific QA
  path.
- `skipped`: OfficeCLI is unavailable or the file is not `.docx`, `.xlsx`, or
  `.pptx`.

For client-facing decks, `skipped` or `partial` is not enough by itself to call
a file `reviewed`; run the existing artifact-specific fallback render check or
rerun the helper with sandbox escalation so screenshot render passes.

## Managed Sandbox Browser Fix

OfficeCLI screenshot mode launches a headless browser. In this WSL/Codex
managed sandbox, browser launch may fail even when Chromium and Playwright are
installed. The helper detects the known failure and records `Status: partial`
instead of conflating it with document QA failure.

For final render QA, rerun the same helper command outside the sandbox or with
approved escalation:

```bash
python3 scripts/officecli_qa.py <artifact.pptx> --out <run>/qa/officecli --required
```

Expected passing evidence:

```text
qa/officecli/qa-summary.md
qa/officecli/render/<artifact>.png
qa/officecli/<artifact>.html
```

## Fallbacks

- `.pptx`: use `preview_pptx.py`, LibreOffice/PDF, PowerPoint, Google Slides, or
  another real renderer.
- `.docx`: use the existing XML validator plus LibreOffice/PDF and Poppler image
  conversion.
- `.xlsx`: use `scripts/recalc.py` and workbook-specific formula/error checks.
- `.pdf`: use `pdf` skill validation/image conversion scripts.
