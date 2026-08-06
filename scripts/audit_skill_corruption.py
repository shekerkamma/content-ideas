#!/usr/bin/env python3
"""Audit skill trees for zero-fill corruption and restore from ranked donors.

Zero-fill corruption is the damage pattern left by a failed WSL VHDX
migration: the file still exists with its original size, but every byte is
NUL. ``verify-recovery-skills.sh`` checks four named skills; this walks every
skill directory under the given roots.

Report-only by default. ``--apply`` writes, and only ever writes a healthy
donor over a file that is already fully NUL.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict

READ_LIMIT = 65536

# Regenerable or non-authoritative trees. Corruption here is noise: bytecode is
# rebuilt on import, caches are re-downloaded, and backups are superseded by
# whatever they were a backup of.
BYTECODE_PARTS = {"__pycache__"}
BYTECODE_SUFFIXES = {".pyc", ".pyo"}
VCS_PARTS = {".git", "node_modules"}


def classify(path: str) -> str:
    """Bucket a corrupt file so live breakage is never buried under noise."""
    parts = path.split(os.sep)
    if any(p in BYTECODE_PARTS for p in parts):
        return "bytecode"
    if os.path.splitext(path)[1] in BYTECODE_SUFFIXES:
        return "bytecode"
    if any("backup" in p.lower() or p.endswith("-archive") or p == "skills-archive" for p in parts):
        return "backup"
    if "cache" in parts or os.path.join("plugins", "cache") in path:
        return "cache"
    return "live"


def is_null_corrupt(path: str) -> bool:
    """True only for a non-empty file whose leading bytes are entirely NUL.

    A zero-byte file is not corrupt. ``b"".strip(b"\\x00")`` is ``b""``, so a
    naive check reports every empty file as damaged -- the size guard below is
    load-bearing, not defensive clutter.
    """
    try:
        if os.path.islink(path) or os.path.getsize(path) == 0:
            return False
        with open(path, "rb") as handle:
            return handle.read(READ_LIMIT).strip(b"\x00") == b""
    except OSError:
        return False


def is_healthy(path: str) -> bool:
    try:
        if os.path.islink(path) or os.path.getsize(path) == 0:
            return False
        with open(path, "rb") as handle:
            return handle.read(READ_LIMIT).strip(b"\x00") != b""
    except OSError:
        return False


def split_skill(path: str):
    """Return ``(skill_name, relpath_within_skill)`` for a file under ``*/skills/<name>/``."""
    parts = path.split(os.sep)
    for index in range(len(parts) - 1, -1, -1):
        if parts[index] == "skills" and index + 2 <= len(parts) - 1:
            return parts[index + 1], os.sep.join(parts[index + 2:])
    return None, None


def walk_skill_files(roots):
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in VCS_PARTS]
            if os.sep + "skills" + os.sep not in dirpath + os.sep:
                continue
            for name in filenames:
                yield os.path.join(dirpath, name)


def build_donor_index(roots):
    """Map ``(skill, rel) -> [healthy paths]`` across every scanned root."""
    index = defaultdict(list)
    for path in walk_skill_files(roots):
        if not is_healthy(path):
            continue
        skill, rel = split_skill(path)
        if skill:
            index[(skill, rel)].append(path)
    return index


def git_donor(repo: str, skill: str, rel: str):
    """Recover content from git history -- survives working-tree corruption."""
    spec = "*{}/{}".format(skill, rel.replace(os.sep, "/"))
    try:
        commit = subprocess.run(
            ["git", "-C", repo, "log", "--all", "--format=%H", "-1", "--", spec],
            capture_output=True, text=True, timeout=60,
        ).stdout.strip()
        if not commit:
            return None
        listed = subprocess.run(
            ["git", "-C", repo, "show", "--pretty=", "--name-only", commit, "--", spec],
            capture_output=True, text=True, timeout=60,
        ).stdout.strip().splitlines()
        if not listed:
            return None
        blob = subprocess.run(
            ["git", "-C", repo, "show", "{}:{}".format(commit, listed[0])],
            capture_output=True, timeout=60,
        )
        if blob.returncode != 0 or not blob.stdout.strip(b"\x00"):
            return None
        return commit[:7], listed[0], blob.stdout
    except (OSError, subprocess.SubprocessError):
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="*", default=[os.path.expanduser("~")],
                        help="directories to scan (default: $HOME)")
    parser.add_argument("--git-repo", action="append", default=[],
                        help="repo whose history may hold donors (repeatable)")
    parser.add_argument("--apply", action="store_true",
                        help="write restorations (default: report only)")
    parser.add_argument("--include", default="live",
                        choices=["live", "all"],
                        help="'live' hides bytecode/cache/backup noise")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    roots = [os.path.abspath(os.path.expanduser(r)) for r in (args.roots or [os.path.expanduser("~")])]
    corrupt = [p for p in walk_skill_files(roots) if is_null_corrupt(p)]
    if args.include == "live":
        corrupt = [p for p in corrupt if classify(p) == "live"]

    donors = build_donor_index(roots)
    results = []
    for path in sorted(corrupt):
        skill, rel = split_skill(path)
        entry = {"path": path, "skill": skill, "bucket": classify(path),
                 "donor": None, "donor_kind": None, "restored": False}
        candidates = [d for d in donors.get((skill, rel), []) if d != path]
        if candidates:
            entry["donor"], entry["donor_kind"] = candidates[0], "host-copy"
        else:
            for repo in args.git_repo:
                found = git_donor(repo, skill, rel or "")
                if found:
                    commit, gitpath, blob = found
                    entry["donor"] = "{}@{}:{}".format(repo, commit, gitpath)
                    entry["donor_kind"] = "git-history"
                    entry["_blob"] = blob
                    break

        if args.apply and entry["donor"] and is_null_corrupt(path):
            try:
                if entry["donor_kind"] == "git-history":
                    with open(path, "wb") as handle:
                        handle.write(entry.pop("_blob"))
                else:
                    with open(entry["donor"], "rb") as src, open(path, "wb") as dst:
                        dst.write(src.read())
                entry["restored"] = True
            except OSError as exc:
                entry["error"] = str(exc)
        entry.pop("_blob", None)
        results.append(entry)

    if args.json:
        json.dump(results, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        fixable = [r for r in results if r["donor"]]
        print("corrupt skill files: {} ({} with a donor)".format(len(results), len(fixable)))
        for r in results:
            state = "RESTORED" if r["restored"] else ("fixable" if r["donor"] else "no donor")
            print("  [{}] {}".format(state, r["path"]))
            if r["donor"]:
                print("        via {}: {}".format(r["donor_kind"], r["donor"]))
        if fixable and not args.apply:
            print("\nre-run with --apply to restore the {} fixable file(s)".format(len(fixable)))

    return 1 if any(r["bucket"] == "live" and not r["restored"] and not r["donor"] for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
