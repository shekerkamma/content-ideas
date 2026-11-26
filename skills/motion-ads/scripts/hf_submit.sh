#!/usr/bin/env bash
# Submit one Higgsfield job from the terminal, safely.
#
# The CLI's own "--wait" sometimes hangs on submit or upload. When that happens no job exists and
# nothing is charged, but the script that called it sits there forever. This wrapper:
#   1. asks for the price first and prints it,
#   2. submits WITHOUT --wait, giving up and retrying if the submit stalls,
#   3. polls the job until it finishes,
#   4. downloads the result and prints one line you can paste into the credit log.

usage() {
  cat <<'EOF'
Usage: hf_submit.sh <out-file-without-extension> <model> [higgsfield flags...]

Examples:
  hf_submit.sh keys/K3 nano_banana_pro --prompt "$(cat prompts/K3.txt)" --resolution 4k --aspect_ratio 16:9 --image <upload-id>
  hf_submit.sh shots/S4 kling4_0 --prompt "$(cat prompts/S4.txt)" --mode image-to-video --duration 5 --resolution 1080p \
      --start-image <K3 job-or-upload id> --end-image <K4 job-or-upload id>
  hf_submit.sh sound/music elevenlabs_music_v2_5 --prompt "$(cat prompts/music.txt)" --duration 20 --force_instrumental true

Options (environment):
  HF_STALL=60       seconds to wait for the submit before retrying (default 60)
  HF_TIMEOUT=40m    how long to wait for the job (default 40m)
  HF_MAX=           refuse to submit if the quoted price is above this many credits

Flags differ per model. List them with:  higgsfield model list   and   higgsfield generate create <model> --help
Needs: the higgsfield CLI, signed in (higgsfield auth login), curl, python3.
EOF
}

case "${1:-}" in -h|--help|"") usage; exit 0;; esac
[ $# -ge 2 ] || { usage; exit 2; }
command -v higgsfield >/dev/null || { echo "The higgsfield CLI is not installed or not on PATH." >&2; exit 127; }

out="$1"; model="$2"; shift 2
stall="${HF_STALL:-60}"; timeout="${HF_TIMEOUT:-40m}"
tmp="$(mktemp)"; trap 'rm -f "$tmp"' EXIT

quote="$(higgsfield generate cost "$model" "$@" 2>&1 | tail -1)"
echo "quoted: $quote"
if [ -n "${HF_MAX:-}" ]; then
  price="$(printf '%s' "$quote" | grep -Eo '[0-9]+(\.[0-9]+)?' | head -1)"
  if [ -n "$price" ] && python3 -c "import sys; sys.exit(0 if float('$price') > float('$HF_MAX') else 1)"; then
    echo "Refusing: quoted $price credits is above HF_MAX=$HF_MAX." >&2; exit 3
  fi
fi

id=""
for try in 1 2 3; do
  higgsfield --json generate create "$model" "$@" > "$tmp" 2>&1 &
  pid=$!
  waited=0
  while kill -0 "$pid" 2>/dev/null && [ "$waited" -lt "$stall" ]; do sleep 1; waited=$((waited + 1)); done
  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null
    echo "submit stalled (try $try), nothing was created, retrying" >&2
    continue
  fi
  id="$(python3 -c "import json,sys
try:
    d = json.load(open(sys.argv[1])); d = d[0] if isinstance(d, list) else d
    print(d if isinstance(d, str) else d.get('id', ''))
except Exception:
    print('')" "$tmp")"
  [ -n "$id" ] && break
  echo "submit failed (try $try): $(cat "$tmp")" >&2
done
[ -n "$id" ] || { echo "Could not submit the job. Nothing was charged." >&2; exit 1; }
echo "job: $id"

higgsfield generate wait "$id" --timeout "$timeout" --interval 6s >/dev/null 2>&1
read -r status url < <(higgsfield --json generate get "$id" 2>/dev/null | python3 -c "import json,sys
d = json.load(sys.stdin); print(d.get('status', '?'), d.get('result_url') or '')")
file=""
if [ -n "${url:-}" ]; then
  ext="${url##*.}"; ext="${ext%%\?*}"
  file="$out.$ext"
  mkdir -p "$(dirname "$file")"
  curl -sL "$url" -o "$file"
fi
echo "$model | $quote | ${status:-?} | ${file:-no file} | $id"
[ -n "$file" ] || { echo "The job did not return a file. If it failed, check that it was refunded: higgsfield account transactions" >&2; exit 1; }
