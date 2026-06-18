#!/usr/bin/env bash
set -euo pipefail

REAL_HOME="$(getent passwd "$(id -u)" | cut -d: -f6)"
REAL_HOME="${REAL_HOME:-$HOME}"
export HOME="${REAL_HOME}"
export PATH="${REAL_HOME}/.bun/bin:$PATH"
export MCP_STDIO=1

exec "${REAL_HOME}/.bun/bin/bun" run "${REAL_HOME}/gbrain/src/cli.ts" serve
