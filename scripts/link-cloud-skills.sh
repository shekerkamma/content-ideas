#!/usr/bin/env bash
# Expose the repo's skills/ in Claude Code cloud sessions.
#
# Cloud containers start with no plugins installed, so the content-ideas
# plugin (which serves skills/) never loads there. This links each skill into
# ~/.claude/skills, which Claude Code picks up live. It runs only when
# CLAUDE_CODE_REMOTE=true, so local checkouts that install the plugin don't
# load every skill twice.
set -euo pipefail

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest="$HOME/.claude/skills"
mkdir -p "$dest"

for dir in "$repo"/skills/*/; do
  name="$(basename "$dir")"
  [ -f "$dir/SKILL.md" ] || continue
  # .claude/skills already serves this name; skip it to avoid a duplicate.
  [ -e "$repo/.claude/skills/$name" ] && continue
  # Leave real (non-symlink) skills already in ~/.claude/skills alone.
  [ -e "$dest/$name" ] && [ ! -L "$dest/$name" ] && continue
  ln -sfn "${dir%/}" "$dest/$name"
done
