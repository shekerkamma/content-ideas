#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_DIR = ROOT / "blueprints"
OUT = ROOT / "qa" / "blueprint-audit.tsv"

REQUIRED = [
    "The Diagnostic",
    "The 30-Day Scope",
    "Tech Stack",
    "Build vs",
    "ROI Business Case",
    "Competitor Teardown",
    "Acceptance Criteria",
    "Data Architecture",
    "Deployment Sequencing",
    "Post-Launch Iteration",
]


def main() -> None:
    lines = [
        "\t".join(
            [
                "file",
                "bytes",
                "words",
                "required_sections_found",
                "missing_sections",
                "status",
            ]
        )
    ]

    for path in sorted(BLUEPRINT_DIR.glob("*_Master_Blueprint.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        found = [needle for needle in REQUIRED if needle.lower() in text.lower()]
        missing = [needle for needle in REQUIRED if needle not in found]
        words = len(text.split())
        if len(found) < 10 or words < 1800:
            status = "draft-needs-upgrade"
        elif words < 3000:
            status = "draft-needs-depth-review"
        else:
            status = "structure-ok-needs-evidence-review"
        lines.append(
            "\t".join(
                [
                    path.name,
                    str(path.stat().st_size),
                    str(words),
                    str(len(found)),
                    ", ".join(missing),
                    status,
                ]
            )
        )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
