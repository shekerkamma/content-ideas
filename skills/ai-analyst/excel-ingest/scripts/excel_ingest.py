#!/usr/bin/env python3
"""Turn an Excel workbook into analysis-ready CSVs for the ai-analyst pipeline.

The pipeline is DataFrame-first: once a sheet is loaded correctly, every
profiler and agent runs on it unchanged. The only weak link is the file-to-frame
step, and a bare ``pd.read_excel(path)`` fails *silently* on the normal shape of
a business export — a title row above the table becomes the column names and the
row count is inflated by the banner rows. Nothing raises. This module finds the
real header row, names what it found, and refuses to guess which sheet holds the
data when more than one is plausible.

CLI
---
    python3 excel_ingest.py book.xlsx --list
    python3 excel_ingest.py book.xlsx --sheet Sales --out-dir ./data
    python3 excel_ingest.py book.xlsx --all-sheets --out-dir ./data
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:  # pragma: no cover - guarded at CLI
    pd = None

HEADER_SCAN_ROWS = 25
#: A sheet needs at least this many data rows to be treated as a data table
#: rather than a summary/pivot block.
DATA_SHEET_MIN_ROWS = 15


class ExcelIngestError(RuntimeError):
    """Raised when the workbook cannot be resolved without guessing."""


# ---------------------------------------------------------------------------
# Header detection
# ---------------------------------------------------------------------------

def detect_header(raw, scan=HEADER_SCAN_ROWS):
    """Return ``(header_row_index, confidence)`` for a header-less frame.

    A header row is a row whose filled cells are all strings, sitting above a
    row whose cells are *not* all strings. Both halves matter: the first alone
    matches a title banner, and the second alone matches any numeric row.
    Confidence is ``"high"`` when both hold, ``"low"`` when we fell back to
    row 0 without evidence.
    """
    best_row, best_score, best_both = 0, -1, False
    limit = min(scan, max(len(raw) - 1, 0))
    for i in range(limit):
        row = raw.iloc[i]
        filled = int(row.notna().sum())
        if filled < 2:
            continue  # a banner line is usually one populated cell
        all_strings = all(isinstance(v, str) for v in row.dropna())
        below = raw.iloc[i + 1]
        below_typed = (
            int(below.notna().sum()) >= 2
            and not all(isinstance(v, str) for v in below.dropna())
        )
        score = filled + (10 if all_strings else 0) + (10 if below_typed else 0)
        if score > best_score:
            best_row, best_score, best_both = i, score, (all_strings and below_typed)
    return best_row, ("high" if best_both else "low")


def _merged_ranges(path, sheet_name):
    """Merged cells are the tell for a hand-built report; report, never repair."""
    try:
        from openpyxl import load_workbook
    except ImportError:
        return None
    try:
        wb = load_workbook(path, read_only=False)
        return [str(r) for r in wb[sheet_name].merged_cells.ranges]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Inspection
# ---------------------------------------------------------------------------

def enumerate_sheets(path):
    """Describe every sheet: size, detected header row, and whether it looks
    like a data table or a summary block."""
    if pd is None:
        raise ExcelIngestError("pandas is required: pip install pandas openpyxl")
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Workbook not found: {path}")
    if path.suffix.lower() == ".xls":
        raise ExcelIngestError(
            f"{path.name} is a legacy .xls workbook, which needs the `xlrd` engine "
            "(not installed). Re-save it as .xlsx and re-run."
        )

    book = pd.ExcelFile(path)
    out = []
    for name in book.sheet_names:
        raw = book.parse(name, header=None)
        header_row, confidence = detect_header(raw)
        data_rows = max(len(raw) - header_row - 1, 0)
        out.append(
            {
                "sheet": name,
                "total_rows": int(len(raw)),
                "columns": int(raw.shape[1]),
                "header_row": int(header_row),
                "header_confidence": confidence,
                "data_rows": int(data_rows),
                "looks_like": "data" if data_rows >= DATA_SHEET_MIN_ROWS else "summary",
                "merged_ranges": _merged_ranges(path, name),
            }
        )
    return out


def resolve_sheet(path, sheet=None):
    """Pick the sheet to analyze, or refuse.

    Guessing here is how you analyze a pivot table and report it as the data.
    When two sheets both look like data tables, this raises and names them.
    """
    sheets = enumerate_sheets(path)
    if sheet is not None:
        names = [s["sheet"] for s in sheets]
        if sheet not in names:
            raise ExcelIngestError(f"Sheet {sheet!r} not in workbook. Available: {names}")
        return next(s for s in sheets if s["sheet"] == sheet)

    candidates = [s for s in sheets if s["looks_like"] == "data"]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise ExcelIngestError(
            "No sheet has enough rows to be a data table "
            f"(need >= {DATA_SHEET_MIN_ROWS}). Sheets: "
            + ", ".join(f"{s['sheet']}({s['data_rows']} rows)" for s in sheets)
            + ". Pass --sheet explicitly if one of these really is the data."
        )
    raise ExcelIngestError(
        "Multiple sheets look like data tables: "
        + ", ".join(f"{s['sheet']}({s['data_rows']} rows)" for s in candidates)
        + ". Pass --sheet to choose — this step does not guess."
    )


# ---------------------------------------------------------------------------
# Loading and conversion
# ---------------------------------------------------------------------------

def load_sheet(path, sheet=None, header_row=None):
    """Return ``(DataFrame, info)`` for one sheet, with the header row resolved."""
    info = resolve_sheet(path, sheet)
    hdr = info["header_row"] if header_row is None else int(header_row)
    df = pd.read_excel(path, sheet_name=info["sheet"], header=hdr)
    df = df.dropna(how="all").dropna(axis=1, how="all")
    df.columns = [str(c).strip() for c in df.columns]
    unnamed = [c for c in df.columns if c.startswith("Unnamed:")]
    df = df.reset_index(drop=True).infer_objects()
    info = dict(info, header_row_used=hdr, unnamed_columns=unnamed,
                loaded_rows=int(len(df)), loaded_columns=int(df.shape[1]))
    return df, info


def _slug(text):
    return "".join(c if c.isalnum() else "_" for c in str(text)).strip("_").lower()


def convert(path, out_dir, sheet=None, all_sheets=False, header_row=None):
    """Write one CSV per converted sheet. Returns a list of result dicts."""
    path, out_dir = Path(path), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    targets = (
        [s["sheet"] for s in enumerate_sheets(path)]
        if all_sheets
        else [resolve_sheet(path, sheet)["sheet"]]
    )
    results = []
    for name in targets:
        df, info = load_sheet(path, name, header_row if not all_sheets else None)
        dest = out_dir / f"{_slug(path.stem)}__{_slug(name)}.csv"
        df.to_csv(dest, index=False)
        results.append(dict(info, csv_path=str(dest)))
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("workbook")
    ap.add_argument("--list", action="store_true", help="describe sheets and exit")
    ap.add_argument("--sheet", help="sheet name to convert")
    ap.add_argument("--all-sheets", action="store_true")
    ap.add_argument("--header-row", type=int, help="override header detection (0-based)")
    ap.add_argument("--out-dir", default=".", help="where to write CSVs")
    args = ap.parse_args(argv)

    if pd is None:
        print("ERROR: pandas is required (pip install pandas openpyxl)", file=sys.stderr)
        return 2
    try:
        if args.list:
            print(json.dumps(enumerate_sheets(args.workbook), indent=2))
            return 0
        results = convert(args.workbook, args.out_dir, args.sheet,
                          args.all_sheets, args.header_row)
    except (ExcelIngestError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for r in results:
        warn = ""
        if r["header_confidence"] == "low":
            warn += "  [!] header row not confidently detected — verify the columns"
        if r["unnamed_columns"]:
            warn += f"  [!] unnamed columns: {r['unnamed_columns']}"
        print(f"{r['csv_path']}  ({r['loaded_rows']} rows x {r['loaded_columns']} cols, "
              f"header_row={r['header_row_used']}){warn}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
