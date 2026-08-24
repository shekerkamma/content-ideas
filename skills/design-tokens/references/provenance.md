# Provenance

Adapted from [`plugin87/ux-ui-agent-skills`](https://github.com/plugin87/ux-ui-agent-skills)
at `d19a541` (v2.5.2, 2026-08-24), MIT.

Note: the upstream repo declares MIT in `README.md` and `package.json` but ships
no `LICENSE` file. The declaration is the licence grant of record here.

## What was taken

| Upstream | Here | Change |
|---|---|---|
| `tokens/*.json` (14 files, 450 tokens) | `assets/tokens/` | unchanged |
| `examples/golden/` | `assets/golden/` | unchanged; the fixture `validate_theme_refs` and `lint_hardcodes` default to |
| `examples/brandkit-demo/`, `examples/sample-app/` | `assets/fixtures/` | unchanged; render-gate targets |
| `scripts/validate_tokens.py` | same | token dir repointed to `assets/tokens/` |
| `scripts/validate_contrast.py` | same | colours repointed to `assets/tokens/colors.json` |
| `scripts/validate_theme_refs.py` | same | defaults repointed to `assets/golden/` |
| `scripts/lint_hardcodes.py`, `contrast.py` | same | unchanged |
| `scripts/build_tokens.mjs` | same | input dir repointed |
| 10 render gates | `scripts/*.mjs` | preflight, exit codes, keyboard fix — below |
| `.claude/rules/tokens-and-color.md` | `references/token-architecture.md` | paths repointed; CI paragraph rewritten to this skill's gates |
| `.claude/rules/typography-and-spacing.md` | `references/type-and-spacing.md` | paths repointed |

## What was changed, and why

**1. The silent skip is gone.** Every gate opened with:

```js
try { ({ chromium } = await import('playwright')); }
catch { console.log('<gate>: playwright not installed — SKIPPED'); process.exit(0); }
```

and launched with `chromium.launch({channel:'chrome'}).catch(() => chromium.launch())`.
A missing browser therefore exited 0. Upstream CI installs Chromium in a separate
`render` job, so upstream is not affected; anyone running the gates locally or
adopting the scripts is. `npm test` upstream contains no render gate at all.

`scripts/lib/browser.mjs` replaces both with `openBrowser()`, which exits 1 and
prints `BLOCKED` plus the builds actually present in the Playwright cache. The
same treatment covers the usage paths — `node verify_rtl.mjs` with no argument
was also exit 0.

**2. Exit codes separated.** Upstream used exit 1 for both "could not run" and
"found violations". Here: 0 clean, 1 blocked, 2 findings — matching this repo's
`scripts/design-qa-detect.sh`.

**3. axe-core is local only.** Upstream fell back to
`https://cdnjs.cloudflare.com/.../axe-core/4.10.2/axe.min.js` when `node_modules`
lacked it, then skipped (exit 0) if that also failed. A gate whose rule set can
arrive from two sources can disagree with itself between runs. `injectAxe()`
resolves locally or blocks, and prints the version that ran.

**4. `verify_keyboard.mjs` collection bug fixed.** The loop read:

```js
if (!vis(el) || !operable(el) || !tabbable(el)) continue;
```

so a control that is not in the tab order was removed from the population rather
than reported — the exact WCAG 2.1.1 failure the gate exists to catch, and the
one its own "Fix A" line describes. Non-tabbable elements carrying an interactive
role, outside a composite widget (whose roving-tabindex items are checked
separately) and not `aria-hidden`, now report `[A0 not-in-tab-order]`.

**5. `DESIGN_TOKENS_CHROMIUM` added.** This machine has Playwright installed with
cached Chromium builds 1208 and 1234 while the installed Playwright expects 1228,
so the bundled launch fails. `auto` selects the newest cached build and prints
it; an explicit path is checked with `existsSync` first, because `executablePath`
is accepted without verification and a wrong path launches nothing while looking
configured.

## What was deliberately not taken

- **The 17 `SKILL.md` files.** Two collide by name with skills already here
  (`design-review`, `prototype`), and the rest land on a design surface already
  held by `impeccable`, `refero-design`, `frontend-ui-engineering`, `design-html`,
  and `ce-frontend-design`.
- **`CLAUDE.md`, `.claude/rules/`, the Request Router, `templates/product-design/`.**
  These assume the kit governs a product repo's instruction surface;
  `validate_instruction_surface.py` enforces a 320-line CLAUDE.md budget. That is
  the half that exists because the project owns its own repo.
- **`taste/`, `slop_tells.mjs`, `taste_audit.mjs`, `lint_intent.mjs`.** Aesthetic
  judgement, held here by `impeccable` and `refero-design`.
- **`frameworks/` (16 adapters), `components/`, `accessibility/`, `workflows/`.**
  Mostly restatements of framework and WCAG documentation.
- **`evals/`, `accuracy_report.mjs`.** They score upstream's own reference app.
- **`design-systems/library/` (138 systems).** Taken, but to
  `skills/refero-design/references/design-systems/` where reference corpora
  belong — not here.
