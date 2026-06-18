#!/usr/bin/env python3
"""Build client-facing MagicPath pre-sales demo accelerator deck."""
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR
from PIL import Image, ImageDraw, ImageFont


TOTAL = 18
OUT = "docs/reports/magicpath-presales-demo-accelerator-reviewed.pptx"
ASSET_DIR = Path("docs/reports/magicpath_presales_assets")
FFMPEG = "/home/shekerk/snap/codex/64/.dotnet/tools/ffmpeg"

d = Deck(footer="MagicPath Pre-Sales Demo Accelerator | June 2026")
b = d.b



def _font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def _wrap(draw, text, font, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def make_video_card(path, title, subtitle, bullets, tag):
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (1280, 720), "#0A1628")
    dr = ImageDraw.Draw(img)
    dr.rectangle([0, 0, 1280, 18], fill="#00C9A7")
    dr.rectangle([1000, 0, 1280, 720], fill="#12243A")
    dr.rectangle([70, 94, 940, 600], outline="#00C9A7", width=3)
    dr.rectangle([92, 118, 918, 575], fill="#F4F7F8")
    dr.polygon([(475, 300), (475, 420), (595, 360)], fill="#00C9A7")
    dr.text((70, 35), tag.upper(), font=_font(24, True), fill="#00C9A7")
    dr.text((1040, 75), "VIDEO\nDEMO", font=_font(42, True), fill="#FFFFFF", spacing=4)
    dr.text((70, 625), title, font=_font(38, True), fill="#FFFFFF")
    dr.text((70, 670), subtitle, font=_font(20), fill="#D9DFE5")
    y = 195
    for bullet in bullets:
        for j, line in enumerate(_wrap(dr, bullet, _font(23), 245)):
            prefix = "- " if j == 0 else "  "
            dr.text((1030, y), prefix + line, font=_font(23), fill="#D9DFE5")
            y += 34
        y += 12
    img.save(path)
    return path


def make_storyboard_video(name, title, frames):
    work = ASSET_DIR / name
    work.mkdir(parents=True, exist_ok=True)
    for i, (headline, body) in enumerate(frames):
        frame = Image.new("RGB", (1280, 720), "#0A1628")
        dr = ImageDraw.Draw(frame)
        dr.rectangle([0, 0, 1280, 18], fill="#00C9A7")
        dr.rectangle([90, 95, 1190, 610], fill="#F4F7F8")
        dr.rectangle([90, 95, 1190, 152], fill="#12243A")
        dr.text((125, 112), title, font=_font(24, True), fill="#00C9A7")
        dr.text((125, 210), headline, font=_font(48, True), fill="#0A1628")
        y = 310
        for line in _wrap(dr, body, _font(30), 940):
            dr.text((125, y), line, font=_font(30), fill="#1B2B3C")
            y += 42
        dr.rectangle([980, 470, 1140, 555], fill="#00C9A7")
        dr.text((1018, 492), f"{i+1}/4", font=_font(34, True), fill="#0A1628")
        frame.save(work / f"frame_{i:02d}.png")
    out = ASSET_DIR / f"{name}.mp4"
    if Path(FFMPEG).exists():
        subprocess.run([
            FFMPEG, "-y", "-framerate", "0.5", "-i", str(work / "frame_%02d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf", "scale=1280:720", str(out)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out


def build_assets():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    cards = {
        "official": make_video_card(
            ASSET_DIR / "video-card-magicpath-official.png",
            "MagicPath Official Tutorials",
            "Proof library for product mechanics and feature walkthroughs.",
            ["Shared canvas", "Figma import", "External agents", "Code output"],
            "External video",
        ),
        "pietro": make_video_card(
            ASSET_DIR / "video-card-pietro-short.png",
            "The Future of Design with MagicPath AI",
            "Short demo-style proof point for executive audiences.",
            ["AI design canvas", "Interactive prototype", "Design-to-code motion"],
            "External video",
        ),
        "interview": make_video_card(
            ASSET_DIR / "video-card-founder-interview.png",
            "Founder Demo / Interview",
            "Longer context on MagicPath's design-to-development vision.",
            ["Product vision", "Workflow rationale", "Design systems"],
            "External video",
        ),
    }
    videos = {
        "manufacturing": make_storyboard_video("manufacturing-demo-storyboard", "Manufacturing Demo Storyboard", [
            ("Brief", "VP Manufacturing needs downtime and maintenance risk visible before a line stoppage."),
            ("Canvas", "MagicPath generates a plant dashboard with asset health, severity-ranked alerts, and SAP PM status."),
            ("Agent build", "Codex turns the design into a clickable prototype with mock sensor data and work-order flow."),
            ("Demo close", "The buyer clicks an alert, opens root cause, and sees the POC path to historian and SAP integration."),
        ]),
        "legal": make_storyboard_video("legal-demo-storyboard", "Legal Demo Storyboard", [
            ("Brief", "Managing partner wants AI review without hallucinated legal decisions."),
            ("Canvas", "MagicPath creates upload, clause risk review, and partner approval screens."),
            ("Agent build", "The prototype uses a sample NDA, confidence scores, risk flags, and human override."),
            ("Demo close", "The firm sees AI embedded in the existing review workflow, not replacing legal judgment."),
        ]),
        "healthcare": make_storyboard_video("healthcare-demo-storyboard", "Healthcare Demo Storyboard", [
            ("Brief", "Practice manager needs intake work removed from the front desk without disrupting EHR operations."),
            ("Canvas", "MagicPath creates mobile intake and staff queue screens with verification badges."),
            ("Agent build", "The prototype lets a patient submit intake and appear in a staff dashboard immediately."),
            ("Demo close", "The practice sees the ROI: fewer phone calls, faster intake, cleaner pre-visit records."),
        ]),
    }
    return cards, videos


CARDS, VIDEOS = build_assets()


def footer(s, n, dark=False):
    d.footer(s, n, TOTAL, dark=dark)


def chip(s, text, left, top, width, fill=None, color=None):
    fill = fill or b.NAVY_2
    color = color or b.TEAL
    d.rect(s, left, top, width, Inches(0.42), fill, radius=0.08)
    d.text(
        s,
        text,
        left + Inches(0.08),
        top + Inches(0.04),
        width - Inches(0.16),
        Inches(0.34),
        size=10.5,
        color=color,
        bold=True,
        align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE,
        shrink=True,
    )


def section_label(s, text, top=1.55):
    d.text(s, text, d.M, Inches(top), d.CW, Inches(0.3), size=10.5, color=b.MUTED, bold=True)


def metric_card(s, left, top, title, value, body, fill=None):
    d.rect(s, left, top, Inches(3.65), Inches(1.55), fill or b.SOFT, radius=0.05, shadow=True)
    d.text(s, title, left + Inches(0.18), top + Inches(0.14), Inches(3.25), Inches(0.28),
           size=10.5, color=b.MUTED, bold=True, shrink=True)
    d.text(s, value, left + Inches(0.18), top + Inches(0.45), Inches(3.25), Inches(0.48),
           size=22, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, left + Inches(0.18), top + Inches(1.0), Inches(3.25), Inches(0.55),
           size=9.8, color=b.INK, shrink=True)


def scenario_card(s, idx, title, buyer, demo, close, left, top, accent):
    d.rect(s, left, top, Inches(3.9), Inches(2.15), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, left, top, Inches(3.9), Inches(0.08), accent)
    d.text(s, f"{idx}", left + Inches(0.18), top + Inches(0.22), Inches(0.35), Inches(0.35),
           size=16, color=accent, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, title, left + Inches(0.62), top + Inches(0.17), Inches(3.1), Inches(0.34),
           size=13.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, buyer, left + Inches(0.2), top + Inches(0.62), Inches(3.45), Inches(0.32),
           size=10.3, color=b.MUTED, bold=True, shrink=True)
    d.text(s, demo, left + Inches(0.2), top + Inches(0.98), Inches(3.45), Inches(0.5),
           size=10.2, color=b.INK, shrink=True)
    d.text(s, close, left + Inches(0.2), top + Inches(1.55), Inches(3.45), Inches(0.45),
           size=9.6, color=b.NAVY, bold=True, shrink=True)


# 1. Cover
s = d.slide(fill=b.NAVY)
d.rect(s, Inches(11.35), 0, Inches(1.98), d.H, b.NAVY_2)
d.rect(s, Inches(11.35), 0, Inches(0.08), d.H, b.TEAL)
d.text(s, "EXECUTIVE STRATEGY DECK", d.M, Inches(0.92), Inches(7), Inches(0.35),
       size=13, color=b.TEAL, bold=True)
d.text(s, "MagicPath as a\nPre-Sales Demo\nAccelerator",
       d.M, Inches(1.42), Inches(9.8), Inches(2.55),
       size=42, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.rect(s, d.M, Inches(4.25), Inches(1.35), Inches(0.06), b.TEAL)
d.text(s, "Compress the path from prospect brief to tailored clickable prototype by combining AI design generation, product capture, and coding-agent handoff.",
       d.M, Inches(4.55), Inches(8.8), Inches(0.95), size=15, color=b.MUTED, shrink=True)
x = d.M
for label in ["Business Scenarios", "POC Packaging", "Sales Motion", "Evidence Base"]:
    chip(s, label, x, Inches(5.55), Inches(2.15))
    x += Inches(2.35)
footer(s, 1, dark=True)


# 2. Executive thesis
s = d.slide(fill=b.WHITE)
d.header(s, "The Executive Thesis", "MagicPath turns pre-sales from explanation into experience")
d.rect(s, d.M, Inches(1.68), d.CW, Inches(1.0), b.NAVY, radius=0.04)
d.text(s, "MagicPath can materially compress the path from prospect brief to tailored clickable prototype by combining AI design generation, existing design/product capture, and coding-agent handoff into one workflow.",
       Inches(0.85), Inches(1.78), Inches(11.5), Inches(0.78),
       size=16, color=b.WHITE, bold=True, shrink=True)
metric_card(s, d.M, Inches(3.05), "Buyer Problem", '"Show me mine"', "Prospects need to see their workflow, data, systems, and operating language before they believe.", b.SOFT)
metric_card(s, Inches(4.65), Inches(3.05), "Sales Constraint", "Demo gap", "Generic demos undersell value; custom prototypes are usually too slow and expensive.", b.SOFT)
metric_card(s, Inches(8.7), Inches(3.05), "MagicPath Role", "Same-cycle proof", "A tailored prototype becomes the artifact that converts discovery into scoped POC.", b.LIGHT_TEAL)
d.rect(s, d.M, Inches(5.55), d.CW, Inches(0.72), b.GOLD, radius=0.03)
d.text(s, "Commercial implication: the demo stops being a marketing asset and becomes the first implementation artifact.",
       Inches(0.85), Inches(5.63), Inches(11.5), Inches(0.55), size=14, color=b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
footer(s, 2)


# 3. Pre-sales bottleneck
s = d.slide(fill=b.WHITE)
d.header(s, "The Pre-Sales Bottleneck", "The moment deals slow down is the moment the prospect asks for relevance")
items = [
    ("Static mockup", "Looks polished but cannot prove the workflow, exception handling, or system fit.", b.CORAL),
    ("Generic demo", "Shows product capability but fails the buyer's mental test: would this work here?", b.GOLD),
    ("Custom prototype", "High-conviction path, but often takes days or weeks of solution architect and developer time.", b.TEAL),
]
for i, (title, body, color) in enumerate(items):
    left = d.M + i * Inches(4.05)
    d.rect(s, left, Inches(1.85), Inches(3.75), Inches(2.6), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, left, Inches(1.85), Inches(3.75), Inches(0.08), color)
    d.text(s, title, left + Inches(0.22), Inches(2.15), Inches(3.3), Inches(0.42),
           size=19, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, left + Inches(0.22), Inches(2.85), Inches(3.3), Inches(1.25),
           size=12.5, color=b.INK, shrink=True)
d.text(s, "What needs to change", d.M, Inches(5.05), Inches(3), Inches(0.35),
       size=12, color=b.MUTED, bold=True)
d.rect(s, d.M, Inches(5.5), d.CW, Inches(0.8), b.NAVY, radius=0.04)
d.text(s, "Move from 'we can explain the solution' to 'we can put a believable first version in the prospect's hands while the buying energy is still high.'",
       Inches(0.9), Inches(5.6), Inches(11.3), Inches(0.58), size=15, color=b.WHITE, bold=True, shrink=True)
footer(s, 3)


# 4. Workflow
s = d.slide(fill=b.WHITE)
d.header(s, "The MagicPath Acceleration Loop", "A single workflow connects discovery, design, agent build, and demo")
steps = [
    ("1", "Prospect brief", "Industry, buyer, workflow, systems, metrics, objections"),
    ("2", "MagicPath canvas", "Prompt, Figma import, website capture, design systems"),
    ("3", "Agent handoff", "Codex / Claude Code / Cursor reads canvas context"),
    ("4", "Prototype build", "Clickable flow, mock data, realistic states, integration placeholders"),
    ("5", "Live demo", "Prospect interacts; team captures changes as POC scope"),
]
box_w = Inches(2.25)
for i, (num, title, body) in enumerate(steps):
    left = d.M + i * Inches(2.48)
    d.rect(s, left, Inches(2.05), box_w, Inches(2.15), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, left, Inches(2.05), box_w, Inches(0.08), b.TEAL if i < 2 else b.GOLD if i == 2 else b.CORAL)
    d.text(s, num, left + Inches(0.14), Inches(2.28), Inches(0.42), Inches(0.42),
           size=18, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, title, left + Inches(0.14), Inches(2.83), box_w - Inches(0.28), Inches(0.4),
           size=13.2, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, left + Inches(0.14), Inches(3.32), box_w - Inches(0.28), Inches(0.78),
           size=10.2, color=b.INK, shrink=True)
    if i < len(steps) - 1:
        d.text(s, "→", left + box_w + Inches(0.03), Inches(2.85), Inches(0.18), Inches(0.45),
               size=16, color=b.MUTED, align=PP_ALIGN.CENTER)
d.rect(s, d.M, Inches(5.25), d.CW, Inches(0.9), b.LIGHT_TEAL, radius=0.04)
d.text(s, "Core operating principle: the design canvas becomes the sales spec, the coding agent becomes the demo builder, and the live prototype becomes the qualification artifact.",
       Inches(0.9), Inches(5.37), Inches(11.3), Inches(0.65), size=14, color=b.NAVY, bold=True, shrink=True)
footer(s, 4)


# 5. Evidence base
s = d.slide(fill=b.WHITE)
d.header(s, "What Is Substantiated", "Use source-backed claims with executives; avoid unbenchmarked promises")
claims = [
    ("Shared human + agent canvas", "MagicPath positions the product as a real-time canvas where humans and agents design together, with external agents including Claude Code, Codex, and Cursor.", "MagicPath docs / homepage", b.TEAL),
    ("Figma and web capture inputs", "MagicPath documents Figma Connect and web/product capture paths, supporting the 'start from existing context' motion.", "MagicPath Figma Connect; UX Tools", b.GOLD),
    ("Code output and agent handoff", "MagicPath describes code export and agent-driven workflows; recent Codex plugin messaging supports Codex as a design/build surface.", "MagicPath docs; Codex plugin blog", b.CORAL),
    ("Market validation of the pattern", "Anthropic's Claude Design also validates the design-to-code handoff pattern through prototype generation and Claude Code handoff.", "Anthropic Claude Design", b.ACCENT),
]
for i, (title, body, src, color) in enumerate(claims):
    top = Inches(1.72) + i * Inches(1.22)
    d.rect(s, d.M, top, Inches(0.12), Inches(0.9), color)
    d.text(s, title, Inches(0.85), top, Inches(3.75), Inches(0.32), size=13.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(4.55), top, Inches(6.0), Inches(0.54), size=11.2, color=b.INK, shrink=True)
    d.text(s, src, Inches(10.75), top, Inches(1.75), Inches(0.54), size=9.5, color=b.MUTED, bold=True, shrink=True)
d.rect(s, d.M, Inches(6.3), d.CW, Inches(0.48), b.SOFT, radius=0.03)
d.text(s, "Recommended wording: 'materially compress' and 'same-cycle prototype' are defensible; exact cost/time ratios should be based on internal benchmark runs.",
       Inches(0.85), Inches(6.37), Inches(11.5), Inches(0.46), size=10.8, color=b.NAVY, bold=True, shrink=True)
footer(s, 5)


# 6. Six scenarios
s = d.slide(fill=b.WHITE)
d.header(s, "Six Business Scenarios", "Each demo turns a vertical workflow into a clickable proof-of-fit")
scenario_card(s, 1, "Manufacturing", "Buyer: VP Manufacturing / Plant VP", "Predictive maintenance or quality dashboard with alerts, asset health, and SAP PM placeholder.", "Close signal: plant leader sees their downtime or scrap workflow.", d.M, Inches(1.75), b.TEAL)
scenario_card(s, 2, "Legal", "Buyer: Managing Partner / Legal Ops", "Contract review workspace with risk highlights, confidence, citations, and human approval.", "Close signal: trust barrier drops because humans stay in control.", Inches(4.66), Inches(1.75), b.GOLD)
scenario_card(s, 3, "Healthcare", "Buyer: Practice Manager / COO", "Mobile intake flow plus staff dashboard with verification badges and EHR sync indicators.", "Close signal: ROI is obvious when intake time falls from minutes to seconds.", Inches(8.72), Inches(1.75), b.CORAL)
scenario_card(s, 4, "Financial Services", "Buyer: VP Mortgage Ops / Risk", "Document processing console with extracted fields, source links, compliance checklist.", "Close signal: AI recommends; underwriter decides.", d.M, Inches(4.3), b.ACCENT)
scenario_card(s, 5, "Construction", "Buyer: Project Director / Safety Lead", "Site command center with progress, safety exceptions, imagery, and morning report.", "Close signal: current weekly reporting becomes daily operating intelligence.", Inches(4.66), Inches(4.3), b.TEAL)
scenario_card(s, 6, "AI Readiness", "Buyer: CTO / Transformation Lead", "Assessment portal with maturity radar, ranked use cases, ROI ranges, next-step CTAs.", "Close signal: vague AI interest becomes three funded projects.", Inches(8.72), Inches(4.3), b.GOLD)
footer(s, 6)


# 7. Scenario playbook
s = d.slide(fill=b.WHITE)
d.header(s, "Scenario Playbook", "What the sales team needs to prepare before the meeting")
rows = [
    ("Manufacturing", "Plant layout, SAP PM/QM language, OEE/downtime metric", "Asset health heatmap; alert-to-work-order flow", "Predictive maintenance or quality POC"),
    ("Legal", "Template, clause taxonomy, review authority model", "Upload → risk review → partner sign-off", "Template-based review automation"),
    ("Healthcare", "Patient intake steps, insurance/EHR context, staffing pain", "Mobile intake + staff verification dashboard", "HIPAA-ready intake automation POC"),
    ("Mortgage Ops", "Borrower package, LOS context, underwriting checklist", "Extraction review + compliance sign-off", "Document AI + human adjudication POC"),
    ("Construction", "Site portfolio, reporting cadence, safety categories", "Map → site drilldown → morning report", "Computer vision and reporting POC"),
    ("AI Readiness", "Tech stack, data maturity, executive priorities", "Wizard → recommendations → ROI cards", "Paid discovery and roadmap sprint"),
]
headers = ["Scenario", "Inputs", "Prototype Moment", "Next Commercial Step"]
widths = [Inches(2.1), Inches(3.4), Inches(3.35), Inches(3.45)]
lefts = [d.M, Inches(2.82), Inches(6.32), Inches(9.77)]
for j, h in enumerate(headers):
    d.rect(s, lefts[j], Inches(1.72), widths[j], Inches(0.42), b.NAVY)
    d.text(s, h, lefts[j] + Inches(0.08), Inches(1.77), widths[j] - Inches(0.16), Inches(0.32),
           size=10.2, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
for i, row in enumerate(rows):
    top = Inches(2.18) + i * Inches(0.72)
    fill = b.SOFT if i % 2 == 0 else b.WHITE
    for j, val in enumerate(row):
        d.rect(s, lefts[j], top, widths[j], Inches(0.64), fill, line=b.GRID)
        d.text(s, val, lefts[j] + Inches(0.08), top + Inches(0.06), widths[j] - Inches(0.16), Inches(0.52),
               size=9.4 if j else 10.2, color=b.NAVY if j == 0 else b.INK, bold=(j == 0), shrink=True)
footer(s, 7)


# 8. POC packaging
s = d.slide(fill=b.WHITE)
d.header(s, "Turn Demos Into Packaged POCs", "The prototype should make the next purchase decision smaller and clearer")
packages = [
    ("Lite", "$15K-$25K", "2 weeks", "Clickable prototype + workflow validation + data/integration plan", "Best for ambiguous AI readiness or early-stage prospects", b.TEAL),
    ("Focused POC", "$40K-$75K", "4-6 weeks", "One workflow, one dataset, one operating dashboard, one success metric", "Best default package after a vertical demo", b.GOLD),
    ("Production Pilot", "$100K-$250K", "8-12 weeks", "Secure deployment, system integration, user testing, adoption workflow", "Best when executive sponsor already owns budget", b.CORAL),
]
for i, (name, price, time, scope, fit, color) in enumerate(packages):
    left = d.M + i * Inches(4.05)
    d.rect(s, left, Inches(1.85), Inches(3.75), Inches(3.55), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, left, Inches(1.85), Inches(3.75), Inches(0.1), color)
    d.text(s, name, left + Inches(0.22), Inches(2.12), Inches(3.3), Inches(0.36), size=18, color=b.NAVY, bold=True)
    d.text(s, price, left + Inches(0.22), Inches(2.62), Inches(3.3), Inches(0.45), size=22, color=color, bold=True, shrink=True)
    d.text(s, time, left + Inches(0.22), Inches(3.12), Inches(3.3), Inches(0.28), size=11, color=b.MUTED, bold=True)
    d.text(s, scope, left + Inches(0.22), Inches(3.58), Inches(3.3), Inches(0.78), size=11.2, color=b.INK, shrink=True)
    d.text(s, fit, left + Inches(0.22), Inches(4.55), Inches(3.3), Inches(0.55), size=10.4, color=b.NAVY, bold=True, shrink=True)
d.rect(s, d.M, Inches(6.05), d.CW, Inches(0.55), b.NAVY, radius=0.03)
d.text(s, "Pricing principle: MagicPath accelerates the demo, not the value. Charge for risk reduction, workflow specificity, and implementation confidence.",
       Inches(0.85), Inches(6.13), Inches(11.5), Inches(0.48), size=11.6, color=b.TEAL, bold=True, shrink=True)
footer(s, 8)


# 9. Sales operating model
s = d.slide(fill=b.WHITE)
d.header(s, "The Sales Operating Model", "Define who does what so the workflow scales beyond founder-led demos")
lanes = [
    ("Account Exec", "Owns discovery, buyer map, business pain, commercial next step", b.CORAL),
    ("Solution Lead", "Translates discovery into demo brief, workflow, metrics, data assumptions", b.GOLD),
    ("MagicPath Operator", "Creates canvas, imports context, refines screens, enforces brand/workflow realism", b.TEAL),
    ("Coding Agent Lead", "Turns canvas into clickable app, mock data, deployment, demo script", b.ACCENT),
]
for i, (role, body, color) in enumerate(lanes):
    top = Inches(1.75) + i * Inches(1.15)
    d.rect(s, d.M, top, Inches(2.75), Inches(0.78), color, radius=0.04)
    d.text(s, role, d.M + Inches(0.18), top + Inches(0.08), Inches(2.38), Inches(0.62),
           size=13, color=b.WHITE if color != b.GOLD else b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.text(s, body, Inches(3.25), top + Inches(0.06), Inches(9.1), Inches(0.66), size=12.3, color=b.INK, shrink=True)
d.rect(s, d.M, Inches(6.35), d.CW, Inches(0.45), b.SOFT, radius=0.03)
d.text(s, "Repeatable artifact stack: discovery brief, MagicPath canvas, prototype repo, demo script, POC scope, post-demo decision memo.",
       Inches(0.85), Inches(6.42), Inches(11.5), Inches(0.46), size=10.8, color=b.NAVY, bold=True, shrink=True)
footer(s, 9)


# 10. ROI logic
s = d.slide(fill=b.WHITE)
d.header(s, "ROI Logic For Sales Leaders", "The business case is not only cheaper demos; it is higher conversion velocity")
metric_card(s, d.M, Inches(1.85), "Cycle Compression", "Days, not weeks", "Earlier relevance reduces the dead zone after discovery.", b.LIGHT_TEAL)
metric_card(s, Inches(4.65), Inches(1.85), "Qualification Quality", "Better mutual fit", "Clickable workflows reveal integration, adoption, and sponsor gaps early.", b.SOFT)
metric_card(s, Inches(8.7), Inches(1.85), "POC Conversion", "Scoped next step", "The demo becomes the first draft of the POC statement of work.", b.SOFT)
d.text(s, "Measure this motion with commercial metrics, not design metrics:", d.M, Inches(4.15), d.CW, Inches(0.35), size=13.5, color=b.NAVY, bold=True)
metrics = [
    "Discovery-to-demo elapsed time",
    "Demo-to-POC conversion rate",
    "POC scope clarity at proposal stage",
    "Average sales cycle duration",
    "Solution architect hours per qualified demo",
    "Executive sponsor engagement after demo",
]
for i, m in enumerate(metrics):
    col = i % 2
    row = i // 2
    left = d.M + col * Inches(6.15)
    top = Inches(4.65) + row * Inches(0.52)
    d.text(s, [{"text": m, "bullet": True, "size": 12.2, "space_before": 4}], left, top, Inches(5.8), Inches(0.38), shrink=True)
footer(s, 10)


# 11. Governance
s = d.slide(fill=b.WHITE)
d.header(s, "Guardrails For Executive-Grade Demos", "The prototype must feel specific without pretending to be production")
guardrails = [
    ("Label assumptions", "Mark mock data, placeholder integrations, and unverified AI outputs clearly."),
    ("Keep human approval visible", "Legal, healthcare, finance, and safety demos should show review, override, and audit trails."),
    ("Use realistic domain language", "Borrow the buyer's operating vocabulary: SAP PM, EHR sync, LOS, OEE, DTI, site safety."),
    ("Do not overclaim readiness", "Demo acceleration does not remove security, compliance, integration, or change-management work."),
    ("Capture edits live", "Every 'can it also do X?' becomes either a canvas update or a POC backlog item."),
]
for i, (title, body) in enumerate(guardrails):
    top = Inches(1.78) + i * Inches(0.95)
    d.rect(s, d.M, top, Inches(0.48), Inches(0.48), b.NAVY, radius=0.08)
    d.text(s, str(i + 1), d.M + Inches(0.05), top + Inches(0.02), Inches(0.38), Inches(0.42),
           size=15, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, title, Inches(1.28), top - Inches(0.02), Inches(3.5), Inches(0.32), size=13.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(4.65), top - Inches(0.02), Inches(7.7), Inches(0.46), size=11.5, color=b.INK, shrink=True)
footer(s, 11)


# 12. Demo storyboard
s = d.slide(fill=b.WHITE)
d.header(s, "A 90-Second Demo Storyboard", "Use the same narrative spine across every vertical")
story = [
    ("Open on pain", "Show the exact workflow bottleneck the prospect described."),
    ("Reveal tailored UI", "Use their language, systems, roles, and metrics."),
    ("Click the exception", "Open an alert, flagged clause, intake issue, safety violation, or document mismatch."),
    ("Show human control", "Approve, reject, escalate, or assign; do not imply blind automation."),
    ("Create the next step", "Generate work order, review queue, report, roadmap, or POC scope."),
    ("Ask for implementation data", "Shift from imagination to access: dataset, system, owner, timeline."),
]
for i, (title, body) in enumerate(story):
    left = d.M + (i % 3) * Inches(4.1)
    top = Inches(1.85) + (i // 3) * Inches(2.05)
    d.rect(s, left, top, Inches(3.78), Inches(1.55), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, left, top, Inches(3.78), Inches(0.08), b.TEAL if i < 3 else b.GOLD)
    d.text(s, f"{i+1}. {title}", left + Inches(0.2), top + Inches(0.22), Inches(3.35), Inches(0.48),
           size=12.6, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, left + Inches(0.2), top + Inches(0.72), Inches(3.35), Inches(0.55),
           size=11.2, color=b.INK, shrink=True)
d.rect(s, d.M, Inches(6.15), d.CW, Inches(0.48), b.NAVY, radius=0.03)
d.text(s, "Rule: one interaction every 15 seconds. The buyer should touch the workflow, not watch a product tour.",
       Inches(0.85), Inches(6.22), Inches(11.5), Inches(0.32), size=12, color=b.TEAL, bold=True, shrink=True)
footer(s, 12)


# 13. Competitive context
s = d.slide(fill=b.WHITE)
d.header(s, "Competitive Context", "MagicPath wins when the demo motion needs multi-agent flexibility and external tooling")
cols = [
    ("MagicPath-led motion", ["Shared canvas for humans and agents", "Figma import, web capture, prompt-to-design", "External agents: Codex, Claude Code, Cursor", "Good fit for sales teams that need fast vertical prototypes"], b.TEAL),
    ("Claude Design pattern", ["Native Anthropic visual creation surface", "Prototype and handoff to Claude Code", "Validates the market direction", "Good fit when the team is standardized on Claude"], b.GOLD),
    ("Traditional custom demo", ["High control and production realism", "Slow and expensive for early-stage deals", "Often requires scarce solution architect capacity", "Best reserved for late-stage enterprise pursuits"], b.CORAL),
]
for i, (title, bullets, color) in enumerate(cols):
    left = d.M + i * Inches(4.05)
    d.rect(s, left, Inches(1.85), Inches(3.75), Inches(4.1), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, left, Inches(1.85), Inches(3.75), Inches(0.1), color)
    d.text(s, title, left + Inches(0.2), Inches(2.15), Inches(3.35), Inches(0.42), size=15, color=b.NAVY, bold=True, shrink=True)
    for j, bullet in enumerate(bullets):
        d.text(s, [{"text": bullet, "bullet": True, "size": 10.8, "space_before": 4}],
               left + Inches(0.25), Inches(2.78) + j * Inches(0.56), Inches(3.3), Inches(0.42), shrink=True)
footer(s, 13)


# 14. Roadmap
s = d.slide(fill=b.WHITE)
d.header(s, "30-Day Rollout Plan", "Stand up the demo accelerator as a repeatable sales capability")
weeks = [
    ("Week 1", "Build the demo library", "Pick six vertical scenarios, define reusable prompts, components, mock datasets, and demo scripts."),
    ("Week 2", "Create operating standards", "Define intake brief, QA checklist, disclosure language, prototype repo structure, and handoff process."),
    ("Week 3", "Pilot with live pursuits", "Run 3-5 active opportunities through the workflow; measure elapsed time and buyer response."),
    ("Week 4", "Package for scale", "Convert best demos into reusable templates and align POC packages, pricing, and sales enablement."),
]
for i, (week, title, body) in enumerate(weeks):
    top = Inches(1.75) + i * Inches(1.2)
    d.rect(s, d.M, top, Inches(1.25), Inches(0.75), b.NAVY, radius=0.04)
    d.text(s, week, d.M + Inches(0.1), top + Inches(0.08), Inches(1.05), Inches(0.58),
           size=13, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, title, Inches(2.0), top, Inches(3.3), Inches(0.48), size=13.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(5.2), top, Inches(7.2), Inches(0.58), size=11.6, color=b.INK, shrink=True)
d.rect(s, d.M, Inches(6.35), d.CW, Inches(0.45), b.LIGHT_TEAL, radius=0.03)
d.text(s, "Decision required: choose first three live opportunities and assign one MagicPath operator plus one coding-agent lead.",
       Inches(0.85), Inches(6.42), Inches(11.5), Inches(0.46), size=10.8, color=b.NAVY, bold=True, shrink=True)
footer(s, 14)



# 15. Short demo videos: external proof
s = d.slide(fill=b.WHITE)
d.header(s, "Short Demo Videos To Substantiate The Motion", "External proof assets plus the talk track sales should use")
video_items = [
    ("MagicPath Official Tutorials", "https://www.youtube.com/@MagicPathAI", CARDS["official"], "Use this as the product proof library: canvas workflow, agent features, import/export mechanics."),
    ("Pietro short demo", "https://www.youtube.com/watch?v=ZSOb2uijfSE", CARDS["pietro"], "Use this as the fast executive proof point: design surface to interactive prototype."),
    ("Founder demo/interview", "https://www.youtube.com/watch?v=LhCA5GzqbPU", CARDS["interview"], "Use this when the buyer wants broader context on the design-to-development shift."),
]
for i, (title, url, img, note) in enumerate(video_items):
    left = d.M + i * Inches(4.05)
    pic = s.shapes.add_picture(str(img), left, Inches(1.75), width=Inches(3.75), height=Inches(2.11))
    pic.click_action.hyperlink.address = url
    d.text(s, title, left, Inches(4.05), Inches(3.75), Inches(0.32), size=12.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, note, left, Inches(4.45), Inches(3.75), Inches(0.65), size=10.6, color=b.INK, shrink=True)
    link = d.text(s, url, left, Inches(5.22), Inches(3.75), Inches(0.36), size=8.3, color=b.ACCENT, shrink=True)
    link.click_action.hyperlink.address = url
d.rect(s, d.M, Inches(6.2), d.CW, Inches(0.5), b.NAVY, radius=0.03)
d.text(s, "Meeting usage: do not play long videos in full. Open 20-40 seconds, point to the workflow pattern, then switch to the tailored prospect demo.",
       Inches(0.85), Inches(6.27), Inches(11.5), Inches(0.46), size=10.8, color=b.TEAL, bold=True, shrink=True)
footer(s, 15)


# 16. Short demo videos: custom storyboard assets
s = d.slide(fill=b.WHITE)
d.header(s, "Short Demo Videos Built For This Deck", "Local MP4 storyboards for the three highest-fit sales scenarios")
custom_items = [
    ("Manufacturing", VIDEOS["manufacturing"], "Alert-to-work-order demo for VP Manufacturing or Plant VP."),
    ("Legal", VIDEOS["legal"], "Contract-risk workflow for Managing Partner or Legal Ops."),
    ("Healthcare", VIDEOS["healthcare"], "Patient intake automation for Practice Manager or COO."),
]
for i, (title, path, note) in enumerate(custom_items):
    left = d.M + i * Inches(4.05)
    poster = Path(str(path).replace(".mp4", "")) / "frame_03.png"
    pic = s.shapes.add_picture(str(poster), left, Inches(1.78), width=Inches(3.75), height=Inches(2.11))
    pic.click_action.hyperlink.address = str(path.resolve())
    d.text(s, title, left, Inches(4.1), Inches(3.75), Inches(0.32), size=14, color=b.NAVY, bold=True, shrink=True)
    d.text(s, note, left, Inches(4.48), Inches(3.75), Inches(0.45), size=10.8, color=b.INK, shrink=True)
    d.text(s, "Local MP4: " + str(path), left, Inches(5.08), Inches(3.75), Inches(0.46), size=8.3, color=b.ACCENT, shrink=True)
d.rect(s, d.M, Inches(6.18), d.CW, Inches(0.52), b.LIGHT_TEAL, radius=0.03)
d.text(s, "These MP4s are short storyboard assets, not product recordings. Use them to tee up what the live MagicPath/Codex demo should prove.",
       Inches(0.85), Inches(6.26), Inches(11.5), Inches(0.46), size=10.8, color=b.NAVY, bold=True, shrink=True)
footer(s, 16)


# 17. Video-based slide structure
s = d.slide(fill=b.WHITE)
d.header(s, "How To Use Video In The Sales Meeting", "A short video should accelerate belief, then hand off to the live tailored prototype")
sequence = [
    ("0:00-0:20", "Pattern proof", "Play a MagicPath clip showing design-to-prototype mechanics."),
    ("0:20-0:45", "Vertical relevance", "Show the local storyboard for the buyer's industry scenario."),
    ("0:45-1:30", "Tailored demo", "Switch to the prospect-specific clickable prototype and let the buyer drive."),
    ("1:30-2:00", "POC bridge", "Convert questions into data access, integration scope, owners, and success metrics."),
]
for i, (time, title, body) in enumerate(sequence):
    top = Inches(1.85) + i * Inches(1.05)
    d.rect(s, d.M, top, Inches(1.45), Inches(0.66), b.NAVY, radius=0.04)
    d.text(s, time, d.M + Inches(0.1), top + Inches(0.1), Inches(1.25), Inches(0.46), size=11, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.text(s, title, Inches(2.2), top, Inches(3.0), Inches(0.32), size=15, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(5.0), top, Inches(7.35), Inches(0.5), size=11.8, color=b.INK, shrink=True)
d.rect(s, d.M, Inches(6.35), d.CW, Inches(0.45), b.GOLD, radius=0.03)
d.text(s, "Never let the video become the demo. The video validates the workflow pattern; the tailored prototype closes the relevance gap.",
       Inches(0.85), Inches(6.42), Inches(11.5), Inches(0.46), size=10.8, color=b.NAVY, bold=True, shrink=True)
footer(s, 17)


# 18. Sources
s = d.slide(fill=b.WHITE)
d.header(s, "Sources And Recommended Proof Assets", "Use these links to substantiate the deck and build the demo library")
sources = [
    ("MagicPath documentation", "https://www.magicpath.ai/documentation", "Official product claims: shared canvas, agents, design systems, code export."),
    ("MagicPath homepage", "https://www.magicpath.ai/", "External agents and design-code workflow positioning."),
    ("MagicPath Figma Connect", "https://www.magicpath.ai/documentation/features/figma-connect", "Figma import / interactive prototype workflow."),
    ("MagicPath Codex plugin", "https://www.magicpath.ai/blog/magicpath-official-codex-plugin", "Codex plugin announcement and agentic app workflow."),
    ("UX Tools article", "https://www.uxtools.co/blog/3-ways-magicpath-closes-the-design-to-code-gap", "Third-party validation of Figma, live product, prompt, and code output paths."),
    ("Anthropic Claude Design", "https://www.anthropic.com/news/claude-design-anthropic-labs", "Market validation of prototype-to-Claude-Code handoff pattern."),
    ("MagicPath YouTube", "https://www.youtube.com/@MagicPathAI", "Tutorials and demo videos for sales enablement."),
]
for i, (name, url, note) in enumerate(sources):
    top = Inches(1.68) + i * Inches(0.78)
    d.text(s, name, d.M, top, Inches(2.85), Inches(0.26), size=11.2, color=b.NAVY, bold=True, shrink=True)
    d.text(s, url, Inches(3.35), top, Inches(4.9), Inches(0.26), size=8.6, color=b.ACCENT, shrink=True)
    d.text(s, note, Inches(8.45), top, Inches(4.0), Inches(0.34), size=9.4, color=b.INK, shrink=True)
d.rect(s, d.M, Inches(6.45), d.CW, Inches(0.38), b.SOFT, radius=0.03)
d.text(s, "Deck status: reviewed after PPTX structural validation and preview render. Video-card slides link to external proof assets and local storyboard MP4s; claims requiring internal benchmarks are framed as hypotheses or recommended metrics.",
       Inches(0.85), Inches(6.51), Inches(11.5), Inches(0.42), size=9.8, color=b.NAVY, bold=True, shrink=True)
footer(s, 18)


d.save(OUT)
