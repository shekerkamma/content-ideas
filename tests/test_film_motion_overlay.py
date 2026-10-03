"""Planner and cut detection for skills/film-motion-overlay.

Rules written after bugs on the five DG32 films (2026-10-03):

- Spoken numbers must find their card: "thirty-two hundred cycles" is the "~3,242 cycles" card.
- 25 of 234 first-pass targets were uppercase labels (table header rows, kickers, captions) that share
  words with the sentence but are never what it is about; the planner skips them.
- Build records drift from the encoded film (+0.13 s by slide 13), so slide cuts are measured from the
  film. The first detector used absolute darkness and fired every 2 s on a dark navy title slide; it now
  looks for a dip relative to both neighbours.
"""

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "skills" / "film-motion-overlay" / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


plan = _load("plan_overlay")


class NumberWords(unittest.TestCase):
    def test_spoken_numbers(self):
        self.assertIn("39", plan.numbers_in_words("latched within thirty-nine cycles"))
        self.assertIn("114", plan.numbers_in_words("a clock at one hundred fourteen megahertz"))
        self.assertIn("3200", plan.numbers_in_words("about thirty-two hundred cycles"))


class Planner(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "film.json").write_text(json.dumps({"segments": [{"slide": 1, "start": 0.0, "duration": 20.0}]}))
        (self.tmp / "f.vtt").write_text("WEBVTT\n\n00:00:01.000 --> 00:00:04.000\nEach row costs about thirty-two hundred cycles by analysis.\n\n"
                                       "00:00:05.000 --> 00:00:08.000\nWhat the design does is what matters.\n\n"
                                       "00:00:09.000 --> 00:00:12.000\nAnd nothing else changes here.\n")
        rows = [{"kind": "textbox", "slide": 1, "text": "Title of the slide", "bbox": [48, 40, 900, 60]},
                {"kind": "textbox", "slide": 1, "text": "~3,242 cycles per query row, analytic", "bbox": [700, 300, 300, 40]},
                {"kind": "shape", "slide": 1, "bbox": [690, 260, 330, 160]},
                {"kind": "textbox", "slide": 1, "text": "WHAT THE DESIGN DOES", "bbox": [60, 300, 400, 30]},
                {"kind": "textbox", "slide": 1, "text": "The design keeps the control core untouched", "bbox": [60, 420, 500, 40]}]
        (self.tmp / "i.ndjson").write_text("\n".join(json.dumps(r) for r in rows))

    def test_targets(self):
        r = subprocess.run([sys.executable, str(SCRIPTS / "plan_overlay.py"), "--film-json", str(self.tmp / "film.json"), "--vtt", str(self.tmp / "f.vtt"),
                            "--inspect", str(self.tmp / "i.ndjson"), "--out", str(self.tmp / "plan.json")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        moves = json.load(open(self.tmp / "plan.json"))["segments"][0]["moves"]
        self.assertEqual(moves[0]["target"]["bbox"], [690, 260, 330, 160])          # the spoken number finds the card, grown to it
        self.assertNotEqual((moves[1]["target"] or {}).get("text"), "WHAT THE DESIGN DOES")   # a header label is never a target
        self.assertIsNone(moves[2]["target"])                                      # nothing named: keep the framing


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not installed")
class Cuts(unittest.TestCase):
    def test_dark_title_slide_gives_no_false_cuts(self):
        tmp = Path(tempfile.mkdtemp()); parts = []
        for k, colour in enumerate(["0x0b1a2e", "0xf2f2f2", "0x0b1a2e"]):   # dark navy, white, dark navy: 4 s each
            p = tmp / f"s{k}.mp4"; parts.append(p)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c={colour}:s=320x180:d=4:r=30",
                            "-vf", "fade=t=in:st=0:d=0.25,fade=t=out:st=3.75:d=0.25", "-pix_fmt", "yuv420p", str(p)], check=True)
        (tmp / "l.txt").write_text("".join(f"file '{p}'\n" for p in parts))
        film = tmp / "film.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "l.txt"), "-c", "copy", str(film)], check=True)
        cuts = json.loads(subprocess.run([sys.executable, str(SCRIPTS / "find_cuts.py"), str(film)], capture_output=True, text=True, check=True).stdout)
        self.assertEqual(len(cuts), 2, cuts)
        for got, want in zip(cuts, [4.0, 8.0]):
            self.assertAlmostEqual(got, want, delta=0.1)


if __name__ == "__main__":
    unittest.main()
