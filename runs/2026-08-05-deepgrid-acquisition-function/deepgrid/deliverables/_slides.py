# ── COVER ───────────────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)
bg = ASSET / "harvested" / "deck_image1.png"
if bg.exists():
    s.shapes.add_picture(str(bg), 0, 0, d.W, d.H)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.text(s, "CLIENT ACQUISITION OPERATING SYSTEM", Inches(0.85), Inches(1.80),
       Inches(9.0), Inches(0.4), size=13, color=b.TEAL, bold=True)
d.text(s, "How DeepGrid wins clients", Inches(0.85), Inches(2.30), Inches(8.6),
       Inches(1.2), size=44, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.rect(s, Inches(0.85), Inches(3.75), Inches(1.6), Inches(0.05), b.TEAL)
d.text(s, "Who we sell to, what we sell, what we may claim, and how a lead travels — "
          "built as files the team and the tooling both read",
       Inches(0.85), Inches(4.05), Inches(9.2), Inches(0.75), size=15,
       color=b.LIGHT_TEAL, shrink=True)
for i, chip in enumerate(["2 segments now", "price by function",
                          "9 claims retired", "1 lead state machine"]):
    x = Inches(0.85) + i * Inches(2.6)
    d.rect(s, x, Inches(5.30), Inches(2.45), Inches(0.44), b.NAVY_2, radius=0.25, line=b.ACCENT)
    d.text(s, chip, x, Inches(5.42), Inches(2.45), Inches(0.26), size=10,
           color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER)
page(s, dark=True)
notes(s, """
This deck documents an operating system, not a strategy opinion. Everything in it is written
into six context files that sit in the run folder — the deck is the readable version, the
files are what actually removes work.
The test that matters is not whether this deck is persuasive. It is whether a cold session,
given only those six files, produces outbound a founder would send.
""")

# ── THE SYSTEM ──────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "The acquisition system is six files, not a playbook",
         "Level 3 of a ten-level ladder — the level everything above inherits from")
rows = [
    ["01-offer.md", "What we sell, how it is priced, what is excluded", "Founder approval on pricing"],
    ["02-icp.md", "Who buys, who does not, and the prioritisation test", "Ready"],
    ["03-voice.md", "How we write, and the banned-words list", "**Blocked** — needs six real samples"],
    ["04-proof.md", "Every claim we may make, with evidence state", "Founder approval on claimable set"],
    ["05-objections.md", "Ten objections and the honest answer to each", "Replace after 10 real calls"],
    ["06-process.md", "Lead states, stages, owners, approval gates", "Ready"],
]
table(s, ["File", "What it carries", "Status"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(2.6), Inches(6.4), Inches(3.13)], highlight={2},
      row_h=Inches(0.50), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(5.10), Inches(6.4), Inches(1.5), b.NAVY, radius=0.04)
d.text(s, "Why files and not a document", d.M + Inches(0.22), Inches(5.28), Inches(5.9),
       Inches(0.32), size=14, color=b.TEAL, bold=True)
d.text(s, "Today every outbound message requires a human to reconcile four documents that "
          "disagree, and to remember which claims were retired. Files move that from a "
          "per-message task to a one-time write — and any tooling reads the same source the "
          "team does.",
       d.M + Inches(0.22), Inches(5.66), Inches(5.9), Inches(0.85), size=12,
       color=b.LIGHT_TEAL, shrink=True)
d.rect(s, Inches(7.25), Inches(5.10), Inches(5.48), Inches(1.5), hx("FFF4D6"), radius=0.04)
d.rect(s, Inches(7.25), Inches(5.10), Inches(0.06), Inches(1.5), b.GOLD)
d.text(s, "The gate this must pass", Inches(7.48), Inches(5.28), Inches(5.0), Inches(0.32),
       size=14, color=b.NAVY, bold=True)
d.text(s, "A cold session, given only these six files and no other context, writes an "
          "outbound email to a port operator that a founder would send with light edits — "
          "and refuses any claim absent from 04-proof.md.",
       Inches(7.48), Inches(5.66), Inches(5.0), Inches(0.85), size=12,
       color=b.INK, shrink=True)
page(s)
notes(s, """
The framework this comes from is explicit that a deliverable which removes no work from
someone's calendar is a toy. So the deliverable is the files; this slide is the map.
Note the blocked row. Voice cannot be invented — it needs three real emails and three real
posts a founder actually wrote. Inventing one would produce the model's default voice, which
is the exact failure Level 3 exists to fix.
""")

# ── WHO WE SELL TO ──────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Two segments now — the ones needing nothing we do not hold",
         "From 02-icp.md · the prioritisation test is what the buyer requires us to already have")
rows = [
    ["Government / PSU / defence", "Foreign silicon excluded by rule; GeM access proven",
     "Eligibility, not certification", "NOW"],
    ["Plant, yard and port operators", "Private land — no homologation gate at all",
     "A working demo and a site reference", "NOW"],
    ["Large organised fleets (50+)", "Real safety P&L, single decision-maker",
     "Certified AEBS — not held until 2027", "DESIGN PARTNER"],
    ["OEM / Tier-1 line-fit", "One relationship covers thousands of vehicles",
     "Homologation + a relationship we lack", "START NOW, CLOSES LATE"],
]
table(s, ["Segment", "Why it is addressable", "What it requires us to hold", "Priority"],
      rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(3.0), Inches(3.8), Inches(3.5), Inches(1.83)], highlight={0, 1},
      row_h=Inches(0.56), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(4.35), d.CW, Inches(1.9), hx("FDECEE"), radius=0.04)
d.rect(s, d.M, Inches(4.35), Inches(0.06), Inches(1.9), b.CORAL)
d.text(s, "Disqualifiers — these matter more than the qualifiers",
       d.M + Inches(0.25), Inches(4.53), Inches(8), Inches(0.32), size=14,
       color=b.NAVY, bold=True)
d.text(s, [
    {"text": "Sub-five-truck operators (~3.5M). No purchasing process, price anchored at "
             "₹4,500–11,000. Not addressable directly at any sane cost.", "size": 11.5,
     "color": b.INK, "bullet": True},
    {"text": "Anyone buying purely to pass inspection — they will buy a ₹15,000–40,000 box "
             "and they are right to.", "size": 11.5, "color": b.INK, "bullet": True,
     "space_before": 6},
    {"text": "Anyone needing certification today, or a quantified insurance outcome. Walk "
             "rather than invent one.", "size": 11.5, "color": b.INK, "bullet": True,
     "space_before": 6},
], d.M + Inches(0.25), Inches(4.92), d.CW - Inches(0.5), Inches(1.2), shrink=True)
page(s)
notes(s, """
The prioritisation rule is deliberately narrow and it is the whole slide: what does this
buyer require us to already hold?
Government and yard operators require eligibility and a demo. Both exist today. Everything
else waits on certification or a relationship we do not have.
The red panel is the half most ICP work omits. Knowing who wastes your time saves more weeks
than knowing who to target, and the third bullet is a discipline point — walking away from a
buyer who needs a number we cannot evidence is cheaper than inventing it.
""")

# ── WHAT WE SELL ────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Price the function, give away the warnings",
         "From 01-offer.md · the pricing change that removes the buyer's best objection")
photo(s, "module-m2", d.M, Inches(1.86), Inches(2.9), Inches(1.75))
photo(s, "compute-box", Inches(3.68), Inches(1.86), Inches(2.9), Inches(1.75))
photo(s, "detection", Inches(6.86), Inches(1.86), Inches(2.9), Inches(1.75))
photo(s, "truck", Inches(10.04), Inches(1.86), Inches(2.69), Inches(1.75))
rows = [
    ["Certified AEBS (AIS-162)", "Radar, brake actuation, proving-ground homologation",
     "A ₹30k camera box cannot do this at any price", "PRICE IT"],
    ["Driver monitoring (DMS)", "In-cabin perception, AIS-184 addressable",
     "Hard to approximate; fleet-relevant", "PRICE IT"],
    ["LDW / BSD / warnings", "Warning-only functions",
     "Exactly what the cheap box does adequately", "RIDE FREE"],
]
table(s, ["Function", "What it is", "Why it prices — or does not", "Action"], rows,
      d.M, Inches(3.85), d.CW,
      col_w=[Inches(2.9), Inches(4.0), Inches(4.0), Inches(1.23)], highlight={0, 1},
      row_h=Inches(0.54), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(6.02), d.CW, Inches(0.62), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(6.02), Inches(0.06), Inches(0.62), b.GOLD)
d.text(s, "Sell the bundle and the buyer compares ₹2.3L to ₹30,000 on the box's terms. Sell "
          "the function and the box has no answer. Never open a fleet conversation on price.",
       d.M + Inches(0.25), Inches(6.16), d.CW - Inches(0.5), Inches(0.4),
       size=12, color=b.INK, bold=True, shrink=True)
page(s)
notes(s, """
This is the single most useful change in the whole system and it costs nothing to adopt.
Neither of DeepGrid's plans prices by function — everything is quoted as a kit, which forces
a bundle-versus-box comparison that the cheap box wins.
Split it. AEBS needs radar, brake actuation and homologation; a camera box cannot deliver it
regardless of price. Driver monitoring is similarly hard to fake. Those two carry the price.
The warning functions are what the cheap box does fine. Giving them away removes the buyer's
strongest comparison and costs no margin that was ever winnable.
""")

# ── WHAT WE MAY CLAIM ───────────────────────────────────────────────────────
s = d.slide()
d.header(s, "What we may claim — and the nine claims now retired",
         "From 04-proof.md · this file is the ceiling on every claim the system may make")
d.text(s, "May be claimed", d.M, Inches(1.80), Inches(6.2), Inches(0.3),
       size=13, color=b.NAVY, bold=True)
table(s, ["Claim", "State"], [
    ["GeM procurement record held", "CONTRACTED"],
    ["₹23.01L delivered — Robot Training", "CONTRACTED*"],
    ["YOLOv11n at 40 fps on FPGA", "MEASURED"],
    ["Attention head at 24.25 ms", "MEASURED"],
    ["DGS001 running on FPGA", "SILICON"],
    ["15 provisional patents filed", "FILED"],
], d.M, Inches(2.14), Inches(6.2), col_w=[Inches(4.5), Inches(1.7)],
    highlight={0, 2, 3}, row_h=Inches(0.42), left_cols=(0,))
d.text(s, "* sits in Deepgrid Datacentre, not Semi. IP is MCEME-owned. Not ADAS revenue — "
          "this caveat must always travel with it.",
       d.M, Inches(5.05), Inches(6.2), Inches(0.5), size=10, color=b.MUTED,
       italic=True, shrink=True)
d.text(s, "Retired — never say", Inches(7.05), Inches(1.80), Inches(5.68), Inches(0.3),
       size=13, color=b.NAVY, bold=True)
table(s, ["Retired claim", "Why"], [
    ["“39.3 TOPS measured”", "Artix-7 ceilings ~1.8 TOPS"],
    ["“84% / 88% gross margin”", "Retracted; blend needs 120%"],
    ["“12.9× cheaper”", "Their ASP vs our die cost"],
    ["“₹1 Cr defence revenue”", "₹23.01L; rest is L1"],
    ["“Transformer VLA on-chip”", "Bandwidth-bound"],
    ["“Mandate live since Apr 2026”", "That rule was a draft"],
    ["“Mandate-ready” · “ASIL-D”", "Neither is held"],
    ["Any insurance / accident %", "No baseline, no actuary"],
], Inches(7.05), Inches(2.14), Inches(5.68), col_w=[Inches(3.1), Inches(2.58)],
    row_h=Inches(0.42), left_cols=(0, 1))
page(s)
notes(s, """
This is the page that protects the business, and it belongs in front of anyone client-facing
before their first meeting.
The left column is short on purpose. Two contracted items, two measured numbers, one live
demo, one filing. That is a real and defensible position for a company at this stage — and
far stronger than a longer list that collapses on inspection.
The right column exists because every one of those claims is disprovable by a competent
evaluator in a single meeting. Being caught once costs the credibility of everything else in
the room, including the true things on the left.
""")

# ── HOW A LEAD TRAVELS ──────────────────────────────────────────────────────
s = d.slide()
d.header(s, "One intake path, one state machine, one record per lead",
         "From 06-process.md · this is the foundation everything automated sits on")
states = ["new", "researched", "contacted", "replied", "booked", "proposed", "won / lost / dead"]
w = (d.CW - Inches(0.36)) / len(states)
for i, st in enumerate(states):
    x = d.M + i * (w + Inches(0.06))
    fill = b.ACCENT if i < 6 else b.NAVY
    d.rect(s, x, Inches(1.90), w, Inches(0.62), fill, radius=0.06)
    d.text(s, st, x, Inches(2.06), w, Inches(0.3), size=10.5, color=b.WHITE,
           bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, "Every lead enters the same way regardless of source — referral, inbound, event, "
          "cold, GeM tender alert. Same record shape, same first step. Multiple intake paths "
          "is the most common reason these systems collapse.",
       d.M, Inches(2.68), d.CW, Inches(0.5), size=11.5, color=b.MUTED, shrink=True)
rows = [
    ["1–2", "Source and qualify", "Commercial lead", "Passes ICP; disqualifiers cleared"],
    ["3", "Research", "Commercial lead", "Buying trigger found, or “none found” recorded"],
    ["4–5", "Contact and discovery", "Commercial lead", "Requirement, timeline, decision unit"],
    ["6", "Technical review", "CTO", "Their evaluator has seen demo and proof kit"],
    ["7–8", "Proposal and close", "Commercial + founder", "Priced by function; founder approved"],
    ["9", "Deploy", "Engineering", "Installed; baseline measurement started"],
]
table(s, ["Stage", "What happens", "Owner", "Exit criterion"], rows, d.M, Inches(3.32),
      d.CW, col_w=[Inches(0.9), Inches(3.4), Inches(2.6), Inches(5.23)],
      row_h=Inches(0.46), left_cols=(0, 1, 2, 3))
d.rect(s, d.M, Inches(6.20), d.CW, Inches(0.55), hx("FDECEE"), radius=0.04)
d.rect(s, d.M, Inches(6.20), Inches(0.06), Inches(0.55), b.CORAL)
d.text(s, "Human approval, not negotiable: anything sent to a client · any price · any "
          "contract · any claim not in 04-proof.md · any lead scoring above 9.",
       d.M + Inches(0.25), Inches(6.33), d.CW - Inches(0.5), Inches(0.32),
       size=11.5, color=b.INK, bold=True, shrink=True)
page(s)
notes(s, """
The state machine looks trivial and is the thing most acquisition systems get wrong.
One record, one state, one store. If two people — or later, two agents — disagree about
where a lead is, the store is broken and no amount of process fixes it.
One intake path matters just as much. The temptation is to handle referrals differently from
cold leads because referrals feel special. That is exactly how the record shape diverges and
the pipeline stops being countable.
The approval line at the bottom is written down in advance deliberately, so it is never a
judgement call in the moment.
""")

# ── THE LADDER ──────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "Where this goes next — and what must not be skipped",
         "The ten-level ladder · we are building Level 3")
rows = [
    ["1–2", "Saved prompt, chain", "Trivial once the Brain exists", "After L3"],
    ["3", "The Brain — six context files", "Removes per-message reconciliation", "**BUILDING NOW**"],
    ["4", "Packaged skills", "A job runs identically whoever runs it", "Next"],
    ["5", "Deliverable machine", "Proposal in minutes from call notes", "Next"],
    ["6", "Connections — inbox, calendar, CRM", "**Blocked: no CRM or shared store exists**", "Blocked"],
    ["7–8", "Agent, then Scout/Writer/Closer/Auditor", "Volume without quality collapse", "Later"],
    ["9–10", "Scheduled, then the full function", "Pipeline moves on days nobody works", "Later"],
]
table(s, ["Level", "What it is", "What it removes", "Status"], rows, d.M, Inches(1.82),
      d.CW, col_w=[Inches(1.0), Inches(4.3), Inches(5.2), Inches(1.63)], highlight={1},
      row_h=Inches(0.50), left_cols=(0, 1, 2))
d.rect(s, d.M, Inches(5.50), d.CW, Inches(1.15), b.NAVY, radius=0.04)
d.text(s, "The rule that governs the whole ladder", d.M + Inches(0.25), Inches(5.68),
       Inches(7), Inches(0.32), size=14, color=b.TEAL, bold=True)
d.text(s, "Do not skip levels — Level 7 built on a broken Level 3 is just a faster mess. And "
          "every level must remove a task from somebody's calendar. If it does not, it is a "
          "toy and should be deleted. That test is why this system is files rather than a "
          "strategy document.",
       d.M + Inches(0.25), Inches(6.04), d.CW - Inches(0.5), Inches(0.5),
       size=12.5, color=b.LIGHT_TEAL, shrink=True)
page(s)
notes(s, """
The ladder matters because the instinct is always to jump to agents and schedules, which is
where the visible magic is.
Level 6 is genuinely blocked and worth naming: there is no CRM or shared store, so there is
nowhere for a connected system to read and write. That is a prerequisite purchase or build,
not something to work around.
The rule in the navy band is the one I would hold everyone to, including me. It is the test
that distinguishes a working system from a deck about a system.
""")

# ── NEXT STEPS ──────────────────────────────────────────────────────────────
s = d.slide()
d.header(s, "What happens next", "Three of these need a founder, not a commercial lead")
rows = [
    ["1", "Founder supplies six real writing samples", "Founder", "This week", "03-voice.md is blocked without them"],
    ["2", "Founder approves the claimable set in 04-proof.md", "Founder", "This week", "Nothing goes out until this is signed"],
    ["3", "Founder approves pricing in 01-offer.md", "Founder", "This week", "Price-by-function is a commitment, not a description"],
    ["4", "Run the cold-chat gate test", "Commercial lead", "Week 2", "Pass or the files are too thin"],
    ["5", "Withdraw the June IM from circulation", "Founder", "Immediately", "It carries six retired claims"],
    ["6", "Name a defence programme and an SI partner", "Commercial lead", "Weeks 1–12", "Track A has a proposition and no pipeline"],
    ["7", "Choose a CRM or shared store", "Founder", "Month 2", "Unblocks Level 6 and everything above"],
    ["8", "Replace drafted objections with real call wording", "Commercial lead", "After 10 calls", "Imagined objections are the weakest file"],
]
table(s, ["#", "Action", "Owner", "When", "Why"], rows, d.M, Inches(1.82), d.CW,
      col_w=[Inches(0.55), Inches(4.6), Inches(2.1), Inches(1.6), Inches(3.28)],
      highlight={0, 1, 2}, row_h=Inches(0.50), left_cols=(0, 1, 4))
d.rect(s, d.M, Inches(6.10), d.CW, Inches(0.62), hx("FFF4D6"), radius=0.04)
d.rect(s, d.M, Inches(6.10), Inches(0.06), Inches(0.62), b.GOLD)
d.text(s, "Items 1–3 are founder decisions and they gate everything else. None takes more "
          "than an hour; all three are commitments rather than descriptions.",
       d.M + Inches(0.25), Inches(6.24), d.CW - Inches(0.5), Inches(0.4),
       size=12, color=b.INK, bold=True, shrink=True)
page(s)
notes(s, """
Three of the eight need a founder specifically, and they are the three that gate the rest.
Voice samples cannot be delegated or invented. The claimable set is a commitment about what
the company will assert publicly. Pricing by function is a real pricing decision, not a
presentation choice.
Item five costs nothing and should happen today — the June IM is the most polished document
in the set and carries six claims that have been retired.
Item eight is the honest weakness in what has been built: the objection responses are drafted
from verified evidence rather than taken from real conversations, which is the opposite of
what the framework asks for. They are a starting point to be replaced, not a finished file.
""")

out = OUT / "DeepGrid-client-acquisition-system-draft.pptx"
d.save(out, validate=True)
print(f"slides: {d.n}")
