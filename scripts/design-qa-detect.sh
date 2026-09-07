#!/usr/bin/env bash
# design-qa-detect.sh — pinned Impeccable HTML design-QA gate.
#
# Referenced by portable-skills/marp/SKILL.md and
# skills/genspark-branded-deck/SKILL.md as the preferred gate for HTML-derived
# decks before PPTX export. Impeccable does not understand native .pptx; use
# skills/pptx-design-quality/scripts/lint_pptx.py for the PowerPoint artifact.
#
# Usage: design-qa-detect.sh <html-path-or-dir-or-url> [impeccable detect flags...]
# Exit codes: 0 clean · 2 anti-patterns found (printed) · 1 blocked (Node < 24
# or npx unavailable)
set -uo pipefail

IMPECCABLE_VERSION="3.5.0"
REQUIRED_NODE_MAJOR=24

if ! command -v node >/dev/null 2>&1; then
  echo "design-qa-detect: node not found (requires Node >= ${REQUIRED_NODE_MAJOR}; run 'nvm use ${REQUIRED_NODE_MAJOR}')" >&2
  exit 1
fi

node_major="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null)"
if [ -z "$node_major" ] || [ "$node_major" -lt "$REQUIRED_NODE_MAJOR" ]; then
  echo "design-qa-detect: Node ${node_major:-unknown} < ${REQUIRED_NODE_MAJOR} (run 'nvm use ${REQUIRED_NODE_MAJOR}')" >&2
  exit 1
fi

if [ "$#" -lt 1 ]; then
  echo "usage: design-qa-detect.sh <html-path-or-dir-or-url> [impeccable detect flags...]" >&2
  exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "design-qa-detect: npx not found (requires Node >= ${REQUIRED_NODE_MAJOR} with npx on PATH)" >&2
  exit 1
fi

exec npx --yes "impeccable@${IMPECCABLE_VERSION}" detect "$@"
