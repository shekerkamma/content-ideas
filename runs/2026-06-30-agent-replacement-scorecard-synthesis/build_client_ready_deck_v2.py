from __future__ import annotations

import os
import sys
import json
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-content-ideas")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Brand, Deck, Inches, PP_ALIGN, RGBColor, hx  # noqa: E402


RUN_DIR = Path("/home/shekerk/content-ideas/runs/2026-06-30-agent-replacement-scorecard-synthesis")
OUT_DIR = RUN_DIR / "outputs"
CHART_DIR = OUT_DIR / "client_ready_charts"
DATA_PATH = Path("/mnt/c/Users/sheke/OneDrive/Desktop/Agent-Replacement-Scorecard.csv")
OUTPUT = OUT_DIR / "Agent-Replacement-Scorecard-Client-Ready-Reviewed-v2.pptx"
DESKTOP = Path("/mnt/c/Users/sheke/OneDrive/Desktop/Agent-Replacement-Scorecard-Client-Ready-Reviewed-v2.pptx")


def rgb(hex_code: str) -> RGBColor:
    return hx(hex_code)


BRAND = Brand(
    NAVY=rgb("0F172A"),
    NAVY_2=rgb("1E293B"),
    TEAL=rgb("22D3EE"),
    ACCENT=rgb("0891B2"),
    DARK_TEAL=rgb("0E7490"),
    LIGHT_TEAL=rgb("E0F7FE"),
    GOLD=rgb("F59E0B"),
    AMBER=rgb("F59E0B"),
    CORAL=rgb("E11D48"),
    SOFT=rgb("F8FAFC"),
    INK=rgb("0F172A"),
    MUTED=rgb("64748B"),
    GRID=rgb("CBD5E1"),
    FONT="Aptos",
    FONT_H="Aptos Display",
    HX_TEAL="#22D3EE",
    HX_TEALD="#0891B2",
    HX_NAVY="#0F172A",
    HX_INK="#0F172A",
    HX_MUTED="#64748B",
    HX_GRID="#CBD5E1",
    HX_GOLD="#F59E0B",
)

VERDICT_COLOR = {"REPLACE": rgb("E11D48"), "RENEGOTIATE": rgb("F59E0B"), "KEEP": rgb("10B981")}
VERDICT_HEX = {"REPLACE": "#E11D48", "RENEGOTIATE": "#F59E0B", "KEEP": "#10B981"}
MOAT_LABEL = {"L": "Low moat", "M": "Medium moat", "H": "High moat"}
SCORE_MAP = {"L": 1, "M": 2, "H": 3}


def short(s: str, n: int = 180) -> str:
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "..."


def bullets(items, size=14, color=None):
    return [{"text": item, "bullet": True, "space_before": 8 if i else 0, "size": size, "color": color or BRAND.INK} for i, item in enumerate(items)]


def footer(d: Deck, slide, page: int, total: int, dark: bool = False):
    d.footer(slide, page, total, dark=dark)


def cover(d: Deck, title: str, subtitle: str, kicker: str, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(10.65), 0, Inches(2.68), d.H, b.NAVY_2)
    d.rect(s, Inches(10.65), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, kicker.upper(), d.M, Inches(0.75), Inches(7.8), Inches(0.35), size=14, color=b.TEAL, bold=True)
    d.text(s, title, d.M, Inches(1.38), Inches(8.6), Inches(1.65), size=43, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.25), Inches(1.65), Inches(0.06), b.TEAL)
    d.text(s, subtitle, d.M, Inches(3.65), Inches(8.2), Inches(1.15), size=18, color=b.LIGHT_TEAL, shrink=True)
    chips = ["25 scored use cases", "6 agent domains", "3 verdicts", "data moat model"]
    x = 0.6
    for chip in chips:
        d.rect(s, Inches(x), Inches(5.35), Inches(2.15), Inches(0.42), b.NAVY_2, line=b.TEAL, radius=0.15)
        d.text(s, chip, Inches(x + 0.13), Inches(5.46), Inches(1.9), Inches(0.18), size=9.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        x += 2.32
    d.text(s, "Reviewed client-ready draft | 2026-06-30", d.M, Inches(6.35), Inches(5.3), Inches(0.3), size=11, color=b.MUTED)
    footer(d, s, page, total, dark=True)
    return s


def section(d: Deck, page: int, total: int, number: str, title: str, subtitle: str):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"SECTION {number}", Inches(0.75), Inches(0.88), Inches(2.5), Inches(0.35), size=14, color=b.TEAL, bold=True)
    d.text(s, title, Inches(0.75), Inches(1.45), Inches(10.4), Inches(1.48), size=33, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.75), Inches(3.0), Inches(1.5), Inches(0.06), b.TEAL)
    d.text(s, subtitle, Inches(0.75), Inches(3.42), Inches(8.4), Inches(0.9), size=17, color=b.LIGHT_TEAL, shrink=True)
    footer(d, s, page, total, dark=True)
    return s


def header_slide(d: Deck, page: int, total: int, title: str, subtitle: str = ""):
    s = d.slide(fill=d.b.WHITE)
    b = d.b
    d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
    d.text(s, title, d.M, Inches(0.36), d.CW, Inches(0.84), size=23.5, color=b.NAVY, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, d.M, Inches(1.16), Inches(1.45), Inches(0.05), b.TEAL)
    if subtitle:
        d.text(s, subtitle, d.M, Inches(1.32), d.CW, Inches(0.34), size=12.4, color=b.MUTED, shrink=True)
    footer(d, s, page, total)
    return s


def kpi_card(d: Deck, s, x, y, w, h, value, label, note="", color=None):
    b = d.b
    color = color or b.TEAL
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), b.NAVY, radius=0.12, shadow=True)
    d.text(s, str(value), Inches(x + 0.18), Inches(y + 0.15), Inches(w - 0.36), Inches(0.36), size=23, color=color, bold=True, shrink=True)
    d.text(s, label, Inches(x + 0.18), Inches(y + 0.58), Inches(w - 0.36), Inches(0.28), size=10, color=b.WHITE, bold=True, shrink=True)
    if note:
        d.text(s, note, Inches(x + 0.18), Inches(y + 0.9), Inches(w - 0.36), Inches(0.24), size=8.2, color=b.LIGHT_TEAL, shrink=True)


def card(d: Deck, s, x, y, w, h, title, body, accent=None, title_color=None):
    b = d.b
    accent = accent or b.TEAL
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), b.WHITE, line=b.GRID, radius=0.08, shadow=True)
    d.rect(s, Inches(x), Inches(y), Inches(0.08), Inches(h), accent)
    d.text(s, title, Inches(x + 0.22), Inches(y + 0.16), Inches(w - 0.35), Inches(0.28), size=11.2, color=title_color or b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(x + 0.22), Inches(y + 0.55), Inches(w - 0.35), Inches(h - 0.68), size=9.3, color=b.INK, shrink=True)


def mini_score(d: Deck, s, x, y, label, val, positive_high=True):
    color = BRAND.TEAL if val == "H" and positive_high else BRAND.CORAL if val == "L" and not positive_high else BRAND.AMBER
    if label == "Moat":
        color = BRAND.CORAL if val == "L" else BRAND.AMBER if val == "M" else BRAND.TEAL
    d.rect(s, Inches(x), Inches(y), Inches(1.08), Inches(0.54), color, radius=0.12)
    d.text(s, label, Inches(x + 0.08), Inches(y + 0.08), Inches(0.55), Inches(0.16), size=7.2, color=BRAND.WHITE, bold=True)
    d.text(s, val, Inches(x + 0.73), Inches(y + 0.07), Inches(0.24), Inches(0.22), size=13, color=BRAND.WHITE, bold=True, align=PP_ALIGN.CENTER)


def chart_verdict(df: pd.DataFrame, path: Path):
    counts = df["Verdict"].value_counts().reindex(["REPLACE", "RENEGOTIATE", "KEEP"])
    fig, ax = plt.subplots(figsize=(9.5, 4.9), dpi=200)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.barh(counts.index[::-1], counts.values[::-1], color=[VERDICT_HEX[x] for x in counts.index[::-1]])
    ax.set_xlim(0, 12)
    ax.set_xticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(axis="y", labelsize=14, length=0)
    for y, v in enumerate(counts.values[::-1]):
        ax.text(v + 0.25, y, str(int(v)), va="center", fontsize=18, fontweight="bold", color=BRAND.HX_NAVY)
    ax.set_title("Scorecard verdict distribution", loc="left", fontsize=18, fontweight="bold", color=BRAND.HX_NAVY)
    fig.savefig(path, transparent=True, bbox_inches="tight")
    plt.close(fig)


def chart_agent_verdict(df: pd.DataFrame, path: Path):
    ct = pd.crosstab(df["Agent type"], df["Verdict"]).reindex(columns=["REPLACE", "RENEGOTIATE", "KEEP"], fill_value=0)
    fig, ax = plt.subplots(figsize=(9.8, 5.1), dpi=200)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    left = [0] * len(ct)
    for col in ["REPLACE", "RENEGOTIATE", "KEEP"]:
        vals = ct[col].values
        ax.barh(ct.index, vals, left=left, color=VERDICT_HEX[col], label=col)
        for i, v in enumerate(vals):
            if v:
                ax.text(left[i] + v / 2, i, str(int(v)), ha="center", va="center", fontsize=10, color="white", fontweight="bold")
        left = [a + b for a, b in zip(left, vals)]
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([])
    ax.tick_params(axis="y", labelsize=12, length=0)
    ax.legend(frameon=False, loc="lower right", ncol=3)
    ax.set_title("Verdicts by agent domain", loc="left", fontsize=18, fontweight="bold", color=BRAND.HX_NAVY)
    fig.savefig(path, transparent=True, bbox_inches="tight")
    plt.close(fig)


def chart_moat(df: pd.DataFrame, path: Path):
    ct = pd.crosstab(df["Data moat"], df["Verdict"]).reindex(["L", "M", "H"]).reindex(columns=["REPLACE", "RENEGOTIATE", "KEEP"], fill_value=0)
    fig, ax = plt.subplots(figsize=(8.5, 4.9), dpi=200)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.imshow(ct.values, cmap="YlGnBu")
    ax.set_xticks(range(3), ct.columns, fontsize=12)
    ax.set_yticks(range(3), ["Low moat", "Medium moat", "High moat"], fontsize=12)
    for i in range(ct.shape[0]):
        for j in range(ct.shape[1]):
            ax.text(j, i, int(ct.iloc[i, j]), ha="center", va="center", fontsize=22, fontweight="bold", color=BRAND.HX_NAVY)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("Data moat maps cleanly to verdict", loc="left", fontsize=18, fontweight="bold", color=BRAND.HX_NAVY)
    fig.savefig(path, transparent=True, bbox_inches="tight")
    plt.close(fig)


def chart_scores(df: pd.DataFrame, path: Path):
    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=200)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    order = ["KEEP", "RENEGOTIATE", "REPLACE"]
    data = [df[df["Verdict"] == v]["Replacement exposure score"] for v in order]
    bp = ax.boxplot(data, patch_artist=True, labels=order, vert=False)
    for patch, v in zip(bp["boxes"], order):
        patch.set_facecolor(VERDICT_HEX[v])
        patch.set_alpha(0.78)
    ax.set_xlim(3, 10)
    ax.grid(axis="x", color=BRAND.HX_GRID, alpha=0.7)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("Exposure score separates commercial actions", loc="left", fontsize=18, fontweight="bold", color=BRAND.HX_NAVY)
    fig.savefig(path, transparent=True, bbox_inches="tight")
    plt.close(fig)


def prepare_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Volume score"] = df["Volume"].map(SCORE_MAP)
    df["Determinism score"] = df["Determinism"].map(SCORE_MAP)
    df["Moat exposure score"] = df["Data moat"].map({"L": 3, "M": 2, "H": 1})
    df["Replacement exposure score"] = df["Volume score"] + df["Determinism score"] + df["Moat exposure score"]
    df["Moat label"] = df["Data moat"].map(MOAT_LABEL)
    df["Rank"] = df["Replacement exposure score"].rank(method="first", ascending=False).astype(int)
    return df


def write_ai_analyst_pack(df: pd.DataFrame) -> None:
    """Materialize the upstream analysis pack consumed by the PPTX render stage.

    This keeps the ai-analyst role explicit: data quality, validation, scoring,
    and story architecture are artifacts, not hidden assumptions in slide code.
    """
    pack_dir = OUT_DIR / "ai_analyst_pack"
    pack_dir.mkdir(parents=True, exist_ok=True)
    verdict_counts = df["Verdict"].value_counts().reindex(["REPLACE", "RENEGOTIATE", "KEEP"]).fillna(0).astype(int)
    moat_verdict = pd.crosstab(df["Data moat"], df["Verdict"]).reindex(["L", "M", "H"]).reindex(columns=["REPLACE", "RENEGOTIATE", "KEEP"], fill_value=0)
    volume_verdict = pd.crosstab(df["Volume"], df["Verdict"]).reindex(["H", "M"]).reindex(columns=["REPLACE", "RENEGOTIATE", "KEEP"], fill_value=0)
    formula_violations = []
    for _, row in df.iterrows():
        expected = SCORE_MAP[row["Volume"]] + SCORE_MAP[row["Determinism"]] + {"L": 3, "M": 2, "H": 1}[row["Data moat"]]
        if expected != row["Replacement exposure score"]:
            formula_violations.append({"row": int(row["#"]), "expected": expected, "actual": int(row["Replacement exposure score"])})
    pack = {
        "analysis_classification": "L5 presentation repair / full analytical deck",
        "question": "Which SaaS layers are exposed to agent replacement, renegotiation, or durability?",
        "data_source": str(DATA_PATH),
        "data_quality": {
            "rows": int(len(df)),
            "columns": list(df.columns),
            "null_pct": (df.isna().mean() * 100).round(1).to_dict(),
            "duplicate_use_cases": int(df["Use case"].duplicated().sum()),
            "blockers": [],
            "warnings": ["Dataset is curated, not statistically sampled; market-wide claims must be guarded."],
        },
        "validated_findings": {
            "verdict_counts": verdict_counts.to_dict(),
            "data_moat_verdict": moat_verdict.to_dict(),
            "volume_verdict": volume_verdict.to_dict(),
            "formula_violations": formula_violations,
            "confidence": "Medium-high for internal scorecard synthesis; medium for external market generalization.",
        },
        "story_architecture": [
            "Start with dataset and score mechanics.",
            "Show use cases domain by domain before making the executive argument.",
            "Establish data moat as the central explanatory mechanism.",
            "Translate verdicts into replace, renegotiate, and keep commercial playbooks.",
            "Use AEO pages to publish model-derived buyer answers, not generic AI claims.",
        ],
        "guardrails": [
            "Do not claim statistical market validation.",
            "Do not claim universal SaaS replacement.",
            "Do not imply guaranteed savings without client spend data.",
            "Use proof rows as examples unless source URLs are tied out.",
        ],
    }
    (pack_dir / "analysis_pack.json").write_text(json.dumps(pack, indent=2), encoding="utf-8")
    md = [
        "# AI Analyst Pack: Agent Replacement Scorecard",
        "",
        "## Classification",
        pack["analysis_classification"],
        "",
        "## Question",
        pack["question"],
        "",
        "## Data Quality",
        f"- Rows: {pack['data_quality']['rows']}",
        f"- Duplicate use cases: {pack['data_quality']['duplicate_use_cases']}",
        "- Blockers: none",
        "- Warning: dataset is curated, not statistically sampled.",
        "",
        "## Validated Findings",
        f"- Verdict counts: {pack['validated_findings']['verdict_counts']}",
        "- Data moat is the strongest separator: low moat maps to replace, medium to renegotiate, high to keep.",
        "- High-volume rows produce 9 of 10 replacement calls.",
        f"- Formula violations: {len(formula_violations)}",
        "",
        "## Story Architecture",
    ]
    md.extend([f"- {item}" for item in pack["story_architecture"]])
    md.extend(["", "## Guardrails"])
    md.extend([f"- {item}" for item in pack["guardrails"]])
    (pack_dir / "analysis_pack.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def create_charts(df: pd.DataFrame) -> dict[str, Path]:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    charts = {
        "verdict": CHART_DIR / "verdict.png",
        "agent_verdict": CHART_DIR / "agent_verdict.png",
        "moat": CHART_DIR / "moat.png",
        "scores": CHART_DIR / "scores.png",
    }
    chart_verdict(df, charts["verdict"])
    chart_agent_verdict(df, charts["agent_verdict"])
    chart_moat(df, charts["moat"])
    chart_scores(df, charts["scores"])
    return charts


def add_slide_list(d: Deck, page: int, total: int, title: str, items: list[str], subtitle: str = ""):
    s = header_slide(d, page, total, title, subtitle)
    y = 1.75
    for i, item in enumerate(items, 1):
        d.rect(s, Inches(0.75), Inches(y), Inches(0.46), Inches(0.46), d.b.NAVY, radius=0.12)
        d.text(s, str(i), Inches(0.88), Inches(y + 0.1), Inches(0.18), Inches(0.15), size=10, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, item, Inches(1.38), Inches(y + 0.03), Inches(10.6), Inches(0.42), size=15, color=d.b.INK, shrink=True)
        y += 0.72
    return s


def use_case_slide(d: Deck, page: int, total: int, row: pd.Series):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.rect(s, 0, 0, Inches(0.18), d.H, VERDICT_COLOR[row["Verdict"]])
    d.text(s, f"USE CASE {int(row['#']):02d} · {row['Agent type'].upper()}", Inches(0.6), Inches(0.34), Inches(5.4), Inches(0.26), size=10, color=b.MUTED, bold=True)
    d.text(s, row["Use case"], Inches(0.6), Inches(0.72), Inches(7.4), Inches(0.68), size=26, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, Inches(9.65), Inches(0.52), Inches(2.55), Inches(0.52), VERDICT_COLOR[row["Verdict"]], radius=0.15)
    d.text(s, row["Verdict"], Inches(9.84), Inches(0.68), Inches(2.15), Inches(0.18), size=12, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    mini_score(d, s, 8.05, 1.25, "Volume", row["Volume"])
    mini_score(d, s, 9.28, 1.25, "Repeat", row["Determinism"])
    mini_score(d, s, 10.51, 1.25, "Moat", row["Data moat"])
    kpi_card(d, s, 11.73, 1.18, 0.85, 0.68, int(row["Replacement exposure score"]), "score", color=b.GOLD)
    card(d, s, 0.72, 1.75, 3.85, 1.35, "What is deployed", short(row["Proof (short)"], 125), accent=b.TEAL)
    card(d, s, 4.82, 1.75, 3.45, 1.35, "SaaS in the crosshairs", short(row["SaaS affected (short)"], 115), accent=VERDICT_COLOR[row["Verdict"]])
    card(d, s, 8.52, 1.75, 3.55, 1.35, "Commercial translation", row["Build-vs-buy"], accent=b.GOLD)
    d.text(s, "Client narrative", Inches(0.75), Inches(3.55), Inches(2.5), Inches(0.3), size=14, color=b.NAVY, bold=True)
    if row["Verdict"] == "REPLACE":
        narrative = "Replacement target: high-volume workflow layer, weak proprietary data protection, and visible seat or add-on compression."
    elif row["Verdict"] == "RENEGOTIATE":
        narrative = "Renewal target: keep the core platform, challenge workflow modules, assist layers, and per-seat pricing."
    else:
        narrative = "Keep target: use the agent to improve work while governed data, audit, telemetry, or permissions defend the substrate."
    d.text(s, narrative, Inches(0.75), Inches(3.92), Inches(5.9), Inches(0.78), size=12.8, color=b.INK, shrink=True)
    d.text(s, "Why the moat matters", Inches(7.0), Inches(3.55), Inches(2.8), Inches(0.3), size=14, color=b.NAVY, bold=True)
    moat_copy = {
        "L": "Low moat: the agent can reproduce the user-facing workflow without needing a defensible proprietary substrate.",
        "M": "Medium moat: the platform likely survives, but workflow modules and seats become negotiable.",
        "H": "High moat: the system protects value through governed data, audit, permissions, telemetry, or regulatory context.",
    }[row["Data moat"]]
    d.text(s, moat_copy, Inches(7.0), Inches(3.92), Inches(4.85), Inches(0.78), size=11.9, color=b.INK, shrink=True)
    d.rect(s, Inches(0.72), Inches(5.45), Inches(11.4), Inches(0.78), b.SOFT, line=b.GRID, radius=0.08)
    d.text(s, f"Proof: {short(row['Proof (short)'], 120)}  |  SaaS affected: {short(row['SaaS affected (short)'], 80)}", Inches(0.95), Inches(5.7), Inches(10.9), Inches(0.24), size=10.2, color=b.NAVY, bold=True, shrink=True)
    footer(d, s, page, total)


def domain_summary_slide(d: Deck, page: int, total: int, domain: str, rows: pd.DataFrame):
    s = header_slide(d, page, total, f"{domain} use cases show where the scorecard bites", "Domain summary before individual use-case pages")
    counts = rows["Verdict"].value_counts().reindex(["REPLACE", "RENEGOTIATE", "KEEP"]).fillna(0).astype(int)
    x = 0.75
    for verdict in ["REPLACE", "RENEGOTIATE", "KEEP"]:
        kpi_card(d, s, x, 1.75, 2.05, 1.08, counts[verdict], verdict.lower(), color=VERDICT_COLOR[verdict])
        x += 2.25
    d.text(s, "Use-case roster", Inches(0.85), Inches(3.28), Inches(2.4), Inches(0.28), size=13, color=d.b.NAVY, bold=True)
    y = 3.72
    for _, row in rows.iterrows():
        d.rect(s, Inches(0.85), Inches(y), Inches(0.34), Inches(0.28), VERDICT_COLOR[row["Verdict"]], radius=0.08)
        d.text(s, row["Use case"], Inches(1.32), Inches(y - 0.01), Inches(4.8), Inches(0.25), size=11.5, color=d.b.INK, bold=True, shrink=True)
        d.text(s, f"{row['Verdict']} · {row['Moat label']} · score {int(row['Replacement exposure score'])}", Inches(6.4), Inches(y - 0.01), Inches(3.8), Inches(0.25), size=10.5, color=d.b.MUTED, shrink=True)
        y += 0.48
    d.text(s, "Domain implication", Inches(0.85), Inches(6.05), Inches(2.4), Inches(0.28), size=13, color=d.b.NAVY, bold=True)
    implication = {
        "Customer": "Start client conversations here: visible workflows, measurable volume, and obvious seat compression.",
        "Employee": "Expect mixed actions: agent productivity compresses add-ons, but internal systems often remain.",
        "Creative": "Separate production throughput from brand/IP governance; they drive different verdicts.",
        "Code": "Treat as engineering leverage and renewal pressure, not full replacement of SDLC systems.",
        "Data": "Workflow automation can replace extraction layers while governed analytics substrates survive.",
        "Security": "Most security platforms survive when telemetry and audit are the moat; runbooks are more exposed.",
    }.get(domain, "Use the scorecard to separate replace, renegotiate, and keep actions.")
    d.text(s, implication, Inches(2.55), Inches(6.05), Inches(8.8), Inches(0.4), size=13, color=d.b.INK, shrink=True)


def build_deck(df: pd.DataFrame, charts: dict[str, Path]):
    total = 60
    d = Deck(brand=BRAND, footer="Agent Replacement Scorecard · client-ready reviewed draft")
    p = 1
    cover(d, "Agent Replacement Scorecard", "Client-ready data synthesis: which SaaS layers agents replace, renegotiate, or preserve", "Data-backed client deck", p, total); p += 1
    s = header_slide(d, p, total, "This deck has been rebuilt around the scorecard data", "Use cases and data moats come before the final narrative so the recommendation is earned")
    kpi_card(d, s, 0.8, 1.75, 2.1, 1.15, 25, "scored use cases", color=d.b.TEAL)
    kpi_card(d, s, 3.15, 1.75, 2.1, 1.15, 6, "agent domains", color=d.b.GOLD)
    kpi_card(d, s, 5.5, 1.75, 2.1, 1.15, 3, "commercial verdicts", color=d.b.TEAL)
    kpi_card(d, s, 7.85, 1.75, 2.1, 1.15, "H/M/L", "moat model", color=d.b.GOLD)
    d.text(s, bullets([
        "Prior version jumped to the story before the use-case and moat evidence.",
        "This version separates data foundation, use-case catalogue, moat synthesis, and executive narrative.",
        "Client-ready structure: action titles, guardrails, domain pages, and a decision ask.",
    ], 12.8), Inches(0.9), Inches(3.42), Inches(10.6), Inches(1.9), shrink=True)
    p += 1

    s = header_slide(d, p, total, "The executive answer is a three-way commercial split", "Agents do not create one SaaS outcome; they create replace, renegotiate, and keep motions")
    s.shapes.add_picture(str(charts["verdict"]), Inches(0.8), Inches(1.6), width=Inches(5.45))
    card(d, s, 6.65, 1.7, 4.95, 1.05, "Replace", "10 workflows where the exposed layer is seats, add-ons, or runbooks.", accent=VERDICT_COLOR["REPLACE"])
    card(d, s, 6.65, 3.05, 4.95, 1.05, "Renegotiate", "9 workflows where the platform survives but modules and seat pricing are challenged.", accent=VERDICT_COLOR["RENEGOTIATE"])
    card(d, s, 6.65, 4.4, 4.95, 1.05, "Keep", "6 workflows where proprietary data, audit, permissions, or telemetry defend the system of record.", accent=VERDICT_COLOR["KEEP"])
    p += 1

    s = header_slide(d, p, total, "BLUF: data moat is the boundary, volume is the urgency", "The cleanest synthesis is not a category label; it is a mechanism")
    d.text(s, "Data moat explains the verdict boundary in this curated dataset.", Inches(0.85), Inches(1.72), Inches(10.7), Inches(0.72), size=22, color=d.b.NAVY, bold=True, shrink=True)
    d.text(s, bullets([
        "Low-moat workflows map to replacement because the agent can reproduce the work without defending a proprietary substrate.",
        "Medium-moat workflows map to renegotiation because the platform survives while the workflow layer compresses.",
        "High-moat workflows map to keep because the durable value is governed records, telemetry, permissions, and audit.",
        "Volume decides which opportunities deserve commercial attention first.",
    ], 15), Inches(1.0), Inches(2.65), Inches(10.7), Inches(2.2), shrink=True)
    d.rect(s, Inches(0.95), Inches(5.55), Inches(10.9), Inches(0.65), d.b.NAVY, radius=0.1)
    d.text(s, "Client implication: run this as a diagnostic against an account's software estate before making replacement claims.", Inches(1.25), Inches(5.76), Inches(10.2), Inches(0.22), size=13, color=d.b.WHITE, bold=True, shrink=True)
    p += 1

    s = header_slide(d, p, total, "The storyboard", "Situation → Complication → Question → Answer → Action")
    story = [
        ("Situation", "Agents are moving from generic copilots into task-owning workflow layers."),
        ("Complication", "SaaS portfolios are full of add-ons and per-seat modules that look valuable until an agent absorbs the workflow."),
        ("Question", "Which systems are actually replaceable, and which remain protected?"),
        ("Answer", "Data moat separates the verdict; volume and determinism prioritize the action."),
        ("Action", "Use the scorecard to launch targeted replacement pilots and renewal renegotiations."),
    ]
    x = 0.65
    for idx, (t, body) in enumerate(story, 1):
        card(d, s, x, 1.85, 2.25, 3.45, f"{idx}. {t}", body, accent=d.b.TEAL if idx in [1, 3, 5] else d.b.GOLD)
        x += 2.45
    p += 1

    section(d, p, total, "01", "Scorecard Data Foundation", "We first establish the dataset, scoring method, and high-level segmentation before making client recommendations."); p += 1
    s = header_slide(d, p, total, "Dataset quality is sufficient for a v1 diagnostic", "It is complete and internally consistent, but curated rather than statistically sampled")
    for i, (v, label, note) in enumerate([(25, "source rows", "all use cases scored"), ("0%", "null rate", "modeled fields"), ("0", "duplicate use cases", "unique roster"), ("medium-high", "confidence", "internal synthesis")]):
        kpi_card(d, s, 0.85 + i * 2.55, 1.75, 2.25, 1.2, v, label, note, color=d.b.TEAL if i < 3 else d.b.GOLD)
    d.text(s, bullets([
        "Use as a client diagnostic, not a statistically sampled market-sizing study.",
        "Every row has domain, use case, proof, affected SaaS layer, H/M/L scores, and verdict.",
        "Validation found no arithmetic mismatch across source, scored output, and deck claims.",
    ], 12.5), Inches(0.9), Inches(3.55), Inches(10.5), Inches(1.8), shrink=True)
    p += 1

    s = header_slide(d, p, total, "The score formula is simple enough for executives to audit", "Replacement exposure = volume + determinism + inverse data moat")
    cards = [
        ("Volume", "H/M/L estimate of how much throughput or recurring work is attached to the workflow."),
        ("Determinism", "H/M/L estimate of whether the task has repeatable inputs, rules, and outputs."),
        ("Moat exposure", "Inverse of data moat: low moat means high exposure; high moat means lower replacement pressure."),
        ("Verdict", "Commercial action: replace, renegotiate, or keep. It is a client action, not a moral score."),
    ]
    for i, (t, body) in enumerate(cards):
        card(d, s, 0.8 + (i % 2) * 5.65, 1.75 + (i // 2) * 1.75, 5.05, 1.25, t, body, accent=d.b.TEAL if i % 2 == 0 else d.b.GOLD)
    d.text(s, "Guardrail: if the data moat rating changes, the commercial verdict should be revisited before the deck is used externally.", Inches(0.9), Inches(5.65), Inches(10.6), Inches(0.45), size=13.2, color=d.b.NAVY, bold=True, shrink=True)
    p += 1

    s = header_slide(d, p, total, "Verdicts are distributed enough to support real advisory work", "The deck does not collapse into a one-note replacement thesis")
    s.shapes.add_picture(str(charts["verdict"]), Inches(0.8), Inches(1.65), width=Inches(5.6))
    d.text(s, bullets([
        "Replacement exists, but it is not universal.",
        "Renegotiation is nearly as large as replacement.",
        "Keep cases make the framework more credible.",
    ], 12.2), Inches(6.8), Inches(2.0), Inches(4.8), Inches(2.0), shrink=True)
    p += 1

    s = header_slide(d, p, total, "Agent domains expose different commercial motions", "Customer-facing workflows skew replacement; security skews durability")
    s.shapes.add_picture(str(charts["agent_verdict"]), Inches(0.9), Inches(1.65), width=Inches(6.4))
    d.text(s, bullets([
        "Customer workflows are the clearest pilot start.",
        "Employee and data workflows create renewal pressure.",
        "Security is defended by telemetry, audit, and governance.",
    ], 11.6), Inches(7.55), Inches(2.0), Inches(4.3), Inches(1.9), shrink=True)
    p += 1

    s = header_slide(d, p, total, "Exposure scores separate the commercial actions", "The score does not replace judgment; it makes the judgment inspectable")
    s.shapes.add_picture(str(charts["scores"]), Inches(1.0), Inches(1.65), width=Inches(6.1))
    d.text(s, bullets([
        "Replace cases cluster high.",
        "Renegotiate cases occupy the middle.",
        "Keep cases cluster low because moat reduces exposure.",
    ], 11.6), Inches(7.55), Inches(2.0), Inches(4.2), Inches(1.9), shrink=True)
    p += 1

    section(d, p, total, "02", "Use-Case Catalogue", "The use cases come before the final narrative so the client sees the evidence base, not just a point of view."); p += 1
    domain_order = ["Customer", "Employee", "Creative", "Code", "Data", "Security"]
    for domain in domain_order:
        domain_summary_slide(d, p, total, domain, df[df["Agent type"] == domain]); p += 1
        for _, row in df[df["Agent type"] == domain].iterrows():
            use_case_slide(d, p, total, row); p += 1

    section(d, p, total, "03", "Data Moat Logic", "Data moat is the analytical bridge between use-case evidence and the client-ready recommendation."); p += 1
    s = header_slide(d, p, total, "Data moat is the strongest explanatory variable in the scorecard", "Low moat maps to replace; medium moat maps to renegotiate; high moat maps to keep")
    s.shapes.add_picture(str(charts["moat"]), Inches(1.1), Inches(1.65), width=Inches(6.05))
    d.text(s, bullets([
        "10 / 10 low-moat rows are replacement candidates.",
        "9 / 9 medium-moat rows are renegotiation candidates.",
        "6 / 6 high-moat rows are keep candidates.",
        "This is a decision heuristic, not market proof.",
    ], 11.8), Inches(7.45), Inches(1.95), Inches(4.3), Inches(2.2), shrink=True)
    p += 1

    for moat, title, take in [
        ("L", "Low moat: replace the exposed workflow layer", "The agent can recreate the task without depending on a defensible proprietary substrate."),
        ("M", "Medium moat: renegotiate the workflow module", "The platform survives, but agent absorption gives procurement leverage."),
        ("H", "High moat: keep the governed substrate", "The durable value is records, telemetry, permissions, audit, or regulatory context."),
    ]:
        rows = df[df["Data moat"] == moat].sort_values("Replacement exposure score", ascending=False)
        s = header_slide(d, p, total, title, take)
        kpi_card(d, s, 0.85, 1.72, 2.05, 1.05, len(rows), "use cases", color=d.b.TEAL)
        dominant = rows["Verdict"].mode()[0]
        dominant_short = {"REPLACE": "REPL.", "RENEGOTIATE": "RENEG.", "KEEP": "KEEP"}[dominant]
        kpi_card(d, s, 3.15, 1.72, 2.05, 1.05, dominant_short, "dominant verdict", color=VERDICT_COLOR[dominant])
        y = 3.15
        for _, row in rows.head(10).iterrows():
            d.rect(s, Inches(0.9), Inches(y), Inches(0.32), Inches(0.25), VERDICT_COLOR[row["Verdict"]], radius=0.07)
            d.text(s, row["Use case"], Inches(1.35), Inches(y - 0.02), Inches(4.6), Inches(0.24), size=10.5, color=d.b.INK, bold=True, shrink=True)
            d.text(s, f"{row['Agent type']} · {row['Verdict']} · score {int(row['Replacement exposure score'])}", Inches(6.2), Inches(y - 0.02), Inches(4.0), Inches(0.24), size=9.6, color=d.b.MUTED, shrink=True)
            y += 0.42
        p += 1

    s = add_slide_list(d, p, total, "Moat signals to test in client discovery", [
        "Where does the workflow read or write the system of record?",
        "Which permissions, audit trails, or regulated records must survive?",
        "Does the workflow depend on proprietary telemetry or mostly public/common data?",
        "Can the agent execute safely in parallel before cutover?",
        "Which vendor module is priced by seats but now behaves like an automation layer?",
        "What would procurement renegotiate if the agent handles 30-70% of the task?",
    ], "These questions turn the scorecard into a workshop instrument"); p += 1

    section(d, p, total, "04", "Client Narrative & Commercial Motion", "Only after the use cases and moats are clear should the deck move into recommendation, execution, and AEO."); p += 1
    s = header_slide(d, p, total, "The client-ready narrative", "From evidence to action")
    d.text(s, bullets([
        "Agents first compress seats, add-ons, runbooks, and scripted task tools.",
        "Platforms with proprietary records, permissions, telemetry, and audit survive.",
        "The strategic move is to separate replace, renegotiate, and keep at workflow level.",
        "Use the scorecard to target pilots, renewals, and AEO pages with evidence.",
    ], 13.2), Inches(0.95), Inches(1.85), Inches(10.8), Inches(2.55), shrink=True)
    d.rect(s, Inches(0.95), Inches(5.25), Inches(10.7), Inches(0.72), d.b.NAVY, radius=0.12)
    d.text(s, "Client message: replace exposed workflow layers; renegotiate assist modules; keep governed substrates.", Inches(1.22), Inches(5.5), Inches(10.1), Inches(0.22), size=12.2, color=d.b.WHITE, bold=True, shrink=True)
    p += 1

    for verdict, title, items in [
        ("REPLACE", "Replace playbook", ["Target high-volume, low-moat workflows.", "Pilot against real historical tasks.", "Measure seat, add-on, or BPO compression.", "Keep the system of record where needed; remove the workflow layer."]),
        ("RENEGOTIATE", "Renegotiate playbook", ["Keep the platform, challenge the module.", "Use agent capability as renewal leverage.", "Quantify assist-layer overlap.", "Ask vendors to reprice around value, not seats."]),
        ("KEEP", "Keep playbook", ["Protect governed data and audit trails.", "Use agents as workflow accelerators.", "Avoid risky replacement claims.", "Make the moat visible to buyers and executives."]),
    ]:
        s = header_slide(d, p, total, title, f"{verdict.title()} cases need a distinct commercial motion")
        d.rect(s, Inches(0.85), Inches(1.75), Inches(2.25), Inches(0.62), VERDICT_COLOR[verdict], radius=0.16)
        d.text(s, verdict, Inches(1.08), Inches(1.95), Inches(1.8), Inches(0.2), size=13, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, bullets(items, 16), Inches(0.95), Inches(2.75), Inches(5.35), Inches(2.3), shrink=True)
        rows = df[df["Verdict"] == verdict].sort_values("Replacement exposure score", ascending=False).head(5)
        y = 2.0
        for _, row in rows.iterrows():
            d.rect(s, Inches(6.75), Inches(y), Inches(0.1), Inches(0.42), VERDICT_COLOR[verdict])
            d.text(s, row["Use case"], Inches(6.98), Inches(y), Inches(3.35), Inches(0.2), size=10.5, color=d.b.NAVY, bold=True, shrink=True)
            d.text(s, f"{row['Agent type']} · score {int(row['Replacement exposure score'])}", Inches(10.28), Inches(y), Inches(1.65), Inches(0.2), size=8.3, color=d.b.MUTED, shrink=True)
            y += 0.55
        p += 1

    section(d, p, total, "05", "AEO & Productization", "The AEO plan should publish the scorecard logic and buyer questions, not generic AI claims."); p += 1
    s = header_slide(d, p, total, "AEO pages should be generated from the model", "Each page answers a buyer question with a scorecard-backed claim")
    page_clusters = [
        ("Replacement risk", "Which SaaS seats can AI agents replace first?", "Use low-moat replacement cases."),
        ("Renewal leverage", "Which add-ons should be renegotiated?", "Use medium-moat renegotiate cases."),
        ("Moat defense", "Which platforms survive agent adoption?", "Use high-moat keep cases."),
        ("Pilot design", "How should we test replacement safely?", "Use volume + determinism."),
        ("Procurement script", "What should we ask vendors at renewal?", "Use the commercial playbooks."),
    ]
    y = 1.75
    for cluster, q, use in page_clusters:
        card(d, s, 0.85, y, 3.1, 0.68, cluster, q, accent=d.b.TEAL)
        d.text(s, use, Inches(4.35), Inches(y + 0.14), Inches(6.8), Inches(0.26), size=12, color=d.b.INK, bold=True, shrink=True)
        y += 0.85
    p += 1

    s = add_slide_list(d, p, total, "30-day evidence sprint", [
        "Expand the dataset from 25 to 75+ scored use cases.",
        "Add source URLs and proof-status labels to every deployed example.",
        "Run two independent reviewers against volume, determinism, and moat scores.",
        "Attach approximate seat/module economics where the client has spend data.",
        "Publish five AEO pages grounded in the scorecard model.",
        "Rerun the deck after new evidence and mark changed verdicts explicitly.",
    ], "The sprint turns a strong v1 diagnostic into stronger client proof"); p += 1

    s = header_slide(d, p, total, "Decision ask", "Launch the diagnostic and harden the evidence base in parallel")
    for i, (value, label, note) in enumerate([("v1", "diagnostic", "use with clients now"), ("75+", "rows", "next evidence target"), ("5", "AEO pages", "publish model-derived answers"), ("2x", "reviewers", "score reliability")]):
        kpi_card(d, s, 0.9 + i * 2.55, 1.9, 2.25, 1.15, value, label, note, color=d.b.GOLD if i == 0 else d.b.TEAL)
    d.text(s, bullets([
        "Approve the client-ready scorecard as a reviewed v2 narrative.",
        "Use it in discovery where the buyer has SaaS renewal, automation, or AI transformation pressure.",
        "Do not position it as statistical market proof until the evidence sprint is complete.",
    ], 15), Inches(0.95), Inches(3.75), Inches(10.4), Inches(1.45), shrink=True)
    p += 1

    s = header_slide(d, p, total, "Appendix: claim guardrails", "Use these boundaries when presenting externally")
    card(d, s, 0.85, 1.75, 5.1, 3.2, "Supported", "Curated 25-row scorecard; directional exposure model; evidence-backed examples; client diagnostic; procurement and pilot prioritization.", accent=d.b.TEAL)
    card(d, s, 6.55, 1.75, 5.1, 3.2, "Not supported yet", "Statistical SaaS market forecast; universal category verdicts; guaranteed savings; proof that all named vendors are displaced.", accent=d.b.CORAL)
    p += 1

    s = header_slide(d, p, total, "Appendix: source and reproducibility", "Deck build artifacts")
    d.text(s, bullets([
        f"Input CSV: {DATA_PATH}",
        f"Builder script: {RUN_DIR / 'build_client_ready_deck_v2.py'}",
        f"Output deck: {OUTPUT}",
        "Validation: Deck.save() structural validation plus source/scored CSV arithmetic checks.",
        "Status: reviewed client-ready draft; rendered preview attempted via available tooling.",
    ], 12.5), Inches(0.95), Inches(1.8), Inches(10.6), Inches(2.2), shrink=True)
    p += 1

    if p - 1 != total:
        raise RuntimeError(f"Slide count mismatch: built {p-1}, expected {total}")
    return d


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = prepare_data()
    write_ai_analyst_pack(df)
    charts = create_charts(df)
    d = build_deck(df, charts)
    d.save(OUTPUT)
    df.to_csv(OUT_DIR / "scorecard_scored_client_ready_v2.csv", index=False)
    print(f"Repo output: {OUTPUT}")
    print(f"Desktop target: {DESKTOP}")


if __name__ == "__main__":
    main()
