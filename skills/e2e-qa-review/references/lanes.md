# Specialist lanes

This skill is the orchestrator. Four specialist skills each run as a **lane**: a deterministic lane is a
script whose output lands in `qa/lanes-results.json`, and a judgment lane is a reviewer (a subagent where the
host has them) that reads that skill's own rulebook and returns findings in the triage schema below. The
specialist skills stay canonical: this file says when each one runs and what it owns, and never copies
their rules.

## Who owns which defect

One defect, one owner. When two lanes report the same thing, the owner's evidence decides the grade and the
other report is folded into it, not counted twice.

| Defect class | Owner | Why the others defer |
|---|---|---|
| Missing names, contrast, roles, target size, heading order | sweep (axe-core WCAG 2.2, rendered) | source regexes cannot see computed names or colours |
| Layout shift from images | sweep `noBox` (rendered: attributes **or** CSS aspect-ratio) | the guidelines regex is line-based: `width` on the next JSX line, or CSS `aspect-ratio`, reads as missing |
| Menus, links, typed URLs, 404 | nav gate | nothing else drives a pointer |
| Anti-patterns in CSS/markup (overused fonts, gradient text, side tabs, flat type scale, layout transitions) | impeccable detector, **warning and above** | it is the only lane that knows the pattern catalogue |
| Drift from DESIGN.md (undocumented colours, sizes, radii) | improve-ui reviewer, fed impeccable's **advisory** list as candidates | a colour outside the doc is a candidate, not a defect, until a contract and a runtime path prove it |
| `transition: all`, `outline: none`, `...`, icon buttons with no label | guidelines script (source) | cheap and exact at file:line |
| Focus visibility, forms, motion, typography rules the script cannot regex | guidelines reviewer (the rest of its rulebook) | needs reading, not matching |
| Scroll timeline: dead scroll, frozen clips, cues that never peak, contrast over moving media | scroll-craft harness, **only on scroll-craft engine pages** (`data-sc-act`) | a static screenshot is one frame; failures live between frames |
| Generic scroll reveals (IntersectionObserver fade-ins) | sweep `reveal` check | the scroll-craft harness reads its own engine's state and has nothing to read elsewhere |
| Hierarchy, density, composition, "does this page say anything" | impeccable critique + scroll-craft taste floor, in the one visual round | rendered judgment; source cannot establish it |

## Deterministic lanes: `scripts/lanes.py`

```bash
python3 "$SKILL_DIR/scripts/lanes.py" qa/lanes.json   # 0 clean, 2 findings, 1 an applicable lane BLOCKED
```

| Lane | Runs | Needs | Not applicable when |
|---|---|---|---|
| `guidelines` | `web-design-guidelines/scripts/audit.mjs <src>` | Node >= 18 | never; 0 files scanned is BLOCKED, not clean |
| `impeccable` | `npx impeccable@<pin> detect --json <src>` | Node >= 24 (found on PATH or under nvm) | never |
| `scrollcraft` | `scroll-craft/scripts/shoot.mjs` at desktop, 390 px and reduced motion | `playwright-core` in the site, installed Chrome (bundled Chromium has no h264) | the build contains no `data-sc-act` |

**Test the browser's h264, don't assume it.** scroll-craft refuses bundled Chromium because "Chromium ships
without an h264 decoder", and a browser without it leaves every scrub clip on its poster: FROZEN CLIP and
STUCK ON POSTER then describe the browser, not the page. That premise is build-dependent. Measured here on
2026-09-27 with a real libx264 clip: Playwright's chromium-1228 played it (`videoWidth` 320, `currentTime`
advancing), identical to Google Chrome 154. Before trusting a clip verdict, play one h264 file in the
browser the lane will use; `scrollChrome` pins a different one. Headless screenshots here also time out
intermittently (a different pass each run), so each pass gets one retry and `passes` records it.

Peer skills are found by config `skillDirs`, then `E2E_QA_<NAME>_DIR`, then a sibling of this skill, then
`~/.claude/skills`, `~/.agents/skills`, `.agents/skills`, `.claude/skills`, `~/.codex/skills`, then the
Claude plugin cache (`scroll-craft` ships in the `nateherk-design` plugin). A lane whose skill is missing is
**BLOCKED with the reason**, never dropped: a lane that skips must not read as a lane that passed.

The impeccable pin (`impeccableVersion`, default `4.1.0`) is policy: tune it in the config, and bump it
together with `scripts/design-qa-detect.sh` in the content-ideas repo. The detector scans **source** by
default (`src`), because a fix edits source and a built bundle drags in vendored libraries: on dr-silicon-v3
the `dist/` scan returned 437 findings, 36 of them from a minified vis-network, against 15 warnings on `app/`.

## Judgment lanes: reviewer briefs

Run these in step 7, one reviewer per lane, in parallel where the host has subagents. Each brief is
self-contained, since a reviewer has none of this conversation. Hand each the contract, its routes, the
relevant slice of `qa/sweep-results.json` / `qa/lanes-results.json`, and the base URL.

**Every reviewer returns only this, one row per finding:**

```
| # | Finding | file:line or route@width | Evidence it is true | How to show it is false | Owner lane |
```

The orchestrator then grades each row supported / unresolved / contradicted (SKILL.md step 7). A reviewer
never edits product source.

### impeccable — critique
> Load the `impeccable` skill and follow `reference/critique.md` for these routes, using its detector output
> in `qa/lanes-results.json` as input rather than re-running it. The brief wins: if `DESIGN.md` or the
> contract pins a look, judge against that look, not against the pattern catalogue. Report hierarchy, type,
> colour and layout problems visible in the screenshots. Do not report anything the sweep owns
> (accessibility) or the nav gate owns (menus).

### improve-ui — drift audit
> Load the `improve-ui` skill. Your candidates are the impeccable `advisory` list in
> `qa/lanes-results.json` (colours, sizes and radii outside `DESIGN.md`) plus anything you trace yourself.
> Apply its three proofs to every candidate: a binding contract, a runtime path proving the value reaches
> this surface, and one determined correction. Report at most three. Write plans under `design-plans/` only
> if the orchestrator asks. Accessibility is out of your scope here; the sweep owns it.

A computed-style check is usually the fastest runtime proof. On dr-silicon-v3 it split one detector rule
four ways: `body { font-family: Arial }` was dead (Inter won the cascade: contradicted), `.eyebrow` really
rendered Arial (supported), `.mono` fell back to generic `monospace` (supported), and two selectors matched
nothing on the audited routes (unresolved).

### web-design-guidelines — the rest of the rulebook
> Load `web-design-guidelines` and review the source against the rules its `audit.mjs` cannot match: focus
> states, forms, motion and reduced motion, typography (curly quotes, `…`, non-breaking spaces between
> numbers and units, tabular figures), content overflow, lazy loading. Output its terse `file:line` format
> plus the evidence columns. Skip image dimensions and ARIA names: the sweep owns those on the rendered page.

### scroll-craft — taste floor (scroll-driven or motion-heavy pages only)
> Load `nateherk-design:scroll-craft` and read `references/taste.md` (the refuse list and the squint test)
> and `references/verify.md` ("What the harness cannot tell you"). On the contact sheets, report
> composition, motion that lurches or stalls, copy landing on the busiest part of a frame, and acts that say
> nothing. Its refuse list joins the contract's leave-out list. Do not rebuild or restyle the page; this is
> review, not a build.

Skip a judgment lane only with a one-line reason in the report (e.g. "scroll-craft taste: no scroll-driven
sections"). A skipped reviewer is a *Could not confirm* item, not a pass.
