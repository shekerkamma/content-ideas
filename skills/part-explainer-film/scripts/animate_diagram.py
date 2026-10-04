#!/usr/bin/env python3
"""Animate a real draw.io architecture diagram for the web: signal flow on every connector and the
storyboard's reading path lit zone by zone, inside the SVG (runs as an <img>, no script).

Inputs are the ones the film already has: zones.json (locate_zones.py, the zone boxes in the SVG's own
coordinates; its "svg" names the source) and the story-architect storyboard (beat order and zones).
draw.io's base64 PNG label fallbacks are dropped (about 1.1 MB of a 1.2 MB file; browsers render the
foreignObject instead). Gate: with motion off the animated SVG must render pixel-identical to the source;
a first version reset the diagram's own dashed paths to solid, which only that diff caught.

Usage: animate_diagram.py <zones.json> <storyboard.json> <out.svg>
"""
import json, pathlib, re, sys

BEAT_S = 2.6                      # seconds each beat stays lit
ACCENT = "#b54708"                # the diagrams' own accent, which holds contrast on their light ground


def build(zones_json, storyboard_json, dest, slug="diagram"):
    zones = json.load(open(zones_json))
    src = pathlib.Path(zones["svg"])
    if not src.exists(): sys.exit(f"BLOCKED: {slug}: {src} missing")
    beats = json.load(open(storyboard_json))["beats"]
    svg = src.read_text(encoding="utf-8")
    # draw.io puts a base64 PNG of every label inside <switch>, after the foreignObject, for viewers that
    # cannot render HTML in SVG. Browsers render the foreignObject, so the PNGs (1.1 MB of a 1.2 MB file)
    # never show; the render is checked unchanged after removing them.
    svg, dropped = re.subn(r'<image\b[^>]*href="data:image/png;base64,[^"]*"[^>]*/>', "", svg)
    n = len(beats); total = n * BEAT_S; on = 100 / n
    norm = lambda t: re.sub(r"\s+", " ", t).strip()          # diagram names carry double spaces ("Flight control  ·  hard real-time")
    boxes = {norm(k): v for k, v in zones["zones"].items()}
    lit, missing = [], []
    for k, b in enumerate(beats):
        for z in b.get("zones", []):
            box = boxes.get(norm(z))
            if not box: missing.append(z); continue
            x, y, w, h = box["x"], box["y"], box["w"], box["h"]
            lit.append(f'<g class="dga-beat" style="animation-delay:{k * BEAT_S:.2f}s">'
                       f'<rect x="{x - 4}" y="{y - 4}" width="{w + 8}" height="{h + 8}" rx="12"/>'
                       f'<circle cx="{x + w - 18}" cy="{y + 18}" r="15"/><text x="{x + w - 18}" y="{y + 23.5}">{k + 1}</text></g>')
    if missing: sys.exit(f"BLOCKED: {slug}: beat zones not in zones.json: {sorted(set(missing))}")
    style = f"""<style>
path[fill="none"][stroke]:not([stroke="none"]):not([stroke-dasharray]) {{ stroke-dasharray: 7 6; animation: dga-flow 1.1s linear infinite; }}
path[fill="none"][stroke][stroke-dasharray] {{ animation: dga-flow 1.1s linear infinite; }}
@keyframes dga-flow {{ to {{ stroke-dashoffset: -13; }} }}
.dga-beat {{ opacity: 0; animation: dga-beat {total:.2f}s linear infinite both; }}
.dga-beat rect {{ fill: {ACCENT}; fill-opacity: .07; stroke: {ACCENT}; stroke-width: 3.5; }}
.dga-beat circle {{ fill: {ACCENT}; }}
.dga-beat text {{ fill: #fff; font: 700 17px Inter, Arial, sans-serif; text-anchor: middle; }}
@keyframes dga-beat {{ 0% {{ opacity: 0; }} {on * .08:.3f}% {{ opacity: 1; }} {on * .92:.3f}% {{ opacity: 1; }} {on:.3f}% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
@media (prefers-reduced-motion: reduce) {{ path {{ animation: none !important; }} path:not([stroke-dasharray]) {{ stroke-dasharray: none !important; }} .dga-beat {{ animation: none !important; opacity: 0; }} }}
</style>"""
    out = re.sub(r"(<svg\b[^>]*>)", r"\1" + style.replace("\\", "\\\\"), svg, count=1)
    out = out.replace("</svg>", '<g class="dga-path">' + "".join(lit) + "</g></svg>", 1) if out.rstrip().endswith("</svg>") else None
    if out is None: sys.exit(f"BLOCKED: {slug}: SVG does not end in </svg>")
    dest = pathlib.Path(dest)
    dest.write_text(out, encoding="utf-8")
    print(f"{slug}: {dropped} fallback PNGs dropped, {n} beats, {len(lit)} zone lights, {total:.0f} s loop -> {dest.name} (from {src.name})")
    return dest.name


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[3]).stem)
