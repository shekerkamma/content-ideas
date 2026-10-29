#!/usr/bin/env python3
"""Validate the contract-loop state layer and report what a cold run should do next.

Checks the four artifacts exist, that feature_list.json holds a binary status
per item, that every item names the check that decides it, and that the progress
log is being written.

Stdlib only. Exits 0 when the state layer is sound, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VALID_STATUS = {"passing", "failing"}
PLACEHOLDER = "replace me"


def check_feature_list(path: Path) -> tuple[list[str], list[str], list[dict]]:
    fails: list[str] = []
    warns: list[str] = []
    items: list[dict] = []

    if not path.is_file():
        return [f"missing {path.name}"], warns, items

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.name} is not valid JSON: {exc}"], warns, items

    if not isinstance(data, dict):
        return [f"{path.name} must be a JSON object"], warns, items

    raw_items = data.get("items")
    if not isinstance(raw_items, list):
        return [f"{path.name} has no `items` list"], warns, items
    if not raw_items:
        return [f"{path.name} has an empty `items` list"], warns, items

    seen_ids: set = set()
    for idx, item in enumerate(raw_items):
        label = f"item[{idx}]"
        if not isinstance(item, dict):
            fails.append(f"{label} is not an object")
            continue

        item_id = item.get("id")
        if item_id is None:
            fails.append(f"{label} has no `id`")
        elif item_id in seen_ids:
            fails.append(f"{label} duplicates id {item_id!r}")
        else:
            seen_ids.add(item_id)
            label = f"item {item_id}"

        name = str(item.get("name", "")).strip()
        if not name:
            fails.append(f"{label} has no `name`")
        elif PLACEHOLDER in name.lower():
            fails.append(f"{label} still holds the scaffold placeholder name")

        status = str(item.get("status", "")).strip().lower()
        if status not in VALID_STATUS:
            fails.append(
                f"{label} status is {status or '(empty)'!r} — must be exactly "
                f"'passing' or 'failing'. A third value is how a loop stops "
                f"being auditable."
            )

        verified_by = str(item.get("verified_by", "")).strip()
        if not verified_by:
            fails.append(
                f"{label} has no `verified_by` — if you cannot name the check "
                f"that decides, the item is written badly. Rewrite it."
            )
        elif PLACEHOLDER in verified_by.lower():
            fails.append(f"{label} still holds the scaffold placeholder verified_by")

        if "notes" not in item:
            warns.append(f"{label} has no `notes` field")

        items.append(item)

    return fails, warns, items


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Validate a graph-engineering state layer.",
    )
    ap.add_argument("--dir", default=".", help="Directory holding the state layer")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = ap.parse_args(argv)

    root = Path(args.dir).expanduser().resolve()
    fails: list[str] = []
    warns: list[str] = []

    fl_fails, fl_warns, items = check_feature_list(root / "feature_list.json")
    fails += fl_fails
    warns += fl_warns

    progress = root / "claude-progress.txt"
    if not progress.is_file():
        fails.append("missing claude-progress.txt")
    elif not progress.read_text(encoding="utf-8").strip():
        warns.append("claude-progress.txt is empty — a cold run learns nothing from it")

    init = root / "init.sh"
    if not init.is_file():
        warns.append("missing init.sh — every run will rediscover how to boot")
    elif not init.stat().st_mode & 0o111:
        warns.append("init.sh is not executable (chmod +x it)")

    if not (root / ".git").is_dir():
        warns.append("not a git repo — no history of the work")

    auditor = root / ".claude" / "agents" / "auditor.md"
    if not auditor.is_file():
        warns.append("missing .claude/agents/auditor.md — no critic installed")

    print(f"state layer: {root}\n")

    if items:
        passing = [i for i in items if str(i.get("status", "")).lower() == "passing"]
        failing = [i for i in items if str(i.get("status", "")).lower() == "failing"]
        print(f"  items:   {len(items)}  ({len(passing)} passing, {len(failing)} failing)")
        if failing:
            nxt = failing[0]
            print(f"  next:    [{nxt.get('id')}] {str(nxt.get('name', ''))[:70]}")
            print(f"  verify:  {str(nxt.get('verified_by', ''))[:70]}")
        else:
            print("  next:    nothing failing — every item passes")
        print()

    for f in fails:
        print(f"  [FAIL] {f}")
    for w in warns:
        print(f"  [WARN] {w}")

    blocking = fails or (warns if args.strict else [])
    if blocking:
        print(f"\nFAIL ({len(fails)} blocking, {len(warns)} advisory)")
        return 1

    if warns:
        print(f"\nPASS with {len(warns)} advisory finding(s).")
    else:
        print("PASS — a cold run can pick this up.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
