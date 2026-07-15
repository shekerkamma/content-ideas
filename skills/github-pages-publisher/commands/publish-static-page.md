# publish-static-page — Publish Static HTML To GitHub Pages

Publish a static HTML report/page to GitHub Pages without manually handling `gh-pages`
worktrees, commits, pushes, or cache-busted verification URLs.

## Usage

```text
/publish-static-page --source <file-or-dir> --slug <url-path>
```

Examples:

```text
/publish-static-page --source runs/2026-07-14-beacon-li-competitor-analysis/client-package/pages/beacon-li-competitor-analysis --slug beacon-li-competitor-analysis
```

```text
/publish-static-page --source runs/<run>/client-package/site/index.html --slug <report-slug>
```

## Procedure

Load and use the `github-pages-publisher` skill.

If the user did not provide `--source` or `--slug`, ask for the missing value.

Run the publisher script from the installed global skill when available:

```bash
~/.claude/skills/github-pages-publisher/scripts/publish-static-page.sh \
  --source <file-or-dir> \
  --slug <url-path>
```

If running in Codex and the Claude skill path is unavailable, use:

```bash
~/.codex/skills/github-pages-publisher/scripts/publish-static-page.sh \
  --source <file-or-dir> \
  --slug <url-path>
```

Report:

- live URL
- publish commit
- HTTP verification result
