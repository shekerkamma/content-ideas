#!/usr/bin/env python3
"""Apply and verify this machine's model-routing policy across WSL and Windows hosts.

    host_setup.py apply            idempotent; safe to re-run
    host_setup.py verify [--live]  read-only; exit 1 if any check fails
                                   --live also makes real model calls (Hermes, dsh)

Policy (decided 2026-09-29; background in CLAUDE.md):
  * graphify extraction runs on Claude Sonnet 5.5 via `graphify-pro` (claude-cli).
  * CLIProxyAPI (Windows) is reachable from WSL at 127.0.0.1:8317 via
    cliproxy-forward.service; its gemini-api-key is the paid, credit-backed key by design.
  * Hermes Gemini goes only through the `cliproxyapi` provider (Antigravity, Pro plan):
    its .env blanks GOOGLE_API_KEY/GEMINI_API_KEY (loaded with override=True, which is
    what beats the paid key ~/.bashrc exports), and Antigravity-only model ids the proxy
    cannot route are replaced by gemini-3.5-flash.
  * GBrain runs on a no-billing key with gemini-embedding-2 / 3.8-flash / 3.5-flash-lite,
    and every host connects with its own bearer token.
Secrets are never written by this script and never printed: tokens are read from
each host's own config and reported only as pass/fail.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HOME = Path.home()
WIN = Path(os.environ.get("WIN_HOME", f"/mnt/c/Users/{os.environ.get('USER', 'sheke')}"))
GIT_BASH = "/mnt/c/Program Files/Git/bin/bash.exe"

HERMES_ENVS = [HOME / ".hermes/.env", WIN / "AppData/Local/hermes/.env"]
HERMES_CONFIGS = [HOME / ".hermes/config.yaml", WIN / "AppData/Local/hermes/config.yaml"]
DEAD_PROXY_IDS = ("gemini-3-flash-agent", "gemini-3.5-flash-low", "gemini-3.5-flash-extra-low")
LIVE_PROXY_ID = "gemini-3.5-flash"
GBRAIN_CONFIG = HOME / ".gbrain/config.json"
GBRAIN_MODELS = {"chat_model": "google:gemini-3.8-flash", "expansion_model": "google:gemini-3.5-flash-lite"}
GBRAIN_RECIPE = HOME / "gbrain/src/core/ai/recipes/google.ts"
GBRAIN_PATCH = REPO / "docs/patches/gbrain-0.42-google-recipe-models.patch"
PROXY_CONFIG = WIN / ".cli-proxy-api/config.yaml"
RULE_FILES = [HOME / ".claude/CLAUDE.md", HOME / ".codex/AGENTS.md", WIN / ".claude/CLAUDE.md",
              WIN / ".codex/AGENTS.md", WIN / ".gemini/GEMINI.md"]
BLANK_BLOCK = ("\n# Gemini goes through the cliproxyapi provider (Antigravity, Pro plan). These blank any\n"
               "# paid key inherited from the shell (~/.bashrc exports GEMINI_API_KEY); .env loads with override=True.\n"
               "GOOGLE_API_KEY=\nGEMINI_API_KEY=\n")


# ---------------------------------------------------------------- pure transforms (tested)
def blank_gemini_keys(text: str) -> str:
    """Drop every GOOGLE_API_KEY/GEMINI_API_KEY line, then append one blanking block."""
    kept = re.sub(r"^(?:export\s+)?(?:GOOGLE_API_KEY|GEMINI_API_KEY)=.*\n?", "", text, flags=re.M)
    kept = re.sub(r"\n# Gemini goes through the cliproxyapi provider.*\n# paid key inherited.*\n", "\n", kept)
    return kept.rstrip("\n") + "\n" + BLANK_BLOCK


def gemini_key_values(text: str) -> list[str]:
    return re.findall(r"^(?:export\s+)?(?:GOOGLE_API_KEY|GEMINI_API_KEY)=(.*)$", text, flags=re.M)


def replace_dead_ids(text: str) -> str:
    """Replace Antigravity-only ids CLIProxyAPI cannot route with one gemini-3.5-flash entry."""
    out, placed = [], LIVE_PROXY_ID in re.findall(r"^\s*-\s*(\S+)\s*$", text, flags=re.M)
    for line in text.split("\n"):
        m = re.match(r"^(\s*-\s*)(\S+)\s*$", line)
        if m and m.group(2) in DEAD_PROXY_IDS:
            if not placed:
                out.append(m.group(1) + LIVE_PROXY_ID)
                placed = True
            continue
        out.append(line)
    return "\n".join(out)


# ---------------------------------------------------------------- helpers
def env_value(path: Path, key: str) -> str | None:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(rf"\s*(?:export\s+)?{key}\s*[:=]\s*[\"']?([^\"'\s]+)", line)
            if m:
                return m.group(1)
    except FileNotFoundError:
        return None
    return None


def backup_once(path: Path) -> None:
    bak = path.with_name(path.name + ".bak-host-setup")
    if path.exists() and not bak.exists():
        shutil.copy2(path, bak)


def sh(cmd: list[str] | str, timeout: int = 120, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                          shell=isinstance(cmd, str), **kw)


def mcp_search(token: str, url: str = "http://127.0.0.1:3131/mcp") -> tuple[bool, str]:
    def rpc(body, sid=None):
        h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
             "Authorization": f"Bearer {token}"}
        if sid:
            h["mcp-session-id"] = sid
        r = urllib.request.urlopen(urllib.request.Request(url, json.dumps(body).encode(), h), timeout=60)
        t = r.read().decode()
        m = re.findall(r"data: (\{.*\})", t)
        return (json.loads(m[-1]) if m else (json.loads(t) if t.strip() else {})), r.headers.get("mcp-session-id")
    try:
        _, sid = rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "host-setup", "version": "1"}}})
        rpc({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
        b, _ = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                    "params": {"name": "search", "arguments": {"query": "DeepGrid", "limit": 1}}}, sid)
        ok = "result" in b and not b["result"].get("isError")
        return ok, "search OK" if ok else str(b)[:100]
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        return False, type(e).__name__


# ---------------------------------------------------------------- apply
def apply() -> int:
    for script in ("install-graphify-pro.sh", "install-cliproxy-forward.sh"):
        r = sh(["bash", str(REPO / "scripts" / script)], timeout=300)
        print(f"[{'ok' if r.returncode == 0 else 'FAIL'}] {script}")
        if r.returncode:
            print(r.stderr[-400:])
    for p in HERMES_ENVS:
        if p.parent.is_dir():
            backup_once(p)
            old = p.read_text(encoding="utf-8") if p.exists() else ""
            new = blank_gemini_keys(old)
            p.write_text(new, encoding="utf-8")
            print(f"[ok] hermes .env gemini keys blanked: {p}{'' if new != old else ' (unchanged)'}")
    for p in HERMES_CONFIGS:
        if p.exists():
            old = p.read_text(encoding="utf-8")
            new = replace_dead_ids(old)
            if new != old:
                backup_once(p)
                p.write_text(new, encoding="utf-8")
            print(f"[ok] hermes cliproxyapi model ids: {p}{'' if new != old else ' (unchanged)'}")
    if GBRAIN_CONFIG.exists():
        d = json.loads(GBRAIN_CONFIG.read_text())
        if any(d.get(k) != v for k, v in GBRAIN_MODELS.items()):
            backup_once(GBRAIN_CONFIG)
            d.update(GBRAIN_MODELS)
            GBRAIN_CONFIG.write_text(json.dumps(d, indent=2))
            os.chmod(GBRAIN_CONFIG, 0o600)
            print("[ok] gbrain chat/expansion models set (restart gbrain.service to load)")
        else:
            print("[ok] gbrain chat/expansion models (unchanged)")
    if GBRAIN_RECIPE.exists() and "gemini-embedding-2" not in GBRAIN_RECIPE.read_text():
        r = sh(["git", "-C", str(GBRAIN_RECIPE.parents[4]), "apply", str(GBRAIN_PATCH)])
        print(f"[{'ok' if r.returncode == 0 else 'FAIL'}] gbrain recipe patch applied {r.stderr.strip()[:200]}")
    print("Not automated (need secrets or a login): GBrain bearer tokens per host, the no-billing "
          "key in gbrain.service, and embedding migration. `verify` checks each of them.")
    return 0


# ---------------------------------------------------------------- verify
class Checks:
    def __init__(self):
        self.failed = 0

    def __call__(self, ok: bool, what: str, detail: str = "") -> None:
        self.failed += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {what}" + (f" — {detail}" if detail else ""))


def verify(live: bool) -> int:
    c = Checks()
    proxy_key = env_value(HOME / ".dsh/.credentials.yaml", "CLIPROXY_API_KEY") or ""
    # --- proxy + forwarder
    active = sh(["systemctl", "--user", "is-active", "cliproxy-forward.service"]).stdout.strip()
    c(active == "active", "WSL cliproxy-forward.service active", active)
    try:
        code = urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:8317/v1/models", headers={"Authorization": f"Bearer {proxy_key}"}), timeout=8).status
    except Exception as e:  # noqa: BLE001
        code = getattr(e, "code", type(e).__name__)
    c(code == 200, "WSL 127.0.0.1:8317 reaches CLIProxyAPI", f"HTTP {code}")
    paid = os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY", "")
    pk = re.search(r"gemini-api-key:\s*\n\s*-\s*api-key:\s*[\"']?([^\"'\s]+)", PROXY_CONFIG.read_text()) \
        if PROXY_CONFIG.exists() else None
    c(bool(pk) and bool(paid) and pk.group(1) == paid, "CLIProxyAPI gemini-api-key is the paid (credit-backed) key")
    # --- graphify-pro
    r = sh(["graphify-pro", "--check"])
    c(r.returncode == 0 and "claude-sonnet-5-5" in r.stdout, "WSL graphify-pro → claude-sonnet-5-5", r.stderr.strip()[:120])
    if Path(GIT_BASH).exists():
        r = sh([GIT_BASH, "-lc", "graphify-pro --check"])
        c(r.returncode == 0 and "claude-sonnet-5-5" in r.stdout, "Windows graphify-pro → claude-sonnet-5-5",
          (r.stdout + r.stderr).strip()[-120:])
    for f in RULE_FILES:
        if f.parent.is_dir():
            c(f.exists() and "graphify-pro" in f.read_text(encoding="utf-8"), f"graphify rule present: {f}")
    # --- hermes
    for p in HERMES_ENVS:
        if p.exists():
            vals = gemini_key_values(p.read_text(encoding="utf-8"))
            c(bool(vals) and all(v.strip() == "" for v in vals), f"Hermes .env blanks Gemini keys: {p}")
    for p in HERMES_CONFIGS:
        if p.exists():
            left = [i for i in DEAD_PROXY_IDS if re.search(rf"^\s*-\s*{re.escape(i)}\s*$", p.read_text(), re.M)]
            c(not left, f"Hermes cliproxyapi has no unroutable ids: {p}", ", ".join(left))
    # --- gbrain
    svc = sh(["systemctl", "--user", "show", "gbrain.service", "-p", "Environment"]).stdout
    gkey = (re.search(r"GOOGLE_GENERATIVE_AI_API_KEY=(\S+)", svc) or [None, ""])[1]
    c(bool(gkey) and gkey != paid, "GBrain service key is not the paid key")
    if GBRAIN_CONFIG.exists():
        d = json.loads(GBRAIN_CONFIG.read_text())
        want = dict(GBRAIN_MODELS, embedding_model="google:gemini-embedding-2")
        bad = {k: d.get(k) for k, v in want.items() if d.get(k) != v}
        c(not bad, "GBrain config.json models current", json.dumps(bad) if bad else "")
    c(GBRAIN_RECIPE.exists() and "gemini-embedding-2" in GBRAIN_RECIPE.read_text(), "GBrain recipe allows embedding-2")
    tokens = {}
    try:
        cj = json.loads((HOME / ".claude.json").read_text())
        for proj, pv in (cj.get("projects") or {}).items():
            g = (pv.get("mcpServers") or {}).get("gbrain")
            if g:
                tokens[f"Claude Code WSL ({Path(proj).name})"] = g["headers"]["Authorization"].split()[-1]
    except Exception:  # noqa: BLE001
        pass
    tokens["Codex WSL/Desktop"] = env_value(HOME / ".bashrc", "GBRAIN_REMOTE_TOKEN")
    tokens["Hermes WSL"] = env_value(HERMES_ENVS[0], "MCP_GBRAIN_API_KEY")
    tokens["Hermes Windows"] = env_value(HERMES_ENVS[1], "MCP_GBRAIN_API_KEY")
    try:
        g = json.loads((WIN / ".claude.json").read_text())["mcpServers"]["gbrain"]
        tokens["Claude Code Windows"] = g["headers"]["Authorization"].split()[-1]
    except Exception:  # noqa: BLE001
        tokens["Claude Code Windows"] = None
    if shutil.which("powershell.exe"):
        v = sh(["powershell.exe", "-NoProfile", "-Command",
                "[Environment]::GetEnvironmentVariable('MCP_GBRAIN_API_KEY','User')"]).stdout.strip()
        tokens["Antigravity (Windows user env)"] = v or None
    for host, tok in tokens.items():
        ok, why = mcp_search(tok) if tok else (False, "no token configured")
        c(ok, f"GBrain MCP from {host}", "" if ok else why)
    if shutil.which("powershell.exe"):
        r = sh(["powershell.exe", "-NoProfile", "-Command",
                "try{(Invoke-WebRequest -UseBasicParsing -TimeoutSec 5 http://127.0.0.1:3131/health).StatusCode}catch{'fail'}"])
        c(r.stdout.strip() == "200", "Windows reaches GBrain at 127.0.0.1:3131", r.stdout.strip())
    # --- live model calls
    if live:
        def hermes_answers(provider: str, model: str, windows: bool) -> bool:
            tok = f"TOK{random.randint(10000, 99999)}"
            q = f"Reply with exactly this token and nothing else: {tok}"
            if windows:
                cmd = ["powershell.exe", "-NoProfile", "-Command",
                       f"Set-Location $env:USERPROFILE; hermes chat -Q -q '{q}' --provider {provider} -m {model}"]
            else:
                cmd = ["hermes", "chat", "-Q", "-q", q, "--provider", provider, "-m", model]
            try:
                return tok in sh(cmd, timeout=240, cwd="/tmp").stdout
            except subprocess.TimeoutExpired:
                return False
        for win in (False, True):
            if win and not shutil.which("powershell.exe"):
                continue
            side = "Windows" if win else "WSL"
            c(hermes_answers("cliproxyapi", "gemini-3.8-flash-high", win), f"LIVE Hermes {side} cliproxyapi answers (Pro plan)")
            c(not hermes_answers("gemini", "gemini-3.8-flash", win), f"LIVE Hermes {side} built-in gemini is blocked (no paid key)")
        tok = f"TOK{random.randint(10000, 99999)}"
        r = sh(["dsh", "--profile", "headless", f"Reply with exactly this token and nothing else: {tok}"], timeout=240, cwd="/tmp")
        c(tok in r.stdout, "LIVE dsh default model answers")
    print(f"\n{'ALL CHECKS PASSED' if not c.failed else f'{c.failed} CHECK(S) FAILED'}")
    return 1 if c.failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["apply", "verify"])
    ap.add_argument("--live", action="store_true", help="verify: also make real model calls")
    a = ap.parse_args()
    return apply() if a.action == "apply" else verify(a.live)


if __name__ == "__main__":
    sys.exit(main())
