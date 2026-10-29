---
name: bonanno-book-shelf
description: "The working method from \"The Book-to-Skill Setup Guide\" by Brad Bonanno. Main job: turn a book, PDF or document you own into an agent skill that runs the book's frameworks on your work (install the converter, convert a book, write a description that actually gets pulled, add PREP/GRADE modes, build a skill from summaries when you don't own the book, and fold your own results back in). Use whenever someone says: turn this book into a skill, convert this PDF, put this on Claude's bookshelf, my book skill never gets used, write a skill description, I don't own the book, or asks which books to convert first."
---

# Bonanno — The Book Shelf Method

## Core idea

Claude has already read the books. That is exactly the problem. Asked *about* a
book it names the frameworks back at you; asked to *use* one it defaults to the
most probable output and writes what everyone else writes. A summary does not
fix this, because a summary is what it is already doing. What fixes it is
forcing the model to run the actual techniques with the actual worked examples
and decision rules in front of it.

So the unit of value is not the book's content — it is the book's *structure*,
loaded on demand. Progressive disclosure is the whole mechanism: only a skill's
name and description load every session; the chapters stay on the shelf until a
job matches. That is how you read a book anyway. You do not reread it to write
one ad; you flip to the page you need.

**The test of a book skill is not "does it describe the book." It is "can Claude
run the book on my work."**

## Workflow

**PREP** — before the work. Take the user's inputs and produce a one-page plan
using the book's framework, citing the chapter each step comes from.

**GRADE** — after the work. Take the transcript or draft back in and score it
step by step against the same framework, naming what was skipped.

Every step must be traceable to a chapter file. A step you cannot point at a
chapter for is a step the book did not give you.

## Chapter index

| # | Chapter | Read it when |
|---|---|---|
| 01 | [Install the converter](chapters/01-install.md) | Setting up, choosing personal vs project scope |
| 02 | [Convert your first book](chapters/02-convert.md) | Running a conversion, or one failed |
| 03 | [A job, not a book report](chapters/03-job-not-report.md) | A skill never gets pulled, or reads like a summary |
| 04 | [The five books to convert first](chapters/04-five-books.md) | Deciding what to convert, in what order |
| 05 | [When you don't own the book](chapters/05-dont-own-it.md) | No copy available |
| 06 | [Keep the shelf sharp](chapters/06-keep-sharp.md) | Maintaining a shelf over time |
| 07 | [Field notes: measured conversions](chapters/07-field-notes.md) | Reading extractor output; what detection gets wrong |

Supporting files: [glossary.md](glossary.md) · [patterns.md](patterns.md) · [cheatsheet.md](cheatsheet.md)

## Anti-patterns

- **Converting a book you do not own.** The method's one hard rule. Never pirate
  a book to feed this workflow.
- **A description that names the book instead of the job.** "Knowledge from
  $100M Offers" gets ignored forever; the description is the *only* thing the
  model sees before deciding to pull the skill.
- **Shipping a book report.** Chapters that summarize rather than give runnable
  steps produce nothing the model could not already have guessed.
- **Trusting a conversion you never tested.** Three prompts, or you do not know.
- **Trusting the extractor's chapter count as the chapter list.** It under-counts
  and over-counts on the same document (Ch 07).
- **Using the summary workaround on a wording book.** For Breakthrough
  Advertising the wording *is* the value; summaries do not carry it.
