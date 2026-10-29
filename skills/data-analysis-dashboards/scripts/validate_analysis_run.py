#!/usr/bin/env python3
"""Validate matrix-run completeness and semantic invariants."""

import csv
import json
import sys
from pathlib import Path

REQUIRED = {"segment-threat-matrix.csv", "oem-gate-matrix.csv", "evidence-confidence-matrix.csv", "action-matrix.csv", "analysis-summary.json", "data-quality-report.md"}


def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main(raw):
    root = Path(raw); errors = []
    missing = REQUIRED - {p.name for p in root.iterdir()} if root.is_dir() else REQUIRED
    if missing: errors.append(f"missing artifacts: {sorted(missing)}")
    if not errors:
        summary = json.loads((root / "analysis-summary.json").read_text(encoding="utf-8"))
        segment = rows(root / "segment-threat-matrix.csv"); evidence = rows(root / "evidence-confidence-matrix.csv")
        gates = rows(root / "oem-gate-matrix.csv")
        if len(segment) != summary.get("competitor_count"): errors.append("competitor count does not tie out")
        if sum(int(x["evidence_total"]) for x in evidence) != summary.get("evidence_count"): errors.append("evidence count does not tie out")
        if len(gates) != summary.get("competitor_count", 0) * 7: errors.append("OEM gate matrix must contain seven rows per competitor")
        for row in segment:
            for seg in "ABC":
                label, value = row[f"segment_{seg}_threat"], row[f"segment_{seg}_ordinal"]
                if label == "NOT_ASSESSABLE" and value != "": errors.append(f"{row['competitor']} segment {seg}: NOT_ASSESSABLE was scored")
                if label != "NOT_ASSESSABLE" and value not in {"0", "1", "2", "3"}: errors.append(f"{row['competitor']} segment {seg}: invalid ordinal")
    if errors:
        print("INVALID"); [print(f"- {x}") for x in errors]; return 1
    print(f"VALID: analytical run at {root}"); return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]) if len(sys.argv) == 2 else 2)
