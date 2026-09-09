#!/usr/bin/env python3
"""Normalize validated DeepGrid dossiers into analytical matrices and an SWD chart."""

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

THREAT_SCORE = {"NONE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3}
GATES = ["A-sample", "false-positive-data", "ISO-26262", "AIS-162", "IATF-16949", "AEC-Q100", "supply-continuity"]


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def validate(path, validator):
    result = subprocess.run([sys.executable, str(validator), str(path)], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"dossier validation failed for {path}:\n{result.stdout}{result.stderr}")


def ratio(num, den):
    return "" if not den else round(num / den, 4)


def chart(segment_rows, out, ai_root):
    try:
        sys.path.insert(0, str(ai_root))
        from helpers.chart_helpers import action_title, save_chart, swd_style
        import matplotlib.pyplot as plt
        import numpy as np
    except Exception as exc:
        return f"chart unavailable: {exc}"
    competitors = [row["competitor"] for row in segment_rows]
    values = [[float(row[f"segment_{s}_ordinal"]) if row[f"segment_{s}_ordinal"] != "" else np.nan for s in "ABC"] for row in segment_rows]
    colors = swd_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    masked = np.ma.masked_invalid(np.array(values, dtype=float))
    cmap = plt.matplotlib.colors.ListedColormap(["#E5E7EB", "#FCD34D", "#F59E0B", "#DC2626"])
    cmap.set_bad("#F7F6F2")
    ax.imshow(masked, vmin=0, vmax=3, cmap=cmap, aspect="auto")
    ax.set_xticks(range(3), ["Segment A", "Segment B", "Segment C"])
    ax.set_yticks(range(len(competitors)), competitors)
    for i, row in enumerate(segment_rows):
        for j, seg in enumerate("ABC"):
            label = row[f"segment_{seg}_threat"]
            ax.text(j, i, "N/A" if label == "NOT_ASSESSABLE" else label, ha="center", va="center", fontsize=9, color=colors["gray900"])
    action_title(ax, "Threat is concentrated where evidence supports direct overlap")
    ax.tick_params(length=0)
    save_chart(fig, str(out / "segment-threat-overview.png"))
    plt.close(fig)
    return "generated"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dossier", action="append", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    skill = Path(__file__).resolve().parents[1]
    repo = skill.parents[1]
    validator = repo / "skills/deepgrid-competitive-intelligence/scripts/validate_dossier.py"
    ai_root = repo / "skills/ai-analyst"
    out = Path(args.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    dossiers = []
    for raw in args.dossier:
        path = Path(raw).resolve(); validate(path, validator)
        dossiers.append((path, json.loads(path.read_text(encoding="utf-8"))))
    names = [d[1]["competitor"]["name"] for d in dossiers]
    if len(names) != len(set(names)):
        raise ValueError("duplicate competitor names")

    segment_rows, gate_rows, evidence_rows, action_rows = [], [], [], []
    total_evidence = Counter(); total_status = Counter()
    for path, data in dossiers:
        name = data["competitor"]["name"]
        segrow = {"competitor": name, "as_of": data["competitor"]["as_of"]}
        refs = set()
        for seg in "ABC":
            item = data["segments"][seg]; label = item["threat"]
            segrow[f"segment_{seg}_threat"] = label
            segrow[f"segment_{seg}_ordinal"] = THREAT_SCORE.get(label, "")
            segrow[f"segment_{seg}_evidence_count"] = len(set(item.get("evidence_ids", [])))
            refs.update(item.get("evidence_ids", []))
        all_evidence = data.get("evidence", []); statuses = Counter(x["status"] for x in all_evidence)
        assessable = sum(segrow[f"segment_{s}_threat"] != "NOT_ASSESSABLE" for s in "ABC")
        segrow["assessable_segments"] = assessable
        segrow["high_threat_segments"] = sum(segrow[f"segment_{s}_threat"] == "HIGH" for s in "ABC")
        segment_rows.append(segrow)
        for index, value in enumerate(data["segments"]["B"].get("oem_gates", [])):
            gate_rows.append({"competitor": name, "gate_number": index + 1, "gate": GATES[index], "status": "UNAVAILABLE" if value is None else str(value).upper()})
        evidence_rows.append({
            "competitor": name, "evidence_total": len(all_evidence), "verified_count": statuses["VERIFIED"],
            "company_claim_count": statuses["COMPANY_CLAIM"], "inferred_count": statuses["INFERRED"],
            "unavailable_count": statuses["UNAVAILABLE"], "conflicted_count": statuses["CONFLICTED"],
            "verified_evidence_share": ratio(statuses["VERIFIED"], len(all_evidence)),
            "sourced_evidence_share": ratio(statuses["VERIFIED"] + statuses["COMPANY_CLAIM"] + statuses["CONFLICTED"], len(all_evidence)),
            "referenced_evidence_count": len(refs), "evidence_coverage": ratio(len(refs), len(all_evidence)),
            "known_oem_gates": sum(x is not None for x in data["segments"]["B"].get("oem_gates", [])),
        })
        for move in data.get("counter_moves", []):
            action_rows.append({"competitor": name, **{k: move.get(k, "") for k in ("owner", "action", "done_when", "trigger", "stop_or_escalate")}})
        total_evidence[name] = len(all_evidence); total_status.update(statuses)

    write_csv(out / "segment-threat-matrix.csv", list(segment_rows[0]), segment_rows)
    write_csv(out / "oem-gate-matrix.csv", ["competitor", "gate_number", "gate", "status"], gate_rows)
    write_csv(out / "evidence-confidence-matrix.csv", list(evidence_rows[0]), evidence_rows)
    write_csv(out / "action-matrix.csv", ["competitor", "owner", "action", "done_when", "trigger", "stop_or_escalate"], action_rows)
    chart_status = chart(segment_rows, out, ai_root)
    summary = {
        "schema_version": 1, "analysis_question": "Where does each competitor threaten DeepGrid by Segment A/B/C, and how strong is the supporting evidence?",
        "analysis_level": "L5", "unit_of_analysis": "competitor", "competitor_count": len(dossiers),
        "input_dossiers": [str(x[0]) for x in dossiers], "evidence_count": sum(total_evidence.values()),
        "evidence_status_counts": dict(total_status), "chart_status": chart_status,
        "comparison_status": "portfolio" if len(dossiers) >= 2 else "single-company diagnostic",
        "method_note": "Threat ordinals support display only; NOT_ASSESSABLE is excluded, not scored zero."
    }
    (out / "analysis-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    missing = sum(row[f"segment_{s}_threat"] == "NOT_ASSESSABLE" for row in segment_rows for s in "ABC")
    report = f"# Data quality report\n\n- Input dossiers: {len(dossiers)}\n- Competitors: {len(names)} (unique)\n- Evidence records: {sum(total_evidence.values())}\n- Segment cells not assessable: {missing} of {len(dossiers) * 3}\n- Chart: {chart_status}\n- Source tie-out: passed; every input passed the DeepGrid dossier validator.\n- Semantic guardrail: NOT_ASSESSABLE was preserved as missing and excluded from ordinal analysis.\n- Confidence: {'medium' if missing else 'high'}; evidence status mix is retained in `evidence-confidence-matrix.csv`.\n"
    (out / "data-quality-report.md").write_text(report, encoding="utf-8")
    print(f"BUILT: {len(dossiers)} dossier(s), {sum(total_evidence.values())} evidence records -> {out}")


if __name__ == "__main__":
    main()
