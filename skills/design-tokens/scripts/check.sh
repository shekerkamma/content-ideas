#!/usr/bin/env bash
# check.sh — the dependency-free half of the gate: stdlib Python only, no browser.
#
# These four run anywhere Python 3 runs, including Codex and CI with no Node.
# They check the token source and the code that references it. They do NOT
# check the rendered page — that is scripts/run_gates.sh, and a clean run here
# is not evidence that anything renders correctly.
#
# Usage:
#   check.sh                      # the bundled assets/tokens/ + assets/golden/
#   check.sh <tokens.json> <theme.css> <src-dir>
#
# Exit 0 = clean, 1 = a validator failed.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOKENS="${1:-}"
THEME="${2:-}"
SRC="${3:-}"

fail=0
run() { echo "-- $1"; shift; "$@" || fail=1; }

if [ -n "$TOKENS" ]; then
  run "tokens parse + aliases resolve" python3 "$HERE/validate_tokens.py" "$TOKENS"
  run "WCAG contrast, light + dark"    python3 "$HERE/validate_contrast.py" "$TOKENS"
else
  run "tokens parse + aliases resolve" python3 "$HERE/validate_tokens.py"
  run "WCAG contrast, light + dark"    python3 "$HERE/validate_contrast.py"
fi

if [ -n "$THEME" ] && [ -n "$SRC" ]; then
  run "every var() resolves to the theme" python3 "$HERE/validate_theme_refs.py" "$THEME" "$SRC"
  run "no hardcoded hex/px/timing"        python3 "$HERE/lint_hardcodes.py" "$SRC"
else
  run "every var() resolves to the theme" python3 "$HERE/validate_theme_refs.py"
  run "no hardcoded hex/px/timing"        python3 "$HERE/lint_hardcodes.py" "$HERE/../assets/golden"
fi

echo
if [ $fail -ne 0 ]; then echo "FAIL: token source or its consumers are inconsistent."; exit 1; fi
echo "OK: token source is valid, contrast passes, and no consumer drifts off-theme."
echo "Note: nothing was rendered. Run scripts/run_gates.sh for the page itself."
