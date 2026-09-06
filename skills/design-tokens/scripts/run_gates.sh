#!/usr/bin/env bash
# run_gates.sh — the render-gate battery for one page, with a real preflight.
#
# Every gate here opens the page in Chromium and measures it. None of them can
# pass by not running: a missing browser or rule set is BLOCKED (exit 1), never
# a silent skip. See lib/browser.mjs for why that distinction is load-bearing.
#
# Usage:
#   run_gates.sh <file.html> [--dark] [--open=<selector>] [--skip=axe,rtl,...]
#
# Exit codes (matching scripts/design-qa-detect.sh):
#   0  every gate ran and the page is clean
#   1  blocked — a gate could not run, so the page is UNMEASURED
#   2  the gates ran and found violations
#
# Requires: node >= 18, `npm i -D playwright axe-core`, and a Chromium build
# (`npx playwright install --with-deps chromium`). If Playwright's expected
# build is missing but another is cached, DESIGN_TOKENS_CHROMIUM=auto uses it
# and prints which one.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET=""
DARK=""
OPEN=""
SKIP=""

for arg in "$@"; do
  case "$arg" in
    --dark) DARK="--dark" ;;
    --open=*) OPEN="$arg" ;;
    --skip=*) SKIP="${arg#--skip=}" ;;
    --*) ;;
    *) TARGET="$arg" ;;
  esac
done

if [ -z "$TARGET" ]; then
  echo "usage: run_gates.sh <file.html> [--dark] [--open=<selector>] [--skip=axe,rtl]" >&2
  exit 1
fi
if [ ! -e "$TARGET" ]; then
  echo "BLOCKED: $TARGET does not exist — nothing was measured." >&2
  exit 1
fi

skipped() { case ",$SKIP," in *",$1,"*) return 0 ;; *) return 1 ;; esac; }

BLOCKED_GATES=()
FAILED_GATES=()
RAN=0

run_gate() {
  local name="$1"; shift
  if skipped "$name"; then echo "-- $name: skipped by --skip"; return; fi
  echo "-- $name"
  node "$HERE/$1" "${@:2}"
  local rc=$?
  case $rc in
    0) RAN=$((RAN + 1)) ;;
    2) RAN=$((RAN + 1)); FAILED_GATES+=("$name") ;;
    *) BLOCKED_GATES+=("$name") ;;
  esac
}

run_gate contrast        measure_render.mjs        "$TARGET" $DARK
run_gate states          verify_states.mjs         "$TARGET" $DARK
run_gate axe             axe_audit.mjs             "$TARGET" $DARK
run_gate target-size     verify_target_size.mjs    "$TARGET" $DARK
run_gate keyboard        verify_keyboard.mjs       "$TARGET"
run_gate overflow        verify_overflow.mjs       "$TARGET"
run_gate responsive      verify_responsive.mjs     "$TARGET"
run_gate reduced-motion  verify_reduced_motion.mjs "$TARGET"
run_gate rtl             verify_rtl.mjs            "$TARGET"
[ -n "$OPEN" ] && run_gate focus-trap verify_focustrap.mjs "$TARGET" "$OPEN" $DARK

echo
if [ ${#BLOCKED_GATES[@]} -gt 0 ]; then
  echo "BLOCKED: ${#BLOCKED_GATES[@]} gate(s) could not run: ${BLOCKED_GATES[*]}"
  echo "The page is UNMEASURED on those criteria. Do not report it as reviewed."
  exit 1
fi
if [ ${#FAILED_GATES[@]} -gt 0 ]; then
  echo "FINDINGS: $RAN gate(s) ran, ${#FAILED_GATES[@]} failed: ${FAILED_GATES[*]}"
  exit 2
fi
echo "OK: $RAN gate(s) ran, all clean."
exit 0
