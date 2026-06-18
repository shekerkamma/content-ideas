#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <windows-or-wsl-path>" >&2
  exit 2
fi

input_path="$1"

to_windows_path() {
  local p="$1"
  if [[ "$p" =~ ^[A-Za-z]:\\ ]]; then
    printf '%s\n' "$p"
    return 0
  fi
  if [[ "$p" == /mnt/* ]]; then
    python3 - "$p" <<'PY'
import sys
from pathlib import PurePosixPath

p = PurePosixPath(sys.argv[1])
parts = p.parts
if len(parts) >= 4 and parts[1] == "mnt":
    drive = parts[2].upper() + ":"
    rest = "\\".join(parts[3:])
    print(drive + ("\\" + rest if rest else ""))
else:
    raise SystemExit(1)
PY
    return 0
  fi
  printf '%s\n' "$p"
}

windows_path="$(to_windows_path "$input_path")"

if [ -x /mnt/c/Windows/System32/cmd.exe ] && [ -e /init ]; then
  /mnt/c/Windows/System32/cmd.exe /C start "" "$windows_path"
  exit 0
fi

cat >&2 <<EOF
Windows open is not available from this shell.

Why:
- This session is running in a confined runtime where normal WSL Windows-exe interop is unavailable.
- Typical symptoms are:
  - \`xdg-open\` falling back to broken Linux GUI handlers
  - \`cmd.exe\` or \`powershell.exe\` failing even when present on /mnt/c
  - missing \`/init\` inside the current mount namespace

Open this file from a normal WSL or Windows terminal instead:
  cmd.exe /C start "" "$windows_path"
EOF

exit 1
