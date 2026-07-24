#!/usr/bin/env python3
"""Templated dossier -> branded PPTX builder (Canva-Pro palette). One deck per company."""
import sys
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, Pt, PP_ALIGN
OUTDIR = "/home/shekerk/content-ideas/runs/2026-06-24-agent-validation-authority-deck/dossiers"
C = PP_ALIGN.CENTER

def make_deck(D):
    d = Deck(footer=f"{D['name']} · Company Dossier · Positioning Evidence · 2026-06-24")
    b = d.b
    def grid(n, gap=0.25, left=None, tw=None):
        left = d.M if left is None else left; tw = d.CW if tw is None else tw
        g = Inches(gap); w = (tw-g*(n-1))/n
        return [(left+int((w+g)*i), w) for i in range(n)]
    def card(s, x, y, w, h, title, lines, accent=None):
        accent = accent or b.TEAL
        d.rect(s, x, y, w, h, b.WHITE, radius=0.06, shadow=True)
        d.rect(s, x, y, Inches(0.09), h, accent)
        d.text(s, title, x+Inches(0.24), y+Inches(0.15), w-Inches(0.42), Inches(0.5), size=14, color=b.NAVY, bold=True, shrink=True)
        if lines:
            d.text(s, [{"text": t, "size": 11, "space_before": 4} for t in lines],
                   x+Inches(0.24), y+Inches(0.68), w-Inches(0.46), h-Inches(0.84), color=b.INK, shrink=True)
    def stat(s, x, y, w, h, num, label):
        d.rect(s, x, y, w, h, b.NAVY, radius=0.06, shadow=True)
        d.text(s, num, x, y+Inches(0.2), w, Inches(0.6), size=24, color=b.GOLD, bold=True, align=C, shrink=True)
        d.text(s, label, x+Inches(0.1), y+Inches(0.82), w-Inches(0.2), h-Inches(0.92), size=10.5, color=b.LIGHT_TEAL, align=C, shrink=True)
    T = 11; pg = [1]
    def foot(s):
        d.footer(s, pg[0], T); pg[0]+=1

    # 1 COVER
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(11.6), 0, Inches(1.73), d.H, b.NAVY_2); d.rect(s, Inches(11.54), 0, Inches(0.06), d.H, b.TEAL)
    d.text(s, "COMPANY DOSSIER", d.M, Inches(1.4), Inches(9), Inches(0.4), size=14, color=b.TEAL, bold=True)
    d.text(s, D['name'], d.M, Inches(2.0), Inches(10.4), Inches(1.1), size=48, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.25), Inches(1.6), Inches(0.06), b.TEAL)
    d.text(s, D['tagline'], d.M, Inches(3.5), Inches(10.2), Inches(0.7), size=20, color=b.LIGHT_TEAL, bold=True, shrink=True)
    d.text(s, D['one_line'], d.M, Inches(4.4), Inches(10.2), Inches(0.8), size=14, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, d.M, Inches(5.6), Inches(5.2), Inches(0.5), b.NAVY_2, radius=0.3, line=b.GOLD)
    d.text(s, D['pattern'], d.M, Inches(5.71), Inches(5.2), Inches(0.3), size=12.5, color=b.GOLD, align=C, bold=True, shrink=True)

    # 2 SNAPSHOT (6 stats)
    s = d.slide(fill=b.WHITE); d.header(s, D['tagline'], "Snapshot")
    r1 = grid(3); r2 = grid(3)
    for (x, w), (num, lab) in zip(r1, D['snapshot'][:3]):
        stat(s, x, Inches(1.75), w, Inches(1.75), num, lab)
    for (x, w), (num, lab) in zip(r2, D['snapshot'][3:6]):
        stat(s, x, Inches(3.75), w, Inches(1.75), num, lab)
    foot(s)

    # 3 ORIGIN
    s = d.slide(fill=b.WHITE); d.header(s, "Why this team could win", "Origin & founders")
    card(s, d.M, Inches(1.7), d.CW, Inches(2.6), "Founders", D['origin'], accent=b.TEAL)
    d.rect(s, d.M, Inches(4.55), d.CW, Inches(0.95), b.GOLD, radius=0.05)
    d.text(s, "LESSON:  "+D['why_win'], d.M+Inches(0.25), Inches(4.72), d.CW-Inches(0.5), Inches(0.6), size=14.5, color=b.NAVY, bold=True, shrink=True)
    foot(s)

    # 4 PROBLEM & ICP
    s = d.slide(fill=b.WHITE); d.header(s, "The problem & who pays", "Business problem & ICP")
    cols = grid(2, gap=0.3)
    card(s, cols[0][0], Inches(1.75), cols[0][1], Inches(3.5), "The problem", D['problem'], accent=b.CORAL)
    card(s, cols[1][0], Inches(1.75), cols[1][1], Inches(3.5), "ICP", D['icp'], accent=b.TEAL)
    foot(s)

    # 5 SOLUTION
    s = d.slide(fill=b.WHITE); d.header(s, "What they actually do", "The solution")
    card(s, d.M, Inches(1.75), d.CW, Inches(3.6), "Product", D['solution'], accent=b.TEAL)
    foot(s)

    # 6 USP
    s = d.slide(fill=b.WHITE); d.header(s, "What makes them differentiated", "Unique selling points")
    usp = D['usp']; cols = grid(len(usp), gap=0.18)
    for (x, w), (t, body) in zip(cols, usp):
        d.rect(s, x, Inches(1.85), w, Inches(3.5), b.SOFT, radius=0.06)
        d.rect(s, x, Inches(1.85), w, Inches(0.1), b.TEAL)
        d.text(s, t, x+Inches(0.13), Inches(2.05), w-Inches(0.26), Inches(0.9), size=12.5, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, x+Inches(0.13), Inches(2.95), w-Inches(0.26), Inches(2.3), size=10.5, color=b.INK, shrink=True)
    foot(s)

    # 7 POSITIONING
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
    d.text(s, "THE POSITIONING MOVE", d.M, Inches(0.85), Inches(9), Inches(0.4), size=14, color=b.TEAL, bold=True)
    d.text(s, D['pattern'], d.M, Inches(1.4), Inches(11.5), Inches(0.6), size=24, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.25), d.CW, Inches(1.3), b.NAVY_2, radius=0.05)
    d.rect(s, d.M, Inches(2.25), Inches(0.12), Inches(1.3), b.GOLD)
    d.text(s, "“"+D['verbatim']+"”", d.M+Inches(0.35), Inches(2.45), d.CW-Inches(0.7), Inches(0.95), size=17, color=b.WHITE, bold=True, italic=True, shrink=True)
    d.text(s, [{"text": t, "size": 13, "color": b.LIGHT_TEAL, "bullet": True, "space_before": 6} for t in D['pos_notes']],
           d.M, Inches(3.85), d.CW, Inches(2.3), shrink=True)
    foot(s)

    # 8 MOAT
    s = d.slide(fill=b.WHITE); d.header(s, "The moat — 5 layers, none the model", "Defensibility")
    moats = D['moat']; cols = grid(len(moats), gap=0.18)
    for (x, w), (t, body) in zip(cols, moats):
        d.rect(s, x, Inches(1.95), w, Inches(3.3), b.NAVY, radius=0.06, shadow=True)
        d.rect(s, x, Inches(1.95), w, Inches(0.1), b.TEAL)
        d.text(s, t, x+Inches(0.13), Inches(2.18), w-Inches(0.26), Inches(0.85), size=12.5, color=b.GOLD, bold=True, shrink=True)
        d.text(s, body, x+Inches(0.13), Inches(3.05), w-Inches(0.26), Inches(2.0), size=10.5, color=b.LIGHT_TEAL, shrink=True)
    foot(s)

    # 9 GTM / PRICING / TRACTION
    s = d.slide(fill=b.WHITE); d.header(s, "Pricing, GTM & traction", "How they sell and what it produced")
    cols = grid(2, gap=0.3)
    card(s, cols[0][0], Inches(1.75), cols[0][1], Inches(2.2), "Pricing & GTM", D['gtm'], accent=b.TEAL)
    ts = D['traction']; tcols = grid(len(ts), gap=0.18, left=cols[1][0], tw=cols[1][1])
    for (x, w), (num, lab) in zip(tcols, ts):
        stat(s, x, Inches(1.75), w, Inches(2.2), num, lab)
    d.rect(s, d.M, Inches(4.3), d.CW, Inches(1.1), b.SOFT, radius=0.05)
    d.text(s, "PROOF:  "+D['proof'], d.M+Inches(0.25), Inches(4.5), d.CW-Inches(0.5), Inches(0.7), size=13.5, color=b.INK, bold=True, shrink=True)
    foot(s)

    # 10 COMPETITORS
    s = d.slide(fill=b.WHITE); d.header(s, "Competitors & the edge", "Landscape")
    comps = D['competitors']; y0 = Inches(1.75); rh = Inches(0.72)
    for i, (c, note) in enumerate(comps):
        yy = y0 + int(rh*1.05)*i
        d.rect(s, d.M, yy, d.CW, rh, b.SOFT if i % 2 == 0 else b.WHITE, radius=0.06)
        d.rect(s, d.M, yy, Inches(0.09), rh, b.TEAL)
        d.text(s, c, d.M+Inches(0.28), yy+Inches(0.2), Inches(3.6), Inches(0.4), size=13, color=b.NAVY, bold=True, shrink=True)
        d.text(s, note, d.M+Inches(4.0), yy+Inches(0.21), d.CW-Inches(4.3), Inches(0.4), size=12, color=b.INK, shrink=True)
    d.text(s, "Edge:  "+D['edge'], d.M, Inches(5.55), d.CW, Inches(0.5), size=13.5, color=b.ACCENT, bold=True, shrink=True)
    foot(s)

    # 11 LESSONS
    s = d.slide(fill=b.WHITE); d.header(s, "Lessons for OUR positioning", "What to borrow")
    les = D['lessons']; y0 = Inches(1.75); rh = Inches(0.66)
    for i, t in enumerate(les):
        yy = y0 + int(rh*1.05)*i
        d.rect(s, d.M, yy, d.CW, rh, b.SOFT, radius=0.08)
        d.rect(s, d.M, yy, Inches(0.1), rh, b.GOLD)
        d.text(s, t, d.M+Inches(0.3), yy+Inches(0.19), d.CW-Inches(0.6), Inches(0.4), size=13, color=b.INK, bold=True, shrink=True)
    foot(s)

    out = f"{OUTDIR}/{D['slug']}-deck-branded-draft.pptx"
    d.save(out)
    return out

DATA = [
 dict(slug="harvey", name="Harvey AI", tagline="The AI operating system for elite legal work",
   pattern="Pattern 6 · Proprietary-Data Moat",
   one_line="In a high-stakes vertical the moat is workflow + data + compliance — not the model.",
   snapshot=[("2022","Founded · SF"),("~$300M","ARR (Jun 2026)"),("$11B","Valuation · 56x rev"),
             ("$1.5B+","Total raised"),("2,000","orgs · 2/3 AmLaw 100"),("960","team · 200+ lawyers")],
   origin=["Winston Weinberg (ex-litigator, O'Melveny) + Gabriel Pereyra (ex-DeepMind/Meta).",
           "Domain insider + frontier researcher = trust in a conservative vertical.",
           "OpenAI Startup Fund anchored the seed; early GPT-4 access → durable distribution edge."],
   why_win="The founding-team composition IS the positioning: buyers trust 'one of us built this.'",
   problem=["Elite legal work: high-stakes, language-heavy, $1,000+/hr labor.",
            "Source docs are unstructured and not in public training corpora.",
            "Errors carry malpractice/privilege risk; work sits behind ethical walls."],
   icp=["Phase 1: lawyers at elite global firms.","Phase 2: corporate in-house — 4% → 42% of revenue in ~1 year.","$300B+ legal market = the labor budget, not software."],
   solution=["Assistant — ask, draft, translate, research across case law.",
             "Agents — execute legal work end-to-end (M&A diligence over a full data room).",
             "25,000+ custom workflow agents; Spectre internal agent infrastructure.",
             "Cloud-agents switch (2026): usage doubled QoQ; token use ~12x YoY."],
   usp=[("Vertical depth","Ethical walls + matter confidentiality — no feature flag replicates it."),
        ("Embedded legal engineers","200+ lawyers co-build and tune per firm."),
        ("Lighthouse program","Co-developed with Allen & Overy, PwC."),
        ("Benchmark authorship","Publishes the Legal Agent Benchmark — defines 'good.'"),
        ("Compliance as product","SOC 2, residency, matter-level permissioning.")],
   verbatim="AI designed for legal and professional services — focus on what only lawyers can do.",
   pos_notes=["Scrapped its own model in 2025 when frontier models beat it — and revenue accelerated.",
              "Defensibility is the layer above (workflow/data) and below (compliance), never the weights.",
              "Vertical agent now verticalizing by industry; calibrated augment → autopilot glide."],
   moat=[("Data flywheel","100K lawyers' corrections train it."),("Workflow lock-in","Matter/doc/billing systems."),
         ("Compliance moat","Privilege, bar ethics, residency."),("Social-proof cascade","5 AmLaw firms → next 20."),
         ("Benchmark authority","Defines the category.")],
   gtm=["~$1,200/lawyer/month, 20-seat minimums + custom-model fees.","Moving toward outcome pricing for narrow tasks.","Lighthouse → marquee references → social-proof cascade; $150M Azure tie."],
   traction=[("3x","ARR in 10 mo"),("56x","revenue multiple"),("60+","countries")],
   proof="$100M (Aug '25) → $190M (Jan '26) → ~$300M (Jun '26); valuation $1.5B → $11B.",
   competitors=[("Legora","Collaborative legal AI, $5.6B, strong in Europe/M&A."),
                ("Spellbook / Robin / Luminance","Contract-centric tools."),
                ("EvenUp","Personal-injury sub-vertical squeeze, $2B+."),
                ("OpenAI / Gemini bundles","Held off by compliance + proprietary data, not capability.")],
   edge="Elite install base + embedded legal engineering + benchmark authorship + compliance depth.",
   lessons=["Pick a high-stakes, slow-feedback 'golden zone' workflow.",
            "Concede the model; build the moat one layer up or down.",
            "Wrap software in services — embedded domain engineers.",
            "Co-develop with marquee partners, then weaponize the social-proof cascade.",
            "Author the benchmark to own the definition of 'good.'"]),

 dict(slug="sierra", name="Sierra", tagline="Get paid only when the AI resolves the case",
   pattern="Pattern 3 · Services-as-Software + Outcome Pricing",
   one_line="Outcome pricing as the entire positioning — sold on brand relationship, not cost-cutting.",
   snapshot=[("2023","Founded · SF"),("$0→$165M","ARR"),("$15.8B","Valuation"),
             ("~$1.6B","Total raised"),("40%","of the Fortune 50"),("$0.10–$1","per resolution")],
   origin=["Bret Taylor (ex-Salesforce co-CEO, OpenAI chair, Google Maps) + Clay Bavor (18 yrs Google).",
           "Met at Google in 2005; reunited over lunch in 2023.",
           "Went vertical + narrow (customer service) when everyone else went horizontal."],
   why_win="Founder brand + enterprise-software instinct IS the GTM in a trust-gated market.",
   problem=["$400B/yr spent on customer service — 'the last analog channel.'",
            "A human-handled US call costs ~$10.",
            "Sierra's per-resolution cost is $0.10–$1.00 — the unit economics pick the customer."],
   icp=["Fortune 1000 with >$100M/yr contact-center spend.","Heavily regulated: financial services, healthcare.","50% of customers have >$1B revenue, 20% >$10B."],
   solution=["Agent OS — one agent across chat, voice/IVR, WhatsApp, email, ChatGPT, 34+ languages.",
             "Ghostwriter builds a production agent from SOPs — live in weeks, no engineering.",
             "Agent Data Platform — memory + systems of record; support → sales → loyalty."],
   usp=[("Outcome pricing","Paid only on resolution; escalation is free."),
        ("Speed-to-live","Production agent in weeks, no engineers — the real lever."),
        ("Brand-aligned","'Show up at your best,' not cost-cutting."),
        ("Regulated trust","FS/healthcare guardrails + Taylor's enterprise credibility."),
        ("Agent Data Platform","Memory + decisioning compound per customer.")],
   verbatim="Pay for a job well done.",
   pos_notes=["Pricing manifesto (Dec 2024): paid only when the AI resolves with no human; sales = commission.",
              "Framed as deeper customer relationships, not short-term cost-cutting — a larger budget.",
              "Replacement-leaning, but positioned on upside, not headcount."],
   moat=[("Outcome accountability","Pricing forces the product to work."),("Speed-to-live","Competitors underestimate it."),
         ("Enterprise brand trust","Fortune-50 references."),("Compliance","FS/healthcare guardrails."),
         ("Data flywheel","Agent Data Platform; NDR expands.")],
   gtm=["Per-resolution; sales = commission; escalation = free.","4 design partners → 11-month stealth build → marquee references.","~$400B TAM; 'digitize the last analog channel.'"],
   traction=[("7 qtrs","$0→$100M"),("40%","of Fortune 50"),("34+","languages")],
   proof="$0 → $100M ARR in 7 quarters → ~$165M (May 2026); $15.8B valuation.",
   competitors=[("Decagon","Per-resolution, $250M Series D; AI-native SaaS."),
                ("Intercom Fin","$0.99/resolution + $1M guarantee; mid-market."),
                ("Ada / Agentforce / PolyAI","CX and voice agents.")],
   edge="Regulated enterprise brand trust + multi-channel single agent + Agent Data Platform + founder pedigree.",
   lessons=["Make pricing the positioning — per-result billing forces quality and is the pitch.",
            "The lever under outcome pricing is speed-to-live.",
            "Go vertical + narrow first, then expand the agent's job.",
            "Found with a brand the buyer already trusts.",
            "Frame as relationship/upside, not cost-cutting — a bigger budget."]),

 dict(slug="cursor", name="Cursor", tagline="The fastest-scaling B2B software company in history",
   pattern="Pattern 8 · Interface Paradigm + Adapter",
   one_line="An AI-native code editor that augments the developer — and won with zero marketing spend.",
   snapshot=[("2022","Founded · SF · Anysphere"),("$1M→$2B","ARR"),("$60B","Valuation"),
             ("$3.4B+","Total raised"),("~50","people at $2B ARR"),("4","MIT-grad founders")],
   origin=["Michael Truell, Aman Sanger, Arvid Lunnemark, Sualeh Asif — MIT, no prior startups.",
           "Spent year one building the WRONG product (CAD / mechanical-engineering tools).",
           "Pivoted to an AI editor in 2023; Cmd+K + codebase indexing was the turning point."],
   why_win="Admitting you're building the wrong product for people you don't understand was the unlock.",
   problem=["AI coding tools were capped by bolting AI onto existing IDEs.",
            "The bet: reimagine the editor from first principles, controlling the IDE itself."],
   icp=["Individual professional developers — bottom-up, word of mouth.","60% enterprise revenue by 2026."],
   solution=["A fork of VS Code — fully compatible, zero switching cost.",
             "Tab predicts the next EDIT/diff with whole-codebase context (vs Copilot's current file).",
             "Composer (multi-file agentic editing), Background Agents (async).",
             "Proprietary models: Fusion (Tab), Composer (RL-trained)."],
   usp=[("Fastest autocomplete","Tab predicts edits across the codebase, not tokens."),
        ("Augment, not replace","The developer stays in the driver's seat."),
        ("Zero switching","VS Code fork — adopt in minutes."),
        ("Proprietary models","Cheap high-volume inference; margin-positive."),
        ("Word-of-mouth","$1M → $100M ARR with zero marketing spend.")],
   verbatim="AI makes developers 10x more productive — and developers stay central.",
   pos_notes=["Interface paradigm (own the editor) + Adapter (VS Code fork = no switching).",
              "Augment pole — the deliberate opposite of Devin's 'replace the engineer.'",
              "Vertically integrated the model once it had the usage data — flipped margins."],
   moat=[("Bottom-up lock-in","Workflows/prompts/codebase adapt to Cursor."),("Proprietary models","Cost + capability edge."),
         ("Brand","'Fastest-scaling SaaS ever' is its own funnel."),("Capital","$3.4B+, now SpaceX/xAI."),
         ("Daily-use hook","Tab is used constantly.")],
   gtm=["Free / Pro $20 (+$20 credits) / Business $40 / Enterprise custom.","Zero marketing — word of mouth from devs at OpenAI, Perplexity, Shopify.","Bottom-up individual → team → enterprise (60%)."],
   traction=[("Fastest","to $1B & $2B ARR"),("~50","people at $2B"),("60%","enterprise revenue")],
   proof="$1M (Dec '23) → $100M (Oct '24) → $2B (Feb '26); valuation $400M → $60B.",
   competitors=[("GitHub Copilot","Distribution — 90% of Fortune 100, $10/mo."),
                ("Claude Code","Terminal-native, developer mindshare."),
                ("Replit / Lovable","Non-developer builder canvas."),
                ("Cognition / Devin + Windsurf","Autonomous-agent pole.")],
   edge="Revenue leader + augment clarity + proprietary models + word-of-mouth gravity.",
   lessons=["Own the surface — a fork is Adapter and new-paradigm at once.",
            "Pick augment-vs-replace loudly; clarity beat muddier rivals.",
            "Word-of-mouth bottom-up beats a sales team when value is obvious in minutes.",
            "Vertically integrate the model once you have the usage data."]),

 dict(slug="cognition", name="Cognition · Devin", tagline="The AI software engineer",
   pattern="Pattern 5 · Replacement (the autopilot pole)",
   one_line="Branded full autonomy before models could deliver it — then bought the opposite pole (Windsurf).",
   snapshot=[("2023","Founded · NYC→SF"),("$492M","run-rate (May '26)"),("$26B","Valuation"),
             ("<$20M","lifetime net burn"),("350+","enterprise customers"),("Scott Wu","CEO · IOI gold")],
   origin=["A small group of engineers, a decade of friendship, a New York apartment.",
           "Scott Wu — competitive-programming gold medalist, ex-founding engineer at Scale AI.",
           "Launched Devin on March 12, 2024 as 'the world's first AI software engineer.'"],
   why_win="Claim the pole loudly; let the models catch up to the positioning.",
   problem=["'Software abundance — engineers become architects, tasking an army of agents.'",
            "30M software engineers, each to be made ~10x more productive."],
   icp=["Enterprise engineering teams where 'Devin is already a top contributor.'","350+ enterprise customers (via Windsurf)."],
   solution=["Devin — autonomous agent: plan, write, debug, deploy async (Jira ticket → PR).",
             "Windsurf — the agentic IDE for hands-on, decision-by-decision work.",
             "Now owns both forms: agent (delegate) + IDE (augment).",
             "SWE-1.6 model; Devin in Windsurf; Devin Desktop."],
   usp=[("Full autonomy","'The AI software engineer,' not an assistant."),
        ("Complete suite","IDE + agent after the Windsurf acquisition."),
        ("Usage pricing","~by the hour, ~10x cheaper than your time."),
        ("Capital efficiency","<$20M net burn to a $26B valuation."),
        ("Elite talent","Olympiad + Scale AI pedigree.")],
   verbatim="Devin, the AI software engineer.",
   pos_notes=["Replacement pole — the explicit opposite of Cursor's augment.",
              "Early Devin made mistakes ('ahead of its time'); the bet was models would catch up.",
              "Bought Windsurf (Jul 2025) to also own the augment IDE — spanning both poles."],
   moat=[("Category brand","First mover on full autonomy."),("Enterprise GTM","Windsurf's 350+ + scaled machine."),
         ("Two-product suite","IDE + agent under one roof."),("Capital efficiency","<$20M burn = optionality."),
         ("Talent","Competitive-programming pedigree.")],
   gtm=["Usage-based, ~by the hour, '~10x cheaper than the value of your time.'","Retired Core / Team ($500/mo) for a 5-tier ladder (Apr 2026).","Windsurf supplied a scaled GTM machine + bottom-up IDE funnel."],
   traction=[("$1M→$73M","Devin ARR / 9 mo"),("$492M","run-rate"),("<$20M","net burn")],
   proof="Devin $1M → $73M ARR in 9 months; company-wide $492M run-rate; $26B valuation.",
   competitors=[("Cursor","Augment pole, $2–3B ARR, the revenue leader."),
                ("GitHub Copilot / Claude Code / Codex","Assistant–agent hybrids.")],
   edge="Full-autonomy brand + IDE-plus-agent suite + enterprise base + capital efficiency.",
   lessons=["Brand the category before the tech is ready — let models catch up.",
            "Pick the pole loudly; 'assign-a-ticket-get-a-PR' is a bigger sale than autocomplete.",
            "Buy the opposite pole when you can (Windsurf).",
            "Capital efficiency is itself a positioning asset."]),
]

for D in DATA:
    make_deck(D)
print("ALL 4 DOSSIER DECKS BUILT")
