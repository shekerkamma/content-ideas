#!/usr/bin/env bash
# Rebuild the scorecard and republish the GitHub Pages hub (landing + scorecard + graph).
# One command: bash publish_pages.sh
set -euo pipefail

REPO_SSH="git@github.com:shekerkamma/content-ideas.git"
RUN="/home/shekerk/content-ideas/runs/2026-06-22-agentic-ai-vs-saas-reddit-strategy"
GRAPH="/home/shekerk/content-ideas/runs/2026-06-22-gcp-genai-usecases-graph/graphify-out/graph.html"

echo "==> regenerating scorecard from source"
python3 "$RUN/build_scorecard.py"

TMP="$(mktemp -d)"
cp "$RUN/landing.html"                       "$TMP/index.html"      # hub at /
cp "$RUN/agent-replacement-scorecard.html"   "$TMP/scorecard.html"  # dashboard at /scorecard.html
cp "$GRAPH"                                  "$TMP/graph.html"      # graph at /graph.html

cd "$TMP"
git init -q -b gh-pages
git remote add origin "$REPO_SSH"
git add -A
git -c user.name=shekerk -c user.email=shekerkamma@gmail.com commit -q -m "Republish Pages hub: landing + scorecard + graph

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
echo "==> pushing gh-pages"
git push -f -q -u origin gh-pages
echo "==> done. Live in ~1 min:"
echo "    https://shekerkamma.github.io/content-ideas/"
rm -rf "$TMP"
