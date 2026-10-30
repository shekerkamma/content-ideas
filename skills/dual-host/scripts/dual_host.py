#!/usr/bin/env python3
"""Run one Claude Code change on both hosts (WSL and Windows) and show where they differ.

Stdlib only. Run from WSL. Windows is reached through /mnt/c and its claude.exe.

  dual_host.py paths                  show both hosts' claude binary, home and settings.json
  dual_host.py backup <label>         copy both settings.json to settings.json.bak-<label>
  dual_host.py claude -- <args...>    run `claude <args>` on WSL, then on Windows
  dual_host.py parity [--full]        compare plugins (id, version, enabled) and skill names

Environment: DUAL_HOST_WIN_HOME (default /mnt/c/Users/$USER),
DUAL_HOST_WIN_CLAUDE (default <win home>/.local/bin/claude.exe).
Exit: 0 ok, 1 a host failed or parity differs, 2 usage or a host is missing.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

WIN_HOME = Path(os.environ.get("DUAL_HOST_WIN_HOME", f"/mnt/c/Users/{os.environ.get('USER', '')}"))
HOSTS = {
    "wsl": {"home": Path.home(), "claude": shutil.which("claude") or "claude", "cwd": Path.home()},
    "windows": {"home": WIN_HOME,
                "claude": os.environ.get("DUAL_HOST_WIN_CLAUDE", str(WIN_HOME / ".local/bin/claude.exe")),
                # claude.exe must start from a Windows folder, not a \\wsl$ path
                "cwd": WIN_HOME},
}


def settings(host):
    return HOSTS[host]["home"] / ".claude" / "settings.json"


def run_claude(host, args, stdin=None):
    h = HOSTS[host]
    return subprocess.run([h["claude"], *args], cwd=h["cwd"], input=stdin,
                          capture_output=True, text=True, timeout=300)


def cmd_paths():
    ok = True
    for host, h in HOSTS.items():
        s = settings(host)
        exe = Path(h["claude"]).exists() or shutil.which(h["claude"]) is not None
        ok &= exe and s.exists()
        print(f"{host:8} claude={h['claude']} ({'found' if exe else 'MISSING'})")
        print(f"{'':8} settings={s} ({'found' if s.exists() else 'MISSING'})")
    return 0 if ok else 2


def cmd_backup(label):
    for host in HOSTS:
        s = settings(host)
        dest = s.with_name(f"settings.json.bak-{label}")
        if dest.exists():
            print(f"{host}: {dest} already exists; pick another label")
            return 2
        shutil.copy2(s, dest)
        json.loads(s.read_text(encoding="utf-8"))  # fail loudly if the source is already broken
        print(f"{host}: backed up to {dest}")
    return 0


def cmd_claude(args):
    if args and args[0] == "--":
        args = args[1:]
    if not args:
        print("usage: dual_host.py claude -- <claude args>")
        return 2
    stdin = None if sys.stdin.isatty() else sys.stdin.read()
    rc = 0
    for host in HOSTS:
        r = run_claude(host, args, stdin)
        print(f"===== {host}: claude {' '.join(args)} → exit {r.returncode}")
        print((r.stdout + r.stderr).strip()[-4000:])
        rc |= r.returncode != 0
    return rc


def plugins(host):
    r = run_claude(host, ["plugin", "list", "--json"])
    if r.returncode != 0:
        raise RuntimeError(f"{host}: claude plugin list failed: {r.stderr.strip()[:300]}")
    return {p["id"]: (p.get("version"), p.get("enabled")) for p in json.loads(r.stdout)}


def skills(host):
    d = HOSTS[host]["home"] / ".claude" / "skills"
    return {p.name for p in d.iterdir() if (p / "SKILL.md").exists()} if d.exists() else set()


def cmd_parity(full=False):
    try:
        pw, pn = plugins("wsl"), plugins("windows")
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as e:
        print(e)
        return 2
    differs = False
    print(f"Plugins: WSL {len(pw)}, Windows {len(pn)}, on both {len(pw.keys() & pn.keys())}")
    for pid in sorted(pw.keys() | pn.keys()):
        a, b = pw.get(pid), pn.get(pid)
        if a == b:
            continue
        differs = True
        fmt = lambda v: "—" if v is None else f"{v[0]} {'on' if v[1] else 'off'}"
        print(f"  {pid:55} WSL {fmt(a):18} Windows {fmt(b)}")
    sw, sn = skills("wsl"), skills("windows")
    print(f"Skills in ~/.claude/skills: WSL {len(sw)}, Windows {len(sn)}, on both {len(sw & sn)}")
    for label, names in (("WSL only", sorted(sw - sn)), ("Windows only", sorted(sn - sw))):
        shown = names if full else names[:15]
        for name in shown:
            print(f"  {label:13} {name}")
        if len(names) > len(shown):
            print(f"  {label:13} … {len(names) - len(shown)} more (add --full)")
    differs |= sw != sn
    return 1 if differs else 0


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    cmd, rest = argv[0], argv[1:]
    if cmd == "paths":
        return cmd_paths()
    if cmd == "backup" and len(rest) == 1:
        return cmd_backup(rest[0])
    if cmd == "claude":
        return cmd_claude(rest)
    if cmd == "parity":
        return cmd_parity(full="--full" in rest)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
