#!/usr/bin/env python3
"""The blocks inside each zone of a draw.io diagram, as data a carousel can redraw natively and large.

A block is a vertex whose label starts with a bold name (<b>Name</b><br>sub-line); it belongs to the zone
whose box contains its centre. Reading order is top-to-bottom, left-to-right. Pasting the diagram itself
into a 1080-px slide left labels ~5 px tall on a phone; redrawn, a block's name is 30 px.
Usage: zone_blocks.py <diagram.drawio> --zones zones.json   (adds "blocks" to each zone in zones.json)
"""
import argparse, html, json, re, sys, xml.etree.ElementTree as ET

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("drawio"); ap.add_argument("--zones", required=True); a = ap.parse_args()
    z = json.load(open(a.zones)); dx, dy = z["offset"]
    cells = list(ET.parse(a.drawio).getroot().iter("mxCell")); byid = {c.get("id"): c for c in cells}
    def absgeo(c):
        g = c.find("mxGeometry"); x, y = float(g.get("x", 0)), float(g.get("y", 0)); p = byid.get(c.get("parent"))
        while p is not None and p.get("vertex") and p.find("mxGeometry") is not None:
            pg = p.find("mxGeometry"); x += float(pg.get("x", 0)); y += float(pg.get("y", 0)); p = byid.get(p.get("parent"))
        return x + dx, y + dy, float(g.get("width", 0)), float(g.get("height", 0))
    out = {k: [] for k in z["zones"]}
    for c in cells:
        if not c.get("vertex") or c.find("mxGeometry") is None: continue
        v = html.unescape(c.get("value") or "")
        # sub-line after a line break ("<b>SRAM</b><br>32 KB") or after a dot ("<b>3-phase PWM</b>  ·  dead-time"):
        # requiring the break silently dropped half the DG32-LITE blocks, 3-phase PWM and SAR ADC among them
        m = re.match(r"\s*<b>(.*?)</b>\s*(?:<br\s*/?>|·)?\s*(.*)$", v, re.S)
        if not m: continue
        x, y, w, h = absgeo(c); cx, cy = x + w / 2, y + h / 2
        home = [k for k, b in z["zones"].items() if b["x"] <= cx <= b["x"] + b["w"] and b["y"] <= cy <= b["y"] + b["h"] and (b["w"] * b["h"]) > w * h * 1.02]   # 1.5x skipped blocks that nearly fill their zone (Fault matrix, PMU + RTC)
        if not home: continue
        k = min(home, key=lambda k: z["zones"][k]["w"] * z["zones"][k]["h"])   # the innermost zone
        sub = re.sub(r"<[^>]+>", " ", m.group(2) or ""); sub = " ".join(sub.split())
        out[k].append({"name": " ".join(re.sub(r"<[^>]+>", " ", m.group(1)).split()), "sub": sub, "y": y, "x": x})
    for k, bl in out.items():
        bl.sort(key=lambda b: (round(b["y"] / 20), b["x"])); z["zones"][k]["blocks"] = [{"name": b["name"], "sub": b["sub"]} for b in bl]
    json.dump(z, open(a.zones, "w"), indent=1, ensure_ascii=False)
    print("; ".join(f"{k.split('·')[0].strip()}: {len(v)}" for k, v in out.items()))

if __name__ == "__main__":
    main()
