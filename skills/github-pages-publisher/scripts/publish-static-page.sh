#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Publish a static HTML artifact to GitHub Pages, matching the repo's actual Pages mode.

Usage:
  publish-static-page.sh --source <file-or-dir> --slug <url-path> [--repo owner/name] [--remote origin]

Examples:
  publish-static-page.sh \
    --source runs/2026-07-14-beacon-li-competitor-analysis/client-package/pages/beacon-li-competitor-analysis \
    --slug beacon-li-competitor-analysis

  publish-static-page.sh \
    --source runs/.../client-package/site/index.html \
    --slug beacon-li-competitor-analysis
EOF
}

die() {
  echo "error: $*" >&2
  exit 1
}

SOURCE=""
SLUG=""
REPO=""
REMOTE="origin"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) SOURCE="${2:-}"; shift 2 ;;
    --slug) SLUG="${2:-}"; shift 2 ;;
    --repo) REPO="${2:-}"; shift 2 ;;
    --remote) REMOTE="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

[[ -n "$SOURCE" ]] || die "--source is required"
[[ -n "$SLUG" ]] || die "--slug is required"
[[ -e "$SOURCE" ]] || die "source does not exist: $SOURCE"
command -v gh >/dev/null || die "gh CLI is required"
command -v git >/dev/null || die "git is required"
command -v python3 >/dev/null || die "python3 is required"
command -v curl >/dev/null || die "curl is required"

if [[ -z "$REPO" ]]; then
  REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
fi
[[ -n "$REPO" ]] || die "could not infer repo; pass --repo owner/name"

PAGES_JSON="$(gh api "repos/$REPO/pages")"
BUILD_TYPE="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("build_type",""))' <<<"$PAGES_JSON")"
HTML_URL="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("html_url","").rstrip("/"))' <<<"$PAGES_JSON")"
SOURCE_BRANCH="$(python3 -c 'import json,sys; print((json.load(sys.stdin).get("source") or {}).get("branch",""))' <<<"$PAGES_JSON")"
SOURCE_PATH="$(python3 -c 'import json,sys; print((json.load(sys.stdin).get("source") or {}).get("path","/"))' <<<"$PAGES_JSON")"

[[ -n "$HTML_URL" ]] || die "GitHub Pages has no html_url for $REPO"

if [[ "$BUILD_TYPE" != "legacy" ]]; then
  die "Pages build_type is '$BUILD_TYPE'. Add/use a repo-default workflow publisher for Actions Pages; this script currently handles legacy branch Pages safely."
fi

[[ -n "$SOURCE_BRANCH" ]] || die "Pages legacy source branch is missing"

ROOT="$(git rev-parse --show-toplevel)"
TMP_PARENT="${TMPDIR:-/tmp}"
WORKTREE="$(mktemp -d "$TMP_PARENT/pages-publish.XXXXXX")"
cleanup() {
  git -C "$ROOT" worktree remove --force "$WORKTREE" >/dev/null 2>&1 || true
}
trap cleanup EXIT

git -C "$ROOT" fetch "$REMOTE" "$SOURCE_BRANCH"
git -C "$ROOT" worktree add "$WORKTREE" "$REMOTE/$SOURCE_BRANCH" >/dev/null

TARGET_ROOT="$WORKTREE"
if [[ "$SOURCE_PATH" != "/" ]]; then
  TARGET_ROOT="$WORKTREE/${SOURCE_PATH#/}"
fi
TARGET_DIR="$TARGET_ROOT/$SLUG"
mkdir -p "$TARGET_DIR"

if [[ -d "$SOURCE" ]]; then
  cp -R "$SOURCE"/. "$TARGET_DIR"/
else
  cp "$SOURCE" "$TARGET_DIR/index.html"
fi

touch "$WORKTREE/.nojekyll"

if git -C "$WORKTREE" diff --quiet -- "$TARGET_DIR" "$WORKTREE/.nojekyll"; then
  echo "No Pages changes to publish for $SLUG"
else
  git -C "$WORKTREE" add "$TARGET_DIR" "$WORKTREE/.nojekyll"
  git -C "$WORKTREE" commit -m "Publish $SLUG"
  git -C "$WORKTREE" push "$REMOTE" "HEAD:$SOURCE_BRANCH"
fi

COMMIT="$(git -C "$WORKTREE" rev-parse --short HEAD)"
URL="$HTML_URL/$SLUG/?v=$COMMIT"
STATUS="$(curl -L --fail --silent --show-error -o /tmp/pages-publish-check.html -w '%{http_code}' "$URL")"
[[ "$STATUS" == "200" ]] || die "published URL verification failed: HTTP $STATUS $URL"

echo "Published: $URL"
echo "Commit: $COMMIT"
