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
RULE='- **graphify: run model-backed extraction on the Pro subscription.** Start every graphify Bash block that can call an LLM with `eval "$(graphify-pro --env)"`. It routes graphify through CLIProxyAPI to `claude-sonnet-4-6` (measured ~5x richer than gemini-3.1-pro, every node grounded), fails closed if the proxy is down, and never uses the billed GEMINI_API_KEY. Pass `root=` = the corpus dir. Source: content-ideas/scripts/graphify-pro.'

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
  if [ -f "$f" ] && grep -q "$MARK" "$f"; then echo "present: $f"; return; fi
  { [ -s "$f" ] && printf '\n'; printf '# graphify\n%s\n' "$RULE"; } >> "$f"
  echo "added:   $f"
}
add_rule "$HOME/.claude/CLAUDE.md"
add_rule "$HOME/.codex/AGENTS.md"
add_rule "$WIN_HOME/.claude/CLAUDE.md"
add_rule "$WIN_HOME/.codex/AGENTS.md"
add_rule "$WIN_HOME/.gemini/GEMINI.md"
