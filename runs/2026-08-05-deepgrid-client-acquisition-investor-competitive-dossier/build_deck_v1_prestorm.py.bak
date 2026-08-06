#!/usr/bin/env python3
"""Build the DeepGrid client-acquisition strategy deck.

Charts are NATIVE python-pptx charts (editable in PowerPoint, Excel-backed) —
matplotlib is not installed on this host, and native charts are the better
artifact anyway.

Kept in the run folder so QA fixes stay reproducible (CLAUDE.md PPTX gate #8).
"""
import sys
from pathlib import Path

KIT = Path("/home/sheke/content-ideas/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(KIT))

from pptx.util import Inches, Pt, Emu                      # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR            # noqa: E402
from pptx.chart.data import CategoryChartData              # noqa: E402
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION  # noqa: E402
from pptxkit import Deck, Brand, hx                        # noqa: E402

OUT = Path(__file__).resolve().parent
d = Deck(footer="DeepGrid Semi — client acquisition strategy · July-corrected basis · 5 Aug 2026")
b = d.b
YRS = ["FY27", "FY28", "FY29", "FY30", "FY31", "FY32"]
TOTAL = 22
_page = {"n": 0}


def notes(s, txt):
    s.notes_slide.notes_text_frame.text = txt.strip()


def page(s, dark=False):
    _page["n"] += 1
    d.footer(s, _page["n"], TOTAL, dark=dark)


def style_chart(gf, *, colors, legend=True, num_fmt='0.0"%"', font=9,
                gap=60, smooth=False, markers=False):
    ch = gf.chart
    ch.font.size = Pt(font)
    ch.font.name = b.FONT
    ch.has_title = False
    if legend:
        ch.has_legend = True
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(font)
    else:
        ch.has_legend = False
    for i, ser in enumerate(ch.series):
        col = colors[i % len(colors)]
        if ch.chart_type in (XL_CHART_TYPE.LINE, XL_CHART_TYPE.LINE_MARKERS):
            ser.format.line.color.rgb = col
            ser.format.line.width = Pt(2.5)
            ser.smooth = smooth
        else:
            ser.format.fill.solid()
            ser.format.fill.fore_color.rgb = col
    try:
        ch.value_axis.has_major_gridlines = True
        ch.value_axis.major_gridlines.format.line.color.rgb = b.GRID
        ch.value_axis.major_gridlines.format.line.width = Pt(0.5)
        ch.value_axis.tick_labels.number_format = num_fmt
        ch.value_axis.tick_labels.number_format_is_linked = False
        ch.value_axis.tick_labels.font.size = Pt(font)
        ch.value_axis.format.line.fill.background()
        ch.category_axis.tick_labels.font.size = Pt(font)
        ch.category_axis.format.line.color.rgb = b.GRID
    except Exception:
        pass
    try:
        ch.plots[0].gap_width = gap
    except Exception:
        pass
    return ch


def add_chart(s, kind, cats, series, left, top, w, h, **kw):
    cd = CategoryChartData()
    cd.categories = cats
    for name, vals in series:
        cd.add_series(name, vals)
    gf = s.shapes.add_chart(kind, left, top, w, h, cd)
    return style_chart(gf, **kw)


def table(s, headers, rows, left, top, width, *, col_w, row_h=Inches(0.34),
          head_fill=None, highlight=None, size=11.5, left_cols=(0,)):
    """Lightweight grid from rects + text. highlight: set of row indices.
    left_cols: column indices rendered left-aligned — use for prose cells,
    since centring a long sentence in a table cell is hard to scan."""
    head_fill = head_fill or b.NAVY
    x = left
    d.rect(s, left, top, width, row_h, head_fill)
    for i, htxt in enumerate(headers):
        d.text(s, htxt, x + Inches(0.10), top + Inches(0.05), col_w[i] - Inches(0.16),
               row_h - Inches(0.08), size=size, color=b.WHITE, bold=True, shrink=True,
               align=PP_ALIGN.LEFT if i == 0 else PP_ALIGN.CENTER)
        x += col_w[i]
    y = top + row_h
    for r, row in enumerate(rows):
        hl = highlight and r in highlight
        d.rect(s, left, y, width, row_h,
               hx("FFF4D6") if hl else (b.SOFT if r % 2 == 0 else b.WHITE))
        if hl:
            d.rect(s, left, y, Inches(0.055), row_h, b.GOLD)
        x = left
        for i, cell in enumerate(row):
            d.text(s, str(cell), x + Inches(0.10), y + Inches(0.05), col_w[i] - Inches(0.16),
                   row_h - Inches(0.08), size=size, color=b.INK,
                   bold=bool(hl and i == 0), shrink=True,
                   align=PP_ALIGN.LEFT if i in left_cols else PP_ALIGN.CENTER)
            x += col_w[i]
        y += row_h
    return y


def cards(s, items, top, *, cols=3, height=Inches(1.6), gap=Inches(0.22), size=11.5):
    cw = (d.CW - gap * (cols - 1)) / cols
    for i, (title, body) in enumerate(items):
        r, c = divmod(i, cols)
        x = d.M + c * (cw + gap)
        y = top + r * (height + gap)
        d.rect(s, x, y, cw, height, b.WHITE, line=b.GRID, radius=0.06, shadow=True)
        d.rect(s, x, y, cw, Inches(0.05), b.TEAL)
        d.text(s, title, x + Inches(0.18), y + Inches(0.20), cw - Inches(0.36),
               Inches(0.46), size=13, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.18), y + Inches(0.70), cw - Inches(0.36),
               height - Inches(0.86), size=size, color=b.MUTED, shrink=True)


def kpi(s, items, top, *, height=Inches(1.5)):
    n = len(items)
    gap = Inches(0.22)
    cw = (d.CW - gap * (n - 1)) / n
    for i, (num, label, note, col) in enumerate(items):
        x = d.M + i * (cw + gap)
        d.rect(s, x, top, cw, height, b.NAVY, radius=0.05)
        d.text(s, num, x + Inches(0.16), top + Inches(0.16), cw - Inches(0.32), Inches(0.62),
               size=32, color=col, bold=True, font=b.FONT_H, shrink=True)
        d.text(s, label, x + Inches(0.16), top + Inches(0.80), cw - Inches(0.32), Inches(0.30),
               size=11.5, color=b.WHITE, bold=True, shrink=True)
        d.text(s, note, x + Inches(0.16), top + Inches(1.10), cw - Inches(0.32), Inches(0.32),
               size=9.5, color=b.LIGHT_TEAL, shrink=True)


def kpi_at(s, items, left, top, width, *, height=Inches(1.4), gap=Inches(0.18)):
    """KPI row confined to an explicit box — use whenever a chart shares the slide,
    so the cards cannot be laid over the plot area."""
    n = len(items)
    cw = (width - gap * (n - 1)) / n
    for i, (num, label, note, col) in enumerate(items):
        x = left + i * (cw + gap)
        d.rect(s, x, top, cw, height, b.NAVY, radius=0.05)
        d.text(s, num, x + Inches(0.15), top + Inches(0.14), cw - Inches(0.30), Inches(0.56),
               size=27, color=col, bold=True, font=b.FONT_H, shrink=True)
        d.text(s, label, x + Inches(0.15), top + Inches(0.73), cw - Inches(0.30), Inches(0.28),
               size=11, color=b.WHITE, bold=True, shrink=True)
        d.text(s, note, x + Inches(0.15), top + Inches(1.01), cw - Inches(0.30), Inches(0.28),
               size=9.5, color=b.LIGHT_TEAL, shrink=True)


def divider(s, num, title, subtitle):
    d.rect(s, 0, 0, d.W, d.H, b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"SECTION {num}", Inches(0.85), Inches(2.6), Inches(6), Inches(0.4),
           size=14, color=b.TEAL, bold=True)
    d.text(s, title, Inches(0.85), Inches(3.05), Inches(11), Inches(1.0),
           size=42, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, Inches(0.85), Inches(4.15), Inches(1.6), Inches(0.05), b.TEAL)
    d.text(s, subtitle, Inches(0.85), Inches(4.42), Inches(10.5), Inches(0.6),
           size=15, color=b.LIGHT_TEAL, shrink=True)


def badge(s, txt, left, top, fill, *, w=Inches(1.5), fg=None):
    d.rect(s, left, top, w, Inches(0.30), fill, radius=0.3)
    d.text(s, txt, left, top + Inches(0.045), w, Inches(0.24), size=9.5,
           color=fg or b.WHITE, bold=True, align=PP_ALIGN.CENTER)




ASSET = Path(__file__).resolve().parent / "assets"


def photo(s, name, left, top, width, height):
    """Place a harvested product photo, cropped to fill the box."""
    from PIL import Image
    src = ASSET / "product" / f"{name}.png"
    if not src.exists():
        d.rect(s, left, top, width, height, b.SOFT, line=b.GRID)
        return
    tgt = ASSET / "fitted" / f"{name}_{int(width)}x{int(height)}.png"
    tgt.parent.mkdir(parents=True, exist_ok=True)
    if not tgt.exists():
        im = Image.open(src).convert("RGB")
        want = width / height
        have = im.width / im.height
        if have > want:
            nw = int(im.height * want)
            im = im.crop(((im.width - nw) // 2, 0, (im.width + nw) // 2, im.height))
        else:
            nh = int(im.width / want)
            im = im.crop((0, (im.height - nh) // 2, im.width, (im.height + nh) // 2))
        im.save(tgt)
    s.shapes.add_picture(str(tgt), left, top, width, height)
# ── COVER ───────────────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)
bg = ASSET / "harvested" / "deck_image1.png"
if bg.exists():
    s.shapes.add_picture(str(bg), 0, 0, d.W, d.H)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.text(s, "CLIENT ACQUISITION STRATEGY", Inches(0.85), Inches(1.85), Inches(8.4), Inches(0.4),
       size=14, color=b.TEAL, bold=True)
d.text(s, "Who to sell to, what to say,\nand what never to say",
       Inches(0.85), Inches(2.35), Inches(8.2), Inches(1.6),
       size=40, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.rect(s, Inches(0.85), Inches(4.15), Inches(1.6), Inches(0.05), b.TEAL)
d.text(s, "DeepGrid Semi · commercial lead briefing · built on the July-corrected basis",
       Inches(0.85), Inches(4.45), Inches(8.4), Inches(0.5), size=15,
       color=b.LIGHT_TEAL, shrink=True)
for i, chip in enumerate(["Oct 2026 is the real deadline", "2 tracks", "5 banned claims",
                          "whitespace closing"]):
    x = Inches(0.85) + i * Inches(2.6)
    d.rect(s, x, Inches(5.35), Inches(2.45), Inches(0.44), b.NAVY_2, radius=0.25, line=b.ACCENT)
    d.text(s, chip, x, Inches(5.47), Inches(2.45), Inches(0.26), size=10,
           color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER)
page(s, dark=True)
notes(s, """
This deck answers a commercial question, not an investor one: which clients to pursue, in what
order, with which words.
It stands on the July Pre-Series A corrected basis and enforces that deck's banned-claims list
throughout. Where a market fact is new, it was verified independently this week and is
sourced on the slide.
""")

# ── EXECUTIVE SUMMARY ───────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Sell Track A now on proof you already hold; validate Track B against a clock",
         "Executive summary — the commercial answer")
d.rect(s, d.M, Inches(1.78), d.CW, Inches(0.95), b.NAVY, radius=0.04)
d.text(s, "BLUF", d.M + Inches(0.22), Inches(1.92), Inches(1.0), Inches(0.3),
       size=11, color=b.TEAL, bold=True)
d.text(s, "The mandate wave that matters commercially is October 2026 — existing production "
          "models — not the April date the decks lead with. And the low-BOM vertically-"
          "integrated whitespace is closing about 18 months earlier than assumed. Both push "
          "the same conclusion: sell what is provable now, and put a date on what is not.",
       d.M + Inches(1.35), Inches(1.88), d.CW - Inches(1.6), Inches(0.76),
       size=13, color=b.WHITE, shrink=True)
cards(s, [
    ("Track A — sell now",
     "Sovereign defence, border surveillance and port AGV. On-die HSM, Indian-designed, "
     "shipping on FPGA today. Backed by a live GeM record and ₹23.01L delivered — the only "
     "line needing neither the certificate nor the tapeout."),
    ("Track B — validate, don't promise",
     "3PL and dedicated fleet retrofit against the Oct 2026 deadline. Positioning is marked "
     "PENDING VALIDATION in your own deck. Twenty buyer interviews, one paid pilot, 90 days "
     "— or the statement is retracted."),
    ("The clock that changed",
     "Netrasemi went production-ready in May 2026 with three OEM trials, on ₹107 Cr. Your "
     "July map placed them in 2027. The head-start is shorter than the 30-month runway "
     "assumes."),
], Inches(2.92), cols=3, height=Inches(2.15))
d.rect(s, d.M, Inches(5.32), d.CW, Inches(0.62), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(5.32), Inches(0.06), Inches(0.62), b.GOLD)
d.text(s, "Discipline rule from the July deck, unchanged: the retrofit-price line never appears "
          "in a defence conversation, and the sovereign-data line never appears in a fleet one.",
       d.M + Inches(0.25), Inches(5.46), d.CW - Inches(0.5), Inches(0.4),
       size=12.5, color=b.INK, bold=True, shrink=True)
page(s)
notes(s, """
Lead with the two moves and the reason they are different.
Track A is sellable today because its proof already exists — defence revenue, a GeM record,
and silicon running on FPGA. It needs neither AIS certification nor the tapeout.
Track B is the bigger market and the weaker position. Your own deck marks the statement
pending validation with a 90-day kill criterion. Honour that.
The third card is the new information in this deck and the reason not to sequence leisurely.
""")

# ── DIVIDER 01 ──────────────────────────────────────────────────────────────
s = d.slide()
divider(s, "01", "The demand clock", "When the buyer is actually forced to act")
page(s, dark=True)
notes(s, "First movement — the timing that drives urgency in every conversation.")

# ── MANDATE PHASING ─────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "October 2026 is the deadline that creates buyers — not April",
         "GSR 184(E) is phased; the decks lead with the wrong date")
rows = [
    ["March 2025", "GSR 184(E) notified", "AIS-162/184/186/187/188 for M2, M3, N2, N3", "Done"],
    ["April 2026", "New models must comply", "Applies to newly introduced models only", "Passed"],
    ["October 2026", "Existing production models", "The volume wave — every model in production", "2 months"],
    ["2027 – Jan 2028", "Further systems phase in", "Additional ADAS functions layered on", "Runway"],
]
table(s, ["When", "What", "Scope", "Status"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(2.0), Inches(3.2), Inches(5.4), Inches(1.53)], highlight={2},
      row_h=Inches(0.50), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(4.45), Inches(6.4), Inches(1.75), b.NAVY, radius=0.04)
d.text(s, "Why this changes the pitch", d.M + Inches(0.22), Inches(4.63), Inches(5.9),
       Inches(0.32), size=14, color=b.TEAL, bold=True)
d.text(s, "April 2026 only bound new model introductions — a small population. October 2026 "
          "binds everything already in production. That is when fleet and OEM buyers are "
          "actually forced to move, and it is eight weeks away.",
       d.M + Inches(0.22), Inches(5.00), Inches(5.9), Inches(1.05), size=12,
       color=b.LIGHT_TEAL, shrink=True)
d.rect(s, Inches(7.25), Inches(4.45), Inches(5.48), Inches(1.75), hx("FDECEE"), radius=0.04)
d.rect(s, Inches(7.25), Inches(4.45), Inches(0.06), Inches(1.75), b.CORAL)
d.text(s, "The uncomfortable corollary", Inches(7.48), Inches(4.63), Inches(5.0), Inches(0.32),
       size=14, color=b.NAVY, bold=True)
d.text(s, "AIS certification is a path, not held. If the October wave lands before "
          "certification does, the buyer who is forced to act cannot buy from DeepGrid — "
          "they buy the compliance box. Track A does not have this problem.",
       Inches(7.48), Inches(5.00), Inches(5.0), Inches(1.05), size=12,
       color=b.INK, shrink=True)
badge(s, "VERIFIED", d.M, Inches(6.38), b.ACCENT, w=Inches(1.3))
d.text(s, "Phasing confirmed independently, Aug 2026 · electraytech.com; novushitech.com",
       Inches(2.05), Inches(6.42), Inches(9), Inches(0.3), size=10, color=b.MUTED, italic=True)
page(s)
notes(s, """
This is the single most useful correction in the deck for a commercial lead.
Every DeepGrid document says the mandate is live since April 2026 and stops there. That is
true but commercially misleading: April bound only newly introduced models. October 2026
binds existing production models, which is the entire installed model range.
So the demand event is eight weeks out, not four months past. That changes outreach urgency
and it changes which buyer is feeling pressure right now.
The red panel is the risk that comes with it: urgency you cannot serve goes to a competitor.
If certification is not held by October, the forced buyer buys a ₹30,000 box. Say this
internally; do not say it to a customer.
""")

# ── WHAT WE SELL ────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "What you are selling: a certified system, not a chip",
         "One six-chiplet 28nm die underneath four product lines")
photo(s, "module-m2", d.M, Inches(1.86), Inches(3.0), Inches(1.9))
photo(s, "compute-box", Inches(3.78), Inches(1.86), Inches(3.0), Inches(1.9))
photo(s, "detection", Inches(6.96), Inches(1.86), Inches(3.0), Inches(1.9))
photo(s, "robots", Inches(10.14), Inches(1.86), Inches(2.59), Inches(1.9))
for i, (cap, sub) in enumerate([("DGrid Alpha module", "M.2 form factor"),
                                ("A100 compute box", "1ch / 2ch / 4ch"),
                                ("D-Drive perception", "transformer VLA, no HD maps"),
                                ("Phase-3 autonomy", "yards, ports, defence")]):
    x = [d.M, Inches(3.78), Inches(6.96), Inches(10.14)][i]
    w = Inches(3.0) if i < 3 else Inches(2.59)
    d.text(s, cap, x, Inches(3.84), w, Inches(0.26), size=11.5, color=b.NAVY, bold=True,
           align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, sub, x, Inches(4.10), w, Inches(0.24), size=10, color=b.MUTED,
           align=PP_ALIGN.CENTER, shrink=True)
rows = [
    ["AD0", "Smart mirror / 360", "₹0.50L", "Retrofit entry — the upgrade-ladder foot in the door"],
    ["AD2", "Full truck ADAS kit", "₹2.0–2.5L", "The mandate product — compute + software + sensors"],
    ["AD4", "Off-highway autonomy", "₹0.45–3.5 Cr", "Private land: yards, ports, defence — no FMVSS, no cert gate"],
]
table(s, ["Line", "Product", "Price", "What it is for commercially"], rows, d.M,
      Inches(4.50), d.CW, col_w=[Inches(0.9), Inches(3.0), Inches(1.9), Inches(6.33)],
      highlight={1}, row_h=Inches(0.50), left_cols=(0, 1, 3))
d.text(s, "TSMC 28nm HPC+ · 39.3 TOPS INT8 · 64 PCOREs · ~57.1 mm² die · 8.6 ms of a 33.3 ms "
          "frame budget (74% headroom)", d.M, Inches(6.62), d.CW, Inches(0.3), size=10.5,
       color=b.MUTED, italic=True, shrink=True)
page(s)
notes(s, """
Lead with the system, not the silicon. Buyers do not purchase a die — they purchase a
certified box that does a job, and the chip is why you can price it where you do.
The AD0 smart mirror is the underrated commercial asset. It is a cheap way into a fleet that
establishes the relationship and the data-rights clause, and the upgrade ladder reuses it at
every subsequent step.
AD4 off-highway deserves attention because it sidesteps the certification gate entirely —
private land, no homologation dependency. That is why it sits in Track A rather than Track B.
""")


# ── WHY OWNING THE SILICON MATTERS ──────────────────────────────────────────
s = d.slide()
d.header(s, "Why owning the silicon is the argument — in a buyer's language",
         "Four claims, each of which a competitor cannot simply match")
cards(s, [
    ("Cost — the one they feel",
     "₹2L kit against ₹6.5–15L imports, because the die is ~$30 of board BOM rather than a "
     "bought-in $6,000-class part. A merchant incumbent cannot shrink to that without "
     "cannibalising its own margin."),
    ("Capability — the one they test",
     "Heavy transformer VLA models run on-chip. A YOLO-class edge part cannot host them. "
     "This is the claim to lead with in a fleet room, because the ₹30,000 box has no answer."),
    ("India-fit — the one they believe",
     "Models and 12-bit radar trained on Indian road data — cattle, autos, unmarked lanes. A "
     "foreign chip vendor cannot reach that data, and every Indian fleet operator already "
     "knows why it matters."),
    ("Control — the one procurement asks",
     "Indigenous supply, no import dependence, on-die HSM. In government and defence "
     "procurement this stops being a feature and becomes an eligibility criterion."),
], Inches(1.90), cols=2, height=Inches(2.0))
d.rect(s, d.M, Inches(6.24), d.CW, Inches(0.62), b.NAVY, radius=0.04)
d.text(s, "Sequence matters: capability opens a fleet conversation, control opens a defence "
          "one, and cost closes both. Cost never opens.",
       d.M + Inches(0.25), Inches(6.38), d.CW - Inches(0.5), Inches(0.36),
       size=12.5, color=b.WHITE, bold=True, shrink=True)
page(s)
notes(s, """
These four are the positioning core, restated as things a buyer can act on rather than things
a founder finds interesting.
The instruction at the bottom is the one to internalise. Cost is your strongest fact and your
weakest opener — leading with it invites the compliance-box comparison in a fleet room and
signals commodity in a defence room.
Capability and control are the openers. Cost is what you close on once the buyer already
wants the capability.
""")


# ── DIVIDER 02 ──────────────────────────────────────────────────────────────
s = d.slide()
divider(s, "02", "Who to sell to", "Two tracks, two proof burdens, never the same room")
page(s, dark=True)
notes(s, "Second movement — the ICP and the positioning discipline.")

# ── ICP SEGMENTS ────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Six segments, five reachable — and only two worth this quarter",
         "Where the ₹2.3L price holds and where it does not")
rows = [
    ["Government / PSU / defence", "Foreign silicon excluded; GeM record already held",
     "Yes, at a premium", "TRACK A — now"],
    ["Plant and yard operators", "Own the land and the vehicles; become the Phase-3 customer",
     "Yes", "TRACK A — now"],
    ["Large organised fleets (50+)", "Real safety P&L, single decision-maker, can run a pilot",
     "Yes", "TRACK B — validate"],
    ["OEM / Tier-1 line-fit", "One relationship covers thousands of vehicles",
     "Yes — the volume engine", "Start now, closes late"],
    ["3PL and freight aggregators", "Aggregate small operators into one contract",
     "Partly — will negotiate hard", "Later"],
    ["Sub-five-truck owner-operators", "~3.5M operators, no purchasing process, hard price anchor",
     "No — needs channel and a cheaper SKU", "Not addressable"],
]
table(s, ["Segment", "Why it is addressable", "Does ₹2.3L hold?", "Priority"], rows,
      d.M, Inches(1.82), d.CW,
      col_w=[Inches(3.0), Inches(4.7), Inches(2.5), Inches(1.93)], highlight={0, 1},
      row_h=Inches(0.54), left_cols=(0, 1, 2, 3))
d.rect(s, d.M, Inches(5.72), d.CW, Inches(0.95), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(5.72), Inches(0.06), Inches(0.95), b.GOLD)
d.text(s, "The two highlighted rows need neither the certificate nor the tapeout",
       d.M + Inches(0.25), Inches(5.87), Inches(7), Inches(0.3), size=13,
       color=b.NAVY, bold=True)
d.text(s, "That is the whole reason they are this quarter's targets. Every other segment is "
          "gated on something DeepGrid does not yet hold, and selling into a gate you cannot "
          "open burns the relationship you will need later.",
       d.M + Inches(0.25), Inches(6.20), d.CW - Inches(0.5), Inches(0.42),
       size=12, color=b.INK, shrink=True)
page(s)
notes(s, """
Six segments, and the prioritisation is driven by one test: does this buyer require something
we do not yet have?
Government and yard operators do not. They can buy the FPGA product today, on indigenous
supply and private-land grounds respectively.
Everyone else is waiting on AIS certification, the tapeout, or an OEM relationship that does
not exist yet. Start those conversations — especially OEM, which has the longest cycle — but
do not forecast them as this quarter's revenue.
The bottom row is the honest exclusion: 3.5 million operators the plan explicitly cannot
reach directly.
""")


# ── BUYER COMMITTEE ─────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Who actually signs, and what each of them is afraid of",
         "Buyer committee by track — the fear is what you sell against")
d.text(s, "TRACK A · defence / PSU / yard", d.M, Inches(1.82), Inches(6.0), Inches(0.3),
       size=12.5, color=b.TEAL, bold=True)
table(s, ["Role", "What they fear"], [
    ["Programme / procurement officer", "Foreign dependency and audit exposure"],
    ["Security or data officer", "Exfiltration — answered physically by on-die HSM"],
    ["Operations lead", "A pilot that disrupts a working site"],
    ["Finance", "A capital line with no precedent to compare"],
], d.M, Inches(2.18), Inches(6.0), col_w=[Inches(2.7), Inches(3.3)], row_h=Inches(0.50),
    left_cols=(0, 1))
d.text(s, "TRACK B · 3PL / dedicated fleet", Inches(7.05), Inches(1.82), Inches(5.68),
       Inches(0.3), size=12.5, color=b.GOLD, bold=True)
table(s, ["Role", "What they fear"], [
    ["Fleet owner / promoter", "Spending ₹2.3L when ₹30k passes inspection"],
    ["Safety / compliance head", "Being non-compliant in October"],
    ["Finance / NBFC partner", "Capital outlay without a payback story"],
    ["Driver / union", "Surveillance framing of driver monitoring"],
], Inches(7.05), Inches(2.18), Inches(5.68), col_w=[Inches(2.6), Inches(3.08)],
    row_h=Inches(0.50), left_cols=(0, 1))
d.rect(s, d.M, Inches(4.85), d.CW, Inches(1.4), b.NAVY, radius=0.04)
d.text(s, "The two hardest people in the room", d.M + Inches(0.25), Inches(5.03), Inches(6),
       Inches(0.32), size=14, color=b.TEAL, bold=True)
d.text(s, "In Track A it is the security officer — and they are the easiest to win, because "
          "on-die HSM is a physical answer rather than a policy assurance. In Track B it is "
          "the driver and the union: driver monitoring reads as surveillance unless it is "
          "introduced as protection from false blame. Get that framing wrong once and the "
          "pilot dies on the shop floor rather than in the boardroom.",
       d.M + Inches(0.25), Inches(5.40), d.CW - Inches(0.5), Inches(0.75),
       size=12.5, color=b.LIGHT_TEAL, shrink=True)
page(s)
notes(s, """
Committees, not buyers. Every one of these people can stop a deal and only one of them can
start it.
The security officer in Track A is your ally once they understand the HSM argument, because
you are handing them a defensible answer to a question they are usually forced to fudge.
The driver and union point in Track B is the one most commonly missed. Driver-monitoring
systems get torn out or taped over when they arrive framed as surveillance. Introduced as
evidence that protects the driver from false blame in an accident, the same hardware is
welcomed. That framing decision happens once, early, and is hard to reverse.
""")


# ── TRACK A ─────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Track A — sovereign defence and off-highway: sell this now",
         "Primary track · the only line needing neither the certificate nor the tapeout")
d.rect(s, d.M, Inches(1.82), Inches(7.4), Inches(1.35), b.NAVY, radius=0.04)
d.text(s, "POSITIONING STATEMENT", d.M + Inches(0.25), Inches(1.98), Inches(4), Inches(0.28),
       size=10.5, color=b.TEAL, bold=True)
d.text(s, "“For sovereign UGV, border-surveillance and port-AGV programs where data cannot "
          "leave Indian soil, DGrid Alpha is the only Indian-designed combo-die whose on-die "
          "HSM makes data-exfil physically impossible — shipping today on FPGA, ASIC drop-in "
          "next.”",
       d.M + Inches(0.25), Inches(2.30), Inches(6.9), Inches(0.78), size=12.5,
       color=b.WHITE, italic=True, shrink=True)
photo(s, "truck", Inches(8.15), Inches(1.82), Inches(4.58), Inches(1.35))
cards(s, [
    ("Why it closes",
     "Data sovereignty is a procurement rule, not a preference. Foreign silicon is excluded "
     "from government fleets outright, so the comparison set is small and the on-die HSM is "
     "a physical answer rather than a policy promise."),
    ("What you can prove today",
     "₹23.01L delivered on a GeM Robot Training contract · a GeM record held · perception on "
     "FPGA at measured 40fps. Note the contract sits in Deepgrid Datacentre and its IP is "
     "MCEME-owned — it proves procurement access, not ADAS revenue."),
    ("Kill criterion — from your own deck",
     "Track drops from primary if Month 6 arrives without either a second signed contract, "
     "or audited confirmation of the ₹1 Cr revenue's commercial nature."),
], Inches(3.40), cols=3, height=Inches(2.4))
page(s)
notes(s, """
Track A is where the next contract most plausibly comes from, and the reason is structural
rather than promotional: procurement rules exclude foreign silicon from government fleets, so
DeepGrid is competing against a very short list.
The on-die HSM claim is the strongest thing in the whole positioning set because it is a
physical property, not a policy assurance. A buyer worried about exfiltration can be shown
why it cannot happen.
Note the kill criterion is already written and dated. One booked contract is traction; it is
not yet a repeatable motion, and the second contract is what proves it.
""")

# ── TRACK B ─────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Track B — fleet retrofit: run it as an experiment, not a promise",
         "Secondary track · your own deck marks this PENDING VALIDATION")
d.rect(s, d.M, Inches(1.82), Inches(7.4), Inches(1.35), b.NAVY_2, radius=0.04)
d.text(s, "POSITIONING STATEMENT · PENDING VALIDATION", d.M + Inches(0.25), Inches(1.98),
       Inches(5.5), Inches(0.28), size=10.5, color=b.GOLD, bold=True)
d.text(s, "“For N2/N3 fleet operators facing 2027–28 ADAS mandate deadlines, DGrid Alpha "
          "ships one retrofit kit that satisfies AEBS, LDW, DMS and BSD at roughly 1/3 the "
          "imported-stack price — pending first paid pilot.”",
       d.M + Inches(0.25), Inches(2.30), Inches(6.9), Inches(0.78), size=12.5,
       color=b.WHITE, italic=True, shrink=True)
photo(s, "compute-box", Inches(8.15), Inches(1.82), Inches(4.58), Inches(1.35))
cards(s, [
    ("Why it is not yet sellable as stated",
     "No paid pilot has closed. The price claim is real against imports and irrelevant "
     "against the ₹15–40k compliance box that satisfies the same inspector. Nothing in the "
     "documents shows a buyer who chose ₹2.3L over ₹30,000."),
    ("What makes it convert",
     "Not price. The buyer must want capability — which means the conversation is about "
     "what a compliance box cannot do: transformer perception, driver monitoring, and a "
     "certified latency budget on one part."),
    ("Kill criterion — from your own deck",
     "The statement is retracted from decks, site and sales collateral if the first 20 buyer "
     "interviews fail to produce one paid pilot in 90 days."),
], Inches(3.40), cols=3, height=Inches(2.4))
page(s)
notes(s, """
Be disciplined about this one, because it is the larger market and therefore the more
tempting story.
The price argument that works against a ₹6.5L import does nothing against a ₹30,000 box. Both
satisfy the inspector while enforcement is transitional. So leading with price in a fleet
conversation loses on the buyer's own terms.
The conversation that can win is capability — what the cheap box physically cannot do. That
reframes the comparison away from compliance cost and toward accident exposure, which is also
where the insurer motion eventually lives.
Twenty interviews, ninety days, one paid pilot. If it does not land, retract the statement
rather than softening it.
""")

# ── POSITIONING DISCIPLINE ──────────────────────────────────────────────────
s = d.slide()
d.header(s, "One story per buyer — the two tracks never meet",
         "Positioning discipline · carried unchanged from the July deck")
d.rect(s, d.M, Inches(1.90), Inches(6.15), Inches(2.5), b.NAVY, radius=0.04)
d.text(s, "IN A DEFENCE ROOM", d.M + Inches(0.25), Inches(2.10), Inches(5.6), Inches(0.3),
       size=12, color=b.TEAL, bold=True)
d.text(s, [
    {"text": "Say: data sovereignty, on-die HSM, Indian-designed, shipping on FPGA, GeM "
             "record, ₹1 Cr booked.", "size": 12, "color": b.WHITE},
    {"text": "Never say: the retrofit price line, the 1/3-of-imports comparison, fleet ROI, "
             "or anything about insurance.", "size": 12, "color": b.CORAL,
     "space_before": 12},
], d.M + Inches(0.25), Inches(2.50), Inches(5.6), Inches(1.75), shrink=True)
d.rect(s, Inches(7.05), Inches(1.90), Inches(5.68), Inches(2.5), b.NAVY_2, radius=0.04)
d.text(s, "IN A FLEET ROOM", Inches(7.30), Inches(2.10), Inches(5.1), Inches(0.3),
       size=12, color=b.GOLD, bold=True)
d.text(s, [
    {"text": "Say: mandate deadline, one kit covers AEBS/LDW/DMS/BSD, install time, "
             "capability the cheap box cannot match.", "size": 12, "color": b.WHITE},
    {"text": "Never say: sovereign data, HSM exfiltration, defence customers, or anything "
             "implying a government-only product.", "size": 12, "color": b.CORAL,
     "space_before": 12},
], Inches(7.30), Inches(2.50), Inches(5.1), Inches(1.75), shrink=True)
d.rect(s, d.M, Inches(4.65), d.CW, Inches(1.45), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(4.65), Inches(0.06), Inches(1.45), b.GOLD)
d.text(s, "Why this matters more than it sounds", d.M + Inches(0.25), Inches(4.82),
       Inches(6), Inches(0.3), size=13, color=b.NAVY, bold=True)
d.text(s, "A blurred positioning statement reads as a company that has not chosen. A defence "
          "buyer who hears a fleet-price pitch concludes the product is a commodity; a fleet "
          "buyer who hears a sovereignty pitch concludes it is not for them. The two stories "
          "are individually strong and jointly weak.",
       d.M + Inches(0.25), Inches(5.16), d.CW - Inches(0.5), Inches(0.8),
       size=12, color=b.INK, shrink=True)
page(s)
notes(s, """
This is the rule that is easiest to break under pressure, usually with the best intentions —
you are in a fleet meeting, it is going badly, and the defence traction is right there as
proof that somebody buys this.
Resist it. The defence proof does not transfer; it actively signals that the fleet product is
a side project.
The same applies in reverse and is more dangerous, because a defence procurement officer who
hears a price-per-unit retrofit pitch will re-categorise the whole conversation as commodity
purchasing.
""")

# ── BANNED CLAIMS ───────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Five claims you may not make — and what to say instead",
         "Enforced from the July deck · unreconciled math, unmeasured effect, or forecast-as-demand")
rows = [
    ["01", "“84% ASIC gross margin”", "Unreconciled arithmetic — retracted until reconciled",
     "“Chip-level margin curve; blended systems margin FY32 88%. We publish the arithmetic.”"],
    ["02", "Any insurance-premium-reduction %", "No actuarial partner, no signed data-share, no baseline",
     "Silence — until a pilot produces a delta an insurer will co-sign"],
    ["03", "“Mandate-ready” for AD2", "Not mapped 1:1 to chiplets in a public homologation doc",
     "“AIS-184/186/187/188 addressable by design; AIS-140 native via S100.”"],
    ["04", "Any accident-reduction %", "Nothing measured — no fleet baseline exists yet",
     "“Pilot design targets a measurable delta; here is the measurement plan.”"],
    ["05", "“5M+ truck TAM” as pipeline", "TAM ≠ SAM ≠ SOM ≠ pipeline",
     "“TAM 5M+; addressable at our BOM ~1.2M; pipeline is what has a name.”"],
]
table(s, ["#", "Banned claim", "Why", "Use instead"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(0.6), Inches(3.1), Inches(4.0), Inches(4.43)], highlight={0, 1},
      row_h=Inches(0.62), left_cols=(0, 1, 2, 3))
d.rect(s, d.M, Inches(5.66), d.CW, Inches(0.95), hx("FDECEE"), radius=0.04)
d.rect(s, d.M, Inches(5.66), Inches(0.06), Inches(0.95), b.CORAL)
d.text(s, "The June IM still contains four of these five", d.M + Inches(0.25), Inches(5.81),
       Inches(7), Inches(0.3), size=13, color=b.NAVY, bold=True)
d.text(s, "It leads with “84% gross margin”, “<$3 die”, “5M+ Trucks” as a headline metric and "
          "“₹2–2.5L mandate-ready kit”. If that document is still in circulation, withdraw it "
          "— it contradicts your own corrections ledger.",
       d.M + Inches(0.25), Inches(6.14), d.CW - Inches(0.5), Inches(0.42),
       size=12, color=b.INK, shrink=True)
page(s)
notes(s, """
This slide is the single most valuable page in the deck for someone about to walk into a
customer meeting, and it came from your own July work rather than from me.
Every banned claim shares a failure mode: it sounds like evidence and is not. A buyer's
technical evaluator will test them, and being caught once on any of the five costs you the
credibility of everything else in the room.
The red panel is the live problem. The June Information Memorandum is the most polished
artefact in the set and it repeats four banned claims. Anyone forwarding it is undoing the
correction work.
""")

# ── PROOF KIT ───────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "What you can put in front of a buyer today",
         "The proof kit — and the honest gaps beside it")
rows = [
    ["₹23.01L delivered — Robot Training", "CONTRACTED", "Sits in Deepgrid Datacentre, NOT Semi. IP is MCEME-owned (Cl. 27)"],
    ["₹78.39L Robotics Assistant", "L1 ONLY", "Lowest bidder, not an award. Never call this revenue"],
    ["GeM record", "CONTRACTED", "Procurement eligibility already established"],
    ["DGS001 module running on FPGA", "SILICON", "Live demo — perception measured at 40fps"],
    ["YOLOv11n at 40fps on FPGA", "MEASURED", "A number you may quote; it was measured"],
    ["15 provisional patents filed Mar 2026", "FILED", "Filed, not granted — say filed"],
    ["Carla-validated D-Drive loop", "VALIDATION", "Simulation, not road. Say so"],
    ["AIS-162/188 certification", "NOT HELD", "A path via NATRAX. Never imply otherwise"],
    ["28nm ASIC silicon", "ROADMAP", "Tapes out ~Q1–mid 2027. FPGA ships today"],
    ["Fleet accident-reduction data", "NONE", "No baseline exists. Banned claim #4"],
    ["Insurer premium-reduction data", "NONE", "No actuarial partner. Banned claim #2"],
]
table(s, ["Asset", "State", "How to use it"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(4.4), Inches(2.0), Inches(5.73)], highlight={0, 1, 2},
      row_h=Inches(0.38), left_cols=(0, 2))
d.rect(s, d.M, Inches(6.14), d.CW, Inches(0.55), b.NAVY, radius=0.04)
d.text(s, "BP-1A states it plainly: “none of it is trucking/ADAS revenue.” Quote ₹23.01L "
          "delivered, in the right entity — never “₹1 Cr defence revenue”.",
       d.M + Inches(0.25), Inches(6.26), d.CW - Inches(0.5), Inches(0.32),
       size=12.5, color=b.WHITE, bold=True, shrink=True)
page(s)
notes(s, """
This is the page to keep open during call preparation.
Everything above the line is showable, and the top three are contracted or measured — they
survive a technical evaluator.
Everything below is where salespeople get into trouble, because each gap has an adjacent
claim that sounds reasonable and is not supported. Filed patents become "patented".
Carla validation becomes "road-validated". A certification path becomes "certified".
Say the state, not the aspiration. The evidence column is deliberately blunt so there is no
ambiguity about which is which.
""")

# ── DIVIDER 03 ──────────────────────────────────────────────────────────────
s = d.slide()
divider(s, "03", "The competitive ground", "What you are actually being compared against")
page(s, dark=True)
notes(s, "Third movement — arenas, the price ladder, and the closing whitespace.")

# ── PRICE LADDER ────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Two contests, not one — and only one of them is won",
         "The price ladder the buyer actually sees")
add_chart(s, XL_CHART_TYPE.BAR_CLUSTERED,
          ["AIS-140 GPS device", "“AIS-compliant” ADAS box", "DGrid full kit (AD2)",
           "Mobileye EyeQ", "Continental ARS", "Qualcomm SA8295", "Nvidia Orin"],
          [("Price (₹ lakh)", [0.08, 0.28, 2.30, 6.50, 10.0, 12.5, 15.0])],
          d.M, Inches(1.82), Inches(7.3), Inches(4.3),
          colors=[b.TEAL], legend=False, num_fmt='0.0"L"', gap=45)
d.rect(s, Inches(8.15), Inches(1.82), Inches(4.58), Inches(4.3), b.NAVY, radius=0.04)
d.text(s, "How to use this in a room", Inches(8.38), Inches(2.04), Inches(4.1), Inches(0.34),
       size=15, color=b.TEAL, bold=True)
d.text(s, [
    {"text": "Against imports: you win, 2.8–6.5×. This contest is already settled and does "
             "not need re-arguing.", "size": 11.5, "color": b.WHITE},
    {"text": "Against the compliance box: you are ~20× the ₹4,500–11,000 anchor. Price is "
             "not an argument you can win here.", "size": 11.5, "color": b.GOLD,
     "space_before": 10},
    {"text": "So never open a fleet conversation on price. Open on what the ₹30,000 box "
             "physically cannot do — transformer perception, driver monitoring, and a "
             "certified latency budget on one part.", "size": 11, "color": b.LIGHT_TEAL,
     "space_before": 10},
    {"text": "The import comparison is for OEM and Tier-1 rooms, where the incumbent bid "
             "actually is ₹6.5L+.", "size": 11, "color": b.LIGHT_TEAL, "space_before": 10},
], Inches(8.38), Inches(2.52), Inches(4.1), Inches(3.4), shrink=True)
badge(s, "VERIFIED", d.M, Inches(6.28), b.ACCENT, w=Inches(1.3))
d.text(s, "AIS-140 street pricing confirmed independently Aug 2026; import prices per company "
          "deck, not independently benchmarked",
       Inches(2.05), Inches(6.32), Inches(10), Inches(0.3), size=10, color=b.MUTED, italic=True)
page(s)
notes(s, """
The chart is deliberately drawn on one axis so the asymmetry is visible: DeepGrid sits far
closer to the compliance box than to the imports, but the buyer's mental anchor is the box.
The practical instruction is the second bullet. Opening on price in a fleet room invites the
comparison you lose. Opening on capability moves the conversation to ground where a ₹30,000
device has no answer at all.
Keep the import comparison for OEM and Tier-1 conversations, where the alternative bid really
is ₹6.5 lakh and up.
""")

# ── WHITESPACE CLOSING ──────────────────────────────────────────────────────
s = d.slide()
d.header(s, "The whitespace is closing about 18 months earlier than mapped",
         "Finding · verified independently this week · this is new information")
rows = [
    ["Netrasemi", "Mapped “(2027)” in the July deck",
     "A2000 production-ready May 2026 · 3 OEM trials live incl. automotive · ₹107 Cr Series A led by Zoho",
     "Validation"],
    ["Netrasemi A4000", "Not mapped", "Edge-AI server chip targeting fab readiness Q2 2027", "Roadmap"],
    ["RoshAI", "Mapped as software-first", "Raised ₹22 Cr for autonomous vehicles in industrial use — adjacent to Phase-3 yards", "Validation"],
    ["Mobileye", "Import comparison only", "Selected by Mahindra for ADAS across six future models", "Production"],
]
table(s, ["Player", "July deck position", "What is true in Aug 2026", "Evidence state"], rows,
      d.M, Inches(1.82), d.CW,
      col_w=[Inches(1.9), Inches(2.9), Inches(6.0), Inches(1.33)], highlight={0},
      row_h=Inches(0.66), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(5.24), Inches(6.4), Inches(1.6), hx("FDECEE"), radius=0.04)
d.rect(s, d.M, Inches(5.24), Inches(0.06), Inches(1.6), b.CORAL)
d.text(s, "What this does to the runway thesis", d.M + Inches(0.25), Inches(5.41),
       Inches(5.9), Inches(0.3), size=13, color=b.NAVY, bold=True)
d.text(s, "Slide 25 of the July deck says the whitespace has a shelf life and that by 2027–28 "
          "at least one peer becomes a real competitor. That is arriving early. Netrasemi is "
          "production-ready now, on roughly twice the capital DeepGrid is raising.",
       d.M + Inches(0.25), Inches(5.75), Inches(5.9), Inches(1.0), size=12,
       color=b.INK, shrink=True)
d.rect(s, Inches(7.25), Inches(5.24), Inches(5.48), Inches(1.6), b.NAVY, radius=0.04)
d.text(s, "But read the evidence state carefully", Inches(7.48), Inches(5.41), Inches(5.0),
       Inches(0.3), size=13, color=b.TEAL, bold=True)
d.text(s, "Netrasemi's A2000 is an edge-AI SoC for video analytics across IoT, healthcare and "
          "surveillance — automotive is one target sector, not the product. It is not a "
          "certified ADAS combo-die with drive-by-wire. The whitespace narrowed; it did not "
          "close.",
       Inches(7.48), Inches(5.75), Inches(5.0), Inches(1.0), size=12,
       color=b.LIGHT_TEAL, shrink=True)
page(s)
notes(s, """
This is the finding this run was for, and it needs to be delivered with its caveat attached.
The headline: a peer your own map placed in 2027 is production-ready now, with three OEM
trials and more capital than you are raising. The 30-month head-start that underwrites the
sequencing is shorter than planned.
The caveat, which matters just as much: the A2000 is a general edge-AI SoC for video
analytics. Automotive is one of several target sectors. It is not an AIS-certified ADAS
combo-die with drive-by-wire actuation, and calling it a direct competitor today would be the
same evidence error the banned-claims list exists to prevent.
Correct reading: the whitespace narrowed, the clock sped up, the differentiated position still
exists — and it now has to be converted faster.
""")

# ── DIVIDER 04 ──────────────────────────────────────────────────────────────
s = d.slide()
divider(s, "04", "Running the motion", "Objections, channel, and the next 90 days")
page(s, dark=True)
notes(s, "Fourth movement — execution.")

# ── OBJECTIONS ──────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "The five objections you will hear, and the honest answer",
         "Battlecards · every answer stays inside the banned-claims rules")
rows = [
    ["“A ₹30,000 box passes the same inspection.”",
     "Correct today, while enforcement is transitional. It cannot do transformer perception, "
     "driver monitoring or a certified latency budget. Move to capability, never argue price."],
    ["“Are you actually AIS certified?”",
     "No — certification is a path, not held. Say so plainly and point to the NATRAX route. "
     "Never say “mandate-ready”."],
    ["“Why not Mobileye? Mahindra chose them.”",
     "True, and for OEM line-fit they have the relationships. Our ground is indigenous supply, "
     "sovereign data, and price at 2.8–6.5× below — strongest where foreign silicon is excluded."],
    ["“What premium reduction will my insurer give?”",
     "We do not have an actuarial partner or a measured baseline, so we will not quote a "
     "number. Here is the pilot measurement plan instead."],
    ["“What if you don't tape out?”",
     "The FPGA product ships today and Track A revenue does not depend on the tapeout. The "
     "ASIC changes cost, not capability."],
]
table(s, ["Objection", "The answer"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(4.5), Inches(7.63)], highlight={0}, row_h=Inches(0.66), left_cols=(0, 1))
d.rect(s, d.M, Inches(5.92), d.CW, Inches(0.62), b.NAVY, radius=0.04)
d.text(s, "Every one of these concedes something true. That is deliberate — a conceded weakness "
          "buys credibility for the claim that follows it.",
       d.M + Inches(0.25), Inches(6.06), d.CW - Inches(0.5), Inches(0.36),
       size=12.5, color=b.WHITE, bold=True, shrink=True)
page(s)
notes(s, """
These are drafted so that each answer opens by conceding the true part of the objection.
That is not politeness, it is technique: a salesperson who concedes an accurate criticism is
believed on the next sentence, and one who deflects is not.
Objection two is the one people fudge. Do not. "Mandate-ready" is a banned claim precisely
because a technical evaluator can check it and will.
Objection five matters more after the Netrasemi finding — buyers who follow the sector will
start asking about tapeout timing, and the honest answer is genuinely reassuring for Track A.
""")

# ── CHANNEL ─────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Channel is the business model, not a sales motion",
         "Dealers, NBFCs and insurers — and the one thing you cannot yet say")
cards(s, [
    ("Dealers — reach",
     "The only way to touch operators below the organised segment. 75–80% of operators own "
     "fewer than five trucks and cannot be sold to directly at any sane acquisition cost."),
    ("NBFCs — affordability",
     "They already finance the truck. Financing the kit alongside it converts a ₹2.3L capital "
     "decision into a monthly line, which is the only framing in which the compliance-box "
     "comparison stops mattering."),
    ("Insurers — the unlock, unquantified",
     "An insurer subsidising part of the kit against a premium discount is the strongest "
     "commercial idea in the plan. It is also where banned claim #2 applies: no percentage "
     "may be quoted until a pilot produces a delta an insurer co-signs."),
], Inches(1.88), cols=3, height=Inches(2.45))
d.rect(s, d.M, Inches(4.60), d.CW, Inches(1.5), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(4.60), Inches(0.06), Inches(1.5), b.GOLD)
d.text(s, "How to sell the insurer motion without quoting a number",
       d.M + Inches(0.25), Inches(4.78), Inches(7), Inches(0.32), size=13.5,
       color=b.NAVY, bold=True)
d.text(s, "Sell the mechanism, not the outcome: “we instrument the fleet, we measure the "
          "delta, and we bring your insurer the data.” That is a real offer, it is fully "
          "supportable today, and it sets up the actuarial partnership that eventually makes "
          "the percentage sayable. Quoting a number now costs you the partnership later.",
       d.M + Inches(0.25), Inches(5.16), d.CW - Inches(0.5), Inches(0.8),
       size=12.5, color=b.INK, shrink=True)
page(s)
notes(s, """
The channel is where this plan actually lives or dies, because the direct-sale segment is
explicitly declared unreachable.
The insurer card is the interesting tension. BP-1A leans on insurer co-funding as the answer
to the price problem, while the July deck bans any premium-reduction percentage until
measured. Both are right, and the resolution is on the gold band: sell the measurement
mechanism rather than the promised outcome.
That is a stronger sales position than an invented number anyway — it gives the insurer a
reason to participate rather than something to disprove.
""")

# ── 90 DAYS ─────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "The next 90 days", "Sequenced so the October wave is not missed")
rows = [
    ["1", "Withdraw the June IM from circulation", "Week 1", "It repeats four banned claims"],
    ["2", "Second defence contract — Track A proof", "Weeks 1–8", "Kill criterion is Month 6; do not wait"],
    ["3", "20 fleet buyer interviews, 1 paid pilot", "Weeks 1–12", "Track B kill criterion, already dated"],
    ["4", "Certification status letter for buyers", "Week 2", "Removes the “are you certified” fudge"],
    ["5", "One NBFC and one insurer conversation", "Weeks 2–6", "Sell the measurement mechanism, no %"],
    ["6", "Re-map the whitespace against Netrasemi", "Week 3", "The 2027 assumption no longer holds"],
    ["7", "OEM/Tier-1 first meeting", "Weeks 4–12", "BP-1A concedes no contact exists yet"],
]
table(s, ["#", "Action", "When", "Why now"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(0.55), Inches(5.2), Inches(1.9), Inches(4.48)], highlight={0, 1, 2},
      row_h=Inches(0.52), left_cols=(0, 1, 3))
d.rect(s, d.M, Inches(6.10), d.CW, Inches(0.62), b.NAVY, radius=0.04)
d.text(s, "Items 2 and 3 are the two kill criteria your own deck already set. Everything else "
          "exists to make those two land.",
       d.M + Inches(0.25), Inches(6.24), d.CW - Inches(0.5), Inches(0.36),
       size=12.5, color=b.WHITE, bold=True, shrink=True)
page(s)
notes(s, """
Sequenced against the October wave rather than against internal convenience.
Item one is free and urgent. The June IM is the most polished document in the set and the
least compliant with your own rules; every copy in circulation is a liability.
Items two and three are not new — they are the kill criteria already written into the July
deck. What this plan adds is refusing to let them drift, because the Netrasemi finding says
the window is shorter than assumed.
Item seven is the highest-value and slowest: BP-1A concedes there is no OEM contact yet, and
OEM line-fit is where the volume actually is.
""")

# ── CLOSE ───────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "What would change this strategy", "Kill criteria and watch items")
rows = [
    ["No second defence contract by Month 6", "Track A drops from primary", "Your own kill criterion"],
    ["No paid fleet pilot in 90 days", "Track B statement is retracted everywhere", "Your own kill criterion"],
    ["AIS certification slips past October 2026", "The forced-buyer wave goes to compliance boxes", "New — from the mandate phasing"],
    ["Netrasemi announces a certified ADAS part", "The differentiated position closes, not narrows", "New — watch quarterly"],
    ["An insurer declines the measurement pilot", "The channel's affordability answer weakens", "Channel dependency"],
]
table(s, ["Trigger", "What it means", "Source"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(4.3), Inches(5.5), Inches(2.33)], highlight={0, 1},
      row_h=Inches(0.56), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(5.32), d.CW, Inches(1.25), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(5.32), Inches(0.06), Inches(1.25), b.GOLD)
d.text(s, "The one-line summary", d.M + Inches(0.25), Inches(5.50), Inches(6), Inches(0.3),
       size=13, color=b.NAVY, bold=True)
d.text(s, "Sell Track A now on proof that already exists, run Track B as a dated experiment, "
          "withdraw the June IM today, and treat the October wave as the deadline it actually "
          "is. The differentiated position is real — it is just worth less every quarter it "
          "goes unconverted.",
       d.M + Inches(0.25), Inches(5.84), d.CW - Inches(0.5), Inches(0.65),
       size=12.5, color=b.INK, shrink=True)
page(s)
notes(s, """
Close on triggers rather than exhortation, because the two that matter are already written
down and dated in your own deck.
The third and fourth rows are new and come from this week's research. Both are watch items
rather than immediate decisions, but both have the property that you will not notice them
passing unless someone is explicitly looking.
The summary line is the whole deck: the position is genuinely differentiated and genuinely
perishable.
""")

out = OUT / "DeepGrid-client-acquisition-draft.pptx"
d.save(out, validate=True)
print(f"slides: {d.n}")
