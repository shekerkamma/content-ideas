# Glossary — the author's terms

**Book skill** — a folder holding a `SKILL.md` plus chapters, glossary, patterns
and cheat sheet, derived from one book (or one folder of documents), that an
agent pulls off the shelf when a job matches.

**The bookshelf** — the progressive-disclosure model. Only skill names and
descriptions load at session start; everything else waits until needed.

**The front of the skill** — the name and the description line. The only part
loaded every session, and therefore the only thing that decides whether the
skill gets used at all.

**Front matter** — same thing, viewed as a budget: every skill's front matter is
in every session, so it must stay short.

**Book report** — the failure mode. A skill that *describes* a book instead of
running it. Claude already has plenty of those.

**PREP mode** — the "before" half of a book skill's workflow: inputs in,
one-page plan out, each step citing its chapter.

**GRADE mode** — the "after" half: transcript or draft back in, scored step by
step against the same framework, naming what was skipped.

**The workaround** — building a book skill from five or six long written
summaries plus three summary-video transcripts, when you do not own the book.

**Framework book** vs **wording book** — the distinction that decides whether
the workaround is legitimate. A framework book's value is named steps and
decision rules (workaround fine). A wording book's value is verbatim examples
and annotated ads (buy it).

**Update / fold-in mode** — pointing the converter at your own notes plus an
existing skill slug, merging your results into the book's chapters.

**Text-heavy** vs **technical** — the one question the converter asks. Text-heavy
uses `pdftotext` (fast). Technical uses a layout-aware extractor to preserve
tables and diagrams.

**Structural detection** — chapter splitting from real headings (Markdown `#`,
DOCX heading styles). Reliable when the source has them (Ch 07).

**Numeric detection** — chapter splitting from leading numbers on a line. Both
misses headings with trailing badges and captures inner numbered lists (Ch 07).

**`chapters_detected`** — the extractor's chapter *count*. A hint, not a map;
verify against the source before writing chapters (Ch 07).

