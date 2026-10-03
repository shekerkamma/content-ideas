"""Gates and measurements for skills/part-explainer-film.

Every rule here was written after a bug, while ten explainer films were built (2026-10-03):

- The spoken-word counter counted every acronym letter by letter and every number as one or two words,
  so a dense SKU-8 scene read 176 wpm (MIPI counted as four) and another 118 (3,840 counted as two), and
  two speed-tuning passes chased a counting error. MIPI is one word; 3,840 is five.
- The transcript comparison failed correct audio three ways: the transcriber writes "15" for "fifteen",
  splits "bus load" into "busload", and hears homophones ("poll" as "pole"). None is a voice error.
- The zone locator kept "&amp;" in zone names, skipped bus bars, and the scaffold missed names that differ
  only in spacing, so three storyboards blocked against their own diagrams.
- The script gate is the one thing between authored copy and paid voice; its planted-defect control
  (10 defects, exit 2) is pinned here so a later edit cannot quietly weaken it.
"""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "skills" / "part-explainer-film" / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


spoken = _load("spoken")
measure = _load("measure_voice")


class SpokenWords(unittest.TestCase):
    def test_numbers_count_as_their_spoken_words(self):
        for tok, n in [("3,840", 5), ("3.3", 3), ("1280", 5), ("28", 2), ("5", 1), ("100", 2)]:
            self.assertEqual(spoken.spoken_words(tok), n, tok)

    def test_acronyms_spelled_or_said(self):
        # LVDS and RGB are spelled letter by letter; MIPI and ASIC are said as words
        for tok, n in [("LVDS", 4), ("RGB", 3), ("MIPI", 1), ("ASIC", 1), ("SKU-3", 4)]:
            self.assertEqual(spoken.spoken_words(tok), n, tok)

    def test_tags_are_not_spoken(self):
        self.assertEqual(spoken.spoken_words("[thoughtful] One die."), 2)


class TranscriptNormalisation(unittest.TestCase):
    def test_spoken_numbers_become_digits(self):
        self.assertEqual(measure.norm("up to the fifteenth over a thirty day outage")[-3:], ["30", "day", "outage"])
        self.assertEqual(measure.norm("thirty-two hundred cycles"), ["3200", "cycles"])
        self.assertEqual(measure.norm("one hundred fourteen"), ["114"])
        self.assertEqual(measure.norm("fifteen")[0], measure.norm("15")[0])

    def test_homophones_and_transcriber_spellings_match(self):
        self.assertEqual(measure.norm("a pulse and a poll"), measure.norm("a pulse and a pole"))
        self.assertEqual(measure.norm("77 gigahertz"), measure.norm("77 ghz"))
        self.assertEqual(measure.norm("1.2 kilometres"), measure.norm("1.2 kilometers"))

    def test_part_names_split_the_same_way(self):
        self.assertEqual(measure.norm("SKU-3 must prove"), measure.norm("SKU3 must prove"))


DRAWIO = """<mxfile><diagram><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>
<mxCell id="z1" value="Sensing &amp;amp; math" style="rounded=0;verticalAlign=top;align=left;" vertex="1" parent="1"><mxGeometry x="40" y="100" width="300" height="200" as="geometry"/></mxCell>
<mxCell id="z2" value="Flight control  ·  hard real-time" style="rounded=0;verticalAlign=top;align=left;" vertex="1" parent="1"><mxGeometry x="360" y="100" width="300" height="200" as="geometry"/></mxCell>
<mxCell id="bus" value="&lt;b&gt;On-chip bus&lt;/b&gt;  ·  two masters" style="rounded=0;fillColor=#0A1628;" vertex="1" parent="1"><mxGeometry x="40" y="320" width="620" height="40" as="geometry"/></mxCell>
</root></mxGraphModel></diagram></mxfile>"""
SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="700" height="400" viewBox="0 0 700 400">'
       '<rect x="11" y="100" width="300" height="200"/><rect x="331" y="100" width="300" height="200"/></svg>')


class LocateAndScaffold(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "d.drawio").write_text(DRAWIO); (self.tmp / "d.svg").write_text(SVG)

    def locate(self):
        r = subprocess.run([sys.executable, str(SCRIPTS / "locate_zones.py"), str(self.tmp / "d.drawio"), str(self.tmp / "d.svg"),
                            "--out", str(self.tmp / "zones.json")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return json.load(open(self.tmp / "zones.json"))

    def test_offset_measured_and_names_unescaped(self):
        z = self.locate()
        self.assertEqual(z["offset"], [-29.0, 0.0])
        self.assertIn("Sensing & math", z["zones"])
        self.assertIn("On-chip bus", z["zones"])          # a bus bar, keyed by its bold lead name

    def test_scaffold_matches_names_that_differ_only_in_spacing(self):
        self.locate()
        sb = {"id": "t", "headline": "H", "lead": "L", "closing": {"title": "C", "body": "B"},
              "beats": [{"marks": [], "title": "T", "body": "B", "zones": ["Flight control · hard real-time"]}]}
        (self.tmp / "sb.json").write_text(json.dumps(sb))
        r = subprocess.run([sys.executable, str(SCRIPTS / "scaffold_scenes.py"), str(self.tmp / "sb.json"), "--zones", str(self.tmp / "zones.json"),
                            "--kicker", "K", "--out", str(self.tmp / "scenes.json")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        beat = json.load(open(self.tmp / "scenes.json"))["scenes"][1]
        self.assertEqual(beat["zones"], ["Flight control  ·  hard real-time"])   # stored as the diagram writes it


def _scenes(tmp, beat_narration, beat_label="Surges stop at the door"):
    d = {"part": "t", "kicker": "K", "headline": "One die turns a 28 V bus into four rails", "scenes": [
        {"id": "open", "kind": "open", "marks": [], "zones": [], "label": "A 28 V bus", "narration":
         "[thoughtful] Avionics power starts on a 28 volt bus. Yet every rail must come up in order.", "source": "A 28 V bus carries 80 V surges."},
        {"id": "b1", "kind": "beat", "marks": [], "zones": [], "label": beat_label, "narration": beat_narration,
         "source": "Input conditioning clamps surges and blocks reverse polarity with an ideal diode."},
        {"id": "close", "kind": "close", "marks": [], "zones": [], "label": "Still to prove", "narration":
         "[serious] None of this is silicon yet. Every figure is a target... [confident] Bring us your bus profile.", "source": "Pre-silicon."}]}
    p = Path(tmp) / "scenes.json"; p.write_text(json.dumps(d)); return p


class ScriptGate(unittest.TestCase):
    def run_gate(self, p):
        return subprocess.run([sys.executable, str(SCRIPTS / "gate_script.py"), str(p), "--wpm", "145"], capture_output=True, text=True)

    def test_clean_script_passes(self):
        tmp = tempfile.mkdtemp()
        r = self.run_gate(_scenes(tmp, "First, the surges stop at the door. The input stage clamps them, and refuses a reversed supply."))
        self.assertNotIn("FINDING b1", r.stdout)

    def test_planted_defects_are_each_caught(self):
        tmp = tempfile.mkdtemp()
        bad = ("[pause] [excited] It clamps at 47 volts — and is certified. "
               "Input conditioning clamps surges and blocks reverse polarity with an ideal diode.")
        r = self.run_gate(_scenes(tmp, bad, beat_label="Buck"))
        self.assertEqual(r.returncode, 2)
        for needle in ["pause tag", "not in", "dash in narration", "banned claim word", "number 47",
                       "echoes its source", "label has 1 words", "tags in one scene"]:
            self.assertIn(needle, r.stdout, needle)


if __name__ == "__main__":
    unittest.main()
