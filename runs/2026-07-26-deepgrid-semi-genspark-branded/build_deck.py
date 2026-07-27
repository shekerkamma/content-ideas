#!/usr/bin/env python3
"""build_deck.py — emit deck.html for the DeepGrid Semi Pre-Series A deck.

Applies template.css (structure) + theme.css (identity) to a slide spec.
Every band is absolutely positioned with an explicit top/height so each text
node gets a generous bounding box — that is what keeps the exported native
PowerPoint text boxes from re-wrapping relative to the HTML.

  python3 build_deck.py --out deck.html
"""
import argparse, html, pathlib

RIGHT_RAIL = "DEEPGRID SEMI · PRE-SERIES A"
DISCLAIMER = "Not an offer to sell securities · For discussion only"

# ----------------------------------------------------------------- emitters

def _cards(n, items, top=None, height=None, extra=""):
    out = [f'<div class="band n{n}" style="{extra}">']
    for it in items:
        cls = "card" + (" " + it["v"] if it.get("v") else "")
        out.append(f'<div class="{cls}">')
        if it.get("k"):   out.append(f'<div class="k">{it["k"]}</div>')
        if it.get("h"):   out.append(f'<div class="h">{it["h"]}</div>')
        if it.get("big"): out.append(f'<div class="big {it.get("bigv","")}">{it["big"]}</div>')
        if it.get("p"):   out.append(f'<div class="p">{it["p"]}</div>')
        out.append("</div>")
    out.append("</div>")
    return "\n".join(out)


def _chain(nodes, top=None, height=None):
    out = ['<div class="chain">']
    for i, it in enumerate(nodes):
        if i:
            out.append('<div class="arrow"></div>')
        cls = "card" + (" " + it["v"] if it.get("v") else "")
        out.append(f'<div class="{cls}">')
        out.append(f'<div class="k">{it["k"]}</div><div class="h">{it["h"]}</div><div class="p">{it["p"]}</div>')
        out.append("</div>")
    out.append("</div>")
    return "\n".join(out)


def _rows(items, top=None):
    out = ['<div class="rows">']
    for it in items:
        hi = " hi" if it.get("hi") else ""
        out.append(f'<div class="row{hi}"><div class="rl">{it["l"]}</div>'
                   f'<div class="rv {it.get("vc","c")}">{it["v"]}</div>'
                   f'<div class="rw">{it["w"]}</div></div>')
    out.append("</div>")
    return "\n".join(out)


def _split(specs, blocks, top=None):
    out = ['<div class="split">', '<div class="spec">']
    for s in specs:
        out.append(f'<div class="si"><div class="k">{s["k"]}</div><div class="v">{s["v"]}</div></div>')
    out.append('</div><div class="tblock">')
    for b in blocks:
        out.append(f'<div class="tb {b["v"]}"><div class="k">{b["k"]}</div><div class="p">{b["p"]}</div></div>')
    out.append("</div></div>")
    return "\n".join(out)


def _kpi(items, top=None, height=190):
    cls = "kpi abs" if top is not None else "kpi"
    st = f'style="top:{top}px;height:{height}px"' if top is not None else ""
    out = [f'<div class="{cls}" {st}>']
    for it in items:
        cls = ' class="decide"' if it.get("decide") else ""
        out.append(f'<div{cls}><div class="k">{it["k"]}</div><div class="v">{it["v"]}</div>'
                   f'<div class="n">{it["n"]}</div></div>')
    out.append("</div>")
    return "\n".join(out)


def _callout(c, top=None):
    return ('<div class="callout">'
            f'<div class="cond">{c["cond"]}</div>'
            f'<div class="then">{c["then"]}</div>'
            f'<div class="not">{c["not"]}</div></div>')


def _bars(b, top=None):
    return f'''<div class="bars">
<div class="bcol"><div class="bar"><div class="fill a" style="height:{b['a_h']}%"><span class="pct">{b['a_v']}</span></div></div><div class="bcap"><b>{b['a_t']}</b><br>{b['a_s']}</div></div>
<div class="bmid"><div class="bdelta">{b['delta']}</div><div class="bline"></div></div>
<div class="bcol"><div class="bar"><div class="fill c" style="height:{b['b_h']}%"><span class="pct">{b['b_v']}</span></div></div><div class="bcap"><b>{b['b_t']}</b><br>{b['b_s']}</div></div>
<div class="bnote"><p>{b['p1']}</p><p>{b['p2']}</p></div></div>'''


def _srcs(items, top=None):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<ul class="srcs">{lis}</ul>'


def _note(text, top=None, v=""):
    return f'<div class="note {v}">{text}</div>'


# ----------------------------------------------------------------- slides

def slides():
    S = []

    # ===================== SECTION 1 — COMPANY, PROBLEM, SOLUTION =====================

    S.append(dict(kind="cover", label="COVER", body=f'''
<div class="wafer"></div>
<div class="die-1"></div><div class="die-2"></div><div class="die-3"></div>
<div class="die-t">DGRID<br><span>ALPHA / 28nm</span></div>
<div class="brand-l">DEEPGRID · SEMI</div>
<div class="brand-r">PRE-SERIES A · CONFIDENTIAL</div>
<div class="brand-rule"></div>
<div class="eyebrow">Investor + GTM Strategy</div>
<div class="mega">Vertically integrated<br>edge-AI silicon for<br><span class="c">commercial vehicles.</span></div>
<div class="lede">Fabless custom-ASIC combo-die for autonomous and ADAS commercial fleets in India and the GCC.
FPGA-validated architecture, a 28&nbsp;nm ASIC path to a ~$30 board, and an evidence-led go-to-market plan
built to survive contact with buyers.</div>
''' + _kpi([
        dict(k="Blended Ask", v="₹55 Cr", n="₹45 Cr CCPS equity + ₹10 Cr CGTMSE debt (~$4.79M)"),
        dict(k="Primary ICP Score", v="79.2<em>%</em>", n="Tactical Defense &amp; Off-Highway/Port, 3.96/5 weighted"),
        dict(k="Cost Reduction", v="3–7<em>×</em>", n="vs imported ADAS stacks at equivalent function"),
        dict(k="GTM Decision", v="Proceed with<br>Conditions", n="5 conditions, day-90 re-scoring gate", decide=True),
    ], 770, 180)))

    S.append(dict(sec="EXECUTIVE SUMMARY", label="EXEC SUMMARY",
        title='The architecture works. The <span class="r">board economics</span> don\'t.',
        sub="FPGA silicon proved the compute. It also proved the board cost has to come down by two orders of magnitude.",
        body=_cards(4, [
            dict(k="01 · Validated", h="Compute proven", big="39.3", bigv="c",
                 p='TOPS INT8 measured on FPGA. <b>64 × 512</b> MAC lattice, dual-issue at <b>600 MHz</b>.'),
            dict(k="02 · The problem", h="FPGA board cost", big="₹35,000", bigv="r", v="alert",
                 p="Per unit. Uneconomic at any fleet volume — this is why the tapeout is the ask."),
            dict(k="03 · The fix", h="28 nm ASIC die", big="$3.876", bigv="c",
                 p='At <b>1M</b> chips on TSMC 28&nbsp;nm HPC+. Under four dollars, supplier-quoted.'),
            dict(k="04 · Outcome", h="Board BOM", big="~$30", bigv="c", v="accent",
                 p="Once six functions collapse onto one combo-die. The squeeze zone stops being ours."),
        ], 290, 330)
        + _note('A validated architecture on an uneconomic board is a <b>research result, not a product.</b> '
                'The raise converts one into the other.', 660)))

    S.append(dict(sec="CORE PROBLEM", label="CORE PROBLEM", title="The Squeeze Zone.",
        sub="Every pure-play autonomy stack in India inherits merchant-silicon economics — and prices itself out of its own market.",
        body=_chain([
            dict(k="Layer 1 · Software players", h="Pure-Play<br>AI Software",
                 p="Minus Zero, Swaayatt Robots, RoshAI — algorithm-first and hardware-agnostic. Excellent perception IP, but silicon is treated as a black-box commodity."),
            dict(k="Layer 2 · Where value leaks", h="The Squeeze<br>Zone", v="alert",
                 p='Merchant silicon (NVIDIA DRIVE, Ambarella, Mobileye, Qualcomm) drives per-vehicle BOM past <b class="r">$6,000</b>. Add radar, cameras, enclosure and integration and the stack cannot land under fleet payback thresholds.'),
            dict(k="Layer 3 · Market outcome", h="Sales limited<br>to rich fleets.",
                 p="Only US, EU and GCC logistics majors can amortise that cost. Indian and cost-sensitive GCC fleets are shut out of the safety-mandate wave entirely."),
        ], 300, 310)
        + _note('The constraint is <b>structural, not algorithmic.</b> No amount of model quality moves a '
                '$6,000 bill of materials — <span class="c">only owning the die does.</span>', 650)))

    S.append(dict(sec="SOLUTION", label="SOLUTION",
        title="DGrid&nbsp;Alpha — a single combo-die closes the BOM gap.",
        sub="Four proven engineering choices, one BOM slot, ~$30 board cost.",
        body=_cards(4, [
            dict(k="01 · Compute fabric", h="3D Systolic<br>Tensor Cube",
                 p='<b>64 × 512 MAC</b> lattice, dual-issue at <b>600&nbsp;MHz</b> → measured <b class="c">39.3 TOPS INT8</b>.<br><br>Sized for one 8MP camera cluster plus 4-corner radar without off-chip DRAM thrash.'),
            dict(k="02 · Firmware", h="Batch-dispatch<br>scheduler",
                 p='Micro-batches perception ops across camera and radar streams for a measured <b class="c">~200×</b> utilisation gain over naive per-frame dispatch on the same silicon.<br><br>The reason the MAC array reaches its TOPS ceiling.'),
            dict(k="03 · Integration", h="Six chiplets,<br>one combo-die",
                 p="ADAS, radar DSP, thermal and LiDAR DSP, secure enclave, telematics and driver-health in one package on 28&nbsp;nm HPC+.<br><br>Replaces the four-to-six chip stack most Tier-1 designs still ship."),
            dict(k="04 · Cost outcome", h="~$30 board<br>BOM at scale", v="accent",
                 p='Die at <b class="c">$3.876</b>, board around <b class="c">$30</b> — against a merchant tier that starts near $3,500 and runs past $6,000.'),
        ], 285, 345)))

    chiplets_a = [
        dict(k="A100", h="ADAS &amp; AI", p='The inference engine. <b class="c">39.3</b> TOPS INT8 across perception, fusion and planning.'),
        dict(k="R100", h="Radar DSP", p='<b>77 GHz</b> radar signal processing on-die. Removes the discrete radar DSP from the kit.'),
        dict(k="T100", h="Thermal &amp; LiDAR DSP", p="Thermal camera and LiDAR front-end processing for low-visibility and night operation."),
    ]
    chiplets_b = [
        dict(k="D100", h="Secure enclave", p="Lockstep RISC-V safety island. The basis of the sovereign data-security argument.", v="accent"),
        dict(k="S100", h="SDV telematics", p="AIS-140-class telematics on-die, so the retrofit kit needs no secondary tracker."),
        dict(k="H100", h="Driver health", p="Bio-ADC front end for drowsiness and fatigue detection, feeding the mandate functions."),
    ]
    S.append(dict(sec="ARCHITECTURE", label="ARCHITECTURE",
        title="Six chiplets on one 28&nbsp;nm combo-die.",
        sub="Roughly 57.1&nbsp;mm² of die on TSMC 28&nbsp;nm HPC+, with a predicted 96.7% yield.",
        body=_cards(3, chiplets_a, 285, 200) + _cards(3, chiplets_b, 505, 200)
        + _note('Two of these six — <span class="c">D100</span> and <span class="c">S100</span> — are what no '
                'merchant ADAS SoC bundles. They are the sovereignty and the no-second-tracker arguments.', 735)))

    S.append(dict(sec="WHAT THE MONEY BUYS", label="TAPEOUT",
        title='The die cost is quoted. The <span class="r">yield is not proven.</span>',
        sub="This is the single technical risk the raise exists to retire.",
        body=_split([
            dict(k="Node", v="TSMC <b>28 nm</b> HPC+, roughly <b>57.1 mm²</b> of die"),
            dict(k="Die cost", v="<b>$3.876</b> at 1M chips — supplier-quoted, under $4"),
            dict(k="Predicted yield", v="<b>96.7%</b> — a model output, not a measurement"),
        ], [
            dict(v="ok", k="What has to be true", p="Multi-project-wafer silicon confirms the FPGA-validated compute and the 28&nbsp;nm yield model, so the <b>$3.876</b> die cost survives contact with real wafers."),
            dict(v="kill", k="What proves it wrong", p="The full-die shuttle misses timing, power or yield. <b>$370K</b> is committed before that gate clears — 11.7% of the total tapeout budget."),
        ], 300)))

    S.append(dict(sec="CORRECTIONS LEDGER", label="CORRECTIONS",
        title='Four figures from earlier materials are <span class="r">retracted.</span>',
        sub="Stated here rather than quietly swapped, because an investor who finds the discrepancy later discounts everything else.",
        body=_rows([
            dict(l="“₹25 Cr ask”", vc="a", v="Superseded", w="Reconciled against Use of Funds: ₹45&nbsp;Cr equity CCPS + ₹10&nbsp;Cr CGTMSE debt = <b>₹55 Cr</b> blended."),
            dict(l="“Under $3 die”", vc="a", v="Superseded", w="The quoted die cost is <b>$3.876</b> at 1M chips — under four dollars, not three."),
            dict(l="“774× advantage”", vc="r", v="Retracted", w="Unsourced: it divided an unsourced $3,000 by our own cost. The sourced comparison is <b>12.9×</b>."),
            dict(l="“$8M NRE”", vc="r", v="Retracted", w="The line-item build-up totals <b>$3.17M</b>. The 3,636-unit break-even that figure implied is void."),
        ], 300)
        + _note('Every correction appears on a slide, labelled, beside the figure it replaces. '
                '<b>No number in this deck is a silent swap.</b>', 660, "warn")))

    # ===================== SECTION 2 — ICP & GTM (the heart) =====================

    S.append(dict(sec="HOW THE SEGMENT WAS CHOSEN", label="METHOD",
        title="The beachhead was scored, not picked.",
        sub="Ten weighted dimensions, five candidate segments, and an adversarial pass that found two real gaps.",
        body=_rows([
            dict(l="Source intake", v="Complete", w="<b>34</b> claims classified fact, claim, inference or unknown before any scoring began."),
            dict(l="Segment scoring", v="Complete", w="Ten weighted dimensions applied independently to five candidate segments."),
            dict(l="Approval gate", vc="g", v="Passed", w="Scorecard signed off before any go-to-market design work started."),
            dict(l="Validation design", v="Complete", w="A <b>27</b>-question buyer discovery guide and a paid-pilot charter."),
            dict(l="Challenge review", vc="a", v="2 gaps open", w="An adversarial pass found two real gaps. Both are still open and both are named in this deck."),
        ], 300)))

    S.append(dict(sec="SCORING DIMENSIONS · 1 OF 2", label="DIMENSIONS 1/2",
        title='Five dimensions decide whether a segment <span class="c">can buy.</span>',
        sub="These are the qualifying gates — fail one badly and the segment cannot transact at all.",
        body=_cards(5, [
            dict(k="01", h="Regulatory compulsion", p="Is the purchase mandated or discretionary? Mandates convert cost-sensitive buyers into deadline-driven ones."),
            dict(k="02", h="Certification friction", p="How much homologation and integration sits between a working part and a shipped vehicle."),
            dict(k="03", h="Price elasticity", p="The BOM ceiling the segment actually clears — not the price we would like to charge."),
            dict(k="04", h="Sales cycle", p="Months from first contact to signed order. Long cycles burn a pre-revenue balance sheet."),
            dict(k="05", h="ODD entropy", p="How unconstrained the operating domain is. Constrained domains ship years earlier."),
        ], 290, 300)))

    S.append(dict(sec="SCORING DIMENSIONS · 2 OF 2", label="DIMENSIONS 2/2",
        title='Five more decide whether it <span class="c">compounds.</span>',
        sub="These separate a segment that can buy once from a segment that builds a business.",
        body=_cards(5, [
            dict(k="06", h="Budget authority", p="Whether the person with the problem also controls the money to fix it."),
            dict(k="07", h="Competitive pressure", p="How contested the segment already is, and by whom."),
            dict(k="08", h="Unit-economics margin", p="Gross margin the segment supports at the price it will actually clear."),
            dict(k="09", h="Repeatability", p="Whether a win is a template or a one-off. Lumpy revenue does not compound."),
            dict(k="10", h="Evidence strength", p="What we have actually observed in this segment, as opposed to modelled."),
        ], 290, 300)
        + _note("Weights — problem 15% · urgency 15% · budget 12% · fit 12% · certification friction 10% · "
                "sales cycle 10% · competitive pressure 8% · margin 8% · repeatability 5% · evidence 5%.", 620)))

    S.append(dict(sec="WEIGHTED SCORECARD · 5 SEGMENTS", label="SCORECARD",
        title="Defense scores highest on evidence, not enthusiasm.",
        sub="The founder's preferred segment came second — which is the point of scoring before choosing.",
        body=_rows([
            dict(l="Tactical Defense &amp; Port", v="3.96 · 79.2%", hi=True, w="Wins evidence strength, budget authority and technical fit. Ships on FPGA today."),
            dict(l="3PL &amp; Fleet Retrofit", v="3.40 · 68.0%", w="The scale story, and the working hypothesis. Zero signed customers."),
            dict(l="AD0 Owner-Operator", vc="a", v="2.62 · 52.4%", w="Below threshold. Fragmented buying, no consolidated budget authority."),
            dict(l="OEM &amp; Tier-1", vc="a", v="2.32 · 46.4%", w="Worst certification friction and sales cycle of any segment scored."),
            dict(l="Commercial Insurers", vc="r", v="2.15 · 43.0%", w="Lowest score. Carries an unverified premium-reduction claim."),
        ], 300)))

    S.append(dict(sec="PRIMARY ICP · 79.2%", label="ICP A · DEFENSE",
        title='Defense is the only segment with <span class="c">revenue on the board.</span>',
        sub="Cost-insensitive, sovereignty-driven, and reachable with the silicon that already exists.",
        body=_split([
            dict(k="Targets", v="Sovereign UGVs, border surveillance, seaport AGVs"),
            dict(k="Why it buys", v="Cost-insensitive; buys <b>data sovereignty</b> via the D100 lockstep enclave"),
            dict(k="Score", v="<b>3.96</b> / 5 — evidence 5/5, budget 5/5, fit 5/5"),
        ], [
            dict(v="ok", k="What has to be true", p="Sovereign buyers pay for sovereignty rather than price, and an on-die enclave is a differentiator they cannot satisfy with imported compute."),
            dict(v="kill", k="What proves it wrong", p="The <b>₹1 Cr</b> already booked turns out to be grant or subsidy, not a commercial sale. Defense and Fleet then become evidence-equal."),
        ], 300)))

    S.append(dict(sec="SECONDARY EXPERIMENT · 68.0%", label="ICP B · FLEET",
        title='Fleet carries the scale story and <span class="r">none of the evidence.</span>',
        sub="This is the segment the FY32 model depends on, and it has not yet sold a single unit.",
        body=_split([
            dict(k="Targets", v="Medium and heavy <b>N2/N3</b> trucks, aftermarket retrofit"),
            dict(k="Price point", v="<b>₹2–2.5 Lakh</b> — a roadmap figure carried as an assumption"),
            dict(k="Score", v="<b>3.40</b> / 5 — strongest on scale, weakest on evidence"),
        ], [
            dict(v="ok", k="What has to be true", p="Mandate deadlines turn a cost-sensitive retrofit buyer into a non-discretionary one, and <b>₹2–2.5 Lakh</b> clears their ceiling."),
            dict(v="kill", k="What proves it wrong", p="Fewer than one of the first <b>20</b> buyer interviews converts to a paid pilot inside <b>90</b> days. Fleet then stays secondary."),
        ], 300)))

    S.append(dict(sec="DEFERRED · 46.4%", label="ICP C · OEM",
        title='OEM line-fit is the real scale, at the <span class="a">worst timing.</span>',
        sub="Right destination, wrong sequence — and the friction scores say so unambiguously.",
        body=_split([
            dict(k="Targets", v="OEM factory line-fit and Tier-1 module embedding"),
            dict(k="Friction", v="Certification <b>1/5</b> and sales cycle <b>1/5</b> — worst of any segment"),
            dict(k="Score", v="<b>2.32</b> / 5 — real long-term scale, wrong sequence"),
        ], [
            dict(v="ok", k="What has to be true", p="A signed Tier-1 partnership shortcuts both the homologation burden and the sales cycle, because the partner already carries both."),
            dict(v="kill", k="What proves it wrong", p="No Tier-1 signs. Any OEM go-to-market spend before that signature is dead capital, and the lane stays closed."),
        ], 300)))

    S.append(dict(sec="DEFERRED AND ANTI-ICP", label="ANTI-ICP",
        title='One segment is not a customer. It\'s a <span class="r">partner test.</span>',
        sub="Naming an anti-ICP is what stops a plausible-sounding segment from absorbing a year of runway.",
        body=_rows([
            dict(l="OEM &amp; Tier-1", vc="a", v="Deferred", w="Real long-term scale, worst near-term friction. No go-to-market spend until a Tier-1 partnership is signed."),
            dict(l="Commercial Insurers", vc="r", v="Anti-ICP", w="Lowest score of the five. The premium-reduction benefit is unverified, and the financial model carries zero insurer revenue rows."),
        ], 310)
        + _note('Insurers may be an <b>evidence partner</b> — never a direct customer — until a pilot proves the '
                'premium mechanism against observed loss data. <span class="c">Partners until they pay.</span>', 530, "alert")))

    S.append(dict(sec="SELECTION SYNTHESIS", label="SYNTHESIS",
        title="Defense wins six months. It cannot win the decade.",
        sub="Both segments are right about different things, which is why this resolves as a sequence rather than a choice.",
        body=_rows([
            dict(l="Evidence · budget · fit", v="Defense 5/5", w="Booked revenue, cost-insensitive buyers, and silicon that ships on FPGA today."),
            dict(l="Repeatability", vc="a", v="Defense 2/5", w="Defense contracts are lumpy. They do not compound into the systems-revenue business the raise is built on."),
            dict(l="Market scale", v="Fleet wins", w="The multi-million-truck market is where FY32 revenue comes from — and it has no signed customer yet."),
        ], 300)
        + _note('Run Defense as resourced primary for six months to generate the missing Fleet evidence, with Fleet '
                'funded in parallel as an experiment. <b>This is a sequenced two-track plan, not a pivot.</b> The '
                'strongest counter-case — that a defense-first motion undercuts a narrative built on fleet scale — '
                'is exactly why the sequencing must stay explicit in every document.', 570)))

    S.append(dict(sec="BUYING COMMITTEE · DEFENSE", label="BUYERS · DEFENSE",
        title="In Defense, the blocker outranks the champion.",
        sub="Five roles, and the one that can stop the deal is not the one that wants it.",
        body=_rows([
            dict(l="Economic buyer", v="Procurement", w="Defense procurement or port authority. Fears vendor lock-in."),
            dict(l="Technical buyer", v="Integrator", w="Systems integration engineer. Fears undocumented failure modes."),
            dict(l="Champion", vc="a", v="Unidentified", w="Program manager — not yet named in any account. A gap, not a role."),
            dict(l="Blocker", vc="r", v="Compliance", w="Security clearance and compliance office. A mandatory gate with no workaround."),
            dict(l="End user", v="Operator", w="UGV and AGV operators. Judge reliability in the field."),
        ], 300)
        + _note('Minimum proof to advance: a <b>second signed contract</b>, or an audited confirmation of the '
                '₹1&nbsp;Cr already booked.', 745)))

    S.append(dict(sec="BUYING COMMITTEE · FLEET", label="BUYERS · FLEET",
        title="In Fleet, the mandate deadline is the champion.",
        sub="The safety officer facing an AIS deadline is the only role with a reason to move first.",
        body=_rows([
            dict(l="Economic buyer", vc="a", v="Fleet owner", w="Fleet owner or operator. Fears unproven return and payback."),
            dict(l="Technical buyer", v="Telematics", w="Maintenance and telematics manager. Fears integration downtime."),
            dict(l="Champion", v="Compliance", w="Safety officer facing the AIS mandate deadline. The natural ally."),
            dict(l="Blocker", vc="a", v="Procurement", w="Procurement, or the vehicle owner on attached fleets."),
            dict(l="End user", v="Driver", w="Cabin reliability and tolerance for false positives."),
        ], 300)
        + _note('Minimum proof to advance: <b>one signed paid pilot</b> from the first twenty discovery interviews.', 745)))

    S.append(dict(sec="POSITIONING · TWO TRACKS", label="POSITIONING",
        title="Two tracks, two sentences, two kill criteria.",
        sub="Each statement ships with the condition that would disprove it.",
        body=_rows([
            dict(l="Defense", v="Sovereignty", w="“Sovereign edge-AI silicon with an on-die lockstep security enclave — no imported compute inside the trust boundary.” Kill criterion: a second signed contract, or the ₹1&nbsp;Cr audited."),
            dict(l="Fleet", vc="a", v="Price · pending", w="“Mandate-ready ADAS retrofit at a domestic price point.” Carried as <b>pending validation</b>. Kill criterion: one paid pilot from the first twenty interviews."),
        ], 310)
        + _note('Neither statement leaves the building without its kill criterion attached. '
                '<span class="c">A positioning claim with no disproof condition is marketing, not strategy.</span>', 560)))

    S.append(dict(sec="CLAIM DISCIPLINE", label="CLAIMS TO STOP",
        title='Five claims come <span class="r">off the slides</span> today.',
        sub="Each one is either unreconciled, unmeasured, or a forecast being presented as demand.",
        body=_cards(5, [
            dict(v="alert", k="Stop", h="“84% ASIC margin”", p='Unreconciled, and the surrounding text implies 92–93%. Use the modelled FY32 gross margin of <b class="a">88%</b>.'),
            dict(v="alert", k="Stop", h="“Premium cut 10–15%”", p="Unverified. The model carries zero insurer revenue rows. State the partner test, not a benefit."),
            dict(v="alert", k="Stop", h="“Mandate-ready”", p="Unvalidated against the operative dates. State the target date, not readiness against it."),
            dict(v="alert", k="Stop", h="“Accident reduction %”", p="Nothing has been measured. No vehicle trial has been run or published."),
            dict(v="alert", k="Stop", h="“5M+ trucks”", p="A market forecast, not demand. Real pipeline is twenty interviews and one pilot gate."),
        ], 290, 300)))

    S.append(dict(sec="PRICING LOGIC", label="PRICING",
        title='We don\'t have a price. We have a <span class="c">plan to find one.</span>',
        sub="Manufacturing false precision here would be the fastest way to lose credibility in diligence.",
        body=_split([
            dict(k="Fleet", v="<b>₹2–2.5 Lakh</b> is a roadmap figure, not a quote or a tested band"),
            dict(k="Defense", v="Contract-negotiated per sovereign buyer"),
            dict(k="Kit build-up", v="~<b>$200</b>: ASIC $30 · radar $100 · cameras $50 · enclosure $20"),
        ], [
            dict(v="ok", k="What has to be true", p="Willingness-to-pay questions inside the discovery guide return a defensible price band within the first twenty interviews."),
            dict(v="kill", k="What proves it wrong", p="Interviews return a ceiling below the kit's landed cost. The retrofit lane then needs a different configuration, not a different price."),
        ], 300)))

    S.append(dict(sec="CHANNEL STRATEGY", label="CHANNEL",
        title="Direct, until a partner earns the margin.",
        sub="Every indirect channel stays closed until there is a reason — and a signature — to open it.",
        body=_rows([
            dict(l="Direct · Defense", v="Now", w="Recommended primary motion. Sovereign buyers expect a direct technical relationship."),
            dict(l="Direct · Fleet", v="Pilot only", w="Recommended for the pilot phase, to keep discovery signal unfiltered by a reseller."),
            dict(l="System integrators", vc="a", v="Not yet", w="No partner identified. Revisit once the retrofit configuration is frozen."),
            dict(l="Defense primes", vc="a", v="After 2 wins", w="Considered only after two signed Defense contracts of our own."),
        ], 300)))

    S.append(dict(sec="EXECUTION · NEXT 90 DAYS", label="90-DAY PLAN",
        title="Ninety days to turn evidence into a decision.",
        sub="Three phases, one hard gate, and a stop-doing list that protects the runway.",
        body=_cards(3, [
            dict(k="Weeks 1–4", h="Evidence", p="Audit the <b>₹1 Cr</b> revenue back to its contract. Run <b>10</b> buyer interviews. Name <b>3</b> target accounts."),
            dict(k="Weeks 5–9", h="Conversion", p="Sell one <b>paid Fleet pilot</b>. Advance one Defense technical evaluation. Open the second contract."),
            dict(k="Weeks 10–13", h="Governance", p="Re-score both segments against the <b>same scorecard</b>. Hard gate on Fleet at day 90.", v="accent"),
        ], 300, 260)
        + _note("Stop-doing list — no OEM go-to-market spend until a Tier-1 signs · no insurer-facing sales motion · "
                "no AD0 resourcing pending the evidence check · no external claim that is not on the sourced list.", 600, "warn")))

    S.append(dict(sec="ONE DISCIPLINE NOTE", label="KILL SWITCH",
        title='One kill switch governs <span class="r">both tracks.</span>',
        sub="Stated now, so that failing it later is a decision rather than a drift.",
        body=_callout(dict(
            cond="If the ₹1&nbsp;Cr is not a commercial sale <em>and</em> no Fleet pilot converts by day&nbsp;90 —",
            then="then neither track has evidence, and the ₹55&nbsp;Cr case rests on a forecast alone. The honest response is to "
                 "<b>raise a smaller bridge against the tapeout only</b> — funding the three MPW shuttles that de-risk the die — "
                 "rather than a growth round against a market we have not yet sold into.",
            **{"not": 'What we should <span class="r">not</span> do is fund a two-segment go-to-market motion after both segments have failed their own test.'}
        ), 320)))

    # ===================== SECTION 3 — COMPETITIVE LANDSCAPE =====================

    S.append(dict(sec="STRATEGIC PLAYBOOKS", label="PLAYBOOKS",
        title='Every credible player picks <span class="a">one lane.</span>',
        sub="None of them runs all three motions, and none of them does it at a ~$30 board cost.",
        body=_cards(5, [
            dict(k="USA", h="Aurora", p='Heavy-OEM, long-haul Class-8. Dual NVIDIA DRIVE Thor. Board BOM past <b class="r">$6,000</b>. Continental industrialises it.'),
            dict(k="USA · DoD", h="Kodiak", p="Dual-use: highway freight plus DoD contracts. Ambarella <b>CV3-AD685</b> as the compute."),
            dict(k="USA", h="Gatik", p="Constrained middle-mile only. NVIDIA DRIVE AGX Orin. Isuzu box trucks for Walmart and Kroger."),
            dict(k="China", h="DeepWay", p="China domestic fleets. High-compute NPU with Baidu Apollo, in “Xingtu” L4 electric trucks."),
            dict(v="accent", k="India", h="DeepGrid", p='Own 28&nbsp;nm combo-die at <b class="c">~$30</b> board BOM. The only lane choice not set by a chip vendor.'),
        ], 290, 310)))

    S.append(dict(sec="SILICON DEPENDENCY", label="DEPENDENCY",
        title="Four of five rent their compute.",
        sub="Whoever owns the die owns the cost structure — and everyone else inherits it.",
        body=_rows([
            dict(l="Aurora", vc="a", v="NVIDIA", w="Two DRIVE Thor parts. BOM past $6,000. The roadmap moves when NVIDIA's does."),
            dict(l="Kodiak", vc="a", v="Ambarella", w="CV3-AD685. Single-vendor dependency on a merchant ADAS SoC."),
            dict(l="Gatik", vc="a", v="NVIDIA", w="DRIVE AGX Orin. Margin structure set by someone else's die price."),
            dict(l="DeepWay", vc="a", v="Baidu · NPU", w="Domestic Chinese stack. Vertically closer, but not export-positioned."),
            dict(l="DeepGrid", v="None", hi=True, w="Own 28&nbsp;nm combo-die. No chip vendor anywhere in the cost structure."),
        ], 300)))

    S.append(dict(sec="COST ADVANTAGE", label="COST STRUCTURE",
        title='Twelve-point-nine times, on a <span class="c">sourced comparison.</span>',
        sub="The number that replaced the retracted 774× claim — and where each half of it comes from.",
        body=_cards(4, [
            dict(k="Die level", h="vs Mobileye ASP", big="12.9×", bigv="c", v="accent",
                 p='Mobileye\'s <b>$50</b> ASP divided by our <b>$3.876</b> die cost at 1M chips.'),
            dict(k="Kit level", h="vs imported ADAS", big="3–7×", bigv="c",
                 p="Against company-stated import bands of <b>₹5–18 Lakh</b> for equivalent function."),
            dict(k="Our die", h="At 1M chips", big="$3.876", p="TSMC 28&nbsp;nm HPC+, roughly 57.1&nbsp;mm². Supplier-quoted."),
            dict(k="Our board", h="After integration", big="~$30", p="Six functions on one die removes four vendors' parts from the BOM."),
        ], 290, 330)
        + _note('The retracted 774× figure divided an unsourced $3,000 by our own cost. '
                '<span class="c">That is not a comparison</span> — and it is not used anywhere in this deck.', 660, "warn")))

    S.append(dict(sec="DOMESTIC LANDSCAPE", label="INDIA WAVE",
        title="India's silicon wave is real, and a year behind.",
        sub="A genuine lead, but a perishable one — the window is roughly twelve months wide.",
        body=_cards(3, [
            dict(k="Vision SoC", h="Netrasemi", p="A2000 SoC on TSMC <b>12&nbsp;nm</b>. <b>₹125 Cr</b> raised. Launch expected mid-<b>2027</b>."),
            dict(k="RISC-V MCU", h="Mindgrove", p="RISC-V microcontroller on TSMC <b>28&nbsp;nm</b>. Bosch MoU signed. <b>$10.3M</b> raised."),
            dict(k="GaN RF", h="Agnit", p="GaN devices for RF and power. Defense radar pilots running. <b>$7.47M</b> raised."),
        ], 300, 240)
        + _note("None is shipping an ADAS combo-die today. The nearest domestic ASIC competitor reaches launch roughly "
                "twelve months behind DeepGrid's current position — a lead that is real but not durable.", 580)))

    S.append(dict(sec="SOFTWARE-FIRST AUTONOMY", label="SOFTWARE-FIRST",
        title='Better algorithms don\'t change the <span class="a">die price.</span>',
        sub="Three credible Indian autonomy teams, all inheriting the same cost structure.",
        body=_cards(3, [
            dict(k="Perception IP", h="Minus Zero", p="Hardware-agnostic autonomy stack. Inherits whatever the merchant SoC costs."),
            dict(k="Research-led", h="Swaayatt Robots", p="Constrained-route autonomy research. No silicon position of its own."),
            dict(k="Middleware", h="RoshAI", p="Fleet autonomy middleware. Runs on standard parts at standard prices."),
        ], 300, 240)
        + _note("Hardware-agnostic autonomy inherits the squeeze zone by construction. Algorithm quality is a product "
                "advantage; it is not a cost-structure advantage — and this market is decided on cost structure.", 580)))

    S.append(dict(sec="COMPETITIVE SYNTHESIS", label="COMPETITIVE",
        title="One position nobody else occupies.",
        sub="The claim is structural, and it is the only one worth defending in diligence.",
        body=_rows([
            dict(l="Vertical integration", v="Only one", hi=True, w="The only Indian company with a single-die ADAS combo-die of its own design."),
            dict(l="Cost structure", v="12.9×", w="A ~$30 board BOM against a merchant tier that starts near $3,500 and runs past $6,000."),
            dict(l="Timing", v="~12 months", w="First mover on retrofittable, mandate-targeted ADAS for India and the GCC."),
        ], 300)
        + _note('The defensible claim is <b>structural, not performance-based.</b> We are not asserting better '
                'perception than Mobileye. We are asserting a different cost structure than anyone else selling '
                'into this market — and cost structure is what this market decides on.', 570)))

    # ===================== SECTION 4 — ROADMAP & REGULATORY =====================

    S.append(dict(sec="ROADMAP · THREE PHASES", label="ROADMAP",
        title="Three phases, each gated on the last one's evidence.",
        sub="The original pitch already sequenced Defense first. The scorecard confirms that sequence rather than inventing it.",
        body=_cards(3, [
            dict(k="Months 0–6", h="Phase 1 · Wedge", p="Tactical and off-highway deployments. <b>Audit and confirm</b> the ₹1&nbsp;Cr already booked. Open the second contract."),
            dict(k="Months 6–18", h="Phase 2 · Volume", p="Close the <b>₹55 Cr</b> blended raise. TSMC <b>28&nbsp;nm</b> MPW tape-out. Launch the retrofit kit."),
            dict(k="Months 18–36", h="Phase 3 · Scale", p="Tier-1 alliances and OEM line-fit. Shift toward <b>recurring</b> per-vehicle software revenue.", v="accent"),
        ], 300, 250)
        + _note("Each phase has a named gate. Phase 2 does not start until the ₹1&nbsp;Cr is audited; Phase 3 does not "
                "start until a Tier-1 signs.", 590)))

    S.append(dict(sec="PHASE 2 GATE · THE TAPEOUT", label="TAPEOUT PHASING",
        title='Only $370K is at risk before the <span class="c">yield gate.</span>',
        sub="Three shuttles de-risk the die before the expensive 88% of the budget is committed.",
        body=_split([
            dict(k="At risk pre-validation", v="<b>$370K</b> — 11.7% of the $3.17M total"),
            dict(k="MPW phasing", v="<b>$69K</b> A100 · <b>$69K</b> R100 · <b>$232K</b> full-die shuttle"),
            dict(k="Committed after the gate", v="<b>$1.0M</b> backend to GDSII · <b>$1.0M</b> mask · <b>$800K</b> IP and PHY"),
        ], [
            dict(v="ok", k="What has to be true", p="Three shuttles de-risk the die before the mask set is ordered, so the expensive <b>88%</b> of the budget only spends after silicon proves out."),
            dict(v="kill", k="What proves it wrong", p="The full-die shuttle misses timing, power or yield. The programme then stops at <b>$370K</b> rather than at <b>$3.17M</b>."),
        ], 300)))

    S.append(dict(sec="REGULATORY · INDIA", label="INDIA MANDATE",
        title='The mandate dates in earlier materials were <span class="r">wrong.</span>',
        sub="This matters because the entire Fleet timing argument is built on them.",
        body=_rows([
            dict(l="AIS-184 · AEBS", v="1 Oct 2027", w="Autonomous emergency braking. Served by A100 compute with the R100 radar DSP."),
            dict(l="AIS-186 · ESC", v="1 Oct 2027", w="Electronic stability control. A100 with the D100 lockstep safety enclave."),
            dict(l="AIS-187 to 190", v="1 Jan 2028", w="Lane keeping, curve speed, fatigue detection and telematics. A100 with S100 and H100."),
        ], 300)
        + _note('Earlier materials carried Apr/Oct <b>2026</b> dates. The operative dates are <b>1 October 2027</b> for '
                'AEBS and ESC, and <b>1 January 2028</b> for all four functions. Both must be confirmed against the '
                'final MoRTH Gazette before either is presented as settled.', 570, "warn")))

    S.append(dict(sec="REGULATORY · GCC", label="GCC MANDATE",
        title="The GCC needs one chiplet we already have.",
        sub="S100 turns a compliance requirement into a bill-of-materials advantage.",
        body=_split([
            dict(k="Saudi Arabia", v="TGA safety requirements plus the <b>WASL</b> fleet-tracking mandate"),
            dict(k="The S100 advantage", v="On-die telematics removes the <b>secondary tracker</b> from the kit"),
            dict(k="Timing", v="Phase 3. The beachhead stays India"),
        ], [
            dict(v="ok", k="What has to be true", p="Removing a discrete tracker is a real BOM and installation-time advantage in a mandate-driven GCC fleet tender."),
            dict(v="kill", k="What proves it wrong", p="GCC homologation treats an integrated tracker as non-compliant and requires a separately certified standalone unit anyway."),
        ], 300)))

    # ===================== SECTION 5 — FINANCIALS =====================

    S.append(dict(sec="REVENUE · MANAGEMENT MODEL", label="REVENUE",
        title='Six years to <span class="c">₹1,388 Cr</span> on the model.',
        sub="Management projection, unaudited. This is model output, not observed data.",
        body=_cards(5, [
            dict(k="FY28", h="₹41.17 Cr", p="First full year of retrofit-kit revenue."),
            dict(k="FY29", h="₹144.73 Cr", p="Net income turns positive this year.", v="accent"),
            dict(k="FY30", h="₹351.35 Cr", p="Volume ramp against the mandate deadlines."),
            dict(k="FY31", h="₹731.54 Cr", p="OEM line-fit begins contributing."),
            dict(k="FY32", h="₹1,387.95 Cr", p='EBITDA <b class="c">₹536.63 Cr</b> at 39% of revenue.'),
        ], 290, 250)
        + _note("FY27 opens the ramp at ₹6.0&nbsp;Cr. FY32 revenue was previously misstated as ₹1,128&nbsp;Cr on a cover "
                "slide; the reconciled figure is <b>₹1,387.95 Cr</b>, confirmed seven times in the workbook.", 580, "warn")))

    S.append(dict(sec="GROSS MARGIN WALK", label="MARGIN WALK",
        title='Margin expands because the <span class="c">die gets cheaper.</span>',
        sub="Not because the retrofit price goes up — it stays inside the same band throughout the model.",
        body=_bars(dict(
            a_h=53, a_v="53%", a_t="FY27 gross margin", a_s="first silicon, low volume",
            delta="+35 pt", b_h=88, b_v="88%", b_t="FY32 gross margin", b_s="at volume on 28 nm",
            p1="The walk is <b>53 → 74 → 79 → 82 → 85 → 88%</b>. It is driven by wafer volume and test automation — "
               "not by raising the retrofit price, which stays inside the ₹2–2.5&nbsp;Lakh band throughout the model.",
            p2='<span class="c">FY32 EBITDA is ₹536.63 Cr, or 39% of revenue.</span> Net income ₹381.37&nbsp;Cr, '
               'positive from FY2029.',
        ), 300)))

    S.append(dict(sec="BREAK-EVEN", label="BREAK-EVEN",
        title='Break-even lands in the <span class="r">final year of the model.</span>',
        sub="Said plainly, because the earlier figure made it look four years earlier than it is.",
        body=_cards(4, [
            dict(k="Total NRE", h="Tapeout cost", big="$3.17M", p="From the line-item build-up, with MPW phasing inside it."),
            dict(k="Volume to recover", h="Chips at $18.12 margin", big="174,908", p="Per the reviewed analysis recomputation."),
            dict(k="Crossing year", h="Break-even", big="FY2032", bigv="r", v="alert", p="The final year of the six-year model."),
            dict(k="Pre-gate risk", h="Committed early", big="11.7%", bigv="c", p="Only $370K spends before the yield gate."),
        ], 290, 320)
        + _note('The earlier “$8M NRE and 3,636-unit break-even” pairing is <b>void in both halves</b> and is not used '
                'anywhere in this deck.', 650, "warn")))

    S.append(dict(sec="RECURRING REVENUE", label="SOFTWARE",
        title="Software is the second half of the model.",
        sub="Per-vehicle subscription revenue, priced off a sovereignty constraint rather than a feature list.",
        body=_rows([
            dict(l="Base · ₹10,000/yr", v="Telemetry", w="Per vehicle. Telemetry capture and a basic fleet dashboard."),
            dict(l="Advanced · ₹15,000/yr", v="Compliance", w="Adds mandate compliance reporting and an insurer data interface."),
            dict(l="Premium · ₹25,000/yr", v="Analytics", hi=True, w="Adds fleet analytics, over-the-air updates and data-governance controls."),
        ], 300)
        + _note('Behavioural data stays on-device inside the D100 enclave rather than leaving the vehicle. '
                '<span class="c">The sovereignty constraint is the pricing argument</span> — not a compliance cost '
                'to be absorbed.', 570)))

    S.append(dict(sec="CAPITAL STRUCTURE", label="CAPITAL",
        title="₹55 Cr blended. Subsidies are upside, not the plan.",
        sub="Sized to stand alone, so that no incentive decision sits on the critical path.",
        body=_rows([
            dict(l="Equity · ₹45 Cr", v="CCPS", w="Compulsorily convertible preference shares. Terms negotiable."),
            dict(l="Debt · ₹10 Cr", v="CGTMSE", w="Drawn across the build; a 25% draw gives roughly ₹47.5&nbsp;Cr funded."),
            dict(l="P-DLI", vc="a", v="Upside", w="Up to 50% design-cost reimbursement, capped at ₹15&nbsp;Cr."),
            dict(l="Deployment incentive", vc="a", v="Upside", w="Four to six percent of net sales, capped at ₹30&nbsp;Cr."),
        ], 300)
        + _note("Capital raised to date is <b>₹2.48 Cr</b> — ₹2&nbsp;Cr angel, ₹0.36&nbsp;Cr ARAI, ₹0.12&nbsp;Cr HDFC. "
                "The raise is sized to stand alone at ₹55&nbsp;Cr blended, with no incentive award assumed.", 660)))

    # ===================== SECTION 6 — RISK, DECISION, CLOSE =====================

    S.append(dict(sec="CHALLENGE FINDINGS", label="RED TEAM",
        title='An adversarial pass found <span class="r">five problems.</span>',
        sub="Printed here rather than in an appendix, because two of them gate the decision.",
        body=_cards(5, [
            dict(v="alert", k="Gap 1", h="Primes unassessed", p="Indian defense primes were never benchmarked. A cleared incumbent is a different problem than Netrasemi."),
            dict(v="alert", k="Gap 2", h="₹1 Cr unconfirmed", p="Commercial sale, or grant? If a grant, Defense and Fleet are evidence-equal and the sequencing argument fails."),
            dict(v="alert", k="Method", h="Circular evidence", p="The scorecard rates Defense highest partly on evidence that is itself the unconfirmed ₹1&nbsp;Cr."),
            dict(v="alert", k="Balance sheet", h="Working capital", p="<b>₹2.48 Cr</b> raised against a <b>₹55 Cr</b> ask, with government payment cycles of 90–180+ days."),
            dict(v="alert", k="Data", h="Yield disagreement", p="The workbook models <b>94.5%</b>; the memorandum states <b>96.7%</b>. Immaterial to die cost — but print only one."),
        ], 290, 310)))

    S.append(dict(sec="THE DECISION", label="DECISION",
        title="Proceed — with five conditions, in order.",
        sub="Not an unconditional go. Two of the five are evidence gates that could reopen the segment choice.",
        body=_split([
            dict(k="Condition 1", v="Confirm the nature of the <b>₹1 Cr</b> revenue within one week"),
            dict(k="Condition 2", v="Add Indian defense primes to the competitive benchmark"),
            dict(k="Condition 3", v="Model working-capital exposure to <b>90–180</b> day payment cycles"),
        ], [
            dict(v="ok", k="Conditions 4 and 5", p="Keep every external document in sequenced two-track framing, never a flat pivot narrative. Treat the day-90 checkpoint as a hard re-scoring gate against the same scorecard."),
            dict(v="kill", k="If a condition slips", p="Any condition unmet at day 90 reopens the segment decision. The scorecard is <b>re-run</b>, not re-argued."),
        ], 300)))

    S.append(dict(sec="THE ASK", label="CLOSE",
        title="A defensible ask, on the record.",
        sub="Four numbers, five conditions, and one thing we are actually asking you to fund.",
        body=_kpi([
            dict(k="Blended Ask", v="₹55 Cr", n="₹45 Cr CCPS equity + ₹10 Cr CGTMSE debt (~$4.79M)"),
            dict(k="Primary ICP Score", v="79.2<em>%</em>", n="Tactical Defense &amp; Off-Highway/Port, 3.96/5"),
            dict(k="First profitable year", v="FY2029", n="Net income positive on the management model"),
            dict(k="GTM Decision", v="Proceed with<br>Conditions", n="5 conditions, day-90 re-scoring gate", decide=True),
        ])
        + _note('We are not asking you to believe the forecast. We are asking you to fund the '
                '<span class="c">three MPW shuttles that test it</span> — $370K of at-risk capital against a '
                '$3.17M programme, with a hard gate before the mask set is ordered.', 560)))

    S.append(dict(sec="SOURCES", label="SOURCES",
        title="Where the numbers come from.",
        sub="Every figure in this deck traces to one of these; the evidence ledger carries the row-level detail.",
        body=_srcs([
            "Business Plan v2 workbook — P&amp;L, Use of Funds, Assumptions, CGTMSE sheets",
            "Reviewed Pre-Series A analysis — 132-row evidence ledger",
            "Tapeout Expenses sheet — NRE line-item build-up and MPW phasing",
            "Supplier die-cost quotation — TSMC 28&nbsp;nm HPC+ at 1M chips",
            "Information Memorandum, July 2026 — architecture, team, mandate dates",
            "MoRTH AIS standards — AIS-184, 186, 187, 188, 189, 190",
            "Competitor public disclosures — Aurora, Kodiak, Gatik, DeepWay",
            "Domestic semiconductor funding announcements — Netrasemi, Mindgrove, Agnit",
        ], 300)))

    return S


# ----------------------------------------------------------------- assemble

def render(S):
    out = []
    for i, s in enumerate(S, 1):
        nn = f"{i:02d}"
        if s.get("kind") == "cover":
            out.append(f'<section class="slide cover" data-title="{s["label"]}">{s["body"]}\n'
                       f'<div class="ft-l">{nn} · {s["label"]}</div>'
                       f'<div class="ft-r">{DISCLAIMER}</div></section>')
        else:
            out.append(f'''<section class="slide" data-title="{s['label']}">
<div class="ch-l">{nn} · {s['sec']}</div>
<div class="ch-r">{RIGHT_RAIL}</div>
<div class="rule"></div>
<h2 class="title">{s['title']}</h2>
<p class="sub">{s['sub']}</p>
<div class="cbody">
{s['body']}
</div>
<div class="ft-l">{nn} · {s['label']}</div>
<div class="ft-r">{DISCLAIMER}</div>
</section>''')
    return "\n\n".join(out)


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DeepGrid Semi — Pre-Series A Investor &amp; GTM Strategy</title>
<link rel="stylesheet" href="theme.css">
<link rel="stylesheet" href="template.css">
</head>
<body>
<div class="progress"><div class="progress-fill" id="progressFill"></div></div>
<div class="viewport"><div class="stage" id="stage">
"""

TAIL = """
</div></div>
<nav class="deck-nav"><button class="nav-btn" id="prevBtn">&#8592;</button>
<div class="counter"><span id="curNum">01</span> / <span id="totNum">00</span></div>
<button class="nav-btn" id="nextBtn">&#8594;</button></nav>
<script>
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var total=slides.length, cur=0;
  var stage=document.getElementById('stage'), fill=document.getElementById('progressFill');
  var curNum=document.getElementById('curNum'), totNum=document.getElementById('totNum');
  var prevBtn=document.getElementById('prevBtn'), nextBtn=document.getElementById('nextBtn');
  totNum.textContent=String(total).padStart(2,'0');
  function fit(){stage.style.setProperty('--fit',Math.min(window.innerWidth/1920,window.innerHeight/1080));}
  window.addEventListener('resize',fit); fit();
  function draw(){slides.forEach(function(s,i){s.classList.toggle('is-active',i===cur)});
    fill.style.width=(cur/(total-1)*100)+'%';curNum.textContent=String(cur+1).padStart(2,'0');
    prevBtn.disabled=cur===0;nextBtn.disabled=cur===total-1;}
  function go(i){cur=Math.max(0,Math.min(total-1,i));draw()}
  nextBtn.onclick=function(){go(cur+1)};prevBtn.onclick=function(){go(cur-1)};
  document.addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();go(cur+1)}
    else if(e.key==='ArrowLeft'){e.preventDefault();go(cur-1)}});
  draw();
  window.__deck={total:total,
    fitOne:function(){stage.style.setProperty('--fit',1);},
    show:function(i){slides.forEach(function(s,k){s.classList.remove('is-active');
      s.classList.toggle('render-static',k===i);});}};
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="deck.html")
    a = ap.parse_args()
    S = slides()
    pathlib.Path(a.out).write_text(HEAD + render(S) + TAIL, encoding="utf-8")
    print(f"DONE: {len(S)} slides -> {a.out}")
