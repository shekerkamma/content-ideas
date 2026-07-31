# Competitor Analysis Quality Gates

Use this checklist before a competitor-analysis artifact is called client-ready.

## Story Quality

- The first substantive slide/section answers the executive question.
- The method is visible: competitor arenas, rubric, scoring logic, and source confidence.
- Competitors are grouped by buyer job and threat model, not by alphabetical order or vendor category marketing.
- The analysis includes a threat-priority view, not only a comparison matrix.
- The final recommendation follows from the heatmap, battlecards, proof gaps, and roadmap.

## Research Quality

- GBrain or durable memory recall is attempted before external research when available.
- Primary/company sources are preferred for product, pricing, positioning, customer, and funding claims.
- Specialist research tools are used before generic search.
- Every important claim has one of: source citation, confidence label, or explicit assumption.
- Current facts that can change, such as funding, leadership, product scope, or pricing, are verified close to delivery time.

## Differentiation Quality

The final answer must state:

- where the target wins today
- where incumbents can compress or commoditize the position
- which proof would change buyer confidence
- whether the target should compete, partner, attach, or avoid each arena

## Deck Quality

- Native PPTX uses the branded template/workflow.
- Slide count meets the user requirement.
- Every slide has structured content and an action title.
- No client-facing slide exposes internal process terms, file paths, raw prompts, or tool logs unless the user asked for an audit appendix.
- Preview/contact sheets show no obvious overlap, off-slide text, or unreadable dense tables.
- OfficeCLI QA or equivalent real-render QA is passed before using `reviewed`.

## HTML Quality

- The HTML page is self-contained unless the user asks for a framework app.
- Navigation tabs and sections match one-to-one.
- Playwright or equivalent browser validation activates every tab and reaches the final recommendation.
- The published URL is verified after deployment with a cache-busting query string.

## Delivery Quality

- Final response includes local paths, Windows paths when relevant, public URL when published, QA status, and artifact status.
- If a required gate is skipped or unavailable, status is `draft` or `blocked`, not `reviewed`.
