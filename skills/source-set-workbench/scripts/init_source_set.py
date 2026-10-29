#!/usr/bin/env python3
"""Scaffold a source-set workspace: one job, one manifest, one output dir.

Stdlib only. State lives under $CONTENT_HOME (default ~/Documents/Content),
never the current working directory.

Usage:
    python3 init_source_set.py "Q3 paid channel review"
    python3 init_source_set.py "US expansion" --goal "Decide whether to enter the US in 12 months"
    python3 init_source_set.py "US expansion" --adopt ~/Downloads/reports --json
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import shutil
import sys
from pathlib import Path

MANIFEST = "SOURCES.md"
BRIEF = "brief.md"

SOURCE_EXTS = {
    ".pdf", ".md", ".txt", ".csv", ".tsv", ".json", ".docx", ".xlsx",
    ".pptx", ".html", ".htm", ".vtt", ".srt", ".rtf",
}


def content_home() -> Path:
    return Path(os.environ.get("CONTENT_HOME", Path.home() / "Documents" / "Content"))


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")
    return slug[:60] or "source-set"


def next_source_id(existing: int) -> str:
    return f"S{existing + 1}"


def manifest_header(job: str, goal: str) -> str:
    today = _dt.date.today().isoformat()
    return f"""# Source manifest — {job}

One source set = one job. Every row gets a stable ID; every claim in every
output cites one. A source that is not in this table cannot be cited, and a
claim that cites nothing does not ship.

- **Job:** {job}
- **Decision this must serve:** {goal or "TBD — fill this in before Stage 1"}
- **Opened:** {today}

| ID | Title | Type | Origin | Retrieved | Trust |
|----|-------|------|--------|-----------|-------|
"""


def brief_template(job: str, goal: str) -> str:
    today = _dt.date.today().isoformat()
    return f"""# Brief — {job}

Answer all four before Stage 1. A source set without a decision attached
becomes a pile.

## 1. What am I trying to figure out?

{goal or "_TBD_"}

## 2. What information do I already have?

_List what is in `sources/` and what it covers._

## 3. What information am I missing?

_Leave blank — Stage 2 fills this in and ranks it._

## 4. What do I want created at the end?

_Name the artifact: report, deck, model, SOP, recommendation. Stage picks
follow from this._

---

- Opened: {today}
- Status: `framing`
"""


def scan_sources(src_dir: Path) -> list[Path]:
    found = []
    for path in sorted(src_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in SOURCE_EXTS:
            found.append(path)
    return found


def build_rows(files: list[Path], src_dir: Path, start: int = 0) -> list[str]:
    today = _dt.date.today().isoformat()
    rows = []
    for i, path in enumerate(files, start=start + 1):
        rel = path.relative_to(src_dir)
        kind = path.suffix.lower().lstrip(".")
        rows.append(f"| S{i} | {rel.name} | {kind} | `sources/{rel}` | {today} | unrated |")
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Scaffold a source-set workspace.")
    ap.add_argument("job", help="What this source set is for (one job).")
    ap.add_argument("--goal", default="", help="The decision the job must serve.")
    ap.add_argument("--adopt", default="", help="Copy an existing folder of sources in.")
    ap.add_argument("--root", default="", help="Override workspace root.")
    ap.add_argument("--json", action="store_true", help="Machine-readable output.")
    args = ap.parse_args(argv)

    slug = slugify(args.job)
    root = Path(args.root) if args.root else content_home() / "workbench" / slug
    src_dir = root / "sources"
    out_dir = root / "outputs"

    created = not root.exists()
    src_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    adopted = 0
    if args.adopt:
        origin = Path(args.adopt).expanduser()
        if not origin.is_dir():
            print(f"error: --adopt path is not a directory: {origin}", file=sys.stderr)
            return 2
        for path in sorted(origin.rglob("*")):
            if path.is_file() and path.suffix.lower() in SOURCE_EXTS:
                target = src_dir / path.name
                if not target.exists():
                    shutil.copy2(path, target)
                    adopted += 1

    files = scan_sources(src_dir)
    manifest = root / MANIFEST
    if not manifest.exists():
        manifest.write_text(
            manifest_header(args.job, args.goal) + "\n".join(build_rows(files, src_dir)) + "\n",
            encoding="utf-8",
        )
    else:
        existing = len(re.findall(r"^\| S\d+ \|", manifest.read_text(encoding="utf-8"), re.M))
        known = set(re.findall(r"`sources/([^`]+)`", manifest.read_text(encoding="utf-8")))
        new = [f for f in files if str(f.relative_to(src_dir)) not in known]
        if new:
            with manifest.open("a", encoding="utf-8") as fh:
                fh.write("\n".join(build_rows(new, src_dir, start=existing)) + "\n")

    brief = root / BRIEF
    if not brief.exists():
        brief.write_text(brief_template(args.job, args.goal), encoding="utf-8")

    result = {
        "root": str(root),
        "sources_dir": str(src_dir),
        "outputs_dir": str(out_dir),
        "manifest": str(manifest),
        "brief": str(brief),
        "sources_indexed": len(files),
        "adopted": adopted,
        "created": created,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"workspace: {root}")
        print(f"  sources indexed: {len(files)}" + (f" (adopted {adopted})" if adopted else ""))
        print(f"  manifest:        {manifest}")
        print(f"  brief:           {brief}")
        if not files:
            print("\n  next: drop sources into sources/ and re-run to index them.")
        if not args.goal:
            print("  next: fill in the decision this must serve in brief.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
