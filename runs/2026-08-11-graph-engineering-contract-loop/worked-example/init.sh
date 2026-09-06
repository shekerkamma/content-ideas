#!/usr/bin/env bash
# Boot script for: Skill integrity audit
#
# Every run calls this instead of rediscovering how to launch the thing.
# Keep it fast and idempotent. Exit non-zero if the environment is not usable.

set -euo pipefail

echo "[init] project: Skill integrity audit"
echo "[init] pwd: $(pwd)"

# --- Add environment setup below. Examples:
# python3 -m venv .venv && source .venv/bin/activate
# npm install --silent
# docker compose up -d

echo "[init] ready"
