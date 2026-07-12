from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-content-ideas")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Brand, Deck, Inches, PP_ALIGN, RGBColor, hx


RUN_DIR = Path("/home/shekerk/content-ideas/runs/2026-06-30-agent-replacement-scorecard-synthesis")
OUT_DIR = RUN_DIR / "outputs"
CHART_DIR = OUT_DIR / "executive_story_charts"
DATA_PATH = Path("/mnt/c/Users/sheke/OneDrive/Desktop/Agent-Replacement-Scorecard.csv")
OUTPUT = OUT_DIR / "Agent-Replacement-Scorecard-Executive-Story-Reviewed-v3.pptx"
DESKTOP = Path("/mnt/c/Users/sheke/OneDrive/Desktop/Agent-Replacement-Scorecard-Executive-Story-Reviewed-v3.pptx")


def rgb(hex_code: str) -> RGBColor:
    return hx(hex_code)


BRAND = Brand(
    NAVY=rgb("0B1020"),
    NAVY_2=rgb("162033"),
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
    HX_NAVY="#0B1020",
    HX_INK="#0F172A",
    HX_MUTED="#64748B",
    HX_GRID="#CBD5E1",
    HX_GOLD="#F59E0B",
)

VERDICT = {"REPLACE": rgb("E11D48"), "RENEGOTIATE": rgb("F59E0B"), "KEEP": rgb("10B981")}
VHEX = {"REPLACE": "#E11D48", "RENEGOTIATE": "#F59E0B", "KEEP": "#10B981"}
SCORE_MAP = {"L": 1, "M": 2, "H": 3}


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Volume score"] = df["Volume"].map(SCORE_MAP)
    df["Determinism score"] = df["Determinism"].map(SCORE_MAP)
    df["Moat exposure score"] = df["Data moat"].map({"L": 3, "M": 2, "H": 1})
    df["Exposure score"] = df["Volume score"] + df["Determinism score"] + df["Moat exposure score"]
    df["Moat"] = df["Data moat"].map({"L": "Low", "M": "Medium", "H": "High"})
    return df


def clean(s: str, n: int = 130) -> str:
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "..."


def bullet(items, size=13):
    return [{"text": x, "bullet": True, "space_before": 7 if i else 0, "size": size, "color": BRAND.INK} for i, x in enumerate(items)]


def footer(d: Deck, s, page: int, total: int, dark=False):
    d.footer(s, page, total, dark=dark)


def header(d: Deck, page: int, total: int, title: str, subtitle: str = ""):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
    d.text(s, title, d.M, Inches(0.34), d.CW, Inches(0.92), size=20.8, color=b.NAVY, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, d.M, Inches(1.14), Inches(1.4), Inches(0.05), b.TEAL)
    if subtitle:
        d.text(s, subtitle, d.M, Inches(1.3), d.CW, Inches(0.34), size=12.6, color=b.MUTED, shrink=True)
    footer(d, s, page, total)
    return s


def section(d: Deck, page: int, total: int, num: str, title: str, subtitle: str):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"SECTION {num}", Inches(0.75), Inches(0.86), Inches(2.2), Inches(0.28), size=13, color=b.TEAL, bold=True)
    d.text(s, title, Inches(0.75), Inches(1.48), Inches(10.5), Inches(1.3), size=35, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.75), Inches(3.05), Inches(1.45), Inches(0.06), b.TEAL)
    d.text(s, subtitle, Inches(0.75), Inches(3.42), Inches(8.8), Inches(0.86), size=16, color=b.LIGHT_TEAL, shrink=True)
    footer(d, s, page, total, dark=True)
    return s


def card(d: Deck, s, x, y, w, h, title, body, color=None, dark=False):
    b = d.b
    fill = b.NAVY if dark else b.WHITE
    text = b.WHITE if dark else b.INK
    line = None if dark else b.GRID
    color = color or b.TEAL
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), fill, line=line, radius=0.08, shadow=not dark)
    d.rect(s, Inches(x), Inches(y), Inches(0.08), Inches(h), color)
    d.text(s, title, Inches(x + 0.22), Inches(y + 0.16), Inches(w - 0.36), Inches(0.28), size=10.5, color=color if dark else b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(x + 0.22), Inches(y + 0.55), Inches(w - 0.36), Inches(h - 0.7), size=8.6, color=text, shrink=True)


def kpi(d: Deck, s, x, y, value, label, note="", color=None):
    b = d.b
    color = color or b.TEAL
    d.rect(s, Inches(x), Inches(y), Inches(2.25), Inches(1.05), b.NAVY, radius=0.1, shadow=True)
    d.text(s, str(value), Inches(x + 0.18), Inches(y + 0.14), Inches(1.9), Inches(0.36), size=22, color=color, bold=True, shrink=True)
    d.text(s, label, Inches(x + 0.18), Inches(y + 0.58), Inches(1.9), Inches(0.22), size=9.4, color=b.WHITE, bold=True, shrink=True)
    if note:
        d.text(s, note, Inches(x + 0.18), Inches(y + 0.84), Inches(1.9), Inches(0.18), size=7.6, color=b.LIGHT_TEAL, shrink=True)


def make_charts(df: pd.DataFrame) -> dict[str, Path]:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    charts = {}
    counts = df["Verdict"].value_counts().reindex(["REPLACE", "RENEGOTIATE", "KEEP"])
    fig, ax = plt.subplots(figsize=(8.8, 4.4), dpi=200)
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    ax.barh(counts.index[::-1], counts.values[::-1], color=[VHEX[x] for x in counts.index[::-1]])
    ax.set_xlim(0, 12); ax.set_xticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.tick_params(axis="y", labelsize=12, length=0)
    for y, v in enumerate(counts.values[::-1]):
        ax.text(v + .2, y, str(int(v)), va="center", fontsize=17, fontweight="bold", color=BRAND.HX_NAVY)
    charts["verdict"] = CHART_DIR / "verdict.png"
    fig.savefig(charts["verdict"], transparent=True, bbox_inches="tight"); plt.close(fig)

    ct = pd.crosstab(df["Data moat"], df["Verdict"]).reindex(["L", "M", "H"]).reindex(columns=["REPLACE", "RENEGOTIATE", "KEEP"], fill_value=0)
    fig, ax = plt.subplots(figsize=(7.6, 4.2), dpi=200)
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    ax.imshow(ct.values, cmap="YlGnBu")
    ax.set_xticks(range(3), ["Replace", "Renegotiate", "Keep"], fontsize=10)
    ax.set_yticks(range(3), ["Low moat", "Medium moat", "High moat"], fontsize=10)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, int(ct.iloc[i, j]), ha="center", va="center", fontsize=20, fontweight="bold", color=BRAND.HX_NAVY)
    for sp in ax.spines.values(): sp.set_visible(False)
    charts["moat"] = CHART_DIR / "moat_matrix.png"
    fig.savefig(charts["moat"], transparent=True, bbox_inches="tight"); plt.close(fig)

    ct2 = pd.crosstab(df["Agent type"], df["Verdict"]).reindex(columns=["REPLACE", "RENEGOTIATE", "KEEP"], fill_value=0)
    fig, ax = plt.subplots(figsize=(8.8, 4.5), dpi=200)
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    left = [0] * len(ct2)
    for col in ["REPLACE", "RENEGOTIATE", "KEEP"]:
        vals = ct2[col].values
        ax.barh(ct2.index, vals, left=left, color=VHEX[col], label=col)
        left = [a + b for a, b in zip(left, vals)]
    ax.set_xticks([])
    ax.tick_params(axis="y", labelsize=10, length=0)
    ax.legend(frameon=False, loc="lower right", ncol=3, fontsize=8)
    for sp in ax.spines.values(): sp.set_visible(False)
    charts["domain"] = CHART_DIR / "domain_stack.png"
    fig.savefig(charts["domain"], transparent=True, bbox_inches="tight"); plt.close(fig)
    return charts


def write_strategy_pack(df: pd.DataFrame):
    pack_dir = OUT_DIR / "ai_analyst_pack_v3"
    pack_dir.mkdir(parents=True, exist_ok=True)
    pack = {
        "role": "ai-analyst upstream pack supporting executive story deck",
        "executive_thesis": "Agents are not simply replacing SaaS categories; they are shifting value from seat-based workflow software to agent-executed work, while governed data substrates remain durable.",
        "business_decision": "Use the scorecard to decide which workflow layers to replace, which vendor modules to renegotiate, and which systems of record to keep.",
        "validated_counts": df["Verdict"].value_counts().reindex(["REPLACE", "RENEGOTIATE", "KEEP"]).astype(int).to_dict(),
        "data_quality": {
            "rows": int(len(df)),
            "null_pct": (df.isna().mean() * 100).round(1).to_dict(),
            "duplicate_use_cases": int(df["Use case"].duplicated().sum()),
            "guardrail": "Curated evidence base; do not present as statistically sampled market proof.",
        },
        "storyboard": [
            "The SaaS value pool is moving from seats to executable work.",
            "Replacement happens at the workflow layer, not usually at the system-of-record layer.",
            "Data moat separates replace, renegotiate, and keep decisions.",
            "Use cases show where each motion applies.",
            "The client action is a portfolio diagnostic, not a blanket replacement campaign.",
        ],
    }
    (pack_dir / "executive_story_pack.json").write_text(json.dumps(pack, indent=2), encoding="utf-8")
    (pack_dir / "executive_story_pack.md").write_text(
        "# AI Analyst Executive Story Pack\n\n"
        f"## Thesis\n{pack['executive_thesis']}\n\n"
        f"## Business Decision\n{pack['business_decision']}\n\n"
        "## Storyboard\n" + "\n".join(f"- {x}" for x in pack["storyboard"]) + "\n",
        encoding="utf-8",
    )


def use_case_rows(d: Deck, s, df: pd.DataFrame, x: float, y: float, w: float, max_rows=7):
    for _, r in df.head(max_rows).iterrows():
        d.rect(s, Inches(x), Inches(y + 0.02), Inches(0.12), Inches(0.28), VERDICT[r["Verdict"]])
        if w < 6:
            d.text(s, r["Use case"], Inches(x + 0.25), Inches(y), Inches(w - 0.35), Inches(0.22), size=8.8, color=d.b.NAVY, bold=True, shrink=True)
        else:
            d.text(s, r["Use case"], Inches(x + 0.25), Inches(y), Inches(w * 0.50), Inches(0.22), size=9.2, color=d.b.NAVY, bold=True, shrink=True)
            d.text(s, f"{r['Agent type']} · {r['Moat']} moat · {r['Verdict'].title()}", Inches(x + w * 0.58), Inches(y), Inches(w * 0.38), Inches(0.22), size=8.0, color=d.b.MUTED, shrink=True)
        y += 0.42


def build_deck(df: pd.DataFrame, charts: dict[str, Path]) -> Deck:
    total = 37
    d = Deck(brand=BRAND, footer="Agent Replacement Scorecard · executive story reviewed draft")
    p = 1
    b = d.b

    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(10.65), 0, Inches(2.68), d.H, b.NAVY_2)
    d.rect(s, Inches(10.65), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "EXECUTIVE STORY DECK", d.M, Inches(0.75), Inches(6.5), Inches(0.3), size=13, color=b.TEAL, bold=True)
    d.text(s, "Agent Replacement Scorecard", d.M, Inches(1.32), Inches(9.2), Inches(1.35), size=38, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "Where AI agents create replacement pressure, renewal leverage, and durable SaaS moats", d.M, Inches(3.05), Inches(8.7), Inches(0.8), size=20, color=b.LIGHT_TEAL, shrink=True)
    d.text(s, "Reviewed client-ready draft | Built from scorecard evidence + executive storyline", d.M, Inches(6.3), Inches(7.4), Inches(0.3), size=10.5, color=b.MUTED)
    footer(d, s, p, total, dark=True); p += 1

    s = header(d, p, total, "The plot: AI agents shift value from SaaS seats to executable work", "The business question is not which app dies; it is which workflow layer loses pricing power")
    card(d, s, .8, 1.85, 3.6, 2.1, "Old SaaS model", "Value captured through seats, add-ons, workflow modules, and scripted human-in-the-loop tasks.", b.CORAL)
    card(d, s, 4.85, 1.85, 3.6, 2.1, "Agentic work model", "Value shifts to agents that execute work across tools, data, and approvals.", b.TEAL)
    card(d, s, 8.9, 1.85, 3.0, 2.1, "Executive decision", "Replace the exposed layer. Renegotiate the module. Keep the governed substrate.", b.GOLD)
    d.rect(s, Inches(.85), Inches(5.25), Inches(10.9), Inches(.65), b.NAVY, radius=.1)
    d.text(s, "Decision framework for software portfolio action, not a CSV report.", Inches(1.15), Inches(5.47), Inches(10.3), Inches(.2), size=12, color=b.WHITE, bold=True, shrink=True)
    p += 1

    s = header(d, p, total, "Executive summary: the scorecard creates three commercial motions", "Each motion has a different owner, risk profile, and buying conversation")
    s.shapes.add_picture(str(charts["verdict"]), Inches(.85), Inches(1.68), width=Inches(5.2))
    card(d, s, 6.55, 1.75, 4.85, .82, "Replace", "Target workflow layers where seats, add-ons, or runbooks are the exposed value pool.", VERDICT["REPLACE"])
    card(d, s, 6.55, 2.9, 4.85, .82, "Renegotiate", "Use agents as renewal leverage where the core platform survives but modules compress.", VERDICT["RENEGOTIATE"])
    card(d, s, 6.55, 4.05, 4.85, .82, "Keep", "Protect systems where governed data, telemetry, permissions, and audit are the moat.", VERDICT["KEEP"])
    p += 1

    s = header(d, p, total, "What executives should take away", "The scorecard changes the discussion from AI enthusiasm to portfolio action")
    for i, (title, body, color) in enumerate([
        ("CFO", "Find spend categories where agent execution challenges seat and module pricing.", b.GOLD),
        ("CIO", "Protect systems of record while exposing workflow layers to agent pilots.", b.TEAL),
        ("COO", "Use volume and determinism to prioritize automation programs.", b.ACCENT),
        ("CMO / CRO", "Publish AEO pages that answer buyer questions with scored evidence.", b.CORAL),
    ]):
        card(d, s, .8 + (i % 2) * 5.65, 1.8 + (i // 2) * 1.65, 5.05, 1.15, title, body, color)
    p += 1

    s = header(d, p, total, "The answer is a portfolio diagnostic, not a replacement manifesto", "Blanket claims are weak; workflow-level classification is useful")
    d.text(s, bullet([
        "The exposed object is usually a workflow layer: support interaction, extraction, drafting, runbook execution, or guided selling.",
        "The durable object is usually a governed substrate: records, identity, permissions, telemetry, audit, regulated data, or proprietary corpus.",
        "The scorecard is valuable because it tells a client which conversation to have with each vendor.",
    ], 14), Inches(.95), Inches(1.9), Inches(10.5), Inches(2.0), shrink=True)
    p += 1

    section(d, p, total, "01", "Decision Frame", "The deck starts with the business architecture of the problem, then uses the data to prove the frame."); p += 1

    s = header(d, p, total, "Agents attack workflows before they attack systems", "This is why category-level SaaS replacement claims sound naive to executives")
    card(d, s, .85, 1.8, 3.3, 2.4, "Workflow layer", "Human interaction, task execution, drafting, summarization, triage, routing, extraction, or recommendation.", b.CORAL)
    card(d, s, 4.75, 1.8, 3.3, 2.4, "Control layer", "Approvals, policies, escalations, human accountability, and audit gates.", b.GOLD)
    card(d, s, 8.65, 1.8, 3.3, 2.4, "Substrate layer", "System of record, proprietary data, permissions, telemetry, and compliance record.", b.TEAL)
    d.text(s, "Client implication: replacement pressure is highest when SaaS monetizes workflow without owning the substrate.", Inches(.9), Inches(5.35), Inches(10.7), Inches(.4), size=12.2, color=b.NAVY, bold=True, shrink=True)
    p += 1

    s = header(d, p, total, "The scorecard answers four executive questions", "These are the questions a client can actually act on")
    for i, q in enumerate([
        "Which workflows should we pilot for agent replacement?",
        "Which SaaS modules should we renegotiate at renewal?",
        "Which systems should we protect as durable substrates?",
        "Which buyer questions should we publish for AEO and demand capture?",
    ]):
        d.rect(s, Inches(.9), Inches(1.85 + i * .85), Inches(.42), Inches(.42), b.NAVY, radius=.08)
        d.text(s, str(i + 1), Inches(1.03), Inches(1.96 + i * .85), Inches(.16), Inches(.14), size=9, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, q, Inches(1.55), Inches(1.9 + i * .85), Inches(9.9), Inches(.28), size=15, color=b.INK, bold=True, shrink=True)
    p += 1

    s = header(d, p, total, "The commercial motion depends on data moat", "Moat is the bridge between technical feasibility and business action")
    s.shapes.add_picture(str(charts["moat"]), Inches(.95), Inches(1.65), width=Inches(5.2))
    card(d, s, 6.65, 1.85, 4.7, .85, "Low moat → Replace", "Workflow can be recreated without a proprietary substrate.", VERDICT["REPLACE"])
    card(d, s, 6.65, 3.0, 4.7, .85, "Medium moat → Renegotiate", "Platform survives, workflow modules and seats compress.", VERDICT["RENEGOTIATE"])
    card(d, s, 6.65, 4.15, 4.7, .85, "High moat → Keep", "Governed data and control-plane value remain durable.", VERDICT["KEEP"])
    p += 1

    s = header(d, p, total, "Volume and determinism decide where to start", "Moat tells you the motion; volume and repeatability tell you the urgency")
    card(d, s, .85, 1.85, 3.35, 1.7, "High volume", "Creates enough economic pressure to matter in a renewal, operating plan, or automation business case.", b.GOLD)
    card(d, s, 4.8, 1.85, 3.35, 1.7, "High determinism", "Makes the workflow easier to test, replay, constrain, and measure.", b.TEAL)
    card(d, s, 8.75, 1.85, 3.05, 1.7, "Low moat", "Turns feasibility into replacement leverage.", b.CORAL)
    d.text(s, "Priority rule: start with high-volume, deterministic workflows where the vendor is monetizing an exposed workflow layer.", Inches(.9), Inches(4.85), Inches(10.8), Inches(.45), size=14, color=b.NAVY, bold=True, shrink=True)
    p += 1

    section(d, p, total, "02", "Use-Case Evidence", "The use cases are not a catalogue for its own sake; they show where the commercial motions appear."); p += 1

    for domain in ["Customer", "Employee", "Creative", "Code", "Data", "Security"]:
        rows = df[df["Agent type"] == domain]
        s = header(d, p, total, f"{domain} workflows show a different replacement pattern", "Domain-level evidence before the final story")
        for i, verdict in enumerate(["REPLACE", "RENEGOTIATE", "KEEP"]):
            val = int((rows["Verdict"] == verdict).sum())
            kpi(d, s, .85 + i * 2.35, 1.75, val, verdict.lower(), color=VERDICT[verdict])
        use_case_rows(d, s, rows.sort_values("Exposure score", ascending=False), .95, 3.35, 10.4, 6)
        implication = {
            "Customer": "Best starting point for replacement pilots because volume, visibility, and seat compression are easy to explain.",
            "Employee": "Mostly a productivity and renewal story: keep core systems, pressure assist layers.",
            "Creative": "Separate production throughput from brand/IP governance.",
            "Code": "Treat as engineering leverage, not wholesale SDLC replacement.",
            "Data": "Extraction can be replaced; governed analytics substrates usually survive.",
            "Security": "Telemetry and audit defend the platform; runbooks are more exposed.",
        }[domain]
        d.rect(s, Inches(.9), Inches(6.15), Inches(10.8), Inches(.46), b.SOFT, line=b.GRID, radius=.08)
        d.text(s, f"Executive implication: {implication}", Inches(1.1), Inches(6.3), Inches(10.3), Inches(.16), size=10.2, color=b.NAVY, bold=True, shrink=True)
        p += 1

    s = header(d, p, total, "Replace candidates share one economic pattern", "The exposed value pool is not the database; it is the workflow labor or seat layer")
    use_case_rows(d, s, df[df["Verdict"] == "REPLACE"].sort_values("Exposure score", ascending=False), .95, 1.9, 10.6, 10)
    p += 1

    s = header(d, p, total, "Renegotiate candidates are where executives can act fastest", "The vendor remains important, but pricing and packaging become vulnerable")
    use_case_rows(d, s, df[df["Verdict"] == "RENEGOTIATE"].sort_values("Exposure score", ascending=False), .95, 1.9, 10.6, 9)
    p += 1

    s = header(d, p, total, "Keep candidates create credibility", "A serious deck must explain what survives, not only what breaks")
    use_case_rows(d, s, df[df["Verdict"] == "KEEP"].sort_values("Exposure score", ascending=False), .95, 1.9, 10.6, 6)
    p += 1

    section(d, p, total, "03", "Executive Storyline", "Now that the frame and evidence are established, the storyline becomes sharper and less primitive."); p += 1

    s = header(d, p, total, "The market shift is from software access to work execution", "Seat-based SaaS is exposed when a buyer no longer needs a human in every workflow seat")
    d.text(s, bullet([
        "SaaS monetized access: users logged into tools to move work forward.",
        "Agents monetize execution: work moves through tools with fewer human seats.",
        "The durable value shifts toward systems that hold governed context and control.",
    ], 15), Inches(.95), Inches(1.9), Inches(10.8), Inches(2.0), shrink=True)
    p += 1

    s = header(d, p, total, "The strategic risk is misclassifying the layer", "Replacing a workflow layer is smart; replacing a governed substrate is usually reckless")
    card(d, s, .85, 1.9, 5.1, 2.2, "Bad executive read", "Declare a category dead, ignore governance, and overpromise displacement.", b.CORAL)
    card(d, s, 6.55, 1.9, 5.1, 2.2, "Good executive read", "Separate task execution from control systems, then pick the right commercial motion.", b.TEAL)
    p += 1

    s = header(d, p, total, "The client conversation changes by function", "The same scorecard creates different questions for different executives")
    for i, (role, ask, color) in enumerate([
        ("CFO", "Where can we challenge seat/module spend?", b.GOLD),
        ("CIO", "Which substrates must stay governed?", b.TEAL),
        ("COO", "Which workflows are ready for parallel-run pilots?", b.ACCENT),
        ("CRO/CMO", "Which buyer questions should our AEO pages answer?", b.CORAL),
    ]):
        card(d, s, .85 + (i % 2) * 5.65, 1.8 + (i // 2) * 1.55, 5.05, 1.05, role, ask, color)
    p += 1

    s = header(d, p, total, "The scorecard becomes a workshop, not a slide artifact", "The client value is in applying the frame to their actual software estate")
    d.text(s, bullet([
        "Inventory workflows and attached vendors.",
        "Score volume, determinism, and data moat.",
        "Assign replace / renegotiate / keep by workflow layer.",
        "Translate the result into pilots, renewal asks, and AEO content.",
    ], 15), Inches(.95), Inches(1.9), Inches(10.2), Inches(2.2), shrink=True)
    p += 1

    section(d, p, total, "04", "Commercial Motions", "The executive output is not insight; it is a set of decisions, owners, and next actions."); p += 1

    for verdict, title, body, owner in [
        ("REPLACE", "Replace the exposed workflow layer", "Pilot agent execution where the workflow is high-volume, repeatable, and weakly defended by proprietary data.", "COO + CIO + function owner"),
        ("RENEGOTIATE", "Renegotiate the module or seat bundle", "Keep the platform, but use agent capability to challenge assist modules, add-ons, and per-seat economics.", "CFO + procurement + CIO"),
        ("KEEP", "Keep the governed substrate", "Protect systems where value resides in permissions, audit, telemetry, records, and regulatory control.", "CIO + risk + data owner"),
    ]:
        s = header(d, p, total, title, f"Primary owner: {owner}")
        d.rect(s, Inches(.9), Inches(1.9), Inches(2.45), Inches(.58), VERDICT[verdict], radius=.12)
        d.text(s, verdict, Inches(1.08), Inches(2.08), Inches(2.05), Inches(.18), size=12, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, body, Inches(.95), Inches(2.9), Inches(5.2), Inches(1.2), size=15, color=b.INK, bold=True, shrink=True)
        use_case_rows(d, s, df[df["Verdict"] == verdict].sort_values("Exposure score", ascending=False), 6.7, 1.9, 4.8, 5)
        p += 1

    s = header(d, p, total, "The 30-day action plan", "Move from thesis to client operating artifact")
    steps = [
        ("Week 1", "Map the client software estate to workflows."),
        ("Week 2", "Score volume, determinism, and data moat with stakeholders."),
        ("Week 3", "Build the replace / renegotiate / keep portfolio view."),
        ("Week 4", "Pick pilots, renewal asks, and AEO pages."),
    ]
    for i, (wk, txt) in enumerate(steps):
        card(d, s, .85 + i * 2.85, 1.9, 2.45, 2.25, wk, txt, b.TEAL if i % 2 == 0 else b.GOLD)
    p += 1

    s = header(d, p, total, "Decision ask", "Approve the scorecard as a client-facing diagnostic, not a static research deck")
    d.text(s, bullet([
        "Use the deck to open executive conversations about SaaS spend, agent pilots, and renewal leverage.",
        "Use the scorecard workshop to generate client-specific replacement and renegotiation actions.",
        "Use the AEO plan to publish buyer-facing answers grounded in the model.",
    ], 15), Inches(.95), Inches(1.9), Inches(10.4), Inches(1.8), shrink=True)
    d.rect(s, Inches(.95), Inches(5.25), Inches(10.7), Inches(.65), b.NAVY, radius=.1)
    d.text(s, "Approve v3 for client use after proof-source URL tieout.", Inches(1.25), Inches(5.47), Inches(10), Inches(.2), size=13, color=b.WHITE, bold=True, shrink=True)
    p += 1

    section(d, p, total, "05", "Appendix", "Method, guardrails, and use-case detail for reviewers."); p += 1

    s = header(d, p, total, "Method guardrails", "What this deck can and cannot claim")
    card(d, s, .85, 1.85, 5.1, 2.4, "Supported", "Curated scorecard; directional exposure logic; use-case-backed commercial motions; workshop diagnostic.", b.TEAL)
    card(d, s, 6.55, 1.85, 5.1, 2.4, "Not yet supported", "Statistical market sizing; universal SaaS replacement forecast; guaranteed savings; source-verified proof URLs for every row.", b.CORAL)
    p += 1

    for label, subset in [
        ("Appendix: replacement use cases", df[df["Verdict"] == "REPLACE"]),
        ("Appendix: renegotiation use cases", df[df["Verdict"] == "RENEGOTIATE"]),
        ("Appendix: keep use cases", df[df["Verdict"] == "KEEP"]),
    ]:
        s = header(d, p, total, label, "Detailed roster for reviewers")
        use_case_rows(d, s, subset.sort_values("Exposure score", ascending=False), .95, 1.85, 10.8, 10)
        p += 1

    s = header(d, p, total, "Reproducibility", "Artifacts generated alongside this deck")
    d.text(s, bullet([
        f"Input scorecard: {DATA_PATH}",
        f"AI Analyst pack: {OUT_DIR / 'ai_analyst_pack_v3'}",
        f"Deck builder: {RUN_DIR / 'build_executive_story_deck_v3.py'}",
        f"Output deck: {OUTPUT}",
    ], 11.5), Inches(.95), Inches(1.9), Inches(10.8), Inches(1.7), shrink=True)
    p += 1

    if p - 1 != total:
        raise RuntimeError(f"built {p-1} slides, expected {total}")
    return d


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    write_strategy_pack(df)
    charts = make_charts(df)
    deck = build_deck(df, charts)
    deck.save(OUTPUT)
    df.to_csv(OUT_DIR / "scorecard_scored_executive_story_v3.csv", index=False)
    print(f"Repo output: {OUTPUT}")
    print(f"Desktop target: {DESKTOP}")


if __name__ == "__main__":
    main()
