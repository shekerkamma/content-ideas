#!/usr/bin/env python3
"""Preview wrapper that escapes $ signs for matplotlib."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/branded-pptx-deck/scripts"))

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.default"] = "regular"

import matplotlib.pyplot as plt

_orig_text = plt.Axes.text
def _safe_text(self, x, y, s, *args, **kwargs):
    if isinstance(s, str):
        s = s.replace("$", "\\$")
    return _orig_text(self, x, y, s, *args, **kwargs)
plt.Axes.text = _safe_text

from pathlib import Path
from preview_pptx import render

src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/reports/hyundai-deal-prep-uc05.pptx")
render(src, Path("docs/reports/_preview"))
