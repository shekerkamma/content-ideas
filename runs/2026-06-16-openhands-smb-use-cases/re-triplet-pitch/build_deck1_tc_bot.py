#!/usr/bin/env python3
"""Deck 1 of 3 — Transaction Coordinator Bot (12 slides)"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, Brand, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor

OUT_DIR  = os.path.join(os.path.dirname(__file__), "decks")
OUT_PATH = os.path.join(OUT_DIR, "01-tc-bot-pitch.pptx")
FOOTER   = "Transaction Coordinator Bot · AI Engineering for Real Estate"
TOTAL    = 12
os.makedirs(OUT_DIR, exist_ok=True)

d = Deck(footer=FOOTER)
b = d.b

# ── shared helpers ────────────────────────────────────────────────────────────

def chip(s, text, left, top, w=Inches(2.2), h=Inches(0.32), bg=None, fg=None):
    bg = bg or b.TEAL
    fg = fg or b.NAVY
    d.rect(s, left, top, w, h, bg, radius=0.06)
    d.text(s, text, left+Inches(0.12), top+Inches(0.04), w-Inches(0.18), h-Inches(0.06),
           size=10, color=fg, bold=True)

def stat_tile(s, num, label, note, left, top, w=Inches(3.8), h=Inches(1.8),
              num_color=None, bg=None):
    bg = bg or b.NAVY
    num_color = num_color or b.TEAL
    d.rect(s, left, top, w, h, bg, radius=0.06, shadow=True)
    d.text(s, num,   left+Inches(0.22), top+Inches(0.2),  w-Inches(0.3), Inches(0.7),
           size=36, color=num_color, bold=True, shrink=True)
    d.text(s, label, left+Inches(0.22), top+Inches(0.95), w-Inches(0.3), Inches(0.4),
           size=12, color=b.WHITE, bold=True, shrink=True)
    d.text(s, note,  left+Inches(0.22), top+Inches(1.38), w-Inches(0.3), Inches(0.35),
           size=9.5, color=b.LIGHT_TEAL, shrink=True)

def feature_card(s, num, title, body, left, top, w=Inches(5.9), h=Inches(2.4)):
    d.rect(s, left, top, w, h, b.WHITE, radius=0.05, shadow=True)
    d.rect(s, left, top, Inches(0.08), h, b.TEAL, radius=0.02)
    d.text(s, str(num), left+Inches(0.18), top+Inches(0.14),
           Inches(0.36), Inches(0.36), size=14, color=b.TEAL, bold=True)
    d.text(s, title, left+Inches(0.65), top+Inches(0.14),
           w-Inches(0.82), Inches(0.42), size=13, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, left+Inches(0.18), top+Inches(0.62), w-Inches(0.36), Inches(0.03), b.SOFT)
    d.text(s, body, left+Inches(0.18), top+Inches(0.74),
           w-Inches(0.36), h-Inches(0.86), size=10.5, color=b.INK, shrink=True, ls=1.2)

def process_step(s, n, title, desc, left, top, w=Inches(12.1)):
    h = Inches(0.72)
    bg = b.TEAL if n % 2 == 1 else b.NAVY_2
    d.rect(s, left, top, Inches(0.52), h, bg, radius=0.04)
    d.text(s, str(n), left, top+Inches(0.12), Inches(0.52), Inches(0.48),
           size=16, color=b.WHITE if bg==b.NAVY_2 else b.NAVY,
           bold=True, align=PP_ALIGN.CENTER)
    d.rect(s, left+Inches(0.62), top, w-Inches(0.62), h, b.SOFT, radius=0.04)
    d.text(s, title, left+Inches(0.82), top+Inches(0.06),
           Inches(3.5), Inches(0.32), size=11.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, desc, left+Inches(0.82), top+Inches(0.38),
           w-Inches(1.1), Inches(0.3), size=10, color=b.INK, shrink=True)

def timeline_row(s, week, title, items, top):
    d.rect(s, d.M, top, Inches(1.1), Inches(1.35), b.TEAL, radius=0.04)
    d.text(s, week, d.M, top+Inches(0.18), Inches(1.1), Inches(0.4),
           size=11, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, title, d.M+Inches(1.2), top+Inches(0.06),
           Inches(4.0), Inches(0.38), size=12, color=b.NAVY, bold=True, shrink=True)
    for i, item in enumerate(items):
        d.rect(s, d.M+Inches(1.2)+Inches(0.12), top+Inches(0.48)+i*Inches(0.3),
               Inches(0.12), Inches(0.12), b.TEAL, radius=0.04)
        d.text(s, item, d.M+Inches(1.48), top+Inches(0.44)+i*Inches(0.3),
               Inches(10.5), Inches(0.3), size=10, color=b.INK, shrink=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, d.W-Inches(0.18), 0, Inches(0.18), d.H, b.TEAL)
d.rect(s, 0, d.H-Inches(0.12), d.W, Inches(0.12), b.TEAL)
d.text(s, "DONE-FOR-YOU AI ENGINEERING · REAL ESTATE", d.M, Inches(1.0),
       Inches(10), Inches(0.38), size=12, color=b.TEAL, bold=True)
d.text(s, "Transaction\nCoordinator Bot", d.M, Inches(1.52),
       Inches(10), Inches(2.6), size=60, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(4.3), Inches(5.5), Inches(0.06), b.TEAL)
d.text(s, "Your AI-powered TC that never misses a deadline, chases every document,\nand keeps every party informed — without you touching it.",
       d.M, Inches(4.5), Inches(10.5), Inches(0.9), size=16, color=b.LIGHT_TEAL, ls=1.3, shrink=True)
chip(s, "Closes unlimited transactions", d.M, Inches(5.6), w=Inches(2.8))
chip(s, "$2,500/month flat", d.M+Inches(3.0), Inches(5.6), w=Inches(1.8), bg=b.GOLD)
chip(s, "Setup in 1 week", d.M+Inches(5.0), Inches(5.6), w=Inches(1.6), bg=b.AMBER)
d.footer(s, 1, TOTAL, dark=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
d.rect(s, 0, Inches(0.12), d.W, Inches(1.2), b.NAVY)
d.text(s, "THE PROBLEM", d.M, Inches(0.18), Inches(6), Inches(0.28),
       size=10, color=b.TEAL, bold=True)
d.text(s, '"I\'m paying my TC $2,000 a month and half the time\nI still have to chase people myself."',
       d.M, Inches(0.48), d.CW, Inches(0.78), size=20, color=b.WHITE, italic=True, shrink=True)
# three pain cards
pain_cards = [
    ("You're paying for something that still breaks",
     "Human TCs handle paperwork but miss contingency dates, forget to follow up with title, and go on vacation during your busiest closing week."),
    ("Every missed deadline is money — or worse",
     "One missed contingency can give the buyer grounds to walk. One missed inspection date can trigger a contract renegotiation. One forgotten doc delays close by a week."),
    ("You become the fallback",
     "When your TC drops the ball, you find out when the lender calls you directly. Now you're doing TC work on top of listing appointments."),
]
cw3 = (d.CW - Inches(0.4)) / 3
for i, (title, body) in enumerate(pain_cards):
    cx = d.M + i*(cw3+Inches(0.2))
    d.rect(s, cx, Inches(1.5), cw3, Inches(4.3), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, cx, Inches(1.5), cw3, Inches(0.06), b.CORAL, radius=0.02)
    d.text(s, title, cx+Inches(0.2), Inches(1.68), cw3-Inches(0.3), Inches(0.72),
           size=13, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, cx+Inches(0.2), Inches(2.46), cw3-Inches(0.4), Inches(0.03), b.GRID)
    d.text(s, body, cx+Inches(0.2), Inches(2.58), cw3-Inches(0.3), Inches(2.9),
           size=11, color=b.INK, shrink=True, ls=1.25)
d.text(s, "The bot eliminates all three. It never sleeps, never goes on vacation, and never forgets.",
       d.M, Inches(6.05), d.CW, Inches(0.38), size=12, color=b.ACCENT, bold=True, shrink=True)
d.footer(s, 2, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — WHAT THIS ACTUALLY COSTS YOU
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "What a Manual Transaction Process Actually Costs You",
         "The numbers agents don't add up — until they do")
stats = [
    ("$300–$500", "per transaction", "TC fee, paid whether close happens or not"),
    ("$2,000–$4,000", "per month", "At 6–8 closings: TC cost before your own time"),
    ("2–4 hrs", "per transaction", "Agent time chasing docs, parties, and deadlines"),
    ("1 in 12", "deals fall apart", "Due to missed contingency or document delay"),
]
sw = (d.CW - Inches(0.6)) / 4
for i, (num, label, note) in enumerate(stats):
    stat_tile(s, num, label, note, d.M + i*(sw+Inches(0.2)), Inches(1.85), w=sw)
# cost scenario box
d.rect(s, d.M, Inches(3.9), d.CW, Inches(1.5), b.SOFT, radius=0.05)
d.text(s, "Scenario: You close 8 deals this month",
       d.M+Inches(0.25), Inches(4.0), Inches(6), Inches(0.38),
       size=12, color=b.NAVY, bold=True)
scenario_items = [
    ("TC fees:", "$400 × 8 = $3,200"),
    ("Your time (2 hrs × 8):", "16 hours — at $250/hr opportunity cost = $4,000"),
    ("1 deal falls through (1 in 12):", "$12,000 in lost commission"),
    ("Total exposure:", "$7,200 in direct cost + $12,000 risk = $19,200"),
]
for i, (label, val) in enumerate(scenario_items):
    lx = d.M + Inches(0.25)
    ly = Inches(4.45) + i*Inches(0.22)
    d.text(s, label, lx, ly, Inches(3.5), Inches(0.2), size=10.5, color=b.MUTED, bold=True)
    d.text(s, val, lx+Inches(3.6), ly, Inches(7.5), Inches(0.2), size=10.5, color=b.INK)
d.rect(s, d.M, Inches(5.58), d.CW, Inches(0.72), b.NAVY, radius=0.05)
d.text(s, "The bot costs $2,500/month. At 8 closings, you're saving $700 in TC fees alone — and eliminating the 16 hours and the deal-fall-through risk entirely.",
       d.M+Inches(0.25), Inches(5.64), d.CW-Inches(0.4), Inches(0.6),
       size=11.5, color=b.GOLD, bold=True, shrink=True)
d.footer(s, 3, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — WHAT THE BOT DOES (6 CAPABILITIES)
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Six Things the Bot Does Automatically",
         "Every capability that a human TC does — plus the ones they forget")
caps = [
    ("Contract Intake", "Upload the signed purchase agreement — the bot reads it, extracts every date, and opens the deal file in under 2 minutes."),
    ("Calendar Population", "All contingency dates auto-populate into Google Calendar with reminders for every party — buyer, seller, title, lender, and you."),
    ("Daily Status Emails", "Every party receives a daily deal status digest: what's complete, what's due in the next 48 hours, and who owes what."),
    ("Document Chase Sequences", "Missing doc? The bot sends a polite ask on day 1, a firmer ask on day 3, and flags you on day 5. You only intervene for true exceptions."),
    ("Milestone Confirmations", "When each contingency clears — inspection, financing, title — all parties receive an automatic confirmation with the next milestone due."),
    ("File Close + Archive", "When the last document lands, the bot closes the deal file, generates a transaction summary, and archives everything to your Notion workspace."),
]
cw2 = (d.CW - Inches(0.2)) / 2
for i, (title, body) in enumerate(caps):
    row, col = divmod(i, 2)
    cx = d.M + col*(cw2+Inches(0.2))
    cy = Inches(1.75) + row*Inches(1.72)
    feature_card(s, i+1, title, body, cx, cy, w=cw2, h=Inches(1.62))
d.footer(s, 4, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — HOW A DEAL RUNS (7-STEP PROCESS)
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "How a Deal Runs — From Executed Contract to Close",
         "Seven automated steps. You only appear when something needs a human decision.")
steps = [
    ("Contract Upload", "You or your assistant uploads the signed purchase agreement to the deal portal. Takes 60 seconds."),
    ("Auto-Extraction", "Bot reads the contract, extracts all dates, parties, and contingency conditions. Deal file opens automatically."),
    ("Calendar + Welcome", "Google Calendar populated for all parties. Welcome email sent to buyer, seller, title company, and lender within 5 minutes."),
    ("Daily Check-Ins", "Every morning, automated status digest goes to all parties. Every evening, bot checks for document completeness."),
    ("Chase Sequences", "Any missing document triggers a polite follow-up sequence: Day 1 ask → Day 3 reminder → Day 5 escalation to you."),
    ("Milestone Confirmations", "Inspection cleared? Financing approved? Each milestone triggers an automatic confirmation and updates the deal timeline."),
    ("Close + Archive", "Final walkthrough confirmed, title cleared, keys exchanged — bot closes the file, sends a transaction summary, archives to Notion."),
]
for i, (title, desc) in enumerate(steps):
    process_step(s, i+1, title, desc, d.M, Inches(1.75)+i*Inches(0.78))
d.footer(s, 5, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — DAILY AUTOMATED COMMUNICATION
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "What Automated Communication Looks Like",
         "Every party stays informed. Nobody calls you wondering what's happening.")
# left: what each party receives
d.rect(s, d.M, Inches(1.75), Inches(5.8), Inches(5.0), b.SOFT, radius=0.05)
d.text(s, "WHAT EACH PARTY RECEIVES", d.M+Inches(0.2), Inches(1.85),
       Inches(5.4), Inches(0.28), size=9.5, color=b.TEAL, bold=True)
parties = [
    ("You (the agent)", b.TEAL,
     ["Daily deal summary — all active transactions", "Exception alerts when something needs your decision",
      "Weekly close pipeline report"]),
    ("Buyer + Buyer's Agent", b.GOLD,
     ["Daily status: what's complete, what's next", "Document request with clear deadline",
      "Contingency clearance confirmations"]),
    ("Title Company", b.AMBER,
     ["Open title order confirmation", "Daily doc checklist status",
      "Close date confirmation 72 hours out"]),
    ("Lender", b.CORAL,
     ["Appraisal order confirmation", "Financing contingency deadline reminder",
      "Clear-to-close request with deadline"]),
]
for i, (name, color, items) in enumerate(parties):
    py = Inches(2.22) + i*Inches(1.12)
    d.rect(s, d.M+Inches(0.2), py, Inches(0.08), Inches(0.86), color)
    d.text(s, name, d.M+Inches(0.42), py+Inches(0.04), Inches(2.0), Inches(0.28),
           size=10.5, color=b.NAVY, bold=True)
    for j, item in enumerate(items):
        d.text(s, f"· {item}", d.M+Inches(0.42), py+Inches(0.34)+j*Inches(0.22),
               Inches(5.0), Inches(0.2), size=9.5, color=b.INK, shrink=True)
# right: sample email mock
RX = d.M + Inches(6.1)
RW = d.CW - Inches(6.1)
d.rect(s, RX, Inches(1.75), RW, Inches(5.0), b.NAVY, radius=0.05, shadow=True)
d.text(s, "SAMPLE: DAILY STATUS EMAIL", RX+Inches(0.2), Inches(1.88),
       RW-Inches(0.3), Inches(0.26), size=8.5, color=b.TEAL, bold=True)
d.rect(s, RX+Inches(0.2), Inches(2.2), RW-Inches(0.4), Inches(0.03), b.NAVY_2)
email_lines = [
    ("From:", "TC Bot <tc@yourbrokerage.com>"),
    ("To:", "sarah.johnson@email.com"),
    ("Subject:", "Deal Update — 1234 Oak Street [Day 8 of 30]"),
    ("", ""),
    ("", "Hi Sarah,"),
    ("", ""),
    ("✅  Complete:", "Earnest money received"),
    ("✅  Complete:", "Inspection scheduled (Tue Jun 18, 10am)"),
    ("⏳  Due Fri:", "Lender pre-approval letter"),
    ("⏳  Due Fri:", "HOA docs from seller"),
    ("📋  Next up:", "Financing contingency deadline — Jun 24"),
]
for i, (label, val) in enumerate(email_lines):
    ly = Inches(2.3) + i*Inches(0.26)
    if label:
        d.text(s, label, RX+Inches(0.2), ly, Inches(1.2), Inches(0.24),
               size=9, color=b.MUTED, bold=True)
        d.text(s, val, RX+Inches(1.45), ly, RW-Inches(1.65), Inches(0.24),
               size=9, color=b.WHITE, shrink=True)
    else:
        d.text(s, val, RX+Inches(0.2), ly, RW-Inches(0.3), Inches(0.24),
               size=9, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 6, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — DOCUMENT TRACKING + CHASE SEQUENCES
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Document Tracking + Automatic Chase Sequences",
         "Every missing document triggers a three-step escalation. You only appear at step 4.")
# timeline of chase
chase_steps = [
    (b.TEAL,  "Day 1 — Polite Ask",
     "Automated email to the responsible party: 'Hi [Name], just a reminder that [Document] is due by [Date]. Please upload to the deal portal at your convenience. Let me know if you have questions.'"),
    (b.AMBER, "Day 3 — Firm Reminder",
     "Second automated email with urgency: 'Hi [Name], [Document] is now 2 days overdue. This is required to keep the [Date] contingency on track. Please upload today.'"),
    (b.CORAL, "Day 5 — Escalation Alert",
     "You receive a text and email: 'ACTION NEEDED: [Document] is 4 days overdue from [Party]. Contingency deadline is [Date]. Recommend you call directly.'"),
    (b.GOLD,  "You Step In (Exceptions Only)",
     "You make one call. The bot logs the outcome, resets the chase timer if needed, and handles all follow-up communication from there."),
]
for i, (color, title, body) in enumerate(chase_steps):
    cy = Inches(1.75) + i*Inches(1.3)
    d.rect(s, d.M, cy, Inches(0.08), Inches(1.1), color)
    d.rect(s, d.M+Inches(0.18), cy, d.CW-Inches(0.18), Inches(1.1), b.SOFT, radius=0.04)
    d.text(s, title, d.M+Inches(0.4), cy+Inches(0.1),
           Inches(4.0), Inches(0.34), size=12.5, color=b.NAVY, bold=True)
    d.text(s, body, d.M+Inches(0.4), cy+Inches(0.48),
           d.CW-Inches(0.65), Inches(0.56), size=10.5, color=b.INK, shrink=True, ls=1.2)
d.rect(s, d.M, Inches(7.0), d.CW, Inches(0.28), b.LIGHT_TEAL, radius=0.03)
d.text(s, "Result: 92% of missing documents are received before you ever need to make a call.",
       d.M+Inches(0.2), Inches(7.02), d.CW-Inches(0.3), Inches(0.24),
       size=10.5, color=b.ACCENT, bold=True, shrink=True)
d.footer(s, 7, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — TECHNOLOGY STACK
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The Technology Behind It", "Three layers — all connected, all automated, all yours.")
layers = [
    ("INTELLIGENCE LAYER", b.NAVY, b.TEAL, b.WHITE,
     "OpenHands AI Agent Runtime",
     "The AI engine that reads contracts, makes decisions, and orchestrates every task. Open-source, self-hosted — your data never leaves your environment.",
     ["Reads and interprets purchase agreements", "Makes scheduling + sequencing decisions",
      "Escalates intelligently based on urgency", "Runs 24/7 with zero downtime"]),
    ("INTEGRATION LAYER", b.NAVY_2, b.AMBER, b.WHITE,
     "MCP Server Connections",
     "Pre-built connections to every tool your deal needs. No custom coding per integration — plug in, configure, run.",
     ["Google Calendar — all parties, all deadlines", "Gmail — branded email sequences",
      "Twilio — SMS alerts for you + parties", "Notion — deal file archive + reporting"]),
    ("OVERSIGHT LAYER", b.SOFT, b.ACCENT, b.NAVY,
     "Your Agent Dashboard",
     "One view of every active transaction. See what the bot did, what's pending, and where exceptions need your attention. Accessible from any device.",
     ["Live deal pipeline view", "Exception queue (only what needs you)",
      "Document completion status per deal", "Weekly close forecast"]),
]
lw = (d.CW - Inches(0.4)) / 3
for i, (label, bg, accent, fg, name, desc, feats) in enumerate(layers):
    lx = d.M + i*(lw+Inches(0.2))
    d.rect(s, lx, Inches(1.75), lw, Inches(5.2), bg, radius=0.06, shadow=True)
    d.text(s, label, lx+Inches(0.18), Inches(1.86), lw-Inches(0.3), Inches(0.26),
           size=8.5, color=accent, bold=True)
    d.text(s, name, lx+Inches(0.18), Inches(2.18), lw-Inches(0.3), Inches(0.52),
           size=13.5, color=fg, bold=True, shrink=True)
    d.rect(s, lx+Inches(0.18), Inches(2.76), lw-Inches(0.36), Inches(0.03), accent)
    d.text(s, desc, lx+Inches(0.18), Inches(2.88), lw-Inches(0.3), Inches(1.1),
           size=10, color=b.LIGHT_TEAL if bg==b.NAVY or bg==b.NAVY_2 else b.INK,
           shrink=True, ls=1.2)
    for j, f in enumerate(feats):
        fy = Inches(4.08) + j*Inches(0.48)
        d.rect(s, lx+Inches(0.18), fy+Inches(0.06), Inches(0.1), Inches(0.1), accent, radius=0.04)
        d.text(s, f, lx+Inches(0.36), fy, lw-Inches(0.5), Inches(0.42),
               size=9.5, color=fg if bg != b.SOFT else b.INK, shrink=True)
d.footer(s, 8, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — ROI COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The ROI Comparison — Before and After",
         "At 6+ transactions/month, the bot pays for itself. Above that, it generates margin.")
rows = [
    ("",                     "Human TC (Current)",        "TC Bot (This Service)",     True),
    ("Cost per transaction",  "$300–$500 per deal",        "$0 — flat monthly rate",    False),
    ("Monthly cost at 6 deals","$1,800–$3,000",            "$2,500 flat",               False),
    ("Monthly cost at 10 deals","$3,000–$5,000",           "$2,500 flat",               False),
    ("Your time per deal",    "2–4 hours chasing",         "< 15 min (exceptions only)",False),
    ("Works nights/weekends", "No",                        "Yes — 24/7",                False),
    ("Vacation coverage",     "Covered by you",            "Uninterrupted",             False),
    ("Contingency miss rate", "~8% (industry avg)",        "< 1% (automated tracking)", False),
    ("Scales to more deals",  "Costs more per deal",       "Same price regardless",     False),
]
col_w = [Inches(3.5), Inches(4.2), Inches(4.2)]
col_x = [d.M, d.M+Inches(3.6), d.M+Inches(7.9)]
rh = Inches(0.5)
for ri, row in enumerate(rows):
    for ci, cell in enumerate(row[:3]):
        ry = Inches(1.82) + ri*rh
        is_hdr = ri == 0
        is_bot = ci == 2 and not is_hdr
        bg = b.NAVY if is_hdr else (b.LIGHT_TEAL if is_bot else (b.WHITE if ri%2==0 else b.SOFT))
        d.rect(s, col_x[ci], ry, col_w[ci]-Inches(0.06), rh-Inches(0.03), bg)
        tc = b.WHITE if is_hdr else (b.ACCENT if is_bot else b.INK)
        d.text(s, cell, col_x[ci]+Inches(0.12), ry+Inches(0.1),
               col_w[ci]-Inches(0.22), rh-Inches(0.12), size=10.5 if not is_hdr else 10,
               color=tc, bold=(is_hdr or is_bot), shrink=True)
d.rect(s, d.M, Inches(6.35), d.CW, Inches(0.55), b.NAVY, radius=0.05)
d.text(s, "Break-even: 5 transactions/month. Every deal above that is pure margin. Most active agents close 6–12.",
       d.M+Inches(0.2), Inches(6.42), d.CW-Inches(0.3), Inches(0.42),
       size=12, color=b.GOLD, bold=True, shrink=True)
d.footer(s, 9, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — WHAT'S INCLUDED
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "What's Included in Your Monthly Subscription",
         "Everything you need to run TC operations on autopilot — no add-ons, no surprises.")
included = [
    ("Deal Intake System",      "Web-based deal portal. You or your assistant uploads the purchase agreement — that's it. Works from any device."),
    ("Contract Intelligence",   "Auto-extraction of all dates, parties, and contingency conditions from any standard purchase agreement."),
    ("Google Calendar Sync",    "All deal dates populate automatically for every party. Contingency reminders set 7 days, 3 days, and 24 hours in advance."),
    ("Email Automation",        "Branded daily status emails for all parties. Templates customized with your brokerage name and headshot."),
    ("SMS Alerts",              "Text notifications for you on exceptions and escalations. Optional buyer/seller SMS for critical deadlines."),
    ("Document Chase System",   "Three-step escalation sequence for every missing document. You only get pulled in on day 5 exceptions."),
    ("File Archive",            "Completed deals archived to Notion. Every document, every communication, every date — searchable forever."),
    ("Monthly Support Check-In","30-minute call each month to review performance, adjust templates, and handle any edge cases from your market."),
]
iw = (d.CW - Inches(0.2)) / 2
for i, (title, body) in enumerate(included):
    row, col = divmod(i, 2)
    ix = d.M + col*(iw+Inches(0.2))
    iy = Inches(1.75) + row*Inches(1.24)
    d.rect(s, ix, iy, iw, Inches(1.14), b.WHITE, radius=0.04, shadow=True)
    d.rect(s, ix, iy, Inches(0.07), Inches(1.14), b.TEAL)
    d.text(s, f"✓  {title}", ix+Inches(0.18), iy+Inches(0.1),
           iw-Inches(0.28), Inches(0.34), size=11.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, ix+Inches(0.18), iy+Inches(0.48),
           iw-Inches(0.28), Inches(0.6), size=10, color=b.INK, shrink=True, ls=1.15)
d.footer(s, 10, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — SETUP TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Four-Week Setup — From Signed Agreement to First Automated Deal",
         "Your first fully automated transaction closes before the end of month one.")
timeline = [
    ("Week 1", "Configure + Connect",
     ["Connect Google Calendar and Gmail with your brokerage credentials",
      "Set up deal portal with your forms and branding",
      "Configure email templates with your name, headshot, and brokerage"]),
    ("Week 2", "Test + Calibrate",
     ["Run a test deal through the full pipeline with a past transaction",
      "Review email output and adjust tone/language to match your voice",
      "Confirm all party notifications arrive correctly"]),
    ("Week 3", "First Live Deal",
     ["Your first real transaction runs through the bot",
      "We monitor in real-time and handle any edge cases",
      "You observe — approve or override anything that needs your judgment"]),
    ("Week 4", "Hand Off + Optimize",
     ["You run the second deal independently",
      "30-minute debrief call: what worked, what to adjust",
      "Bot running autonomously — you supervise from the dashboard"]),
]
for i, (week, title, items) in enumerate(timeline):
    timeline_row(s, week, title, items, Inches(1.9) + i*Inches(1.38))
d.rect(s, d.M, Inches(7.08), d.CW, Inches(0.26), b.LIGHT_TEAL, radius=0.03)
d.text(s, "Setup fee: $500 one-time (covers weeks 1–4 configuration and onboarding support)",
       d.M+Inches(0.2), Inches(7.1), d.CW-Inches(0.3), Inches(0.22),
       size=10, color=b.ACCENT, shrink=True)
d.footer(s, 11, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — PRICING + NEXT STEPS
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, Inches(0.12), d.H, b.TEAL)
d.rect(s, 0, d.H-Inches(0.12), d.W, Inches(0.12), b.TEAL)
d.text(s, "SIMPLE PRICING. NO SURPRISES.", d.M+Inches(0.2), Inches(0.65),
       Inches(10), Inches(0.38), size=12, color=b.TEAL, bold=True)
# price box
d.rect(s, d.M+Inches(0.2), Inches(1.15), Inches(5.5), Inches(2.4), b.NAVY_2, radius=0.08, shadow=True)
d.text(s, "$2,500", d.M+Inches(0.5), Inches(1.35), Inches(4.0), Inches(1.2),
       size=72, color=b.GOLD, bold=True, shrink=True)
d.text(s, "/ month", d.M+Inches(0.5), Inches(2.45), Inches(3.0), Inches(0.38),
       size=18, color=b.LIGHT_TEAL)
d.text(s, "+ $500 one-time setup fee · No long-term contract · Cancel with 30 days notice",
       d.M+Inches(0.5), Inches(2.92), Inches(5.0), Inches(0.48),
       size=10.5, color=b.MUTED, shrink=True)
# what you get bullets
d.text(s, "For $2,500/month you get:", d.M+Inches(6.2), Inches(1.15),
       Inches(6.5), Inches(0.38), size=12, color=b.TEAL, bold=True)
gets = ["Unlimited transactions — no per-deal fee",
        "All 8 included features (no add-ons)",
        "24/7 autonomous operation",
        "Monthly support check-in",
        "Cancel anytime — no lock-in"]
for i, g in enumerate(gets):
    d.rect(s, d.M+Inches(6.2), Inches(1.62)+i*Inches(0.52), Inches(0.14), Inches(0.14), b.TEAL, radius=0.04)
    d.text(s, g, d.M+Inches(6.5), Inches(1.58)+i*Inches(0.52), Inches(6.2), Inches(0.44),
           size=11.5, color=b.WHITE, shrink=True)
# next steps
d.rect(s, d.M+Inches(0.2), Inches(3.75), d.CW-Inches(0.2), Inches(0.06), b.TEAL)
d.text(s, "THREE STEPS TO GET STARTED", d.M+Inches(0.2), Inches(3.95),
       Inches(8), Inches(0.32), size=11, color=b.TEAL, bold=True)
steps3 = [
    ("1", "Book a 20-min intro call", "We review your current TC setup and confirm the bot is the right fit."),
    ("2", "Sign + pay setup fee", "We start configuration within 48 hours of your signed agreement."),
    ("3", "Run your first automated deal", "Week 3 — your first real transaction closes with the bot in the TC seat."),
]
for i, (n, title, body) in enumerate(steps3):
    sx = d.M + Inches(0.2) + i*Inches(4.2)
    d.rect(s, sx, Inches(4.38), Inches(0.44), Inches(0.44), b.TEAL, radius=0.08)
    d.text(s, n, sx, Inches(4.4), Inches(0.44), Inches(0.4),
           size=16, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, title, sx+Inches(0.6), Inches(4.4), Inches(3.4), Inches(0.36),
           size=12, color=b.WHITE, bold=True, shrink=True)
    d.text(s, body, sx+Inches(0.6), Inches(4.82), Inches(3.4), Inches(0.52),
           size=10, color=b.LIGHT_TEAL, shrink=True, ls=1.2)
d.rect(s, d.M+Inches(0.2), Inches(5.55), d.CW-Inches(0.2), Inches(0.06), b.NAVY_2)
d.text(s, "[your website or booking link here]",
       d.M+Inches(0.2), Inches(5.7), d.CW-Inches(0.2), Inches(0.38),
       size=14, color=b.GOLD, bold=True)
d.footer(s, 12, TOTAL, dark=True)

d.save(OUT_PATH)
print(f"Deck 1 saved: {OUT_PATH} ({d.n} slides)")
