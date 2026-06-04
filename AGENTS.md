OpenHands implementation source of truth for strategy/pipeline builds:
- https://github.com/OpenHands/OpenHands
- https://docs.openhands.dev/

GBrain knowledge rule:
- If `gbrain` is available as an MCP server in Claude Code, Codex, or another
  host, use it by default for cross-session memory and retrieval before
  repeating strategy or pipeline research from scratch.
- Use GBrain as the durable knowledge layer for recurring prospects,
  companies, people, verticals, themes, prior research, and named accounts.
- Treat GBrain retrieval as embedding-backed semantic retrieval by default, not
  just keyword lookup.
- Prefer semantic recall first; use synthesis only when the task needs merged
  interpretation rather than simple recall.
- Read from GBrain first when the task references a company, person, vertical,
  or use case that may have appeared in prior runs.
- Write durable findings back to GBrain after strategy/pipeline work when they
  are likely to matter again across sessions.
- GBrain is not the system of record for deliverables.
- Pipeline artifacts, briefs, decks, feed data, and client-facing outputs must
  still be written to local repo/run files.

Research-plugin rule:
- In Codex Desktop or any host that exposes high-quality research plugins
  such as `exa`, prefer those plugins for source discovery and current web
  research during Stage 1 and strategy work.
- In terminal-first hosts such as Codex CLI, prefer the closest equivalent:
  an MCP-connected research server or a local CLI/API wrapper for tools such as
  Exa when available.
- Concrete terminal patterns to prefer when available:
  - Exa MCP over HTTP/remote MCP
  - a local Exa API wrapper that calls `https://api.exa.ai/search`
- Use them to improve discovery of official product pages, docs, GitHub repos,
  competitive signals, and current operator proof points.
- Codex Desktop plugin access is an advantage for discovery, not an exception
  to the repo workflow. The same delivery and verification rules still apply.
- This does not replace:
  - local file generation
  - branded PPTX build and QA
  - repo-specific workflow rules
  - verifying that final sources are primary and current

Client-facing PPTX rule:
- Always use the branded PowerPoint template resolved from
  `BRANDED_PPTX_TEMPLATE`, or fall back to
  `~/.claude/templates/branded-template.pptx` when that env var is unset
- Or use the `branded-pptx-deck` / `pptxkit` workflow that wraps that template
- Never ship a client-facing `.pptx` built from an ad hoc blank presentation
- Every slide must have structured content, not placeholder filler
- Use the branded detailed use-case realization layout when presenting a use case
- PPTX QA is mandatory before delivery
- Check text overlap/overflow/collisions before calling a deck final
- If branded preview tooling is unavailable, mark the deck unreviewed rather than silently delivering it
- Use explicit deck status: `draft`, `reviewed`, or `blocked`
- Use matching filename suffixes for deliverables
- Keep the branded builder script with the run artifacts so QA fixes are reproducible
- Copy reviewed decks only to a delivery destination resolved from
  `CLIENT_DELIVERY_DIR` when one is configured for the host

@CLAUDE.md
