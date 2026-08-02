# Building a design template from a source deck (re-author route)

**Load this when:** Route 0 selected **re-author** — the user wants a new/expanded
deck that must still look like their reference. Not for verbatim reproduction
(use `verbatim-recovery.md`), and not for this skill's stock template.

The goal is a deck that is *ours to regenerate* but *theirs to look at*: identity
extracted from the source, structure owned by us, reskinnable from one file.

## Three files, three jobs — never blur them

| File | Owns | Rule |
|---|---|---|
| `theme.css` | Identity: palette, type roles, surfaces | **Tokens only.** Swap this file to reskin the whole deck. |
| `template.css` | Structure: chrome rails, archetypes, spacing | Reads `var(--…)` only. **No hex literals, no font names.** |
| `build_deck.py` | Content: the slide spec → `deck.html` | No styling decisions. Emits classes, not inline colour. |

If a colour or font name appears in `template.css`, the reskin is already broken.

## Step 1 — extract identity, do not invent it

Pull the source's real tokens (for Genspark: its `chrome.css` — see
`verbatim-recovery.md`). Transcribe them verbatim into `theme.css`: grounds,
rules, ink ramp, semantic accents, font roles, type scale. Keep the source's own
semantic intent (which accent means *us*, which means *risk*).

Then read 3–4 rendered slides to learn the **layout system**, not just the colours:
margins, content width, the chrome rails top and bottom, panel radius and border,
the KPI/stat band, the card grid. Those details are what make it recognisable.

## Step 2 — structure, with two hard-won rules

**Centre the content column; don't hand-place bands.** Per-slide magic
`top:`/`height:` numbers produce slides that are top-heavy with a dead bottom
third. One absolutely positioned column between the rails, vertically centred,
makes every slide compose itself:

```css
.cbody{position:absolute;left:120px;top:272px;width:1680px;height:692px;
  display:flex;flex-direction:column;justify-content:center;gap:26px}
```

**Let cards stretch and distribute.** A tall card with top-aligned content reads
hollow. Make the card a flex column and pin the body low:

```css
.card{display:flex;flex-direction:column}
.card .p{margin-top:auto;padding-top:18px}   /* label top, body bottom */
```
Watch for later rules re-setting `margin-top` on the same element and defeating this.

## Step 3 — keep it exportable

Everything in `references/hybrid-export-traps.md` applies to CSS you author:

- Never style an inline tag (`span`, `b`, `em`) `display:block` — it is captured
  twice and prints on top of itself. Use `<br>` with an inline child.
- Give any element whose box hugs its glyphs a full-width block box, or
  PowerPoint's metrics push the last character onto a second line:
  `.pct{display:block;width:100%;text-align:center}`
- Percentage-height bars are fine; percentage-height *text* is not.

## Step 4 — generate, then gate

Emit `deck.html` from a spec so the deck is reproducible and the run folder can
rebuild it. Then run the full ladder: `render.mjs` → contact sheets (look at every
one) → `check_layout_overflow.mjs` → `render_hybrid.mjs` →
**`check_export_coverage.mjs`** → `build_editable_pptx.py --stage <w>` →
`officecli_qa.py` → per-slide Office renders of the densest slides.

## Honest limits of this route

A derived template is *not* the source deck. It will differ in density, in the
diagrams you did not rebuild, and in any archetype you chose not to implement. If
the user wants their deck, this route is the wrong one — reproduce it verbatim.
Say which route you took and why, in one line, at delivery.
