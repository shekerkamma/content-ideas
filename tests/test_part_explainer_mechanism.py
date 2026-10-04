"""Mechanism mode of skills/part-explainer-film (scripts/mechanism): the animated films.

Every rule here was written after a bug while nine mechanism films were built (2026-10-03):

- The cue resolver read "3.3" (a rail the narration says) as 3.3 x the scene and put a rail 47 s into a
  14 s scene; a cue "8" was read the same way. Spoken words now resolve first.
- The transcriber returned overlapping neighbours ("or" 9.20-9.36 s, "0.9" from 8.88 s); the caption
  builder sorts by start, so the burned-in line read "1.2 0.9. or". Every film had two to five such swaps.
- The site captions merged sentences across a dropped ellipsis ("100 volt spikes Yet every rail") and
  two cues overlapped where scenes share their 0.5 s tails; one cue came out with its end before its start.
- A composed second chain used an id-derived class with no CSS, and the error colour read as copper.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

MECH = Path(__file__).resolve().parents[1] / "skills" / "part-explainer-film" / "scripts" / "mechanism"
sys.path.insert(0, str(MECH))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, MECH / f"{name}.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


lib = _load("lib"); sys.modules["lib"] = lib   # specs import "lib"; another skill ships a "lib" package
make = _load("make"); deliver = _load("deliver")
WS = [{"text": "rails", "start": 1.0}, {"text": "3.3,", "start": 2.0}, {"text": "1.8", "start": 3.0},
      {"text": "rail", "start": 4.0}, {"text": "8", "start": 5.0}, {"text": "µs.", "start": 5.4}]


class Resolve(unittest.TestCase):
    def test_spoken_numbers_are_words_not_fractions(self):
        self.assertEqual(make.resolve("3.3", WS, 10), 2.0)
        self.assertEqual(make.resolve("8", WS, 10), 5.0)

    def test_nth_occurrence_and_forced_fraction(self):
        self.assertEqual(make.resolve("rail#2", WS, 10), 4.0)
        self.assertEqual(make.resolve("@0.5", WS, 10), 5.0)
        self.assertEqual(make.resolve(0.25, WS, 10), 2.5)

    def test_small_decimal_is_a_fraction_only_when_unspoken(self):
        self.assertEqual(make.resolve("0.4", WS, 10), 4.0)

    def test_micro_sign_survives_normalisation(self):
        self.assertEqual(make.resolve("µs", WS, 10), 5.4)

    def test_unspoken_cue_blocks(self):
        with self.assertRaises(SystemExit):
            make.resolve("volts", WS, 10)


class Align(unittest.TestCase):
    def test_overlapping_transcriber_times_come_out_in_order(self):
        heard = [{"word": "1.2", "start": 8.5, "end": 9.2}, {"word": "or", "start": 9.2, "end": 9.36},
                 {"word": "0.9.", "start": 8.88, "end": 10.06}]
        out = make.align("1.2 or 0.9.", heard)
        self.assertEqual([w["text"] for w in sorted(out, key=lambda w: w["start"])], ["1.2", "or", "0.9."])
        self.assertTrue(all(b["start"] >= a["end"] for a, b in zip(out, out[1:])))

    def test_captions_use_the_script_spelling_and_drop_tags(self):
        out = make.align("[thoughtful] SKU-3 holds... Then", [{"word": "SKU3", "start": 0, "end": .5},
                                                                {"word": "holds", "start": .5, "end": 1},
                                                                {"word": "then", "start": 1.8, "end": 2}])
        self.assertEqual([w["text"] for w in out], ["SKU-3", "holds", "Then"])


class Cues(unittest.TestCase):
    def w(self, text, s, e): return {"text": text, "start": s, "end": e}

    def test_a_dropped_ellipsis_pause_splits_the_cue(self):
        ws = [self.w("100", 0, .3), self.w("volt", .3, .6), self.w("spikes", .6, 1.0), self.w("Yet", 1.7, 1.9), self.w("every.", 1.9, 2.2)]
        self.assertEqual([c[2] for c in deliver.cues(ws)], ["100 volt spikes", "Yet every."])

    def test_no_cue_runs_past_max_words(self):
        ws = [self.w(f"w{i}", i * .2, i * .2 + .2) for i in range(30)]
        self.assertTrue(all(len(c[2].split()) <= 12 for c in deliver.cues(ws)))


class Primitives(unittest.TestCase):
    at = staticmethod(lambda cue: 1.0)

    def test_a_second_chain_keeps_unique_ids_and_the_frame_class(self):
        body, _, _ = lib.compose(lib.chain("f01", self.at, [("A",), ("B",)]), lib.chain("f01", self.at, [("C",), ("D",)], ns="c"))
        self.assertIn('id="f01c-n0"', body); self.assertIn('id="f01-n0"', body)
        self.assertNotIn('class="f01c-box"', body)

    def test_an_error_state_is_tinted_not_just_recoloured(self):
        _, _, tl = lib.chain("f01", self.at, [("A",), ("B",)], light=[(1, "x", "err")])
        self.assertIn("backgroundColor", tl); self.assertIn("borderWidth:4", tl)

    def test_micro_sign_is_shielded_from_uppercase(self):
        self.assertIn("text-transform:none", lib.E("8 µs"))


class Specs(unittest.TestCase):
    def test_every_spec_has_a_close_and_callable_builds(self):
        specs = sorted((MECH / "specs").glob("*.py"))
        self.assertGreaterEqual(len(specs), 9)
        for p in specs:
            mod = _load_spec(p)
            self.assertIn("close", mod.SCENES, p.name)
            for sid, sc in mod.SCENES.items():
                self.assertTrue(callable(sc["build"]) and sc["scene"], f"{p.name}:{sid}")


def _load_spec(p):
    spec = importlib.util.spec_from_file_location(p.stem.replace("-", "_"), p)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


if __name__ == "__main__":
    unittest.main()


class AnimatedDiagram(unittest.TestCase):
    """scripts/animate_diagram.py: written after a motion-off diff showed the diagram's own dashed paths
    turned solid, and after the fallback PNGs were found to be 1.1 MB of every 1.2 MB diagram."""

    def setUp(self):
        import json, tempfile
        self.ad = importlib.util.module_from_spec(s := importlib.util.spec_from_file_location("animate_diagram", MECH.parent / "animate_diagram.py"))
        s.loader.exec_module(self.ad)
        self.tmp = Path(tempfile.mkdtemp())
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200"><switch><foreignObject/>'
               '<image href="data:image/png;base64,AAAA" width="1" height="1"/></switch>'
               '<path d="M0 0 L10 0" fill="none" stroke="#000"/><path d="M0 5 L10 5" fill="none" stroke="#000" stroke-dasharray="3 3"/></svg>')
        (self.tmp / "d.svg").write_text(svg)
        json.dump({"svg": str(self.tmp / "d.svg"), "zones": {"Host  ·  control": {"x": 10, "y": 10, "w": 100, "h": 50}}}, open(self.tmp / "z.json", "w"))
        json.dump({"beats": [{"zones": ["Host · control"]}, {"zones": []}]}, open(self.tmp / "s.json", "w"))

    def test_fallback_pngs_dropped_and_zone_names_matched_across_spacing(self):
        out = self.tmp / "o.svg"; self.ad.build(self.tmp / "z.json", self.tmp / "s.json", out)
        t = out.read_text()
        self.assertNotIn("data:image/png", t)
        self.assertIn('class="dga-beat"', t)

    def test_motion_off_keeps_the_diagrams_own_dashes(self):
        out = self.tmp / "o.svg"; self.ad.build(self.tmp / "z.json", self.tmp / "s.json", out)
        t = out.read_text()
        self.assertIn('path:not([stroke-dasharray]) { stroke-dasharray: none !important; }', t)
        self.assertNotIn('path { animation: none !important; stroke-dasharray: none', t)

    def test_a_beat_zone_missing_from_the_diagram_blocks(self):
        import json
        json.dump({"beats": [{"zones": ["Nowhere"]}]}, open(self.tmp / "s.json", "w"))
        with self.assertRaises(SystemExit):
            self.ad.build(self.tmp / "z.json", self.tmp / "s.json", self.tmp / "o.svg")
