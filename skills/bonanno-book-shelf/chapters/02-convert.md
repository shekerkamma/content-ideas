# 02 — Convert your first book

> **Hard rule: only convert books and documents you own a copy of.**

## The command
```
/book-to-skill ~/Books/100m-offers.pdf 100m-offers
```
The last word is the name the skill gets.

## The one question it asks
Technical or text-heavy. Business books are text-heavy — pick that and it pulls
the words out in about a second. Then it finds the chapters on its own and
writes one at a time. A 200-page book takes a few minutes.

## What lands in your skills folder
| File | What's in it | When Claude reads it |
|---|---|---|
| `SKILL.md` | Core ideas, a workflow, an index of every chapter | Name + description load every session; the rest loads when the job matches |
| `chapters/` | One file per chapter: frameworks, rules, examples | When it needs exact wording or a worked example |
| `glossary.md` | The author's own terms, defined as the author defines them | When you use the author's language in a prompt |
| `patterns.md` | Every named technique, in one place | When applying a technique to your work |
| `cheatsheet.md` | The decision rules, compressed | When it needs to make a call fast |

This layout *is* the reason it works: only the front of the skill loads at
session start; everything else stays on the shelf until asked for.

## Three things that catch people out
1. **Scanned PDFs have no text to extract.** The converter stops on page one and
   tells you. Run OCR first (`ocrmypdf in.pdf out.pdf`; on a Mac, Preview or
   Vision OCR) and feed it the text file. The author's copy of *The Challenger
   Sale* was a scan and got done this way.
2. **A folder of PDFs becomes one skill.** Point the command at the folder and
   it builds one skill with a chapter per document and a routing table in
   SKILL.md. That is how the ten $100M Playbooks became a single skill.
3. **Test with three real prompts before you trust it.** Ask for something the
   book is meant to do, something adjacent, and something unrelated. It should
   pull the skill for the first two and leave it alone for the third.
