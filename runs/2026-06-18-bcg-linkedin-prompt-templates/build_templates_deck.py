#!/usr/bin/env python3
"""
build_templates_deck.py
Converts bcg-linkedin-prompt-templates.md → one branded PPTX deck.

Each skill gets TWO slides:
  A) Prompt Template card  — hook, command, Claude-returns bullets, hashtags
  B) LinkedIn Post preview — the actual post copy to publish

Plus a cover and OS-chain summary slide.
"""

import re, sys
from pathlib import Path
from datetime import date

PPTXKIT = Path.home() / ".claude/skills/branded-pptx-deck/scripts"
sys.path.insert(0, str(PPTXKIT))
from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor

# ── BCG brand ─────────────────────────────────────────────────────────────────
B = Brand(
    NAVY=RGBColor(0x00, 0x18, 0x24),
    NAVY_2=RGBColor(0x00, 0x26, 0x34),
    TEAL=RGBColor(0x00, 0x99, 0x6B),
    ACCENT=RGBColor(0x00, 0x77, 0x55),
    DARK_TEAL=RGBColor(0x00, 0x66, 0x44),
    LIGHT_TEAL=RGBColor(0xCC, 0xEE, 0xE4),
    GOLD=RGBColor(0xFF, 0xB8, 0x00),
    AMBER=RGBColor(0xF2, 0xA8, 0x3B),
    CORAL=RGBColor(0xE0, 0x5A, 0x6B),
    WHITE=RGBColor(0xFF, 0xFF, 0xFF),
    SOFT=RGBColor(0xF4, 0xF7, 0xF8),
    INK=RGBColor(0x1B, 0x2B, 0x3C),
    MUTED=RGBColor(0x5B, 0x6B, 0x7C),
)

DOMAIN_COLORS = {
    "01": RGBColor(0x00, 0x77, 0x55),   # Diagnosis — teal
    "02": RGBColor(0x00, 0x77, 0x55),
    "03": RGBColor(0x00, 0x77, 0x55),
    "04": RGBColor(0x00, 0x55, 0x99),   # Market — blue
    "05": RGBColor(0x00, 0x55, 0x99),
    "06": RGBColor(0x00, 0x55, 0x99),
    "07": RGBColor(0x00, 0x55, 0x99),
    "08": RGBColor(0x77, 0x44, 0x00),   # Strategic — amber
    "09": RGBColor(0x77, 0x44, 0x00),
    "10": RGBColor(0x77, 0x44, 0x00),
    "11": RGBColor(0x77, 0x44, 0x00),
    "12": RGBColor(0x55, 0x00, 0x88),   # Execution — purple
    "13": RGBColor(0x55, 0x00, 0x88),
    "14": RGBColor(0x55, 0x00, 0x88),
    "15": RGBColor(0x99, 0x22, 0x00),   # Risk — red
    "16": RGBColor(0x99, 0x22, 0x00),
    "17": RGBColor(0x99, 0x22, 0x00),
    "18": RGBColor(0x99, 0x22, 0x00),
    "19": RGBColor(0x00, 0x44, 0x66),   # Comms — navy-blue
    "20": RGBColor(0x00, 0x44, 0x66),
    "21": RGBColor(0x00, 0x44, 0x66),
}

DOMAIN_LABELS = {
    "01": "01 / DIAGNOSIS & FRAMING",
    "02": "01 / DIAGNOSIS & FRAMING",
    "03": "01 / DIAGNOSIS & FRAMING",
    "04": "02 / MARKET INTELLIGENCE",
    "05": "02 / MARKET INTELLIGENCE",
    "06": "02 / MARKET INTELLIGENCE",
    "07": "02 / MARKET INTELLIGENCE",
    "08": "03 / STRATEGIC CHOICE",
    "09": "03 / STRATEGIC CHOICE",
    "10": "03 / STRATEGIC CHOICE",
    "11": "03 / STRATEGIC CHOICE",
    "12": "04 / EXECUTION",
    "13": "04 / EXECUTION",
    "14": "04 / EXECUTION",
    "15": "05 / RISK & GOVERNANCE",
    "16": "05 / RISK & GOVERNANCE",
    "17": "05 / RISK & GOVERNANCE",
    "18": "05 / RISK & GOVERNANCE",
    "19": "06 / EXECUTIVE COMMS",
    "20": "06 / EXECUTIVE COMMS",
    "21": "06 / EXECUTIVE COMMS",
}


# ── Parser ────────────────────────────────────────────────────────────────────

def parse_templates(md_path: Path) -> list[dict]:
    text = md_path.read_text()
    blocks = re.split(r'\n## (\d{2} — .+?)\n', text)
    skills = []
    for i in range(1, len(blocks), 2):
        heading = blocks[i].strip()
        body = blocks[i + 1]

        # linkedin post body (strip markdown fences and headers)
        post_match = re.search(r'### LinkedIn Post\n(.*?)### Claude Prompt', body, re.S)
        prompt_match = re.search(r'### Claude Prompt.*?```\n(.*?)```', body, re.S)

        post_raw = post_match.group(1).strip() if post_match else ""
        prompt_raw = prompt_match.group(1).strip() if prompt_match else ""

        # clean post text of bold markers
        post_clean = re.sub(r'\*\*(.+?)\*\*', r'\1', post_raw)

        # hook = first line with ** **
        hook_match = re.search(r'\*\*(.+?)\*\*', post_raw)
        hook = hook_match.group(1) if hook_match else heading

        # slash command
        cmd_match = re.search(r'(/[\w-]+)', prompt_raw)
        cmd = cmd_match.group(1) if cmd_match else ""

        # "Claude returns:" bullets
        returns_match = re.search(r'Claude returns:\n(→.*?)(?:\n\n|The quality|What\'s|\Z)', post_raw, re.S)
        returns_lines = []
        if returns_match:
            for line in returns_match.group(1).splitlines():
                line = line.strip()
                if line.startswith("→"):
                    returns_lines.append(line[1:].strip())

        # consulting insight lines (the "body" paragraphs between hook and prompt)
        lines = [l.strip() for l in post_clean.splitlines() if l.strip()]
        body_lines = []
        for l in lines:
            if l.startswith("#"):
                break
            if l.startswith("/"):
                break
            if "Claude returns:" in l:
                break
            body_lines.append(l)
        # keep first 4 non-hook body lines
        insight_lines = [l for l in body_lines[1:] if l and not l.startswith("```")][:4]

        # hashtags
        tags_match = re.search(r'(#\w[\w].*)', post_raw)
        tags = tags_match.group(1) if tags_match else ""

        num = heading.split(" — ")[0].strip()
        skills.append({
            "num": num,
            "heading": heading,
            "hook": hook,
            "cmd": cmd,
            "prompt": prompt_raw,
            "returns": returns_lines,
            "insight": insight_lines,
            "tags": tags,
            "post_clean": post_clean,
        })
    return skills


# ── Slide builders ────────────────────────────────────────────────────────────

def slide_cover(d: Deck, total_content_slides: int):
    b = d.b
    s = d.slide(fill=b.NAVY)

    # left green spine
    d.rect(s, 0, 0, Inches(0.25), d.H, b.TEAL)

    # BCG × Claude chip
    d.rect(s, Inches(0.5), Inches(0.32), Inches(2.4), Inches(0.42), b.TEAL, radius=0.05)
    d.text(s, "BCG × CLAUDE CODE", Inches(0.52), Inches(0.34), Inches(2.36), Inches(0.38),
           size=11, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    d.text(s, "THE CONSULTANT'S GUIDE TO CLAUDE",
           Inches(0.5), Inches(0.96), d.CW, Inches(0.5),
           size=14, color=b.TEAL, bold=True)

    d.text(s, "21 BCG-Style\nPrompt Templates",
           Inches(0.5), Inches(1.55), Inches(11), Inches(2.4),
           size=52, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)

    d.rect(s, Inches(0.5), Inches(4.15), Inches(3.5), Inches(0.07), b.GOLD)

    d.text(s, "Push Claude Opus to its limits and turn it into an MBB-grade consulting engine.",
           Inches(0.5), Inches(4.4), Inches(10), Inches(0.5),
           size=15, color=b.LIGHT_TEAL)

    # 6 domain chips in a row
    domains = [
        ("01 Diagnose", B.TEAL),
        ("02 Map", RGBColor(0x00, 0x55, 0x99)),
        ("03 Choose", RGBColor(0x77, 0x44, 0x00)),
        ("04 Execute", RGBColor(0x55, 0x00, 0x88)),
        ("05 Govern", RGBColor(0x99, 0x22, 0x00)),
        ("06 Communicate", RGBColor(0x00, 0x44, 0x66)),
    ]
    chip_w = Inches(1.9)
    gap = Inches(0.15)
    x0 = Inches(0.5)
    for label, col in domains:
        d.rect(s, x0, Inches(5.1), chip_w, Inches(0.42), col, radius=0.06)
        d.text(s, label, x0 + Inches(0.05), Inches(5.12),
               chip_w - Inches(0.1), Inches(0.38),
               size=10.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        x0 += chip_w + gap

    d.text(s, f"21 skills · {total_content_slides} slides · {date.today()}",
           Inches(0.5), Inches(6.8), Inches(10), Inches(0.38),
           size=10, color=b.MUTED)

    d.text(s, "Anthropic × BCG · skills repo: /strategy-consulting/",
           Inches(0.5), Inches(7.1), Inches(10), Inches(0.3),
           size=9, color=b.MUTED)


def slide_prompt_template(d: Deck, skill: dict, page: int, total: int):
    """Full-slide prompt template card: hook + insight + command + what-you-get."""
    b = d.b
    num = skill["num"]
    accent = DOMAIN_COLORS.get(num, b.TEAL)
    domain = DOMAIN_LABELS.get(num, "")

    s = d.slide(fill=b.NAVY)

    # left accent spine (domain color)
    d.rect(s, 0, 0, Inches(0.28), d.H, accent)

    # domain label
    d.text(s, domain, Inches(0.45), Inches(0.28), Inches(6), Inches(0.36),
           size=11, color=accent, bold=True)

    # skill number badge
    d.rect(s, d.W - Inches(1.5) - d.M, Inches(0.22), Inches(1.5), Inches(0.44),
           accent, radius=0.06)
    d.text(s, f"SKILL {num}", d.W - Inches(1.5) - d.M + Inches(0.05), Inches(0.24),
           Inches(1.4), Inches(0.4),
           size=12, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)

    # hook — large white headline (left half only, right panel overlaps)
    hook = skill["hook"]
    d.text(s, hook, Inches(0.45), Inches(0.78), Inches(6.9), Inches(1.4),
           size=28, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)

    # gold rule
    d.rect(s, Inches(0.45), Inches(2.28), Inches(2.8), Inches(0.06), b.GOLD)

    # insight lines (left half)
    y_insight = Inches(2.5)
    for line in skill["insight"][:3]:
        if not line:
            continue
        d.text(s, line, Inches(0.45), y_insight, Inches(6.9), Inches(0.48),
               size=13.5, color=b.LIGHT_TEAL, shrink=True)
        y_insight += Inches(0.48)

    # ── right panel: command box ──────────────────────────────────────────────
    panel_x = Inches(7.8)
    panel_w = Inches(5.1)
    panel_y = Inches(0.78)
    panel_h = Inches(5.8)

    d.rect(s, panel_x, panel_y, panel_w, panel_h,
           RGBColor(0x00, 0x26, 0x34), radius=0.04)

    # "THE PROMPT" label
    d.text(s, "THE PROMPT", panel_x + Inches(0.18), panel_y + Inches(0.16),
           panel_w - Inches(0.3), Inches(0.32),
           size=10, color=accent, bold=True)

    # command in gold monospace style
    cmd = skill["cmd"]
    d.rect(s, panel_x + Inches(0.15), panel_y + Inches(0.55),
           panel_w - Inches(0.3), Inches(0.44),
           RGBColor(0x00, 0x12, 0x1A), radius=0.03)
    d.text(s, cmd, panel_x + Inches(0.22), panel_y + Inches(0.57),
           panel_w - Inches(0.44), Inches(0.4),
           size=15, color=b.GOLD, bold=True)

    # prompt body
    prompt_lines = skill["prompt"].splitlines()[:7]
    y_p = panel_y + Inches(1.12)
    for pl in prompt_lines:
        pl = pl.strip()
        if not pl:
            y_p += Inches(0.12)
            continue
        d.text(s, pl, panel_x + Inches(0.18), y_p,
               panel_w - Inches(0.3), Inches(0.36),
               size=10.5, color=b.LIGHT_TEAL, shrink=True)
        y_p += Inches(0.38)
        if y_p > panel_y + panel_h - Inches(0.2):
            break

    # ── left bottom: Claude returns ───────────────────────────────────────────
    returns_y = max(y_insight + Inches(0.25), Inches(3.8))
    d.text(s, "Claude returns:", Inches(0.45), returns_y,
           Inches(7.0), Inches(0.36),
           size=12, color=b.TEAL, bold=True)
    returns_y += Inches(0.38)

    for item in skill["returns"][:5]:
        if returns_y > Inches(6.4):
            break
        # arrow chip
        d.rect(s, Inches(0.45), returns_y + Inches(0.06),
               Inches(0.26), Inches(0.26), accent, radius=0.05)
        d.text(s, "→", Inches(0.45), returns_y + Inches(0.04),
               Inches(0.26), Inches(0.3),
               size=11, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, item, Inches(0.82), returns_y,
               Inches(6.7), Inches(0.46),
               size=11.5, color=b.WHITE, shrink=True)
        returns_y += Inches(0.52)

    # footer
    d.footer(s, page, total, dark=True)


def slide_linkedin_post(d: Deck, skill: dict, page: int, total: int):
    """Light slide: the actual LinkedIn post copy ready to publish."""
    b = d.b
    num = skill["num"]
    accent = DOMAIN_COLORS.get(num, b.TEAL)

    s = d.slide(fill=b.SOFT)

    # top band
    d.rect(s, 0, 0, d.W, Inches(0.16), accent)

    # "LINKEDIN POST — COPY & PUBLISH" header
    d.text(s, "LINKEDIN POST — COPY & PUBLISH",
           d.M, Inches(0.28), Inches(7), Inches(0.36),
           size=11, color=accent, bold=True)

    # skill name chip
    chip_w = Inches(3.5)
    d.rect(s, d.W - chip_w - d.M, Inches(0.22), chip_w, Inches(0.4),
           b.NAVY, radius=0.04)
    label = skill["heading"].split(" — ", 1)[-1] if " — " in skill["heading"] else skill["heading"]
    # truncate long labels
    if len(label) > 34:
        label = label[:32] + "…"
    d.text(s, label, d.W - chip_w - d.M + Inches(0.08), Inches(0.24),
           chip_w - Inches(0.16), Inches(0.36),
           size=10, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    # hook as big black headline
    d.text(s, skill["hook"],
           d.M, Inches(0.76), d.CW, Inches(0.9),
           size=22, color=b.NAVY, bold=True, font=b.FONT_H, shrink=True)

    d.rect(s, d.M, Inches(1.74), Inches(2.0), Inches(0.05), accent)

    # post body — left column
    col_w = Inches(5.5)
    post_lines = [l for l in skill["post_clean"].splitlines() if l.strip()]
    # skip the hook line (first line)
    post_lines = post_lines[1:]
    # strip markdown artifacts before rendering
    clean_post_lines = []
    hit_returns = False
    for ln in post_lines:
        ln = ln.strip()
        if not ln:
            clean_post_lines.append("")
            continue
        if ln.startswith("```"):              # fence markers
            continue
        if ln.lower().startswith("the prompt:"):
            continue
        if ln.startswith("/"):               # slash commands
            continue
        if ln.startswith("["):               # prompt fill-in fields
            continue
        if "claude returns:" in ln.lower():
            hit_returns = True
        if hit_returns:
            continue                         # shown on prompt-template slide
        clean_post_lines.append(ln)

    y = Inches(1.9)
    for line in clean_post_lines[:16]:
        if y > Inches(6.62):
            break
        line = line.strip()
        if not line:
            y += Inches(0.12)
            continue
        if line.startswith("#"):
            d.text(s, line, d.M, y, col_w, Inches(0.3),
                   size=9.5, color=accent, shrink=True)
            y += Inches(0.32)
            continue
        if line.startswith("→"):
            d.text(s, line, d.M + Inches(0.1), y, col_w - Inches(0.1),
                   Inches(0.42), size=10.5, color=b.INK, shrink=True)
            y += Inches(0.44)
            continue
        h = Inches(0.44) if len(line) > 60 else Inches(0.32)
        d.text(s, line, d.M, y, col_w, h, size=11, color=b.INK, shrink=True)
        y += h + Inches(0.04)

    # right column: command box
    rx = Inches(6.8)
    rw = Inches(6.1)
    d.rect(s, rx, Inches(1.76), rw, Inches(4.96), b.NAVY, radius=0.04)

    d.text(s, "COPY THIS PROMPT INTO CLAUDE CODE", rx + Inches(0.2), Inches(1.92),
           rw - Inches(0.35), Inches(0.34),
           size=10, color=accent, bold=True)

    # command
    d.rect(s, rx + Inches(0.18), Inches(2.34), rw - Inches(0.36), Inches(0.46),
           RGBColor(0x00, 0x0C, 0x14), radius=0.03)
    d.text(s, skill["cmd"],
           rx + Inches(0.26), Inches(2.36), rw - Inches(0.52), Inches(0.42),
           size=16, color=b.GOLD, bold=True)

    # prompt fields
    prompt_lines = skill["prompt"].splitlines()
    py = Inches(2.94)
    for pl in prompt_lines[:11]:
        pl = pl.strip()
        if not pl:
            py += Inches(0.1)
            continue
        color = b.GOLD if pl.startswith("/") else b.LIGHT_TEAL
        d.text(s, pl, rx + Inches(0.2), py, rw - Inches(0.35),
               Inches(0.36), size=11, color=color, shrink=True)
        py += Inches(0.37)
        if py > Inches(6.55):
            break

    d.footer(s, page, total)


def slide_os_chain(d: Deck, page: int, total: int):
    """Final slide: the full 6-phase OS chain."""
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.28), d.H, b.TEAL)

    d.text(s, "THE CONSULTING OPERATING SYSTEM",
           Inches(0.45), Inches(0.28), Inches(11), Inches(0.4),
           size=12, color=b.TEAL, bold=True)

    d.text(s, "21 Skills · One Chain · Any Engagement",
           Inches(0.45), Inches(0.78), Inches(10), Inches(0.7),
           size=30, color=b.WHITE, bold=True, font=b.FONT_H)

    d.rect(s, Inches(0.45), Inches(1.58), Inches(3.0), Inches(0.07), b.GOLD)

    phases = [
        ("01", "DIAGNOSE",   "Situation Assessment\nGrowth Barriers\nAssumption Audit",      B.TEAL),
        ("02", "MAP",        "Market Mapping\nCompetitive Intel\nCustomer Segmentation\nProfit Pools", RGBColor(0x00, 0x55, 0x99)),
        ("03", "CHOOSE",     "Strategic Options\nPricing Strategy\nBusiness Case\nPortfolio Review",   RGBColor(0x77, 0x44, 0x00)),
        ("04", "EXECUTE",    "Operating Model\nInitiative Prioritization\nTransformation Roadmap",     RGBColor(0x55, 0x00, 0x88)),
        ("05", "GOVERN",     "Risk & Mitigation\nWar Gaming\nKPI Architecture\nValue Realization",     RGBColor(0x99, 0x22, 0x00)),
        ("06", "COMMUNICATE","Stakeholder Alignment\nNarrative Builder\nDecision Memo",               RGBColor(0x00, 0x44, 0x66)),
    ]

    card_w = Inches(1.97)
    card_h = Inches(4.6)
    gap = Inches(0.09)
    x0 = Inches(0.45)

    for num, phase, skills_text, col in phases:
        # card background
        d.rect(s, x0, Inches(1.8), card_w, card_h, RGBColor(0x00, 0x26, 0x34), radius=0.04)
        # color header
        d.rect(s, x0, Inches(1.8), card_w, Inches(0.56), col, radius=0.04)
        # num + phase label
        d.text(s, num, x0 + Inches(0.1), Inches(1.84), Inches(0.4), Inches(0.48),
               size=18, color=b.WHITE, bold=True)
        d.text(s, phase, x0 + Inches(0.52), Inches(1.9), card_w - Inches(0.62), Inches(0.36),
               size=13, color=b.WHITE, bold=True, shrink=True)

        # skills list
        sy = Inches(2.5)
        for skill_name in skills_text.strip().splitlines():
            d.text(s, "· " + skill_name.strip(), x0 + Inches(0.12), sy,
                   card_w - Inches(0.2), Inches(0.36),
                   size=10.5, color=b.LIGHT_TEAL, shrink=True)
            sy += Inches(0.38)

        x0 += card_w + gap

    d.text(s, "Run /strategy-consulting to enter the full chain from any Claude Code session",
           Inches(0.45), Inches(6.78), Inches(12), Inches(0.38),
           size=10.5, color=b.MUTED)

    d.footer(s, page, total, dark=True)


# ── Main ──────────────────────────────────────────────────────────────────────

def build(md_path: Path, out_path: Path):
    skills = parse_templates(md_path)
    print(f"Parsed {len(skills)} skills from {md_path.name}")

    # total slides: 1 cover + 2 per skill + 1 OS chain
    total = 1 + len(skills) * 2 + 1

    d = Deck(brand=B, footer=f"The Consultant's Guide to Claude · BCG-Style Prompt Templates · {date.today()}")

    # Cover
    slide_cover(d, total)

    # Per-skill pair
    for i, skill in enumerate(skills):
        page_a = 2 + i * 2
        page_b = page_a + 1
        slide_prompt_template(d, skill, page_a, total)
        slide_linkedin_post(d, skill, page_b, total)
        print(f"  {skill['num']} {skill['cmd']:30s}  slides {page_a}–{page_b}")

    # OS Chain summary
    slide_os_chain(d, total, total)

    d.save(out_path)
    print(f"\n✓ Saved: {out_path}  ({d.n} slides)")
    return out_path


if __name__ == "__main__":
    here = Path(__file__).parent
    md = here / "bcg-linkedin-prompt-templates.md"
    out = here / "BCG-Consultant-Guide-to-Claude-Prompt-Templates.pptx"
    build(md, out)
