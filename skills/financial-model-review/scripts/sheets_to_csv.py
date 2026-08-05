#!/usr/bin/env python3
"""Flatten a financial-model workbook into tidy long-format CSV.

Exists to hand a spreadsheet model to `ai-analyst`, whose CSV connector wants
one row per observation rather than a grid. Emits:

    sheet, section, block, line_item, attrs, period, column, value

`section` is the nearest standalone heading above the table ("GROSS PROFIT
(Rs Cr)"); `block` is the header row's own leading label ("Product — UNITS").
Both are kept because either one alone can collide: a sheet may repeat the
same `block` label under two sections, or repeat the same section across
several blocks. Without them, melting a multi-block sheet silently merges
line items that share a name — "ADAS" revenue and "ADAS" gross profit become
one indistinguishable series.

`attrs` carries the non-numeric label columns that sit between the line item and
the first period (e.g. "Commercial model=Product Sales; Launch=FY2027"). These
are real analytical dimensions — recurring vs one-time revenue, launch cohort —
and dropping them silently loses findings the numbers alone cannot show.

Period columns are detected from header rows containing two or more period-like
tokens (FY2027, 2027, Q1 2027, Jan-25). Rows above the first header on a sheet
are treated as titles/notes and skipped.

Usage:
    python3 sheets_to_csv.py MODEL.xlsx --outdir data/model/
    python3 sheets_to_csv.py MODEL.xlsx --outdir data/model/ --single tidy.csv
"""

import argparse
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_workbook import extract, index_to_col  # noqa: E402

PERIOD_RE = re.compile(
    r"^(FY\s?\d{2,4}|CY\s?\d{2,4}|Q[1-4](\s?[\'’]?\d{2,4})?|"
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\-']?\d{0,4})$",
    re.IGNORECASE,
)
BARE_YEAR_RE = re.compile(r"^\d{4}$")
YEAR_MIN, YEAR_MAX = 1990, 2100


def is_period(val):
    """A bare 4-digit number is only a period inside a plausible year range.

    Without the range check, unit counts like 2200 or 8000 read as years and a
    data row gets mistaken for a header — which silently drops the rows beneath
    it instead of failing loudly.
    """
    if val in (None, ""):
        return False
    text = str(val).strip()
    if BARE_YEAR_RE.match(text):
        return YEAR_MIN <= int(text) <= YEAR_MAX
    return bool(PERIOD_RE.match(text))


def is_header_row(cells):
    """True when the row carries one unbroken run of 2+ period labels.

    Header rows legitimately open with label columns ("Product | Model |
    Launch | FY2027 | ...") and legitimately close with annotation columns
    ("... | FY2032 | Share FY32"), so periods need not span the whole row.
    What distinguishes a header is that its periods are *contiguous* and
    nothing period-like appears outside that run — a data row that happens to
    contain scattered year-like numbers fails on both counts.
    """
    ordered = sorted(cells.items())
    flags = [is_period(v) for _, v in ordered]
    best_start, best_len = -1, 0
    run_start = None
    for idx, flag in enumerate(flags + [False]):
        if flag and run_start is None:
            run_start = idx
        elif not flag and run_start is not None:
            if idx - run_start > best_len:
                best_start, best_len = run_start, idx - run_start
            run_start = None
    if best_len < 2:
        return False
    # No period labels stranded outside the main run.
    return sum(flags) == best_len


def is_number(val):
    if isinstance(val, (int, float)):
        return True
    try:
        float(str(val).replace(",", ""))
        return True
    except (ValueError, AttributeError):
        return False


def to_number(val):
    return float(str(val).replace(",", "")) if not isinstance(val, (int, float)) else float(val)


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-") or "sheet"


def tidy_sheet(sheet):
    """Melt one sheet into observation rows."""
    rows = sheet["rows"]
    periods = {}       # column index -> period label
    attr_cols = {}     # column index -> attribute name, from the header row
    block = ""         # the header row's own leading label ("Product — UNITS")
    section = ""       # nearest standalone heading above it ("GROSS PROFIT")
    out = []

    skipped_cols = {}   # trailing annotation columns, reported not silently dropped

    for r in rows:
        cells = r["cells"]
        if not cells:
            continue
        # A genuine header row redefines the column->period map.
        if is_header_row(cells):
            periods = {i: v for i, v in cells.items() if is_period(v)}
            first = min(cells)
            label = cells[first] if first not in periods else ""
            block = str(label).strip()
            # label columns between the line item and the first period
            first_period = min(periods)
            attr_cols = {i: str(v).strip() for i, v in cells.items()
                         if first < i < first_period and str(v).strip()}
            # Columns after the period run (e.g. "Share FY32", "GM FY32") are
            # not period-indexed, so they cannot be melted. They are usually
            # derived and recomputable, but say so rather than dropping quietly.
            for i, v in cells.items():
                if i > max(periods) and str(v).strip():
                    skipped_cols[str(v).strip()] = index_to_col(i)
            continue

        if not any(is_number(v) for v in cells.values()):
            # A standalone short line is a section heading; a long one is prose.
            # Only headings should scope the rows beneath them.
            text = str(cells[min(cells)]).strip()
            if len(cells) == 1 and len(text) < 60 and not text.endswith("."):
                section = text
            continue

        if not periods:
            continue

        first = min(cells)
        line_item = str(cells[first]).strip()
        if is_number(cells[first]) or not line_item:
            continue

        attrs = "; ".join(
            f"{name}={str(cells[i]).strip()}"
            for i, name in sorted(attr_cols.items())
            if cells.get(i) not in (None, "") and not is_number(cells.get(i))
        )
        for col, period in sorted(periods.items()):
            val = cells.get(col)
            if val is None or val == "" or not is_number(val):
                continue
            out.append(
                {
                    "sheet": sheet["name"],
                    "section": section,
                    "block": block,
                    "line_item": line_item,
                    "attrs": attrs,
                    "period": str(period).strip(),
                    "column": index_to_col(col),
                    "value": to_number(val),
                }
            )
    if skipped_cols:
        for name, col in sorted(skipped_cols.items(), key=lambda x: x[1]):
            print(f"    note: column {col} \"{name}\" is not period-indexed and was "
                  f"not melted (derived value — recompute if needed)")
    return out


FIELDS = ["sheet", "section", "block", "line_item", "attrs", "period", "column", "value"]


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("workbook")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--single", metavar="NAME",
                    help="also write every sheet into one combined CSV")
    args = ap.parse_args()

    book = extract(args.workbook)
    os.makedirs(args.outdir, exist_ok=True)

    combined = []
    for sheet in book["sheets"]:
        rows = tidy_sheet(sheet)
        if not rows:
            print(f"  (skip) {sheet['name']}: no period-indexed rows detected")
            continue
        path = os.path.join(args.outdir, f"{slug(sheet['name'])}.csv")
        write_csv(path, rows)
        combined.extend(rows)
        items = len({r["line_item"] for r in rows})
        print(f"  wrote {path}  ({len(rows)} obs, {items} line items)")

    if args.single and combined:
        path = os.path.join(args.outdir, args.single)
        write_csv(path, combined)
        print(f"  wrote {path}  ({len(combined)} obs, combined)")

    if not combined:
        sys.exit("no period-indexed data found — check the header rows")


if __name__ == "__main__":
    main()
