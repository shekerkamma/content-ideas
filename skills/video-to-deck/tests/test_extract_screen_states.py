import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "extract_screen_states.py"
SPEC = importlib.util.spec_from_file_location("extract_screen_states", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class ScreenStateTests(unittest.TestCase):
    def test_parse_crop(self):
        self.assertEqual(MODULE.parse_crop("10,20,30,40"), (10, 20, 40, 60))
        with self.assertRaises(ValueError):
            MODULE.parse_crop("10,20,0,40")

    def test_selects_subtle_content_change_and_last_frame(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = []
            for index in range(3):
                image = Image.new("L", (100, 60), 20)
                if index >= 1:
                    for x in range(20, 80):
                        for y in range(20, 40):
                            image.putpixel((x, y), 220)
                path = Path(directory) / f"frame_{index}.png"
                image.save(path)
                paths.append(path)
            selected, deltas = MODULE.select_state_indices(paths, threshold=1.0, crop=None)
            self.assertEqual(selected, [0, 1, 2])
            self.assertGreater(deltas[1], 1.0)


if __name__ == "__main__":
    unittest.main()
