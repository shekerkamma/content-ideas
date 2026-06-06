#!/usr/bin/env bash
set -euo pipefail

TARGET_PATH="${1:-second-brain}"
TARGET_PATH="${TARGET_PATH/#\~/$HOME}"

mkdir -p "$TARGET_PATH/raw" "$TARGET_PATH/wiki" "$TARGET_PATH/projects" "$TARGET_PATH/archive"

GITIGNORE="$TARGET_PATH/.gitignore"
touch "$GITIGNORE"
for line in ".DS_Store" "*.swp" "*.tmp"; do
  grep -qxF "$line" "$GITIGNORE" || echo "$line" >> "$GITIGNORE"
done

if [ ! -f "$TARGET_PATH/README.md" ]; then
  cat > "$TARGET_PATH/README.md" <<'INNER'
# My Second Brain

I dump raw stuff into `/raw`. AI turns it into clean notes in `/wiki`.

## Folders

- `/raw` — inbox for captured notes, links, screenshots, PDFs, and scraps
- `/wiki` — clean notes written and maintained by AI
- `/projects` — active work, one folder per project, each with its own README
- `/archive` — processed `/raw` files move here as a permanent record

## The Loop

1. Capture into `/raw`.
2. Run an agent with the prompt in `translate.md`.
3. Read the updated `/wiki`.

The whole folder is a git repo, so nothing is lost.
INNER
fi

if [ ! -f "$TARGET_PATH/AGENTS.md" ]; then
  cat > "$TARGET_PATH/AGENTS.md" <<'INNER'
You are working in a personal second brain — a knowledge management system, not a code project. Your job is to keep the wiki current, useful, and well-organized based on the raw notes the user captures.

Read `README.md` first. This is the source of truth for the system.

## Common Tasks

- Translate raw: run the prompt in `translate.md` against `/raw`.
- Project digest: summarize a `/projects/<name>/` folder into its README.
- Answer questions: read `/wiki` and `/archive` to answer questions about prior thinking.

## Hard Rules

1. Never delete anything from `/raw` or `/archive`. Move only, never delete.
2. Never overwrite a `/wiki` entry blindly. Always read it first, then merge.
3. Never modify `/archive` after a file lands there.
4. When uncertain, log the uncertainty in the entry instead of guessing.

## Wiki Voice and Structure

- Default tone: clear, factual, terse.
- Preserve the user's phrasing when it carries signal.
- Use headings only when they help.
- Use bullets only when the content is genuinely a list.
- Keep one topic per file with kebab-case filenames.
INNER
fi

if [ ! -f "$TARGET_PATH/CLAUDE.md" ]; then
  cp "$TARGET_PATH/AGENTS.md" "$TARGET_PATH/CLAUDE.md"
fi

if [ ! -f "$TARGET_PATH/translate.md" ]; then
  cat > "$TARGET_PATH/translate.md" <<'INNER'
Translate the contents of `/raw` into durable wiki notes.

Process:

1. Read each new file in `/raw`.
2. Decide whether it belongs in an existing wiki note or a new one in `/wiki`.
3. If the target wiki note already exists, read it first and merge carefully.
4. Preserve distinctive phrasing from the source when it adds signal.
5. Record uncertainty explicitly instead of inventing details.
6. After processing a raw file, move it into `/archive` without editing its contents.

Output standard:

- Markdown only
- Clear, factual, terse
- One topic per file
- Kebab-case filenames
- No filler summaries
INNER
fi

echo "bootstrapped second brain at $TARGET_PATH"
