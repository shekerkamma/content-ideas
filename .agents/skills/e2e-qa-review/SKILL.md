---
name: e2e-qa-review
description: Use when a website or web app must be proven ready to ship end to end — "QA the site", "end-to-end review", "review all pages and sub pages", "is it ready to ship", "run the full QA", "what are the risks of merging this", "check it on phone and desktop". Builds with checked exit codes, serves it the way GitHub Pages does, sweeps every route at two widths with axe-core WCAG 2.2 and structural checks, drives every menu by pointer, keyboard and phone, runs the design detector, runs the specialist skills as lanes (web-design-guidelines, impeccable detector + critique, improve-ui drift proofs, scroll-craft's scroll harness and taste floor), checks declared content actually renders, does one bounded visual round, triages every finding as supported / unresolved / contradicted, fixes, re-verifies, checks the live deploy, and reports Blocked on me / Changed / Found / Could not confirm. Not for native .pptx decks (pptx-design-quality) or a single-component design critique (impeccable).
license: MIT
metadata:
  category: Product Verification
  version: '1.1'
  cost-tier: 'Gates are scripts: any model can run them (Haiku). Triage, the visual round and fixes need Sonnet. Cross-family review uses Codex CLI on subscription auth.'
  compatibility: >-
    Scripts need Node >= 20 with `playwright` and `axe-core` resolvable from the target project,
    `$E2E_QA_NODE_MODULES`, or this skill's repo; Node >= 24 for the impeccable lane; Python 3 (Pillow
    optional, for contact sheets). Claude Code, Codex and OpenHands; subagent fan-out degrades to
    sequential passes where a host has no subagents.
  sources: >-
    claude.dev "Getting the most out of Opus 5.5" (2026-09-22); Theo, "Getting the most out of Opus 5.5"
    (youtube ejjBbaq9RmY, 20:00-25:20); the deepgrid-platform-v2 and deepgrid-dr-silicon-v3 QA runs
    (2026-09-26/27), whose false greens are in references/false-greens.md.
---

# End-to-end QA review

A page that loads is not a page that works, and a green gate is not a verified claim. This skill runs the
whole path from build to live URL, and every finding it reports carries the evidence that makes it true,
the evidence that could make it false, and what nobody could check.

Resolve `SKILL_DIR` to the directory holding this file; scripts are `SKILL_DIR/scripts/*`. Run them **from
the target project's directory**. They resolve `playwright` and `axe-core` from the project first, then
`$E2E_QA_NODE_MODULES`, then this skill's own repo, and print which one served the run.

This is a compound skill. It owns the run, the gates, the triage and the report; four specialist skills run
inside it as **lanes** (step 5 deterministic, step 7 judgment), each keeping its own rules. Who owns which
defect, how peers are located, and the reviewer briefs: [references/lanes.md](references/lanes.md).

## 0. Contract first (before touching anything)

Write `qa/CONTRACT.md` in the project (or the run folder) with four things, in the user's words where they
gave them. The Opus 5.5 guide's first rule: name the finish line, then let it run.

1. **Done means** — e.g. "every route passes the sweep at desktop and phone with 0 axe violations, every menu
   link reachable by pointer, keyboard and phone, the live URL serves this commit".
2. **Stops** — keep going when a step needs no input; stop only when blocked on the user, or before anything
   destructive or outward (deleting data, force-pushing, changing another repo or deployment).
3. **Leave-out list for design** — the defaults this product must not have (see
   [references/design-bans.md](references/design-bans.md)); "avoid a generic look" is not a list.
4. **Scope** — the routes (every page and sub-page), the widths (1440 and 390 at minimum), the live URL.

Keep the task list in a file (`qa/TASKS.md`), ticked as it goes. Long runs outlive the context window; the
file does not.

## 1. Build, and read the build's own exit code

```bash
npm run build > qa/build.log 2>&1; echo "build exit $?"
```

Never `build | tail && gate`: the pipe returns `tail`'s status, so a failed build leaves the gates testing
the previous output. Check `$?` of the build, and that the output's timestamp moved.

## 2. Serve it the way the host serves it

```bash
python3 "$SKILL_DIR/scripts/serve_pages.py" <dist-dir> <base-slug> <port> &
```

GitHub Pages resolves `/x` to `x.html` before `x/`, never lists a directory, and answers a missing path with
the site's `404.html` (status 404). `python3 -m http.server` does none of that, so it fails routes that work
live and passes ones that 404 live. Use this server, or the host's own preview.

## 3. Sweep every route at two widths

Write `qa/sweep.json` (see [references/config.md](references/config.md)), then:

```bash
node "$SKILL_DIR/scripts/sweep.mjs" qa/sweep.json      # exit 0 clean, 2 findings, 1 blocked
python3 "$SKILL_DIR/scripts/summarize.py" qa/sweep-results.json > qa/SWEEP.md
```

Per route and width it records: HTTP status, page errors, failed requests, one h1, heading skips, sideways
scroll, broken images, images with no reserved box, targets under 24 px, em dashes, numbered counters,
italic heading accents, monospace labels, pill buttons, eyebrow density, reveals that never finished, and
axe-core WCAG 2.2 A/AA violations. It scrolls each page end to end first so lazy content exists, and saves a
first-viewport screenshot for step 6.

## 4. Drive the navigation like a person

```bash
node "$SKILL_DIR/scripts/nav_gate.mjs" qa/nav.json    # exit 0 clean, 2 findings, 1 blocked
```

Every dropdown is hovered and every link reached with a straight pointer path, at a human speed, then
clicked and landed on; Enter opens, Tab reaches a link, Escape closes and returns focus; the phone sheet is
opened and every link tapped; the URLs people type (`/About`, `/about/`, `/about.html`, a bare section path)
must reach a real page. External links are checked by address and target, never followed.

**Before trusting a clean run of either gate on a new site, or after editing a gate,** point it at
`assets/fixtures/broken/` (serve it with `serve_pages.py … fx <port>`). Every defect there is planted and
commented; the sweep must exit 2 on `/` and stay clean on `/a` and the 404 route, and the nav gate must
report the hover gap, Tab, Escape, click-toggle, missing phone sheet and `/A`. `tests/test_e2e_qa_review.py`
runs exactly that. The fixture caught two gate bugs while this skill was written: the 404 route's own
document 404 counted as a page error, and top links matched by `href` attribute silently missed relative
hrefs.

## 5. Specialist lanes and content integrity

```bash
python3 "$SKILL_DIR/scripts/lanes.py" qa/lanes.json   # 0 clean, 2 findings, 1 an applicable lane BLOCKED
```

- **guidelines**: `web-design-guidelines`' source audit, file:line.
- **impeccable**: the detector over the source; warnings gate, advisory drift goes to the improve-ui reviewer.
- **scrollcraft**: scroll-craft's own harness (dead scroll, frozen clips, cues that never peak, contrast over
  moving media) at desktop, phone and reduced motion, only when the build uses its engine; otherwise it is
  recorded as not applicable, with the reason.

Verify each hit in context before it counts: a stroke-width transition or a regex string is not a layout
transition or a broken image, and a line-based `<img>` rule misses `width` on the next line.
- **Declared vs rendered.** When data declares N sections, cards or items, assert N render. A deleted switch
  case renders nothing and type-checks clean; only a count catches it. Make discriminated-union renderers
  exhaustive (`const missing: never = s`).

## 6. One bounded visual round

Tile the sweep's screenshots (`python3 "$SKILL_DIR/scripts/contact_sheet.py" <shots-dir> qa/sheet`) and look
at them, desktop and phone, once. Check hierarchy, the leave-out list, empty frames, cropped labels,
and anything 3D actually drawing. Fix everything the round shows in one batch, confirm with at most one more
round, and stop. Open-ended polishing is not verification.

## 7. Review fan-out and triage (large surfaces)

For more than ~10 routes, or when asked for a review, split by surface: one subagent per page group, each
handed the contract, its routes and the sweep rows, each returning findings with file:line, the failing
evidence and how to show it fails. On Opus 5.5, say plainly that it may use subagents; it holds back
otherwise. Alongside the page-group reviewers, run the **judgment lanes** from
[references/lanes.md](references/lanes.md): impeccable critique, the improve-ui drift audit (three proofs per
candidate), the rest of the web-design-guidelines rulebook, and the scroll-craft taste floor where scroll
drives the page. Every reviewer returns the same row schema, so triage is one pass. Optionally add a reviewer
from another model family, where one is set up
([references/cross-family.md](references/cross-family.md)). Different families find different things.

Grade every finding before it reaches the report:

- **Supported** — reproduced from the evidence, in context.
- **Unresolved** — plausible, not reproduced; stays in the report under *Could not confirm*.
- **Contradicted** — the evidence says otherwise; drop it and say why in one line.

## 8. Fix, re-verify, ship, check live

Fix the supported findings (this skill fixes; improve-ui only plans), rebuild (check `$?`), rerun steps 3-5 on the new build, commit and push. Then
wait for CI and check the live URL serves the new commit (a `build-info.json` or equivalent), with the
sweep and the nav gate run once more against it. A CDN may serve the old page for its cache lifetime
(`max-age=600` on GitHub Pages): say so rather than calling the deploy failed.

## 9. Report

Use [references/report-template.md](references/report-template.md). The order is fixed: **Blocked on me**
first, then **Changed**, **Found** (supported only), **Could not confirm** (unresolved, and every surface no
gate reached: a real phone, a screen reader, Safari, anything behind a login), then **Merge risk**: the
worst realistic thing that happens if this ships today.

## Judgment rules

Policy lives here, not in the steps. Edit these to tune the skill.

- **Evidence over assertion.** A finding without a reproduction is unresolved, however plausible.
- **Classify before fixing.** A failing gate is either a site defect or a measurement defect. Prove which
  before changing the site: the smooth-scroll, sticky-header, hover-residue and local-server traps in
  [references/false-greens.md](references/false-greens.md) all looked like site defects.
- **Negative controls for new checks.** A check nobody has seen fail can pass on an empty population.
  Break it once on purpose (remove a case, point it at a bogus route) before trusting its green.
- **Fix the source, not the symptom.** A generic fix at the owning layer (one effect that makes every
  overflowing table focusable) beats ten local patches, provided it is scoped to what actually overflows.
- **Reference content is not yours to rewrite.** When the user names a content authority, keep its wording
  and flag doubts; change punctuation or markup, not claims.
- **Pinned look wins.** Where the user pinned an existing look, design-default bans are reported, not
  enforced.
- **Bounded visual passes.** One round, one confirmation round, stop.
- **Stop only when blocked or before anything destructive or outward.** Otherwise keep going and put status
  in the same message as the next action.

## Gotchas

- **Piped build hides failure** — see step 1.
- **Wrong server** — see step 2; the symptom is "every route without a trailing slash 404s".
- **Smooth scrolling lies to measurements** — `scroll-behavior: smooth` animates `scrollTo` and focus scrolls;
  wait for it to settle or scroll with `behavior: 'instant'` before measuring positions.
- **axe `target-size` "partially obscured"** after a full-page scroll is usually the sticky header over the
  element at that scroll position. Test WCAG 2.4.11 directly: Shift+Tab through the page and check the
  focused element's box against the header's bottom, after the scroll settles.
- **Hover residue** — reusing one tab across captures leaves the last hover state on every screenshot.
- **Element screenshots taller than the viewport** repeat sticky headers inside the image; not a defect.
- **`page.evaluate` during a redirect** throws "execution context destroyed"; retry after load.
- **Lane skills resolve in a fixed order**, and a plugin skill (scroll-craft) lives in the plugin cache, not
  `~/.claude/skills`. `lanes-results.json` records which directory served each lane; check it when a lane's
  output looks unfamiliar.
- **impeccable's skill-bundle update can fail upstream** ("Could not verify skill bundle: HTTP 404") while
  the npm detector at the same version works. The detector lane pins the npm package, so it is unaffected.
- **Catalogue is not proof** for anything external (a model id, a provider route, a video id): test it.

## Skill Relationships

### Category
Product Verification

### Dependencies
- None hard-required: every gate in steps 1-4 is this skill's own. The lanes need their skills; a missing
  one is reported BLOCKED with its reason, never skipped silently.
  - `web-design-guidelines`, `impeccable` (+ npm `impeccable@4.1.0`), `improve-ui`,
    `nateherk-design:scroll-craft` (plugin); a Codex CLI for cross-family review.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `web-design-guidelines` | Orchestrated lane | step 5 script + step 7 reviewer (rest of its rulebook) | `qa/lanes-results.json` · review rows |
| `impeccable` | Orchestrated lane | step 5 detector (warnings gate) + step 7 critique | `qa/lanes-results.json` · review rows |
| `improve-ui` | Orchestrated lane, then downstream | step 7 drift audit over impeccable's advisory list; plans only if asked | review rows · `design-plans/*.md` |
| `nateherk-design:scroll-craft` | Orchestrated lane + behavioral overlay | scroll-craft engine pages: step 5 harness; scroll-driven pages: step 7 taste floor, refuse list joins the leave-out list | `qa/scroll/*/sheet.png` · review rows |
| `design-tokens` | Complement | token contract + ten WCAG render gates on one page | its gate output |
| `claudex-loop:codex-review` | Complement | cross-family review with a persistent session | `PLAN-REVIEW-LOG.md` |
| `pptx-design-quality` | Alternative / Peer | the deliverable is a native deck, not a site | — |

### Runtime Preamble
"I'll write the QA contract first (what done means, when I stop), then build, serve like the host, sweep
every route at two widths, drive the menus, run the specialist lanes (web-design-guidelines, impeccable,
improve-ui, and scroll-craft where scroll drives the page), and report Blocked on me / Changed / Found / Could not confirm.
For a native deck use pptx-design-quality instead."

## Host Compatibility

- Claude Code: canonical `skills/e2e-qa-review/`, discovered through the `~/.claude/skills/e2e-qa-review`
  symlink and the project `.claude/settings.json` skills list.
- Codex: exposed by `.codex-plugin/plugin.json` (`"skills": "./skills/"`).
- OpenHands / DeepSeek Harness: byte-identical mirror at `.agents/skills/e2e-qa-review/`.
- Tools: Claude `Task` subagents map to Codex multi-agent tools where available, otherwise sequential passes
  over the same page groups. `AskUserQuestion` maps to one plain question, only when blocked.
