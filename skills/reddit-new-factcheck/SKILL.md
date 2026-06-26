---
name: reddit-new-factcheck
description: Use when someone wants to fact-check a research document, deck, PDF, pasted text, Google Doc text, or selected browser text against Reddit evidence and update the original deck with fact-check annotations.
argument-hint: "[document path or text] [optional Reddit thread URLs/json]"
permissions:
  env:
    - SCRAPECREATORS_API_KEY
    - EXA_API_KEY
  network:
    - https://www.reddit.com
    - https://api.scrapecreators.com
    - https://api.exa.ai
  file_read:
    - runs/
    - /tmp/
  file_write:
    - runs/
    - /tmp/
  shell:
    allowed_scripts:
      - scripts/prepare_factcheck.py
      - scripts/annotate_input_deck.py
      - scripts/old_reddit_evidence.py
---

# reddit-new-factcheck

Use this skill to turn a content research document into a claim-level fact-check
package grounded in Reddit evidence. For slide inputs, the required work product
is an annotated copy of the original PPTX with fact-check marks on the source
slides. Markdown and JSON artifacts remain the audit trail. The original deck is
the canonical deliverable, and any executive summary content must stay inside
that same annotated PPTX. Do not create a separate summary deck by default. It
is for documents, decks, PDFs, uploaded files, pasted text, Google Doc page
text, and browser-selected text. It is not for live streams, YouTube
transcripts, or automated Reddit posting.

## Runtime Preamble

I will fact-check the document against Reddit evidence and update the original
deck with evidence-backed annotations when the input is a PPTX. Reddit is
treated as community/operator evidence, not as the final authority for hard
statistics. Numeric, regulatory, market-size, funding, and date claims must be
marked as requiring primary-source corroboration unless the question is only
whether the claim appears in Reddit discussion.

Raw Reddit search output is not evidence. A post or comment can support a claim
only after it passes the Reddit evidence qualification gate: relevant subreddit
or source context, matching practitioner/persona language, matching workflow
language, and a concrete pain, workaround, objection, or adoption signal. Noisy
keyword matches, generic discussions, celebrity/politics/gaming/movie threads,
or company-name-only mentions must be discarded and reported as rejected.

## Workflow

### Step 1: Normalize The Input

Resolve the input from `$ARGUMENTS`:

- File path: `.md`, `.txt`, `.pptx`, or `.pdf`.
- Pasted text or selected browser text: save it to the run folder as
  `input.txt` before running the helper.
- Google Doc page text: use the selected text/current page text path first. Use
  Drive export only when the user explicitly asks for connector access.

Create a run folder:

```bash
python3 skills/reddit-new-factcheck/scripts/prepare_factcheck.py \
  --input "$DOCUMENT_PATH" \
  --topic "$TOPIC"
```

The helper writes:

- `document-segments.json` - source text split into locators such as slide/page.
- `claim-pack.json` - claim candidates with source locator and Reddit queries.
- `reddit-factcheck-report.md` - report scaffold.

For image-only PPTX files, use adjacent `deck.md`, `<same-name>.md`, or OCR.
If none exists, stop and report that the deck is image-only and needs OCR.
For PDFs, use `pdftotext` when installed. If unavailable, use an approved OCR or
PDF extraction adapter and record that adapter in the report.

### Step 2: Classify Claim Type

For each claim, classify the evidence need:

- `reddit_evidence` - pain, language, sentiment, objections, user experience,
  vendor complaints, community demand, practitioner discussion.
- `primary_required` - percentages, dollar figures, market size, dates,
  regulation, funding, headcount, adoption rates, named company facts.
- `mixed` - a strategic claim that needs primary-source facts plus Reddit
  evidence for market language or adoption pain.

Use Reddit verdict labels, not bare `TRUE` / `FALSE`:

- `Qualified Reddit support`
- `Contradicted by Reddit evidence`
- `Weak qualified Reddit support`
- `No qualified Reddit evidence`
- `Requires primary-source corroboration`

### Step 3: Discover Or Provide Reddit Sources

Preferred order:

1. Use supplied Reddit thread URLs or existing `thread_data.json` files.
2. Use the existing `reddit-seo-pipeline` extractor for each known URL:

   ```bash
   python3 /home/shekerk/.codex/skills/reddit-seo-pipeline/scripts/reddit_thread_extractor.py \
     "$REDDIT_URL" \
     --output "$RUN_DIR/reddit-thread-N.json"
   ```

3. If broad discovery is needed, use the best available Reddit discovery tool:
   `content-outlier-research`, `/last30days`, Exa, ScrapeCreators, or logged-in
   Playwright Reddit search. Do not start with generic web search.
4. If Reddit JSON/API access is blocked but `old.reddit.com` is reachable, use
   the fallback collector:

   ```bash
   python3 skills/reddit-new-factcheck/scripts/old_reddit_evidence.py \
     --claim-pack "$RUN_DIR/claim-pack.json" \
     --out-dir "$RUN_DIR/reddit-evidence-raw" \
     --max-queries 8 \
     --max-threads 10
   ```

   This writes normalized `reddit-thread-*.json` files from real Reddit HTML,
   plus `reddit-discovery-manifest.json`. It is valid Reddit evidence, not
   generic web search, but should be labeled as HTML-extracted.
5. If discovery tools are unavailable, ask for candidate Reddit URLs or produce
   a claim/query pack only.

### Step 4: Build The Evidence Pack

When one or more Reddit JSON files exist, score them against the claim pack:

```bash
python3 skills/reddit-new-factcheck/scripts/prepare_factcheck.py \
  --input "$DOCUMENT_PATH" \
  --topic "$TOPIC" \
  --out-dir "$RUN_DIR" \
  --reddit-json "$RUN_DIR/reddit-thread-1.json"
```

This adds `reddit-evidence-pack.json` and refreshes
`reddit-factcheck-report.md`.

Evidence pack gating requirements:

- Treat collector output as raw discovery, not validated evidence.
- Every accepted evidence item must include qualification metadata showing the
  workflow/persona/pain match.
- Reject threads from unrelated broad/noise subreddits unless the text clearly
  matches the claim's practitioner workflow.
- Reject evidence when the only match is a company name, one generic noun, or a
  broad AI term.
- If no items pass the gate, the claim verdict must be
  `no_qualified_reddit_evidence`, even when raw Reddit results exist.
- For market research decks, explicitly show which verticals have qualified
  Reddit signal and which are unsupported by qualified Reddit data.

### Step 5: Write The Evidence Report

Read `claim-pack.json` and `reddit-evidence-pack.json`, then write a final
`reddit-factcheck-report.md` with:

- document source and extraction method
- claim inventory by source locator
- verdict per claim
- supporting and contradictory Reddit evidence
- top Reddit sources with subreddit/thread/comment metadata when available
- primary-source follow-up list for claims Reddit cannot verify
- methodology and limitations

The Markdown report is not the client-facing endpoint. It is the source artifact
for the annotation pass and the place where dense evidence, limitations, and
source-level details live.

### Step 6: Update The Input Deck With Fact Checks

When the input is a PPTX, create a review copy of the original deck and annotate
the source slides directly. Never overwrite the original file. Do not generate a
standalone summary deck unless the user explicitly asks for one. The annotated
original deck is the only default client-facing artifact.

Default output naming:

```text
<input-slug>-reddit-factchecked-draft.pptx
<input-slug>-reddit-factchecked-reviewed.pptx
```

Use this annotation model:

- Add a small fact-check rail or badge on slides that contain checked claims.
- Use stable claim IDs from `claim-pack.json` (for example, `C-014`) so every
  visual mark traces back to `reddit-factcheck-report.md`.
- Show the Reddit verdict, confidence, and shortest useful rationale on-slide.
- Put source URLs, subreddit/thread/comment metadata, dates, and longer evidence
  excerpts in a per-slide evidence appendix or speaker-note equivalent.
- For image-only decks, preserve the slide image and overlay annotations; do not
  attempt to recreate the original design from scratch.
- For dense slides, add a following "Fact Check Notes" slide rather than
  crowding the original slide.
- Prepend two executive summary slides at the start of the original deck:
  one for verdict counts and evidence coverage, one for the recommended deck
  edits. These slides must read like executive explanation, not like a Reddit
  comment dump, and they must read like client-ready deck content rather than an
  internal notes page.
  The first slide should answer: what Reddit validated, what it did not, and
  what still requires official sourcing.
  The second slide should answer: what to keep, what to rewrite, and what to
  replace with primary-source support.

Client-ready PPTX rule:

- The annotated deck is client-facing only when the branded Canva template is
  available via `BRANDED_PPTX_TEMPLATE` or the fallback template at
  `~/.claude/templates/branded-template.pptx`.
- The annotation pass must fail closed if that template is unavailable.
- Do not produce a client-facing deck from a blank or ad hoc PowerPoint shell.
- Keep the original deck structure, but the prepended summary slides and any
  added fact-check surfaces must follow the branded template contract and use
  the template's executive slide language, not generic utility text.
- Template-native slide generation is required for inserted executive slides.
  Do not approximate the branded look with a MARP export, a plain blank layout,
  or generic utility text blocks. If the branded template contract cannot be
  honored, fail closed instead of falling back to a generic shell.

Fact checks must be evidence-backed, not opinion labels. Each annotation must
come from `reddit-evidence-pack.json` or be explicitly marked
`No Reddit evidence found` / `Requires primary-source corroboration`.

Generate the annotated review copy with:

```bash
python3 skills/reddit-new-factcheck/scripts/annotate_input_deck.py \
  --input-pptx "$DOCUMENT_PATH" \
  --claim-pack "$RUN_DIR/claim-pack.json" \
  --evidence-pack "$RUN_DIR/reddit-evidence-pack.json" \
  --out "$RUN_DIR/<input-slug>-reddit-factchecked-draft.pptx" \
  --summary-json "$RUN_DIR/annotated-deck-summary.json"
```

If `reddit-evidence-pack.json` does not exist yet, omit `--evidence-pack`; the
deck must remain `draft` and the annotations should say evidence is pending or
primary-source-required. The summary slides still stay inside the annotated
original deck; they are not a separate artifact.

Recommended badge labels:

- `Reddit-supported`
- `Contradicted on Reddit`
- `Weak Reddit support`
- `No Reddit evidence`
- `Primary source required`

Recommended visual treatment:

- Green accent for Reddit-supported claims.
- Amber accent for weak/no Reddit evidence.
- Red accent for contradicted claims.
- Blue/neutral accent for primary-source-required claims.

## Source / Tool Order

1. Read this `SKILL.md` and run `scripts/prepare_factcheck.py` locally.
2. Use supplied files, adjacent source files, and prior run artifacts.
3. Use GBrain recall for recurring companies, verticals, claims, or prior
   source bundles.
4. Use existing Reddit skills/tools: `reddit-seo-pipeline`,
   `content-outlier-research`, `/last30days`, ScrapeCreators, Exa, or logged-in
   Playwright.
5. Use official sources only for primary-source corroboration.
6. Use generic web search only as a fallback and label it as non-Reddit
   discovery.

## Output Contract

Default run folder:

```text
runs/YYYY-MM-DD-reddit-factcheck-<input-slug>/
  document-segments.json
  claim-pack.json
  reddit-evidence-pack.json
  reddit-factcheck-report.md
  annotate_input_deck.py
  annotated-deck-summary.json
  <input-slug>-reddit-factchecked-draft.pptx
  <input-slug>-reddit-factchecked-reviewed.pptx
  reddit-thread-*.json
  reddit-evidence-raw/
    reddit-discovery-manifest.json
    reddit-thread-*.json
```

Minimal delivery status values:

- `draft` - claims extracted, evidence gathered, and an annotated input deck
  with prepended executive summary slides was generated but not visually
  reviewed. No separate summary deck should exist unless explicitly requested.
- `reviewed` - Reddit sources were inspected, limitations are explicit, and the
  annotated input deck passed PPTX QA as a branded client-ready deck.
- `blocked` - required extraction/discovery/OCR/source access failed.

## Host Compatibility

### Target Hosts

- Claude Code: yes - use repo-local `skills/reddit-new-factcheck/SKILL.md`.
- Codex/OpenAI: yes - `.codex-plugin/plugin.json` exposes `./skills/`.
- OpenHands: yes - use the same repo-local skill path when project skills are
  enabled.

### Canonical Source

`skills/reddit-new-factcheck/` is the canonical shared source. Do not maintain a
separate `.claude` or `.agents` copy unless it is a thin wrapper.

### Tool Mapping

- Claude `Read` / `Grep` / `Glob` -> Codex shell reads and `rg`.
- Claude `Edit` / `MultiEdit` -> Codex `apply_patch`.
- Claude `Bash` -> Codex shell command.
- Claude `AskUserQuestion` -> concise chat question or AGENTS numbered choices.
- Claude `Task` / subagent -> main-thread execution unless a multi-agent tool is
  explicitly available.

## Skill Relationships

### Category

Data & Analysis

### Dependencies

Skills that must be installed for full delivery:

- `reddit-seo-pipeline` - extracts known Reddit thread URLs into JSON evidence.
- `branded-pptx-deck` - creates and QA-checks the client-facing branded deck.

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `reddit-seo-pipeline` | Sequential upstream | when Reddit thread URLs are known | `reddit-thread-*.json` |
| `pipeline-runner` | Complement | when the fact-check supports strategy pipeline outputs | `runs/*/content-research.md`, decks, briefs |
| `content-research` | Sequential upstream | when a research brief is the document being checked | `content-research.md` |
| `gbrain` | Prerequisite / memory layer | when recurring companies, verticals, or prior claims may exist | GBrain recall results, not deliverables |
| `branded-pptx-deck` | Sequential downstream | always for client-facing delivery | `reddit-factcheck-dossier-branded-reviewed.pptx` |

### Runtime Preamble

This skill uses `reddit-seo-pipeline` for thread extraction when URLs are known.
For broad discovery, it uses Reddit-aware discovery tools before generic search.
It writes local run artifacts as the source of record and treats GBrain as memory
only.

## Gotchas

- **Reddit is not a primary source:** it validates community evidence, language,
  sentiment, and objections. It does not prove market size or regulatory facts.
- **Image-only decks:** PPTX files exported as slide images have no text runs.
  Use adjacent Markdown or OCR and state the extraction method.
- **Anonymous Reddit access can fail:** Reddit may block direct JSON/search
  requests. Prefer known URLs, logged-in Playwright, approved APIs, or
  ScrapeCreators.
- **No automated posting:** never post replies or comments to Reddit.
- **Do not hide discovery gaps:** if no Reddit URLs or discovery tools are
  available, deliver the claim/query pack and mark evidence collection blocked.
