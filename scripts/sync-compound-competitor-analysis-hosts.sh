#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${CONTENT_IDEAS_ROOT:-/home/sheke/content-ideas}"
export PRESENTATION_HOST_MANIFEST="${COMPOUND_COMPETITOR_HOST_MANIFEST:-$REPO_ROOT/config/compound-competitor-analysis-hosts.json}"

exec bash "$REPO_ROOT/scripts/sync-presentation-pipeline-hosts.sh"
