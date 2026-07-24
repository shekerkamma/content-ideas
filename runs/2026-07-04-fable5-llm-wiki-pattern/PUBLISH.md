# Publish The LLM Wiki Agent Demo

The demo is safe to publish because it is static HTML/CSS/JS. It does not expose
local files, API keys, model calls, or private wiki content.

## Option 1: GitHub Pages Workflow

This repo includes a manual workflow:

- `.github/workflows/llm-wiki-agent-demo-pages.yml`

To publish:

1. Commit this run folder and the workflow.
2. Push to GitHub.
3. In the GitHub repo, open `Settings -> Pages`.
4. Set `Build and deployment -> Source` to `GitHub Actions`.
5. Open `Actions -> Publish LLM Wiki Agent Demo`.
6. Click `Run workflow`.

The workflow publishes only:

```text
runs/2026-07-04-fable5-llm-wiki-pattern/interactive-demo/
```

## Option 2: Any Static Host

Upload the contents of this folder:

```text
runs/2026-07-04-fable5-llm-wiki-pattern/interactive-demo/
```

to any static host:

- GitHub Pages
- Netlify
- Vercel static deployment
- Cloudflare Pages
- internal static web server

The entry point is:

```text
index.html
```

## Suggested Positioning

LLM Wiki Agent is a model-neutral markdown second-brain workflow for Codex and
Claude Code. It uses raw sources, generated wiki pages, index routing, operation
logs, backlinks, and progressive-disclosure querying.

## Static Demo vs Local Agent

The published demo is for education and sharing. The real local agent workflow
lives in:

```text
skills/llm-wiki-agent/
```

Use the static demo to explain the workflow. Use the skill and CLI script to
create real wikis.
