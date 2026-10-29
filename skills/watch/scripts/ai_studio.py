#!/usr/bin/env python3
"""Run watch.py with the host's existing AI Studio key (CLIProxyAPI config), without copying it.

Standard library only, so it runs under WSL and Windows Python alike. The key is read from the
`gemini-api-key` list in the CLIProxyAPI config and injected only into the child process; it is
never printed. Defaults: engine gemini and model gemini-pro-latest, each unless the caller (flag,
environment, or ~/.config/watch/.env) already chose one.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
DEFAULT_MODEL = 'gemini-pro-latest'
CANDIDATES = [Path.home() / '.cli-proxy-api' / 'config.yaml',
              Path('/mnt/c/Users/sheke/.cli-proxy-api/config.yaml')]


def read_keys(path: Path) -> list[str]:
    """api-key values under the top-level `gemini-api-key:` list (enough YAML for this file)."""
    keys, inside = [], False
    for line in path.read_text(encoding='utf-8').splitlines():
        if re.match(r'^\S', line):  # A new top-level key ends the section.
            inside = line.split('#', 1)[0].strip() == 'gemini-api-key:'
            continue
        match = inside and re.match(r'^\s*-?\s*api-key:\s*["\']?([^"\'\s#]+)', line)
        if match:
            keys.append(match.group(1))
    return keys


def credential() -> str:
    override = os.environ.get('WATCH_CLIPROXY_CONFIG')
    for path in [Path(override)] if override else CANDIDATES:
        if path.is_file():
            keys = read_keys(path)
            if len(keys) > 1:
                raise SystemExit(f'{path} lists {len(keys)} Gemini keys; set WATCH_CLIPROXY_CONFIG to a config with one.')
            if keys:
                return keys[0]
    raise SystemExit('No AI Studio key found in the CLIProxyAPI config; no request was made.')


def configured(name: str) -> bool:
    if os.environ.get(name):
        return True
    sys.path.insert(0, str(SCRIPTS))
    from config import CONFIG_FILE  # noqa: E402 - resolved per host (WSL or Windows home)
    try:
        return any(re.match(rf'^{name}=\S', line) for line in Path(CONFIG_FILE).read_text(encoding='utf-8').splitlines())
    except OSError:
        return False


def main() -> None:
    args = sys.argv[1:]
    env = dict(os.environ, GEMINI_API_KEY=credential())
    if not configured('WATCH_GEMINI_MODEL'):
        env['WATCH_GEMINI_MODEL'] = DEFAULT_MODEL
    if not any(a == '--engine' or a.startswith('--engine=') for a in args):
        args += ['--engine', 'gemini']
    command = [sys.executable, '-B', str(SCRIPTS / 'watch.py'), *args]
    if os.name == 'nt':  # execv on Windows detaches from the console; run and pass the exit code through.
        import subprocess
        raise SystemExit(subprocess.call(command, env=env))
    os.execve(sys.executable, command, env)


if __name__ == '__main__':
    main()
