#!/usr/bin/env python3
"""Initialize per-run deck design context without overwriting user files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, help="Deck run directory")
    parser.add_argument("--title", required=True, help="Reader-facing deck title")
    args = parser.parse_args()

    run_dir = Path(args.run)
    run_dir.mkdir(parents=True, exist_ok=True)
    brief_path = run_dir / "deck-brief.md"
    design_path = run_dir / "deck-design.json"
    template_profile_path = run_dir / "template-profile.json"

    created: list[Path] = []
    if not brief_path.exists():
        brief_path.write_text(
            (ASSETS_DIR / "deck-brief.template.md").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        created.append(brief_path)

    if not design_path.exists():
        design = json.loads(
            (ASSETS_DIR / "deck-design.template.json").read_text(encoding="utf-8")
        )
        design["deck"]["name"] = args.title
        design_path.write_text(
            json.dumps(design, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        created.append(design_path)

    if not template_profile_path.exists():
        template_profile_path.write_text(
            (ASSETS_DIR / "template-profile.template.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        created.append(template_profile_path)

    for path in created:
        print(f"created: {path}")
    for path in (brief_path, design_path, template_profile_path):
        if path not in created:
            print(f"kept existing: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
