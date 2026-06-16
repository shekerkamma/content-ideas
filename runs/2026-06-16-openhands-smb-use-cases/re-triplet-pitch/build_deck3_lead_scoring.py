#!/usr/bin/env python3
"""Deck 3 of 3 — Lead Scoring + CRM Drip System (12 slides)"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, Brand, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor

OUT_DIR  = os.path.join(os.path.dirname(__file__), "decks")
OUT_PATH = os.path.join(OUT_DIR, "03-lead-scoring-pitch.pptx")
FOOTER   = "Lead Scoring + CRM Drip System · AI Engineering for Real Estate"
TOTAL    = 12
os.makedirs(OUT_DIR, exist_ok=True)

d = Deck(footer=FOOTER)
b = d.b
AMBER = b.AMBER   # primary accent for this deck

def chip(s, text, left, top, w=Inches(2.4), h=Inches(0.32), bg=None, fg=None):
    bg = bg or AMBER
    fg = fg or b.NAVY
    d.rect(s, left, top, w, h, bg, radius=0.06)
    d.text(s, text, left+Inches(0.12), top+Inches(0.04), w-Inches(0.18), h-Inches(0.06),
           size=10, color=fg, bold=True)

def stat_tile(s, num, label, note, left, top, w=Inches(3.8), h=Inches(1.8), num_col=None):
    num_col = num_col or AMBER
    d.rect(s, left, top, w, h, b.NAVY, radius=0.06, shadow=True)
    d.text(s, num,   left+Inches(0.22), top+Inches(0.18), w-Inches(0.3), Inches(0.72),
           size=36, color=num_col, bold=True, shrink=True)
    d.text(s, label, left+Inches(0.22), top+Inches(0.95), w-Inches(0.3), Inches(0.4),
           size=12, color=b.WHITE, bold=True, shrink=True)
    d.text(s, note,  left+Inches(0.22), top+Inches(1.38), w-Inches(0.3), Inches(0.35),
           size=9.5, color=b.LIGHT_TEAL, shrink=True)

def feature_card(s, num, title, body, left, top, w=Inches(5.9), h=Inches(2.4)):
    d.rect(s, left, top, w, h, b.WHITE, radius=0.05, shadow=True)
    d.rect(s, left, top, Inches(0.08), h, AMBER, radius=0.02)
    d.text(s, str(num), left+Inches(0.18), top+Inches(0.14),
           Inches(0.36), Inches(0.36), size=14, color=AMBER, bold=True)
    d.text(s, title, left+Inches(0.65), top+Inches(0.14),
           w-Inches(0.82), Inches(0.42), size=13, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, left+Inches(0.18), top+Inches(0.62), w-Inches(0.36), Inches(0.03), b.SOFT)
    d.text(s, body, left+Inches(0.18), top+Inches(0.74),
           w-Inches(0.36), h-Inches(0.86), size=10.5, color=b.INK, shrink=True, ls=1.2)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, d.W-Inches(0.12), 0, Inches(0.12), d.H, AMBER)
d.rect(s, 0, d.H-Inches(0.12), d.W, Inches(0.12), AMBER)
d.text(s, "DONE-FOR-YOU AI ENGINEERING · REAL ESTATE", d.M, Inches(1.0),
       Inches(10), Inches(0.38), size=12, color=AMBER, bold=True)
d.text(s, "Lead Scoring +\nCRM Drip System", d.M, Inches(1.52),
       Inches(10), Inches(2.6), size=54, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(4.3), Inches(5.5), Inches(0.06), AMBER)
d.text(s, "Know who in your database is ready to buy or sell — before they call someone else.",
       d.M, Inches(4.5), Inches(10.5), Inches(0.62), size=16, color=b.LIGHT_TEAL, shrink=True)
chip(s, "Scores your entire database", d.M, Inches(5.35), w=Inches(2.8))
chip(s, "$3,000/month flat", d.M+Inches(3.0), Inches(5.35), w=Inches(1.8), bg=b.TEAL, fg=b.NAVY)
chip(s, "Finds deals you're missing now", d.M+Inches(5.0), Inches(5.35), w=Inches(2.6), bg=b.GOLD)
d.footer(s, 1, TOTAL, dark=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.rect(s, 0, 0, d.W, Inches(0.12), AMBER)
d.rect(s, 0, Inches(0.12), d.W, Inches(1.2), b.NAVY)
d.text(s, "THE PROBLEM", d.M, Inches(0.18), Inches(6), Inches(0.28),
       size=10, color=AMBER, bold=True)
d.text(s, '"I have 400 contacts in my phone and I have no idea\nwhich 20 of them are ready to transact right now."',
       d.M, Inches(0.46), d.CW, Inches(0.82), size=19, color=b.WHITE, italic=True, shrink=True)
pain_cards = [
    ("Your database is your biggest untapped asset",
     "Industry research shows 67% of buyers and sellers choose the first agent who contacts them at the right moment. Your database already has those people — you just can't see who they are."),
    ("You follow up by gut feeling — and miss the signal",
     "You call your sphere when you have time, not when they're ready. The 5% who are ready to move this quarter go cold because your last touch was three months ago."),
    ("Competitors stay top-of-mind while you're busy",
     "The agent who does reach out at the right moment — with the right message — wins the listing. It doesn't have to be you to lose."),
]
cw3 = (d.CW - Inches(0.4)) / 3
for i, (title, body) in enumerate(pain_cards):
    cx = d.M + i*(cw3+Inches(0.2))
    d.rect(s, cx, Inches(1.5), cw3, Inches(4.3), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, cx, Inches(1.5), cw3, Inches(0.06), AMBER, radius=0.02)
    d.text(s, title, cx+Inches(0.2), Inches(1.68), cw3-Inches(0.3), Inches(0.78),
           size=13, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, cx+Inches(0.2), Inches(2.52), cw3-Inches(0.4), Inches(0.03), b.GRID)
    d.text(s, body, cx+Inches(0.2), Inches(2.64), cw3-Inches(0.3), Inches(2.84),
           size=11, color=b.INK, shrink=True, ls=1.25)
d.text(s, "The Lead Scoring System reads your database and surfaces who's ready — every Monday morning.",
       d.M, Inches(6.05), d.CW, Inches(0.38), size=12, color=b.ACCENT, bold=True, shrink=True)
d.footer(s, 2, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — THE DATABASE IS ALREADY WORTH MONEY
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Your Database Is Already Worth $300K+ — You Just Can't See the Signal",
         "The deals are already in your contacts. The system finds them.")
stats = [
    ("400", "average contacts", "Typical active agent database size after 3+ years"),
    ("5–8%", "ready to transact", "Industry benchmark: 20–32 of your contacts are in buying/selling mode right now"),
    ("67%", "choose first contact", "Buyers and sellers pick the first agent who reaches out at the right moment"),
    ("$240K", "in your database", "20 contacts × 3% close rate × $400K avg price × 3% commission = $240K annual revenue potential"),
]
sw = (d.CW - Inches(0.6)) / 4
for i, (num, label, note) in enumerate(stats):
    stat_tile(s, num, label, note, d.M + i*(sw+Inches(0.2)), Inches(1.85), w=sw)
# what the system finds
d.rect(s, d.M, Inches(3.88), d.CW, Inches(0.38), b.NAVY)
d.text(s, "WHAT THE SYSTEM SURFACES FROM A TYPICAL 400-CONTACT DATABASE",
       d.M+Inches(0.2), Inches(3.94), d.CW-Inches(0.3), Inches(0.28),
       size=9.5, color=AMBER, bold=True)
findings = [
    ("Hot (transact in 30 days):",    "3–5 contacts",  "Life event, recent search activity, or direct inquiry signal detected"),
    ("Warm (transact in 90 days):",   "8–12 contacts", "Elevated engagement — opening emails, clicking listings, referral source"),
    ("Incubating (3–12 months):",     "18–25 contacts","Long-term nurture — periodic contact keeps you top-of-mind"),
    ("Dormant (no signal):",          "350+ contacts", "No action needed — bot keeps a light touch on auto-pilot"),
]
for i, (label, count, note) in enumerate(findings):
    fy = Inches(4.38) + i*Inches(0.58)
    d.rect(s, d.M, fy, d.CW, Inches(0.5), b.WHITE if i%2==0 else b.SOFT)
    d.text(s, label, d.M+Inches(0.15), fy+Inches(0.12), Inches(3.2), Inches(0.28),
           size=10.5, color=b.NAVY, bold=True)
    d.text(s, count, d.M+Inches(3.4), fy+Inches(0.12), Inches(1.5), Inches(0.28),
           size=11, color=AMBER, bold=True)
    d.text(s, note, d.M+Inches(5.0), fy+Inches(0.12), Inches(7.5), Inches(0.28),
           size=10, color=b.INK, shrink=True)
d.footer(s, 3, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — THE 12 SCORING SIGNALS
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "12 Signals That Predict Transaction Readiness",
         "The system watches all 12 simultaneously — you'd never have time to track even three manually.")
signals = [
    ("Recency of Last Contact",  "Days since last meaningful interaction with this contact"),
    ("Email Open Rate",          "Frequency of opening your emails in the last 90 days"),
    ("Listing Click Activity",   "Did they click on listing links? How many? How recently?"),
    ("Life Event Detection",     "Job change, marriage, divorce, or new baby detected via LinkedIn/social"),
    ("Neighborhood Search",      "Inquiries about specific neighborhoods — a strong buying signal"),
    ("Equity Position",          "How much equity does their current home have? Ready to move up?"),
    ("Time Since Last Purchase", "Years since they last bought — typical hold period suggests readiness"),
    ("Price Range Engagement",   "Which price range listings do they engage with most?"),
    ("Referral Source Quality",  "Contacts referred by past clients close at 3× the rate of cold leads"),
    ("Past Transaction History", "How many times have they transacted? Move-up buyers vs first-timers?"),
    ("Seasonal Pattern Match",   "Do their past transactions cluster in a season? Spring/fall buyer?"),
    ("Direct Inquiry Signal",    "Did they reply to an email, visit your website, or text you?"),
]
sw2 = (d.CW - Inches(0.2)) / 2
for i, (name, desc) in enumerate(signals):
    row, col = divmod(i, 2)
    sx = d.M + col*(sw2+Inches(0.2))
    sy = Inches(1.75) + row*Inches(0.72)
    bg = b.SOFT if row % 2 == 0 else b.WHITE
    d.rect(s, sx, sy, sw2, Inches(0.62), bg, radius=0.03)
    d.rect(s, sx, sy, Inches(0.06), Inches(0.62), AMBER)
    d.text(s, name, sx+Inches(0.16), sy+Inches(0.06), Inches(2.8), Inches(0.24),
           size=10.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, desc, sx+Inches(0.16), sy+Inches(0.32), sw2-Inches(0.28), Inches(0.26),
           size=9.5, color=b.INK, shrink=True)
d.rect(s, d.M, Inches(6.95), d.CW, Inches(0.32), b.LIGHT_TEAL, radius=0.03)
d.text(s, "No single signal predicts readiness. The system weights all 12 together and produces a composite score — updated every 24 hours.",
       d.M+Inches(0.2), Inches(6.98), d.CW-Inches(0.3), Inches(0.26),
       size=10, color=b.ACCENT, bold=True, shrink=True)
d.footer(s, 4, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — FIVE CAPABILITIES
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Five Capabilities — From Scoring to Closing",
         "The system finds the signal, sends the right message, and alerts you when to call.")
caps = [
    ("Lead Scoring Engine", "Scores every contact daily across 12 signals. Produces a composite readiness score (1–100) that updates every 24 hours. No manual input required after setup."),
    ("Monday Morning Report", "Every Monday at 7am, you receive a ranked list of your top contacts by readiness score — with the reason they ranked high and a suggested first touchpoint."),
    ("Automated Drip Sequences", "Four sequences run in the background for every contact segment: New Lead, Past Client, Long-Term Nurture, and Referred Contact — each with its own cadence and messaging."),
    ("Hot-Lead Alert System", "When a contact crosses a score threshold or takes a direct buying signal action (email reply, website visit, listing click), you receive an immediate SMS: 'Sarah Johnson just opened your last 4 emails. Good time to call.'"),
    ("Database Health Reports", "Monthly report shows who's been touched, who's gone cold, who's heating up, and what the projected close pipeline looks like for the next 90 days."),
]
for i, (title, body) in enumerate(caps):
    cy = Inches(1.75) + i * Inches(1.1)
    d.rect(s, d.M, cy, d.CW, Inches(1.0), b.SOFT if i%2==0 else b.WHITE, radius=0.04, shadow=True)
    d.rect(s, d.M, cy, Inches(0.07), Inches(1.0), AMBER)
    d.text(s, str(i+1), d.M+Inches(0.18), cy+Inches(0.08),
           Inches(0.36), Inches(0.36), size=16, color=AMBER, bold=True)
    d.text(s, title, d.M+Inches(0.65), cy+Inches(0.1),
           Inches(3.5), Inches(0.32), size=12, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, d.M+Inches(4.3), cy+Inches(0.08),
           d.CW-Inches(4.5), Inches(0.84), size=10.5, color=b.INK, shrink=True, ls=1.2)
d.footer(s, 5, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — THE MONDAY MORNING REPORT
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The Monday Morning Report — Your Weekly Call List",
         "Every Monday at 7am. Ranked by readiness. Reason included. Suggested action included.")
# mock report card
d.rect(s, d.M, Inches(1.75), d.CW, Inches(5.22), b.NAVY, radius=0.06, shadow=True)
d.text(s, "YOUR LEAD PRIORITY REPORT  ·  Week of June 16, 2026",
       d.M+Inches(0.25), Inches(1.88), d.CW-Inches(0.4), Inches(0.28),
       size=9.5, color=AMBER, bold=True)
d.rect(s, d.M+Inches(0.25), Inches(2.24), d.CW-Inches(0.4), Inches(0.03), b.NAVY_2)
# header row
hcols = ["Rank", "Contact", "Score", "Why They Ranked", "Suggested Action"]
hwidths = [Inches(0.6), Inches(2.0), Inches(0.9), Inches(5.1), Inches(3.4)]
hx = [d.M+Inches(0.25), d.M+Inches(0.95), d.M+Inches(3.05), d.M+Inches(4.05), d.M+Inches(9.28)]
for ci, (hdr, hw, hcx) in enumerate(zip(hcols, hwidths, hx)):
    d.text(s, hdr, hcx, Inches(2.3), hw, Inches(0.26),
           size=8.5, color=b.TEAL, bold=True)
contacts = [
    ("#1", "Sarah Johnson",  "94", "Opened 4 emails in 3 days + clicked listing on Oak St",    "Call today — high intent signal", b.GOLD),
    ("#2", "Mike & Dana T.", "87", "8 years since last purchase — equity threshold crossed",    "Send 'thinking of selling?' note", AMBER),
    ("#3", "Tom Reyes",      "81", "Referred by past client Martinez — referred leads 3× higher", "Warm intro call — mention the Martinez referral", b.TEAL),
    ("#4", "Lisa Park",      "74", "Started opening emails again after 4-month dormancy",       "Re-engagement email + follow-up call", b.TEAL),
    ("#5", "James & Ann C.", "68", "New job listing detected on LinkedIn + price range searches","Market update email + call in 2 weeks", AMBER),
]
for ri, (rank, name, score, reason, action, sc) in enumerate(contacts):
    ry = Inches(2.65) + ri*Inches(0.86)
    row_bg = b.NAVY_2 if ri % 2 == 0 else b.NAVY
    d.rect(s, d.M+Inches(0.25), ry, d.CW-Inches(0.4), Inches(0.8), row_bg, radius=0.03)
    d.text(s, rank,   hx[0], ry+Inches(0.12), hwidths[0], Inches(0.56), size=12, color=sc, bold=True)
    d.text(s, name,   hx[1], ry+Inches(0.06), hwidths[1], Inches(0.34), size=11, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, hx[2], ry+Inches(0.18), Inches(0.6), Inches(0.36), sc, radius=0.04)
    d.text(s, score,  hx[2]+Inches(0.04), ry+Inches(0.2), Inches(0.54), Inches(0.3),
           size=12, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, reason, hx[3], ry+Inches(0.06), hwidths[3], Inches(0.36), size=9.5, color=b.LIGHT_TEAL, shrink=True)
    d.text(s, action, hx[4], ry+Inches(0.06), hwidths[4], Inches(0.36), size=9.5, color=b.WHITE, shrink=True)
d.rect(s, d.M+Inches(0.25), Inches(7.0), d.CW-Inches(0.4), Inches(0.24), b.NAVY_2, radius=0.03)
d.text(s, "You have 20 more contacts scored 40–67 in your full report · 350 contacts on automated nurture · Next report: Mon Jun 23",
       d.M+Inches(0.45), Inches(7.03), d.CW-Inches(0.6), Inches(0.2),
       size=9, color=b.MUTED, shrink=True)
d.footer(s, 6, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — DRIP SEQUENCES
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Four Automated Drip Sequences — Running 24/7",
         "Every contact in your database is in one of four sequences. All automated. All branded to you.")
seqs = [
    (b.TEAL, "New Lead", "For contacts who just entered your database — from an open house, referral, or lead form.",
     ["Day 1 — Personalized welcome email (mentions how you met)",
      "Day 3 — Neighborhood market snapshot relevant to their search area",
      "Day 7 — 'Are you working with an agent?' soft check-in",
      "Day 14 — Curated listing suggestions based on their profile",
      "Day 30 — Check-in call prompt sent to you if no response"]),
    (b.GOLD, "Past Client", "Your buyers and sellers from previous transactions — your highest-value segment.",
     ["Quarterly — Market update for their specific neighborhood",
      "Annually — 'Happy home anniversary' email + estimated equity update",
      "Semi-annually — 'Thinking of moving up?' prompt for 3–7 year owners",
      "Event-triggered — Congrats note on LinkedIn job change or life event",
      "Referral ask — 6 months post-close: 'Know anyone thinking of moving?'"]),
    (AMBER, "Long-Term Nurture", "Contacts who aren't ready yet but will be — keep your name in their head.",
     ["Monthly — Market trend email (automated, data-driven)",
      "Quarterly — Neighborhood sold report for their area",
      "Bi-annually — 'Your home value has changed' equity update",
      "Hot event — Immediate alert to you if engagement score spikes",
      "12-month check-in — Soft 'still planning to move?' touch"]),
    (b.CORAL, "Referred Contact", "Leads sent to you by past clients — close at 3× the rate of cold leads.",
     ["Day 1 — Warm intro email (mentions referrer by name)",
      "Day 2 — Personal call prompt sent to you",
      "Day 5 — Value-add email: market report for their target area",
      "Day 10 — 'Ready to chat?' direct booking link",
      "Ongoing — Elevated scoring: referred contacts rank higher in Monday report"]),
]
sw2 = (d.CW - Inches(0.2)) / 2
for i, (color, name, desc, items) in enumerate(seqs):
    row, col = divmod(i, 2)
    sx = d.M + col*(sw2+Inches(0.2))
    sy = Inches(1.75) + row*Inches(2.6)
    d.rect(s, sx, sy, sw2, Inches(2.5), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, sx, sy, sw2, Inches(0.44), color, radius=0.04)
    d.text(s, name, sx+Inches(0.18), sy+Inches(0.08), sw2-Inches(0.3), Inches(0.28),
           size=13, color=b.NAVY if color==b.GOLD or color==AMBER else b.WHITE, bold=True)
    d.text(s, desc, sx+Inches(0.18), sy+Inches(0.52), sw2-Inches(0.3), Inches(0.42),
           size=9.5, color=b.INK, shrink=True, ls=1.2)
    for j, item in enumerate(items):
        d.rect(s, sx+Inches(0.18), sy+Inches(1.02)+j*Inches(0.3), Inches(0.1), Inches(0.1), color, radius=0.04)
        d.text(s, item, sx+Inches(0.36), sy+Inches(0.98)+j*Inches(0.3),
               sw2-Inches(0.5), Inches(0.28), size=9.5, color=b.INK, shrink=True)
d.footer(s, 7, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — HOT-LEAD ALERTS
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Hot-Lead Alerts — Know When to Call Before They Call Someone Else",
         "The system watches for buying signals 24/7. You get a text the moment one fires.")
# triggers list
LW = Inches(5.8)
d.rect(s, d.M, Inches(1.75), LW, Inches(5.1), b.SOFT, radius=0.05)
d.text(s, "WHAT TRIGGERS A HOT-LEAD ALERT", d.M+Inches(0.2), Inches(1.86),
       LW-Inches(0.3), Inches(0.28), size=9.5, color=AMBER, bold=True)
triggers = [
    (AMBER, "Score Spike",          "Contact's score jumps 15+ points in 48 hours — sudden increase in engagement"),
    (b.GOLD, "Direct Inquiry",      "Contact replies to any email, fills out a form, or texts you directly"),
    (b.TEAL, "Listing Click Burst", "Contact clicks 3+ listings in a single session — active search behavior"),
    (b.CORAL, "Long Dormant → Active", "Contact who hadn't opened an email in 60+ days suddenly opens 3 in a row"),
    (AMBER, "Referral Introduction", "A past client introduces you to a new contact via email forward or LinkedIn"),
    (b.TEAL, "Social Life Event",   "Marriage, job change, or relocation post detected on LinkedIn or Facebook"),
    (b.GOLD, "Website Visit",       "Contact visits your website listing page or bio page directly"),
    (b.NAVY, "Equity Milestone",    "Contact's home crosses the equity threshold that typically triggers a move-up"),
]
for i, (color, name, desc) in enumerate(triggers):
    ty = Inches(2.24) + i*Inches(0.56)
    d.rect(s, d.M+Inches(0.2), ty, Inches(0.1), Inches(0.42), color, radius=0.04)
    d.text(s, name, d.M+Inches(0.42), ty+Inches(0.02), Inches(2.0), Inches(0.24),
           size=10.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, desc, d.M+Inches(0.42), ty+Inches(0.26), LW-Inches(0.65), Inches(0.22),
           size=9.5, color=b.INK, shrink=True)
# right: SMS mock
RX = d.M + LW + Inches(0.3)
RW = d.CW - LW - Inches(0.3)
d.rect(s, RX, Inches(1.75), RW, Inches(5.1), b.NAVY, radius=0.05, shadow=True)
d.text(s, "SAMPLE HOT-LEAD ALERT (SMS)", RX+Inches(0.2), Inches(1.88),
       RW-Inches(0.3), Inches(0.26), size=8.5, color=AMBER, bold=True)
sms_lines = [
    "🔥 HOT LEAD — Sarah Johnson",
    "",
    "Score: 82 → 94 (+12 in 24h)",
    "",
    "What happened:",
    "· Opened your last 4 emails",
    "· Clicked Oak St listing 3×",
    "· Visited your website bio",
    "",
    "Best action: Call now.",
    "Last contact: 18 days ago.",
    "Script: 'Hi Sarah, just wanted",
    "to check in — I noticed you",
    "were looking at some listings",
    "and wanted to see if you have",
    "any questions...'",
]
for i, line in enumerate(sms_lines):
    is_header = i == 0
    ly = Inches(2.24) + i*Inches(0.27)
    d.text(s, line, RX+Inches(0.2), ly, RW-Inches(0.3), Inches(0.26),
           size=10 if is_header else 9.5,
           color=AMBER if is_header else b.WHITE,
           bold=is_header, shrink=True)
d.footer(s, 8, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — ROI MATH
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The ROI Math — Found Commission From Your Existing Database",
         "This system pays for itself with one additional closing per year. Most agents see it in 90 days.")
stats2 = [
    ("400", "contacts scored", "Every contact scored daily — not just your 'hot' leads"),
    ("20–32", "ready now (est.)", "5–8% of any typical database in active buying/selling mode"),
    ("3×", "referral close rate", "Referred contacts close at 3× the rate of cold leads"),
    ("$3,000/mo", "system cost", "Flat monthly rate — no per-contact or per-close fees"),
]
sw = (d.CW - Inches(0.6)) / 4
for i, (num, label, note) in enumerate(stats2):
    stat_tile(s, num, label, note, d.M + i*(sw+Inches(0.2)), Inches(1.85), w=sw)
# found commission math
d.rect(s, d.M, Inches(3.88), d.CW*0.6, Inches(2.5), b.SOFT, radius=0.05)
d.text(s, "Found commission scenario — 400 contact database",
       d.M+Inches(0.2), Inches(3.98), d.CW*0.6-Inches(0.3), Inches(0.38),
       size=11.5, color=b.NAVY, bold=True)
scenario = [
    ("Database size:",                     "400 contacts"),
    ("Contacts in buying/selling mode:",   "20–32 (5–8%)"),
    ("System improvement in conversion:",  "+15–30% through timely contact"),
    ("Additional deals per year:",         "3–6 additional closings"),
    ("Average commission per deal:",       "$9,000 ($300K × 3%)"),
    ("Additional annual revenue:",         "$27,000–$54,000"),
    ("System annual cost:",               "$36,000 ($3K × 12)"),
    ("Net return (conservative):",         "Break-even at 4 deals. Positive from deal 5+."),
]
for i, (label, val) in enumerate(scenario):
    ly = Inches(4.44) + i*Inches(0.24)
    d.text(s, label, d.M+Inches(0.2), ly, Inches(3.8), Inches(0.22),
           size=10, color=b.MUTED, bold=True)
    d.text(s, val, d.M+Inches(4.1), ly, d.CW*0.6-Inches(4.3), Inches(0.22),
           size=10, color=b.INK, shrink=True)
# return card
RX = d.M + d.CW*0.6 + Inches(0.2)
RW = d.CW - d.CW*0.6 - Inches(0.2)
d.rect(s, RX, Inches(3.88), RW, Inches(2.5), b.NAVY, radius=0.06, shadow=True)
d.text(s, "Year 1 return\n(conservative)", RX+Inches(0.2), Inches(4.0),
       RW-Inches(0.3), Inches(0.68), size=13, color=b.LIGHT_TEAL, bold=True, shrink=True)
d.text(s, "$27K–$54K", RX+Inches(0.2), Inches(4.78), RW-Inches(0.3), Inches(0.84),
       size=38, color=AMBER, bold=True, shrink=True)
d.text(s, "in additional commission", RX+Inches(0.2), Inches(5.66), RW-Inches(0.3), Inches(0.34),
       size=10.5, color=b.LIGHT_TEAL, shrink=True)
d.rect(s, d.M, Inches(6.55), d.CW, Inches(0.52), b.LIGHT_TEAL, radius=0.04)
d.text(s, "Note: most agents see 2–3 additional closings within the first 90 days — from contacts already in their database who were signaling readiness and not being called.",
       d.M+Inches(0.2), Inches(6.6), d.CW-Inches(0.3), Inches(0.42),
       size=10.5, color=b.ACCENT, shrink=True, ls=1.2)
d.footer(s, 9, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — WHAT'S INCLUDED
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "What's Included — Your Complete CRM Intelligence Layer",
         "One flat monthly fee covers everything from import to close pipeline reporting.")
included = [
    ("Contact Import", "We import your contacts from any source: CSV export, Google Contacts, Follow Up Boss, or a simple spreadsheet. No manual re-entry."),
    ("12-Signal Scoring Engine", "All 400+ contacts scored daily across 12 readiness signals. Composite score updated every 24 hours. No manual input after setup."),
    ("Monday Morning Report", "Weekly prioritized callback list delivered by 7am every Monday — ranked, with reason and suggested action per contact."),
    ("Four Drip Sequences", "All four automated sequences (New Lead, Past Client, Long-Term Nurture, Referred) — customized to your voice and brokerage brand."),
    ("Hot-Lead Alert System", "Immediate SMS to your phone when any contact crosses a readiness threshold or takes a direct buying signal action."),
    ("Database Health Report", "Monthly report: who's been touched, who's gone cold, who's heating up, and projected close pipeline for the next 90 days."),
    ("Quarterly Recalibration", "Every quarter we review your scoring model against your actual closings — and adjust signal weights to improve accuracy for your specific market."),
    ("Monthly Support Check-In", "30-minute call to review report accuracy, update sequences, and discuss any contacts you want to prioritize or remove."),
]
iw = (d.CW - Inches(0.2)) / 2
for i, (title, body) in enumerate(included):
    row, col = divmod(i, 2)
    ix = d.M + col*(iw+Inches(0.2))
    iy = Inches(1.75) + row*Inches(1.24)
    d.rect(s, ix, iy, iw, Inches(1.14), b.WHITE, radius=0.04, shadow=True)
    d.rect(s, ix, iy, Inches(0.07), Inches(1.14), AMBER)
    d.text(s, f"✓  {title}", ix+Inches(0.18), iy+Inches(0.1),
           iw-Inches(0.28), Inches(0.34), size=11.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, ix+Inches(0.18), iy+Inches(0.48),
           iw-Inches(0.28), Inches(0.6), size=10, color=b.INK, shrink=True, ls=1.15)
d.footer(s, 10, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — SETUP TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "10-Day Setup — First Monday Report in Under Two Weeks",
         "Your database is scored, your sequences are live, and your first report arrives before the end of week 2.")
tl = [
    ("Days 1–3", "Import + Score",
     ["Contact import from your CRM/CSV/Google Contacts — any format",
      "Initial scoring run across all 12 signals",
      "First draft of your Monday report (internal review before delivery)"]),
    ("Days 4–6", "Sequence Setup",
     ["All four drip sequences configured with your brokerage name, headshot, and tone",
      "Email templates reviewed with you — adjustments made to match your voice",
      "Hot-lead alert thresholds set based on your market and response preferences"]),
    ("Days 7–9", "Test + Validate",
     ["Test Monday report reviewed together — you confirm the top-ranked contacts make sense",
      "One live drip sequence test email sent to your own address for review",
      "Hot-lead alert tested: verify SMS delivery to your number"]),
    ("Day 10", "Go Live",
     ["All contacts in active sequences",
      "First official Monday morning report delivered at 7am",
      "You're running — call your top 5 contacts this week"]),
]
for i, (period, title, items) in enumerate(tl):
    wy = Inches(1.92) + i*Inches(1.28)
    d.rect(s, d.M, wy, Inches(1.15), Inches(1.08), AMBER, radius=0.04)
    d.text(s, period, d.M, wy+Inches(0.14), Inches(1.15), Inches(0.5),
           size=11, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, d.M+Inches(1.25), wy, d.CW-Inches(1.25), Inches(1.08), b.SOFT, radius=0.04)
    d.text(s, title, d.M+Inches(1.45), wy+Inches(0.06), Inches(4.5), Inches(0.32),
           size=12, color=b.NAVY, bold=True, shrink=True)
    for j, item in enumerate(items):
        d.rect(s, d.M+Inches(1.45), wy+Inches(0.44)+j*Inches(0.22),
               Inches(0.1), Inches(0.1), AMBER, radius=0.04)
        d.text(s, item, d.M+Inches(1.65), wy+Inches(0.4)+j*Inches(0.22),
               d.CW-Inches(1.85), Inches(0.22), size=10, color=b.INK, shrink=True)
d.rect(s, d.M, Inches(7.09), d.CW, Inches(0.24), b.LIGHT_TEAL, radius=0.03)
d.text(s, "Setup fee: $750 one-time (covers 10-day import, scoring calibration, sequence setup, and onboarding support)",
       d.M+Inches(0.2), Inches(7.11), d.CW-Inches(0.3), Inches(0.2),
       size=9.5, color=b.ACCENT, shrink=True)
d.footer(s, 11, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — PRICING + CTA
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.12), AMBER)
d.rect(s, 0, d.H-Inches(0.12), d.W, Inches(0.12), AMBER)
d.text(s, "FIND THE DEALS ALREADY IN YOUR DATABASE.", d.M, Inches(0.72),
       Inches(10), Inches(0.38), size=12, color=AMBER, bold=True)
d.rect(s, d.M, Inches(1.2), Inches(5.5), Inches(2.4), b.NAVY_2, radius=0.08, shadow=True)
d.text(s, "$3,000", d.M+Inches(0.3), Inches(1.4), Inches(4.2), Inches(1.1),
       size=72, color=AMBER, bold=True, shrink=True)
d.text(s, "/ month", d.M+Inches(0.3), Inches(2.42), Inches(3.0), Inches(0.38),
       size=18, color=b.LIGHT_TEAL)
d.text(s, "+ $750 one-time setup · No long-term contract · Cancel with 30 days notice",
       d.M+Inches(0.3), Inches(2.92), Inches(5.0), Inches(0.44),
       size=10.5, color=b.MUTED, shrink=True)
d.text(s, "For $3,000/month you get:", d.M+Inches(6.1), Inches(1.2),
       Inches(6.5), Inches(0.38), size=12, color=AMBER, bold=True)
gets = ["All 400+ contacts scored daily",
        "Weekly Monday morning priority report",
        "Four automated drip sequences",
        "Hot-lead SMS alerts — no lag",
        "Monthly database health report",
        "Quarterly scoring recalibration",
        "Cancel anytime — no lock-in"]
for i, g in enumerate(gets):
    d.rect(s, d.M+Inches(6.1), Inches(1.66)+i*Inches(0.46), Inches(0.14), Inches(0.14), AMBER, radius=0.04)
    d.text(s, g, d.M+Inches(6.38), Inches(1.62)+i*Inches(0.46), Inches(6.4), Inches(0.4),
           size=11.5, color=b.WHITE, shrink=True)
d.rect(s, d.M, Inches(3.86), d.CW, Inches(0.06), b.NAVY_2)
d.text(s, "THREE STEPS TO GET STARTED", d.M, Inches(4.02),
       Inches(8), Inches(0.32), size=11, color=AMBER, bold=True)
steps3 = [
    ("1", "20-min intro call", "We review your database, contact sources, and current CRM setup."),
    ("2", "Sign + pay setup fee", "Import and scoring begin within 48 hours."),
    ("3", "First Monday report", "Day 10 — your database is scored, sequences are live, your first report arrives."),
]
for i, (n, title, body) in enumerate(steps3):
    sx = d.M + i*Inches(4.2)
    d.rect(s, sx, Inches(4.44), Inches(0.44), Inches(0.44), AMBER, radius=0.08)
    d.text(s, n, sx, Inches(4.46), Inches(0.44), Inches(0.4),
           size=16, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, title, sx+Inches(0.6), Inches(4.46), Inches(3.4), Inches(0.36),
           size=12, color=b.WHITE, bold=True, shrink=True)
    d.text(s, body, sx+Inches(0.6), Inches(4.88), Inches(3.4), Inches(0.52),
           size=10, color=b.LIGHT_TEAL, shrink=True, ls=1.2)
d.text(s, "[your website or booking link here]",
       d.M, Inches(5.72), d.CW, Inches(0.38), size=14, color=AMBER, bold=True)
d.footer(s, 12, TOTAL, dark=True)

d.save(OUT_PATH)
print(f"Deck 3 saved: {OUT_PATH} ({d.n} slides)")
