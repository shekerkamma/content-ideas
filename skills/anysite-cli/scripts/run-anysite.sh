#!/usr/bin/env bash
set -euo pipefail

if command -v anysite >/dev/null 2>&1; then
  exec anysite "$@"
fi

exec uvx --python 3.12 --from 'anysite-cli[data]' anysite "$@"
