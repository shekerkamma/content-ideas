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
     "shipping on FPGA today. Backed by ₹1 Cr defence revenue and a GeM record — the only "
     "line that needs neither the certificate nor the tapeout."),
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
d.rect(s, d.M, Inches(4.05), Inches(6.4), Inches(1.75), b.NAVY, radius=0.04)
d.text(s, "Why this changes the pitch", d.M + Inches(0.22), Inches(4.23), Inches(5.9),
       Inches(0.32), size=14, color=b.TEAL, bold=True)
d.text(s, "April 2026 only bound new model introductions — a small population. October 2026 "
          "binds everything already in production. That is when fleet and OEM buyers are "
          "actually forced to move, and it is eight weeks away.",
       d.M + Inches(0.22), Inches(4.60), Inches(5.9), Inches(1.05), size=12,
       color=b.LIGHT_TEAL, shrink=True)
d.rect(s, Inches(7.25), Inches(4.05), Inches(5.48), Inches(1.75), hx("FDECEE"), radius=0.04)
d.rect(s, Inches(7.25), Inches(4.05), Inches(0.06), Inches(1.75), b.CORAL)
d.text(s, "The uncomfortable corollary", Inches(7.48), Inches(4.23), Inches(5.0), Inches(0.32),
       size=14, color=b.NAVY, bold=True)
d.text(s, "AIS certification is a path, not held. If the October wave lands before "
          "certification does, the buyer who is forced to act cannot buy from DeepGrid — "
          "they buy the compliance box. Track A does not have this problem.",
       Inches(7.48), Inches(4.60), Inches(5.0), Inches(1.05), size=12,
       color=b.INK, shrink=True)
badge(s, "VERIFIED", d.M, Inches(5.98), b.ACCENT, w=Inches(1.3))
d.text(s, "Phasing confirmed independently, Aug 2026 · electraytech.com; novushitech.com",
       Inches(2.05), Inches(6.02), Inches(9), Inches(0.3), size=10, color=b.MUTED, italic=True)
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

# ── DIVIDER 02 ──────────────────────────────────────────────────────────────
s = d.slide()
divider(s, "02", "Who to sell to", "Two tracks, two proof burdens, never the same room")
page(s, dark=True)
notes(s, "Second movement — the ICP and the positioning discipline.")

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
     "₹1 Cr defence revenue booked · a GeM record already held · perception running on FPGA "
     "at measured 40fps. None of this waits on AIS certification or the 28nm tapeout."),
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
d.rect(s, d.M, Inches(5.10), d.CW, Inches(0.95), hx("FDECEE"), radius=0.04)
d.rect(s, d.M, Inches(5.10), Inches(0.06), Inches(0.95), b.CORAL)
d.text(s, "The June IM still contains four of these five", d.M + Inches(0.25), Inches(5.25),
       Inches(7), Inches(0.3), size=13, color=b.NAVY, bold=True)
d.text(s, "It leads with “84% gross margin”, “<$3 die”, “5M+ Trucks” as a headline metric and "
          "“₹2–2.5L mandate-ready kit”. If that document is still in circulation, withdraw it "
          "— it contradicts your own corrections ledger.",
       d.M + Inches(0.25), Inches(5.58), d.CW - Inches(0.5), Inches(0.42),
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
d.rect(s, d.M, Inches(4.65), Inches(6.4), Inches(1.6), hx("FDECEE"), radius=0.04)
d.rect(s, d.M, Inches(4.65), Inches(0.06), Inches(1.6), b.CORAL)
d.text(s, "What this does to the runway thesis", d.M + Inches(0.25), Inches(4.82),
       Inches(5.9), Inches(0.3), size=13, color=b.NAVY, bold=True)
d.text(s, "Slide 25 of the July deck says the whitespace has a shelf life and that by 2027–28 "
          "at least one peer becomes a real competitor. That is arriving early. Netrasemi is "
          "production-ready now, on roughly twice the capital DeepGrid is raising.",
       d.M + Inches(0.25), Inches(5.16), Inches(5.9), Inches(1.0), size=12,
       color=b.INK, shrink=True)
d.rect(s, Inches(7.25), Inches(4.65), Inches(5.48), Inches(1.6), b.NAVY, radius=0.04)
d.text(s, "But read the evidence state carefully", Inches(7.48), Inches(4.82), Inches(5.0),
       Inches(0.3), size=13, color=b.TEAL, bold=True)
d.text(s, "Netrasemi's A2000 is an edge-AI SoC for video analytics across IoT, healthcare and "
          "surveillance — automotive is one target sector, not the product. It is not a "
          "certified ADAS combo-die with drive-by-wire. The whitespace narrowed; it did not "
          "close.",
       Inches(7.48), Inches(5.16), Inches(5.0), Inches(1.0), size=12,
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
      col_w=[Inches(4.5), Inches(7.63)], highlight={0}, row_h=Inches(0.74), left_cols=(0, 1))
d.rect(s, d.M, Inches(5.70), d.CW, Inches(0.62), b.NAVY, radius=0.04)
d.text(s, "Every one of these concedes something true. That is deliberate — a conceded weakness "
          "buys credibility for the claim that follows it.",
       d.M + Inches(0.25), Inches(5.84), d.CW - Inches(0.5), Inches(0.36),
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
d.rect(s, d.M, Inches(5.68), d.CW, Inches(0.62), b.NAVY, radius=0.04)
d.text(s, "Items 2 and 3 are the two kill criteria your own deck already set. Everything else "
          "exists to make those two land.",
       d.M + Inches(0.25), Inches(5.82), d.CW - Inches(0.5), Inches(0.36),
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
d.rect(s, d.M, Inches(4.90), d.CW, Inches(1.25), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(4.90), Inches(0.06), Inches(1.25), b.GOLD)
d.text(s, "The one-line summary", d.M + Inches(0.25), Inches(5.08), Inches(6), Inches(0.3),
       size=13, color=b.NAVY, bold=True)
d.text(s, "Sell Track A now on proof that already exists, run Track B as a dated experiment, "
          "withdraw the June IM today, and treat the October wave as the deadline it actually "
          "is. The differentiated position is real — it is just worth less every quarter it "
          "goes unconverted.",
       d.M + Inches(0.25), Inches(5.42), d.CW - Inches(0.5), Inches(0.65),
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
