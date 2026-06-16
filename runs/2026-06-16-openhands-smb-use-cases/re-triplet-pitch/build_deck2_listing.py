#!/usr/bin/env python3
"""Deck 2 of 3 — Listing Description + MLS Auto-Post (12 slides)"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, Brand, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor

OUT_DIR  = os.path.join(os.path.dirname(__file__), "decks")
OUT_PATH = os.path.join(OUT_DIR, "02-listing-description-pitch.pptx")
FOOTER   = "Listing Description + MLS Auto-Post · AI Engineering for Real Estate"
TOTAL    = 12
os.makedirs(OUT_DIR, exist_ok=True)

d = Deck(footer=FOOTER)
b = d.b
GOLD = b.GOLD   # primary accent for this deck

def chip(s, text, left, top, w=Inches(2.4), h=Inches(0.32), bg=None, fg=None):
    bg = bg or GOLD
    fg = fg or b.NAVY
    d.rect(s, left, top, w, h, bg, radius=0.06)
    d.text(s, text, left+Inches(0.12), top+Inches(0.04), w-Inches(0.18), h-Inches(0.06),
           size=10, color=fg, bold=True)

def stat_tile(s, num, label, note, left, top, w=Inches(3.8), h=Inches(1.8), num_col=None):
    num_col = num_col or GOLD
    d.rect(s, left, top, w, h, b.NAVY, radius=0.06, shadow=True)
    d.text(s, num,   left+Inches(0.22), top+Inches(0.18), w-Inches(0.3), Inches(0.72),
           size=36, color=num_col, bold=True, shrink=True)
    d.text(s, label, left+Inches(0.22), top+Inches(0.95), w-Inches(0.3), Inches(0.4),
           size=12, color=b.WHITE, bold=True, shrink=True)
    d.text(s, note,  left+Inches(0.22), top+Inches(1.38), w-Inches(0.3), Inches(0.35),
           size=9.5, color=b.LIGHT_TEAL, shrink=True)

def feature_card(s, num, title, body, left, top, w=Inches(5.9), h=Inches(2.4)):
    d.rect(s, left, top, w, h, b.WHITE, radius=0.05, shadow=True)
    d.rect(s, left, top, Inches(0.08), h, GOLD, radius=0.02)
    d.text(s, str(num), left+Inches(0.18), top+Inches(0.14),
           Inches(0.36), Inches(0.36), size=14, color=GOLD, bold=True)
    d.text(s, title, left+Inches(0.65), top+Inches(0.14),
           w-Inches(0.82), Inches(0.42), size=13, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, left+Inches(0.18), top+Inches(0.62), w-Inches(0.36), Inches(0.03), b.SOFT)
    d.text(s, body, left+Inches(0.18), top+Inches(0.74),
           w-Inches(0.36), h-Inches(0.86), size=10.5, color=b.INK, shrink=True, ls=1.2)

def process_step(s, n, title, desc, left, top, w=Inches(12.1)):
    h = Inches(0.72)
    bg = GOLD if n % 2 == 1 else b.NAVY
    fg = b.NAVY if bg == GOLD else b.WHITE
    d.rect(s, left, top, Inches(0.52), h, bg, radius=0.04)
    d.text(s, str(n), left, top+Inches(0.12), Inches(0.52), Inches(0.48),
           size=16, color=fg, bold=True, align=PP_ALIGN.CENTER)
    d.rect(s, left+Inches(0.62), top, w-Inches(0.62), h, b.SOFT, radius=0.04)
    d.text(s, title, left+Inches(0.82), top+Inches(0.06),
           Inches(3.5), Inches(0.32), size=11.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, desc, left+Inches(0.82), top+Inches(0.38),
           w-Inches(1.1), Inches(0.3), size=10, color=b.INK, shrink=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, d.W-Inches(0.12), 0, Inches(0.12), d.H, GOLD)
d.rect(s, 0, d.H-Inches(0.12), d.W, Inches(0.12), GOLD)
d.text(s, "DONE-FOR-YOU AI ENGINEERING · REAL ESTATE", d.M, Inches(1.0),
       Inches(10), Inches(0.38), size=12, color=GOLD, bold=True)
d.text(s, "Listing Description\n+ MLS Auto-Post", d.M, Inches(1.52),
       Inches(10), Inches(2.6), size=54, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(4.3), Inches(5.5), Inches(0.06), GOLD)
d.text(s, "From photo shoot to live listing across every platform — in 15 minutes, not 2 hours.",
       d.M, Inches(4.5), Inches(10.5), Inches(0.62), size=16, color=b.LIGHT_TEAL, shrink=True)
chip(s, "MLS + Zillow + Realtor.com + Social", d.M, Inches(5.35), w=Inches(3.4))
chip(s, "$2,000/month flat", d.M+Inches(3.6), Inches(5.35), w=Inches(1.8), bg=b.TEAL, fg=b.NAVY)
chip(s, "Setup in 1 week", d.M+Inches(5.6), Inches(5.35), w=Inches(1.6), bg=b.AMBER)
d.footer(s, 1, TOTAL, dark=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.rect(s, 0, 0, d.W, Inches(0.12), GOLD)
d.rect(s, 0, Inches(0.12), d.W, Inches(1.2), b.NAVY)
d.text(s, "THE PROBLEM", d.M, Inches(0.18), Inches(6), Inches(0.28),
       size=10, color=GOLD, bold=True)
d.text(s, '"Every listing costs me 2 hours before the sign even goes in the yard."',
       d.M, Inches(0.48), d.CW, Inches(0.78), size=20, color=b.WHITE, italic=True, shrink=True)
pain_cards = [
    ("You're a copywriter now — whether you like it or not",
     "Every listing requires a compelling MLS description, a Zillow blurb, a Facebook post, and an Instagram caption. You write all four from scratch. Every time."),
    ("Inconsistent quality hurts your brand",
     "On a busy week your descriptions are rushed and generic. On a slow week they're great. Buyers notice. Sellers definitely notice when their listing gets fewer calls."),
    ("You're a data entry operator too",
     "After you write the description, you upload it to MLS. Then Zillow. Then Realtor.com. Then type it into Facebook. The same information, entered four different ways, four different times."),
]
cw3 = (d.CW - Inches(0.4)) / 3
for i, (title, body) in enumerate(pain_cards):
    cx = d.M + i*(cw3+Inches(0.2))
    d.rect(s, cx, Inches(1.5), cw3, Inches(4.3), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, cx, Inches(1.5), cw3, Inches(0.06), GOLD, radius=0.02)
    d.text(s, title, cx+Inches(0.2), Inches(1.68), cw3-Inches(0.3), Inches(0.78),
           size=13, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, cx+Inches(0.2), Inches(2.52), cw3-Inches(0.4), Inches(0.03), b.GRID)
    d.text(s, body, cx+Inches(0.2), Inches(2.64), cw3-Inches(0.3), Inches(2.84),
           size=11, color=b.INK, shrink=True, ls=1.25)
d.text(s, "The Listing Assistant writes, formats, and posts — so you can be at your next showing.",
       d.M, Inches(6.05), d.CW, Inches(0.38), size=12, color=b.ACCENT, bold=True, shrink=True)
d.footer(s, 2, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — THE HIDDEN COST OF SLOW LISTINGS
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The Hidden Cost: Slow Listings Sell for Less",
         "Time-to-market is the metric most agents never track — and it directly affects sale price")
stats = [
    ("95 min", "per listing", "Average agent time on description + upload per NAR survey"),
    ("6 listings", "per month", "Typical active agent volume — 570 min/month on admin"),
    ("1–3%", "less", "Properties listed >7 days after photography sell for 1–3% less on average"),
    ("$4,500", "per deal", "At $300K avg price, 1.5% discount = $4,500 left on the table"),
]
sw = (d.CW - Inches(0.6)) / 4
for i, (num, label, note) in enumerate(stats):
    stat_tile(s, num, label, note, d.M + i*(sw+Inches(0.2)), Inches(1.85), w=sw, num_col=GOLD)
# the math box
d.rect(s, d.M, Inches(3.88), d.CW, Inches(1.65), b.SOFT, radius=0.05)
d.text(s, "Your annual exposure from slow listings",
       d.M+Inches(0.25), Inches(3.98), Inches(6), Inches(0.38),
       size=12, color=b.NAVY, bold=True)
math_items = [
    ("Listings per year:", "72 (6/month)"),
    ("Time spent on description + upload:", "72 × 95 min = 114 hours/year"),
    ("At $200/hr opportunity cost:", "$22,800 in time lost to listing admin"),
    ("Listings delayed 3+ days (est. 30%):", "22 listings × 1.5% price discount × $300K avg = $99,000 in reduced sale prices"),
]
for i, (label, val) in enumerate(math_items):
    ly = Inches(4.42) + i*Inches(0.26)
    d.text(s, label, d.M+Inches(0.25), ly, Inches(4.2), Inches(0.24),
           size=10.5, color=b.MUTED, bold=True)
    d.text(s, val, d.M+Inches(4.4), ly, Inches(7.8), Inches(0.24),
           size=10.5, color=b.INK, shrink=True)
d.rect(s, d.M, Inches(5.72), d.CW, Inches(0.72), b.NAVY, radius=0.05)
d.text(s, "The Listing Assistant costs $24,000/year. It eliminates $22,800 in time cost and up to $99,000 in reduced sale prices from slow time-to-market.",
       d.M+Inches(0.25), Inches(5.8), d.CW-Inches(0.4), Inches(0.56),
       size=11.5, color=GOLD, bold=True, shrink=True)
d.footer(s, 3, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — SIX CAPABILITIES
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Six Capabilities in One System",
         "Write, format, adapt, post, track, and report — all from one intake form")
caps = [
    ("MLS Description Writer", "Generates a compliant, compelling MLS description from your intake notes. Trained on high-performing listings in your price range and market."),
    ("Platform Copy Variants", "Automatically writes separate copy for Zillow, Realtor.com, Facebook Marketplace, and an Instagram caption — each formatted for that platform's character limits and audience."),
    ("Photo Formatter", "Uploads your photos, reorders them by standard sequence (exterior, living areas, kitchen, bedrooms, baths, yard), and resizes for each platform's specs."),
    ("Brand Voice Matching", "Learns your writing style from your past listings. Descriptions sound like you — not a template. One round of edits per listing included."),
    ("Scheduled Publishing", "You approve a preview, set a go-live time, and the bot posts to all platforms simultaneously. No more manual uploads at midnight before open house."),
    ("Listing Performance Tracker", "Tracks views, saves, and inquiries per listing across platforms. Monthly report shows which listings generated the most interest and why."),
]
cw2 = (d.CW - Inches(0.2)) / 2
for i, (title, body) in enumerate(caps):
    row, col = divmod(i, 2)
    cx = d.M + col*(cw2+Inches(0.2))
    cy = Inches(1.75) + row*Inches(1.72)
    feature_card(s, i+1, title, body, cx, cy, w=cw2, h=Inches(1.62))
d.footer(s, 4, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — STEP-BY-STEP PROCESS
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "From Photo Shoot to Live Listing — The Process",
         "Seven steps. You handle two of them. The bot handles the rest.")
steps = [
    ("Listing Intake Form", "Fill out the intake: address, key features, selling points, price, your tone notes. 10 minutes max."),
    ("Photo Upload", "Drop your photos into the deal portal — any order, any device, any format. The bot sorts and formats them."),
    ("Description Generation", "Bot writes the MLS description + all platform variants. Takes 2 minutes. Delivered to your preview inbox."),
    ("Your 5-Min Review", "You read the draft, request one round of edits if needed (optional), and hit approve. That's your only required action."),
    ("Platform Formatting", "Bot resizes photos, formats copy for each platform's requirements, and queues everything for go-live."),
    ("Scheduled Go-Live", "At your set time (or immediately on approval), bot posts to MLS, Zillow, Realtor.com, Facebook, and Instagram simultaneously."),
    ("Performance Tracking", "Listing goes live — bot monitors views, saves, and inquiry count. Weekly digest in your inbox. Monthly report at close."),
]
for i, (title, desc) in enumerate(steps):
    process_step(s, i+1, title, desc, d.M, Inches(1.75)+i*Inches(0.78))
d.footer(s, 5, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — SAMPLE LISTING OUTPUT
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "What the Output Looks Like", "Same property — four platform-ready versions, generated in 2 minutes")
# property details strip
d.rect(s, d.M, Inches(1.75), d.CW, Inches(0.5), b.NAVY, radius=0.04)
d.text(s, "Sample Property:  3BR / 2BA · 1,850 sq ft · $385,000 · Updated kitchen · Fenced yard · Good school district",
       d.M+Inches(0.2), Inches(1.82), d.CW-Inches(0.3), Inches(0.38),
       size=10.5, color=b.LIGHT_TEAL, shrink=True)
outputs = [
    ("MLS DESCRIPTION", GOLD,
     "Beautifully updated 3-bedroom, 2-bath home in a sought-after neighborhood zoned for top-rated schools. The recently renovated kitchen features quartz countertops, stainless appliances, and a breakfast bar that opens to the light-filled living area — perfect for everyday living and entertaining. A private fenced backyard with a covered patio extends your living space outdoors. Primary suite with walk-in closet and ensuite bath. Two-car garage. Minutes from shopping, dining, and major commuter routes. Move-in ready — schedule your showing today."),
    ("ZILLOW LISTING REMARKS", b.TEAL,
     "Updated 3BR/2BA · Renovated kitchen with quartz counters · Private fenced yard with covered patio · Top-rated school district · Two-car garage · Move-in ready. This home checks every box — don't miss it."),
    ("FACEBOOK MARKETPLACE", b.AMBER,
     "🏡 JUST LISTED — $385,000 · 3BD / 2BA in [Neighborhood Name]\n✅ Newly renovated kitchen\n✅ Fenced backyard with covered patio\n✅ Top school district\n✅ 2-car garage\nSchedule a private showing: [your link]"),
    ("INSTAGRAM CAPTION", b.CORAL,
     "New listing alert 🏠✨ 3BR/2BA in [Neighborhood] just hit the market at $385K — and that kitchen renovation is 🔥 Swipe to see the backyard. Link in bio to schedule your tour. #JustListed #[YourCity]RealEstate #HomesFor Sale"),
]
ow = (d.CW - Inches(0.3)) / 2
for i, (label, color, text) in enumerate(outputs):
    row, col = divmod(i, 2)
    ox = d.M + col*(ow+Inches(0.15))
    oy = Inches(2.42) + row*Inches(2.1)
    d.rect(s, ox, oy, ow, Inches(1.95), b.SOFT, radius=0.04, shadow=True)
    d.rect(s, ox, oy, ow, Inches(0.32), color, radius=0.04)
    d.text(s, label, ox+Inches(0.14), oy+Inches(0.06), ow-Inches(0.22), Inches(0.24),
           size=9, color=b.NAVY if color==GOLD else b.WHITE, bold=True)
    d.text(s, text, ox+Inches(0.14), oy+Inches(0.4), ow-Inches(0.22), Inches(1.48),
           size=9.5, color=b.INK, shrink=True, ls=1.2)
d.footer(s, 6, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — PLATFORM COVERAGE
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Every Platform, One Submission",
         "One intake form. Five simultaneous posts. Zero manual data entry.")
platforms = [
    ("MLS", b.NAVY, "Primary listing database. Auto-formatted to your local MLS character limits and required fields. Compliant copy every time.", "Primary distribution", "Thousands of buyer agents"),
    ("Zillow", b.TEAL, "Custom Zillow remarks separate from MLS description. Optimized for the Zillow buyer search algorithm and mobile reading patterns.", "100M+ monthly visitors", "Largest buyer audience online"),
    ("Realtor.com", GOLD, "Realtor.com listing remarks formatted for their platform's display requirements. Agent profile linked automatically.", "40M+ monthly visitors", "Strong luxury + move-up segment"),
    ("Facebook Marketplace", b.AMBER, "Property post with photos and CTA link. Formatted for Facebook's housing algorithm and local buyer groups.", "Social discovery", "Local buyers and referral network"),
    ("Instagram", b.CORAL, "Caption with relevant hashtags for your market. Photos formatted for square and portrait display. Optional story assets.", "Visual engagement", "Younger buyers + referral reach"),
]
pw = (d.CW - Inches(0.8)) / 5
for i, (name, color, desc, reach_label, reach_val) in enumerate(platforms):
    px = d.M + i*(pw+Inches(0.2))
    d.rect(s, px, Inches(1.75), pw, Inches(5.1), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, px, Inches(1.75), pw, Inches(0.52), color, radius=0.04)
    d.text(s, name, px+Inches(0.12), Inches(1.82), pw-Inches(0.2), Inches(0.38),
           size=14, color=b.WHITE if color!=GOLD else b.NAVY, bold=True, shrink=True)
    d.text(s, desc, px+Inches(0.12), Inches(2.38), pw-Inches(0.2), Inches(2.2),
           size=9.5, color=b.INK, shrink=True, ls=1.2)
    d.rect(s, px+Inches(0.12), Inches(4.68), pw-Inches(0.24), Inches(0.03), b.GRID)
    d.text(s, reach_label, px+Inches(0.12), Inches(4.78), pw-Inches(0.2), Inches(0.26),
           size=8.5, color=b.MUTED, bold=True)
    d.text(s, reach_val, px+Inches(0.12), Inches(5.06), pw-Inches(0.2), Inches(0.66),
           size=10, color=color if color!=b.CORAL else b.INK, bold=True, shrink=True)
d.rect(s, d.M, Inches(7.02), d.CW, Inches(0.28), b.LIGHT_TEAL, radius=0.03)
d.text(s, "All five platforms post simultaneously. You approve once, the bot distributes everywhere.",
       d.M+Inches(0.2), Inches(7.05), d.CW-Inches(0.3), Inches(0.22),
       size=10.5, color=b.ACCENT, bold=True, shrink=True)
d.footer(s, 7, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — BRAND VOICE + TECHNOLOGY
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Your Voice, Your Brand — Trained On Your Listings",
         "The bot learns how you write. Every description sounds like you, not a template.")
# left: brand voice
LW = Inches(6.0)
d.rect(s, d.M, Inches(1.75), LW, Inches(5.1), b.SOFT, radius=0.05)
d.text(s, "HOW BRAND VOICE TRAINING WORKS", d.M+Inches(0.2), Inches(1.86),
       LW-Inches(0.3), Inches(0.28), size=9.5, color=GOLD, bold=True)
voice_steps = [
    ("Setup (Week 1)",
     "We feed your 5 best past listing descriptions into the training set. The system extracts your vocabulary patterns, sentence length preference, and descriptive style."),
    ("First Listing",
     "Bot generates a draft. You review and mark any phrases you'd change. We update the style model."),
    ("Continuous Calibration",
     "After every listing, you can flag phrases you liked or didn't. The model improves automatically — by listing 5, most agents need zero edits."),
    ("Style Settings",
     "You control: formal vs. conversational, detail-heavy vs. punchy, neighborhood-name mentions, and your standard CTA phrase."),
]
for i, (title, body) in enumerate(voice_steps):
    vy = Inches(2.22) + i*Inches(1.12)
    d.rect(s, d.M+Inches(0.2), vy, Inches(0.06), Inches(0.86), GOLD)
    d.text(s, title, d.M+Inches(0.4), vy+Inches(0.04), LW-Inches(0.6), Inches(0.28),
           size=11, color=b.NAVY, bold=True)
    d.text(s, body, d.M+Inches(0.4), vy+Inches(0.36), LW-Inches(0.6), Inches(0.52),
           size=10, color=b.INK, shrink=True, ls=1.2)
# right: tech stack
RX = d.M + LW + Inches(0.3)
RW = d.CW - LW - Inches(0.3)
d.rect(s, RX, Inches(1.75), RW, Inches(5.1), b.NAVY, radius=0.05, shadow=True)
d.text(s, "THE TECHNOLOGY STACK", RX+Inches(0.2), Inches(1.86),
       RW-Inches(0.3), Inches(0.28), size=9.5, color=GOLD, bold=True)
tech = [
    ("OpenHands AI Runtime", "Reads intake, generates copy, orchestrates posting workflow"),
    ("Google Drive",         "Photo storage and processing pipeline"),
    ("MLS API",              "Direct submission to your local MLS system"),
    ("Zillow Bridge API",    "Zillow listing syndication"),
    ("Realtor.com Feed",     "Realtor.com listing push via RETS/RESO Web API"),
    ("Meta Graph API",       "Facebook Marketplace and Instagram posting"),
    ("Twilio",               "SMS approval notifications to your phone"),
    ("Notion",               "Listing archive and performance log"),
]
for i, (name, role) in enumerate(tech):
    ty = Inches(2.22) + i*Inches(0.5)
    d.rect(s, RX+Inches(0.2), ty+Inches(0.06), Inches(0.1), Inches(0.1), GOLD, radius=0.04)
    d.text(s, name, RX+Inches(0.4), ty, RW-Inches(0.55), Inches(0.24),
           size=10.5, color=b.WHITE, bold=True, shrink=True)
    d.text(s, role, RX+Inches(0.4), ty+Inches(0.24), RW-Inches(0.55), Inches(0.24),
           size=9, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 8, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — ROI MATH
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The ROI Math — Time Recovered + Revenue Protected",
         "Two separate returns: your time back and your commission protected")
# time table
d.rect(s, d.M, Inches(1.75), Inches(6.0), Inches(0.38), b.NAVY)
d.text(s, "TIME RECOVERY", d.M+Inches(0.2), Inches(1.8), Inches(5.6), Inches(0.3),
       size=10, color=GOLD, bold=True)
time_rows = [
    ("Task",                      "Today (Manual)",      "With Listing Assistant", True),
    ("Write MLS description",     "45–60 min",           "10 min (approve draft)", False),
    ("Format platform variants",  "30–45 min",           "0 min (automated)",      False),
    ("Upload photos per platform","20–30 min",           "0 min (automated)",      False),
    ("Post to secondary sites",   "20–30 min",           "0 min (automated)",      False),
    ("Total per listing",         "95–135 min",          "10 min",                 False),
    ("Monthly at 6 listings",     "570–810 min (10–14h)","60 min (1h)",            False),
]
cw3t = [Inches(3.6), Inches(2.95), Inches(3.15)]
cx3t = [d.M, d.M+Inches(3.7), d.M+Inches(6.76)]
rh = Inches(0.44)
for ri, row in enumerate(time_rows):
    for ci, cell in enumerate(row[:3]):
        ry = Inches(2.14) + ri*rh
        is_hdr = ri == 0
        is_new = ci == 2 and not is_hdr
        bg = b.NAVY if is_hdr else (b.LIGHT_TEAL if is_new else (b.WHITE if ri%2==0 else b.SOFT))
        d.rect(s, cx3t[ci], ry, cw3t[ci]-Inches(0.06), rh-Inches(0.03), bg)
        tc = b.WHITE if is_hdr else (b.ACCENT if is_new else b.INK)
        d.text(s, cell, cx3t[ci]+Inches(0.1), ry+Inches(0.08),
               cw3t[ci]-Inches(0.18), rh-Inches(0.1), size=10 if not is_hdr else 9.5,
               color=tc, bold=(is_hdr or is_new), shrink=True)
# revenue table
d.rect(s, d.M, Inches(5.24), Inches(6.0), Inches(0.38), b.NAVY)
d.text(s, "REVENUE PROTECTION", d.M+Inches(0.2), Inches(5.29), Inches(5.6), Inches(0.3),
       size=10, color=GOLD, bold=True)
rev_rows = [
    ("Listings delayed 3+ days:",    "est. 30% of your volume"),
    ("Price discount (research avg):", "1–1.5% below market"),
    ("At $300K avg price:",           "= $3,000–$4,500 per delayed listing"),
    ("At 6 listings/month × 30%:",    "~2 delayed listings × $3,750 avg = $7,500/month at risk"),
    ("Annual exposure:",              "$90,000 in commission at risk from slow time-to-market"),
]
for i, (label, val) in enumerate(rev_rows):
    ly = Inches(5.7) + i*Inches(0.24)
    d.text(s, label, d.M+Inches(0.15), ly, Inches(4.2), Inches(0.22),
           size=10, color=b.MUTED, bold=True)
    d.text(s, val, d.M+Inches(4.4), ly, Inches(5.6), Inches(0.22),
           size=10, color=b.INK, shrink=True)
d.rect(s, d.M+Inches(6.3), Inches(1.75), d.CW-Inches(6.3), Inches(5.12), b.NAVY, radius=0.05, shadow=True)
d.text(s, "Bottom line", d.M+Inches(6.55), Inches(1.92), d.CW-Inches(6.55), Inches(0.38),
       size=13, color=GOLD, bold=True)
summary = [
    ("Annual time cost saved:", "120+ hours = $24,000+"),
    ("Revenue protected:", "up to $90,000/year"),
    ("System cost:", "$24,000/year ($2,000/mo)"),
    ("Net annual return:", "$90,000+ protected"),
]
for i, (label, val) in enumerate(summary):
    sy = Inches(2.42) + i*Inches(0.74)
    d.text(s, label, d.M+Inches(6.55), sy, d.CW-Inches(6.75), Inches(0.28),
           size=9.5, color=b.LIGHT_TEAL)
    d.text(s, val, d.M+Inches(6.55), sy+Inches(0.3), d.CW-Inches(6.75), Inches(0.38),
           size=14, color=GOLD, bold=True, shrink=True)
d.footer(s, 9, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — WHAT'S INCLUDED
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "What's Included — Everything, No Add-Ons",
         "One flat monthly fee. Every feature. No per-listing charges.")
included = [
    ("MLS Description Generator", "Compliant copy for your local MLS. Trained on top-performing listings. One round of edits per listing included."),
    ("Five-Platform Copy Variants", "Separate optimized copy for MLS, Zillow, Realtor.com, Facebook Marketplace, and Instagram — every listing, automatically."),
    ("Photo Processing Pipeline", "Upload in any format. Bot sorts, resizes, and formats photos for each platform's display specifications."),
    ("Brand Voice Profile", "Your writing style captured in setup. Updated automatically as you approve or edit drafts. Sounds like you by listing 5."),
    ("Approval Workflow", "Every listing goes to a preview link first. You approve in one click (or request one round of edits). Nothing goes live without your sign-off."),
    ("Scheduled Publishing", "Set a go-live time or post immediately. Bot handles all simultaneous platform submissions — no manual uploads."),
    ("Performance Dashboard", "Weekly views, saves, and inquiry count per listing. Monthly report showing which listings performed best and why."),
    ("Monthly Support Call", "30-minute check-in to review performance, update brand voice, and handle any edge cases from your market."),
]
iw = (d.CW - Inches(0.2)) / 2
for i, (title, body) in enumerate(included):
    row, col = divmod(i, 2)
    ix = d.M + col*(iw+Inches(0.2))
    iy = Inches(1.75) + row*Inches(1.24)
    d.rect(s, ix, iy, iw, Inches(1.14), b.WHITE, radius=0.04, shadow=True)
    d.rect(s, ix, iy, Inches(0.07), Inches(1.14), GOLD)
    d.text(s, f"✓  {title}", ix+Inches(0.18), iy+Inches(0.1),
           iw-Inches(0.28), Inches(0.34), size=11.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, ix+Inches(0.18), iy+Inches(0.48),
           iw-Inches(0.28), Inches(0.6), size=10, color=b.INK, shrink=True, ls=1.15)
d.footer(s, 10, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — SETUP TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Setup Timeline — Live in Four Weeks",
         "Your first fully automated listing posts before the end of month one.")
tl = [
    ("Week 1", "Connect + Configure",
     ["Connect MLS credentials and platform accounts (MLS, Zillow, Realtor.com, Facebook, Instagram)",
      "Upload 5 past listing descriptions for brand voice training",
      "Set up approval workflow and SMS notifications to your phone"]),
    ("Week 2", "Brand Voice + Test",
     ["System generates sample descriptions from your past listings",
      "You review and flag any phrases to adjust",
      "Test post to a staging environment — verify all platform formats"]),
    ("Week 3", "First Live Listing",
     ["Your first real listing runs through the full pipeline",
      "We monitor the submission and handle any platform-specific issues",
      "You approve the preview and watch it go live on all 5 platforms"]),
    ("Week 4", "Hand Off + Optimize",
     ["You run the second listing independently",
      "30-minute debrief: brand voice adjustments, any platform quirks",
      "System running autonomously — you submit intake, approve, done"]),
]
for i, (week, title, items) in enumerate(tl):
    wy = Inches(1.92) + i*Inches(1.28)
    d.rect(s, d.M, wy, Inches(1.05), Inches(1.08), GOLD, radius=0.04)
    d.text(s, week, d.M, wy+Inches(0.16), Inches(1.05), Inches(0.38),
           size=11, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.rect(s, d.M+Inches(1.15), wy, d.CW-Inches(1.15), Inches(1.08), b.SOFT, radius=0.04)
    d.text(s, title, d.M+Inches(1.35), wy+Inches(0.06), Inches(4.5), Inches(0.32),
           size=12, color=b.NAVY, bold=True, shrink=True)
    for j, item in enumerate(items):
        d.rect(s, d.M+Inches(1.35), wy+Inches(0.44)+j*Inches(0.22),
               Inches(0.1), Inches(0.1), GOLD, radius=0.04)
        d.text(s, item, d.M+Inches(1.55), wy+Inches(0.4)+j*Inches(0.22),
               d.CW-Inches(1.75), Inches(0.22), size=10, color=b.INK, shrink=True)
d.rect(s, d.M, Inches(7.09), d.CW, Inches(0.24), b.LIGHT_TEAL, radius=0.03)
d.text(s, "Setup fee: $500 one-time (covers weeks 1–4 configuration, brand voice training, and platform connections)",
       d.M+Inches(0.2), Inches(7.11), d.CW-Inches(0.3), Inches(0.2),
       size=9.5, color=b.ACCENT, shrink=True)
d.footer(s, 11, TOTAL)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — PRICING + CTA
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.12), GOLD)
d.rect(s, 0, d.H-Inches(0.12), d.W, Inches(0.12), GOLD)
d.text(s, "SIMPLE PRICING. EVERY FEATURE INCLUDED.", d.M, Inches(0.72),
       Inches(10), Inches(0.38), size=12, color=GOLD, bold=True)
d.rect(s, d.M, Inches(1.2), Inches(5.5), Inches(2.4), b.NAVY_2, radius=0.08, shadow=True)
d.text(s, "$2,000", d.M+Inches(0.3), Inches(1.4), Inches(4.2), Inches(1.1),
       size=72, color=GOLD, bold=True, shrink=True)
d.text(s, "/ month", d.M+Inches(0.3), Inches(2.42), Inches(3.0), Inches(0.38),
       size=18, color=b.LIGHT_TEAL)
d.text(s, "+ $500 one-time setup · No long-term contract · Cancel with 30 days notice",
       d.M+Inches(0.3), Inches(2.9), Inches(5.0), Inches(0.44),
       size=10.5, color=b.MUTED, shrink=True)
d.text(s, "For $2,000/month you get:", d.M+Inches(6.1), Inches(1.2),
       Inches(6.5), Inches(0.38), size=12, color=GOLD, bold=True)
gets = ["MLS + 4 platform posting — every listing",
        "Brand voice training (sounds like you)",
        "Photo processing and formatting",
        "Approval workflow before anything goes live",
        "Performance tracking dashboard",
        "Cancel anytime — no lock-in"]
for i, g in enumerate(gets):
    d.rect(s, d.M+Inches(6.1), Inches(1.66)+i*Inches(0.5), Inches(0.14), Inches(0.14), GOLD, radius=0.04)
    d.text(s, g, d.M+Inches(6.38), Inches(1.62)+i*Inches(0.5), Inches(6.4), Inches(0.44),
           size=11.5, color=b.WHITE, shrink=True)
d.rect(s, d.M, Inches(3.8), d.CW, Inches(0.06), b.NAVY_2)
d.text(s, "THREE STEPS TO GET STARTED", d.M, Inches(3.96),
       Inches(8), Inches(0.32), size=11, color=GOLD, bold=True)
steps3 = [
    ("1", "20-min intro call", "We confirm your MLS setup, platforms, and current listing volume."),
    ("2", "Sign + pay setup fee", "Configuration starts within 48 hours."),
    ("3", "First listing live", "Week 3 — your first listing posts to all 5 platforms automatically."),
]
for i, (n, title, body) in enumerate(steps3):
    sx = d.M + i*Inches(4.2)
    d.rect(s, sx, Inches(4.38), Inches(0.44), Inches(0.44), GOLD, radius=0.08)
    d.text(s, n, sx, Inches(4.4), Inches(0.44), Inches(0.4),
           size=16, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, title, sx+Inches(0.6), Inches(4.4), Inches(3.4), Inches(0.36),
           size=12, color=b.WHITE, bold=True, shrink=True)
    d.text(s, body, sx+Inches(0.6), Inches(4.82), Inches(3.4), Inches(0.52),
           size=10, color=b.LIGHT_TEAL, shrink=True, ls=1.2)
d.text(s, "[your website or booking link here]",
       d.M, Inches(5.72), d.CW, Inches(0.38), size=14, color=GOLD, bold=True)
d.footer(s, 12, TOTAL, dark=True)

d.save(OUT_PATH)
print(f"Deck 2 saved: {OUT_PATH} ({d.n} slides)")
