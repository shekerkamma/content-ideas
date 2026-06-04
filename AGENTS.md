OpenHands implementation source of truth for strategy/pipeline builds:
- https://github.com/OpenHands/OpenHands
- https://docs.openhands.dev/

Research-plugin rule:
- In Codex Desktop or any host that exposes high-quality research plugins
  such as `exa`, prefer those plugins for source discovery and current web
  research during Stage 1 and strategy work.
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
- Always use the branded PowerPoint template at
  `/home/shekerk/.claude/templates/branded-template.pptx`
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

@CLAUDE.md
