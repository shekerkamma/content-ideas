---
title: A document extractor's structure count is a hint, not a map
date: 2026-09-06
category: conventions
module: book-to-skill
problem_type: convention
component: document-ingestion
severity: high
applies_when:
  - "Converting a PDF, EPUB, or DOCX into chapters, sections, or a knowledge base"
  - "Trusting a reported chapter/section count without reconciling against the source"
  - "Choosing between a fast text extractor and a layout-aware one"
  - "Verifying generated content against a source that was itself lossily extracted"
tags: [extraction, verification, pdf, docling, pdftotext, book-to-skill, claim-hygiene]
---

# A document extractor's structure count is a hint, not a map

## Context

Validating `book-to-skill` (`virgiliojr94/book-to-skill`, MIT) end to end across a
mixed corpus: an 11-page guide, a 13-page playbook, an 88-page columnar deck, a
19-heading DOCX, a hand-built EPUB, and a 299-page O'Reilly book.

The converter reports a `chapters_detected` count and a `chapters_method`
(`structural` / `numeric` / `none`). That number is a heuristic over extracted
text. **It was wrong in both directions, often on the same document**, and every
failure was silent: the extraction reports success either way.

## Guidance

**Rule 1 — Reconcile the chapter count against the book's own table of contents
before writing a single chapter file.**

Measured on *Low-Code AI* (O'Reilly, 299 pp), which has **8** real chapters:

| Mode | Chapters reported | What they were |
|---|---|---|
| `--mode text` (pdftotext) | **145** | 138 were running page headers (`2 \| Chapter 1: …` on every even page), plus table rows |
| `--mode technical` (docling) | **8** | Exactly the 8 real chapters, with full titles |

An 18x over-count that a reviewer would never notice from the summary line.

**Rule 2 — The error runs in both directions at once, so "it found fewer than I
expected" is not the only failure shape.**

On a 13-page guide with **11** numbered sections, numeric detection reported 8:

- **Missed** the three whose heading line carried a trailing badge
  (`HIGHEST LEVERAGE`, `DO THIS FIRST`) — the two the author flagged as most
  important.
- **Falsely captured** four items from a 7-line checklist living *inside*
  section 10.

**Rule 3 — `--mode text` silently destroys tables. Never use it on a source whose
value includes tabular or code content.**

Same 299-page book, only the flag varying:

| Metric | `text` | `technical` |
|---|---|---|
| Markdown table rows recovered | **0** | **515** |
| Running page headers polluting output | 138 | **0** |
| Chapters | 145 | 8 |

The tool's guidance ("business books are text-heavy, pick that") is about
**speed**, not fidelity. A "text-heavy" business book full of decision tables is
still a table-bearing document.

**Rule 4 — Verifying claims against a lossy extraction proves nothing about the
claims the lossiness destroyed.**

A 16-claim spot-check against the `text`-mode extraction passed completely. It
still missed a wrong chapter table, because the source being checked against had
already lost the real one. Re-extraction with `technical` mode surfaced it: a
use-case table's `Type` column is the book's **implementation tier**
(No-code AutoML / Low-code BigQuery ML / Custom-code), not the ML problem type
that had been inferred from flattened prose. That column *was* the book's central
thesis stated in one table.

**Rule 5 — Zero chapters can be the correct answer.** An 88-page columnar deck
returned `0 (none)`. Investigation showed 201 "heading-shaped" lines that were all
wrapped column text — the document genuinely has no chapter structure. Check what
the document *is* before filing a detection bug.

## Why This Matters

Chapter boundaries decide what goes in every downstream file. A 145-chapter map of
an 8-chapter book does not produce a slightly worse skill; it produces one whose
structure has no relationship to the source. And because the extractor exits 0 and
prints a tidy summary, nothing signals the problem.

This is the same class as the repo's existing gate failures — a check that goes
green because it measured the wrong thing certifies the defect. Here the wrong
thing was a page header.

## When to Apply

- Any conversion of a document into structured chapters or sections.
- Before writing chapter files, always: open the source's ToC and reconcile.
- When choosing an extraction mode: if the source has tables, code, SQL, or
  figures, use the layout-aware mode even when it is nominally "text-heavy".
- When a verification pass over generated content passes cleanly — ask whether
  the source it was checked against could have lost the thing being checked.

## Examples

Reconciliation that caught the 18x over-count, in two commands:

```bash
# what the extractor claims
python3 -c "import json;print(json.load(open('$W/metadata.json'))['chapters_detected'])"   # 145

# what the book actually has
grep -cE "^\s*CHAPTER [0-9]+\s*$" $W/full_text.txt        # 8
grep -cE "^\s*[0-9]+\s+\|\s+Chapter " $W/full_text.txt     # 138  <- the running headers
```

## Related

- `CLAUDE.md` — "a gate whose own assertion was never tested reports a hypothesis,
  not a result"; same discipline, applied to extraction rather than linting.
- `docs/solutions/conventions/artifact-self-description-is-not-evidence.md` —
  the metadata a tool emits about its own output is a self-description.
- `docs/solutions/environment/torch-cuda-arch-mismatch-on-pascal.md` — the
  environment finding from the same validation session.
