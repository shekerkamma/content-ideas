# QA report template

Fixed order. The reader acts on the first section, decides on the last.

```markdown
## Blocked on me
- <decision or approval the run cannot make; "Nothing." if none>

## Changed
- <what was fixed, file:line or commit, and the check that proves it>

## Found (supported)
| # | Where | What fails | Evidence (how to show it fails) | Fixed? |
|---|---|---|---|---|

## Could not confirm
- <unresolved findings, and every surface no gate reached: a real phone, iOS Safari, a screen reader,
  anything behind a login, third-party embeds>

## Merge risk
<one paragraph: the worst realistic thing that happens if this ships today, and how likely>

## Gates
| Gate | Result | Scope |
|---|---|---|
| Build | exit 0 | |
| Route / sweep | n/n | routes x widths |
| Navigation | pass | dropdowns, links, phone, typed URLs |
| axe WCAG 2.2 A/AA | 0 violations | page loads |
| Design detector | 0 | files |
| Live | commit <sha> served | |
```

Grade every finding before it goes in: supported (reproduced), unresolved (plausible, not reproduced: goes
under Could not confirm), contradicted (evidence says otherwise: dropped, one line saying why).
