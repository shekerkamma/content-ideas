#!/usr/bin/env python3
"""AI Analyst-style audit of the Beacon.li competitor deck inputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "ai-analyst-experiment"
OUT = EXP / "outputs"
CHARTS = EXP / "charts"
OUT.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)


HEATMAP_ROWS = [
    ("Beacon.li", 5, 4, 4, 2, 2, 4),
    ("WalkMe/SAP", 3, 5, 5, 5, 5, 5),
    ("Rocketlane", 3, 4, 5, 4, 4, 4),
    ("Unframe AI", 4, 4, 4, 3, 4, 4),
    ("UiPath", 3, 5, 5, 4, 5, 4),
    ("Accenture/IBM", 3, 5, 5, 5, 5, 5),
    ("Pendo/Whatfix", 2, 5, 4, 5, 4, 3),
]
SCORE_COLS = ["execution_depth", "trust", "system_fit", "proof", "distribution", "threat"]

ARENA = {
    "Beacon.li": "Target",
    "WalkMe/SAP": "DAP",
    "Pendo/Whatfix": "DAP",
    "Rocketlane": "Implementation ops",
    "Unframe AI": "Enterprise AI",
    "UiPath": "Automation",
    "Accenture/IBM": "Consulting",
}

POSTURE = {
    "Beacon.li": "own",
    "WalkMe/SAP": "compete/reframe",
    "Pendo/Whatfix": "position away",
    "Rocketlane": "integrate/partner",
    "Unframe AI": "compete on specificity",
    "UiPath": "compete on domain model",
    "Accenture/IBM": "partner/attach",
}


def swd_style():
    plt.rcParams.update(
        {
            "figure.facecolor": "#F7F6F2",
            "axes.facecolor": "#F7F6F2",
            "axes.edgecolor": "#D1D5DB",
            "axes.labelcolor": "#374151",
            "xtick.color": "#374151",
            "ytick.color": "#374151",
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.color": "#E5E7EB",
            "grid.linewidth": 0.8,
        }
    )


def savefig(path: Path):
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="#F7F6F2")
    plt.close()


def load_company_table_tolerant() -> tuple[pd.DataFrame, dict]:
    """Read enough of the source table for QA even if the CSV is not strict.

    The source file has unquoted commas in several prose fields. That is a
    data-quality finding for the experiment, so keep a tolerant loader rather
    than mutating the source artifact.
    """
    path = ROOT / "outputs" / "company-table.csv"
    rows = []
    parse_warnings = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        expected = len(header)
        for line_no, row in enumerate(reader, start=2):
            if len(row) != expected:
                parse_warnings.append({"line": line_no, "expected_fields": expected, "actual_fields": len(row)})
            rows.append(
                {
                    "company": row[0] if row else "",
                    "confidence": row[-1] if row else "",
                    "raw_field_count": len(row),
                }
            )
    return pd.DataFrame(rows), {"expected_fields": expected, "parse_warnings": parse_warnings}


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    company, parse_meta = load_company_table_tolerant()
    scores = pd.DataFrame(HEATMAP_ROWS, columns=["vendor", *SCORE_COLS])
    scores["arena"] = scores["vendor"].map(ARENA)
    scores["recommended_posture"] = scores["vendor"].map(POSTURE)
    scores["enterprise_advantage"] = scores[["trust", "proof", "distribution"]].mean(axis=1)
    scores["beacon_wedge_delta"] = scores["execution_depth"] - scores["enterprise_advantage"]
    scores["threat_pressure_index"] = (
        0.25 * scores["trust"]
        + 0.25 * scores["proof"]
        + 0.25 * scores["distribution"]
        + 0.15 * scores["system_fit"]
        + 0.10 * scores["execution_depth"]
    )
    scores["proof_gap_vs_execution"] = scores["execution_depth"] - scores["proof"]
    scores["is_target"] = scores["vendor"].eq("Beacon.li")
    return company, scores, parse_meta


def data_quality(company: pd.DataFrame, scores: pd.DataFrame, parse_meta: dict) -> dict:
    checks = {
        "company_rows": int(len(company)),
        "scored_rows": int(len(scores)),
        "company_duplicate_names": int(company["company"].duplicated().sum()),
        "score_duplicate_vendors": int(scores["vendor"].duplicated().sum()),
        "company_missing_confidence": int(company["confidence"].isna().sum()),
        "scores_out_of_range": int(((scores[SCORE_COLS] < 1) | (scores[SCORE_COLS] > 5)).sum().sum()),
        "source_csv_parse_warnings": parse_meta["parse_warnings"],
        "scored_vendors_not_in_company_table": sorted(set(scores["vendor"]) - set(company["company"])),
        "company_table_not_scored": sorted(set(company["company"]) - set(scores["vendor"])),
    }
    checks["status"] = "warning" if checks["source_csv_parse_warnings"] or checks["scored_vendors_not_in_company_table"] or checks["company_table_not_scored"] else "passed"
    return checks


def write_csvs(company: pd.DataFrame, scores: pd.DataFrame, checks: dict) -> None:
    scores.to_csv(OUT / "scored-competitor-dataset.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    with (OUT / "data-quality-check.json").open("w", encoding="utf-8") as f:
        json.dump(checks, f, indent=2)


def plot_heatmap(scores: pd.DataFrame) -> None:
    swd_style()
    plot_df = scores.set_index("vendor")[SCORE_COLS]
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(plot_df.values, vmin=1, vmax=5, cmap="YlGnBu")
    ax.set_xticks(range(len(plot_df.columns)), labels=["Exec depth", "Trust", "System fit", "Proof", "Distribution", "Threat"])
    ax.set_yticks(range(len(plot_df.index)), labels=plot_df.index)
    ax.set_title("Beacon's execution edge is real, but proof and distribution lag", loc="left", fontsize=14, fontweight="bold")
    for i in range(plot_df.shape[0]):
        for j in range(plot_df.shape[1]):
            ax.text(j, i, int(plot_df.iloc[i, j]), ha="center", va="center", color="#111827", fontsize=10, fontweight="bold")
    fig.colorbar(im, ax=ax, shrink=0.75, label="Score")
    savefig(CHARTS / "01_scored_heatmap.png")


def plot_gap(scores: pd.DataFrame) -> None:
    swd_style()
    ordered = scores.sort_values("beacon_wedge_delta")
    colors = ["#D97706" if v == "Beacon.li" else "#9CA3AF" for v in ordered["vendor"]]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(ordered["vendor"], ordered["beacon_wedge_delta"], color=colors)
    ax.axvline(0, color="#374151", linewidth=1)
    ax.set_xlabel("Execution depth minus average of trust/proof/distribution")
    ax.set_title("Beacon is the only vendor with a large execution-over-proof wedge", loc="left", fontsize=14, fontweight="bold")
    ax.grid(axis="x", alpha=0.5)
    savefig(CHARTS / "02_execution_vs_enterprise_advantage_gap.png")


def plot_threat(scores: pd.DataFrame) -> None:
    swd_style()
    non_target = scores[~scores["is_target"]].sort_values("threat_pressure_index")
    colors = ["#DC2626" if v in {"WalkMe/SAP", "Accenture/IBM"} else "#9CA3AF" for v in non_target["vendor"]]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(non_target["vendor"], non_target["threat_pressure_index"], color=colors)
    ax.set_xlim(0, 5)
    ax.set_xlabel("Weighted pressure index")
    ax.set_title("WalkMe/SAP and consultancies remain the strongest pressure points", loc="left", fontsize=14, fontweight="bold")
    for i, value in enumerate(non_target["threat_pressure_index"]):
        ax.text(value + 0.05, i, f"{value:.1f}", va="center", fontsize=10)
    savefig(CHARTS / "03_threat_pressure_index.png")


def plot_proof_gap(scores: pd.DataFrame) -> None:
    swd_style()
    ordered = scores.sort_values("proof_gap_vs_execution")
    colors = ["#D97706" if v == "Beacon.li" else "#9CA3AF" for v in ordered["vendor"]]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(ordered["vendor"], ordered["proof_gap_vs_execution"], color=colors)
    ax.axvline(0, color="#374151", linewidth=1)
    ax.set_xlabel("Execution depth score minus proof score")
    ax.set_title("Beacon has the clearest proof gap relative to its execution claim", loc="left", fontsize=14, fontweight="bold")
    ax.grid(axis="x", alpha=0.5)
    savefig(CHARTS / "04_proof_gap_vs_execution_claim.png")


def report(company: pd.DataFrame, scores: pd.DataFrame, checks: dict) -> str:
    top_threats = scores[~scores["is_target"]].sort_values("threat_pressure_index", ascending=False).head(3)
    beacon = scores[scores["vendor"].eq("Beacon.li")].iloc[0]
    missing = checks["company_table_not_scored"]
    scored_missing = checks["scored_vendors_not_in_company_table"]
    lines = [
        "# AI Analyst Experiment: Beacon.li Competitor Analysis",
        "",
        "## Headline Finding",
        "",
        "The strategic answer holds up: Beacon's differentiated claim is implementation execution. The updated official-page pass improves Beacon's enterprise-readiness score, but the analytical model still makes the proof gap explicit.",
        "",
        "## Data Quality",
        "",
        f"- Company table rows: {checks['company_rows']}",
        f"- Scored heatmap rows: {checks['scored_rows']}",
        f"- Duplicate company names: {checks['company_duplicate_names']}",
        f"- Scores outside 1-5 range: {checks['scores_out_of_range']}",
        f"- Source CSV parse warnings: {len(checks['source_csv_parse_warnings'])}",
        f"- Status: {checks['status']}",
    ]
    if missing:
        lines.append(f"- Warning: company-table vendors not directly scored: {', '.join(missing)}")
    if scored_missing:
        lines.append(f"- Warning: scored grouped vendors not exact company-table rows: {', '.join(scored_missing)}")
    lines.extend(
        [
            "",
            "Interpretation: the source CSV is usable for human review but not strict enough for direct dataframe ingestion because several prose fields contain unquoted commas. The deck also uses grouped vendors (`Pendo/Whatfix`, `Accenture/IBM`) while the source table stores some individual companies. This is acceptable for executive storytelling, but analytical outputs should explicitly document grouping and parse warnings.",
            "",
            "## Derived Metrics",
            "",
            "- `enterprise_advantage` = average of trust, proof, and distribution.",
            "- `beacon_wedge_delta` = execution depth minus enterprise advantage.",
            "- `threat_pressure_index` = weighted blend of trust, proof, distribution, system fit, and execution depth.",
            "- `proof_gap_vs_execution` = execution depth minus proof quality.",
            "",
            "## What AI Analyst Adds",
            "",
            f"- Beacon wedge delta: {beacon['beacon_wedge_delta']:.1f}. This remains the strongest positive wedge in the scored set and supports the thesis.",
            f"- Beacon proof gap: {beacon['proof_gap_vs_execution']:.1f}. This is the clearest analytical reason the deck should emphasize a POC benchmark.",
            "- Beacon trust score moves from 3 to 4 after official evidence for SOC 2, RBAC, SSO, audit trails, no backend/API/database access, and `trust.beacon.li`.",
            "- The current heatmap is directionally right, but it should show derived gap metrics or a companion chart so the reader sees *why* proof is the bottleneck.",
            "- The threat matrix should separate `market threat to Beacon` from `Beacon's own vulnerability`; the current single `Threat` column mixes those concepts.",
            "",
            "## Top Threats By Weighted Pressure Index",
            "",
        ]
    )
    for _, row in top_threats.iterrows():
        lines.append(f"- {row['vendor']}: {row['threat_pressure_index']:.1f} ({row['recommended_posture']})")
    lines.extend(
        [
            "",
            "## Recommended Deck Changes",
            "",
            "1. Keep the branded PPTX as the system of record; do not replace it with a generic analytics deck.",
            "2. Add or revise one chart near the heatmap: `Execution claim vs proof gap`, using chart `04_proof_gap_vs_execution_claim.png`.",
            "3. Add a small data-quality note to the source-confidence slide: grouped vendor rows are used for executive readability.",
            "4. Consider renaming the heatmap `Threat` column to `Market pressure`, then add a separate `Beacon vulnerability` callout for proof/distribution gaps.",
            "5. Keep `ai-analyst` as an audit/charts layer in the pipeline, not the primary PPTX generator.",
            "",
            "## Charts Produced",
            "",
            "- `charts/01_scored_heatmap.png`",
            "- `charts/02_execution_vs_enterprise_advantage_gap.png`",
            "- `charts/03_threat_pressure_index.png`",
            "- `charts/04_proof_gap_vs_execution_claim.png`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    company, scores, parse_meta = load_data()
    checks = data_quality(company, scores, parse_meta)
    write_csvs(company, scores, checks)
    plot_heatmap(scores)
    plot_gap(scores)
    plot_threat(scores)
    plot_proof_gap(scores)
    (OUT / "ai-analyst-experiment-report.md").write_text(report(company, scores, checks), encoding="utf-8")
    print(OUT / "ai-analyst-experiment-report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
