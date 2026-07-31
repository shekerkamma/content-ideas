#!/bin/bash

set -euo pipefail

CHROME_BIN=$(find "$HOME/.cache/ms-playwright" -maxdepth 3 -path '*/chrome-linux64/chrome' -type f 2>/dev/null | sort -V | tail -1)

if [ -z "$CHROME_BIN" ]; then
  echo "No Playwright-managed Chrome found under ~/.cache/ms-playwright. Run: npx playwright install chromium" >&2
  exit 1
fi

exec "$CHROME_BIN" "$@"
