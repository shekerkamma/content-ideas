# 07 — Field notes: measured conversions (folded in, Sep 2026)

Own-results chapter, added via update/fold-in per [Ch 06](06-keep-sharp.md). The
book's examples are good; these are from this machine.

## Measured results by source type

| Source | Detection | Result |
|---|---|---|
| `.docx`, 19 headings (python-docx) | structural | 19 chapters, clean |
| Folder of 3 PDFs | numeric | Aggregated to one skill, 8 chapters — confirms P6 |
| 88-page columnar table PDF | none | **0 chapters — correct.** A table deck has no chapter structure; use technical mode |
| Image-only PDF | — | Refused, exit 1, `ocrmypdf` hint — confirms Ch 02 item 1 |

## The failure worth writing down

On a 13-page guide with **11** real numbered sections, numeric detection found
**8** — and simultaneously swallowed a 7-item checklist living *inside* section
10. The three it missed were the ones whose heading line carried a trailing badge
(`HIGHEST LEVERAGE`, `DO THIS FIRST`). Those were the two the author flagged as
most important.

So the error runs in both directions at once: it under-counts real chapters and
over-counts inner lists, on the same document.

**Rule:** `chapters_detected` is a *hint*, not a map. When heading lines carry
trailing labels, read the full text and map the chapters yourself. The tool's own
warning says exactly this — "may miss or duplicate sections" — and it is accurate.

## Anti-pattern

**Trusting the chapter count as the chapter list.** It is a heuristic that both
misses and over-counts. Verify against the source before writing chapters.
