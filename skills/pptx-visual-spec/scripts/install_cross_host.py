#!/usr/bin/env python3
"""Install the governed PPTX skills from repo sources into supported hosts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[3]
REGISTRY = SCRIPT.parents[1] / "references" / "skill-registry.json"
MARKER = ".content-ideas-install.json"


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    ignored_names = {MARKER, ".DS_Store"}
    files = (
        p
        for p in root.rglob("*")
        if p.is_file()
        and p.name not in ignored_names
        and p.suffix != ".pyc"
        and "__pycache__" not in p.parts
    )
    for path in sorted(files):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def host_root(
    name: str,
    config: dict[str, object],
    repo: Path,
    home: Path,
    windows_home: Path | None = None,
) -> Path:
    if "repo_relative" in config:
        return repo / str(config["repo_relative"])
    value = os.environ.get(str(config["env"]))
    if value:
        return Path(value).expanduser()
    if "windows_relative" in config:
        base = windows_home or (
            Path(os.environ["WINDOWS_USER_HOME"]).expanduser()
            if os.environ.get("WINDOWS_USER_HOME")
            else None
        )
        if base is None:
            raise ValueError(
                f"{name} needs --windows-home, WINDOWS_USER_HOME, or {config['env']}"
            )
        return base / str(config["windows_relative"])
    return home / str(config["default"])


def is_managed_copy(destination: Path, source: Path) -> bool:
    marker = destination / MARKER
    if not marker.is_file():
        return False
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return data.get("source") == str(source.resolve())


def remove_managed(destination: Path) -> None:
    if destination.is_symlink():
        destination.unlink()
    else:
        shutil.rmtree(destination)


def install_one(
    source: Path,
    destination: Path,
    mode: str,
    dry_run: bool,
    adopt_identical: bool,
    replace_unmanaged: bool = False,
    backup_root: Path | None = None,
) -> str:
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        return f"ERROR missing source: {source}"

    try:
        return _install_one(
            source,
            destination,
            mode,
            dry_run,
            adopt_identical,
            replace_unmanaged,
            backup_root,
        )
    except OSError as exc:
        return f"ERROR cannot update {destination}: {exc}"


def _install_one(
    source: Path,
    destination: Path,
    mode: str,
    dry_run: bool,
    adopt_identical: bool,
    replace_unmanaged: bool,
    backup_root: Path | None,
) -> str:

    exists = destination.exists() or destination.is_symlink()
    if exists and destination.is_symlink() and destination.resolve() == source.resolve():
        if mode == "symlink" and not destination.readlink().is_absolute():
            return f"ok {destination}"
        if dry_run:
            return f"would normalize {destination}"
        destination.unlink()
        exists = False

    if exists:
        managed = destination.is_dir() and is_managed_copy(destination, source)
        identical = destination.is_dir() and tree_hash(destination) == tree_hash(source)
        if not managed and not (adopt_identical and identical) and not replace_unmanaged:
            return f"CONFLICT unmanaged destination: {destination}"
        if dry_run:
            action = "backup and replace" if replace_unmanaged and not managed and not identical else "refresh"
            return f"would {action} {destination}"
        if replace_unmanaged and not managed and not identical:
            if backup_root is None:
                return f"ERROR backup root required to replace: {destination}"
            backup = backup_root / destination.as_posix().lstrip("/")
            backup.parent.mkdir(parents=True, exist_ok=True)
            if backup.exists() or backup.is_symlink():
                return f"ERROR backup already exists: {backup}"
            shutil.move(str(destination), str(backup))
        else:
            remove_managed(destination)

    if dry_run:
        return f"would install {source.name} -> {destination}"

    destination.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        relative = os.path.relpath(source, destination.parent)
        destination.symlink_to(relative, target_is_directory=True)
    else:
        shutil.copytree(source, destination, symlinks=False)
        marker = {"source": str(source.resolve()), "contract_version": "1.1"}
        (destination / MARKER).write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8")
    return f"installed {source.name} -> {destination}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", action="append", choices=["claude", "codex", "agents", "project-agents", "antigravity", "gemini-config", "all"])
    parser.add_argument("--mode", choices=["auto", "symlink", "copy"], default="auto")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--windows-home", type=Path, help="Windows user profile as a WSL path, such as /mnt/c/Users/name")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--adopt-identical", action="store_true", help="replace an identical unmanaged copy with the managed installation")
    parser.add_argument("--replace-unmanaged", action="store_true", help="back up and replace non-identical unmanaged destinations")
    parser.add_argument("--backup-root", type=Path, help="backup directory used with --replace-unmanaged")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo_root.resolve()
    registry = json.loads((repo / REGISTRY.relative_to(ROOT)).read_text(encoding="utf-8"))
    requested = args.host or list(registry["default_install_hosts"])
    hosts = list(registry["host_roots"]) if "all" in requested else list(dict.fromkeys(requested))
    mode = ("copy" if os.name == "nt" else "symlink") if args.mode == "auto" else args.mode
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = args.backup_root or args.home / ".local/state/content-ideas/pptx-skill-backups" / stamp
    failures = 0

    entries = [dict(registry["contract"], tier="contract", ownership="repo")]
    entries.extend(e for e in registry["skills"] if e["ownership"] != "external")
    for host in hosts:
        config = registry["host_roots"][host]
        try:
            root = host_root(host, config, repo, args.home, args.windows_home)
        except ValueError as exc:
            print(f"[{host}] ERROR {exc}")
            failures += 1
            continue
        host_mode = "copy" if config.get("copy_only") else mode
        for entry in entries:
            allowed = entry.get("install_hosts", registry["default_skill_hosts"])
            if host not in allowed:
                continue
            source = repo / entry["source"]
            destination = root / entry.get("install_name", entry["name"])
            result = install_one(
                source,
                destination,
                host_mode,
                args.dry_run,
                args.adopt_identical,
                args.replace_unmanaged,
                backup_root,
            )
            print(f"[{host}] {result}")
            failures += result.startswith(("ERROR", "CONFLICT"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
