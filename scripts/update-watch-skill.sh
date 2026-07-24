#!/usr/bin/env bash
# Sync the user's claude-video fork from upstream, then install the watch skill
# into Claude Code, Codex, and Windows Antigravity/Gemini skill roots.
set -euo pipefail

FORK_REPO="${WATCH_FORK_REPO:-shekerkamma/claude-video}"
UPSTREAM_REPO="${WATCH_UPSTREAM_REPO:-bradautomates/claude-video}"
REF="${WATCH_REF:-main}"
WIN_USER="${WIN_USER:-sheke}"

tmp="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp"
}
trap cleanup EXIT

say() {
  printf "\n== %s\n" "$*"
}

say "Sync fork from upstream"
if command -v gh >/dev/null 2>&1; then
  gh repo sync "$FORK_REPO" --branch "$REF" --source "$UPSTREAM_REPO"
else
  echo "gh not found; skipping GitHub fork sync and installing from current fork state" >&2
fi

say "Clone fork"
git clone --depth 1 --branch "$REF" "https://github.com/${FORK_REPO}.git" "$tmp/claude-video"

src="$tmp/claude-video/skills/watch"
if [ ! -f "$src/SKILL.md" ] || [ ! -f "$src/scripts/watch.py" ]; then
  echo "ERROR: expected watch skill not found at $src" >&2
  exit 1
fi

say "Install watch skill"
targets=(
  "$HOME/.claude/skills/watch"
  "/mnt/c/Users/${WIN_USER}/.gemini/antigravity/skills/watch"
  "/mnt/c/Users/${WIN_USER}/.gemini/config/skills/watch"
)

for dest in "${targets[@]}"; do
  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  cp -a "$src" "$dest"
  echo "installed $dest"
done

mkdir -p "$HOME/.codex/skills" "$HOME/content-ideas/skills"
rm -f "$HOME/.codex/skills/watch" "$HOME/content-ideas/skills/watch"
ln -s "$HOME/.claude/skills/watch" "$HOME/.codex/skills/watch"
ln -s "$HOME/.claude/skills/watch" "$HOME/content-ideas/skills/watch"

say "Verify"
PYTHONPYCACHEPREFIX="${TMPDIR:-/tmp}/watch-pycache" \
  python3 -m py_compile "$HOME/.claude/skills/watch/scripts/"*.py
python3 "$HOME/.claude/skills/watch/scripts/setup.py" --json

echo
echo "Done. Restart Claude Code, Codex, and Antigravity/Gemini to reload watch."
