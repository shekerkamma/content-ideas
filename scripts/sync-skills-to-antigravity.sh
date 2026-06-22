#!/usr/bin/env bash
# Sync selected WSL-canonical skills into the Windows-side Antigravity skills dir.
#
# Antigravity IDE is Windows-native and does NOT support WSL — it cannot read the
# WSL filesystem, so skills must be COPIED to C:\Users\<user>\.agents\skills\.
# Symlinks can't bridge WSL->Windows for a native app, so there is no live
# propagation: re-run this script after editing any listed skill.
#
# Canonical source of truth stays in WSL (~/.claude/skills/... or ~/.agents/skills/...).
# This script is the single place that defines WHICH skills Antigravity gets.
set -euo pipefail

WIN_USER="${WIN_USER:-sheke}"
WIN_SKILLS="${WIN_SKILLS:-/mnt/c/Users/${WIN_USER}/.agents/skills}"

# dest-name = canonical WSL source path. Add skills here to push them to Antigravity.
declare -A SKILLS=(
  [marp]="$HOME/.claude/skills/marp"
  [refero-design]="$HOME/.agents/skills/refero-design"
  [content-ideas]="$HOME/content-ideas/skills/content-ideas"
  [pipeline-runner]="$HOME/content-ideas/skills/pipeline-runner"
)

[ -d "$WIN_SKILLS" ] || { echo "ERROR: Windows skills dir not found: $WIN_SKILLS" >&2; exit 1; }

for name in "${!SKILLS[@]}"; do
  src="${SKILLS[$name]}"
  if [ ! -e "$src" ]; then echo "skip $name (source missing: $src)"; continue; fi
  dest="$WIN_SKILLS/$name"
  rm -rf "$dest"
  # -L resolves symlinks so Windows receives real files, not dangling links.
  cp -rL "$src" "$dest"
  echo "synced $name -> $dest"
done

echo "Done. Restart Antigravity to pick up changes."
