#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_DIR = ROOT / "gold-standard"
OUT = ROOT / "qa" / "implementation-depth-audit.tsv"

CHECKS = {
    "stack": ["Recommended stack", "Frontend", "Backend"],
    "architecture": ["Architecture", "Core agent loop", "Failure"],
    "schema_or_model": ["Database schema", "Data Architecture", "Table", "Domain"],
    "api_surface": ["API surface", "Method", "Path"],
    "integrations": ["Integration", "Integrations"],
    "folder_structure": ["Folder", "module structure", "services/"],
    "env_vars": ["Environment variables", "API_KEY", "DATABASE_URL"],
    "qa_edges": ["Acceptance Criteria", "Edge cases"],
    "deployment": ["Deployment Sequencing", "Smoke test", "Rollback"],
    "observability": ["Observability", "Logs", "Metrics", "Alerts"],
}


def present(text: str, needles: list[str]) -> bool:
    lower = text.lower()
    return any(needle.lower() in lower for needle in needles)


def main() -> None:
    lines = ["file\tpassed\tfailed\tstatus"]
    for path in sorted(BLUEPRINT_DIR.glob("*_Master_Blueprint.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        failed = [name for name, needles in CHECKS.items() if not present(text, needles)]
        passed = len(CHECKS) - len(failed)
        status = "implementation-reviewed" if not failed else "needs-implementation-depth"
        lines.append(f"{path.name}\t{passed}/{len(CHECKS)}\t{','.join(failed)}\t{status}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
