#!/usr/bin/env bash
set -euo pipefail

# Cross-host installer for the governed client-presentation pipeline.
# Repo-local skills/ is the canonical source; host directories are installations.

REPO_ROOT="${CONTENT_IDEAS_ROOT:-/home/sheke/content-ideas}"
HOST_MANIFEST="${PRESENTATION_HOST_MANIFEST:-$REPO_ROOT/config/presentation-pipeline-hosts.json}"
CLAUDE_SKILLS_ROOT="${CLAUDE_SKILLS_ROOT:-/home/sheke/.claude/skills}"
HERMES_SKILLS_ROOT="${HERMES_SKILLS_ROOT:-/mnt/c/Users/sheke/AppData/Local/hermes/skills}"
ANTIGRAVITY_SKILLS_ROOT="${ANTIGRAVITY_SKILLS_ROOT:-/mnt/c/Users/sheke/.agent/skills}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

mapfile -t SKILLS < <(python3 - "$HOST_MANIFEST" <<'PY'
import json
import pathlib
import sys

manifest = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
for skill in manifest["skills"]:
    print(skill)
PY
)
test "${#SKILLS[@]}" -gt 0 || { echo "empty skill bundle: $HOST_MANIFEST" >&2; exit 1; }

validate_source() {
  local name="$1"
  local source="$REPO_ROOT/skills/$name"
  test -f "$source/SKILL.md" || {
    echo "missing canonical skill: $source/SKILL.md" >&2
    return 1
  }
  if find "$source" -type f \( -name '*.pyc' -o -name '.env' \) -print -quit | grep -q .; then
    echo "forbidden generated/secret file in $source" >&2
    return 1
  fi
  python3 - "$source" <<'PY'
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
binary_suffixes = {".gif", ".ico", ".jpeg", ".jpg", ".pdf", ".png", ".pptx", ".webp", ".woff", ".woff2"}
bad = []
for path in root.rglob("*"):
    if not path.is_file() or path.suffix.lower() in binary_suffixes:
        continue
    if "node_modules" in path.parts or "assets" in path.parts:
        continue
    if b"\0" in path.read_bytes():
        bad.append(str(path))
if bad:
    raise SystemExit("invalid NUL byte in text source: " + ", ".join(bad))
PY
}

install_one() {
  local name="$1"
  local root="$2"
  local host_label="$3"
  local source="$REPO_ROOT/skills/$name"
  local target="$root/$name"
  local backup_root="$root/.content-ideas-backups/$STAMP"

  mkdir -p "$root"
  if test -d "$target"; then
    if diff -qr --exclude='__pycache__' --exclude='*.pyc' "$source" "$target" >/dev/null; then
      echo "$host_label: unchanged $name"
      return 0
    fi
    mkdir -p "$backup_root"
    mv "$target" "$backup_root/$name"
    echo "$host_label: backed up $name -> $backup_root/$name"
  fi

  mkdir -p "$target"
  rsync -a --exclude='__pycache__/' --exclude='*.pyc' --exclude='.env' "$source/" "$target/"
  diff -qr --exclude='__pycache__' --exclude='*.pyc' "$source" "$target" >/dev/null
  echo "$host_label: installed $name"
}

for skill in "${SKILLS[@]}"; do
  validate_source "$skill"
done

for skill in "${SKILLS[@]}"; do
  install_one "$skill" "$CLAUDE_SKILLS_ROOT" "claude-code"
  install_one "$skill" "$HERMES_SKILLS_ROOT" "hermes-windows"
  install_one "$skill" "$ANTIGRAVITY_SKILLS_ROOT" "antigravity-windows"
done

echo "cross-host presentation pipeline synchronized"
echo "canonical=$REPO_ROOT/skills"
echo "claude=$CLAUDE_SKILLS_ROOT"
echo "hermes=$HERMES_SKILLS_ROOT"
echo "antigravity=$ANTIGRAVITY_SKILLS_ROOT"
echo "manifest=$HOST_MANIFEST"
