# False greens and false reds

Every entry cost a real cycle on deepgrid-platform-v2 or deepgrid-dr-silicon-v3 (2026-09-26/27). Each looked
like a verdict about the site and was a verdict about the measurement.

| Symptom | What was actually wrong | Check that tells them apart |
|---|---|---|
| Gates green after a fix that should have changed them | `npm run build \| tail -1 && gate`: the build failed, the pipe returned `tail`'s 0, the gates tested the old `dist/` | `echo "build exit $?"` on the build alone; compare the output's mtime |
| Every route without a trailing slash is "not found" | `python3 -m http.server` does not map `/x` to `x.html`; GitHub Pages does | serve with `scripts/serve_pages.py`; `curl` the same path both ways |
| A bare section path shows a directory listing | same server; Pages would 404 into the site's `404.html` | same |
| A focused element measured far above the viewport | `scroll-behavior: smooth` was still animating the focus scroll | wait ~900 ms, or scroll with `behavior: 'instant'` |
| axe `target-size` "partially obscured" on random links | the sticky header covered them at the scroll position axe ran at | Shift+Tab test for WCAG 2.4.11 after the scroll settles |
| A menu item looks selected on every screenshot | hover state left by the previous capture in the same tab | move the pointer to a corner, or use a fresh page |
| A sticky header appears mid-image | element screenshot taller than the viewport repeats fixed/sticky layers | not a defect; capture the viewport or the element in parts |
| Three sections render nothing, every gate green | a slice-replace edit deleted switch cases; unmatched cases render nothing | exhaustive `never` switch; count declared vs rendered sections |
| A new check passes everywhere | its selector matched nothing (empty population) | break it once on purpose before trusting it |
| Tool says "updated", file unchanged | tool self-report | hash the artifact |
| Menu panel "closes before the pointer reaches the link" | real defect: no menu aim, panel far from its button | fixed with a 180 ms switch delay + 280 ms close delay + panel under its button |
| Phone links "outside the viewport" | real defect: a fixed-height sheet with `overflow: visible` | `overflow-y: auto` on the sheet |
| `/About` 404 | real defect on case-sensitive hosts | a 404 page that lower-cases, strips `/` and `.html`, maps section roots |

The last three were real. The discipline is the same either way: prove which kind it is before changing the site.
