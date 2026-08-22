#!/usr/bin/env python3
"""Emit the L01-L16 layout library as a /design canvas.

Every number here is the Client-Ready PPTX Design System's own, converted once
at the stage scale: the spec is written in POINTS, a canvas artboard is CSS
PIXELS, and a 1280x720 artboard stands for a 13.333x7.5in slide -- so
px = pt / 0.75. Authoring at stage size is the whole point: what the artboard
declares is what derive_template_profile.py --canvas reads back.

Run:  python3 build_canvas.py
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "canvas"

FRAME_W, FRAME_H = 1280, 720
PAD = 48          # 0.500in safe margin
GAP = 16          # 0.167in gutter
RADIUS = 8        # 0.083in card radius
COLUMNS = 12

# Design-system palette (client-ready-pptx-design-system.md, "Color")
MIDNIGHT, SLATE, WHITE = "#0A1628", "#1E293B", "#FFFFFF"
CYAN, TEAL, PALE = "#00B4D8", "#0A9396", "#8DB4D4"
GREEN, MUTED = "#12855B", "#6B7280"
SURFACE, COOL, LINE = "#F8FAFC", "#F4F8FE", "#E2E8F0"

# Type ramp, pt -> px at the stage scale
HEAD, BODY = "Georgia", "Aptos"          # the spec's named fallbacks, applied deliberately
COVER_PX = 64     # 48pt  (spec 40-54pt)
TITLE_PX = 40     # 30pt  (spec 24-30pt)
KPI_PX = 48       # 36pt  (spec 28-40pt)
CARD_PX = 20      # 15pt  (spec 12-16pt)
BODY_PX = 18      # 13.5pt (spec 12-14pt)
LABEL_PX = 13     # 9.75pt (spec 9-11pt)
KICK_PX = 13      # 9.75pt (spec 8-10pt)
FOOT_PX = 10      # 7.5pt  (spec 7-8pt)

STYLE = f"""
  .root {{ width: {FRAME_W}px; height: {FRAME_H}px; padding: {PAD}px;
           box-sizing: border-box; background: {WHITE}; color: {SLATE};
           font-family: "{BODY}", Arial, sans-serif; }}
  .dark {{ background: {MIDNIGHT}; color: {WHITE}; }}
  .kicker {{ font-family: "{BODY}", Arial, sans-serif; font-size: {KICK_PX}px;
             letter-spacing: 1.4px; text-transform: uppercase; color: {CYAN}; }}
  .title {{ font-family: "{HEAD}", Cambria, serif; font-size: {TITLE_PX}px;
            color: {SLATE}; line-height: 1.15; margin: 10px 0 0 0; }}
  .dark .title {{ color: {WHITE}; }}
  .cover {{ font-family: "{HEAD}", Cambria, serif; font-size: {COVER_PX}px;
            color: {WHITE}; line-height: 1.08; }}
  .rule {{ height: 2px; width: 120px; background: {CYAN}; margin: 14px 0 22px 0; }}
  .grid {{ display: grid; grid-template-columns: repeat({COLUMNS}, 1fr); gap: {GAP}px; }}
  .card {{ border-radius: {RADIUS}px; background: {SURFACE};
           border: 1px solid {LINE}; padding: 18px; }}
  .panel {{ border-radius: {RADIUS}px; background: {COOL};
            border: 1px solid {LINE}; padding: 18px; }}
  .slab {{ border-radius: {RADIUS}px; background: {MIDNIGHT}; color: {WHITE}; padding: 22px; }}
  .ch {{ font-family: "{BODY}", Arial, sans-serif; font-size: {CARD_PX}px; font-weight: 600; }}
  .body {{ font-family: "{BODY}", Arial, sans-serif; font-size: {BODY_PX}px; color: {SLATE}; }}
  .dark .body {{ color: {PALE}; }}
  .kpi {{ font-family: "{HEAD}", Cambria, serif; font-size: {KPI_PX}px; color: {CYAN}; }}
  .label {{ font-family: "{BODY}", Arial, sans-serif; font-size: {LABEL_PX}px; color: {MUTED}; }}
  .foot {{ font-family: "{BODY}", Arial, sans-serif; font-size: {FOOT_PX}px; color: {MUTED}; }}
  .node {{ border-radius: {RADIUS}px; background: {TEAL}; color: {WHITE}; padding: 14px; }}
  .ok {{ color: {GREEN}; }}
"""


def artboard(kicker: str, title: str, body: str, *, dark: bool = False, cover: str = "") -> str:
    head = f'<div class="cover">{cover}</div>' if cover else (
        f'<div class="kicker">{kicker}</div>'
        f'<div class="title">{title}</div><div class="rule"></div>'
    )
    return (
        "<!doctype html>\n<html><head><style>" + STYLE + "</style></head><body>\n"
        f'<div class="root{" dark" if dark else ""}">\n{head}\n{body}\n'
        f'<div class="foot">Client-Ready PPTX Design System &middot; layout reference</div>\n'
        "</div></body></html>\n"
    )


def span(n: int) -> str:
    return f'style="grid-column: span {n}"'


def cards(n: int, heads: list[str], notes: list[str]) -> str:
    width = COLUMNS // n
    cells = "".join(
        f'<div class="card" {span(width)}><div class="ch">{heads[i]}</div>'
        f'<div class="body">{notes[i]}</div></div>'
        for i in range(n)
    )
    return f'<div class="grid">{cells}</div>'


def kpis(items: list[tuple[str, str]]) -> str:
    width = COLUMNS // len(items)
    cells = "".join(
        f'<div class="card" {span(width)}><div class="kpi">{value}</div>'
        f'<div class="label">{label}</div></div>'
        for value, label in items
    )
    return f'<div class="grid">{cells}</div>'


LAYOUTS: list[tuple[str, str, str, str, dict]] = [
    ("Cover", "L01", "", "",
     f'<div class="body" style="margin-top:26px">Engagement &middot; audience &middot; date</div>',
     {"dark": True, "cover": "Cover states the promise,<br>not the topic"}),
    ("Executive-Summary", "L02", "EXECUTIVE THESIS", "One thesis, four numbers that carry it",
     f'<div class="grid"><div class="slab" {span(6)}><div class="ch">The thesis</div>'
     f'<div class="body">55/45 split: dark headline panel left, KPI grid right.</div></div>'
     f'<div {span(6)}>' + kpis([("41%", "MARGIN"), ("2.4x", "PIPELINE")]) +
     '<div style="height:16px"></div>' + kpis([("18mo", "PAYBACK"), ("7", "MARKETS")]) +
     "</div></div>", {}),
    ("Three-Card-Argument", "L03", "POSITIONING", "Three evidence cards under one sentence",
     cards(3, ["Where we win", "What it costs", "What must be true"],
           ["Evidence card one.", "Evidence card two.", "Evidence card three."]), {}),
    ("L04-Process-Chain", "L04", "PROCESS CHAIN", "Four nodes, one outcome endpoint",
     '<div class="grid">' + "".join(
         f'<div class="node" {span(2)}><div class="ch">{n}</div></div>'
         for n in ["Intake", "Enrich", "Decide", "Act"]
     ) + f'<div class="slab" {span(4)}><div class="ch">Outcome</div>'
     f'<div class="body">One endpoint, annotated below.</div></div></div>', {}),
    ("L05-Pillars", "L05", "REASONS", "Four equal pillars, numbered",
     cards(4, ["01 Speed", "02 Cost", "03 Risk", "04 Reach"],
           ["Proof.", "Proof.", "Proof.", "Proof."]), {}),
    ("Big-Number", "L06", "OPPORTUNITY", "Metric tiles on top, assumptions below",
     kpis([("$4.2M", "ADDRESSABLE"), ("31%", "ATTACH"), ("9wk", "TIME TO VALUE")]) +
     '<div style="height:16px"></div>' +
     cards(2, ["Assumption", "Sensitivity"], ["Stated, not implied.", "Named driver."]), {}),
    ("Operating-Model", "L07", "SOLUTION ARCHITECTURE", "Hero diagram left, capability layers right",
     f'<div class="grid"><div class="panel" {span(7)}><div class="ch">System view</div>'
     f'<div class="body">Hero visual or diagram sits here.</div></div><div {span(5)}>' +
     "".join(
         f'<div class="card" style="margin-bottom:12px"><div class="ch">{c}</div></div>'
         for c in ["Experience", "Orchestration", "Data"]
     ) + "</div></div>", {}),
    ("L08-Deep-Dive", "L08", "TECHNICAL DEEP DIVE", "Centered diagram on midnight, cyan annotations",
     f'<div class="panel" style="background:#12243A;border-color:#1E293B">'
     f'<div class="ch" style="color:{WHITE}">Centered system diagram</div>'
     f'<div class="body">Cyan dimensions and annotations.</div></div>', {"dark": True}),
    ("Decision-Scorecard", "L09", "OPTIONS", "Six columns, one recommended",
     cards(6, ["A", "B", "C", "D", "E", "F"], ["-", "-", "-", "Pick", "-", "-"]), {}),
    ("Comparison", "L10", "COMPETITIVE VIEW", "One clear win, one honest limitation",
     cards(3, ["We win", "We tie", "We lose"],
           ["Named criterion.", "Named criterion.", "Stated plainly."]), {}),
    ("Roadmap", "L11", "ROADMAP", "Phases across, evidence and risk below",
     '<div class="grid">' + "".join(
         f'<div class="node" {span(3)}><div class="ch">{p}</div></div>'
         for p in ["Sprint", "Scale", "Sustain", "Transfer"]
     ) + "</div><div style='height:16px'></div>" +
     cards(2, ["Evidence", "Risk"], ["Gate per phase.", "Owner named."]), {}),
    ("L12-Financial-Evidence", "L12", "PERFORMANCE", "Table plus three aligned callouts",
     kpis([("+14pt", "GROSS MARGIN"), ("$1.1M", "RUN RATE"), ("0.7x", "CAC PAYBACK")]) +
     '<div style="height:16px"></div>' +
     f'<div class="panel"><div class="body">Units, timeframe, and actual/target/forecast '
     f'stated on the table itself.</div></div>', {}),
    ("L13-Cost-Clarity", "L13", "COST CLARITY", "Three large numbers, one implication",
     kpis([("$180k", "BUILD"), ("$26k/yr", "RUN"), ("$310k", "AVOIDED")]) +
     '<div style="height:16px"></div>' +
     f'<div class="slab"><div class="ch">Bottom line</div>'
     f'<div class="body">The implication, not the arithmetic.</div></div>', {}),
    ("Recommendation-Ask", "L14", "THE ASK", "Midnight ask left, resourcing right",
     f'<div class="grid"><div class="slab" {span(5)}><div class="ch">Approve phase one</div>'
     f'<div class="body">One decision, one owner, one date.</div></div>'
     f'<div class="panel" {span(7)}><div class="ch">Use of resources</div>'
     f'<div class="body">Owners and milestones.</div></div></div>', {}),
    ("L15-Governance", "L15", "GOVERNANCE", "Leaders above, capability grid below",
     cards(3, ["Sponsor", "Delivery lead", "Architect"],
           ["Role evidence.", "Role evidence.", "Role evidence."]) +
     "<div style='height:16px'></div>" +
     cards(4, ["Security", "Data", "Change", "Ops"], ["-", "-", "-", "-"]), {}),
    ("Risk-Mitigation", "L16", "CLOSE", "One line, evidence thumbnails",
     cards(4, ["Proof", "Proof", "Proof", "Proof"], ["Caption.", "Caption.", "Caption.", "Caption."]),
     {"dark": True}),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    for index, (name, lid, kicker, title, body, opts) in enumerate(LAYOUTS):
        filename = f"{name}.dc.html"
        html = artboard(f"{lid} &middot; {kicker}" if kicker else "", title, body, **opts)
        (OUT / filename).write_text(html, encoding="utf-8")
        entries.append(
            {
                "file": filename,
                "x": (index % 4) * (FRAME_W + 120),
                "y": (index // 4) * (FRAME_H + 160),
                "w": FRAME_W,
                "h": FRAME_H,
                "title": f"{lid} {name.replace('-', ' ')}",
            }
        )

    # Main is the representative BODY slide (L03), never the cover: the cover
    # headline is 64px and would set title_pt for the whole deck.
    main_html = (OUT / "Three-Card-Argument.dc.html").read_text(encoding="utf-8")
    (OUT / "Main.dc.html").write_text(main_html, encoding="utf-8")
    entries.append(
        {"file": "Main.dc.html", "x": 0, "y": -(FRAME_H + 200), "w": FRAME_W, "h": FRAME_H,
         "title": "Main (reference artboard = L03)"}
    )

    (OUT / "canvas.json").write_text(
        json.dumps({"artboards": entries, "launch": {"view": "canvas"}}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(entries)} artboards + canvas.json to {OUT}")


if __name__ == "__main__":
    main()
