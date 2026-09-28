---
name: tweak
description: Use when someone wants to adjust a page's look by hand and keep the result — "tweak the spacing", "let me play with the colours", "give me sliders", "fine-tune the design tokens", "hide that section and see how it looks", "/tweak". Serves an HTML page or a built site with a slider panel over its CSS custom properties (colour pickers for colours, sliders for sizes and durations, toggles to hide sections), applies changes live, and on Bake writes the chosen values back into the source stylesheet with a backup. Model-free and deterministic. Not for generating new design variants (impeccable live) or for pages without CSS tokens.
license: MIT
metadata:
  category: Design tooling
  version: '1.0'
  cost-tier: 'Haiku: the agent starts one script and reads its bake report; no model judgment is involved in the tuning itself.'
---

# /tweak: sliders, then bake

Claude Design has a Tweaks panel. This is the same idea for any page on disk: tune the design tokens by eye
in a real browser, then write the numbers back into the stylesheet that owns them. The agent sets it up and
reads the result; the tuning is yours and involves no model calls.

It works on **CSS custom properties declared in a top-level `:root { }`**, which is how token-driven sites
(design-tokens, DESIGN.md, v3) are built. Hard-coded values are out of reach by design: a page with no
tokens gets a BLOCKED message, which is the honest answer, since there is nothing to bake into.

## Run it

```bash
S=<this skill's directory>/scripts
python3 $S/tweak.py <site-root> --bake-into <source.css> [<more.css> ...] [--port 8791] [--page index.html]
```

- `<site-root>`: the folder to serve: a static site, or a build's output (`dist/pages`).
- `--bake-into`: the **source** stylesheet(s) declaring the tokens. For a built site these are the source
  files (`app/v3.css`), never the hashed bundle, which the next build would overwrite.
- Open the printed URL. The panel sits top-right: colours, sizes, other tokens, then a toggle for every
  section that has an `id`. **Bake** writes and prints what changed; **Reset** reloads.

Try it on the bundled demo first:
`python3 $S/tweak.py <skill>/assets/demo --bake-into <skill>/assets/demo/styles.css`
(work on a copy if you want to keep the demo pristine).

For a built site, rebuild after baking (checking the build's exit code) to see the baked values in the
bundle; the panel previews them live without a rebuild.

## What Bake does, exactly

- Each changed token is written into the declaration the cascade uses: the **last** top-level `:root`
  declaration, later `--bake-into` files winning. Only the value text changes; nothing else in the file
  moves (asserted by the tests).
- `:root` blocks inside `@media`, `@supports` or any other at-rule are **never** edited. A dark-mode
  override is a different value on purpose; retune it by switching the OS theme and editing that block
  by hand, or bake light first and edit dark after.
- A value containing `;`, `{` or `}` is refused, so a paste cannot inject a rule.
- Hidden sections are written as one marked block at the end of the first file,
  `/* tweak: hidden sections (baked) */ … /* tweak: end hidden sections */`, with `display: none`.
  Markup is never deleted; un-hide and bake again to remove the block.
- Every bake first copies each touched file to `<file>.bak-tweak-<timestamp>`.

## Judgment rules

- **Tokens only.** If the value you want to move is hard-coded, the fix is to make it a token first
  (design-tokens), not to widen this tool to rewrite arbitrary CSS.
- **Light first.** The tool edits top-level `:root` only; treat dark-mode values as a second, manual pass.
- **Bake is a draft, not a release.** After baking, run the page's QA (e2e-qa-review): a spacing or
  colour change can break contrast, target size or a layout at phone width.
- **Hidden is not removed.** If a section should go for good, delete it in the source in its own change.

## Gotchas

- The panel only finds sections with an `id`; give a section an id to make it toggleable.
- `--bake-into` must name the file where the token is **declared**. If the panel shows a token but Bake
  reports "not declared in a top-level :root", the declaration lives in another file or inside an
  at-rule.
- The server binds 127.0.0.1 and bakes only with the per-run token injected into the served page; opening
  the page from another origin or `file://` shows no panel.
- Never ship `panel.js`: it is injected at serve time and is not written into your files.

## Skill Relationships

| Skill | Pattern | Handoff |
|---|---|---|
| `design-tokens` | Upstream | the `:root` token contract this tool edits |
| `impeccable` (`live`) | Peer | model-generated variants of an element; tweak is model-free token tuning |
| `e2e-qa-review` | Downstream verifier | re-run the sweep after a bake |
| `hig` | Constraint | keep targets at 44 px and body text at 17 px while tuning a mobile page |

## Host Compatibility

Stdlib Python and a browser; no symlinks or shell-specific calls. Works in Claude Code, Codex, DeepSeek
Harness and OpenHands; on Windows run `python`. Canonical at `skills/tweak/`, byte-identical mirror at
`.agents/skills/tweak/`. `tests/test_tweak.py` covers the parser, the bake and its refusals, the token
check, and a Chromium run that drags a slider and bakes.
