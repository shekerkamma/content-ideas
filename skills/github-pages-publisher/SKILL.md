---
name: github-pages-publisher
description: Use when publishing a static HTML artifact from this repo to GitHub Pages. Handles legacy gh-pages branch publishing without manually creating worktrees, commits, pushes, or cache-busted verification URLs.
trigger: /publish-static-page
argument-hint: "--source <file-or-dir> --slug <url-path> [--repo owner/name]"
---

# GitHub Pages Publisher

Use this skill when the user asks to publish, deploy, or share a static HTML report through GitHub Pages.

## Default Command

Prefer the bundled utility from this skill:

```bash
skills/github-pages-publisher/scripts/publish-static-page.sh \
  --source <file-or-directory> \
  --slug <url-path>
```

If the bundled script is not present in the active repo but this skill is installed globally, run the global skill copy:

```bash
~/.codex/skills/github-pages-publisher/scripts/publish-static-page.sh \
  --source <file-or-directory> \
  --slug <url-path>
```

Claude-hosted sessions may also have the same script at:

```bash
~/.claude/skills/github-pages-publisher/scripts/publish-static-page.sh
```

Examples:

```bash
skills/github-pages-publisher/scripts/publish-static-page.sh \
  --source runs/2026-07-14-beacon-li-competitor-analysis/client-package/pages/beacon-li-competitor-analysis \
  --slug beacon-li-competitor-analysis
```

```bash
skills/github-pages-publisher/scripts/publish-static-page.sh \
  --source runs/<run>/client-package/site/index.html \
  --slug <report-slug>
```

## What The Script Does

- Reads the repository's real Pages configuration through `gh api repos/<owner>/<repo>/pages`.
- Detects legacy `gh-pages` branch publishing.
- Creates a temporary worktree for the Pages branch.
- Copies a file as `<slug>/index.html` or a directory into `<slug>/`.
- Commits only the static page artifact on the Pages branch.
- Pushes the Pages branch.
- Verifies the published URL with a cache-busting commit query.

## Rules

- Do not assume a feature-branch workflow can publish Pages. Check the repo's Pages config first.
- Do not hand-manage stale `/tmp/*gh-pages*` worktrees when the script can create and clean one.
- Do not stage unrelated workspace changes to publish a static page.
- If the script reports Actions Pages mode, use or add a repo-default workflow publisher rather than forcing legacy branch publishing.
- Final response must include the live URL, publish commit, and HTTP verification result.

## Slash Usage

Use:

```text
/publish-static-page --source <file-or-dir> --slug <url-path>
```

If arguments are missing, ask for:

- source HTML file or directory
- slug / URL path
- repo owner/name only when it cannot be inferred by `gh repo view`

## Current Repo Note

At the time this skill was added, `shekerkamma/content-ideas` uses legacy GitHub Pages:

- source branch: `gh-pages`
- source path: `/`
- base URL: `https://shekerkamma.github.io/content-ideas/`

The utility is intentionally config-driven so it does not hard-code those values.
