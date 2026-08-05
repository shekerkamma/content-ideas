#!/usr/bin/env python3
"""Extract an .xlsx workbook to readable text or JSON using the stdlib only.

Why this exists: openpyxl is frequently broken or absent on the hosts this repo
runs on, and the repo's runtime rule is stdlib-only. An .xlsx is a zip of XML,
so we read it directly. Formulas are reported alongside their cached values so a
reviewer can see both what the model computes and what it last stored.

Usage:
    python3 extract_workbook.py MODEL.xlsx                  # markdown to stdout
    python3 extract_workbook.py MODEL.xlsx --json out.json  # structured dump
    python3 extract_workbook.py MODEL.xlsx --sheet "P&L"    # one sheet only
"""

import argparse
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
RNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
CELL_RE = re.compile(r"([A-Z]+)(\d+)")


def col_to_index(col):
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n


def index_to_col(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def read_shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.iter(NS + "t")) for si in root]


def sheet_targets(z):
    """Map sheet name -> worksheet part path, via the workbook relationships."""
    rels = {}
    rel_root = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    for rel in rel_root:
        rels[rel.get("Id")] = rel.get("Target")

    out = []
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    for sheet in wb.find(NS + "sheets"):
        target = rels.get(sheet.get(RNS + "id"), "")
        target = target.lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        out.append((sheet.get("name"), target, sheet.get("state", "visible")))
    return out


def cell_value(c, shared):
    ctype = c.get("t")
    v = c.find(NS + "v")
    f = c.find(NS + "f")
    is_el = c.find(NS + "is")

    if is_el is not None:  # inline string
        text = "".join(t.text or "" for t in is_el.iter(NS + "t"))
        return text, None
    if ctype == "s" and v is not None:
        return shared[int(v.text)], None
    if ctype == "e":
        return (v.text if v is not None else "#ERR"), None

    cached = v.text if v is not None else None
    if cached is not None and ctype != "str":
        try:
            num = float(cached)
            cached = int(num) if num == int(num) and abs(num) < 1e15 else num
        except ValueError:
            pass
    formula = ("=" + (f.text or "")) if f is not None else None
    return cached, formula


def extract(path, only_sheet=None):
    z = zipfile.ZipFile(path)
    shared = read_shared_strings(z)
    book = {"file": str(path), "sheets": []}

    for name, target, state in sheet_targets(z):
        if only_sheet and name != only_sheet:
            continue
        if target not in z.namelist():
            continue
        root = ET.fromstring(z.read(target))
        data = root.find(NS + "sheetData")
        rows = []
        if data is not None:
            for row in data:
                cells = {}
                formulas = {}
                for c in row:
                    ref = c.get("r")
                    m = CELL_RE.match(ref or "")
                    if not m:
                        continue
                    ci = col_to_index(m.group(1))
                    val, formula = cell_value(c, shared)
                    if val is not None and val != "":
                        cells[ci] = val
                    if formula:
                        formulas[ci] = formula
                if cells or formulas:
                    rows.append(
                        {"row": int(row.get("r")), "cells": cells, "formulas": formulas}
                    )
        book["sheets"].append({"name": name, "state": state, "rows": rows})
    return book


def to_markdown(book):
    lines = [f"# Workbook: {book['file']}", ""]
    has_formula = False
    for sheet in book["sheets"]:
        lines.append(f"## Sheet: {sheet['name']}  ({sheet['state']})")
        lines.append("")
        for r in sheet["rows"]:
            maxc = max(list(r["cells"]) + list(r["formulas"]) + [0])
            parts = []
            for i in range(1, maxc + 1):
                val = r["cells"].get(i, "")
                formula = r["formulas"].get(i)
                if formula:
                    has_formula = True
                    parts.append(f"{formula} [{val}]" if val != "" else formula)
                else:
                    parts.append(str(val))
            line = " | ".join(parts).rstrip(" |")
            if line.strip():
                lines.append(f"r{r['row']:>3}: {line}")
        lines.append("")
    if not has_formula:
        lines.append(
            "> NOTE: no formulas found in any sheet. This workbook stores only "
            "hardcoded values, so no calculation chain can be audited from the "
            "file itself. Every identity must be re-derived externally."
        )
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("workbook")
    ap.add_argument("--json", metavar="PATH", help="write structured JSON here")
    ap.add_argument("--sheet", help="extract only this sheet")
    args = ap.parse_args()

    try:
        book = extract(args.workbook, args.sheet)
    except (zipfile.BadZipFile, KeyError) as exc:
        sys.exit(f"error: cannot read {args.workbook} as .xlsx ({exc})")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(book, fh, indent=2, ensure_ascii=False)
        print(f"wrote {args.json}")
    else:
        print(to_markdown(book))


if __name__ == "__main__":
    main()
