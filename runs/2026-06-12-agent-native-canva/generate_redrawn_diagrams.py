#!/usr/bin/env python3
"""Render clean portrait diagram assets for the agent-native deck."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RUN_DIR = Path(__file__).resolve().parent
ASSET_DIR = RUN_DIR / "diagram-assets-redrawn"
ASSET_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1200, 2000

NAVY = (13, 25, 44)
NAVY_2 = (20, 43, 69)
TEAL = (0, 198, 164)
ACCENT = (0, 154, 131)
DARK_TEAL = (0, 138, 118)
LIGHT_TEAL = (226, 248, 243)
GOLD = (247, 182, 64)
GOLD_2 = (242, 168, 59)
CORAL = (226, 97, 112)
WHITE = (255, 255, 255)
INK = (24, 36, 52)
SOFT = (248, 245, 238)
MUTED = (92, 105, 122)
PAPER = (250, 247, 240)

FONT = Path("/usr/share/fonts/opentype/tlwg/Loma.otf")
FONT_BOLD = Path("/usr/share/fonts/opentype/tlwg/Loma-Bold.otf")


def f(size: int, bold: bool = False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size=size)


def canvas():
    img = Image.new("RGBA", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        r = int(PAPER[0] * (1 - t) + (242, 238, 230)[0] * t)
        g = int(PAPER[1] * (1 - t) + (242, 238, 230)[1] * t)
        b = int(PAPER[2] * (1 - t) + (242, 238, 230)[2] * t)
        draw.line((0, y, W, y), fill=(r, g, b))
    # faint grid like a whiteboard sketch
    for x in range(0, W, 80):
        draw.line((x, 0, x, H), fill=(235, 231, 223, 40), width=1)
    for y in range(0, H, 80):
        draw.line((0, y, W, y), fill=(235, 231, 223, 40), width=1)
    return img, draw


def glow(img, x, y, radius, color, alpha=120):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(radius / 2.2))
    img.alpha_composite(layer)


def sketch_round(draw, box, radius, fill, outline=None, width=2):
    # Slightly imperfect duplicate strokes create a hand-drawn feel.
    for dx, dy in [(0, 0), (2, -1)]:
        draw.rounded_rectangle(
            (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy),
            radius=radius,
            fill=fill,
            outline=outline or INK,
            width=width,
        )


def rounded(draw, box, radius, fill, outline=None, width=1):
    sketch_round(draw, box, radius, fill, outline, width)


def card(draw, box, title, subtitle, *, fill=(255, 255, 255, 242), title_color=INK,
         subtitle_color=MUTED, radius=36, title_size=34, subtitle_size=20, accent=None):
    rounded(draw, box, radius, fill, outline=(255, 255, 255, 90), width=2)
    x1, y1, x2, y2 = box
    if accent:
        rounded(draw, (x1 + 30, y1 + 30, x1 + 110, y1 + 110), 28, accent)
    draw.text((x1 + 30, y1 + 130), title, font=f(title_size, True), fill=title_color)
    draw.multiline_text((x1 + 30, y1 + 185), subtitle, font=f(subtitle_size), fill=subtitle_color, spacing=8)


def small_label(draw, xy, text, fill=WHITE, size=20, bold=False, anchor="la"):
    draw.text(xy, text, font=f(size, bold), fill=fill, anchor=anchor)


def dot_line(draw, pts, color, width=6, dash=18):
    for a, b in zip(pts, pts[1:]):
        x1, y1 = a
        x2, y2 = b
        length = math.hypot(x2 - x1, y2 - y1)
        steps = max(1, int(length / dash))
        for i in range(steps):
            t1 = i / steps
            t2 = min(1, (i + 0.5) / steps)
            sx = x1 + (x2 - x1) * t1
            sy = y1 + (y2 - y1) * t1
            ex = x1 + (x2 - x1) * t2
            ey = y1 + (y2 - y1) * t2
            draw.line((sx, sy, ex, ey), fill=color, width=width)


def arrow(draw, p1, p2, color, width=8, head=24):
    draw.line((*p1, *p2), fill=color, width=width)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    left = (p2[0] - head * math.cos(ang) + head * 0.55 * math.sin(ang),
            p2[1] - head * math.sin(ang) - head * 0.55 * math.cos(ang))
    right = (p2[0] - head * math.cos(ang) - head * 0.55 * math.sin(ang),
             p2[1] - head * math.sin(ang) + head * 0.55 * math.cos(ang))
    draw.polygon([p2, left, right], fill=color)


def center_robot(draw, cx, cy, scale=1.0, ring=GOLD, core=TEAL):
    r = int(160 * scale)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=core, outline=ring, width=10)
    draw.ellipse((cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16), outline=(255, 255, 255, 30), width=2)
    head_w = int(140 * scale)
    head_h = int(102 * scale)
    rounded(draw, (cx - head_w // 2, cy - head_h // 2 - 8, cx + head_w // 2, cy + head_h // 2 - 8),
            42, fill=(245, 248, 250), outline=(255, 255, 255, 80), width=2)
    rounded(draw, (cx - 74, cy - 20, cx + 74, cy + 36), 28, fill=INK)
    draw.ellipse((cx - 34, cy - 5, cx - 12, cy + 17), fill=LIGHT_TEAL)
    draw.ellipse((cx + 12, cy - 5, cx + 34, cy + 17), fill=LIGHT_TEAL)
    draw.line((cx, cy - 70, cx, cy - 110), fill=WHITE, width=10)
    draw.ellipse((cx - 14, cy - 122, cx + 14, cy - 94), fill=WHITE)


def build_cover():
    img, draw = canvas()
    glow(img, 220, 520, 250, TEAL, 160)
    glow(img, 980, 620, 260, GOLD, 140)
    glow(img, 620, 1460, 240, ACCENT, 120)
    rounded(draw, (120, 250, 1080, 1780), 80, fill=(12, 26, 43, 80), outline=(255, 255, 255, 28), width=2)
    card(draw, (120, 250, 1080, 1780), "Agent-native", "The app becomes a shared surface, not a silo.",
         fill=(255, 255, 255, 18), title_color=WHITE, subtitle_color=LIGHT_TEAL, radius=80,
         title_size=42, subtitle_size=24)
    center_robot(draw, 600, 1020, scale=1.25)
    # floating cards
    for box, t, s, a in [
        ((160, 360, 390, 580), "Files", "Local context\nbrand rules\nproject notes", TEAL),
        ((425, 290, 775, 520), "Memory", "What the agent should\nremember across sessions", GOLD),
        ((825, 380, 1040, 610), "Tools", "MCP\nCLI\nAPI", CORAL),
        ((160, 1320, 390, 1540), "Browser", "Shared view\nof the live app", ACCENT),
        ((445, 1490, 760, 1700), "Surface", "Canvas, docs, sheets\nthat both sides can edit", TEAL),
        ((830, 1270, 1040, 1510), "Write-back", "Outputs become\nfuture context", GOLD_2),
    ]:
        rounded(draw, box, 34, fill=(255, 255, 255, 238), outline=(255, 255, 255, 120), width=2)
        x1, y1, x2, y2 = box
        rounded(draw, (x1 + 24, y1 + 24, x1 + 84, y1 + 84), 20, fill=a)
        draw.text((x1 + 108, y1 + 34), t, font=f(30, True), fill=INK)
        draw.multiline_text((x1 + 108, y1 + 92), s, font=f(18), fill=MUTED, spacing=6)
    # connectors
    for pts, c in [
        ([(390, 470), (490, 610), (540, 810)], TEAL),
        ([(775, 390), (690, 640), (640, 850)], GOLD),
        ([(825, 500), (780, 730), (730, 900)], ACCENT),
        ([(390, 1430), (500, 1300), (560, 1210)], TEAL),
        ([(830, 1410), (770, 1290), (720, 1210)], GOLD_2),
    ]:
        dot_line(draw, pts, c, width=6, dash=18)
    for i, label in enumerate(["Cursor", "Codex", "MCP", "Browser", "Memory"]):
        x = 220 + i * 175
        rounded(draw, (x - 70, 1820, x + 70, 1888), 24, fill=(255, 255, 255, 16), outline=(255, 255, 255, 30), width=2)
        draw.text((x, 1854), label, font=f(20, True), fill=WHITE, anchor="mm")
    img.convert("RGB").save(ASSET_DIR / "hero-architecture.jpg", quality=95)


def build_inversion():
    img, draw = canvas()
    rounded(draw, (110, 130, 1090, 920), 60, fill=(255, 255, 255, 20), outline=(255, 255, 255, 30), width=2)
    rounded(draw, (110, 1080, 1090, 1870), 60, fill=(255, 255, 255, 20), outline=(255, 255, 255, 30), width=2)
    small_label(draw, (160, 180), "APP WITH AN AGENT", WHITE, 30, True)
    small_label(draw, (160, 1130), "AGENT WITH AN APP", WHITE, 30, True)
    # top panel
    rounded(draw, (200, 290, 1000, 790), 44, fill=(247, 249, 250, 245), outline=(255, 255, 255, 80), width=2)
    rounded(draw, (250, 350, 560, 730), 34, fill=(18, 36, 58, 255))
    small_label(draw, (305, 405), "The app", WHITE, 26, True)
    small_label(draw, (305, 455), "Context stays inside\nthis product boundary.", LIGHT_TEAL, 18)
    rounded(draw, (640, 400, 900, 700), 34, fill=(255, 255, 255, 255), outline=(231, 236, 240, 255), width=2)
    center_robot(draw, 770, 535, scale=0.55)
    small_label(draw, (770, 650), "Embedded agent", INK, 20, True, anchor="mm")
    arrow(draw, (560, 545), (650, 545), TEAL, width=8)
    small_label(draw, (610, 507), "suggests", TEAL, 16, True, anchor="mm")
    # bottom panel
    rounded(draw, (200, 1240, 1000, 1740), 44, fill=(247, 249, 250, 245), outline=(255, 255, 255, 80), width=2)
    center_robot(draw, 430, 1490, scale=0.72)
    small_label(draw, (430, 1620), "User agent", WHITE, 20, True, anchor="mm")
    rounded(draw, (590, 1340, 930, 1635), 34, fill=(18, 36, 58, 255))
    small_label(draw, (645, 1390), "App surface", WHITE, 24, True)
    small_label(draw, (645, 1450), "The user brings the agent.\nThe app becomes a tool.", LIGHT_TEAL, 19)
    arrow(draw, (515, 1488), (585, 1488), GOLD, width=10)
    small_label(draw, (552, 1450), "acts on", GOLD, 16, True, anchor="mm")
    rounded(draw, (150, 1870, 1050, 1950), 26, fill=(255, 255, 255, 10))
    small_label(draw, (600, 1910), "Old: app contains the agent   |   New: agent contains the app surface",
                LIGHT_TEAL, 20, True, anchor="mm")
    img.convert("RGB").save(ASSET_DIR / "inversion-diagram.jpg", quality=95)


def build_reference():
    img, draw = canvas()
    glow(img, 570, 1040, 220, TEAL, 150)
    layers = [
        ("Context", "Files, briefs, brand rules", (220, 220, 230)),
        ("Agent loop", "Cursor / Codex / host", (18, 36, 58)),
        ("Tools", "MCP / CLI / API / Browser", TEAL),
        ("Shared surface", "Canvas, docs, sheets, app", GOLD),
        ("Memory", "What gets written back", CORAL),
    ]
    y = 280
    for i, (title, sub, fill) in enumerate(layers):
        rounded(draw, (170, y, 1030, y + 230), 42, fill=(255, 255, 255, 232), outline=(255, 255, 255, 80), width=2)
        rounded(draw, (220, y + 40, 320, y + 140), 28, fill=fill)
        draw.text((350, y + 50), title, font=f(34, True), fill=INK)
        draw.text((350, y + 100), sub, font=f(22), fill=MUTED)
        if i < len(layers) - 1:
            arrow(draw, (600, y + 230), (600, y + 280), TEAL if i == 0 else GOLD, width=10)
        y += 290
    center_robot(draw, 600, 1050, scale=0.72)
    small_label(draw, (600, 1260), "The loop compounds", WHITE, 28, True, anchor="mm")
    small_label(draw, (600, 1310), "Context feeds the agent, the agent uses tools,\nresults become future context.",
                LIGHT_TEAL, 18, anchor="mm")
    img.convert("RGB").save(ASSET_DIR / "reference-architecture.jpg", quality=95)


def build_tools():
    img, draw = canvas()
    center_robot(draw, 600, 1030, scale=1.1)
    small_label(draw, (600, 1235), "External action surface", WHITE, 28, True, anchor="mm")
    tool_specs = [
        ((170, 330, 450, 600), "MCP", "Connects to outside apps", TEAL),
        ((750, 330, 1030, 600), "CLI", "Local commands and scripts", GOLD),
        ((170, 1280, 450, 1550), "API", "Structured programmatic calls", CORAL),
        ((750, 1280, 1030, 1550), "Browser", "Human-visible web actions", ACCENT),
    ]
    for box, title, sub, accent in tool_specs:
        rounded(draw, box, 34, fill=(255, 255, 255, 238), outline=(255, 255, 255, 90), width=2)
        x1, y1, x2, y2 = box
        rounded(draw, (x1 + 28, y1 + 28, x1 + 108, y1 + 108), 24, fill=accent)
        draw.text((x1 + 128, y1 + 40), title, font=f(34, True), fill=INK)
        draw.multiline_text((x1 + 128, y1 + 96), sub, font=f(19), fill=MUTED, spacing=6)
    for p in [((450, 465), (510, 620), TEAL), ((750, 465), (690, 620), GOLD),
              ((450, 1415), (510, 1220), CORAL), ((750, 1415), (690, 1220), ACCENT)]:
        arrow(draw, p[0], p[1], p[2], width=8)
    rounded(draw, (250, 720, 950, 820), 30, fill=(255, 255, 255, 16))
    small_label(draw, (600, 770), "The app needs explicit tool paths, not an embedded chatbot.", LIGHT_TEAL, 24, True, anchor="mm")
    img.convert("RGB").save(ASSET_DIR / "tool-hub.jpg", quality=95)


def build_context():
    img, draw = canvas()
    glow(img, 570, 1210, 220, TEAL, 120)
    for i, (title, sub, accent) in enumerate([
        ("Docs", "Markdown, specs, decisions", TEAL),
        ("Assets", "Images, examples, brand files", GOLD),
        ("History", "Approved output and revisions", CORAL),
    ]):
        y = 260 + i * 250
        rounded(draw, (170, y, 1030, y + 190), 34, fill=(255, 255, 255, 236), outline=(255, 255, 255, 90), width=2)
        rounded(draw, (220, y + 36, 292, y + 108), 24, fill=accent)
        draw.text((332, y + 44), title, font=f(34, True), fill=INK)
        draw.text((332, y + 94), sub, font=f(20), fill=MUTED)
    for y in [456, 706]:
        arrow(draw, (600, y), (600, y + 68), TEAL, width=8)
    rounded(draw, (360, 980, 840, 1290), 42, fill=(18, 36, 58, 255))
    center_robot(draw, 600, 1140, scale=0.74)
    small_label(draw, (600, 1245), "Agent re-reads the context", WHITE, 24, True, anchor="mm")
    rounded(draw, (250, 1490, 950, 1720), 40, fill=(255, 255, 255, 236), outline=(255, 255, 255, 90), width=2)
    small_label(draw, (600, 1540), "Write-back is the moat", INK, 30, True, anchor="mm")
    small_label(draw, (600, 1595), "Every correction, decision, and approved asset becomes future context.", MUTED, 20, anchor="mm")
    img.convert("RGB").save(ASSET_DIR / "context-stack.jpg", quality=95)


def build_workflow():
    img, draw = canvas()
    center_robot(draw, 600, 1020, scale=0.95)
    rounded(draw, (380, 920, 820, 1120), 44, fill=(255, 255, 255, 240), outline=(255, 255, 255, 100), width=2)
    small_label(draw, (600, 970), "Shared surface", INK, 28, True, anchor="mm")
    small_label(draw, (600, 1020), "User and agent watch the same state", MUTED, 20, anchor="mm")
    # loop arrows
    pts = [(600, 560), (910, 820), (980, 1200), (710, 1510), (350, 1490), (210, 1110), (280, 770), (600, 560)]
    for a, b in zip(pts, pts[1:]):
        arrow(draw, a, b, TEAL if a[1] < 1000 else GOLD, width=8)
    for xy, txt, color in [((600, 460), "Watch", WHITE), ((980, 1040), "Correct", GOLD), ((250, 1320), "Compound", TEAL)]:
        draw.ellipse((xy[0]-88, xy[1]-88, xy[0]+88, xy[1]+88), fill=color if color != WHITE else (255,255,255,30), outline=color, width=4)
        small_label(draw, xy, txt, WHITE if color != WHITE else WHITE, 24, True, anchor="mm")
    rounded(draw, (170, 1760, 1030, 1885), 34, fill=(255, 255, 255, 18), outline=(255, 255, 255, 24), width=2)
    small_label(draw, (600, 1818), "Visible feedback turns automation into collaboration.", LIGHT_TEAL, 26, True, anchor="mm")
    img.convert("RGB").save(ASSET_DIR / "workflow-loop.jpg", quality=95)


def build_opportunity():
    img, draw = canvas()
    rounded(draw, (150, 220, 1050, 1630), 54, fill=(255, 255, 255, 16), outline=(255, 255, 255, 30), width=2)
    small_label(draw, (600, 270), "Best wedges have context + tool access", WHITE, 28, True, anchor="mm")
    # axes
    draw.line((300, 620, 300, 1460), fill=(255, 255, 255, 50), width=4)
    draw.line((300, 1460, 980, 1460), fill=(255, 255, 255, 50), width=4)
    small_label(draw, (230, 1030), "shared\ncontext", LIGHT_TEAL, 22, True, anchor="mm")
    small_label(draw, (650, 1545), "tool access", LIGHT_TEAL, 22, True, anchor="mm")
    boxes = [
        (350, 700, 580, 930, "Low value", "Hidden + hard to verify", (255,255,255,16)),
        (620, 700, 910, 930, "Strong wedge", "Visible + editable + repeatable", (0,201,167,55)),
        (350, 980, 580, 1210, "Weak wedge", "Repeatable but not visible", (255,255,255,16)),
        (620, 980, 910, 1210, "Strong wedge", "Shared surface where the agent can act", (255,184,0,55)),
    ]
    for x1, y1, x2, y2, t, s, fill in boxes:
        rounded(draw, (x1, y1, x2, y2), 28, fill=fill, outline=(255,255,255,80), width=2)
        draw.text((x1 + 20, y1 + 20), t, font=f(28, True), fill=WHITE)
        draw.multiline_text((x1 + 20, y1 + 80), s, font=f(18), fill=LIGHT_TEAL, spacing=6)
    rounded(draw, (420, 1280, 840, 1390), 30, fill=(255, 255, 255, 238), outline=(255, 255, 255, 90), width=2)
    small_label(draw, (630, 1338), "Pick the quadrant with repeated work and visible state.", INK, 24, True, anchor="mm")
    img.convert("RGB").save(ASSET_DIR / "opportunity-matrix.jpg", quality=95)


def main():
    build_cover()
    build_inversion()
    build_reference()
    build_tools()
    build_context()
    build_workflow()
    build_opportunity()
    print(f"Rendered assets to {ASSET_DIR}")


if __name__ == "__main__":
    main()
