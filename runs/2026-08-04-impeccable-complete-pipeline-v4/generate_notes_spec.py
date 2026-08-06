#!/usr/bin/env python3
import json
import re
from pathlib import Path

run = Path(__file__).resolve().parent
text = (run / "slide-content.md").read_text(encoding="utf-8")
slides = []
for block in re.split(r"(?=^## Slide \d+:)", text, flags=re.M):
    match = re.search(r"^## Slide (\d+):", block, flags=re.M)
    notes = re.search(r"### Speaker Notes\n(.+?)(?=\n### |\Z)", block, flags=re.S)
    transition = re.search(r"### Transition\n(.+?)(?=\n## |\Z)", block, flags=re.S)
    if match and notes:
        body = notes.group(1).strip()
        if transition and transition.group(1).strip() != "End.":
            body += "\n\nTransition: " + transition.group(1).strip()
        slides.append({"slide": int(match.group(1)), "notes": body})
(run / "native-notes-spec.json").write_text(json.dumps({"slides": slides}, indent=2) + "\n", encoding="utf-8")
print(f"wrote {len(slides)} slide notes")
