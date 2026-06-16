#!/usr/bin/env python3
"""
Build: OpenHands × SMB Done-For-You AI Engineering Team — Top 25 Use Cases
Output: deck/openhands-smb-use-cases-draft.pptx
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, Brand, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor

SKILL_DIR = os.path.expanduser("~/.claude/skills/branded-pptx-deck/scripts")
OUT_DIR   = os.path.join(os.path.dirname(__file__), "deck")
OUT_PATH  = os.path.join(OUT_DIR, "openhands-smb-use-cases-draft.pptx")
FOOTER    = "OpenHands × SMB AI Engineering · Done-For-You · June 2026"
TOTAL     = 27

os.makedirs(OUT_DIR, exist_ok=True)

d = Deck(footer=FOOTER)
b = d.b

# ─── helpers ──────────────────────────────────────────────────────────────────

def cover_chip(s, text, left, top):
    d.rect(s, left, top, Inches(2.4), Inches(0.32), b.TEAL, radius=0.05)
    d.text(s, text, left + Inches(0.15), top + Inches(0.04),
           Inches(2.1), Inches(0.26), size=11, color=b.NAVY, bold=True)

def section_divider(num_str, title, subtitle, page):
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"SECTION {num_str}", Inches(0.45), Inches(2.0), Inches(8), Inches(0.4),
           size=13, color=b.TEAL, bold=True)
    d.text(s, title, Inches(0.45), Inches(2.55), Inches(10), Inches(1.2),
           size=44, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.45), Inches(3.85), Inches(3.5), Inches(0.05), b.TEAL)
    d.text(s, subtitle, Inches(0.45), Inches(4.0), Inches(10), Inches(0.5),
           size=16, color=b.LIGHT_TEAL)
    d.footer(s, page, TOTAL, dark=True)
    return s

def use_case_card(s, left, top, num, title, pain, value, urgency, card_w=Inches(5.9), card_h=Inches(2.55)):
    d.rect(s, left, top, card_w, card_h, b.WHITE, radius=0.04, shadow=True)
    # number chip
    d.rect(s, left + Inches(0.18), top + Inches(0.15), Inches(0.42), Inches(0.42), b.NAVY, radius=0.1)
    d.text(s, f"#{num}", left + Inches(0.18), top + Inches(0.17), Inches(0.42), Inches(0.38),
           size=11, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
    # urgency pill
    urg_col = b.GOLD if urgency >= 9 else (b.TEAL if urgency >= 7 else b.AMBER)
    d.rect(s, left + card_w - Inches(0.9), top + Inches(0.16), Inches(0.72), Inches(0.26), urg_col, radius=0.08)
    d.text(s, f"  {urgency}/10", left + card_w - Inches(0.9), top + Inches(0.16),
           Inches(0.72), Inches(0.26), size=9, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    # title
    d.text(s, title, left + Inches(0.72), top + Inches(0.14), card_w - Inches(0.95), Inches(0.52),
           size=13, color=b.NAVY, bold=True, shrink=True)
    # divider
    d.rect(s, left + Inches(0.18), top + Inches(0.72), card_w - Inches(0.36), Inches(0.025), b.SOFT)
    # pain
    d.text(s, pain, left + Inches(0.18), top + Inches(0.80), card_w - Inches(0.36), Inches(1.2),
           size=11, color=b.INK, shrink=True, ls=1.15)
    # value strip
    d.rect(s, left, top + card_h - Inches(0.42), card_w, Inches(0.42), b.LIGHT_TEAL, radius=0.04)
    d.text(s, f"Value: {value}", left + Inches(0.18), top + card_h - Inches(0.40),
           card_w - Inches(0.36), Inches(0.38), size=10, color=b.ACCENT, bold=True, shrink=True)

def realization_slide(page, num, title, vertical, pain, build_desc, mcp_list, subagent, value, buyer_line, urgency, wave, how_it_works):
    s = d.slide(fill=b.WHITE)
    d.rect(s, 0, 0, d.W, Inches(0.1), b.TEAL)
    # left panel
    PANEL_W = Inches(4.5)
    d.rect(s, 0, Inches(0.1), PANEL_W, d.H - Inches(0.1), b.NAVY)
    d.rect(s, 0, Inches(0.1), Inches(0.1), d.H - Inches(0.1), b.TEAL)
    # use case number + vertical
    d.text(s, f"#{num}  ·  {vertical.upper()}", Inches(0.25), Inches(0.22),
           PANEL_W - Inches(0.35), Inches(0.32), size=10, color=b.TEAL, bold=True)
    # title
    d.text(s, title, Inches(0.25), Inches(0.58), PANEL_W - Inches(0.35), Inches(1.0),
           size=22, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.25), Inches(1.68), Inches(2.0), Inches(0.05), b.TEAL)
    # challenge block
    d.text(s, "THE PAIN", Inches(0.25), Inches(1.82), PANEL_W - Inches(0.35), Inches(0.28),
           size=9, color=b.TEAL, bold=True)
    d.text(s, pain, Inches(0.25), Inches(2.12), PANEL_W - Inches(0.35), Inches(1.0),
           size=11, color=b.LIGHT_TEAL, shrink=True, ls=1.2)
    # how it works
    d.text(s, "HOW IT WORKS", Inches(0.25), Inches(3.22), PANEL_W - Inches(0.35), Inches(0.28),
           size=9, color=b.TEAL, bold=True)
    for i, step in enumerate(how_it_works):
        sy = Inches(3.55) + i * Inches(0.52)
        d.rect(s, Inches(0.25), sy, Inches(0.32), Inches(0.32), b.TEAL, radius=0.08)
        d.text(s, str(i + 1), Inches(0.25), sy, Inches(0.32), Inches(0.32),
               size=9, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, step, Inches(0.65), sy + Inches(0.04), PANEL_W - Inches(0.8), Inches(0.44),
               size=10, color=b.WHITE, shrink=True)
    # buyer line
    d.rect(s, Inches(0.15), Inches(6.35), PANEL_W - Inches(0.25), Inches(0.85), b.NAVY_2, radius=0.04)
    d.text(s, f'"{buyer_line}"', Inches(0.25), Inches(6.38), PANEL_W - Inches(0.4), Inches(0.79),
           size=10, color=b.AMBER, italic=True, shrink=True)
    # right panel — build + stats
    RX = PANEL_W + Inches(0.45)
    RW = d.W - PANEL_W - Inches(0.55)
    # urgency + wave pills
    urg_col = b.GOLD if urgency >= 9 else (b.TEAL if urgency >= 7 else b.AMBER)
    d.rect(s, RX, Inches(0.22), Inches(1.5), Inches(0.32), urg_col, radius=0.06)
    d.text(s, f"Urgency {urgency}/10", RX, Inches(0.24), Inches(1.5), Inches(0.28),
           size=10, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    wave_col = b.TEAL if wave == 1 else b.AMBER
    d.rect(s, RX + Inches(1.6), Inches(0.22), Inches(1.2), Inches(0.32), wave_col, radius=0.06)
    d.text(s, f"Wave {wave}", RX + Inches(1.6), Inches(0.24), Inches(1.2), Inches(0.28),
           size=10, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    # THE BUILD
    d.text(s, "THE BUILD", RX, Inches(0.72), RW, Inches(0.28), size=10, color=b.NAVY, bold=True)
    d.text(s, build_desc, RX, Inches(1.04), RW, Inches(1.35), size=11, color=b.INK, shrink=True, ls=1.2)
    # value stat
    d.rect(s, RX, Inches(2.5), RW, Inches(0.62), b.NAVY, radius=0.06)
    d.text(s, "MONTHLY VALUE TO CLIENT", RX + Inches(0.2), Inches(2.56), RW - Inches(0.3), Inches(0.24),
           size=8.5, color=b.TEAL, bold=True)
    d.text(s, value, RX + Inches(0.2), Inches(2.8), RW - Inches(0.3), Inches(0.26),
           size=12, color=b.GOLD, bold=True, shrink=True)
    # MCP servers
    d.rect(s, RX, Inches(3.24), RW, Inches(0.26), b.SOFT)
    d.text(s, "MCP SERVERS", RX + Inches(0.15), Inches(3.26), Inches(1.5), Inches(0.22),
           size=8.5, color=b.MUTED, bold=True)
    d.text(s, mcp_list, RX + Inches(1.7), Inches(3.26), RW - Inches(1.85), Inches(0.22),
           size=9, color=b.INK, shrink=True)
    # Subagent
    d.rect(s, RX, Inches(3.60), RW, Inches(0.26), b.SOFT)
    d.text(s, "SUBAGENT", RX + Inches(0.15), Inches(3.62), Inches(1.5), Inches(0.22),
           size=8.5, color=b.MUTED, bold=True)
    d.text(s, subagent, RX + Inches(1.7), Inches(3.62), RW - Inches(1.85), Inches(0.22),
           size=9, color=b.INK, shrink=True)
    # footer
    d.footer(s, page, TOTAL)
    return s


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, d.W - Inches(2.0), 0, Inches(2.0), d.H, b.NAVY_2)
d.rect(s, d.W - Inches(2.0), 0, Inches(0.1), d.H, b.TEAL)
d.text(s, "DONE-FOR-YOU", d.M, Inches(1.2), Inches(9), Inches(0.45),
       size=16, color=b.TEAL, bold=True)
d.text(s, "AI Engineering Team", d.M, Inches(1.7), Inches(9.5), Inches(1.5),
       size=52, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(3.3), Inches(4.0), Inches(0.06), b.TEAL)
d.text(s, "Top 25 SMB Use Cases · OpenHands × 131 Specialist Subagents",
       d.M, Inches(3.5), Inches(9), Inches(0.5), size=15.5, color=b.LIGHT_TEAL)
cover_chip(s, "77K+ GitHub Stars", d.M, Inches(4.4))
cover_chip(s, "$2K–$5K/Month", d.M + Inches(2.55), Inches(4.4))
cover_chip(s, "5× Cheaper Than Dev Shop", d.M + Inches(5.1), Inches(4.4))
d.text(s, "June 2026", d.M, Inches(5.1), Inches(3), Inches(0.35),
       size=12, color=b.MUTED)
d.footer(s, 1, TOTAL, dark=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — EXECUTIVE SUMMARY (BLUF)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.rect(s, 0, 0, d.W, Inches(0.1), b.TEAL)
# BLUF banner
d.rect(s, 0, Inches(0.1), d.W, Inches(0.72), b.NAVY)
d.text(s, "THE BOTTOM LINE", d.M, Inches(0.14), Inches(5), Inches(0.3),
       size=9, color=b.TEAL, bold=True)
d.text(s, "One person + OpenHands + a niche = a $50K/mo AI engineering agency. Open source is the new wholesale.",
       d.M, Inches(0.38), d.CW, Inches(0.4), size=14, color=b.WHITE, bold=True, shrink=True)
# three columns
cols = [
    ("SITUATION", b.NAVY, b.WHITE, [
        "77K-star open-source agent runtime (OpenHands) reads code, edits files, opens PRs, and deploys apps autonomously.",
        "131 free specialist subagents via VoltAgent — CRM, HIPAA, document automation, and more.",
        "14,000+ MCP servers provide turnkey integrations to GitHub, Stripe, Twilio, Calendly, Postgres.",
        "Self-hosted on a $20/mo VPS. Setup time: one afternoon.",
    ]),
    ("INSIGHT", b.TEAL, b.NAVY, [
        "SMBs need custom software and can't afford a $15K/mo dev shop or $25K/mo junior hire.",
        "They already Google 'outsource my software development'. You're the answer.",
        "The code is free. The orchestration, the niche positioning, and the AGENTS.md setup is where the margin lives.",
        "Vertical specialization = moat. 'AI team for dental practices' is defensible. 'AI automation' is not.",
    ]),
    ("RECOMMENDATION", b.GOLD, b.NAVY, [
        "Start with Real Estate (33/35 vertical score). No HIPAA, clear ROI link to commission.",
        "Charge $2K–$5K/month per client. Build one AGENTS.md per vertical. The rest is supervision.",
        "Publish what your agents shipped this week. Case studies sell themselves.",
        "Reinvest in vertical-specific subagents. Niche moat compounds month over month.",
    ]),
]
col_w = (d.CW - Inches(0.2)) / 3
for ci, (label, bg, fg, bullets) in enumerate(cols):
    cx = d.M + ci * (col_w + Inches(0.1))
    d.rect(s, cx, Inches(0.95), col_w, d.H - Inches(1.35), bg, radius=0.04, shadow=True)
    d.text(s, label, cx + Inches(0.2), Inches(1.05), col_w - Inches(0.3), Inches(0.3),
           size=10, color=fg, bold=True)
    d.rect(s, cx + Inches(0.2), Inches(1.42), col_w - Inches(0.4), Inches(0.03), RGBColor(0xFF,0xFF,0xFF) if bg == b.NAVY else b.NAVY)
    for bi, bullet in enumerate(bullets):
        by = Inches(1.55) + bi * Inches(1.12)
        d.text(s, bullet, cx + Inches(0.2), by, col_w - Inches(0.35), Inches(1.05),
               size=10.5, color=fg if bg != b.NAVY else b.LIGHT_TEAL, shrink=True, ls=1.2)
d.footer(s, 2, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — THE BUSINESS MODEL (9 STEPS)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The 9-Step Business Model", "From $20/mo VPS to $50K/mo AI engineering agency")
steps = [
    ("1", "Self-host OpenHands on a $20/mo VPS", "Claude Code walks you through setup in one afternoon. No devops degree required."),
    ("2", "Pick one niche", "Real estate, dental, law, HVAC. SMBs that need custom software but can't afford a developer."),
    ("3", "Wrap it in their language", "'Your AI engineering team for dental practices' — not 'OpenHands with 131 subagents'."),
    ("4", "Install specialist subagents", "CRM-specialist for RE, HIPAA-auditor for healthcare, document-automation for law firms."),
    ("5", "Plug in MCP servers", "GitHub, Stripe, Twilio, Postgres, Calendly — your AI team ships, deploys, integrates, and notifies."),
    ("6", "Charge $2K–$5K/month", "Nothing vs. a $15K/mo dev shop or $25K/mo junior hire. You're 5× cheaper and never sleep."),
    ("7", "Build once, sell many", "One landing page. One onboarding call. Record the AGENTS.md setup once. The rest is supervision."),
    ("8", "Become 'the AI team for [niche]'", "Share what your agents shipped this week on X, LinkedIn, YouTube. Case studies sell themselves."),
    ("9", "Reinvest in vertical-specific agents", "Patient-intake-automator for dental. Lease-document-generator for RE. You own the vertical."),
]
cols3 = 3
card_w = (d.CW - Inches(0.3)) / cols3
card_h = Inches(1.55)
for i, (num, title, desc) in enumerate(steps):
    row, col = divmod(i, cols3)
    cx = d.M + col * (card_w + Inches(0.15))
    cy = Inches(1.7) + row * (card_h + Inches(0.12))
    d.rect(s, cx, cy, card_w, card_h, b.SOFT, radius=0.04, shadow=True)
    d.rect(s, cx, cy, Inches(0.08), card_h, b.TEAL, radius=0.02)
    d.text(s, num, cx + Inches(0.15), cy + Inches(0.12), Inches(0.32), Inches(0.32),
           size=16, color=b.TEAL, bold=True)
    d.text(s, title, cx + Inches(0.15), cy + Inches(0.44), card_w - Inches(0.25), Inches(0.4),
           size=11, color=b.NAVY, bold=True, shrink=True)
    d.text(s, desc, cx + Inches(0.15), cy + Inches(0.88), card_w - Inches(0.25), Inches(0.6),
           size=9.5, color=b.INK, shrink=True, ls=1.15)
d.footer(s, 3, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — MARKET SIGNALS (WHY NOW)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Why Now — The Market Is Ready", "Last 30 days signals from Reddit, HN, GitHub, and web sources")
stats = [
    ("77K", "OpenHands GitHub Stars", "Jun 2026 (up from 75K in Apr)"),
    ("131", "Free Specialist Subagents", "VoltAgent marketplace — CRM, HIPAA, legal, e-comm"),
    ("14,000+", "MCP Server Integrations", "GitHub, Stripe, Twilio, Calendly, Postgres, more"),
    ("58%", "SMBs Using AI Daily", "Thryv 2026 survey; 58% save 20+ hrs/month"),
    ("$2K–$5K", "Validated Price Point", "SMBs already pay $1.5K–$5K for single custom agents"),
    ("$0", "Runtime Cost", "Self-host on $20/mo VPS; no per-seat AI license"),
]
stat_w = (d.CW - Inches(0.4)) / 3
for i, (num, label, note) in enumerate(stats):
    row, col = divmod(i, 3)
    sx = d.M + col * (stat_w + Inches(0.2))
    sy = Inches(1.85) + row * Inches(2.35)
    d.rect(s, sx, sy, stat_w, Inches(2.1), b.NAVY, radius=0.06, shadow=True)
    d.text(s, num, sx + Inches(0.2), sy + Inches(0.28), stat_w - Inches(0.3), Inches(0.82),
           size=38, color=b.GOLD, bold=True, shrink=True)
    d.text(s, label, sx + Inches(0.2), sy + Inches(1.12), stat_w - Inches(0.3), Inches(0.5),
           size=12, color=b.WHITE, bold=True, shrink=True)
    d.text(s, note, sx + Inches(0.2), sy + Inches(1.64), stat_w - Inches(0.3), Inches(0.4),
           size=9.5, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 4, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — VERTICAL PRIORITY SCORECARD
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Vertical Priority Scorecard — Start With Real Estate", "7-dimension score across 8 SMB niches · GO = 30–35 · CONDITIONAL = 24–29")
verticals = [
    ("Real Estate",    33, "GO",          "b.TEAL"),
    ("E-Commerce",     29, "CONDITIONAL", "b.AMBER"),
    ("Accounting",     27, "CONDITIONAL", "b.AMBER"),
    ("Mktg Agencies",  27, "CONDITIONAL", "b.AMBER"),
    ("Dental",         26, "CONDITIONAL", "b.AMBER"),
    ("Law Firms",      26, "CONDITIONAL", "b.AMBER"),
    ("Med Spa",        26, "CONDITIONAL", "b.AMBER"),
    ("HVAC/Plumbing",  24, "CONDITIONAL", "b.AMBER"),
]
# bar chart style
bar_max = 35.0
bar_area_w = Inches(7.5)
bar_h = Inches(0.5)
bar_start_x = Inches(3.2)
for i, (name, score, verdict, _) in enumerate(verticals):
    vy = Inches(1.75) + i * Inches(0.62)
    bar_col = b.TEAL if score >= 30 else (b.AMBER if score >= 24 else b.CORAL)
    verdict_col = b.TEAL if verdict == "GO" else b.AMBER
    d.text(s, name, d.M, vy + Inches(0.08), Inches(2.5), bar_h,
           size=11.5, color=b.NAVY, bold=True if score >= 30 else False)
    bar_len = bar_area_w * (score / bar_max)
    d.rect(s, bar_start_x, vy + Inches(0.08), bar_area_w, bar_h - Inches(0.06), b.SOFT)
    d.rect(s, bar_start_x, vy + Inches(0.08), bar_len, bar_h - Inches(0.06), bar_col, radius=0.02)
    d.text(s, f"{score}/35", bar_start_x + bar_len + Inches(0.12), vy + Inches(0.1),
           Inches(0.8), bar_h - Inches(0.06), size=11, color=b.INK, bold=True)
    d.rect(s, Inches(11.7), vy + Inches(0.1), Inches(1.3), Inches(0.32), verdict_col, radius=0.05)
    d.text(s, verdict, Inches(11.7), vy + Inches(0.11), Inches(1.3), Inches(0.3),
           size=9, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
d.footer(s, 5, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — SECTION: REAL ESTATE
# ═══════════════════════════════════════════════════════════════════════════════
section_divider("01", "Real Estate Brokerages", "8 use cases · 33/35 score · GO verdict · No HIPAA ceiling · Starts at #1", 6)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — REAL ESTATE: USE CASES #1–4 (CARDS)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Real Estate — Core Use Cases (Wave 1)", "All four justify $2K–$5K/month on their own ROI math")
re_cards_1 = [
    (1, "Transaction Coordinator Bot",
     "Agents pay $300–$500/transaction to a human TC who still misses contingency dates.",
     "$1,500–$4,000/month saved (TC fees eliminated)", 9),
    (2, "Listing Description + MLS Auto-Post",
     "Agents spend 45–90 min per listing writing descriptions and manually uploading to MLS + Zillow.",
     "8–15 hours/month recovered; faster listings = more closings", 9),
    (3, "Lead Scoring + CRM Drip System",
     "200–500 contacts in a spreadsheet, no scoring — agents call everyone randomly and miss the 5% ready to transact.",
     "1–3 additional closed deals/year = $6K–$18K commission", 9),
    (4, "CMA Generator",
     "Agents spend 2–3 hours per CMA manually pulling comps and formatting in PowerPoint before every listing appt.",
     "10–20 hours/month recovered; faster listing appts", 8),
]
CW2 = (d.CW - Inches(0.2)) / 2
for i, args in enumerate(re_cards_1):
    row, col = divmod(i, 2)
    cx = d.M + col * (CW2 + Inches(0.2))
    cy = Inches(1.75) + row * Inches(2.75)
    use_case_card(s, cx, cy, *args, card_w=CW2, card_h=Inches(2.6))
d.footer(s, 7, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — RE DEEP DIVE: TRANSACTION COORDINATOR BOT
# ═══════════════════════════════════════════════════════════════════════════════
realization_slide(
    8, 1, "Transaction Coordinator Bot", "Real Estate",
    "Agents pay $300–$500 per transaction to a human TC who manually tracks deadlines, chases documents, and emails all parties — and still misses contingency dates.",
    "OpenHands builds a TC automation app: ingests purchase agreement, auto-extracts all deadline dates into Google Calendar, sends daily status emails to all parties (buyer, seller, title, lender), flags missing documents, and closes the deal file when all docs are collected.",
    "GitHub, Google Calendar, Gmail, Stripe, Notion, Twilio",
    "document-automation, crm-specialist",
    "$1,500–$4,000 saved per month (3–8 transactions × $300–$500 TC fee eliminated)",
    "I'm paying my TC $2,000 a month and half the time I still have to chase people myself.",
    9, 1,
    [
        "Ingest purchase agreement PDF, extract all deadline dates",
        "Populate Google Calendar with contingency reminders for all parties",
        "Auto-send daily status digest via Gmail + Twilio SMS",
        "Flag missing docs; close file when complete → invoice via Stripe",
    ]
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — REAL ESTATE: USE CASES #13, 21, 23 (WAVE 2)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Real Estate — Wave 2 Expansion Use Cases", "Add these once the Wave 1 triplet is proven and delivering ROI")
re_cards_2 = [
    (13, "Buyer/Seller Matching + Tour Scheduler",
     "Agents manually cross-reference active listings against buyer criteria in their head or a spreadsheet.",
     "Faster deal close; buyers stay engaged; fewer lost to competing agents", 8),
    (21, "Commission Tracking Dashboard",
     "Broker tracks agent splits in a spreadsheet — calculating caps and paying out takes 5–8 hrs at month-end.",
     "5–8 hours/month recovered; fewer commission disputes", 6),
    (23, "Social Media Content Calendar",
     "Agents know they should post consistently but creating content is time-consuming and they never know what to say.",
     "5–10 hours/month saved; consistent posting builds inbound leads", 6),
]
card_w3 = (d.CW - Inches(0.4)) / 3
for i, args in enumerate(re_cards_2):
    cx = d.M + i * (card_w3 + Inches(0.2))
    use_case_card(s, cx, Inches(1.85), *args, card_w=card_w3, card_h=Inches(3.2))
# wave 2 note
d.rect(s, d.M, Inches(5.2), d.CW, Inches(0.55), b.LIGHT_TEAL, radius=0.04)
d.text(s, "Wave 2 note: these require MLS API access or QuickBooks integration. Sequence after Wave 1 pays for setup cost.",
       d.M + Inches(0.2), Inches(5.25), d.CW - Inches(0.3), Inches(0.44), size=10.5, color=b.ACCENT, shrink=True)
d.footer(s, 9, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — SECTION: DENTAL
# ═══════════════════════════════════════════════════════════════════════════════
section_divider("02", "Dental Practices", "4 use cases · 26/35 score · CONDITIONAL · HIPAA-required · Directly books chairs", 10)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — DENTAL USE CASES (CARDS)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Dental — Use Cases (2 Wave 1, 2 Wave 1)", "All four are Wave 1. Patient Recall and Insurance Pre-Auth are urgency 10/10.")
dental_cards = [
    (5, "Patient Recall + Appointment System",
     "Dental offices lose $50K–$200K/year in unscheduled recall patients — staff reaches maybe 20% calling manually.",
     "15–40 additional hygiene appts/month = $3K–$8K production", 10),
    (6, "Insurance Pre-Auth + Verification Bot",
     "Front desk spends 2–4 hours/day on hold with insurance companies — delays treatment and frustrates patients.",
     "8–15 staff hours/month recovered; $2K–$5K fewer claim denials", 10),
    (12, "New Patient Intake Automation",
     "Patients fill out paper forms in the waiting room, causing delays and incomplete medical histories at check-in.",
     "5–10 min saved per new patient; better intake data improves case acceptance", 8),
    (14, "Review Generation + Reputation Bot",
     "Office gets 3–5 Google reviews/month while competitors get 20–30 — because no one asks at the right moment.",
     "15–30 additional reviews/month = better ranking = more new patients", 7),
]
for i, args in enumerate(dental_cards):
    row, col = divmod(i, 2)
    cx = d.M + col * (CW2 + Inches(0.2))
    cy = Inches(1.75) + row * Inches(2.75)
    use_case_card(s, cx, cy, *args, card_w=CW2, card_h=Inches(2.6))
d.footer(s, 11, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — DENTAL DEEP DIVE: PATIENT RECALL
# ═══════════════════════════════════════════════════════════════════════════════
realization_slide(
    12, 5, "Patient Recall + Appointment System", "Dental Practices",
    "Dental offices lose $50K–$200K/year in unscheduled recall patients who fell off the hygiene schedule. Staff manually calls from a list and reaches maybe 20% of them.",
    "OpenHands builds a HIPAA-compliant recall automation: pulls overdue recall patients from Dentrix/Eaglesoft via API, sends personalized SMS + email sequences with online scheduling link, auto-confirms appointments, sends 48h + day-of reminders, flags no-shows for rebooking.",
    "GitHub, Twilio, Calendly/Acuity, Postgres (HIPAA), SendGrid",
    "hipaa-auditor, patient-communication-specialist",
    "15–40 additional hygiene appointments/month = $3,000–$8,000 in production",
    "I have 400 patients who are 6 months overdue and my front desk doesn't have time to call all of them.",
    10, 1,
    [
        "Pull overdue recall patients from Dentrix/Eaglesoft API",
        "Send personalized SMS + email with online scheduling link",
        "Auto-confirm booking; send 48h + day-of reminders via Twilio",
        "Flag no-shows for immediate rebooking; log all activity in HIPAA Postgres",
    ]
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — SECTION: LAW FIRMS
# ═══════════════════════════════════════════════════════════════════════════════
section_divider("03", "Law Firms (Solo + Small)", "4 use cases · 26/35 score · CONDITIONAL · Document automation below UPL line", 13)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — LAW FIRM USE CASES (CARDS)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Law Firms — Use Cases", "Frame as 'document automation', not 'AI lawyer'. Stays well below UPL risk.")
law_cards = [
    (7, "Contract Generation + E-Sign",
     "Attorneys spend 30–90 min drafting standard engagement letters and NDAs from scratch — then chase clients for wet signatures via email.",
     "10–20 hours/month recovered at $300–$500/hr billable rate", 9),
    (8, "Client Intake Portal + Conflict Check",
     "New client intake is done over phone with a legal pad — no structured data, no conflict check, prospects fall through.",
     "2–5 additional retained clients/month who would have fallen off", 8),
    (16, "Billing Narrative Automation",
     "Attorneys lose 10–20% of billable time to poor time entry — vague descriptions, forgotten timers, and reduced bills.",
     "$2K–$8K/month in recovered billable time and reduced write-downs", 8),
    (15, "Discovery Document Review + Summary",
     "Associates spend 40–80 hours reviewing document productions in discovery at $200–$400/hr — no strategic value.",
     "$5K–$20K in associate time saved per discovery production", 8),
]
for i, args in enumerate(law_cards):
    row, col = divmod(i, 2)
    cx = d.M + col * (CW2 + Inches(0.2))
    cy = Inches(1.75) + row * Inches(2.75)
    use_case_card(s, cx, cy, *args, card_w=CW2, card_h=Inches(2.6))
d.footer(s, 14, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — LAW DEEP DIVE: CONTRACT GENERATION
# ═══════════════════════════════════════════════════════════════════════════════
realization_slide(
    15, 7, "Contract Generation + E-Signature Automation", "Law Firms (Solo + Small)",
    "Attorneys spend 30–90 minutes per client drafting standard engagement letters, NDAs, and boilerplate contracts from scratch in Word — and then chase clients for wet signatures via email.",
    "OpenHands builds a contract factory: attorney inputs client details + matter type → agent selects the right template → customizes with client/matter specifics → generates PDF → sends DocuSign link → logs signed version to Clio/case file automatically.",
    "GitHub, DocuSign API, Clio API, Google Drive, Stripe",
    "document-automation, legal-workflow-specialist",
    "10–20 hours/month recovered at $300–$500/hr = $3,000–$10,000 in recovered time",
    "I spend an hour drafting an NDA I've drafted 200 times before. That's an hour I'm not billing.",
    9, 1,
    [
        "Attorney inputs client name + matter type via simple form",
        "Agent selects correct template from firm library, customizes all fields",
        "Generates branded PDF; fires DocuSign e-signature request automatically",
        "Logs countersigned document to Clio; invoices retainer via Stripe",
    ]
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — SECTION: E-COMMERCE
# ═══════════════════════════════════════════════════════════════════════════════
section_divider("04", "E-Commerce Brands", "4 use cases · 29/35 score · CONDITIONAL · Shopify-first · Direct revenue recovery", 16)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 17 — E-COMMERCE USE CASES (CARDS)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "E-Commerce — Use Cases", "Shopify-native. Founder gets their mornings back. Revenue impact visible in week 1.")
ecomm_cards = [
    (10, "Product Description Factory",
     "Store owners manually write descriptions for every SKU — for a 500-product catalog, this is weeks of work and descriptions go stale.",
     "40–200 hours of copywriting saved; better SEO = organic traffic gains", 8),
    (11, "Abandoned Cart Recovery System",
     "70% of carts are abandoned. Basic Klaviyo 3-email sequence is generic — not tailored to what the customer actually browsed.",
     "10–25% cart recovery rate = $2K–$10K/month in recovered sales", 9),
    (19, "Customer Service Response Automation",
     "DTC founder with 500+ monthly orders receives 50–100 CS emails/day (WISMO, returns, questions) — loses 3–4 hours daily.",
     "3–4 hours/day recovered; 90% of CS volume automated", 8),
    (20, "Inventory Reorder Trigger System",
     "Owners stockout on bestsellers because they're monitoring inventory in a spreadsheet and reorder 2 weeks too late.",
     "Eliminates 2–4 stockout events/year = $10K–$80K in recovered sales", 7),
]
for i, args in enumerate(ecomm_cards):
    row, col = divmod(i, 2)
    cx = d.M + col * (CW2 + Inches(0.2))
    cy = Inches(1.75) + row * Inches(2.75)
    use_case_card(s, cx, cy, *args, card_w=CW2, card_h=Inches(2.6))
d.footer(s, 17, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 18 — E-COMM DEEP DIVE: ABANDONED CART RECOVERY
# ═══════════════════════════════════════════════════════════════════════════════
realization_slide(
    18, 11, "Abandoned Cart Recovery System", "E-Commerce (Shopify)",
    "70% of shopping carts are abandoned. Most stores use Klaviyo's basic 3-email sequence — generic and untailored to what the customer was actually looking at or their purchase history.",
    "OpenHands builds a personalized recovery system: monitors cart abandonment via Shopify webhook → triggers a custom 5-step sequence (email + SMS) personalized to cart contents, customer history, and abandonment timing → A/B tests subject lines → reports recovered revenue weekly.",
    "GitHub, Shopify API, Klaviyo API, Twilio, Stripe",
    "ecommerce-specialist, email-campaign-agent",
    "10–25% cart recovery rate on abandoned revenue = $2,000–$10,000/month in recovered sales",
    "I know people put things in their cart and leave. I just don't have a system to bring them back.",
    9, 1,
    [
        "Shopify webhook fires on cart abandonment → log session data",
        "Enrich with customer history from Klaviyo; personalize message per cart contents",
        "Send 5-step email + SMS sequence (Day 0, Day 1, Day 3, Day 5, Day 7)",
        "A/B test subject lines; report recovered revenue weekly to Stripe dashboard",
    ]
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 19 — SECTION: ACCOUNTING
# ═══════════════════════════════════════════════════════════════════════════════
section_divider("05", "Accounting / Bookkeeping", "4 use cases · 27/35 score · CONDITIONAL · QuickBooks-first · Tax season ROI is acute", 19)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 20 — ACCOUNTING USE CASES (CARDS)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Accounting — Use Cases", "Frame around 'monthly close' and 'tax season survival' — these are their highest-pain moments")
acct_cards = [
    (9, "Monthly Close + Client Reporting",
     "Bookkeepers spend 3–5 days per month per client doing manual reconciliation, then 2–3 hours building P&L summaries in Excel.",
     "20–40 hours/month recovered; can serve 2× more clients at same staff level", 8),
    (18, "Tax Document Collection + Organizer",
     "Each Jan–Mar: accountants spend 40% of time chasing clients for W-2s, 1099s, and docs that arrive in different formats and batches.",
     "20–40 hours recovered in tax season; capacity for 30% more clients", 9),
    (17, "AP Processing + Vendor Management",
     "AP staff manually enter vendor invoices from email attachments into QuickBooks — tedious, error-prone, risks double payments.",
     "5–15 hours/month recovered per AP person; fewer errors and duplicate payments", 7),
    (22, "Client Advisory Digest",
     "Accountants only talk to clients during tax season — missing anomalies, cash flow issues, and advisory upsell opportunities year-round.",
     "Upgrades clients to advisory engagements at $500–$2K/month vs. $100/month bookkeeping", 7),
]
for i, args in enumerate(acct_cards):
    row, col = divmod(i, 2)
    cx = d.M + col * (CW2 + Inches(0.2))
    cy = Inches(1.75) + row * Inches(2.75)
    use_case_card(s, cx, cy, *args, card_w=CW2, card_h=Inches(2.6))
d.footer(s, 20, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 21 — ACCOUNTING DEEP DIVE: MONTHLY CLOSE
# ═══════════════════════════════════════════════════════════════════════════════
realization_slide(
    21, 9, "Monthly Close + Client Reporting Automation", "Accounting / Bookkeeping Firms",
    "Bookkeepers spend 3–5 days per month per client doing manual reconciliation in QuickBooks, then another 2–3 hours building a client-facing P&L summary in Excel or PowerPoint.",
    "OpenHands builds a monthly close pipeline: pulls transactions from QuickBooks/Xero API → auto-categorizes → flags anomalies → generates a branded PDF client report with P&L, cash flow statement, key ratios, and a plain-English narrative → delivers via client portal.",
    "GitHub, QuickBooks API, Xero API, Stripe, Google Drive, SendGrid",
    "financial-analyst, document-automation",
    "20–40 hours/month recovered per client → serve 2× more clients at same staff level",
    "Close week is a nightmare. I'm manually pulling the same numbers from QuickBooks every month for every client.",
    8, 1,
    [
        "Pull all transactions from QuickBooks/Xero API for the close period",
        "Auto-categorize + flag anomalies for accountant review",
        "Generate branded PDF: P&L, cash flow, key ratios, plain-English narrative",
        "Deliver via client portal link; log delivery timestamp; auto-archive to Google Drive",
    ]
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 22 — EXPANSION VERTICALS: MED SPA + HVAC
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Expansion Verticals — Month 5+ (Med Spa + HVAC)", "Add these once the core 5 verticals are proven. Same OpenHands runtime, new AGENTS.md.")
exp_cards = [
    (24, "Med Spa Retail Upsell Automation",
     "Med spa owners know clients should buy retail skincare between treatments but staff forget to recommend — $500–$2K/month in retail revenue left on the table.",
     "Med Spas / Aesthetic Clinics",
     "$500–$2,000/month in incremental retail revenue; improved client retention", 7),
    (25, "HVAC Quote Follow-Up + Review Automation",
     "Contractors send 30–50 quotes/month and follow up on maybe 20% — the other 80% go cold and they never know which jobs they lost or why.",
     "HVAC / Plumbing Contractors",
     "10–20% more quotes converted = 2–4 additional jobs/month at $500–$2K each", 6),
]
exp_w = (d.CW - Inches(0.2)) / 2
for i, (num, title, pain, vertical, value, urgency) in enumerate(exp_cards):
    cx = d.M + i * (exp_w + Inches(0.2))
    d.rect(s, cx, Inches(1.75), exp_w, Inches(4.5), b.SOFT, radius=0.06, shadow=True)
    d.rect(s, cx, Inches(1.75), Inches(0.08), Inches(4.5), b.AMBER, radius=0.02)
    d.text(s, f"#{num}", cx + Inches(0.22), Inches(1.87), Inches(0.6), Inches(0.45),
           size=18, color=b.AMBER, bold=True)
    d.rect(s, cx + exp_w - Inches(1.05), Inches(1.87), Inches(0.87), Inches(0.30), b.AMBER, radius=0.06)
    d.text(s, f"{urgency}/10", cx + exp_w - Inches(1.05), Inches(1.88), Inches(0.87), Inches(0.28),
           size=10, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, title, cx + Inches(0.22), Inches(2.38), exp_w - Inches(0.35), Inches(0.6),
           size=15, color=b.NAVY, bold=True, shrink=True)
    d.text(s, vertical.upper(), cx + Inches(0.22), Inches(3.06), exp_w - Inches(0.35), Inches(0.25),
           size=9, color=b.MUTED, bold=True)
    d.rect(s, cx + Inches(0.22), Inches(3.36), exp_w - Inches(0.44), Inches(0.03), b.GRID)
    d.text(s, pain, cx + Inches(0.22), Inches(3.48), exp_w - Inches(0.35), Inches(1.42),
           size=11, color=b.INK, shrink=True, ls=1.2)
    d.rect(s, cx, Inches(5.8), exp_w, Inches(0.45), b.LIGHT_TEAL, radius=0.04)
    d.text(s, f"Value: {value}", cx + Inches(0.2), Inches(5.84), exp_w - Inches(0.3), Inches(0.37),
           size=10, color=b.ACCENT, bold=True, shrink=True)
d.footer(s, 22, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 23 — PORTFOLIO WAVE MAP
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Portfolio Wave Map — 16 Quick Wins, 9 Strategic Bets", "Value × Feasibility · Wave 1 = ship in 0–4 weeks · Wave 2 = 4–12 weeks")
wave1 = ["#1 TC Bot", "#2 Listing Desc.", "#3 Lead Scoring", "#4 CMA Gen.", "#5 Patient Recall",
         "#6 Insurance Pre-Auth", "#7 Contract Gen.", "#8 Client Intake", "#9 Monthly Close",
         "#10 Product Desc.", "#11 Cart Recovery", "#12 New Patient Intake", "#14 Review Bot",
         "#16 Billing Narrative", "#18 Tax Doc Collect.", "#19 CS Response"]
wave2 = ["#13 Buyer/Seller Match", "#15 Discovery Review", "#17 AP Processing",
         "#20 Inventory Reorder", "#21 Commission Dash", "#22 Advisory Digest",
         "#23 Social Calendar", "#24 MedSpa Upsell", "#25 HVAC Quotes"]
# wave 1 box
d.rect(s, d.M, Inches(1.72), Inches(7.8), Inches(4.95), b.SOFT, radius=0.06)
d.rect(s, d.M, Inches(1.72), Inches(7.8), Inches(0.4), b.TEAL, radius=0.04)
d.text(s, "WAVE 1 — QUICK WINS  (0–4 weeks, show ROI in 30 days)",
       d.M + Inches(0.2), Inches(1.74), Inches(7.4), Inches(0.36), size=11, color=b.NAVY, bold=True)
for i, item in enumerate(wave1):
    row, col = divmod(i, 4)
    ix = d.M + Inches(0.2) + col * Inches(1.88)
    iy = Inches(2.26) + row * Inches(0.58)
    d.rect(s, ix, iy, Inches(1.75), Inches(0.44), b.WHITE, radius=0.04, shadow=True)
    d.text(s, item, ix + Inches(0.1), iy + Inches(0.08), Inches(1.55), Inches(0.3),
           size=9.5, color=b.NAVY, bold=True, shrink=True)
# wave 2 box
d.rect(s, d.M + Inches(8.0), Inches(1.72), Inches(4.55), Inches(4.95), b.SOFT, radius=0.06)
d.rect(s, d.M + Inches(8.0), Inches(1.72), Inches(4.55), Inches(0.4), b.AMBER, radius=0.04)
d.text(s, "WAVE 2 — STRATEGIC BETS  (4–12 weeks)",
       d.M + Inches(8.2), Inches(1.74), Inches(4.1), Inches(0.36), size=11, color=b.NAVY, bold=True)
for i, item in enumerate(wave2):
    iy = Inches(2.26) + i * Inches(0.52)
    d.rect(s, d.M + Inches(8.2), iy, Inches(4.1), Inches(0.42), b.WHITE, radius=0.04, shadow=True)
    d.text(s, item, d.M + Inches(8.4), iy + Inches(0.08), Inches(3.7), Inches(0.3),
           size=9.5, color=b.NAVY, bold=True, shrink=True)
d.footer(s, 23, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 24 — EXECUTION ROADMAP
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "6-Month Execution Roadmap", "Start narrow. Prove the model. Expand vertically. Compound the moat.")
months = [
    ("Month 1", b.TEAL, "Real Estate", ["Deploy TC Bot (#1)", "Listing Description system (#2)", "Lead Scoring CRM (#3)", "Target: 2 paying clients @ $3K/mo = $6K MRR"]),
    ("Month 2", b.TEAL, "Add Dental", ["Patient Recall system (#5)", "Insurance Pre-Auth Bot (#6)", "New Patient Intake (#12)", "Target: +2 dental clients @ $3K/mo = $12K MRR"]),
    ("Month 3", b.TEAL, "Add Law", ["Contract Generation (#7)", "Client Intake Portal (#8)", "Billing Narrative (#16)", "Target: +2 law firm clients = $18K MRR"]),
    ("Month 4", b.AMBER, "Add E-Commerce", ["Product Description Factory (#10)", "Cart Recovery (#11)", "CS Response Automation (#19)", "Target: +3 e-comm clients = $27K MRR"]),
    ("Month 5", b.AMBER, "Add Accounting", ["Monthly Close + Reporting (#9)", "Tax Doc Collection (#18)", "AP Processing (#17)", "Target: +2 accounting clients = $33K MRR"]),
    ("Month 6", b.AMBER, "Wave 2 + Expansion", ["Wave 2 builds per vertical (deeper moat)", "Med Spa & HVAC pilots", "Vertical-specific subagent development", "Target: $40K–$50K MRR + niche content machine live"]),
]
month_w = (d.CW - Inches(0.5)) / 6
for i, (label, col, focus, items) in enumerate(months):
    mx = d.M + i * (month_w + Inches(0.1))
    d.rect(s, mx, Inches(1.72), month_w, Inches(4.95), b.SOFT, radius=0.04)
    d.rect(s, mx, Inches(1.72), month_w, Inches(0.45), col, radius=0.04)
    d.text(s, label, mx + Inches(0.1), Inches(1.75), month_w - Inches(0.15), Inches(0.4),
           size=10, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, focus, mx + Inches(0.1), Inches(2.26), month_w - Inches(0.15), Inches(0.38),
           size=10.5, color=b.NAVY if col == b.TEAL else b.INK, bold=True, shrink=True)
    for j, item in enumerate(items):
        iy = Inches(2.76) + j * Inches(0.82)
        is_target = item.startswith("Target:")
        d.text(s, item, mx + Inches(0.1), iy, month_w - Inches(0.18), Inches(0.78),
               size=9 if not is_target else 9,
               color=b.GOLD if is_target else b.INK,
               bold=is_target, shrink=True, ls=1.15)
d.footer(s, 24, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 25 — TECHNICAL STACK
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "How It Works — The Technical Stack", "Three layers: runtime, specialists, integrations. You manage the orchestration.")
layers = [
    ("RUNTIME LAYER", b.NAVY, b.WHITE, b.TEAL,
     "OpenHands (77K stars · All-Hands-AI)",
     "Self-hosted on $20/mo VPS. Reads codebases, edits files, runs tests, opens PRs, deploys apps. Model-agnostic — runs Claude, GPT-4o, Gemini. CLI: pip install openhands-ai.",
     ["Autonomous file editing", "Test runner + CI integration", "Git + PR workflow", "Sub-agent delegation (v1 SDK)", "MCP-native integration layer"]),
    ("SPECIALIST LAYER", b.NAVY_2, b.WHITE, b.AMBER,
     "131 Subagents (VoltAgent)",
     "Specialist agents installed per vertical. Each inherits parent LLM and shares workspace with independent EventLog. Spawn by name with custom prompts.",
     ["crm-specialist", "hipaa-auditor", "document-automation", "legal-workflow", "ecommerce-specialist", "financial-analyst"]),
    ("INTEGRATION LAYER", b.SOFT, b.NAVY, b.ACCENT,
     "14,000+ MCP Servers",
     "Turnkey integrations to every business system an SMB uses. Tavily MCP already proxied through OpenHands app server for enterprise deployments.",
     ["GitHub · Stripe · Twilio · SendGrid", "QuickBooks · Xero · Postgres", "Shopify · Klaviyo · Gorgias", "DocuSign · Clio · Follow Up Boss", "Google Calendar · Drive · Gmail", "Calendly · Notion · Slack"]),
]
layer_w = (d.CW - Inches(0.4)) / 3
for i, (label, bg, fg, accent, name, desc, features) in enumerate(layers):
    lx = d.M + i * (layer_w + Inches(0.2))
    d.rect(s, lx, Inches(1.72), layer_w, Inches(5.0), bg, radius=0.06, shadow=True)
    d.text(s, label, lx + Inches(0.2), Inches(1.82), layer_w - Inches(0.3), Inches(0.28),
           size=9, color=accent, bold=True)
    d.text(s, name, lx + Inches(0.2), Inches(2.14), layer_w - Inches(0.3), Inches(0.5),
           size=13.5, color=fg, bold=True, shrink=True)
    d.rect(s, lx + Inches(0.2), Inches(2.72), layer_w - Inches(0.4), Inches(0.03), accent)
    d.text(s, desc, lx + Inches(0.2), Inches(2.84), layer_w - Inches(0.3), Inches(1.05),
           size=10, color=fg if bg != b.SOFT else b.INK, shrink=True, ls=1.2)
    for j, feat in enumerate(features):
        fy = Inches(4.0) + j * Inches(0.44)
        d.rect(s, lx + Inches(0.2), fy + Inches(0.06), Inches(0.1), Inches(0.1), accent, radius=0.05)
        d.text(s, feat, lx + Inches(0.38), fy, layer_w - Inches(0.5), Inches(0.38),
               size=9.5, color=fg if bg != b.SOFT else b.INK, shrink=True)
d.footer(s, 25, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 26 — PRICING MODEL
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Why $2K–$5K/Month Works — The Unit Economics", "You're 5× cheaper than a dev shop and 10× faster to deliver value")
# comparison table
comparison = [
    ("Metric",              "Junior Developer",     "Dev Shop / Agency",    "Your AI Team"),
    ("Monthly cost",        "$6,000–$10,000",       "$10,000–$25,000",      "$2,000–$5,000"),
    ("Setup time",          "2–4 weeks to hire",    "4–8 weeks onboarding", "1 week (AGENTS.md)"),
    ("Works nights/wknds",  "No",                   "No",                   "Yes — 24/7"),
    ("Vertical expertise",  "Generic",              "Generic",              "Niche-specific subagents"),
    ("Scales to N clients", "No — 1 client only",  "Sometimes",            "Yes — same runtime"),
    ("Your margin",         "N/A",                  "N/A",                  "~70–80% gross"),
]
col_w_t = [Inches(2.6), Inches(2.7), Inches(2.7), Inches(2.9)]
col_x   = [d.M, d.M + Inches(2.7), d.M + Inches(5.5), d.M + Inches(8.3)]
row_h   = Inches(0.54)
for ri, row in enumerate(comparison):
    for ci, cell in enumerate(row):
        ry = Inches(1.72) + ri * row_h
        is_header = ri == 0
        is_your   = ci == 3
        bg = b.NAVY if is_header else (b.LIGHT_TEAL if is_your and not is_header else b.WHITE if ri % 2 == 0 else b.SOFT)
        d.rect(s, col_x[ci], ry, col_w_t[ci] - Inches(0.05), row_h - Inches(0.03), bg)
        tc = b.WHITE if is_header else (b.NAVY if is_your else b.INK)
        d.text(s, cell, col_x[ci] + Inches(0.12), ry + Inches(0.1), col_w_t[ci] - Inches(0.2), row_h - Inches(0.12),
               size=10.5 if not is_header else 10, color=tc, bold=(is_header or is_your), shrink=True, align=PP_ALIGN.LEFT)
# bottom highlight
d.rect(s, d.M, Inches(5.8), d.CW, Inches(0.66), b.NAVY, radius=0.06)
d.text(s, "At $3K/mo × 10 clients = $30K MRR. At $4K/mo × 15 clients = $60K MRR. Two-person team. No office. No investors.",
       d.M + Inches(0.25), Inches(5.88), d.CW - Inches(0.4), Inches(0.5), size=12.5, color=b.GOLD, bold=True, shrink=True)
d.footer(s, 26, TOTAL)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 27 — CLOSING / NEXT STEPS
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.text(s, "THE ASK", Inches(0.45), Inches(1.3), Inches(10), Inches(0.45),
       size=13, color=b.TEAL, bold=True)
d.text(s, "Start with Real Estate. Ship 3 use cases. Land 2 clients.",
       Inches(0.45), Inches(1.82), Inches(10), Inches(1.0),
       size=36, color=b.WHITE, bold=True, shrink=True)
d.rect(s, Inches(0.45), Inches(2.94), Inches(4.5), Inches(0.05), b.TEAL)
next_steps = [
    ("Week 1", "Self-host OpenHands on a $20/mo VPS. Record the setup once as a video."),
    ("Week 2", "Build TC Bot + Listing Description system for Real Estate. Time: ~1 week with OpenHands."),
    ("Week 3", "Find 2 real estate agents via LinkedIn. Offer a 30-day pilot at $500. Show the TC Bot live."),
    ("Week 4", "Convert pilots to $2K–$3K/month retainers. Document everything as a case study. Publish on LinkedIn."),
    ("Month 2", "Add Dental (Patient Recall system). Repeat the playbook. AGENTS.md is already written."),
    ("Month 6", "10 clients × $3K = $30K MRR. Hire one person to do onboarding calls. You do product."),
]
for i, (label, step) in enumerate(next_steps):
    sy = Inches(3.18) + i * Inches(0.64)
    d.rect(s, Inches(0.45), sy, Inches(1.1), Inches(0.46), b.TEAL, radius=0.04)
    d.text(s, label, Inches(0.45), sy + Inches(0.07), Inches(1.1), Inches(0.35),
           size=10, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, step, Inches(1.7), sy + Inches(0.07), Inches(10.5), Inches(0.42),
           size=10.5, color=b.LIGHT_TEAL, shrink=True)
d.rect(s, Inches(0.45), Inches(7.0), Inches(12.2), Inches(0.3), b.NAVY_2)
d.text(s, "OpenHands: github.com/All-Hands-AI/OpenHands  ·  77K stars  ·  MIT license  ·  pip install openhands-ai",
       Inches(0.55), Inches(7.04), Inches(12.0), Inches(0.25), size=9, color=b.MUTED)
d.footer(s, 27, TOTAL, dark=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SAVE + VALIDATE
# ═══════════════════════════════════════════════════════════════════════════════
d.save(OUT_PATH)
print(f"\nDeck saved: {OUT_PATH}")
print(f"Total slides: {d.n}")
print("\nNext: python3 preview_pptx.py to generate contact sheets for QA")
