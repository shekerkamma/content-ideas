#!/usr/bin/env python3
"""Add or update an API key without the agent ever seeing it.

Run it yourself, in your own terminal (not through Claude):

    python3 scripts/add_key.py OPENAI_API_KEY

It asks for the value twice with echo off, then writes it to both layers of
the two-layer pattern (see CLAUDE.md, Rules):

  1. the "env" block of <project>/.claude/settings.local.json  (Claude Code)
  2. an `export NAME=...` line in ~/.config/keys.env          (Codex, shells)

~/.bashrc only sources keys.env (the line is added if missing), so the keys
sit in one file that Claude Code's settings read-deny. A stale
`export NAME=` for the same name is removed from ~/.bashrc so it cannot
override the new value. An existing entry is replaced; everything else is
kept. Files are rewritten atomically; settings.local.json and keys.env are
chmod 600. The value is never printed, logged, or put on a command line.

--migrate moves every top-level `export *_KEY=` / `*_TOKEN=` / `*_SECRET=` /
`*_PASSWORD=` line out of ~/.bashrc into keys.env verbatim (backup first,
into a read-denied keys.env.bashrc-backup-* file) and prints names only.
Add --dry-run to list the names without changing anything.

--stdin reads the value from standard input instead of the keyboard, for a
password manager pipe (`pass show x | add_key.py NAME --stdin`) and for tests.
--from-env-file PATH copies the value of NAME from an existing .env or
keys file (KEY=value or export KEY=value), e.g. to put a key Hermes already
has into keys.env; the value is never shown.

--hermes also writes NAME=value into Hermes's own env file, ~/.hermes/.env
(override with --hermes-env), which Hermes loads at start. --skip-claude
leaves .claude/settings.local.json untouched, for keys Claude Code should not
get.

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
import time
from pathlib import Path

NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
SECRET_NAME_RE = re.compile(r"(_KEY|_TOKEN|_SECRET|_PASSWORD)$")
EXPORT_RE = re.compile(r"^export\s+([A-Za-z_][A-Za-z0-9_]*)=")
SOURCE_LINE = '[ -f "$HOME/.config/keys.env" ] && . "$HOME/.config/keys.env"  # API keys (add_key.py)\n'
KEYS_HEADER = ("# API keys, sourced from ~/.bashrc. Written by content-ideas/scripts/add_key.py.\n"
               "# Claude Code settings read-deny this file; edit it yourself, not through an agent.\n")


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


def _lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True) if path.exists() else []


def _put_export(lines: list[str], name: str, line: str) -> str:
    """Replace the first `export NAME=` line (dropping later duplicates) or append."""
    if not line.endswith("\n"):
        line += "\n"
    hits = [i for i, l in enumerate(lines) if (m := EXPORT_RE.match(l)) and m.group(1) == name]
    if hits:
        lines[hits[0]] = line
        for i in reversed(hits[1:]):
            del lines[i]
        return "replaced"
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    lines.append(line)
    return "added"


def set_keys_file(path: Path, name: str, value: str) -> str:
    lines = _lines(path) or [KEYS_HEADER]
    action = _put_export(lines, name, f"export {name}={shlex.quote(value)}")
    atomic_write(path, "".join(lines), 0o600)
    return action


def is_sourced(lines: list[str]) -> bool:
    return any("keys.env" in l and not l.lstrip().startswith("#") for l in lines)


def fix_bashrc(path: Path, name: str) -> list[str]:
    """Make ~/.bashrc source keys.env and drop stale exports of NAME. Returns notes."""
    lines = _lines(path)
    notes = []
    before = len(lines)
    lines = [l for l in lines if not ((m := EXPORT_RE.match(l)) and m.group(1) == name)]
    if len(lines) != before:
        notes.append(f"removed {before - len(lines)} old export of {name}")
    if not is_sourced(lines):
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines.append(SOURCE_LINE)
        notes.append("added the line that sources keys.env")
    if notes:
        atomic_write(path, "".join(lines), None)
    return notes


def migrate(bashrc: Path, keys_file: Path, dry_run: bool) -> int:
    lines = _lines(bashrc)
    moved = [(i, m.group(1)) for i, l in enumerate(lines)
             if (m := EXPORT_RE.match(l)) and SECRET_NAME_RE.search(m.group(1))]
    names = [n for _, n in moved]
    if not moved:
        print(f"No secret exports found in {bashrc}; nothing to move.")
        return 0
    print(("Would move" if dry_run else "Moving") + f" {len(moved)} line(s) from {bashrc} to {keys_file}:")
    for n in names:
        print(f"  {n}")
    if dry_run:
        return 0
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = keys_file.with_name(f"{keys_file.name}.bashrc-backup-{stamp}")
    atomic_write(backup, "".join(lines), 0o600)
    klines = _lines(keys_file) or [KEYS_HEADER]
    for i, n in moved:  # in file order, so a later duplicate wins as it did before
        _put_export(klines, n, lines[i])
    atomic_write(keys_file, "".join(klines), 0o600)
    first = moved[0][0]
    keep = []
    for i, l in enumerate(lines):
        if i == first and not is_sourced(lines):
            keep.append(SOURCE_LINE)
        elif i not in {j for j, _ in moved}:
            keep.append(l)
    atomic_write(bashrc, "".join(keep), None)
    print(f"Backup of the old {bashrc.name}: {backup} (chmod 600)")
    print(f"{bashrc} now sources {keys_file}. Open a new shell to load it.")
    return 0


def _dotenv_value(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
        inner = raw[1:-1]
        return re.sub(r"\\(.)", r"\1", inner) if raw[0] == '"' else inner
    return raw.split(" #", 1)[0].strip()


def read_env_file_value(path: Path, name: str) -> str | None:
    """Last assignment of NAME in a KEY=value / export KEY=value file, or None."""
    pat = re.compile(rf"^\s*(?:export\s+)?{re.escape(name)}\s*=(.*)$")
    found = None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        m = pat.match(line)
        if m:
            if line.lstrip().startswith("export"):   # shell syntax, as add_key writes keys.env
                raw = m.group(1).strip()
                if "$" in raw and not raw.startswith("'"):
                    raise ValueError(f"{name} in {path} refers to another variable "
                                     "(contains $); copy that variable instead")
                parts = shlex.split(raw, comments=True)
                found = parts[0] if parts else ""
            else:
                found = _dotenv_value(m.group(1))
    return found


def _dotenv_quote(value: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_\-.:/+=@,]+", value):
        return value
    if "'" not in value:
        return f"'{value}'"
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def set_dotenv(path: Path, name: str, value: str) -> str:
    lines = _lines(path)
    pat = re.compile(rf"^\s*(?:export\s+)?{re.escape(name)}\s*=")
    new = f"{name}={_dotenv_quote(value)}\n"
    hits = [i for i, l in enumerate(lines) if pat.match(l)]
    if hits:
        lines[hits[0]] = new
        for i in reversed(hits[1:]):
            del lines[i]
        action = "replaced"
    else:
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines.append(new)
        action = "added"
    atomic_write(path, "".join(lines), 0o600)
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
    ap.add_argument("name", nargs="?", help="variable name, e.g. OPENAI_API_KEY")
    ap.add_argument("--stdin", action="store_true",
                    help="read the value from standard input instead of the keyboard")
    ap.add_argument("--project-dir", help="project holding .claude/ (default: git top level)")
    ap.add_argument("--keys-file", default="~/.config/keys.env", help="file holding the export lines")
    ap.add_argument("--bashrc", default="~/.bashrc", help="shell file that sources the keys file")
    ap.add_argument("--migrate", action="store_true",
                    help="move secret export lines from --bashrc into --keys-file")
    ap.add_argument("--dry-run", action="store_true", help="with --migrate: list names only")
    ap.add_argument("--from-env-file", metavar="PATH",
                    help="copy the value of NAME from this .env / keys file instead of asking")
    ap.add_argument("--hermes", action="store_true", help="also write NAME into Hermes's env file")
    ap.add_argument("--hermes-env", default="~/.hermes/.env", help="Hermes env file for --hermes")
    ap.add_argument("--skip-claude", action="store_true",
                    help="do not write .claude/settings.local.json")
    args = ap.parse_args(argv)
    keys_file = Path(args.keys_file).expanduser()
    bashrc = Path(args.bashrc).expanduser()

    if args.migrate:
        return migrate(bashrc, keys_file, args.dry_run)
    if not args.name:
        fail("give a variable name, or use --migrate.", 2)

    name = args.name.strip()
    if not NAME_RE.match(name):
        fail(f"{name!r} is not a valid variable name (use A-Z, 0-9 and _, starting with a letter).", 2)

    if args.stdin and args.from_env_file:
        fail("use --stdin or --from-env-file, not both.", 2)
    if args.from_env_file:
        src = Path(args.from_env_file).expanduser()
        if not src.is_file():
            fail(f"{src} does not exist; nothing was changed.")
        try:
            value = read_env_file_value(src, name)
        except ValueError as exc:
            fail(f"{exc}; nothing was changed.")
        if value is None:
            fail(f"{name} is not set in {src}; nothing was changed.")
    elif args.stdin:
        value = sys.stdin.readline().rstrip("\r\n")
    else:
        value = read_hidden(f"Value for {name} (typing is hidden): ")
        again = read_hidden("Same value again: ")
        if value != again:
            fail("the two entries did not match; nothing was changed.")
    if not value.strip():
        fail("empty value; nothing was changed.")
    if "\n" in value or "\x00" in value:
        fail("the value contains a newline or NUL; nothing was changed.")

    if not args.skip_claude:
        settings = project_dir(args.project_dir) / ".claude" / "settings.local.json"
        print(f"{name}: {set_settings(settings, name, value)} in {settings}")
    a2 = set_keys_file(keys_file, name, value)
    notes = fix_bashrc(bashrc, name)
    print(f"{name}: {a2} in {keys_file}")
    if args.hermes:
        hermes_env = Path(args.hermes_env).expanduser()
        print(f"{name}: {set_dotenv(hermes_env, name, value)} in {hermes_env}")
    for n in notes:
        print(f"{bashrc}: {n}")
    print("Restart Claude Code (and open a new shell) so the new value loads.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
