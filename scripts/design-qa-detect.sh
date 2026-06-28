#!/usr/bin/env bash
# design-qa-detect.sh — deterministic design-slop gate for HTML decks / UI.
# Wraps Impeccable's detector (44 rules, no LLM, no API key). Adopted CLI-only;
# the Impeccable *skill* is NOT installed (it collides with refero-design).
# See references/design-md-resources.md ("Design QA gate").
#
# Usage:
#   scripts/design-qa-detect.sh <file-or-dir-or-URL> [more paths...]
#   scripts/design-qa-detect.sh --json <path>        # machine-readable
#
# Exit codes (from Impeccable): 0 = clean, 2 = anti-patterns found, 1 = error.
# Loads a local DESIGN.md by default and suppresses findings that match it, so
# intentional Aurora Glass tokens (teal, glow, gradient) are not flagged —
# only deviations are. Waive false positives with inline
#   <!-- impeccable-disable <rule> -- reason -->
# or a .impeccable/config.json detector.ignoreRules entry.
set -euo pipefail

if [ "$#" -eq 0 ]; then
  echo "usage: $0 <file|dir|URL> [...]   (or --json <path>)" >&2
  exit 1
fi

# Impeccable needs Node 24+; system node here is v22. Prefer nvm's 24 if present.
if command -v node >/dev/null 2>&1 && [ "$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)" -ge 24 ]; then
  : # current node is fine
elif [ -s "$HOME/.nvm/nvm.sh" ]; then
  # shellcheck disable=SC1091
  export NVM_DIR="$HOME/.nvm"; . "$HOME/.nvm/nvm.sh" >/dev/null 2>&1
  nvm use 24 >/dev/null 2>&1 || nvm use node >/dev/null 2>&1 || true
fi

ver="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)"
if [ "$ver" -lt 24 ]; then
  echo "BLOCKED: Impeccable detector needs Node 24+ (found v$(node -v 2>/dev/null || echo none)). Run 'nvm install 24'." >&2
  exit 1
fi

exec npx -y impeccable@latest detect "$@"
