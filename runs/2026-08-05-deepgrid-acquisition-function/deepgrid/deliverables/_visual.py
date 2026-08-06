### BLOCK: DIV_WHO
# ── DIV WHO ─────────────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)
bgp = ASSET / "harvested" / "deck_image37.png"
if bgp.exists():
    s.shapes.add_picture(str(bgp), 0, 0, d.W, d.H)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.rect(s, Inches(0.85), Inches(2.55), Inches(7.2), Inches(2.1), b.NAVY, radius=0.04)
d.text(s, "PART 01", Inches(1.10), Inches(2.78), Inches(6), Inches(0.34),
       size=14, color=b.TEAL, bold=True)
d.text(s, "Who we sell to", Inches(1.10), Inches(3.20), Inches(6.7), Inches(0.9),
       size=40, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.text(s, "Two segments now, and the disqualifiers that save weeks",
       Inches(1.10), Inches(4.06), Inches(6.7), Inches(0.4), size=15,
       color=b.LIGHT_TEAL, shrink=True)
page(s, dark=True)
notes(s, "Part one — targeting.")

### BLOCK: PRICE_CHART
# ── PRICE LADDER ────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Two contests, and only one of them is winnable on price",
         "The ladder the buyer actually sees — from 02-icp.md and 05-objections.md")
add_chart(s, XL_CHART_TYPE.BAR_CLUSTERED,
          ["AIS-140 GPS device", "“AIS-compliant” box", "DeepGrid AD2 kit",
           "Mobileye EyeQ", "Continental ARS", "Nvidia Orin"],
          [("Price (₹ lakh)", [0.08, 0.28, 2.30, 6.50, 10.0, 15.0])],
          d.M, Inches(1.82), Inches(7.3), Inches(4.2),
          colors=[b.TEAL], legend=False, num_fmt='0.0"L"', gap=45)
d.rect(s, Inches(8.15), Inches(1.82), Inches(4.58), Inches(4.2), b.NAVY, radius=0.04)
d.text(s, "How to use this in a room", Inches(8.38), Inches(2.04), Inches(4.1),
       Inches(0.34), size=15, color=b.TEAL, bold=True)
d.text(s, [
    {"text": "Against imports we win 2.8–6.5×. That contest is settled and does not need "
             "re-arguing.", "size": 11.5, "color": b.WHITE},
    {"text": "Against the compliance box we are ~20× the anchor. Price is not an argument "
             "we can win here.", "size": 11.5, "color": b.GOLD, "space_before": 10},
    {"text": "So never open a fleet conversation on price. Open on certified AEBS — what "
             "the ₹30,000 box physically cannot do.", "size": 11, "color": b.LIGHT_TEAL,
     "space_before": 10},
    {"text": "Keep the import comparison for OEM and Tier-1 rooms, where the alternative "
             "bid really is ₹6.5L and up.", "size": 11, "color": b.LIGHT_TEAL,
     "space_before": 10},
], Inches(8.38), Inches(2.52), Inches(4.1), Inches(3.3), shrink=True)
badge(s, "VERIFIED", d.M, Inches(6.22), b.ACCENT, w=Inches(1.3))
d.text(s, "AIS-140 street pricing confirmed independently Aug 2026; import prices per "
          "company deck, not benchmarked", Inches(2.05), Inches(6.26), Inches(10),
       Inches(0.3), size=10, color=b.MUTED, italic=True, shrink=True)
page(s)
notes(s, """
One axis, deliberately, so the asymmetry is impossible to miss: DeepGrid sits far closer to
the compliance box than to the imports, but the buyer's mental anchor is the box.
The instruction is the second bullet. Opening on price invites the comparison we lose.
Opening on certified AEBS moves the conversation to ground where a ₹30,000 device has no
answer at all.
""")

### BLOCK: DIV_HOW
# ── DIV HOW ─────────────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)
bgp = ASSET / "harvested" / "deck_image14.png"
if bgp.exists():
    s.shapes.add_picture(str(bgp), 0, 0, d.W, d.H)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.rect(s, Inches(0.85), Inches(2.55), Inches(7.2), Inches(2.1), b.NAVY, radius=0.04)
d.text(s, "PART 02", Inches(1.10), Inches(2.78), Inches(6), Inches(0.34),
       size=14, color=b.TEAL, bold=True)
d.text(s, "How a lead travels", Inches(1.10), Inches(3.20), Inches(6.7), Inches(0.9),
       size=40, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.text(s, "One intake path, one state machine, written-down approvals",
       Inches(1.10), Inches(4.06), Inches(6.7), Inches(0.4), size=15,
       color=b.LIGHT_TEAL, shrink=True)
page(s, dark=True)
notes(s, "Part two — the pipeline.")

### BLOCK: LADDER_CHART
# ── LADDER CHART ────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Ten levels, built in order — we are at three",
         "Each level must remove a task from somebody's calendar, or it is deleted")
add_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED,
          ["L1\nPrompt", "L2\nChain", "L3\nBrain", "L4\nSkill", "L5\nDeliverable",
           "L6\nConnect", "L7\nAgent", "L8\nTeam", "L9\nAlways on", "L10\nFunction"],
          [("Build effort (hours)", [0.3, 1, 2, 2, 3, 1, 4, 12, 8, 80])],
          d.M, Inches(1.82), Inches(7.5), Inches(3.9),
          colors=[b.TEAL], legend=False, num_fmt='0"h"', gap=40)
d.text(s, "Effort is not the constraint — sequence is. Level 7 built on a broken Level 3 is "
          "just a faster mess.", d.M, Inches(5.82), Inches(7.5), Inches(0.4),
       size=10.5, color=b.MUTED, shrink=True)
kpi_at(s, [("L3", "Building now", "the Brain", b.GOLD),
           ("L6", "Blocked", "no CRM exists", b.CORAL)],
       Inches(8.25), Inches(1.86), Inches(4.48))
d.rect(s, Inches(8.25), Inches(3.48), Inches(4.48), Inches(2.75), b.NAVY, radius=0.04)
d.text(s, "Why Level 3 first", Inches(8.48), Inches(3.70), Inches(4.0), Inches(0.34),
       size=15, color=b.TEAL, bold=True)
d.text(s, [
    {"text": "Levels 1 and 2 are trivial once the Brain exists — and writing them first "
             "would encode the contradictions between the four source documents.",
     "size": 11.5, "color": b.WHITE},
    {"text": "Level 6 is genuinely blocked: there is no CRM or shared store, so a connected "
             "system has nowhere to read and write.", "size": 11, "color": b.LIGHT_TEAL,
     "space_before": 10},
    {"text": "That is a purchase decision, not something to engineer around.",
     "size": 11, "color": b.GOLD, "space_before": 10},
], Inches(8.48), Inches(4.14), Inches(4.0), Inches(1.95), shrink=True)
page(s)
notes(s, """
The chart is build effort, and it deliberately shows that effort is not what governs the
order — sequence is.
Level 10 dwarfs everything else at roughly two to four weeks on top of all the rest, which is
why jumping to it is the classic failure.
The blocked marker on Level 6 is the honest constraint. No CRM means no connection layer, and
no connection layer means agents have nothing real to act on. Fix that before anything above
it is worth attempting.
""")

### BLOCK: DIV_NEXT
# ── DIV NEXT ────────────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)
bgp = ASSET / "harvested" / "deck_image9.png"
if bgp.exists():
    s.shapes.add_picture(str(bgp), 0, 0, d.W, d.H)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.rect(s, Inches(0.85), Inches(2.55), Inches(7.2), Inches(2.1), b.NAVY, radius=0.04)
d.text(s, "PART 03", Inches(1.10), Inches(2.78), Inches(6), Inches(0.34),
       size=14, color=b.TEAL, bold=True)
d.text(s, "What happens next", Inches(1.10), Inches(3.20), Inches(6.7), Inches(0.9),
       size=40, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.text(s, "Three founder decisions gate everything else",
       Inches(1.10), Inches(4.06), Inches(6.7), Inches(0.4), size=15,
       color=b.LIGHT_TEAL, shrink=True)
page(s, dark=True)
notes(s, "Part three — execution.")

### BLOCK: TRACKS
# ── TRACKS ──────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Two tracks, two proof burdens, never the same room",
         "From 02-icp.md and 05-objections.md · positioning discipline")
photo(s, "robots", d.M, Inches(1.86), Inches(6.0), Inches(1.7))
photo(s, "radar-viz", Inches(6.98), Inches(1.86), Inches(5.75), Inches(1.7))
d.rect(s, d.M, Inches(3.68), Inches(6.0), Inches(2.55), b.NAVY, radius=0.04)
d.text(s, "TRACK A · DEFENCE, PSU, YARDS — SELL NOW", d.M + Inches(0.22), Inches(3.86),
       Inches(5.5), Inches(0.3), size=11.5, color=b.TEAL, bold=True)
d.text(s, [
    {"text": "Say: sovereign data, on-die HSM, Indian-designed, shipping on FPGA, GeM "
             "record, ₹23.01L delivered.", "size": 11.5, "color": b.WHITE},
    {"text": "Never say: the retrofit price line, fleet ROI, or anything about insurance.",
     "size": 11.5, "color": b.CORAL, "space_before": 8},
    {"text": "Gate: a named programme and a named SI partner by Month 3, or this is a "
             "services business rather than a silicon one.", "size": 11,
     "color": b.LIGHT_TEAL, "space_before": 8},
], d.M + Inches(0.22), Inches(4.22), Inches(5.5), Inches(1.85), shrink=True)
d.rect(s, Inches(6.98), Inches(3.68), Inches(5.75), Inches(2.55), b.NAVY_2, radius=0.04)
d.text(s, "TRACK B · FLEETS — RECRUIT DESIGN PARTNERS", Inches(7.20), Inches(3.86),
       Inches(5.3), Inches(0.3), size=11.5, color=b.GOLD, bold=True)
d.text(s, [
    {"text": "Say: the 1 Oct 2027 AEBS requirement, one kit covering AEBS and DMS, "
             "influence over what gets certified for your fleet.", "size": 11.5,
     "color": b.WHITE},
    {"text": "Never say: sovereign data, defence customers, or a 2026 deadline.",
     "size": 11.5, "color": b.CORAL, "space_before": 8},
    {"text": "Gate: two design partners committing fleet access and a measurement baseline "
             "by Month 4.", "size": 11, "color": b.LIGHT_TEAL, "space_before": 8},
], Inches(7.20), Inches(4.22), Inches(5.3), Inches(1.85), shrink=True)
d.rect(s, d.M, Inches(6.35), d.CW, Inches(0.5), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(6.35), Inches(0.06), Inches(0.5), b.GOLD)
d.text(s, "A blurred statement reads as a company that has not chosen. The two stories are "
          "individually strong and jointly weak.",
       d.M + Inches(0.25), Inches(6.46), d.CW - Inches(0.5), Inches(0.3),
       size=11.5, color=b.INK, bold=True, shrink=True)
page(s)
notes(s, """
The discipline rule is the easiest to break under pressure and usually with good intentions —
a fleet meeting is going badly and the defence traction is right there as proof somebody buys
this.
Resist it. Defence proof does not transfer; it signals the fleet product is a side project.
In reverse it is worse: a procurement officer who hears a per-unit retrofit pitch
re-categorises the whole conversation as commodity buying.
Both gates are revised from the original plan because verification showed the originals were
either unreachable or measuring the wrong thing.
""")
