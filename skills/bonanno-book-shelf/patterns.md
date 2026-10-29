# Patterns — every named technique

## P1 — Progressive disclosure as the storage model
Put the trigger in the front matter and the substance in chapter files. The
model loads names and descriptions always, chapters only on match. This is what
makes twenty book skills cheap to keep.

## P2 — Job-phrased description
Write the description as the phrases the user would actually type, not as a
statement about the book. Shape: *"The working method from «Title» by Author.
Main job: <verb the outcome> (<named sub-steps>). Use whenever someone says:
<trigger phrase>, <trigger phrase>, … Use it even when the book is not named."*

## P3 — PREP / GRADE two-mode workflow
Every framework book supports a before-mode and an after-mode. PREP produces
the plan; GRADE scores the artifact against the same steps. Together they make
a weekly improvement loop rather than a one-shot lookup.

## P4 — Chapter traceability
Every workflow step names the chapter it came from. A step with no chapter
behind it is a step the model invented.

## P5 — The three-prompt trust test
After conversion, fire three prompts: on-target, adjacent, unrelated. Correct
behavior is pull / pull / leave alone. Anything else means fix the description.

## P6 — Folder-as-book routing
Point the converter at a directory and it produces one skill with a chapter per
document plus a routing table. Correct for a series of short guides (the ten
$100M Playbooks) rather than ten separate skills competing in the front matter.

## P7 — Summary aggregation
Five or six long chapter-by-chapter written summaries, plus three summary-video
transcripts via the watch skill, converted as a folder. Recovers frameworks,
decision rules and most examples. Declare it in `sources.md`.

## P8 — Fold your wins back in
Convert your own outcome notes into the existing skill via update mode. Your
market's examples outrank the book's generic ones.

## P9 — OCR before convert
Scanned PDFs carry no text layer. Run `ocrmypdf in.pdf out.pdf` first, then
convert the result.

## P10 — Verify the chapter map against the source
Never take `chapters_detected` as the chapter list. Grep the full text for
heading-shaped lines and reconcile before writing chapters. Detection misses
headings carrying trailing labels and captures numbered lists inside a chapter
— both on the same document (Ch 07).

