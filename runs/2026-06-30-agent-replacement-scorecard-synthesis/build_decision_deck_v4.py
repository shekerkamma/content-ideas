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
CHART_DIR = OUT_DIR / "decision_deck_v4_charts"
DATA_PATH = Path("/mnt/c/Users/sheke/OneDrive/Desktop/Agent-Replacement-Scorecard.csv")
OUTPUT = OUT_DIR / "Agent-Replacement-Scorecard-Decision-Deck-Reviewed-v4.pptx"
DESKTOP = Path("/mnt/c/Users/sheke/OneDrive/Desktop/Agent-Replacement-Scorecard-Decision-Deck-Reviewed-v4.pptx")


def rgb(h: str) -> RGBColor:
    return hx(h)


BRAND = Brand(
    NAVY=rgb("08111F"),
    NAVY_2=rgb("111C2E"),
    TEAL=rgb("2DD4BF"),
    ACCENT=rgb("0891B2"),
    DARK_TEAL=rgb("0F766E"),
    LIGHT_TEAL=rgb("DFFDF7"),
    GOLD=rgb("F59E0B"),
    AMBER=rgb("F59E0B"),
    CORAL=rgb("E11D48"),
    SOFT=rgb("F8FAFC"),
    INK=rgb("111827"),
    MUTED=rgb("64748B"),
    GRID=rgb("CBD5E1"),
    FONT="Aptos",
    FONT_H="Aptos Display",
    HX_TEAL="#2DD4BF",
    HX_TEALD="#0F766E",
    HX_NAVY="#08111F",
    HX_INK="#111827",
    HX_MUTED="#64748B",
    HX_GRID="#CBD5E1",
    HX_GOLD="#F59E0B",
)

COLORS = {"REPLACE": rgb("E11D48"), "RENEGOTIATE": rgb("F59E0B"), "KEEP": rgb("10B981")}
HEX = {"REPLACE": "#E11D48", "RENEGOTIATE": "#F59E0B", "KEEP": "#10B981"}
SCORE = {"L": 1, "M": 2, "H": 3}


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["volume_score"] = df["Volume"].map(SCORE)
    df["determinism_score"] = df["Determinism"].map(SCORE)
    df["moat_exposure"] = df["Data moat"].map({"L": 3, "M": 2, "H": 1})
    df["exposure_score"] = df["volume_score"] + df["determinism_score"] + df["moat_exposure"]
    df["moat_label"] = df["Data moat"].map({"L": "Low moat", "M": "Medium moat", "H": "High moat"})
    return df


def bullets(items, size=13, color=None):
    return [{"text": x, "bullet": True, "space_before": 7 if i else 0, "size": size, "color": color or BRAND.INK} for i, x in enumerate(items)]


def footer(d: Deck, s, page: int, total: int, dark=False):
    d.footer(s, page, total, dark=dark)


def title_slide(d: Deck, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(9.85), 0, Inches(3.48), d.H, b.NAVY_2)
    d.rect(s, Inches(9.85), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "DECISION DECK", d.M, Inches(0.7), Inches(4), Inches(0.28), size=13, color=b.TEAL, bold=True)
    d.text(s, "Approve a 30-Day Agent Replacement Diagnostic", d.M, Inches(1.28), Inches(8.65), Inches(1.25), size=35, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "A client-ready recommendation for finding replace, renegotiate, and keep actions across SaaS workflows", d.M, Inches(3.05), Inches(8.2), Inches(0.82), size=16.2, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, d.M, Inches(4.35), Inches(1.55), Inches(0.06), b.TEAL)
    d.text(s, "Built from the Agent Replacement Scorecard evidence base · reviewed v4", d.M, Inches(6.2), Inches(7.2), Inches(0.26), size=10.5, color=b.MUTED)
    footer(d, s, page, total, dark=True)


def section(d: Deck, page: int, total: int, label: str, title: str, subtitle: str):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, label, Inches(0.75), Inches(0.85), Inches(2.4), Inches(0.28), size=13, color=b.TEAL, bold=True)
    d.text(s, title, Inches(0.75), Inches(1.45), Inches(10.6), Inches(1.1), size=34, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.75), Inches(2.9), Inches(1.45), Inches(0.06), b.TEAL)
    d.text(s, subtitle, Inches(0.75), Inches(3.3), Inches(8.8), Inches(0.78), size=16, color=b.LIGHT_TEAL, shrink=True)
    footer(d, s, page, total, dark=True)


def slide(d: Deck, page: int, total: int, title: str, subtitle: str = ""):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
    d.text(s, title, d.M, Inches(0.34), d.CW, Inches(0.9), size=22, color=b.NAVY, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, d.M, Inches(1.15), Inches(1.45), Inches(0.05), b.TEAL)
    if subtitle:
        d.text(s, subtitle, d.M, Inches(1.32), d.CW, Inches(0.34), size=12.5, color=b.MUTED, shrink=True)
    footer(d, s, page, total)
    return s


def card(d: Deck, s, x, y, w, h, title, body, color=None, fill=None, dark=False):
    b = d.b
    color = color or b.TEAL
    fill = fill or (b.NAVY if dark else b.WHITE)
    text_color = b.WHITE if dark else b.INK
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), fill, line=None if dark else b.GRID, radius=0.08, shadow=not dark)
    d.rect(s, Inches(x), Inches(y), Inches(0.08), Inches(h), color)
    d.text(s, title, Inches(x + 0.22), Inches(y + 0.15), Inches(w - 0.35), Inches(0.28), size=10.8, color=color if dark else b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(x + 0.22), Inches(y + 0.55), Inches(w - 0.35), Inches(h - 0.68), size=8.8, color=text_color, shrink=True)


def kpi(d: Deck, s, x, y, value, label, note="", color=None):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(2.2), Inches(1.05), b.NAVY, radius=0.1, shadow=True)
    d.text(s, str(value), Inches(x + 0.18), Inches(y + 0.13), Inches(1.85), Inches(0.36), size=21, color=color or b.TEAL, bold=True, shrink=True)
    d.text(s, label, Inches(x + 0.18), Inches(y + 0.58), Inches(1.85), Inches(0.22), size=9.3, color=b.WHITE, bold=True, shrink=True)
    if note:
        d.text(s, note, Inches(x + 0.18), Inches(y + 0.84), Inches(1.85), Inches(0.18), size=7.5, color=b.LIGHT_TEAL, shrink=True)


def make_charts(df: pd.DataFrame) -> dict[str, Path]:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = {}
    counts = df["Verdict"].value_counts().reindex(["REPLACE", "RENEGOTIATE", "KEEP"])
    fig, ax = plt.subplots(figsize=(7.8, 3.9), dpi=200)
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    ax.barh(counts.index[::-1], counts.values[::-1], color=[HEX[v] for v in counts.index[::-1]])
    ax.set_xlim(0, 12); ax.set_xticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.tick_params(axis="y", labelsize=11, length=0)
    for y, v in enumerate(counts.values[::-1]):
        ax.text(v + 0.25, y, str(int(v)), va="center", fontsize=16, fontweight="bold", color=BRAND.HX_NAVY)
    out["verdict"] = CHART_DIR / "verdict.png"
    fig.savefig(out["verdict"], transparent=True, bbox_inches="tight"); plt.close(fig)

    moat = pd.crosstab(df["Data moat"], df["Verdict"]).reindex(["L", "M", "H"]).reindex(columns=["REPLACE", "RENEGOTIATE", "KEEP"], fill_value=0)
    fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=200)
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    ax.imshow(moat.values, cmap="YlGnBu")
    ax.set_xticks(range(3), ["Replace", "Renegotiate", "Keep"], fontsize=10)
    ax.set_yticks(range(3), ["Low moat", "Medium moat", "High moat"], fontsize=10)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, int(moat.iloc[i, j]), ha="center", va="center", fontsize=18, fontweight="bold", color=BRAND.HX_NAVY)
    for sp in ax.spines.values(): sp.set_visible(False)
    out["moat"] = CHART_DIR / "moat.png"
    fig.savefig(out["moat"], transparent=True, bbox_inches="tight"); plt.close(fig)
    return out


def row_list(d: Deck, s, df: pd.DataFrame, x: float, y: float, w: float, n: int = 6):
    for _, r in df.head(n).iterrows():
        d.rect(s, Inches(x), Inches(y + 0.02), Inches(0.1), Inches(0.26), COLORS[r["Verdict"]])
        d.text(s, r["Use case"], Inches(x + 0.22), Inches(y), Inches(w * 0.55), Inches(0.2), size=8.9, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, f"{r['Agent type']} · {r['moat_label']}", Inches(x + w * 0.62), Inches(y), Inches(w * 0.34), Inches(0.2), size=7.8, color=d.b.MUTED, shrink=True)
        y += 0.38


def write_pack(df: pd.DataFrame):
    pack_dir = OUT_DIR / "decision_pack_v4"
    pack_dir.mkdir(parents=True, exist_ok=True)
    pack = {
        "recommendation": "Approve a 30-day AI agent software-portfolio diagnostic.",
        "decision_required": "Use the scorecard as a client-facing workshop operating model.",
        "options": ["Wait for vendors", "Run isolated pilots", "Run portfolio diagnostic"],
        "recommended_option": "Run portfolio diagnostic",
        "evidence_counts": df["Verdict"].value_counts().reindex(["REPLACE", "RENEGOTIATE", "KEEP"]).astype(int).to_dict(),
        "guardrail": "Curated scorecard; source URL tieout required before external final.",
    }
    (pack_dir / "decision_pack.json").write_text(json.dumps(pack, indent=2), encoding="utf-8")


def build(df: pd.DataFrame, charts: dict[str, Path]) -> Deck:
    total = 25
    d = Deck(brand=BRAND, footer="Agent Replacement Scorecard · decision deck reviewed v4")
    p = 1
    b = d.b
    title_slide(d, p, total); p += 1

    s = slide(d, p, total, "Recommendation: approve a 30-day AI agent software-portfolio diagnostic", "The decision is whether to turn a broad AI-agent thesis into a client-specific portfolio action plan")
    d.text(s, "Approve the diagnostic.", Inches(0.85), Inches(1.85), Inches(7.6), Inches(0.5), size=28, color=b.NAVY, bold=True, shrink=True)
    d.text(s, bullets([
        "Classify workflows into replace, renegotiate, and keep actions.",
        "Tie AI-agent potential to SaaS spend, renewal leverage, and governance risk.",
        "Use the scorecard as the workshop operating model, not as a generic research deck.",
    ], 14), Inches(0.95), Inches(2.65), Inches(7.3), Inches(1.55), shrink=True)
    card(d, s, 8.75, 1.85, 3.1, 2.55, "Decision ask", "Approve v4 as a diagnostic sales narrative, subject to proof-source URL tieout before external final.", b.GOLD)
    p += 1

    s = slide(d, p, total, "The executive problem is not 'will AI replace SaaS?'", "The real problem is deciding which workflow spend is exposed before the next renewal cycle")
    card(d, s, .85, 1.8, 3.25, 2.35, "Bad framing", "A category-level prediction: agents replace SaaS.", b.CORAL)
    card(d, s, 4.8, 1.8, 3.25, 2.35, "Better framing", "A workflow-level diagnosis: some layers are exposed; some are defensible.", b.TEAL)
    card(d, s, 8.75, 1.8, 3.25, 2.35, "Best framing", "A portfolio decision: replace, renegotiate, or keep by workflow layer.", b.GOLD)
    d.rect(s, Inches(.9), Inches(5.25), Inches(10.9), Inches(.55), b.NAVY, radius=.08)
    d.text(s, "The deck must sell a decision process, not explain a framework.", Inches(1.15), Inches(5.43), Inches(10.4), Inches(.18), size=12.2, color=b.WHITE, bold=True, shrink=True)
    p += 1

    s = slide(d, p, total, "The answer is a three-motion operating model", "Each motion has a different owner, evidence bar, and executive conversation")
    s.shapes.add_picture(str(charts["verdict"]), Inches(.85), Inches(1.75), width=Inches(5.0))
    card(d, s, 6.55, 1.75, 4.75, .85, "Replace", "Run agent pilots against exposed workflow layers.", COLORS["REPLACE"])
    card(d, s, 6.55, 2.9, 4.75, .85, "Renegotiate", "Challenge modules, add-ons, and seat pricing.", COLORS["RENEGOTIATE"])
    card(d, s, 6.55, 4.05, 4.75, .85, "Keep", "Protect governed systems of record and data moats.", COLORS["KEEP"])
    p += 1

    s = slide(d, p, total, "The diagnostic creates four executive outputs", "This is what the client gets after 30 days")
    outputs = [
        ("Workflow inventory", "Named workflows, vendors, seats/modules, renewal timing."),
        ("Moat scorecard", "Volume, determinism, data moat, and verdict by workflow."),
        ("Action portfolio", "Replace pilots, renegotiation targets, protected systems."),
        ("Roadmap", "Owners, tests, data needs, and 30/60/90-day actions."),
    ]
    for i, (t, body) in enumerate(outputs):
        card(d, s, .85 + (i % 2) * 5.65, 1.8 + (i // 2) * 1.55, 5.05, 1.05, t, body, b.TEAL if i % 2 == 0 else b.GOLD)
    p += 1

    section(d, p, total, "01", "Decision Logic", "The deck should make the decision logic obvious before showing the evidence."); p += 1

    s = slide(d, p, total, "Data moat is the decision boundary", "Moat turns AI feasibility into a commercial action")
    s.shapes.add_picture(str(charts["moat"]), Inches(.9), Inches(1.72), width=Inches(5.15))
    card(d, s, 6.55, 1.8, 4.8, .82, "Low moat", "Replace: agent can recreate the workflow.", COLORS["REPLACE"])
    card(d, s, 6.55, 2.95, 4.8, .82, "Medium moat", "Renegotiate: platform stays, workflow module compresses.", COLORS["RENEGOTIATE"])
    card(d, s, 6.55, 4.1, 4.8, .82, "High moat", "Keep: governed data and control-plane value remain durable.", COLORS["KEEP"])
    p += 1

    s = slide(d, p, total, "Volume and determinism determine sequencing", "The first wave should be economically meaningful and operationally testable")
    card(d, s, .85, 1.85, 3.25, 1.8, "High volume", "Enough spend or work volume to matter to CFO and COO stakeholders.", b.GOLD)
    card(d, s, 4.85, 1.85, 3.25, 1.8, "High determinism", "Repeatable enough for replay, parallel run, QA, and measurement.", b.TEAL)
    card(d, s, 8.85, 1.85, 3.0, 1.8, "Low moat", "Weak enough substrate protection to create replacement leverage.", b.CORAL)
    d.text(s, "Priority rule: start with high-volume, repeatable, weakly defended workflows.", Inches(.95), Inches(5.1), Inches(10.4), Inches(.4), size=12.2, color=b.NAVY, bold=True, shrink=True)
    p += 1

    s = slide(d, p, total, "The scorecard is a workshop instrument", "Executives should not be asked to admire the model; they should use it to make decisions")
    d.text(s, bullets([
        "Map the workflow layer, control layer, and substrate layer.",
        "Score the workflow with business stakeholders, not only AI experts.",
        "Assign the action: replace, renegotiate, or keep.",
        "Translate the action into a pilot, renewal ask, or governance protection.",
    ], 14.5), Inches(.95), Inches(1.9), Inches(10.5), Inches(2.1), shrink=True)
    p += 1

    section(d, p, total, "02", "Options", "A consulting deck must show what was rejected, not only what is recommended."); p += 1

    s = slide(d, p, total, "Three options were considered; only one creates portfolio leverage", "The recommended option links AI capability to renewal economics and operating risk")
    options = [
        ("1. Wait for vendors", "Low effort, but vendors keep control of pricing and packaging.", "Reject", b.CORAL),
        ("2. Run isolated pilots", "Fast learning, but pilots stay disconnected from SaaS spend.", "Partial", b.GOLD),
        ("3. Portfolio diagnostic", "Connects AI, spend, renewal, risk, and operating action.", "Recommend", b.TEAL),
    ]
    for i, (t, body, verdict, color) in enumerate(options):
        card(d, s, .85 + i * 3.9, 1.85, 3.35, 2.55, t, body, color)
        d.rect(s, Inches(1.2 + i * 3.9), Inches(4.75), Inches(2.6), Inches(.42), color, radius=.08)
        d.text(s, verdict, Inches(1.43 + i * 3.9), Inches(4.88), Inches(2.1), Inches(.14), size=9.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    p += 1

    s = slide(d, p, total, "Why isolated pilots are not enough", "Pilots prove feasibility; they do not automatically create renewal leverage")
    card(d, s, .85, 1.85, 5.1, 2.15, "Pilot-only failure mode", "The team demos an agent, but cannot connect it to module spend, vendor pricing, workflow volume, or risk controls.", b.CORAL)
    card(d, s, 6.55, 1.85, 5.1, 2.15, "Diagnostic-led advantage", "The team targets pilots where the commercial motion is already clear: replace, renegotiate, or keep.", b.TEAL)
    p += 1

    section(d, p, total, "03", "Evidence Base", "The scorecard supports the decision; it should not dominate the story."); p += 1

    s = slide(d, p, total, "The current evidence base is enough for a diagnostic offer", "It is not enough for a market-wide replacement forecast")
    for i, (value, label, note, color) in enumerate([
        (25, "scored use cases", "cross-domain examples", b.TEAL),
        (10, "replace candidates", "exposed workflow layers", COLORS["REPLACE"]),
        (9, "renegotiate cases", "module / seat leverage", COLORS["RENEGOTIATE"]),
        (6, "keep cases", "governed substrates", COLORS["KEEP"]),
    ]):
        kpi(d, s, .85 + i * 2.55, 1.85, value, label, note, color)
    d.text(s, bullets([
        "Use as directional consulting evidence.",
        "Add source URLs before external final distribution.",
        "Do not present as statistical market proof.",
    ], 12.5), Inches(.95), Inches(3.75), Inches(10.4), Inches(1.25), shrink=True)
    p += 1

    for verdict, title, subtitle in [
        ("REPLACE", "Replace targets are exposed workflow layers", "The value pool is labor, seats, add-ons, or runbooks."),
        ("RENEGOTIATE", "Renegotiation targets are the fastest executive win", "The platform matters, but modules and seats become vulnerable."),
        ("KEEP", "Keep targets prevent overreach", "Governed data and audit create durable control-plane value."),
    ]:
        s = slide(d, p, total, title, subtitle)
        subset = df[df["Verdict"] == verdict].sort_values("exposure_score", ascending=False)
        row_list(d, s, subset, .95, 1.9, 10.6, 7 if verdict != "KEEP" else 6)
        d.rect(s, Inches(.95), Inches(5.6), Inches(10.7), Inches(.45), BRAND.SOFT, line=BRAND.GRID, radius=.06)
        d.text(s, f"Commercial motion: {verdict.title()} is an action, not a category label.", Inches(1.15), Inches(5.74), Inches(10.2), Inches(.14), size=10.3, color=b.NAVY, bold=True, shrink=True)
        p += 1

    section(d, p, total, "04", "Action Plan", "The recommendation needs owners, timeline, and success metrics."); p += 1

    s = slide(d, p, total, "30-day diagnostic plan", "The work converts a thesis into a client-specific action portfolio")
    plan = [
        ("Week 1", "Inventory workflows, vendors, modules, seats, renewal dates."),
        ("Week 2", "Score volume, determinism, data moat with stakeholders."),
        ("Week 3", "Build replace / renegotiate / keep portfolio view."),
        ("Week 4", "Select pilots, renewal asks, protected systems, and AEO pages."),
    ]
    for i, (wk, body) in enumerate(plan):
        card(d, s, .85 + i * 2.9, 1.85, 2.45, 2.35, wk, body, b.TEAL if i % 2 == 0 else b.GOLD)
    p += 1

    s = slide(d, p, total, "Owners and success metrics", "A decision deck must define who does what after approval")
    rows = [
        ("CFO / procurement", "Renewal leverage list", "Modules/seats challenged"),
        ("CIO / architecture", "System-of-record protection", "Governed systems preserved"),
        ("COO / function leads", "Pilot backlog", "Workflows moved to test"),
        ("Marketing / AEO", "Buyer-answer pages", "Pages shipped and cited"),
    ]
    y = 1.85
    for owner, output, metric in rows:
        card(d, s, .85, y, 3.2, .72, owner, output, b.TEAL)
        d.text(s, metric, Inches(4.55), Inches(y + .24), Inches(6.5), Inches(.18), size=11.2, color=b.NAVY, bold=True, shrink=True)
        y += .88
    p += 1

    s = slide(d, p, total, "Risks and mitigations", "The recommendation is credible only if the weak points are named")
    risks = [
        ("Evidence is curated", "Position as diagnostic; add source URL tieout."),
        ("Spend data unavailable", "Use workshop to collect modules, seats, and renewals."),
        ("Over-replacement risk", "Make keep and renegotiate first-class outcomes."),
        ("Vendor pushback", "Use workflow-level evidence, not category claims."),
    ]
    for i, (risk, mit) in enumerate(risks):
        card(d, s, .85 + (i % 2) * 5.65, 1.85 + (i // 2) * 1.45, 5.05, .95, risk, mit, b.CORAL if i % 2 == 0 else b.GOLD)
    p += 1

    s = slide(d, p, total, "Decision required now", "Approve the diagnostic, then harden the evidence before external final")
    d.text(s, "Approve the 30-day diagnostic.", Inches(.95), Inches(1.8), Inches(10.6), Inches(.55), size=22, color=b.NAVY, bold=True, shrink=True)
    d.text(s, bullets([
        "Use the deck to sell the problem and recommendation.",
        "Use the workshop to produce client-specific actions.",
        "Use proof-source tieout to move from reviewed draft to external final.",
    ], 14), Inches(1.0), Inches(2.75), Inches(10.4), Inches(1.55), shrink=True)
    d.rect(s, Inches(.95), Inches(5.3), Inches(10.8), Inches(.6), b.NAVY, radius=.08)
    d.text(s, "Next gate: source-tied proof pack + client-specific spend fields.", Inches(1.2), Inches(5.5), Inches(10.2), Inches(.18), size=12.2, color=b.WHITE, bold=True, shrink=True)
    p += 1

    section(d, p, total, "05", "Appendix", "Keep the method available without making it the executive story."); p += 1

    s = slide(d, p, total, "Method guardrails", "What this deck can and cannot claim")
    card(d, s, .85, 1.85, 5.1, 2.25, "Supported", "Curated scorecard; workflow-level diagnostic; replace / renegotiate / keep operating model.", b.TEAL)
    card(d, s, 6.55, 1.85, 5.1, 2.25, "Not yet supported", "Statistical market sizing; guaranteed savings; universal category replacement; source-verified proof for every named example.", b.CORAL)
    p += 1

    s = slide(d, p, total, "Reproducibility", "Artifacts generated with the deck")
    d.text(s, bullets([
        f"Decision memo: {OUT_DIR / 'decision_memo_v4.md'}",
        f"Input scorecard: {DATA_PATH}",
        f"Decision pack: {OUT_DIR / 'decision_pack_v4'}",
        f"Builder: {RUN_DIR / 'build_decision_deck_v4.py'}",
    ], 10.8), Inches(.95), Inches(1.85), Inches(10.8), Inches(1.6), shrink=True)
    p += 1

    if p - 1 != total:
        raise RuntimeError(f"built {p - 1}, expected {total}")
    return d


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    write_pack(df)
    charts = make_charts(df)
    deck = build(df, charts)
    deck.save(OUTPUT)
    df.to_csv(OUT_DIR / "scorecard_scored_decision_v4.csv", index=False)
    print(f"Repo output: {OUTPUT}")
    print(f"Desktop target: {DESKTOP}")


if __name__ == "__main__":
    main()
