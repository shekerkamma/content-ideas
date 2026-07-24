#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path("/home/shekerk/content-ideas")
RUN = ROOT / "runs/2026-07-02-video-to-deck-rerun"
sys.path.insert(0, str(ROOT / "skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, Inches, PP_ALIGN, RGBColor

OUT = RUN / "ai-agents-new-saas-video-deck-v3-excalidraw-draft.pptx"

SLIDES = [
    ("Thesis", "AI Agents Are The New SaaS", "v3-thesis-workflow"),
    ("Market Context", "SaaS Packaged Workflows; Agents Execute Them", "v3-market-context"),
    ("Economic Wedge", "Unit Economics Make The Wedge Obvious", "v3-unit-economics"),
    ("Search Discipline", "Pick A Workflow With A Paycheck Attached", "v3-workflow-scorecard"),
    ("Wedge Examples", "Founder-Sized Wedges Start In Urgent Service Work", "v3-wedge-examples"),
    ("Operating Method", "Shadow The Human Before You Build", "v3-shadow-human"),
    ("Build Scope", "Build The Smallest Useful Agent", "v3-smallest-agent"),
    ("Workflow Architecture", "Agentic Workflows Need A Control Pattern", "v3-agentic-workflows"),
    ("Trust Wrapper", "The Wrapper Makes It SaaS", "v3-wrapper-saas"),
    ("Commercialization", "Sell The Pilot Like Labor, Then Productize", "v3-pilot-productize"),
    ("Defensibility", "Own The Workflow", "v3-own-workflow"),
    ("Coverage", "Every Meaningful Visual Beat Is Accounted For", "v3-coverage-map"),
]


def hx(s):
    s = s.strip("#")
    return RGBColor(int(s[:2], 16), int(s[2:4], 16), int(s[4:], 16))


def header(d, s, kicker, title):
    d.text(s, kicker.upper(), d.M, Inches(0.27), Inches(4.2), Inches(0.20),
           size=9.4, color=d.b.DARK_TEAL, bold=True, shrink=True)
    d.text(s, title, d.M, Inches(0.55), Inches(10.6), Inches(0.42),
           size=21.5, color=d.b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.05), Inches(1.1), Inches(0.045), d.b.TEAL)


def add_excalidraw_board(d, s, slug):
    img = RUN / f"ai-agents-new-saas-{slug}.png"
    if not img.exists():
        raise FileNotFoundError(img)
    d.picture_centered(s, img, top=Inches(1.26), width=Inches(11.35), max_bottom=Inches(6.58))
    return img


def source_note(d, s, slug, page, total):
    d.text(s, f"Excalidraw source: ai-agents-new-saas-{slug}.excalidraw",
           d.M, Inches(6.86), Inches(8.8), Inches(0.20), size=7.6, color=d.b.MUTED, shrink=True)
    d.text(s, f"{page} / {total}", d.W - Inches(1.25), Inches(6.86), Inches(0.75), Inches(0.20),
           size=9.5, color=d.b.MUTED, bold=True, align=PP_ALIGN.RIGHT)


def build():
    d = Deck(footer="")
    total = len(SLIDES) + 1

    s = d.slide(fill=d.b.NAVY)
    d.text(s, "VIDEO-TO-DECK V3", d.M, Inches(0.75), Inches(4.5), Inches(0.26),
           size=11, color=d.b.TEAL, bold=True)
    d.text(s, "AI Agents Are The New SaaS", d.M, Inches(1.25), Inches(8.8), Inches(0.78),
           size=36, color=d.b.WHITE, bold=True, shrink=True)
    d.text(s, "Excalidraw-first deck rebuilt from dense hyperframes and transcript storyline.",
           d.M, Inches(2.20), Inches(6.8), Inches(0.45), size=15, color=hx("DCE6EF"), shrink=True)
    d.rect(s, d.M, Inches(3.30), Inches(5.4), Inches(1.15), hx("12243A"), radius=0.07)
    d.text(s, "Delivery rule", d.M + Inches(0.22), Inches(3.52), Inches(4.9), Inches(0.20),
           size=12.5, color=d.b.TEAL, bold=True)
    d.text(s, "Every main content slide uses an Excalidraw-rendered visual. The editable .excalidraw sources are saved beside the PPTX.",
           d.M + Inches(0.22), Inches(3.88), Inches(4.9), Inches(0.34), size=10.8, color=d.b.WHITE, shrink=True)
    add_excalidraw_board(d, s, "v3-thesis-workflow")
    d.text(s, f"1 / {total}", d.W - Inches(1.25), Inches(6.86), Inches(0.75), Inches(0.20),
           size=9.5, color=hx("AAB6C4"), bold=True, align=PP_ALIGN.RIGHT)

    for idx, (kicker, title, slug) in enumerate(SLIDES, 2):
        s = d.slide(fill=d.b.WHITE)
        header(d, s, kicker, title)
        add_excalidraw_board(d, s, slug)
        source_note(d, s, slug, idx, total)

    d.save(OUT)


if __name__ == "__main__":
    build()
