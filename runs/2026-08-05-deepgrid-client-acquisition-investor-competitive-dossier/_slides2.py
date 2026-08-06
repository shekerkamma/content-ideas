# ── COVER ───────────────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)
bg = ASSET / "harvested" / "deck_image1.png"
if bg.exists():
    s.shapes.add_picture(str(bg), 0, 0, d.W, d.H)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.text(s, "CLIENT ACQUISITION STRATEGY  ·  v2, POST-VERIFICATION", Inches(0.85),
       Inches(1.80), Inches(9.0), Inches(0.4), size=13, color=b.TEAL, bold=True)
d.text(s, "Fix the claims first,\nthen run the motion", Inches(0.85), Inches(2.30),
       Inches(8.2), Inches(1.6), size=40, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.rect(s, Inches(0.85), Inches(4.10), Inches(1.6), Inches(0.05), b.TEAL)
d.text(s, "DeepGrid Semi · commercial lead briefing · rebuilt after independent verification "
          "contradicted the previous version",
       Inches(0.85), Inches(4.40), Inches(9.0), Inches(0.6), size=14.5,
       color=b.LIGHT_TEAL, shrink=True)
for i, chip in enumerate(["Oct 2027, not Oct 2026", "9 claims to retire",
                          "72% kit only", "sell by function"]):
    x = Inches(0.85) + i * Inches(2.6)
    d.rect(s, x, Inches(5.35), Inches(2.45), Inches(0.44), b.NAVY_2, radius=0.25, line=b.ACCENT)
    d.text(s, chip, x, Inches(5.47), Inches(2.45), Inches(0.26), size=10,
           color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER)
page(s, dark=True)
notes(s, """
This is version two. Version one was built on vendor blogs that described a draft rule as if it
were law, and it got the central timing claim wrong by roughly eighteen months.
Independent citation verification against the gazette, plus five independent analytical
lenses, produced fourteen contradictions — almost all of them between DeepGrid's own
documents. This deck is rebuilt on what survived.
""")

# ── EXEC SUMMARY ────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "You have 18 months more runway than assumed — and less to say than assumed",
         "Executive summary")
d.rect(s, d.M, Inches(1.78), d.CW, Inches(0.95), b.NAVY, radius=0.04)
d.text(s, "BLUF", d.M + Inches(0.22), Inches(1.92), Inches(1.0), Inches(0.3),
       size=11, color=b.TEAL, bold=True)
d.text(s, "The ADAS perception mandate lands 1 Oct 2027, not Oct 2026 — GSR 184(E) was a "
          "draft. That buys time, and time is what the claim set needs: nine statements "
          "currently in circulation fail on first technical contact. Fix those before anyone "
          "carries this into a buyer meeting.",
       d.M + Inches(1.35), Inches(1.88), d.CW - Inches(1.6), Inches(0.76),
       size=13, color=b.WHITE, shrink=True)
cards(s, [
    ("What changed",
     "The notified rule is G.S.R. 834(E), Nov 2025. AEBS binds 1 Jan 2027 (new) and 1 Oct "
     "2027 (all); perception functions 1 Oct 2027 and 1 Jan 2028. The compliance wall is "
     "later — so is the revenue."),
    ("What survives",
     "Indigenous supply and sovereign-data eligibility. A real kit-level margin of 72%. "
     "Certified AEBS + DMS as a *function* the ₹30k box cannot deliver. Procurement access "
     "already demonstrated on GeM."),
    ("What does not",
     "“39.3 TOPS measured”, “84%” and “88% blended” margins, “12.9× cheaper”, “₹1 Cr "
     "defence revenue”, and transformer-VLA-on-chip. Each is disprovable by a competent "
     "evaluator in one meeting."),
], Inches(2.92), cols=3, height=Inches(2.15))
d.rect(s, d.M, Inches(5.32), d.CW, Inches(0.62), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(5.32), Inches(0.06), Inches(0.62), b.GOLD)
d.text(s, "The sequence is not negotiable: retire the nine claims, then sell Track A on "
          "eligibility, then validate Track B against the 2027 clock.",
       d.M + Inches(0.25), Inches(5.46), d.CW - Inches(0.5), Inches(0.4),
       size=12.5, color=b.INK, bold=True, shrink=True)
page(s)
notes(s, """
Two messages, and the second is the uncomfortable one.
The good news is real: eighteen months of additional runway before the perception mandate
binds. That is time to certify, to tape out, and to build the reference accounts.
The bad news is that the current claim set cannot be used. Nine statements in circulation are
either arithmetically impossible, physically infeasible, or describe a different legal entity.
A salesperson who repeats them will be caught by the first competent technical evaluator, and
the cost of that is not one deal — it is the credibility of everything else in the room.
""")

# ── CLAIMS THAT FAIL ────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Nine claims to retire before anyone sells",
         "Each is disprovable from public sources or DeepGrid's own documents")
rows = [
    ["“39.3 TOPS measured on FPGA”", "Artix-7 board ceilings ~1.8 TOPS — 22× short. The IM correctly calls 39.3 a derivation", "Academic"],
    ["“84% ASIC gross margin”", "Already retracted by the July Corrections Ledger", "July deck"],
    ["“88% blended systems margin”", "Needs 120% margin on all non-kit revenue. Impossible", "Skeptic"],
    ["“12.9× cheaper than Mobileye”", "Compares their ASP to our die cost. Loaded, it is ~2.3×", "Economist"],
    ["“₹1 Cr defence revenue”", "₹23.01L delivered; rest is L1. Different entity; IP MCEME-owned", "BP-1A §9"],
    ["Transformer VLA runs on-chip", "Bandwidth-bound: ~68 ms to stream weights vs a 33.3 ms budget", "Academic"],
    ["“Mandate live since April 2026”", "GSR 184(E) was a draft. Real rule G.S.R. 834(E), Nov 2025", "Gazette"],
    ["“ASIL-D path”", "No functional-safety line item; ISO 26262 pre-audit is on the stop-doing list", "Academic"],
    ["Any insurance or accident-reduction %", "No actuarial partner, no measured baseline", "July deck"],
]
table(s, ["Claim in circulation", "Why it fails", "Source"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(3.9), Inches(6.4), Inches(1.83)], highlight={0, 4, 6},
      row_h=Inches(0.46), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(6.10), d.CW, Inches(0.62), hx("FDECEE"), radius=0.04)
d.rect(s, d.M, Inches(6.10), Inches(0.06), Inches(0.62), b.CORAL)
d.text(s, "The June IM contains six of these nine. Withdraw it from circulation today — it is "
          "the most polished document you have and the least defensible.",
       d.M + Inches(0.25), Inches(6.24), d.CW - Inches(0.5), Inches(0.4),
       size=12.5, color=b.INK, bold=True, shrink=True)
page(s)
notes(s, """
This is the page that matters most, and it should be read before any customer contact.
Three are highlighted because they are the ones most likely to be repeated by someone acting
in good faith: the TOPS number appears on three slides of the July deck, the defence revenue
is the headline proof asset, and the mandate date is in every document.
Note what this list is not. It is not a claim that the technology is bad or the market is
wrong. It is a claim that these specific statements cannot survive scrutiny, and that using
them converts a technical conversation into a credibility problem.
""")

# ── DIVIDER 01 ──────────────────────────────────────────────────────────────
s = d.slide()
divider(s, "01", "The real demand clock", "When the buyer is actually compelled to act")
page(s, dark=True)
notes(s, "First movement — corrected timing, and what the domestic precedent predicts.")

# ── CORRECTED MANDATE ───────────────────────────────────────────────────────
s = d.slide()
d.header(s, "The perception mandate binds 1 October 2027, not October 2026",
         "G.S.R. 834(E) of 11 Nov 2025, amended by 862(E) — verified against the gazette")
rows = [
    ["G.S.R. 184(E)", "20 Mar 2025", "DRAFT for comment — not law", "Superseded"],
    ["G.S.R. 834(E)", "11 Nov 2025", "CMV Sixth Amendment Rules 2025 — the notified rule", "In force"],
    ["AEBS (AIS-162), stability, braking", "1 Jan 2027 new", "1 Oct 2027 all models", "17 months"],
    ["LDWS, DDAWS, BSIS, MOIS (rule 125Q)", "1 Oct 2027 new", "1 Jan 2028 existing", "26 months"],
]
table(s, ["Instrument / system", "First date", "Full application", "From today"], rows,
      d.M, Inches(1.82), d.CW,
      col_w=[Inches(4.4), Inches(2.4), Inches(3.4), Inches(1.93)], highlight={2, 3},
      row_h=Inches(0.52), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(4.35), Inches(6.4), Inches(1.85), b.NAVY, radius=0.04)
d.text(s, "What this changes", d.M + Inches(0.22), Inches(4.53), Inches(5.9), Inches(0.32),
       size=14, color=b.TEAL, bold=True)
d.text(s, "Version one of this deck said October 2026 and treated it as eight weeks away. "
          "That came from vendor blogs which dropped the word “draft”. Five of them agreed, "
          "which looked like corroboration and was correlated error from one upstream "
          "source. The real first wall is 17 months out.",
       d.M + Inches(0.22), Inches(4.90), Inches(5.9), Inches(1.15), size=12,
       color=b.LIGHT_TEAL, shrink=True)
d.rect(s, Inches(7.25), Inches(4.35), Inches(5.48), Inches(1.85), hx("FFF4D6"), radius=0.04)
d.rect(s, Inches(7.25), Inches(4.35), Inches(0.06), Inches(1.85), b.GOLD)
d.text(s, "The commercial read", Inches(7.48), Inches(4.53), Inches(5.0), Inches(0.32),
       size=14, color=b.NAVY, bold=True)
d.text(s, "More runway, later revenue. Certification and tapeout now have room to land before "
          "the wall — which removes the panic case. But Track B's “deadline is coming” pitch "
          "does not bite in 2026, and any FY27 revenue must come from buyers who are not "
          "waiting for the rule.",
       Inches(7.48), Inches(4.90), Inches(5.0), Inches(1.15), size=12,
       color=b.INK, shrink=True)
badge(s, "VERIFIED", d.M, Inches(6.35), b.ACCENT, w=Inches(1.3))
d.text(s, "Gazette text checked directly; corroborated by TOI 5-Nov-2025 and Gadkari's Lok "
          "Sabha reply, 12-Feb-2026", Inches(2.05), Inches(6.39), Inches(10), Inches(0.3),
       size=10, color=b.MUTED, italic=True, shrink=True)
page(s)
notes(s, """
This slide is a correction of my own previous work, and it should be presented as such if
anyone saw version one.
The failure mode is worth naming because it will recur: five independent-looking sources
agreed, and all five were downstream of the same draft notification. Agreement is not
corroboration when the sources share an upstream.
The rule for regulatory claims from here: the gazette or the ministry, or it does not go on a
slide. Vendor blogs are for discovery only.
""")

# ── AIS-140 PRECEDENT ───────────────────────────────────────────────────────
s = d.slide()
d.header(s, "India's own precedent says the box loses and the relationship wins",
         "AIS-140 is the closest domestic analogue — and it is not encouraging for hardware")
cards(s, [
    ("Enforcement took ~8 years",
     "Notified 2018, phased 2019, legacy registrations only caught in Oct 2025, rules still "
     "moving in 2026 — gated on state backend readiness, not on suppliers. Assume the same "
     "slippage risk on 2027–28 dates."),
    ("Prices never consolidated",
     "Devices still sell at ₹3,500–12,000 with 3–4× spreads and no market concentration. "
     "Nobody built a hardware franchise. A mandate caps willingness to pay at the cost of "
     "non-compliance, not the value of safety."),
    ("Value went to the recurring layer",
     "Whoever held the compliance relationship won — Vahan linkage, SIM, certificate "
     "renewal, uptime SLA. Not the box, and certainly not the chip inside it."),
], Inches(1.88), cols=3, height=Inches(2.45))
d.rect(s, d.M, Inches(4.60), d.CW, Inches(1.55), b.NAVY, radius=0.04)
d.text(s, "The strategic implication for DeepGrid", d.M + Inches(0.25), Inches(4.78),
       Inches(7), Inches(0.32), size=14, color=b.TEAL, bold=True)
d.text(s, "If value migrates to the recurring compliance layer again, then the durable "
          "position is not the ₹2.3L kit — it is owning certificate renewal, uptime "
          "reporting and the data relationship that sits on top of it. That is also the only "
          "asset an incumbent with a cheaper regional SKU cannot take away. Build the "
          "recurring layer into the first contracts, not into a later phase.",
       d.M + Inches(0.25), Inches(5.16), d.CW - Inches(0.5), Inches(0.85),
       size=12.5, color=b.LIGHT_TEAL, shrink=True)
page(s)
notes(s, """
This is the finding a commercial lead should argue with hardest, because it cuts against the
whole premise of selling a premium kit.
AIS-140 is the same ministry, the same buyer, the same enforcement machinery. It took eight
years and produced no consolidation. Prices stayed spread three to fourfold, which tells you
the market never rewarded a better box.
What it did reward was whoever ended up holding the ongoing compliance relationship. That is
recurring, defensible, and largely absent from DeepGrid's current commercial design — the
plan sells a kit and treats software as a later phase.
The practical instruction is to put the recurring layer into the first contract, even at a
token price, rather than sequencing it after hardware scale.
""")

# ── DIVIDER 02 ──────────────────────────────────────────────────────────────
s = d.slide()
divider(s, "02", "What you can actually claim", "The evidence that survived verification")
page(s, dark=True)
notes(s, "Second movement — the defensible claim set.")

# ── PROOF KIT ───────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "What you can put in front of a buyer today",
         "Corrected proof kit — state the evidence level, never the aspiration")
rows = [
    ["GeM record + procurement access", "CONTRACTED", "Real, and the strongest Track A asset"],
    ["₹23.01L delivered — Robot Training", "CONTRACTED", "In Deepgrid Datacentre, not Semi. IP MCEME-owned"],
    ["₹78.39L Robotics Assistant", "L1 ONLY", "Lowest bidder, not an award. Never call it revenue"],
    ["YOLOv11n at 40fps on FPGA", "MEASURED", "A real measured number — quote this, not 39.3 TOPS"],
    ["24.25 ms attention head", "MEASURED", "The honest perception-latency datapoint"],
    ["DGS001 module running on FPGA", "SILICON", "Live demo. Artix-7 class — do not imply ASIC performance"],
    ["15 provisional patents, Mar 2026", "FILED", "Filed, not granted. Say filed"],
    ["Carla-validated D-Drive loop", "SIMULATION", "Not road-validated. Say simulation"],
    ["AIS-162/188 certification", "NOT HELD", "A path via NATRAX. Never imply otherwise"],
    ["28nm ASIC silicon", "ROADMAP", "MPW shuttle. Cannot be AEC-Q100 qualified as-is"],
    ["Power / thermal envelope", "NOT STATED", "Appears in no document. Expect this question"],
]
table(s, ["Asset", "State", "How to use it"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(4.4), Inches(2.0), Inches(5.73)], highlight={0, 3, 4},
      row_h=Inches(0.38), left_cols=(0, 2))
d.rect(s, d.M, Inches(6.42), d.CW, Inches(0.5), b.NAVY, radius=0.04)
d.text(s, "Three green rows carry Track A. Everything below “SILICON” is a question you will "
          "be asked, not a claim you can make.",
       d.M + Inches(0.25), Inches(6.53), d.CW - Inches(0.5), Inches(0.3),
       size=12, color=b.WHITE, bold=True, shrink=True)
page(s)
notes(s, """
Keep this open during call preparation. It replaces the version-one proof kit, which
overstated the defence revenue and omitted the power question entirely.
The two measured numbers — 40 fps YOLOv11n and the 24.25 ms attention head — are genuinely
good and genuinely defensible. Lead with them. They are also more persuasive to an engineer
than a derived TOPS figure, because they describe an outcome rather than a capability.
The last row is the one nobody has prepared for. No document states a power or thermal
envelope, and for an M.2 module in a truck cabin at 28nm that is the first question a
serious integrator asks.
""")

# ── MARGIN POSITION ─────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Quote 72% at kit level, and no blended figure at all",
         "72% and 88% cannot both be true — the arithmetic is one line")
d.text(s, "Reconstructing FY2032 from the plan's own segment revenues", d.M, Inches(1.80),
       Inches(7.3), Inches(0.32), size=14, color=b.NAVY, bold=True)
table(s, ["Step", "Value"], [
    ["FY32 revenue", "₹1,387.95 Cr"],
    ["Gross profit implied by 88.4% blended", "₹1,226.95 Cr"],
    ["ADAS kit at BP-1A's stated 72%", "₹657.83 Cr"],
    ["Revenue left across all other lines", "₹474.30 Cr"],
    ["Gross profit still required from it", "₹569.12 Cr"],
    ["Margin that implies", "120.0% — impossible"],
], d.M, Inches(2.20), Inches(7.3), col_w=[Inches(5.1), Inches(2.2)],
    highlight={5}, row_h=Inches(0.44), left_cols=(0,))
d.rect(s, Inches(8.05), Inches(1.80), Inches(4.68), Inches(4.35), b.NAVY, radius=0.04)
d.text(s, "What to say instead", Inches(8.28), Inches(2.02), Inches(4.2), Inches(0.34),
       size=15, color=b.TEAL, bold=True)
d.text(s, [
    {"text": "A blend cannot exceed its best component. 88.4% requires ~89% on the truck "
             "kit — the exact figure BP-1A retracted.", "size": 11.5, "color": b.WHITE},
    {"text": "Hold the kit at 72% and the honest blend is 77.2%. The gap is ₹156 Cr of "
             "gross profit.", "size": 11.5, "color": b.GOLD, "space_before": 10},
    {"text": "So the Corrections Ledger replaced one unsupportable number with another. "
             "Both must go.", "size": 11, "color": b.LIGHT_TEAL, "space_before": 10},
    {"text": "Approved line: “72% kit-level gross margin at ASIC phase, per our own unit "
             "economics. We do not publish a blended figure.”", "size": 11.5,
     "color": b.WHITE, "bold": True, "space_before": 10},
], Inches(8.28), Inches(2.52), Inches(4.2), Inches(3.4), shrink=True)
badge(s, "VERIFIED", d.M, Inches(5.30), b.ACCENT, w=Inches(1.3))
d.text(s, "Recomputed from BP-1A §8 segment revenues", Inches(2.05), Inches(5.34),
       Inches(5.0), Inches(0.3), size=10, color=b.MUTED, italic=True)
page(s)
notes(s, """
This is a one-line argument you should be able to make from memory, because a sharp buyer or
investor will do it in their head.
A blended margin cannot exceed the margin of its best component. The truck kit is roughly two
thirds of revenue. If it earns 72%, there is no arrangement of the remaining third that gets
the blend to 88%.
The approved formulation is deliberately modest: quote the kit number, cite your own unit
economics, and decline to give a blended figure. Declining is stronger than guessing, and it
signals that the numbers you do give have been checked.
""")

# ── COST POSITION ───────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "The advantage is ~2.3×, and it is not really a cost advantage",
         "The cost story rebuilt on the plan's own volumes")
rows = [
    ["Die cost quoted", "$3.876", "But that quote is at 1,000,000 units"],
    ["Plan's peak-year volume", "72,000 units", "18,000 AD2 kits + 54,000 AD0 mirrors"],
    ["NRE loaded over break-even volume", "≈ $18/die", "$3.17M over ~175,000 cumulative chips"],
    ["Effective loaded die cost", "≈ $22", "vs Mobileye's $50 reference"],
    ["Real advantage", "≈ 2.3×", "Not the 12.9× on the current slides"],
]
table(s, ["Line", "Value", "Note"], rows, d.M, Inches(1.82), Inches(7.4),
      col_w=[Inches(3.0), Inches(1.7), Inches(2.7)], highlight={4}, row_h=Inches(0.46),
      left_cols=(0, 2))
d.rect(s, Inches(8.15), Inches(1.82), Inches(4.58), Inches(4.35), b.NAVY, radius=0.04)
d.text(s, "The moat is stated backwards", Inches(8.38), Inches(2.04), Inches(4.1),
       Inches(0.34), size=15, color=b.TEAL, bold=True)
d.text(s, [
    {"text": "Incumbents amortise NRE across tens of millions of units, so their marginal "
             "cost sits *below* the loaded cost here. “They cannot follow us down” is "
             "false.", "size": 11.5, "color": b.WHITE},
    {"text": "What DeepGrid actually owns is cannibalisation immunity — no global ASP to "
             "defend. That is why the incumbent response is a stripped regional SKU, not a "
             "price cut.", "size": 11.5, "color": b.GOLD, "space_before": 10},
    {"text": "Approved line: “we have no legacy ASP to protect, so we can price an "
             "India-specific product at a level a global vendor will not.” True, "
             "defensible, and it survives a cost audit.", "size": 11,
     "color": b.LIGHT_TEAL, "space_before": 10},
], Inches(8.38), Inches(2.52), Inches(4.2), Inches(3.4), shrink=True)
d.text(s, "The 12.9× figure compares Mobileye's selling price to DeepGrid's die cost — the "
          "same category error that got 774× retracted.", d.M, Inches(4.55), Inches(7.4),
       Inches(0.5), size=11, color=b.MUTED, italic=True, shrink=True)
page(s)
notes(s, """
The cost claim needed rebuilding because it compares a competitor's price to our cost, which
is the exact error the Corrections Ledger retracted 774× for. Restating it as 12.9× did not
fix the category error, only the magnitude.
Loaded properly, the advantage is about 2.3×. That is still a real advantage and it is
defensible under audit — which the 12.9× is not.
The more useful reframing is in the gold text. The durable asymmetry is not cost, it is that
DeepGrid has no global price book to protect. Mobileye cannot sell at ₹2.3L in India without
answering for it everywhere else. That argument survives scrutiny and does not require
winning a cost comparison you would lose.
""")

# ── DIVIDER 03 ──────────────────────────────────────────────────────────────
s = d.slide()
divider(s, "03", "Who to sell to", "Two tracks, and what each can actually prove")
page(s, dark=True)
notes(s, "Third movement — targets and positioning.")

# ── WHAT WE SELL ────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Sell a certified function, not a chip and not a bundle",
         "The single most useful pricing change in this deck")
photo(s, "module-m2", d.M, Inches(1.86), Inches(2.9), Inches(1.8))
photo(s, "compute-box", Inches(3.68), Inches(1.86), Inches(2.9), Inches(1.8))
photo(s, "detection", Inches(6.86), Inches(1.86), Inches(2.9), Inches(1.8))
photo(s, "truck", Inches(10.04), Inches(1.86), Inches(2.69), Inches(1.8))
rows = [
    ["Certified AEBS (AIS-162)", "Radar + brake actuation + proving-ground homologation",
     "A ₹30k camera box cannot do this", "PRICE IT"],
    ["Driver monitoring (DMS)", "In-cabin perception, AIS-184 addressable",
     "Hard to fake; fleet-relevant", "PRICE IT"],
    ["LDW / BSD / warnings", "Warning-only functions",
     "Exactly what the cheap box approximates", "RIDE FREE"],
]
table(s, ["Function", "What it is", "Why it prices", "Action"], rows, d.M, Inches(3.90),
      d.CW, col_w=[Inches(3.0), Inches(4.4), Inches(3.4), Inches(1.33)], highlight={0, 1},
      row_h=Inches(0.56), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(5.88), d.CW, Inches(0.75), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(5.88), Inches(0.06), Inches(0.75), b.GOLD)
d.text(s, "Quote certified AEBS and DMS by function and let the warnings ride free. Sell the "
          "bundle and the buyer compares your ₹2.3L to a ₹30,000 box on the box's terms — a "
          "comparison you lose on their ground.",
       d.M + Inches(0.25), Inches(6.04), d.CW - Inches(0.5), Inches(0.5),
       size=12, color=b.INK, shrink=True)
page(s)
notes(s, """
This is the most actionable change in the rebuild and it came from the economist lens.
Neither DeepGrid document prices by function. Everything is quoted as a kit, which forces a
bundle-versus-box comparison the cheap box wins on price.
Split it. AEBS is the function that requires radar, brake actuation and proving-ground
homologation — a ₹30,000 camera cannot deliver it at any price. Driver monitoring is
similarly hard to approximate. Those two carry the price.
The warning functions are what the cheap box does adequately. Giving them away costs nothing
and removes the buyer's strongest comparison.
""")

# ── ICP ─────────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Two segments to work now; the rest wait on things you do not hold",
         "Prioritised by what each buyer requires you to already have")
rows = [
    ["Government / PSU / defence", "Foreign silicon excluded; GeM access proven",
     "Eligibility, not certification", "NOW"],
    ["Plant and yard operators", "Private land — no homologation gate at all",
     "A working demo and a site reference", "NOW"],
    ["Large organised fleets (50+)", "Real safety P&L and a single decision-maker",
     "Certified AEBS — not held until 2027", "VALIDATE"],
    ["OEM / Tier-1 line-fit", "One relationship covers thousands of vehicles",
     "Homologation + a relationship you do not have", "START, CLOSES LATE"],
    ["3PL / freight aggregators", "Aggregate small operators into one contract",
     "Price leverage you cannot yet absorb", "LATER"],
    ["Sub-five-truck operators", "~3.5M operators, no purchasing process",
     "A cheaper SKU that does not exist", "NOT ADDRESSABLE"],
]
table(s, ["Segment", "Why it is addressable", "What it requires you to hold", "Priority"],
      rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(2.9), Inches(3.9), Inches(3.6), Inches(1.73)], highlight={0, 1},
      row_h=Inches(0.56), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(5.45), d.CW, Inches(0.85), b.NAVY, radius=0.04)
d.text(s, "The two green rows are the only segments that need nothing you do not already "
          "have. Everything else is gated on certification, an OEM relationship, or a product "
          "that has not been specified.",
       d.M + Inches(0.25), Inches(5.63), d.CW - Inches(0.5), Inches(0.5),
       size=12.5, color=b.WHITE, bold=True, shrink=True)
page(s)
notes(s, """
The prioritisation test is deliberately narrow: what does this buyer require us to already
hold?
Government and yard operators require eligibility and a working demonstration. Both exist.
Everything else requires certified AEBS, which arrives with the 2027 rule, or an OEM
relationship that BP-1A concedes does not exist.
Start the OEM conversations now anyway — the historian's evidence puts fabless-to-design-in at
five to eight years, with two to three years of relationship before the design-in. It will
never be too early; it can easily be too late.
""")

# ── TRACK A ─────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Track A — real eligibility, but no programme identified yet",
         "Primary track · the gap is pipeline, not proposition")
d.rect(s, d.M, Inches(1.82), Inches(7.4), Inches(1.25), b.NAVY, radius=0.04)
d.text(s, "POSITIONING STATEMENT", d.M + Inches(0.25), Inches(1.96), Inches(4), Inches(0.28),
       size=10.5, color=b.TEAL, bold=True)
d.text(s, "“For sovereign UGV, border-surveillance and port-AGV programmes where data cannot "
          "leave Indian soil, DGrid Alpha is an Indian-designed combo-die whose on-die HSM "
          "makes data exfiltration physically impossible — running today on FPGA.”",
       d.M + Inches(0.25), Inches(2.26), Inches(6.9), Inches(0.7), size=12.5,
       color=b.WHITE, italic=True, shrink=True)
photo(s, "robots", Inches(8.15), Inches(1.82), Inches(4.58), Inches(1.25))
cards(s, [
    ("What is genuinely strong",
     "Procurement eligibility is real and demonstrated on GeM. On-die HSM is a physical "
     "property, not a policy promise. Private-land and defence deployments need no AIS "
     "certification, so the 2027 clock does not gate this track."),
    ("What is missing — and it is the binding constraint",
     "No defence champion is identified in any document, and no systems-integrator partner "
     "exists for ports. Real UGV procurement runs QR → RFI → RFP → seasonal field trials → "
     "CNC, which is multi-year, not multi-quarter."),
    ("Revised kill criterion",
     "The original — a second signed contract by Month 6 — is not reachable through a "
     "genuine defence cycle. Replace with: a **named programme and a named SI partner** "
     "identified by Month 3, or Track A is a services business, not a silicon one."),
], Inches(3.30), cols=3, height=Inches(2.55))
page(s)
notes(s, """
Track A survives the verification better than anything else in the strategy, but its weakness
moved.
The proposition is sound: eligibility is real, the HSM argument is physical, and neither
certification nor the tapeout gates this track.
What the practitioner lens found is that there is no pipeline. No named defence programme, no
SI partner for ports. A UGV procurement cycle is multi-year, so the original Month-6
second-contract test could realistically only be met by taking more non-silicon services work
— which is how the ₹1 Cr came to be robotics training in the first place.
Hence the revised criterion: name the programme and the partner by Month 3. That is
achievable and it tests the right thing.
""")

# ── TRACK B ─────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Track B — the deadline pitch does not work until 2027",
         "Secondary track · re-scope it as certification-led, not deadline-led")
d.rect(s, d.M, Inches(1.82), Inches(7.4), Inches(1.25), b.NAVY_2, radius=0.04)
d.text(s, "POSITIONING STATEMENT · PENDING CERTIFICATION", d.M + Inches(0.25), Inches(1.96),
       Inches(5.5), Inches(0.28), size=10.5, color=b.GOLD, bold=True)
d.text(s, "“For N2/N3 fleet operators preparing for the 1 Oct 2027 AEBS requirement, DeepGrid "
          "is building an India-certified AEBS + DMS system at a fraction of imported cost — "
          "seeking design partners for 2026 pilots.”",
       d.M + Inches(0.25), Inches(2.26), Inches(6.9), Inches(0.7), size=12.5,
       color=b.WHITE, italic=True, shrink=True)
photo(s, "radar-viz", Inches(8.15), Inches(1.82), Inches(4.58), Inches(1.25))
cards(s, [
    ("Why the old statement fails now",
     "It sold urgency against a 2026 deadline that does not exist, and “roughly 1/3 the "
     "imported price” invites the ₹30,000 comparison. Neither survives contact with a "
     "buyer who has read the actual rule."),
    ("What replaces it",
     "Design-partner framing, not vendor framing. You are not selling compliance in 2026 — "
     "you are recruiting fleets who want influence over a product that must be certified "
     "for them by 2027."),
    ("Revised kill criterion",
     "Not “one paid pilot in 90 days” — a pilot at ₹1.27L FPGA COGS is contribution-"
     "negative anyway. Instead: **two design partners who commit fleet access and a "
     "measurement baseline** by Month 4."),
], Inches(3.30), cols=3, height=Inches(2.55))
page(s)
notes(s, """
Track B needed the biggest rethink, because its entire urgency argument rested on the wrong
date.
Selling compliance in 2026 against a 2027 rule makes you look either uninformed or
opportunistic, and a fleet operator who has read the notification will know.
Design-partner framing is more honest and, in this window, more effective: you are asking for
fleet access and a measurement baseline in exchange for influence over a product they will be
legally required to buy in eighteen months. That is a real trade.
It also fixes the pilot economics problem — a design partnership does not require you to sell
a contribution-negative FPGA unit to prove intent.
""")

# ── DIVIDER 04 ──────────────────────────────────────────────────────────────
s = d.slide()
divider(s, "04", "Competition and channel", "Who else is moving, and what the channel costs")
page(s, dark=True)
notes(s, "Fourth movement — competitive reality and route to market.")

# ── NETRASEMI ───────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "The nearest Indian peer is ahead of where your deck places them",
         "Corrected — and the caveat matters as much as the correction")
rows = [
    ["Capital", "July deck: ₹125 Cr", "Verified: ₹107 Cr Series A, Jul 2025, Zoho-led", "Deck overstates"],
    ["Timing", "July deck: “ships mid-2027, a year behind us”",
     "Verified: production-ready declared May 2026, 3 OEM trials live", "~12 months wrong, wrong direction"],
    ["Maturity", "Not assessed", "EE Times: EVK / engineering samples, pre-revenue, full mask mid-2027", "Less advanced than the headline"],
    ["Product fit", "Mapped as an ADAS peer", "A2000 is a 12 TOPS edge-AI SoC on 12nm for video analytics", "Adjacent, not equivalent"],
]
table(s, ["Dimension", "What the deck says", "What is verified", "Read"], rows,
      d.M, Inches(1.82), d.CW,
      col_w=[Inches(1.7), Inches(3.5), Inches(4.6), Inches(2.33)], highlight={1},
      row_h=Inches(0.62), left_cols=(0, 1, 2, 3))
d.rect(s, d.M, Inches(4.65), Inches(6.4), Inches(1.6), hx("FDECEE"), radius=0.04)
d.rect(s, d.M, Inches(4.65), Inches(0.06), Inches(1.6), b.CORAL)
d.text(s, "What it actually threatens", d.M + Inches(0.25), Inches(4.82), Inches(5.9),
       Inches(0.3), size=13, color=b.NAVY, bold=True)
d.text(s, "Not a price war — a design-in race lost on timing, in exactly the months 12–18 "
          "certification window. With 4–7× more free capital, they can fund qualification "
          "cycles DeepGrid would have to choose between.",
       d.M + Inches(0.25), Inches(5.16), Inches(5.9), Inches(0.95), size=12,
       color=b.INK, shrink=True)
d.rect(s, Inches(7.25), Inches(4.65), Inches(5.48), Inches(1.6), b.NAVY, radius=0.04)
d.text(s, "What it does not threaten", Inches(7.48), Inches(4.82), Inches(5.0), Inches(0.3),
       size=13, color=b.TEAL, bold=True)
d.text(s, "The A2000 has no AIS certification, no AEC-Q100, and no ISO 26262 claim. It is a "
          "video-analytics SoC with automotive as one target sector. In a sovereign-data or "
          "certified-AEBS conversation it is not a substitute.",
       Inches(7.48), Inches(5.16), Inches(5.0), Inches(0.95), size=12,
       color=b.LIGHT_TEAL, shrink=True)
page(s)
notes(s, """
Two corrections in one slide, pulling in opposite directions.
The deck understates them on timing — they declared production readiness in May 2026, not
mid-2027 — and overstates their capital at ₹125 Cr when it is ₹107 Cr.
But the independent reporting is more sober than the company declaration: engineering samples,
pre-revenue, full mask mid-2027. So they are ahead of where the deck puts them and behind
their own headline.
The right competitive read is the right-hand panel. In the segments Track A targets, an
uncertified video-analytics SoC is not a substitute. The threat is not this quarter's deal —
it is the design-in race in the certification window.
""")

# ── CHANNEL ─────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "The channel is unaffordable before the tapeout",
         "Dealer and insurer economics, modelled on the plan's own numbers")
rows = [
    ["Dealer margin, ASIC phase", "20% cut leaves ~52% GM", "Workable"],
    ["Dealer margin, FPGA phase", "20% cut collapses GM 45% → 25%", "Opex-covering volume rises 400–600 → ~690–1,030 kits"],
    ["FY27 plan volume", "130 kits", "Roughly 5–8× short of that break-even"],
    ["Dealer working capital", "~₹37,000 carry on ten kits", "≈80% of one unit's margin — unaddressed"],
    ["Insurer subsidy that actually works", "20–30%, not 50%", "₹40,000–70,000 → kit at ₹1.6–1.9L"],
]
table(s, ["Line", "Value", "Consequence"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(3.5), Inches(3.4), Inches(5.23)], highlight={1, 4},
      row_h=Inches(0.50), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(4.60), Inches(6.4), Inches(1.7), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(4.60), Inches(0.06), Inches(1.7), b.GOLD)
d.text(s, "Do not recruit dealers yet", d.M + Inches(0.25), Inches(4.78), Inches(5.9),
       Inches(0.3), size=13, color=b.NAVY, bold=True)
d.text(s, "At FPGA-phase economics a 20% dealer cut makes the unit uneconomic, and the plan's "
          "FY27 volume is far below the volume that cut would require. Sell direct through "
          "2026–27 and build the channel when ASIC economics arrive.",
       d.M + Inches(0.25), Inches(5.12), Inches(5.9), Inches(1.05), size=12,
       color=b.INK, shrink=True)
d.rect(s, Inches(7.25), Inches(4.60), Inches(5.48), Inches(1.7), b.NAVY, radius=0.04)
d.text(s, "The insurer contradiction to resolve", Inches(7.48), Inches(4.78), Inches(5.0),
       Inches(0.3), size=13, color=b.TEAL, bold=True)
d.text(s, "BP-1A makes insurer co-funding a primary engine; the July deck bans insurer "
          "selling outright. Both cannot stand. And at a workable 20–30% the subsidy is a "
          "margin instrument — it does not bridge to the ₹30,000 anchor as BP-1A assumes.",
       Inches(7.48), Inches(5.12), Inches(5.0), Inches(1.05), size=12,
       color=b.LIGHT_TEAL, shrink=True)
page(s)
notes(s, """
The channel model needs sequencing, not abandoning.
The arithmetic is stark: at FPGA-phase margins a normal dealer cut takes the unit
contribution-negative, and the volume required to absorb it is five to eight times the FY27
plan. Recruiting dealers now would mean signing partners you cannot pay properly.
Sell direct through the FPGA phase. It is slower and it is the only affordable option.
The insurer point needs a decision from the founders rather than a salesperson working around
it — the two documents give opposite instructions, and at realistic subsidy levels the
mechanism improves margin rather than solving the price gap.
""")

# ── DIVIDER 05 ──────────────────────────────────────────────────────────────
s = d.slide()
divider(s, "05", "The next 90 days", "Sequenced against a 2027 wall, not a 2026 one")
page(s, dark=True)
notes(s, "Fifth movement — execution.")

# ── 90 DAYS ─────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "The next 90 days", "Claim remediation first — it gates everything else")
rows = [
    ["1", "Withdraw the June IM; retire the nine claims across all collateral", "Week 1", "Six of nine live in that document"],
    ["2", "Publish an approved-claims one-pager for anyone client-facing", "Week 2", "Nobody sells until this exists"],
    ["3", "Name a defence programme and an SI partner for ports", "Weeks 1–12", "Track A's binding constraint"],
    ["4", "Recruit two fleet design partners (access + baseline)", "Weeks 2–16", "Replaces the paid-pilot test"],
    ["5", "Publish a power / thermal envelope", "Weeks 2–6", "First question any integrator asks"],
    ["6", "Decide the insurer question — engine or excluded", "Week 4", "The two documents contradict each other"],
    ["7", "Re-price by function: AEBS + DMS carry, warnings ride free", "Weeks 3–8", "Removes the ₹30k comparison"],
    ["8", "Reconcile die area (57.1 vs 20 mm²) and reissue the cost build", "Weeks 4–10", "The $3.876 rests on the smaller figure"],
]
table(s, ["#", "Action", "When", "Why"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(0.55), Inches(6.0), Inches(1.7), Inches(4.43)], highlight={0, 1},
      row_h=Inches(0.50), left_cols=(0, 1, 3))
d.rect(s, d.M, Inches(6.10), d.CW, Inches(0.62), b.NAVY, radius=0.04)
d.text(s, "Items 1 and 2 gate everything below them. No client-facing activity until the "
          "approved-claims sheet exists.",
       d.M + Inches(0.25), Inches(6.24), d.CW - Inches(0.5), Inches(0.36),
       size=12.5, color=b.WHITE, bold=True, shrink=True)
page(s)
notes(s, """
The sequencing changed because the timing changed. With the wall in late 2027 there is no
reason to rush into buyer meetings with a claim set that will not survive them.
Items one and two are cheap and they gate the rest. An approved-claims one-pager is an
afternoon's work and it is the difference between a salesperson who is trusted and one who is
corrected in the room.
Item five is the quiet one. No document states a power envelope, and for an M.2 module in a
truck cabin that is the first thing a serious integrator asks. Not having an answer reads as
inexperience regardless of how good the silicon is.
""")

# ── CLOSE ───────────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "What would change this strategy", "Triggers, and what each one means")
rows = [
    ["No named defence programme by Month 3", "Track A is services, not silicon", "Revised — the original Month-6 test was unreachable"],
    ["No two design partners by Month 4", "Track B has no 2027 path", "Replaces the paid-pilot criterion"],
    ["AIS certification slips past mid-2027", "You miss the wall you now have time for", "The 18-month gift is spent"],
    ["Netrasemi announces a certified automotive part", "The differentiated position closes", "Watch quarterly"],
    ["Enforcement slips as AIS-140 did", "Revenue moves right again — plan for it", "8-year precedent, same ministry"],
]
table(s, ["Trigger", "What it means", "Note"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(4.3), Inches(4.0), Inches(3.83)], highlight={0, 1},
      row_h=Inches(0.56), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(4.90), d.CW, Inches(1.35), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(4.90), Inches(0.06), Inches(1.35), b.GOLD)
d.text(s, "The one-line summary", d.M + Inches(0.25), Inches(5.08), Inches(6), Inches(0.3),
       size=13, color=b.NAVY, bold=True)
d.text(s, "You have until late 2027, not late 2026 — and the binding constraint is not time or "
          "product, it is that the current claim set cannot survive a technical buyer. Retire "
          "the nine claims, sell Track A on eligibility while naming a real programme, and "
          "recruit fleet design partners against the 2027 rule rather than a deadline that "
          "does not exist.",
       d.M + Inches(0.25), Inches(5.42), d.CW - Inches(0.5), Inches(0.72),
       size=12.5, color=b.INK, shrink=True)
page(s)
notes(s, """
Close on triggers, and on the honest summary.
The first two are revised from the July deck because verification showed the original tests
were either unreachable or measuring the wrong thing.
The last one is the sleeper. AIS-140 took eight years from notification to broad enforcement,
gated on state backend readiness rather than on suppliers. The same ministry is behind this
rule. Build a plan that survives the dates moving right, because on the domestic precedent
that is the base case rather than the pessimistic one.
""")

out = OUT / "DeepGrid-client-acquisition-v2-draft.pptx"
d.save(out, validate=True)
print(f"slides: {d.n}")
