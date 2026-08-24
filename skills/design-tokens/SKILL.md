---
name: design-tokens
description: Use when UI work needs a token contract and proof it survived to the rendered page — "design tokens", "DTCG", "token architecture", "one theme across every screen", "contrast check my theme", "does this UI actually pass WCAG 2.2", "my colours drift between pages", "audit a11y of this HTML", "reflow at 320px", "target size", "focus trap", "reduced motion". Generates and validates a 3-tier DTCG token set, then measures a real page in Chromium against ten WCAG 2.2 criteria. Not for visual direction or aesthetic critique — that is refero-design and impeccable.
license: MIT
metadata:
  category: Design Systems
  version: '1.0'
  compatibility: >-
    Validators are Python 3 stdlib only and run anywhere, including Codex.
    Render gates need Node >= 18 plus `npm i -D playwright axe-core` and a
    Chromium build; without them they report BLOCKED and exit 1.
  adapted-from: plugin87/ux-ui-agent-skills v2.5.2 (MIT) — see references/provenance.md
---

# Design Tokens

A design system is a contract in two halves, and most tooling only checks one.
The **source** half says `action.primary` is `#2563eb` and passes 5.17:1 on
white. The **rendered** half is whether the button on the page you shipped is
actually that colour, at that contrast, in dark mode, at 320px, with the focus
ring intact. This skill gates both, and refuses to conflate them.

Two commands, two different claims:

```bash
scripts/check.sh                        # the token source is internally consistent
DESIGN_TOKENS_CHROMIUM=auto \
  scripts/run_gates.sh page.html        # the rendered page meets WCAG 2.2
```

`check.sh` passing means nothing rendered correctly. It means the JSON is sound.

## When to invoke

- A project needs a token foundation: primitives, semantic aliases, component
  tokens, light and dark, in DTCG `$type`/`$value` form.
- Colours, spacing, or type drift between pages and you want one theme enforced.
- A page, component, or exported HTML deck needs a WCAG 2.2 AA verdict backed by
  measurement rather than inspection.
- A CI gate is wanted for design regressions.

Route elsewhere when the question is what the interface should *look* like:
`refero-design` (research-first visual direction), `impeccable` (craft, polish,
anti-slop), `dataviz` (chart colour), `artifact-design` (Artifact pages).

## The token contract

Read `references/token-architecture.md` before generating or editing tokens, and
`references/type-and-spacing.md` for scale and rhythm. The short version:

```
COMPONENT   button.primary-bg  →  {semantic.action.primary}   used in code
SEMANTIC    action.primary     →  {primitive.blue.600}        used in design
PRIMITIVE   blue.600           →  #2563EB                     never used directly
```

Dark mode swaps at the **semantic** layer only — primitives never change. A
component that reaches past its own tier is the drift these validators exist to
catch.

`assets/tokens/` holds a working 14-file, 450-token set (colour, type, spacing,
shadow, border, breakpoint, motion, gradient, opacity, blur, sizing, states,
theming, data-viz). Use it as the starting shape, not as a house style.

## Validators — stdlib Python, no browser

| Script | Claim it makes |
|---|---|
| `validate_tokens.py` | every file parses; every `{alias}` resolves |
| `validate_contrast.py` | the six required text/action pairs pass WCAG 2.2 in **both** light and dark; tertiary and decorative pairs are reported as advisory, not failed |
| `validate_theme_refs.py` | every `var(--x)` a component uses is defined in the theme — no floating tokens |
| `lint_hardcodes.py` | no raw hex, px, or timing in component code |

`build_tokens.mjs` emits the CSS-variable layer from the JSON (Node builtins
only). Tokens are authored once; every platform artifact is generated.

## Render gates — ten WCAG 2.2 criteria, measured

`run_gates.sh <page.html> [--dark] [--open=<selector>]` runs the battery and
aggregates: **0** clean, **1** blocked, **2** findings.

| Gate | Criterion | What it opens the page to find |
|---|---|---|
| `measure_render.mjs` | 1.4.3 | true alpha-composited contrast of every text node |
| `verify_states.mjs` | 1.4.3 / 1.4.11 | the same, in default, hover, and focus |
| `axe_audit.mjs` | WCAG 2.2 A/AA | roles, names, labels, landmarks, heading order |
| `verify_target_size.mjs` | 2.5.8 | targets under 24x24 that the spacing exception does not rescue |
| `verify_keyboard.mjs` | 2.1.1 | controls the tab order never reaches; Enter/Space/arrow behaviour |
| `verify_focustrap.mjs` | 2.1.2 / 2.4.3 | dialog traps Tab, Escape closes, focus returns |
| `verify_overflow.mjs` | 1.4.10 | silently clipped text, overlapping controls |
| `verify_responsive.mjs` | 1.4.10 | horizontal overflow at 280 / 320 / 414px |
| `verify_reduced_motion.mjs` | 2.3.3 | a reduce policy exists, motion actually stops, no content lost |
| `verify_rtl.mjs` | i18n | layout mirrors without RTL-only overflow |

### A gate that cannot run says so

Every gate here fails loudly when its dependencies are missing. That is the
single largest change from upstream, where each one opened with:

```js
catch { console.log('<gate>: playwright not installed — SKIPPED'); process.exit(0); }
```

Exit 0 on a missing browser is a green light over an unmeasured page. Upstream's
CI installs Chromium in a dedicated job so it never bites there; anyone running
the gates locally, or wiring them into another repo's test command, inherits a
suite that passes by not running. Here that path is `BLOCKED` on stderr and
exit 1, and `run_gates.sh` reports the page as UNMEASURED rather than reviewed.
The same applies to a gate invoked with no target, and to axe-core, which is
loaded from the local install only — never the CDN fallback upstream uses, which
would let the rule set drift between two runs of one gate.

If Playwright's expected Chromium build is absent but another is cached,
`DESIGN_TOKENS_CHROMIUM=auto` uses the newest one and prints which build and
version served the run. `DESIGN_TOKENS_CHROMIUM=<path>` pins one explicitly and
checks the file exists first — `executablePath` is accepted without being
verified, so a path that is set is not a path that resolves.

## Host Compatibility

| Host | Validators (`check.sh`) | Render gates (`run_gates.sh`) |
|---|---|---|
| Claude Code | yes | yes, with Node >= 18 + `npm i -D playwright axe-core` |
| Codex CLI / Desktop | yes — Python 3 stdlib, nothing to install | only where Node and a Chromium build exist |
| OpenHands / generic agent | yes | same condition |
| CI | yes | yes, if the job installs Chromium |

The split is deliberate: the token contract must never depend on a browser, so
the half that gates the source runs everywhere. When the render half cannot run
it reports BLOCKED and exit 1 — a host without Chromium gets no verdict, never a
pass. Do not paper over that by treating `check.sh` as the whole gate.

### Tool Mapping

Everything this skill does is a shell command over local files, so the mapping is
the same on every host: run the scripts with the host's shell tool (Bash on
Claude Code, the equivalent on Codex and OpenHands) and read the files with the
host's file tool. No MCP server, no host-specific API, no Claude-only field is
load-bearing. The exit codes are the interface — 0 clean, 1 blocked, 2 findings —
so a host that can run a command and read its status can run the whole gate.

### Source / Tool Order

This skill performs no external research and needs no network. It reads local
files only:

1. The project's own token source, theme, and component code — the artifact under test.
2. `references/token-architecture.md` and `references/type-and-spacing.md` for the rules.
3. `assets/tokens/` as the starting shape when a project has no tokens yet.

WCAG 2.2 criteria are pinned in the gates themselves and axe-core is resolved
from the local install, never fetched. If a criterion's interpretation is in
question, read the W3C Understanding document directly rather than searching —
and update the gate, not just the prose.

## Judgment rules

Editable policy for any tool this skill recommends. Tune it here; do not bake it
into the steps.

- **Popularity is not fit.** Style Dictionary is the default token build tool
  because it targets CSS, iOS, Android, and Compose from one source — not
  because it is the most starred. Pick Tokens Studio when Figma owns the tokens,
  a 90-line script when the only output is CSS variables, and Style Dictionary
  when more than two platforms consume the same source. `build_tokens.mjs` is
  that 90-line script; it exists so a one-platform project owes nothing to a
  build chain it will not use.
- **Split every comparable in two: what transfers, and what exists because that
  project got big.** Material 3 and Carbon carry token layers worth copying and
  governance apparatus that reflects their org size. `references/token-architecture.md`
  takes the 3-tier hierarchy and the dark-at-semantic rule; it does not import a
  contribution board or a promotion pipeline. State which half a recommendation
  rests on before sizing work against it.
- **Cost every vendor at three points.** Figma Variables, Tokens Studio, and
  Chromatic are free while one person is designing, per-editor or per-snapshot
  once a team touches them, and a roadmap constraint at 10x that. Name the cap
  and the crossing point, not today's invoice. The gates here have no vendor: the
  dependencies are Playwright and axe-core, both MIT/MPL and local.

## Verification

Executed 2026-08-24 on WSL2, Node v24.18.1, Python 3.12, Chromium 151.0.7922.34
(cached build 1234 via `DESIGN_TOKENS_CHROMIUM=auto`; the Playwright install
here expects build 1228, which is absent — the condition the preflight was
written for).

| Command | Result |
|---|---|
| `scripts/check.sh` | exit 0 — 450 tokens across 14 files, 12 required contrast pairs pass light and dark, 4 advisory warnings, 59 theme vars all resolved |
| `run_gates.sh assets/fixtures/brandkit/index.html` | exit 0 — 9 gates ran clean |
| `run_gates.sh assets/fixtures/sample-app/preview.html --open='#delBtn'` | exit 0 — 10 gates ran clean, focus trap included |
| `run_gates.sh assets/fixtures/sample-app/preview.html --dark` | exit 0 — 9 gates ran clean |
| `run_gates.sh assets/fixtures/broken/index.html` | **exit 2 — 6 of 9 gates fired**: contrast (1.84:1 and 1.25:1), states (3), axe (button-name, color-contrast, image-alt), target-size (6 at two widths), responsive (+660px at 280px), reduced-motion (no policy, motion continues) |
| every gate with Playwright's browser absent | exit 1, `BLOCKED`, page reported UNMEASURED |
| every gate with no target argument | exit 1 (upstream: exit 0) |

A clean run on a clean fixture proves nothing on its own — `assets/fixtures/broken/`
is the negative control, and it is broken by construction with each defect
commented against its criterion. If it ever passes, a gate has stopped measuring.

`verify_keyboard.mjs` was fixed during the port: its collection loop skipped
every non-tabbable control, so a `role="button"` div with no `tabindex` — the
plainest WCAG 2.1.1 failure, and the one its own "Fix A" text describes — was
filtered out of the population instead of reported. It now emits
`[A0 not-in-tab-order]`, verified to fire on the broken fixture and stay silent
on both clean ones.

## Known coverage limits

- `verify_overflow.mjs` looks for clipped text and overlapping controls, not page
  overflow; `verify_responsive.mjs` owns that. Both are needed.
- `verify_target_size.mjs` honours the WCAG 2.5.8 spacing exception, so isolated
  small targets pass legitimately. Adjacency is what makes them fail.
- None of these gates judge taste, hierarchy, or whether the design is any good.
  They judge whether it is measurable and accessible. Pair with `refero-design`
  or `impeccable` for the other question.
