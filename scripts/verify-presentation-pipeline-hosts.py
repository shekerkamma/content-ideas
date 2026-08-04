#!/usr/bin/env python3
"""Verify canonical presentation skills and their cross-host installations."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

BINARY_SUFFIXES = {
    ".gif", ".ico", ".jpeg", ".jpg", ".mp3", ".mp4", ".pdf", ".png",
    ".pptx", ".webp", ".woff", ".woff2",
}
EXAMPLE_LINK_PREFIXES = ("...", "charts/", "examples/", "image.png", "path/to/")


def files(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        rel = path.relative_to(root).as_posix()
        result[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def validate_source(skill_dir: Path, expected_name: str) -> list[str]:
    errors: list[str] = []
    manifest = skill_dir / "SKILL.md"
    if not manifest.is_file():
        return [f"missing {manifest}"]
    text = manifest.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append(f"invalid frontmatter boundary: {manifest}")
    else:
        header = text[4:text.find("\n---\n", 4)]
        name_match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", header)
        if not name_match or name_match.group(1).strip() != expected_name:
            errors.append(f"frontmatter name mismatch: {manifest}")
        if not re.search(r"(?m)^description:\s*(?:>|\S)", header):
            errors.append(f"missing description: {manifest}")

    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name == ".env" or path.suffix == ".pyc" or "__pycache__" in path.parts:
            errors.append(f"forbidden generated/secret file: {path}")
            continue
        if path.suffix.lower() not in BINARY_SUFFIXES and "node_modules" not in path.parts:
            data = path.read_bytes()
            if b"\0" in data:
                errors.append(f"invalid NUL byte: {path}")
            if path.suffix == ".py":
                try:
                    ast.parse(data.decode("utf-8"), filename=str(path))
                except Exception as exc:
                    errors.append(f"Python syntax error {path}: {exc}")
        if path.suffix == ".md":
            markdown = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", markdown):
                target = target.strip().split("#", 1)[0].split(" ", 1)[0].strip("<>")
                if not target or "://" in target or target.startswith(("/", "#", "mailto:") + EXAMPLE_LINK_PREFIXES):
                    continue
                if not (path.parent / target).exists():
                    errors.append(f"broken operational link {path}: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="config/presentation-pipeline-hosts.json")
    parser.add_argument("--skip-discovery", action="store_true")
    args = parser.parse_args()
    manifest_path = Path(args.manifest).resolve()
    contract = json.loads(manifest_path.read_text(encoding="utf-8"))
    canonical = Path(os.environ.get("CONTENT_IDEAS_SKILLS_ROOT", contract["canonical_root"]))
    hosts = dict(contract["hosts"])
    hosts["claude-code"] = os.environ.get("CLAUDE_SKILLS_ROOT", hosts["claude-code"])
    hosts["hermes-windows"] = os.environ.get("HERMES_SKILLS_ROOT", hosts["hermes-windows"])
    hosts["antigravity-windows"] = os.environ.get("ANTIGRAVITY_SKILLS_ROOT", hosts["antigravity-windows"])
    errors: list[str] = []

    for name in contract["skills"]:
        source = canonical / name
        errors.extend(validate_source(source, name))
        source_files = files(source)
        for host, root_value in hosts.items():
            target = Path(root_value) / name
            if not target.exists():
                errors.append(f"{host}: missing {target}")
            elif files(target) != source_files:
                errors.append(f"{host}: parity mismatch for {name}")

    node = shutil.which("node")
    if node:
        for name in contract["skills"]:
            for path in (canonical / name).rglob("*"):
                if path.suffix not in {".js", ".mjs"} or "node_modules" in path.parts:
                    continue
                proc = subprocess.run(
                    [node, "--check", str(path)], text=True, capture_output=True, check=False,
                )
                if proc.returncode:
                    errors.append(f"JavaScript syntax error {path}: {proc.stderr.strip()}")

    for name, path_value in contract.get("windows_runtime", {}).items():
        if not Path(path_value).is_file():
            errors.append(f"Windows runtime missing {name}: {path_value}")

    if not args.skip_discovery and shutil.which("hermes"):
        env = os.environ.copy()
        env["HERMES_HOME"] = str(Path(hosts["hermes-windows"]).parent)
        proc = subprocess.run(
            ["hermes", "skills", "list", "--source", "local", "--enabled-only"],
            text=True, capture_output=True, env=env, check=False,
        )
        if proc.returncode:
            errors.append(f"Hermes discovery failed: {proc.stderr.strip()}")
        else:
            for name in contract["skills"]:
                if name not in proc.stdout and name[:20] not in proc.stdout:
                    errors.append(f"Hermes discovery missing: {name}")

    status = "healthy" if not errors else "unhealthy"
    print(json.dumps({
        "status": status,
        "contract_version": contract["contract_version"],
        "skills": len(contract["skills"]),
        "hosts": {"canonical": str(canonical), **hosts},
        "errors": errors,
    }, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
