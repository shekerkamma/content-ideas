# Deck brief

## Audience

A technical/ops leader deciding whether and how to formalize their team's ad hoc AI
workflows into managed multi-agent systems. Assumed familiar with using AI chat tools
day-to-day; not assumed familiar with LangGraph/AutoGen internals or the "graph
engineering" trend discourse.

## Decision

Adopt the six-condition qualifying test before reaching for any orchestration framework,
and start the next AI workflow as a manual first rep (whiteboard jobs + arrows, run once
by hand) rather than a tooling purchase.

## Narrative promise

Structuring AI work as an explicit graph of jobs, arrows, and shared state — not a bigger
prompt or a longer chat — is what makes multi-step AI work checkable and trustworthy; the
mechanics are proven in production frameworks today even though the trend label
("graph engineering") is only weeks old and still contested.

## Voice and tone

Confident, practitioner-to-practitioner, plain English. No hype language, no unqualified
trend claims. Where the source material's own framing overstates consensus (see
grill-me-validation.md), soften to "one active framing" rather than "the agreed next step."

## Anti-references

Not a hype/trend deck riding "graph engineering" as a buzzword. Not a framework sales
pitch for any single vendor (LangGraph, AutoGen, n8n, Make are all named neutrally as
options, not endorsed). Not a screenshot dump of the source video's slides — every
extracted visual sits inside a native slide shell with its own action title and
business-implication text.

## Evidence and editability

Evidence standard: transcript-grounded direct evidence for the mechanical claims (slides
5-12, verbatim from the presenter's own slides); Exa-sourced industry reporting for the
hype-context and tool-status claims (slides 3, 13), cited with a footnote. Exact-state
visuals: the 10 presenter slides captured mid-video are exact-source-evidence and are
placed as cropped, webcam-masked PNG extracts (Route 0) — never redrawn as native shapes.
Editability: hybrid editable — native titles/callouts/captions/footers throughout, plus
source-backed PNG evidence on slides 4-12.

## Success criteria

- The slide-title sequence tells the argument by itself.
- Each slide carries one main message and structured supporting evidence.
- The reviewed deck passes context, visual-spec, structural, design-lint, and render QA.
