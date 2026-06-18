#!/usr/bin/env bash
set -euo pipefail

PORT="${GBRAIN_HTTP_PORT:-3131}"
HOST="${GBRAIN_HTTP_HOST:-127.0.0.1}"
REAL_HOME="$(getent passwd "$(id -u)" | cut -d: -f6)"
REAL_HOME="${REAL_HOME:-$HOME}"
PID_FILE="${REAL_HOME}/.gbrain/gbrain-http.pid"
LOG_DIR="${REAL_HOME}/.gbrain/logs"
LOG_FILE="${LOG_DIR}/gbrain-http.log"
BUN="${REAL_HOME}/.bun/bin/bun"
CLI="${REAL_HOME}/gbrain/src/cli.ts"
HEALTH_URL="http://${HOST}:${PORT}/health"

export HOME="${REAL_HOME}"
export PATH="${REAL_HOME}/.bun/bin:$PATH"

mkdir -p "${LOG_DIR}"

is_running() {
  if [[ -f "${PID_FILE}" ]]; then
    local pid
    pid="$(cat "${PID_FILE}")"
    if [[ -n "${pid}" ]] && kill -0 "${pid}" 2>/dev/null; then
      return 0
    fi
  fi
  return 1
}

start_server() {
  if is_running; then
    echo "gbrain HTTP already running with PID $(cat "${PID_FILE}")"
    return 0
  fi

  setsid "${BUN}" run "${CLI}" serve --http --bind "${HOST}" --port "${PORT}" --suppress-bootstrap-token \
    </dev/null >>"${LOG_FILE}" 2>&1 &
  echo $! > "${PID_FILE}"
  sleep 2
  if ! is_running; then
    echo "gbrain HTTP failed to start; check ${LOG_FILE}" >&2
    return 1
  fi
  echo "gbrain HTTP started on ${HEALTH_URL} with PID $(cat "${PID_FILE}")"
}

stop_server() {
  if ! is_running; then
    rm -f "${PID_FILE}"
    echo "gbrain HTTP is not running"
    return 0
  fi

  local pid
  pid="$(cat "${PID_FILE}")"
  kill "${pid}"
  for _ in $(seq 1 20); do
    if ! kill -0 "${pid}" 2>/dev/null; then
      rm -f "${PID_FILE}"
      echo "gbrain HTTP stopped"
      return 0
    fi
    sleep 0.5
  done

  echo "gbrain HTTP did not stop cleanly; PID ${pid} is still alive" >&2
  return 1
}

status_server() {
  if is_running; then
    echo "pid=$(cat "${PID_FILE}")"
  else
    echo "pid=stopped"
  fi

  if command -v curl >/dev/null 2>&1; then
    curl -fsS "${HEALTH_URL}" || true
  fi
}

case "${1:-status}" in
  start) start_server ;;
  stop) stop_server ;;
  restart) stop_server || true; start_server ;;
  status) status_server ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}" >&2
    exit 2
    ;;
esac
