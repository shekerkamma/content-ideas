"""
Generate carousel background images programmatically using Pillow.
Dark tech aesthetic: gradients, grid lines, glow nodes, circuit traces.
All colors from tokens.json.
"""

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

random.seed(42)  # reproducible

OUT = Path(__file__).resolve().parent / "bg"
OUT.mkdir(exist_ok=True)

W, H = 1080, 1350

# Colors from tokens.json
PRIMARY    = (15, 23, 42)      # #0F172A
SECONDARY  = (30, 41, 59)      # #1E293B
ACCENT     = (34, 211, 238)    # #22D3EE
MUTED      = (148, 163, 184)   # #94A3B8
SUCCESS    = (16, 185, 129)    # #10B981
SURFACE    = (241, 245, 249)   # #F1F5F9


def radial_gradient(w, h, center, radius, inner_color, outer_color):
    """Create a radial gradient image."""
    img = Image.new("RGB", (w, h), outer_color)
    draw = ImageDraw.Draw(img)
    cx, cy = center
    for r in range(radius, 0, -1):
        t = r / radius
        color = tuple(int(inner_color[i] * (1 - t) + outer_color[i] * t) for i in range(3))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    return img


def draw_grid(draw, w, h, spacing=80, color=(30, 41, 59), width=1):
    """Draw a subtle grid pattern."""
    for x in range(0, w, spacing):
        draw.line([(x, 0), (x, h)], fill=color, width=width)
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=color, width=width)


def draw_nodes(img, draw, nodes, node_color, glow_color, glow_radius=30):
    """Draw glowing nodes at specified positions."""
    # Glow layer
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for x, y, r in nodes:
        glow_draw.ellipse([x - glow_radius, y - glow_radius,
                           x + glow_radius, y + glow_radius],
                          fill=(*glow_color, 25))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=glow_radius))

    # Composite glow
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img = Image.alpha_composite(img, glow)

    # Draw solid nodes on top
    draw2 = ImageDraw.Draw(img)
    for x, y, r in nodes:
        draw2.ellipse([x - r, y - r, x + r, y + r], fill=(*node_color, 200))
    return img


def draw_connections(draw, nodes, color, width=1):
    """Draw connecting lines between nearby nodes."""
    for i, (x1, y1, _) in enumerate(nodes):
        for j, (x2, y2, _) in enumerate(nodes):
            if i >= j:
                continue
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if dist < 350:
                alpha = max(0, min(255, int(255 * (1 - dist / 350) * 0.3)))
                draw.line([(x1, y1), (x2, y2)],
                          fill=(*color, alpha), width=width)


# ═══════════════════════════════════════════════════════════════
# BG 1: Cover — radial glow with grid + scattered nodes
# ═══════════════════════════════════════════════════════════════
def make_cover():
    img = radial_gradient(W, H, (W // 2, H // 3), 800, SECONDARY, PRIMARY)
    draw = ImageDraw.Draw(img)
    draw_grid(draw, W, H, spacing=80, color=(25, 35, 52), width=1)

    # Nodes
    nodes = [(random.randint(50, W - 50), random.randint(50, H - 50), random.randint(2, 5))
             for _ in range(25)]
    img = img.convert("RGBA")
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    # Connection lines first
    for i, (x1, y1, _) in enumerate(nodes):
        for j, (x2, y2, _) in enumerate(nodes):
            if i >= j:
                continue
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if dist < 300:
                opacity = int(40 * (1 - dist / 300))
                glow_draw.line([(x1, y1), (x2, y2)],
                               fill=(*ACCENT, opacity), width=1)

    # Node glows
    for x, y, r in nodes:
        for gr in range(30, 0, -1):
            alpha = int(20 * (1 - gr / 30))
            glow_draw.ellipse([x - gr, y - gr, x + gr, y + gr],
                              fill=(*ACCENT, alpha))
        glow_draw.ellipse([x - r, y - r, x + r, y + r],
                          fill=(*ACCENT, 180))

    glow = glow.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.alpha_composite(img, glow)

    # Bottom gradient fade (for pagination area)
    fade = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
    fade_draw = ImageDraw.Draw(fade)
    for i in range(200):
        alpha = int(180 * (i / 200))
        fade_draw.line([(0, i), (W, i)], fill=(*PRIMARY, alpha))
    img.paste(fade, (0, H - 200), fade)

    img.convert("RGB").save(OUT / "bg-cover.png", quality=95)
    print("  bg-cover.png")


# ═══════════════════════════════════════════════════════════════
# BG 2: Body — subtle diagonal lines + corner glow
# ═══════════════════════════════════════════════════════════════
def make_body_01():
    img = Image.new("RGB", (W, H), PRIMARY)
    draw = ImageDraw.Draw(img)

    # Diagonal lines
    for offset in range(-H, W + H, 60):
        color = (22, 30, 48)
        draw.line([(offset, 0), (offset + H, H)], fill=color, width=1)

    # Corner glow top-right
    img = img.convert("RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    cx, cy = W - 100, 200
    for r in range(400, 0, -2):
        alpha = int(15 * (1 - r / 400))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                          fill=(*ACCENT, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=20))
    img = Image.alpha_composite(img, glow)

    img.convert("RGB").save(OUT / "bg-body-01.png", quality=95)
    print("  bg-body-01.png")


# ═══════════════════════════════════════════════════════════════
# BG 3: Body — circuit board traces
# ═══════════════════════════════════════════════════════════════
def make_body_02():
    img = Image.new("RGB", (W, H), PRIMARY)
    img = img.convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Horizontal + vertical circuit traces
    trace_color = (*SECONDARY, 120)
    node_color = (*ACCENT, 60)

    for _ in range(40):
        x = random.randint(0, W)
        y = random.randint(0, H)
        length = random.randint(100, 400)
        if random.random() > 0.5:
            draw.line([(x, y), (x + length, y)], fill=trace_color, width=2)
            # Right-angle turn
            turn_len = random.randint(50, 200)
            draw.line([(x + length, y), (x + length, y + turn_len)],
                      fill=trace_color, width=2)
            # Node at junction
            draw.ellipse([x + length - 4, y - 4, x + length + 4, y + 4],
                         fill=node_color)
        else:
            draw.line([(x, y), (x, y + length)], fill=trace_color, width=2)
            turn_len = random.randint(50, 200)
            draw.line([(x, y + length), (x + turn_len, y + length)],
                      fill=trace_color, width=2)
            draw.ellipse([x - 4, y + length - 4, x + 4, y + length + 4],
                         fill=node_color)

    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=1))
    img = Image.alpha_composite(img, overlay)

    # Subtle bottom-left glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for r in range(500, 0, -3):
        alpha = int(10 * (1 - r / 500))
        glow_draw.ellipse([100 - r, H - 300 - r, 100 + r, H - 300 + r],
                          fill=(*ACCENT, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=30))
    img = Image.alpha_composite(img, glow)

    img.convert("RGB").save(OUT / "bg-body-02.png", quality=95)
    print("  bg-body-02.png")


# ═══════════════════════════════════════════════════════════════
# BG 4: Body — dot matrix / halftone
# ═══════════════════════════════════════════════════════════════
def make_body_03():
    img = Image.new("RGB", (W, H), PRIMARY)
    draw = ImageDraw.Draw(img)

    # Dot matrix
    spacing = 40
    for x in range(spacing, W, spacing):
        for y in range(spacing, H, spacing):
            # Fade based on distance from center-right
            dist = math.sqrt((x - W * 0.7) ** 2 + (y - H * 0.4) ** 2)
            max_dist = 800
            if dist < max_dist:
                size = max(1, int(3 * (1 - dist / max_dist)))
                opacity = int(60 * (1 - dist / max_dist))
                color = tuple(int(ACCENT[i] * opacity / 255 + PRIMARY[i] * (255 - opacity) / 255) for i in range(3))
                draw.ellipse([x - size, y - size, x + size, y + size], fill=color)
            else:
                draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=SECONDARY)

    img.save(OUT / "bg-body-03.png", quality=95)
    print("  bg-body-03.png")


# ═══════════════════════════════════════════════════════════════
# BG 5: Closer — dramatic centered glow
# ═══════════════════════════════════════════════════════════════
def make_closer():
    img = radial_gradient(W, H, (W // 2, H // 2), 700, (25, 40, 65), PRIMARY)
    draw = ImageDraw.Draw(img)

    # Subtle grid
    draw_grid(draw, W, H, spacing=120, color=(20, 30, 48), width=1)

    # Central glow
    img = img.convert("RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    cx, cy = W // 2, H // 2 - 50
    for r in range(500, 0, -2):
        alpha = int(20 * (1 - r / 500))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                          fill=(*ACCENT, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=40))
    img = Image.alpha_composite(img, glow)

    # Horizontal accent line
    line_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    line_draw = ImageDraw.Draw(line_layer)
    ly = H // 2 + 200
    for i in range(W):
        dist = abs(i - W // 2)
        if dist < 400:
            alpha = int(80 * (1 - dist / 400))
            line_draw.point((i, ly), fill=(*ACCENT, alpha))
            line_draw.point((i, ly + 1), fill=(*ACCENT, alpha))
    img = Image.alpha_composite(img, line_layer)

    img.convert("RGB").save(OUT / "bg-closer.png", quality=95)
    print("  bg-closer.png")


print("Generating backgrounds...")
make_cover()
make_body_01()
make_body_02()
make_body_03()
make_closer()
print(f"Done. Files in: {OUT}")
