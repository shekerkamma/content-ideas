"""Block extraction and copy gate for skills/storyboard-to-carousel.

Rules written after bugs (2026-10-03):

- v1 pasted a cropped draw.io diagram and was rejected as unprofessional; v2 redraws each zone's blocks,
  so zone_blocks.py must find them. It first required a line break before a block's sub-line and silently
  dropped half the DG32-LITE blocks ("<b>3-phase PWM</b>  ·  dead-time"), then skipped blocks that nearly
  fill their zone ("Fault matrix", "PMU + RTC").
- The copy gate now checks each beat's hero figure and every close/CTA item like the body: it caught
  "certification" in a D100 call-to-action item on its first run.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "skills" / "storyboard-to-carousel" / "scripts"

DRAWIO = """<mxfile><diagram><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="1"/>
<mxCell id="frame" value="Package" style="verticalAlign=top;align=left;" vertex="1" parent="1"><mxGeometry x="0" y="0" width="1000" height="600" as="geometry"/></mxCell>
<mxCell id="z1" value="Motor drive" style="verticalAlign=top;align=left;" vertex="1" parent="1"><mxGeometry x="20" y="20" width="400" height="300" as="geometry"/></mxCell>
<mxCell id="z2" value="Fault logic" style="verticalAlign=top;align=left;" vertex="1" parent="1"><mxGeometry x="450" y="20" width="200" height="120" as="geometry"/></mxCell>
<mxCell id="b1" value="&lt;b&gt;3-phase PWM&lt;/b&gt;  ·  dead-time  ·  hardware brake" style="rounded=1;" vertex="1" parent="1"><mxGeometry x="40" y="60" width="160" height="60" as="geometry"/></mxCell>
<mxCell id="b2" value="&lt;b&gt;Timers × 2&lt;/b&gt;&lt;br&gt;32-bit" style="rounded=1;" vertex="1" parent="1"><mxGeometry x="220" y="60" width="160" height="60" as="geometry"/></mxCell>
<mxCell id="b3" value="&lt;b&gt;Fault matrix&lt;/b&gt;&lt;br&gt;maskable · latched" style="rounded=1;" vertex="1" parent="1"><mxGeometry x="455" y="25" width="190" height="110" as="geometry"/></mxCell>
</root></mxGraphModel></diagram></mxfile>"""


class ZoneBlocks(unittest.TestCase):
    def test_both_formats_and_a_block_that_fills_its_zone(self):
        tmp = Path(tempfile.mkdtemp()); (tmp / "d.drawio").write_text(DRAWIO)
        zones = {"offset": [0, 0], "width": 1000, "height": 600, "zones": {
            "Package": {"x": 0, "y": 0, "w": 1000, "h": 600}, "Motor drive": {"x": 20, "y": 20, "w": 400, "h": 300},
            "Fault logic": {"x": 450, "y": 20, "w": 200, "h": 120}}}
        (tmp / "zones.json").write_text(json.dumps(zones))
        r = subprocess.run([sys.executable, str(SCRIPTS / "zone_blocks.py"), str(tmp / "d.drawio"), "--zones", str(tmp / "zones.json")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        z = json.load(open(tmp / "zones.json"))["zones"]
        self.assertEqual([b["name"] for b in z["Motor drive"]["blocks"]], ["3-phase PWM", "Timers × 2"])   # innermost zone, both formats
        self.assertEqual(z["Motor drive"]["blocks"][0]["sub"], "dead-time · hardware brake")
        self.assertEqual([b["name"] for b in z["Fault logic"]["blocks"]], ["Fault matrix"])           # nearly fills its zone
        self.assertEqual(z["Package"]["blocks"], [])


def _carousel(tmp, **over):
    slides = [
        {"id": "cover", "kind": "cover", "title": "One die runs the motor loop", "body": "A drive usually splits its loop; SKU-1 keeps it on one die.", "source": "lead", "zones": [], "marks": []},
        {"id": "b1", "kind": "beat", "title": "The host stays out of the loop", "body": "The processor configures the loop but never sits in it.",
         "source": "The core runs at 200 MHz.", "zones": [], "marks": [], "stat": {"value": "200 MHz", "label": "RISC-V core"}},
        {"id": "close", "kind": "close", "title": "Still to prove", "body": "Pre-silicon.", "source": "Retention above 125 °C junction is open.", "zones": [], "marks": [],
         "items": ["ADC isolation from switching edges", "The 1 µs deadline under load", "Retention above 125 °C"]},
        {"id": "cta", "kind": "cta", "title": "Scope SKU-1 against your drive", "body": "Bring us your drive.", "source": "", "zones": [], "marks": [],
         "items": ["Motor and bus voltage", "Loop rate", "Feedback type"]}]
    for k, v in over.items():
        sid, field = k.split("__"); next(s for s in slides if s["id"] == sid)[field] = v
    p = Path(tmp) / "carousel.json"; p.write_text(json.dumps({"part": "t", "kicker": "K", "url": "x/products/sku-1", "slides": slides})); return p


class CopyGate(unittest.TestCase):
    def gate(self, p):
        return subprocess.run([sys.executable, str(SCRIPTS / "gate_carousel.py"), str(p)], capture_output=True, text=True)

    def test_clean_carousel_passes(self):
        r = self.gate(_carousel(tempfile.mkdtemp()))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_defects_in_stat_and_items_are_caught(self):
        p = _carousel(tempfile.mkdtemp(), b1__stat={"value": "47 V", "label": "Certified clamp"},
                      cta__items=["Motor", "Your certification path, and the very long list of every single other requirement that your programme sets"],
                      close__body="It clamps — always.")
        r = self.gate(p)
        self.assertEqual(r.returncode, 2)
        for needle in ["number 47 in stat", "banned word 'Certified' in stat label", "banned word 'certification' in item 2",
                       "item 2 has", "needs exactly 3 items", "dash in body"]:
            self.assertIn(needle, r.stdout, needle)


if __name__ == "__main__":
    unittest.main()
