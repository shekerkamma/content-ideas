#!/usr/bin/env python3
"""Add or update an API key without the agent ever seeing it.

Run it yourself, in your own terminal (not through Claude):

    python3 scripts/add_key.py OPENAI_API_KEY

It asks for the value twice with echo off, then writes it to both layers of
the two-layer pattern (see CLAUDE.md, Rules):

  1. the "env" block of <project>/.claude/settings.local.json  (Claude Code)
  2. an `export NAME=...` line in ~/.bashrc                   (Codex, shells)

An existing entry for the same name is replaced; everything else in both
files is kept. Files are rewritten atomically and the settings file is
chmod 600. The value is never printed, logged, or put on a command line.

--stdin reads the value from standard input instead of the keyboard, for a
password manager pipe (`pass show x | add_key.py NAME --stdin`) and for tests.

Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import termios
from pathlib import Path

NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def fail(msg: str, code: int = 1) -> None:
    print(f"add_key: {msg}", file=sys.stderr)
    sys.exit(code)


def read_hidden(prompt: str) -> str:
    """Read one line from the controlling terminal with echo off.

    Refuses to run without a real terminal, so the value can never fall back
    to a visible stdin read (what getpass does when /dev/tty is missing).
    """
    try:
        fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY)
    except OSError:
        fail("no terminal to read from. Run this in your own terminal window, "
             "not through Claude (or pipe the value in with --stdin).", 3)
    with os.fdopen(fd, "r+", buffering=1) as tty:
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] &= ~termios.ECHO
        try:
            tty.write(prompt)
            tty.flush()
            termios.tcsetattr(fd, termios.TCSAFLUSH, new)
            value = tty.readline()
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, old)
            tty.write("\n")
    return value.rstrip("\r\n")


def atomic_write(path: Path, text: str, mode: int | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if mode is None:
        mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def set_settings(path: Path, name: str, value: str) -> str:
    data: dict = {}
    if path.exists():
        raw = path.read_text(encoding="utf-8-sig")
        if raw.strip():
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                fail(f"{path} is not valid JSON ({exc.msg} at line {exc.lineno}); "
                     "nothing was changed.")
    if not isinstance(data, dict):
        fail(f"{path} does not hold a JSON object; nothing was changed.")
    env = data.setdefault("env", {})
    if not isinstance(env, dict):
        fail(f'"env" in {path} is not an object; nothing was changed.')
    action = "replaced" if name in env else "added"
    env[name] = value
    atomic_write(path, json.dumps(data, indent=2) + "\n", 0o600)
    return action


def set_bashrc(path: Path, name: str, value: str) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True) if path.exists() else []
    line = f"export {name}={shlex.quote(value)}\n"
    pat = re.compile(rf"^\s*export\s+{re.escape(name)}=")
    hits = [i for i, l in enumerate(lines) if pat.match(l)]
    if hits:
        lines[hits[0]] = line
        for i in reversed(hits[1:]):  # drop older duplicates so one value wins
            del lines[i]
        action = "replaced"
    else:
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines.append(line)
        action = "added"
    atomic_write(path, "".join(lines), None)
    return action


def project_dir(arg: str | None) -> Path:
    if arg:
        return Path(arg).expanduser().resolve()
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                             text=True, check=True).stdout.strip()
        return Path(top)
    except (OSError, subprocess.CalledProcessError):
        return Path.cwd()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("name", help="variable name, e.g. OPENAI_API_KEY")
    ap.add_argument("--stdin", action="store_true",
                    help="read the value from standard input instead of the keyboard")
    ap.add_argument("--project-dir", help="project holding .claude/ (default: git top level)")
    ap.add_argument("--bashrc", default="~/.bashrc", help="shell file for the export line")
    args = ap.parse_args(argv)

    name = args.name.strip()
    if not NAME_RE.match(name):
        fail(f"{name!r} is not a valid variable name (use A-Z, 0-9 and _, starting with a letter).", 2)

    if args.stdin:
        value = sys.stdin.readline().rstrip("\r\n")
    else:
        value = read_hidden(f"Value for {name} (typing is hidden): ")
        again = read_hidden(f"Same value again: ")
        if value != again:
            fail("the two entries did not match; nothing was changed.")
    if not value.strip():
        fail("empty value; nothing was changed.")
    if "\n" in value or "\x00" in value:
        fail("the value contains a newline or NUL; nothing was changed.")

    settings = project_dir(args.project_dir) / ".claude" / "settings.local.json"
    bashrc = Path(args.bashrc).expanduser()
    a1 = set_settings(settings, name, value)
    a2 = set_bashrc(bashrc, name, value)
    print(f"{name}: {a1} in {settings}")
    print(f"{name}: {a2} in {bashrc}")
    print("Restart Claude Code (and open a new shell) so the new value loads.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
