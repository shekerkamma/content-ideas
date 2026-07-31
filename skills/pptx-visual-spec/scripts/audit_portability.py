#!/usr/bin/env python3
"""Audit the PPTX skill registry and host installations for portability drift."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from install_cross_host import MARKER, REGISTRY, ROOT, host_root, select_entries, tree_hash


MACHINE_PATH = re.compile(r"/(?:home|Users|mnt/c/Users)/[^/]+", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", action="append", choices=["claude", "codex", "agents", "project-agents", "antigravity", "gemini-config", "all"])
    parser.add_argument("--skill", action="append", help="audit only the named registered skill; repeat for multiple skills")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--windows-home", type=Path, help="Windows user profile as a WSL path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo_root.resolve()
    registry_path = repo / REGISTRY.relative_to(ROOT)
    raw = registry_path.read_text(encoding="utf-8")
    registry = json.loads(raw)
    failures: list[str] = []

    if MACHINE_PATH.search(raw):
        failures.append(f"machine-specific path in registry: {registry_path}")

    try:
        sources = select_entries(registry, args.skill)
    except ValueError as exc:
        print(f"ERROR {exc}")
        return 1
    for entry in sources:
        source = repo / entry["source"]
        if not (source / "SKILL.md").is_file():
            failures.append(f"missing portable source: {source}")

    requested = args.host or []
    if requested:
        hosts = list(registry["host_roots"]) if "all" in requested else list(dict.fromkeys(requested))
        for host in hosts:
            try:
                root = host_root(
                    host,
                    registry["host_roots"][host],
                    repo,
                    args.home,
                    args.windows_home,
                )
            except ValueError as exc:
                failures.append(f"host root [{host}]: {exc}")
                continue
            for entry in sources:
                allowed = entry.get("install_hosts", registry["default_skill_hosts"])
                if host not in allowed:
                    continue
                source = repo / entry["source"]
                destination = root / entry.get("install_name", entry["name"])
                if not (destination.exists() or destination.is_symlink()):
                    failures.append(f"missing [{host}]: {destination}")
                elif destination.is_symlink():
                    if not destination.exists():
                        failures.append(f"broken link [{host}]: {destination}")
                    elif destination.resolve() != source.resolve():
                        failures.append(f"wrong source [{host}]: {destination} -> {destination.resolve()}")
                elif not (destination / MARKER).is_file():
                    failures.append(f"unmanaged copy [{host}]: {destination}")
                elif tree_hash(destination) != tree_hash(source):
                    failures.append(f"drifted copy [{host}]: {destination}")

    if failures:
        print("\n".join(failures))
        return 1
    scope = ", ".join(requested) if requested else "sources"
    print(f"portable registry: valid; audited: {scope}; sources: {len(sources)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
