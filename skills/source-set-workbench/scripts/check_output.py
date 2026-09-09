#!/usr/bin/env python3
"""Gate a workbench output against its source manifest.

The original playbook this skill adapts tells the model to mark unknowns
`INPUT REQUIRED` and never invent them. That is advice, and advice is not a
check. This script is the check.

Three failures are fatal:
  unsourced   a quantitative claim with no [Sn] citation on its line
  dangling    a citation pointing at an ID the manifest does not define
  empty       an output with no citations at all

Two are reported but not fatal by default:
  sentinel    unresolved INPUT REQUIRED / HUMAN INPUT REQUIRED markers
  unused      manifest sources no output claim ever cites

Waive a single line with a trailing `<!-- unsourced: reason -->`.

Usage:
    python3 check_output.py outputs/report.md --manifest SOURCES.md
    python3 check_output.py outputs/*.md --manifest SOURCES.md --strict --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CITE = re.compile(r"\[S(\d+)\]")
SENTINEL = re.compile(r"\b(?:HUMAN )?INPUT REQUIRED\b")
WAIVER = re.compile(r"<!--\s*unsourced:\s*.+?-->", re.I)
MANIFEST_ROW = re.compile(r"^\|\s*S(\d+)\s*\|", re.M)

# A magnitude worth sourcing: money, percent, multiplier, or a number with
# two or more significant digits. Bare "1" or "3" is usually structure, not a claim.
MAGNITUDE = re.compile(
    r"(?<![\w.])(?:"
    r"[$£€]\s?\d[\d,]*(?:\.\d+)?"      # $1,200
    r"|\d[\d,]*(?:\.\d+)?\s?%"          # 65%
    r"|\d+(?:\.\d+)?\s?[xX](?![\w])"    # 2.5x
    r"|\d[\d,]*\.\d+"                   # 69.9
    r"|\d[\d,]{1,}"                     # 100, 1,200
    r")"
)

ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
LIST_MARKER = re.compile(r"^\s*(?:[-*+]|\d{1,2}[.)])\s+")
INLINE_CODE = re.compile(r"`[^`]*`")
MD_LINK_URL = re.compile(r"\]\([^)]*\)")
HEADING_HASH = re.compile(r"^#{1,6}\s+")


def manifest_ids(path: Path) -> set[int]:
    if not path.is_file():
        return set()
    return {int(m) for m in MANIFEST_ROW.findall(path.read_text(encoding="utf-8"))}


def scrub(line: str) -> str:
    """Remove spans where a number is structure or provenance, not a claim."""
    out = line
    out = WAIVER.sub(" ", out)
    out = INLINE_CODE.sub(" ", out)
    out = MD_LINK_URL.sub(" ", out)
    out = CITE.sub(" ", out)
    out = ISO_DATE.sub(" ", out)
    out = HEADING_HASH.sub("", out)
    out = LIST_MARKER.sub("", out)
    return out


def check_file(path: Path, known: set[int], strict: bool) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    unsourced: list[dict] = []
    dangling: list[dict] = []
    sentinels: list[dict] = []
    cited: set[int] = set()

    in_fence = False
    for n, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        ids = [int(x) for x in CITE.findall(raw)]
        cited.update(ids)
        for i in ids:
            if known and i not in known:
                dangling.append({"line": n, "id": f"S{i}", "text": stripped[:120]})

        if SENTINEL.search(raw):
            sentinels.append({"line": n, "text": stripped[:120]})
            continue

        if WAIVER.search(raw):
            continue

        body = scrub(raw)
        if MAGNITUDE.search(body) and not ids:
            unsourced.append({"line": n, "text": stripped[:120]})

    failures = len(unsourced) + len(dangling)
    if not cited and (unsourced or len(lines) > 5):
        empty = True
        failures += 1
    else:
        empty = False
    if strict:
        failures += len(sentinels)

    return {
        "file": str(path),
        "unsourced": unsourced,
        "dangling": dangling,
        "sentinels": sentinels,
        "cited": sorted(cited),
        "empty": empty,
        "failures": failures,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gate a workbench output against its manifest.")
    ap.add_argument("outputs", nargs="+", help="Markdown output file(s) to check.")
    ap.add_argument("--manifest", default="SOURCES.md", help="Path to SOURCES.md.")
    ap.add_argument("--strict", action="store_true", help="Unresolved sentinels are fatal.")
    ap.add_argument("--json", action="store_true", help="Machine-readable output.")
    args = ap.parse_args(argv)

    man_path = Path(args.manifest)
    known = manifest_ids(man_path)
    if not known:
        print(f"warning: no source IDs found in {man_path} — citations cannot be validated",
              file=sys.stderr)

    reports = []
    for spec in args.outputs:
        path = Path(spec)
        if not path.is_file():
            print(f"error: not a file: {path}", file=sys.stderr)
            return 2
        reports.append(check_file(path, known, args.strict))

    all_cited: set[int] = set()
    for r in reports:
        all_cited.update(r["cited"])
    unused = sorted(known - all_cited)
    total = sum(r["failures"] for r in reports)

    if args.json:
        print(json.dumps({
            "manifest": str(man_path),
            "known_sources": len(known),
            "unused_sources": [f"S{i}" for i in unused],
            "failures": total,
            "reports": reports,
        }, indent=2))
    else:
        for r in reports:
            print(f"\n{r['file']}")
            if r["empty"]:
                print("  FAIL empty        no [Sn] citation anywhere in the output")
            for u in r["unsourced"]:
                print(f"  FAIL unsourced    L{u['line']}: {u['text']}")
            for d in r["dangling"]:
                print(f"  FAIL dangling     L{d['line']}: {d['id']} not in manifest")
            for s in r["sentinels"]:
                tag = "FAIL" if args.strict else "warn"
                print(f"  {tag} sentinel     L{s['line']}: {s['text']}")
            if not r["failures"] and not r["sentinels"]:
                print("  clean")
        if unused:
            print(f"\nwarn unused: {', '.join('S%d' % i for i in unused)} "
                  f"— indexed but never cited")
        print(f"\n{total} failure(s) across {len(reports)} file(s)")

    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
