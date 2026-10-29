#!/usr/bin/env python3
"""Refresh Gemini Notebook auth and report the truth about whether it worked.

Why this exists
---------------
`notebooklm auth refresh` (notebooklm-py 0.8.1) can print

    Unexpected error:
    This may be a bug. Please report at https://github.com/teng-lin/...

and exit 2 **after the refresh has already succeeded**. Observed 2026-08-15:
that message appeared, and an immediately following `auth check` reported
"Authentication is valid" with live API calls working.

Mechanism, as far as it could be narrowed without a reproduction:

- `cli/services/playwright_login.py:150` — the "Identifying Google account"
  step catches only `(OSError, ValueError, RuntimeError, httpx.HTTPError)` and
  degrades those to a warning. Anything outside that tuple propagates.
- `cli/error_handler.py:450` — the CLI catch-all renders `str(e.args[0])`, so
  an exception carrying a single empty-string arg prints a blank message and
  exits 2.
- Debug logging shows cookies are **synced to storage_state.json before**
  account identification runs, so the refresh's actual work is already done
  when that step can fail.

The exact exception was not identified — it did not reproduce once the auth
state was healthy. That is fine: the fix does not depend on knowing it. The
exit code is simply not evidence, so this wrapper ignores it and verifies
observable state instead.

Never re-run `notebooklm login` on the strength of that exit code alone. A
login re-prompt is an interactive Google auth flow; triggering it because of a
false negative is the expensive failure this script prevents.

Usage
-----
    python3 auth_refresh.py            # refresh, then verify, exit truthfully
    python3 auth_refresh.py --check-only
    python3 auth_refresh.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

REFRESH_TIMEOUT = 300
CHECK_TIMEOUT = 120

# `auth check` prints this when the session is usable.
VALID_MARKER = "authentication is valid"
# Substrings that mean the session genuinely needs an interactive login.
NEEDS_LOGIN = (
    "storage file not found",
    "not authenticated",
    "run 'notebooklm login'",
)


def find_cli() -> str | None:
    return shutil.which("notebooklm") or (
        os.path.expanduser("~/.local/bin/notebooklm")
        if os.path.exists(os.path.expanduser("~/.local/bin/notebooklm"))
        else None
    )


def run(cli: str, args: list[str], timeout: int) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            [cli, *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "NOTEBOOKLM_HEADLESS_REAUTH": "1"},
        )
        return proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"


def verify(cli: str) -> tuple[bool, bool, str]:
    """Return (is_valid, needs_login, output) from `auth check`."""
    code, out = run(cli, ["auth", "check"], CHECK_TIMEOUT)
    low = out.lower()
    valid = VALID_MARKER in low or (code == 0 and not any(m in low for m in NEEDS_LOGIN))
    needs_login = any(m in low for m in NEEDS_LOGIN)
    return valid, needs_login, out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Refresh auth, then verify it for real.")
    ap.add_argument("--check-only", action="store_true", help="Skip refresh; just verify.")
    ap.add_argument("--json", action="store_true", help="Machine-readable output.")
    args = ap.parse_args(argv)

    cli = find_cli()
    if not cli:
        msg = "notebooklm CLI not found on PATH (uv tool install 'notebooklm-py[browser]')"
        print(json.dumps({"ok": False, "error": msg}) if args.json else f"error: {msg}",
              file=sys.stderr)
        return 2

    refresh_code: int | None = None
    refresh_out = ""
    if not args.check_only:
        refresh_code, refresh_out = run(cli, ["auth", "refresh"], REFRESH_TIMEOUT)

    valid, needs_login, check_out = verify(cli)

    # The whole point: a non-zero refresh exit that ends in a valid session is a
    # false negative, not a failure.
    false_negative = bool(refresh_code) and valid

    result = {
        "ok": valid,
        "refresh_exit_code": refresh_code,
        "session_valid": valid,
        "needs_interactive_login": needs_login and not valid,
        "false_negative_suppressed": false_negative,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if valid:
            print("auth: VALID")
            if false_negative:
                print(f"  note: `auth refresh` exited {refresh_code} but the session is "
                      f"usable — known false negative, exit code ignored")
                first = next((ln.strip() for ln in refresh_out.splitlines()
                              if ln.strip() and "Unexpected error" in ln), "")
                if first:
                    print(f"  it said: {first}")
            print("  do NOT run `notebooklm login` — nothing needs re-authenticating")
        else:
            print("auth: INVALID")
            if needs_login:
                print("  interactive login required — run:  notebooklm login")
            print("  --- auth check output ---")
            for line in check_out.strip().splitlines()[-6:]:
                print(f"  {line}")

    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
