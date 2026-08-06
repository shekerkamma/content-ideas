### BLOCK: WHAT_WE_SELL
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
          "frame budget (74% headroom)", d.M, Inches(6.22), d.CW, Inches(0.3), size=10.5,
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

### BLOCK: WHY_SILICON
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
d.rect(s, d.M, Inches(6.05), d.CW, Inches(0.62), b.NAVY, radius=0.04)
d.text(s, "Sequence matters: capability opens a fleet conversation, control opens a defence "
          "one, and cost closes both. Cost never opens.",
       d.M + Inches(0.25), Inches(6.19), d.CW - Inches(0.5), Inches(0.36),
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

### BLOCK: ICP
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
d.rect(s, d.M, Inches(5.30), d.CW, Inches(0.95), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(5.30), Inches(0.06), Inches(0.95), b.GOLD)
d.text(s, "The two highlighted rows need neither the certificate nor the tapeout",
       d.M + Inches(0.25), Inches(5.45), Inches(7), Inches(0.3), size=13,
       color=b.NAVY, bold=True)
d.text(s, "That is the whole reason they are this quarter's targets. Every other segment is "
          "gated on something DeepGrid does not yet hold, and selling into a gate you cannot "
          "open burns the relationship you will need later.",
       d.M + Inches(0.25), Inches(5.78), d.CW - Inches(0.5), Inches(0.42),
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

### BLOCK: BUYER_COMMITTEE
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

### BLOCK: PROOF_KIT
# ── PROOF KIT ───────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "What you can put in front of a buyer today",
         "The proof kit — and the honest gaps beside it")
rows = [
    ["₹1 Cr defence revenue", "CONTRACTED", "Strongest single asset. Track A only"],
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
      row_h=Inches(0.42), left_cols=(0, 2))
d.rect(s, d.M, Inches(6.10), d.CW, Inches(0.55), b.NAVY, radius=0.04)
d.text(s, "The top three sell Track A today. The bottom four are why Track B is an experiment "
          "and not a pipeline.",
       d.M + Inches(0.25), Inches(6.22), d.CW - Inches(0.5), Inches(0.32),
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
