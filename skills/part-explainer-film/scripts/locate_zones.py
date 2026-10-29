#!/usr/bin/env python3
"""Zone boxes of a draw.io diagram, in the coordinates of its exported SVG.
Reading-path markers are edge labels with no box of their own; render_frames.mjs finds them in the SVG.

draw.io translates the page on export, so .drawio geometry and SVG geometry differ by one
offset. It is measured, not assumed: every zone vertex is matched to the SVG <rect> of the
same width and height, and the most common offset wins. Fewer than two zones agreeing blocks.

Usage: locate_zones.py <diagram.drawio> <diagram.svg> --out zones.json
"""
import argparse, collections, html, json, re, sys, xml.etree.ElementTree as ET

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("drawio"); ap.add_argument("svg"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cells = list(ET.parse(a.drawio).getroot().iter("mxCell"))
    byid = {c.get("id"): c for c in cells}
    def absgeo(c):  # absolute geometry, summing vertex parents
        g = c.find("mxGeometry"); x, y = float(g.get("x", 0)), float(g.get("y", 0))
        p = byid.get(c.get("parent"))
        while p is not None and p.get("vertex") and p.find("mxGeometry") is not None:
            pg = p.find("mxGeometry"); x += float(pg.get("x", 0)); y += float(pg.get("y", 0)); p = byid.get(p.get("parent"))
        return x, y, float(g.get("width", 0)), float(g.get("height", 0))
    svg = open(a.svg, encoding="utf-8").read()
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not m: sys.exit("BLOCKED: SVG has no 0-origin viewBox")
    W, H = float(m.group(1)), float(m.group(2))
    rects = [tuple(map(float, r)) for r in re.findall(r'<rect x="([\d.-]+)" y="([\d.-]+)" width="([\d.]+)" height="([\d.]+)"', svg)]
    zones = {}
    for c in cells:
        if not c.get("vertex") or c.find("mxGeometry") is None: continue
        v = html.unescape(re.sub(r"<[^>]+>", "", c.get("value") or "")).strip()   # "Sensing &amp; math" is "Sensing & math"
        st = c.get("style") or ""
        if v and "verticalAlign=top" in st and "align=left" in st: zones[v] = absgeo(c)
        elif v and "fillColor=#0A1628" in st:   # a bus bar: keyed by its bold lead name ("On-chip bus  ·  two masters ...")
            lead = re.match(r"\s*<b>(.*?)</b>", html.unescape(c.get("value") or ""))
            if lead: zones[html.unescape(lead.group(1)).strip()] = absgeo(c)
    votes = collections.Counter()
    for x, y, w, h in zones.values():
        for rx, ry, rw, rh in rects:
            if abs(rw - w) < 0.6 and abs(rh - h) < 0.6: votes[(round(rx - x, 1), round(ry - y, 1))] += 1
    if not votes or votes.most_common(1)[0][1] < 2:
        sys.exit(f"BLOCKED: could not measure the drawio->svg offset ({dict(votes)}); zones found: {list(zones)}")
    (dx, dy), n = votes.most_common(1)[0]
    sh = lambda b: {"x": round(b[0] + dx, 1), "y": round(b[1] + dy, 1), "w": b[2], "h": b[3]}
    out = {"svg": a.svg, "width": W, "height": H, "offset": [dx, dy], "offset_votes": n,
           "zones": {k: sh(b) for k, b in zones.items()}}
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"{len(zones)} zones, offset {dx},{dy} ({n} zones agree) -> {a.out}")

if __name__ == "__main__":
    main()
