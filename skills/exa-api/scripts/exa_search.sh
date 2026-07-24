#!/usr/bin/env bash
set -euo pipefail

query="${1:-}"
num_results="${2:-10}"

load_env_file() {
  local env_file="$1"
  if [ -f "$env_file" ]; then
    set -a
    # shellcheck disable=SC1090
    . "$env_file"
    set +a
  fi
}

if [ -z "$query" ]; then
  printf 'usage: %s "query" [num_results]\n' "$0" >&2
  exit 2
fi

if [ -z "${EXA_API_KEY:-}" ]; then
  load_env_file "/home/shekerk/.config/intel-pipeline/.env"
fi

if [ -z "${EXA_API_KEY:-}" ]; then
  load_env_file "$HOME/.hermes/.env"
fi

if [ -z "${EXA_API_KEY:-}" ] && [ -f ".env" ]; then
  load_env_file ".env"
fi

if [ -z "${EXA_API_KEY:-}" ] && [ -f ".env.local" ]; then
  load_env_file ".env.local"
fi

if [ -z "${EXA_API_KEY:-}" ]; then
  printf 'EXA_API_KEY is not set\n' >&2
  exit 4
fi

curl -sS https://api.exa.ai/search \
  -H "Content-Type: application/json" \
  -H "x-api-key: ${EXA_API_KEY}" \
  -d "$(node -e '
const query = process.argv[1];
const numResults = Number(process.argv[2] || 10);
process.stdout.write(JSON.stringify({
  query,
  numResults,
  type: "auto",
  contents: {
    text: true,
    highlights: true,
    summary: true
  }
}));
' "$query" "$num_results")"
