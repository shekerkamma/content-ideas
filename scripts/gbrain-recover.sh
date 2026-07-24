#!/usr/bin/env bash
set -euo pipefail

MODE="${1:---check}"
PORT="${GBRAIN_HTTP_PORT:-3131}"
HOST="${GBRAIN_HTTP_HOST:-127.0.0.1}"
REAL_HOME="$(getent passwd "$(id -u)" | cut -d: -f6)"
REAL_HOME="${REAL_HOME:-$HOME}"
GBRAIN_DIR="${REAL_HOME}/.gbrain"
PGLITE_DIR="${GBRAIN_DIR}/brain.pglite"
LOCK_DIR="${PGLITE_DIR}/.gbrain-lock"
POSTMASTER_PID="${PGLITE_DIR}/postmaster.pid"
HEALTH_URL="http://${HOST}:${PORT}/health"

usage() {
  cat >&2 <<EOF
Usage: $0 [--check|--fix]

--check  Report GBrain HTTP/PGLite status without changing files.
--fix    If no live process owns ${PGLITE_DIR}, remove stale PGLite lock
         artifacts, restart gbrain-http.service, and verify /health.
EOF
}

require_mode() {
  case "${MODE}" in
    --check|--fix) ;;
    -h|--help) usage; exit 0 ;;
    *) usage; exit 2 ;;
  esac
}

print_header() {
  printf '\n== %s ==\n' "$1"
}

health_check() {
  if ! command -v curl >/dev/null 2>&1; then
    echo "curl not found; skipping HTTP health check"
    return 1
  fi

  curl -fsS "${HEALTH_URL}"
}

live_owners() {
  if ! command -v lsof >/dev/null 2>&1; then
    echo "lsof not found; cannot prove PGLite ownership" >&2
    return 2
  fi

  lsof +D "${PGLITE_DIR}" 2>/dev/null || true
}

has_live_owner() {
  [[ -n "$(live_owners)" ]]
}

show_status() {
  print_header "GBrain HTTP service"
  systemctl --user status gbrain-http.service --no-pager || true

  print_header "Health"
  health_check || true
  echo

  print_header "PGLite live owners"
  local owners
  owners="$(live_owners)"
  if [[ -n "${owners}" ]]; then
    printf '%s\n' "${owners}"
  else
    echo "none"
  fi

  print_header "Lock artifacts"
  if [[ -e "${LOCK_DIR}" ]]; then
    ls -ld "${LOCK_DIR}"
  else
    echo "missing: ${LOCK_DIR}"
  fi
  if [[ -e "${POSTMASTER_PID}" ]]; then
    ls -l "${POSTMASTER_PID}"
  else
    echo "missing: ${POSTMASTER_PID}"
  fi
}

fix_stale_locks() {
  if [[ ! -d "${PGLITE_DIR}" ]]; then
    echo "PGLite directory not found: ${PGLITE_DIR}" >&2
    exit 1
  fi

  if ! command -v lsof >/dev/null 2>&1; then
    echo "Refusing to remove locks because lsof is unavailable." >&2
    echo "Install lsof or verify manually that no process owns ${PGLITE_DIR}." >&2
    exit 1
  fi

  if has_live_owner; then
    echo "Refusing to remove locks because a live process owns ${PGLITE_DIR}:" >&2
    live_owners >&2
    exit 1
  fi

  rm -rf "${LOCK_DIR}" "${POSTMASTER_PID}"
  systemctl --user restart gbrain-http.service

  for _ in $(seq 1 20); do
    if health_check >/dev/null 2>&1; then
      health_check
      echo
      return 0
    fi
    sleep 1
  done

  echo "GBrain HTTP did not become healthy; inspect service logs:" >&2
  echo "  systemctl --user status gbrain-http.service --no-pager" >&2
  echo "  tail -120 ${GBRAIN_DIR}/logs/gbrain-http.log" >&2
  exit 1
}

require_mode
if [[ "${MODE}" == "--check" ]]; then
  show_status
else
  show_status
  print_header "Recovery"
  fix_stale_locks
fi
