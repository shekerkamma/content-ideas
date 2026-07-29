#!/usr/bin/env python3
"""Rebuild the reviewed 44-slide decision deck through the native branded workflow."""

from __future__ import annotations

import os
import runpy
from pathlib import Path


RUN = Path(__file__).resolve().parents[1]
os.environ["DECK_CONTENT_FILE"] = "outputs/decision-deck-content.json"
os.environ["DECK_OUTPUT_FILE"] = (
    "client-package/semiconductor-channel-decision-deck-skillpipe-draft.pptx"
)
runpy.run_path(str(RUN / "build_deck.py"), run_name="__main__")
