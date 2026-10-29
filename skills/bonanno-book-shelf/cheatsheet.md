# Cheat sheet — the decision rules

| Situation | Rule |
|---|---|
| Do I convert this book? | Only if you own a copy. No exceptions. |
| Personal or project skills folder? | Personal (`~/.claude/skills/`) by default; project only when the books belong to that business. |
| Technical or text-heavy? | Business/prose → text-heavy. Code, tables, formulas, diagrams → technical. |
| PDF won't extract | It's a scan. `ocrmypdf in.pdf out.pdf`, then convert. |
| Ten short related guides | One skill from the folder, not ten skills. |
| Skill never gets pulled | The description is wrong. Rewrite it as trigger phrases + "use it even when the book is not named." |
| Skill gets pulled but output is generic | It's a book report. Add PREP/GRADE modes and chapter citations. |
| Skill used to get pulled and stopped | Check the front matter first. |
| I don't own the book | Framework book → summary workaround. Wording book → buy it. |
| Did the conversion work? | Three prompts: on-target, adjacent, unrelated → pull, pull, ignore. |
| A book skill produced a win | Write the note, fold it in with update mode. |
| Extractor reports N chapters | Treat as a hint. Reconcile against the source before writing (Ch 07). |
| Source is a table/columnar deck | 0 chapters is correct. Use technical mode. |

## The one-line test
**Not "does it describe the book" — "can Claude run the book on my work."**

## Install verification
Fresh session → type `/book` → `book-to-skill` in autocomplete.
