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
# - Full repository installs such as gstack get a lightweight Codex wrapper.
#   Its SKILL.md already resolves runtime assets through ~/.claude/skills/gstack,
#   while linking the entire checkout makes Codex recursively scan node_modules
#   and can delay MCP startup long enough for it to be interrupted.
# - Skills whose canonical source is on /mnt/c are copied into Codex's WSL-side
#   installation. Recursively scanning Windows-mounted symlinks blocks session
#   creation and can prevent MCP startup from completing before the UI deadline.
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
    .*|*.corrupt-backup-*|*.incomplete-backup-*) continue ;;
  esac

  if [ -L "$e" ]; then
    target=$(readlink "$e")
  elif [ -d "$e" ]; then
    target="../../.claude/skills/$e"
  else
    continue
  fi

  # Codex requires YAML frontmatter. A readable path alone is insufficient:
  # damaged all-NUL files previously entered the mirror and emitted loader
  # errors on every startup.
  if [ ! -f "$e/SKILL.md" ] || [ "$(head -c 3 "$e/SKILL.md" 2>/dev/null)" != "---" ]; then
    skipped_no_skill=$((skipped_no_skill + 1))
    continue
  fi

  dest="$CODEX_SKILLS/$e"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    skipped_existing=$((skipped_existing + 1))
    continue
  fi

  if [ "$e" = "gstack" ]; then
    mkdir -p "$dest"
    ln -s ../../../.claude/skills/gstack/SKILL.md "$dest/SKILL.md"
    created=$((created + 1))
    echo "linked   $e (lightweight wrapper)"
    continue
  fi

  resolved=$(readlink -f "$e" 2>/dev/null || true)
  case "$resolved" in
    /mnt/c/*)
      cp -aL "$e" "$dest"
      created=$((created + 1))
      echo "copied   $e (WSL-local mirror)"
      continue
      ;;
  esac

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
