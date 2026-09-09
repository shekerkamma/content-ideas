#!/usr/bin/env python3
"""Ask an MCP server what it actually exposes, and write the answer to disk.

Stdlib only. Speaks MCP JSON-RPC over Streamable HTTP, handling both a plain
JSON response body and an SSE-framed one.

Why this exists as a tool rather than a chat turn: a real server's tool list is
large. The local gbrain server answers `tools/list` with 96 tools; pasting
those schemas into a context window costs more than most of the work they will
ever do. This writes the full map to a file and prints a summary, so the map
can be grepped, diffed, and cited without ever being resident.

    probe_mcp.py servers                      # what is configured, no calls made
    probe_mcp.py probe --url URL [--bearer-env VAR] --out DIR
    probe_mcp.py probe --server NAME --out DIR
    probe_mcp.py show MAP.json [--grep TEXT] [--tool NAME]
    probe_mcp.py diff OLD.json NEW.json

`--bearer-env` names an environment variable; the token itself is never
accepted on the command line and never written into a capability map.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

PROTOCOL_VERSION = "2025-06-18"
REDACTED = "<redacted>"


class ProbeError(RuntimeError):
    pass


# --------------------------------------------------------------------------
# transport
# --------------------------------------------------------------------------

def _post(url: str, payload: dict, token: str | None, timeout: int, session: str | None):
    headers = {
        "Content-Type": "application/json",
        # Streamable HTTP servers may answer with either; ask for both so a
        # server that only speaks SSE does not 406 the probe.
        "Accept": "application/json, text/event-stream",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if session:
        headers["Mcp-Session-Id"] = session
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.headers.get("Mcp-Session-Id"), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        raise ProbeError(f"HTTP {e.code} from {url}: {body}") from None
    except urllib.error.URLError as e:
        raise ProbeError(f"cannot reach {url}: {e.reason}") from None


def _decode(raw: str) -> dict:
    """Accept a bare JSON body or an SSE `data:` frame."""
    raw = raw.strip()
    if not raw:
        raise ProbeError("empty response body")
    if raw.startswith("{"):
        return json.loads(raw)
    for line in raw.splitlines():
        if line.startswith("data:"):
            return json.loads(line.split(":", 1)[1].strip())
    raise ProbeError(f"unrecognised response framing: {raw[:200]}")


class Client:
    def __init__(self, url: str, token: str | None = None, timeout: int = 30):
        self.url, self.token, self.timeout = url, token, timeout
        self.session = None
        self._id = 0

    def rpc(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        payload = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params is not None:
            payload["params"] = params
        sid, raw = _post(self.url, payload, self.token, self.timeout, self.session)
        if sid:
            self.session = sid
        msg = _decode(raw)
        if "error" in msg:
            err = msg["error"]
            raise ProbeError(f"{method}: {err.get('code')} {err.get('message')}")
        return msg.get("result", {})

    def initialize(self) -> dict:
        return self.rpc("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "mcp-capability-probe", "version": "1.0"},
        })


# --------------------------------------------------------------------------
# configured-server discovery (reads config only; makes no calls)
# --------------------------------------------------------------------------

_TOML_SERVER = re.compile(r"^\s*\[mcp_servers\.([A-Za-z0-9_.-]+)\]\s*$")
_TOML_KV = re.compile(r'^\s*([a-z_]+)\s*=\s*"([^"]*)"\s*$')


def _from_mcp_json(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    out = []
    for name, cfg in (data.get("mcpServers") or {}).items():
        if not isinstance(cfg, dict):
            continue
        out.append({
            "name": name,
            "url": cfg.get("url") or cfg.get("serverUrl"),
            "transport": "http" if (cfg.get("url") or cfg.get("serverUrl")) else "stdio",
            "command": cfg.get("command"),
            "source": str(path),
        })
    return out


def _from_codex_toml(path: Path) -> list[dict]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out, cur = [], None
    for line in lines:
        m = _TOML_SERVER.match(line)
        if m:
            if cur:
                out.append(cur)
            cur = {"name": m.group(1), "url": None, "transport": "stdio",
                   "command": None, "source": str(path), "bearer_env": None}
            continue
        if cur is None:
            continue
        if line.strip().startswith("["):
            out.append(cur)
            cur = None
            continue
        kv = _TOML_KV.match(line)
        if kv:
            key, val = kv.groups()
            if key == "url":
                cur["url"], cur["transport"] = val, "http"
            elif key == "command":
                cur["command"] = val
            elif key == "bearer_token_env_var":
                cur["bearer_env"] = val
    if cur:
        out.append(cur)
    return out


def configured_servers(project: Path | None = None) -> list[dict]:
    home = Path.home()
    found: list[dict] = []
    for p in [home / ".claude.json", home / ".cursor" / "mcp.json",
              home / ".claude" / "mcp.json"]:
        if p.is_file():
            found += _from_mcp_json(p)
    if project:
        for p in [project / ".mcp.json", project / ".cursor" / "mcp.json"]:
            if p.is_file():
                found += _from_mcp_json(p)
    codex = home / ".codex" / "config.toml"
    if codex.is_file():
        found += _from_codex_toml(codex)
    seen, uniq = set(), []
    for s in found:
        key = (s["name"], s.get("url"), s.get("command"))
        if key not in seen:
            seen.add(key)
            uniq.append(s)
    return uniq


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_servers(args) -> int:
    servers = configured_servers(Path.cwd())
    if not servers:
        print("No MCP servers found in the config files this tool reads.")
        print("That is 'none configured here', not 'none exist' — a host may")
        print("inject servers at runtime that never appear on disk.")
        return 0
    print(f"{len(servers)} configured MCP server(s):\n")
    for s in servers:
        tgt = s.get("url") or s.get("command") or "?"
        auth = f"  auth:{s['bearer_env']}" if s.get("bearer_env") else ""
        print(f"  {s['name']:<24} {s['transport']:<6} {tgt}{auth}")
        print(f"  {'':<24} from {s['source']}")
    print("\nNo server was contacted. Probe one with:")
    print("  probe_mcp.py probe --server <name> --out ./capability-maps")
    return 0


def _resolve_server(name: str) -> dict:
    for s in configured_servers(Path.cwd()):
        if s["name"] == name:
            return s
    raise ProbeError(f"no configured server named {name!r}; run `servers` to list")


def cmd_probe(args) -> int:
    if args.server:
        cfg = _resolve_server(args.server)
        url = cfg.get("url")
        if not url:
            raise ProbeError(
                f"{args.server} is a {cfg['transport']} server. This probe speaks "
                f"HTTP only; a stdio server must be probed by its own host."
            )
        name = args.server
        bearer_env = args.bearer_env or cfg.get("bearer_env")
    else:
        url, name, bearer_env = args.url, args.name, args.bearer_env
        if not url:
            raise ProbeError("need --url or --server")
        name = name or re.sub(r"[^a-z0-9]+", "-", url.lower()).strip("-")[:40]

    token = None
    if bearer_env:
        token = os.environ.get(bearer_env)
        if not token:
            raise ProbeError(
                f"{bearer_env} is not set in this process. This is a credential "
                f"binding to resolve, not a server that is down."
            )

    client = Client(url, token, timeout=args.timeout)
    info = client.initialize()

    listings, counts = {}, {}
    for method, key in (("tools/list", "tools"),
                        ("resources/list", "resources"),
                        ("prompts/list", "prompts")):
        try:
            res = client.rpc(method)
            items = res.get(key, []) or []
            listings[key] = items
            counts[key] = len(items)
        except ProbeError as exc:
            listings[key] = []
            counts[key] = None
            listings.setdefault("_unsupported", {})[key] = str(exc)

    cap_map = {
        "name": name,
        "url": url,
        "probed_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "auth": {"bearer_env": bearer_env} if bearer_env else None,
        "server_info": info.get("serverInfo", {}),
        "protocol_version": info.get("protocolVersion"),
        "declared_capabilities": info.get("capabilities", {}),
        "counts": counts,
        "tools": listings.get("tools", []),
        "resources": listings.get("resources", []),
        "prompts": listings.get("prompts", []),
        "unsupported": listings.get("_unsupported", {}),
    }

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}.json"
    text = json.dumps(cap_map, indent=2, ensure_ascii=False)
    if token and token in text:  # belt and braces; the token is never stored
        text = text.replace(token, REDACTED)
    out_path.write_text(text + "\n", encoding="utf-8")

    si = cap_map["server_info"]
    print(f"server:   {si.get('name', name)} {si.get('version', '')}".rstrip())
    print(f"url:      {url}")
    print(f"protocol: {cap_map['protocol_version']}")
    for key in ("tools", "resources", "prompts"):
        n = counts[key]
        print(f"{key + ':':<10}{'unsupported' if n is None else n}")
    print(f"\nmap written: {out_path}  ({out_path.stat().st_size / 1024:.1f} KiB)")
    names = [t.get("name", "?") for t in cap_map["tools"]]
    if names:
        head = ", ".join(names[:12])
        print(f"tool names: {head}{' …' if len(names) > 12 else ''}")
    print("\nThe full schemas are on disk, deliberately not printed here.")
    print(f"  search:  probe_mcp.py show {out_path} --grep <text>")
    print(f"  one:     probe_mcp.py show {out_path} --tool <name>")
    return 0


def cmd_show(args) -> int:
    cap = json.loads(Path(args.map).read_text(encoding="utf-8"))
    tools = cap.get("tools", [])
    if args.tool:
        for t in tools:
            if t.get("name") == args.tool:
                print(json.dumps(t, indent=2, ensure_ascii=False))
                return 0
        print(f"no tool named {args.tool!r} in {args.map}", file=sys.stderr)
        print("Discovery is authoritative: if it is not here, the server is not "
              "exposing it, whatever the docs say.", file=sys.stderr)
        return 1
    needle = (args.grep or "").lower()
    hits = [t for t in tools
            if not needle
            or needle in t.get("name", "").lower()
            or needle in (t.get("description") or "").lower()]
    print(f"{len(hits)}/{len(tools)} tool(s) in {cap.get('name')}"
          + (f" matching {args.grep!r}" if needle else ""))
    for t in hits[: args.limit]:
        desc = " ".join((t.get("description") or "").split())[:90]
        print(f"  {t.get('name'):<34} {desc}")
    if len(hits) > args.limit:
        print(f"  … {len(hits) - args.limit} more (raise --limit)")
    return 0


def cmd_diff(args) -> int:
    old = json.loads(Path(args.old).read_text(encoding="utf-8"))
    new = json.loads(Path(args.new).read_text(encoding="utf-8"))
    o = {t.get("name"): t for t in old.get("tools", [])}
    n = {t.get("name"): t for t in new.get("tools", [])}
    added, removed = sorted(set(n) - set(o)), sorted(set(o) - set(n))
    changed = sorted(k for k in set(o) & set(n)
                     if json.dumps(o[k], sort_keys=True) != json.dumps(n[k], sort_keys=True))
    for label, items in (("+ added", added), ("- removed", removed),
                         ("~ changed", changed)):
        for name in items:
            print(f"{label}: {name}")
    if not (added or removed or changed):
        print("no change in the tool surface")
        return 0
    print(f"\n{len(added)} added, {len(removed)} removed, {len(changed)} changed")
    return 1 if removed else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("servers", help="list configured servers; contacts nothing")
    s.set_defaults(func=cmd_servers)

    p = sub.add_parser("probe", help="ask a server what it exposes")
    p.add_argument("--url")
    p.add_argument("--server", help="a name from `servers`")
    p.add_argument("--name")
    p.add_argument("--bearer-env", help="env var holding the bearer token")
    p.add_argument("--out", default="./capability-maps")
    p.add_argument("--timeout", type=int, default=30)
    p.set_defaults(func=cmd_probe)

    sh = sub.add_parser("show", help="search a saved map without loading it whole")
    sh.add_argument("map")
    sh.add_argument("--grep")
    sh.add_argument("--tool")
    sh.add_argument("--limit", type=int, default=40)
    sh.set_defaults(func=cmd_show)

    d = sub.add_parser("diff", help="what changed between two maps")
    d.add_argument("old")
    d.add_argument("new")
    d.set_defaults(func=cmd_diff)

    args = ap.parse_args(argv)
    try:
        return args.func(args)
    except ProbeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
