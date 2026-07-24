#!/usr/bin/env python3
"""Audit cross-host browser MCP configuration without printing credentials."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


SECRET_PATTERNS = (
    re.compile(r"Bearer\s+[A-Za-z0-9._~-]{12,}"),
    re.compile(r"[?&](?:key|token|api_key)=(?!\$\{)[^\s\"']+", re.IGNORECASE),
    re.compile(r'"(?:apiKey|api_key|token|secret)"\s*:\s*"(?!\$\{)[^\"]+"', re.IGNORECASE),
)


@dataclass
class Check:
    name: str
    status: str
    detail: str


def parse_json_mcp_names(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return []
    servers = data.get("mcpServers", {})
    return sorted(servers) if isinstance(servers, dict) else []


def parse_toml_mcp_names(path: Path) -> list[str]:
    try:
        import tomllib

        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    servers = data.get("mcp_servers", {})
    return sorted(servers) if isinstance(servers, dict) else []


def parse_codex_mcp_names(path: Path) -> list[str]:
    """Combine persisted TOML entries with active managed/session entries."""
    names = set(parse_toml_mcp_names(path))
    if not shutil.which("codex"):
        return sorted(names)
    try:
        result = subprocess.run(
            ["codex", "mcp", "list"],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return sorted(names)
    for line in result.stdout.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+)\s{2,}", line)
        if match and match.group(1) != "Name":
            names.add(match.group(1))
    return sorted(names)


def parse_yaml_mcp_names(path: Path) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    names: list[str] = []
    in_section = False
    for line in lines:
        if line == "mcp_servers:":
            in_section = True
            continue
        if in_section and line and not line.startswith(" "):
            break
        match = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line) if in_section else None
        if match:
            names.append(match.group(1))
    return sorted(names)


def find_literal_secrets(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError:
        return False
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def tcp_status(host: str, port: int, timeout: float = 1.5) -> str:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "reachable"
    except OSError:
        return "unreachable"


def dns_status(host: str) -> tuple[str, str]:
    try:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, 443)})
    except OSError as exc:
        return "fail", exc.__class__.__name__
    return "pass", ",".join(addresses[:4])


def https_status(url: str) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "browser-mcp-doctor/1"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return "pass", str(response.status)
    except urllib.error.HTTPError as exc:
        return "reachable", str(exc.code)
    except OSError as exc:
        return "fail", exc.__class__.__name__


def playwright_runtime(repo: Path) -> tuple[str, str]:
    script = (
        "const fs=require('fs');const {chromium}=require('playwright');"
        "const p=chromium.executablePath();process.stdout.write(fs.existsSync(p)?p:'missing')"
    )
    try:
        result = subprocess.run(
            ["node", "-e", script],
            cwd=repo,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "fail", exc.__class__.__name__
    detail = result.stdout.strip() or result.stderr.strip().splitlines()[-1:][0]
    return ("pass" if result.returncode == 0 and detail != "missing" else "fail", detail)


def inventory(home: Path, windows_home: Path | None) -> dict[str, dict[str, Any]]:
    configs: dict[str, tuple[Path, Any]] = {
        "claude": (home / ".claude.json", parse_json_mcp_names),
        "codex": (home / ".codex/config.toml", parse_codex_mcp_names),
        "hermes": (home / ".hermes/config.yaml", parse_yaml_mcp_names),
    }
    if windows_home:
        configs["antigravity"] = (
            windows_home / ".gemini/config/mcp_config.json",
            parse_json_mcp_names,
        )
    output: dict[str, dict[str, Any]] = {}
    for host, (path, parser) in configs.items():
        output[host] = {
            "path": str(path),
            "exists": path.exists(),
            "servers": parser(path),
            "literal_secret_detected": find_literal_secrets(path),
        }
    return output


def run(args: argparse.Namespace) -> dict[str, Any]:
    home = Path(args.home).expanduser()
    windows_home = Path(args.windows_home) if args.windows_home else None
    checks: list[Check] = []

    dns_state, dns_detail = dns_status(args.site)
    checks.append(Check("dns", dns_state, dns_detail))
    http_state, http_detail = https_status(f"https://{args.site}/")
    checks.append(Check("https", http_state, http_detail))
    checks.append(
        Check(
            "wsl_interop",
            "pass" if Path("/proc/sys/fs/binfmt_misc/WSLInterop").exists() else "missing",
            "Windows binaries callable from WSL" if Path("/proc/sys/fs/binfmt_misc/WSLInterop").exists() else "not detected",
        )
    )
    checks.append(Check("wsl_cdp_9222", tcp_status("127.0.0.1", 9222), "127.0.0.1:9222"))
    runtime_state, runtime_detail = playwright_runtime(Path(args.repo))
    checks.append(Check("playwright_chromium", runtime_state, runtime_detail))

    return {
        "site": args.site,
        "checks": [asdict(check) for check in checks],
        "hosts": inventory(home, windows_home),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=os.getcwd())
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--windows-home")
    parser.add_argument("--site", default="genspark.ai")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = run(args)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for check in report["checks"]:
            print(f"{check['name']}: {check['status']} ({check['detail']})")
        for host, data in report["hosts"].items():
            servers = ", ".join(data["servers"]) or "none"
            secret = " literal-secret" if data["literal_secret_detected"] else ""
            print(f"{host}: {servers}{secret}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
