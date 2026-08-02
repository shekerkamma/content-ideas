#!/usr/bin/env bash
# sync-codex-skills.sh — mirror every valid entry in ~/.claude/skills into
# ~/.codex/skills so Codex discovers the same skill set as Claude Code.
# Usage: bash scripts/sync-codex-skills.sh
#
# Codex's global skill discovery is a flat directory scan of ~/.codex/skills
# (confirmed: its .system/.codex-system-skills.marker is just an opaque build
# hash, not a registry, and no other file under ~/.codex references skill
# names) — the same model Claude Code uses for ~/.claude/skills. So mirroring
# is just: for every ~/.claude/skills/<name> that resolves to a real
# SKILL.md, make sure ~/.codex/skills/<name> resolves to the same file.
#
# - Entries already symlinked in ~/.claude/skills get the identical symlink
#   target recreated under ~/.codex/skills (same canonical source, not a
#   pointer back into ~/.claude/skills).
# - Plain directories that exist only under ~/.claude/skills (no separate
#   canonical source) get symlinked back to ~/.claude/skills/<name> itself,
#   per this repo's cross-host convention (CLAUDE.md: "Keep Claude-only UI
#   fields as enhancements" — Codex ignores frontmatter fields it doesn't
#   recognize, e.g. allowed-tools).
# - Anything without a readable SKILL.md (dead symlinks, empty scaffold
#   dirs, utility folders like scripts/ or templates/) is skipped, so this
#   never needs a hand-maintained exclude list.
# - Idempotent: entries that already exist under ~/.codex/skills are left
#   untouched (this is how Codex's own MCP-managed session-handoff skill
#   survives a re-run).
set -uo pipefail

CLAUDE_SKILLS="$HOME/.claude/skills"
CODEX_SKILLS="$HOME/.codex/skills"

if [ ! -d "$CLAUDE_SKILLS" ]; then
  echo "error: $CLAUDE_SKILLS not found" >&2
  exit 1
fi
mkdir -p "$CODEX_SKILLS"

created=0
skipped_existing=0
skipped_no_skill=0

cd "$CLAUDE_SKILLS"
for e in *; do
  # dotfiles/dirs (.system, etc.) and non-skill top-level files (voice.md)
  case "$e" in
    .*) continue ;;
  esac

  if [ -L "$e" ]; then
    target=$(readlink "$e")
  elif [ -d "$e" ]; then
    target="../../.claude/skills/$e"
  else
    continue
  fi

  if [ ! -f "$e/SKILL.md" ]; then
    skipped_no_skill=$((skipped_no_skill + 1))
    continue
  fi

  dest="$CODEX_SKILLS/$e"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    skipped_existing=$((skipped_existing + 1))
    continue
  fi

  ln -s "$target" "$dest"
  if [ -f "$dest/SKILL.md" ]; then
    created=$((created + 1))
    echo "linked   $e"
  else
    echo "FAILED   $e -> $target (does not resolve, removing)" >&2
    rm -f "$dest"
  fi
done

echo
echo "created=$created skipped_existing=$skipped_existing skipped_no_skill=$skipped_no_skill"
