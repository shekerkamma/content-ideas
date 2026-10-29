#!/usr/bin/env bash
# Install graphify-pro on every host that runs graphify, and add the one-line routing rule
# to each host's global instruction file. Idempotent: safe to re-run after editing the script.
#
#   WSL:     ~/.local/bin/graphify-pro -> symlink to this repo's scripts/graphify-pro
#   Windows: C:\Users\<you>\.local\bin\graphify-pro (a copy — Git Bash cannot follow a WSL link)
#   Rules:   Claude Code (WSL + Windows), Codex (WSL + Windows), Antigravity (GEMINI.md)
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$REPO/scripts/graphify-pro"
WIN_HOME="${WIN_HOME:-/mnt/c/Users/${USER:-sheke}}"
MARK="graphify-pro"
RULE='- **graphify: run model-backed extraction on Claude Sonnet 5.5 (Claude plan), never the billed Gemini key.** Start every graphify Bash block that can call an LLM with `eval "$(graphify-pro --env)"`, then call `extract_corpus_parallel(files, backend=os.environ["GRAPHIFY_PRO_BACKEND"], root=<corpus dir>)`. The default is `claude-sonnet-5-5` via the claude-cli backend (28 nodes/37 edges vs 25 for sonnet-4-6, all grounded). It unsets GEMINI_API_KEY and fails closed. `GRAPHIFY_PRO_MODEL=gemini-3.8-flash-high` uses the CLIProxyAPI route instead. Source: content-ideas/scripts/graphify-pro.'

mkdir -p "$HOME/.local/bin"
ln -sfn "$SRC" "$HOME/.local/bin/graphify-pro"
echo "WSL:     $HOME/.local/bin/graphify-pro -> $SRC"

if [ -d "$WIN_HOME" ]; then
  mkdir -p "$WIN_HOME/.local/bin"
  tr -d '\r' < "$SRC" > "$WIN_HOME/.local/bin/graphify-pro"
  chmod 755 "$WIN_HOME/.local/bin/graphify-pro" 2>/dev/null || true
  echo "Windows: $WIN_HOME/.local/bin/graphify-pro (copy)"
fi

add_rule() {
  local f="$1"
  [ -d "$(dirname "$f")" ] || { echo "skip:    $f (host not installed)"; return; }
  if [ -f "$f" ] && grep -q "$MARK" "$f"; then
    if grep -qF -- "$RULE" "$f"; then echo "current: $f"; return; fi
    # Replace the outdated rule line in place; everything else in the file is untouched.
    RULE="$RULE" MARK="$MARK" python3 - "$f" <<'PY'
import os, sys
p = sys.argv[1]; rule, mark = os.environ["RULE"], os.environ["MARK"]
lines = open(p, encoding="utf-8").read().split("\n")
out = [rule if (mark in l and l.lstrip().startswith("- **")) else l for l in lines]
open(p, "w", encoding="utf-8").write("\n".join(out))
PY
    echo "updated: $f"; return
  fi
  { [ -s "$f" ] && printf '\n'; printf '# graphify\n%s\n' "$RULE"; } >> "$f"
  echo "added:   $f"
}
add_rule "$HOME/.claude/CLAUDE.md"
add_rule "$HOME/.codex/AGENTS.md"
add_rule "$WIN_HOME/.claude/CLAUDE.md"
add_rule "$WIN_HOME/.codex/AGENTS.md"
add_rule "$WIN_HOME/.gemini/GEMINI.md"
