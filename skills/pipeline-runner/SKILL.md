---
name: pipeline-runner
version: "1.1.0"
description: >
  Run a use case from /content-ideas through the AI strategy and pre-sales
  pipeline. Reads use cases from the latest feed-data.json, lets the user pick
  one, then chains through: content-research → vertical-scorer →
  ai-strategy-brief → branded-pptx-deck → research-to-strategy →
  presales-deal-prep. Each stage produces a deliverable and gates the next.
  Use when the user picks a use case to pursue, says "run the pipeline", or
  wants to go from signal to deal prep.
argument-hint: "[use case number, name, or 'list']"
user-invocable: true
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# pipeline-runner

Chains a use case hypothesis from `/content-ideas` through the AI strategy and
pre-sales pipeline. Each stage produces a deliverable and gates the next —
a PASS verdict at Stage 2 stops the pipeline early, saving time.

The pipeline consumes existing skills as-is via their slash commands. No
business logic lives here — this is pure orchestration.

---

## Stage 0: Load use case

Resolve `$CONTENT_HOME` (default `~/Documents/Content`). Find the most recent
dated subfolder of `$CONTENT_HOME/research/` that contains a `feed-data.json`
with a `useCases` array. If none exists, tell the user to run `/content-ideas`
first (in strategy mode — their Content Goal must mention strategy/pre-sales).

Parse `useCases[]`. If the user passed a number as an argument, pick that
index (1-based). If they passed a name, fuzzy-match against `title`. If no
argument or `"list"`, present the numbered list:

> **Use cases from {date} feed:**
> 1. {title} ({confidence}, {len(signals)} signals)
> 2. ...
>
> Pick a number to run the pipeline.

Once selected, confirm:

> **Running pipeline for:** {title}
> **Hypothesis:** {hypothesis}
> **Signals:** {count} posts, {count} patterns
> **Suggested prospects:** {orgs joined}
>
> Proceed? / Pick a different one / Add a prospect

---

## Stage 1: Content Research (augment the use case)

Search for the best available sources on the use case topic across YouTube,
web articles, GitHub repos, and documentation. Select 4-6 high-signal sources
covering:

1. **Architecture/deployment** — how this is built in production
2. **Market landscape** — who is winning, funding, valuations
3. **Compliance/regulation** — what governs this space
4. **Integration points** — what systems it connects to
5. **Open-source alternatives** — self-hostable options

If the host exposes stronger research plugins such as `exa`, prefer them for
discovery in this stage so official product pages, docs, GitHub repos,
competitive/vendor signals, and current operator proof points are found faster
and with less search noise than generic web search alone.

In terminal-first hosts such as Codex CLI, prefer the closest equivalent:
an MCP-connected research server or a local CLI/API wrapper for tools such as
Exa when available. Treat that as the terminal analogue to desktop plugin
access.

Codex Desktop plugin access is a discovery advantage, not an exception to the
pipeline contract. The same local artifact-generation, branded-deck, QA,
repo-rule, and source-verification requirements still apply.

Plugin-assisted research does **not** replace:
- local file generation
- branded PPTX build and QA
- repo-specific workflow rules
- verifying that final cited sources are primary and current

If the use case involves agent orchestration, coding automation, MCP servers,
skills, or OpenHands is named in the source material, include the OpenHands
GitHub repo and docs in the Stage 1 source set and treat them as the source of
truth for implementation details:
- `https://github.com/OpenHands/OpenHands`
- `https://docs.openhands.dev/`

Use those sources to upgrade `stack[]`, architecture notes, and implementation
snippets with verified OpenHands primitives rather than generic agent-platform
descriptions.

Run `/content-research` with the selected URLs. This produces:

- Second-brain notes in `~/projects/hyundai-peopletech-deck/second-brain/`
- Obsidian vault entries in `/mnt/c/Users/sheke/Documents/hyundai-ai-vault/content-research/`
- Knowledge graph entries via `/graphify`

After research completes, **update the use case** in `feed-data.json`:

- Upgrade `stats[]` with research-backed numbers (not estimates)
- Upgrade `stack[]` with specific vendor/technology names
- Add new `signals[]` entries from the research sources
- Add new `patterns[]` from cross-source analysis
- Expand `sourceUrls[]` with all researched URLs
- Upgrade `confidence` if signal count increased (3+ = high)

Print status:

```
PIPELINE: {title}
═══════════════════════════════════════
  ✓ Content Research  {count} sources → second-brain + feed-data updated
  ◻ Vertical Score    (pending)
  ◻ Strategy Brief    (pending)
  ◻ PPTX Deck         (pending)
  ◻ Full Strategy     (pending)
  ◻ Deal Prep         (pending)
```

---

## Stage 2: Vertical Scorer (GO/WAIT/PASS gate)

Invoke `/vertical-scorer "{verticalName}"`.

The scorer now benefits from the research gathered in Stage 1 — source URLs
and second-brain notes provide grounded evidence for each scoring dimension.

This is a **gate**:
- **GO** (score 25+/35) → proceed automatically to Stage 3.
- **WAIT/CONDITIONAL** (score 18–24) → warn the user, ask whether to continue.
- **PASS** (score <18) → stop the pipeline. Report the verdict and suggest the
  user pick a different use case or refine the vertical.

Print status:

```
PIPELINE: {title}
═══════════════════════════════════════
  ✓ Content Research  {count} sources
  ✓ Vertical Score    {score}/35 — {verdict}
  ◻ Strategy Brief    (pending)
  ◻ PPTX Deck         (pending)
  ◻ Full Strategy     (pending)
  ◻ Deal Prep         (pending)
```

---

## Stage 3: AI Strategy Brief

Invoke `/ai-strategy-brief "{verticalName}"`.

Pass the hypothesis, source URLs, and second-brain note paths as additional
context so the brief is grounded in the research from Stage 1, not just
web search. The brief should reference the specific market data, competitor
landscape, and cost figures from the research notes.

When the brief is produced, update status:

```
PIPELINE: {title}
═══════════════════════════════════════
  ✓ Content Research  {count} sources
  ✓ Vertical Score    {score}/35 — {verdict}
  ✓ Strategy Brief    {filename}.docx
  ◻ PPTX Deck         (pending)
  ◻ Full Strategy     (pending)
  ◻ Deal Prep         (pending)
```

---

## Stage 4: Branded PPTX Deck

Invoke `/branded-pptx-deck` to generate a multi-slide presentation from the
use case data. The deck uses `pptxkit` from the branded-pptx-deck skill and
follows the Canva-adapted use case realization layout.

This is a hard requirement for client-facing output. Always use the branded
PowerPoint template workflow (`/branded-pptx-deck`, backed by
`/home/shekerk/.claude/templates/branded-template.pptx` in this environment).
Do **not** substitute a hand-built `python-pptx` deck or a blank presentation
theme for external/client delivery. If the branded workflow is unavailable,
stop and report the deck stage as blocked.

Every slide in the deck must carry structured content, not sparse placeholders.
At minimum:
- action-title cover with premise + evidence anchors
- detailed use-case realization slide in the branded layout
- structured market/proof slide
- structured architecture/stack slide
- structured scorecard or risk/controls slide
- structured roadmap/next-step slide

PPTX QA is required before this stage is considered complete:
- `Deck.save()` / branded builder validation must pass
- text overlap, overflow, and collisions must be checked
- if `preview_pptx.py` is available, review the contact-sheet output
- if preview tooling is unavailable, report the deck as unreviewed for visual QA
  rather than presenting it as final client-ready output
- use explicit deck status: `draft`, `reviewed`, or `blocked`
- keep the branded builder script with the run artifacts so QA fixes are reproducible
- deliver the `reviewed` filename, not an earlier draft
- visual QA checklist:
  - no red overflow boxes in `preview_pptx.py`
  - no title/subtitle collisions
  - no clipped text in stat bars, callout strips, or side panels
  - footer/page number present on each slide

**Slides to generate:**

1. **Cover** — title, premise, date, source count, vertical score
2. **Use Case Realization** — the Canva-adapted layout: teal left panel with
   challenge/solution cards, stat boxes, how-it-works, solution stack,
   systems/users bars; navy right strip with organizations
3. **Market Landscape** — who is winning table (from strategy brief research)
4. **Architecture Patterns** — deployment options with cost tiers (from
   content-research notes)
5. **Vertical Scorecard** — 7-dimension score visualization with bars
6. **Risks & Controls** — failure modes and mitigations
7. **90-Day Roadmap** — phased entry plan
8. **Closing** — bottom line takeaways

The deck pulls data from:
- `feed-data.json` useCases[] → slides 1-2
- Content-research second-brain notes → slides 3-4
- Vertical scorer output → slide 5
- Strategy brief research → slides 6-7
- All of the above → slide 8

Save to: `$CONTENT_HOME/research/{date}/{topic-slug}-deck.pptx`
Copy to: `/mnt/c/Users/sheke/OneDrive/Desktop/` for Windows access.

Recommended filename convention:
- `{topic-slug}-deck-draft.pptx` while content/layout is still changing
- `{topic-slug}-deck-reviewed.pptx` after visual QA passes
- `{topic-slug}-deck-blocked.txt` if the PPTX stage cannot be completed cleanly

Update status:

```
PIPELINE: {title}
═══════════════════════════════════════
  ✓ Content Research  {count} sources
  ✓ Vertical Score    {score}/35 — {verdict}
  ✓ Strategy Brief    {filename}.docx
  ✓ PPTX Deck         {filename}.pptx
  ◻ Full Strategy     (pending)
  ◻ Deal Prep         (pending)
```

---

## Stage 5: Research-to-Strategy (optional, user-gated)

Ask: "Generate full strategy research + council + deck? This takes 5–10
minutes and produces a 30-page research doc, knowledge graph, and slide deck."

Options: **Yes — run it** / **Skip — move to deal prep** / **Stop here**

If yes, invoke `/research-to-strategy "{verticalName}" {sourceUrls joined by space}`.

Update status on completion.

---

## Stage 6: Pre-Sales Deal Prep (optional, per prospect)

Ask: "Prep for a specific prospect?" Show the `orgs` from the use case, plus
an option to type a different company name.

If the user picks one, invoke `/presales-deal-prep "{prospectName}"`.

The strategy brief, deck, and vertical context are already in the
conversation, so the deal prep skill can reference them.

Update final status:

```
PIPELINE: {title}
═══════════════════════════════════════
  ✓ Content Research  {count} sources
  ✓ Vertical Score    {score}/35 — {verdict}
  ✓ Strategy Brief    {filename}.docx
  ✓ PPTX Deck         {filename}.pptx
  ✓ Full Strategy     {filename}.pptx + research.md
  ✓ Deal Prep         {prospect}-deal-prep.md
```

---

## Notes

- **No downstream skills are modified.** This skill invokes `/content-research`,
  `/vertical-scorer`, `/ai-strategy-brief`, `/branded-pptx-deck`,
  `/research-to-strategy`, and `/presales-deal-prep` exactly as a human would —
  by their slash commands with string arguments.
- **Content research is the foundation.** Stage 1 grounds every subsequent stage
  in real data — the scorer uses researched evidence, the brief cites specific
  numbers, the deck renders verified facts, and deal prep references actual
  market players. Without it, downstream stages rely on web search alone.
- **Re-runnable.** The user can run `/pipeline-runner` on the same use case
  again (e.g., to add a second prospect in Stage 6) without re-running the
  scraper.
- **Multiple use cases.** The user can run `/pipeline-runner 1`, then
  `/pipeline-runner 2` in the same session to evaluate multiple verticals.
- **Direct skill invocation.** The user can skip the pipeline and invoke any
  downstream skill directly: `/vertical-scorer "On-premise LLM for healthcare"`
  works standalone. The pipeline is a convenience, not a requirement.
- **Stage skipping.** If the user has already run `/content-research` for this
  topic in a prior session, Stage 1 can be skipped — check if second-brain
  notes already exist for the use case's `verticalName` before re-researching.
