# DESIGN.md — Aurora Glass

> Plain-text design system for AI coding/design agents (Google Stitch DESIGN.md format).
> Drop this in a project root and tell the agent: *"Build the UI using DESIGN.md."*
> Derived from the `neon` Marp theme (`~/.claude/skills/marp/SKILL.md`) so slide decks
> and app UI share one identity. Original tokens — safe for client work.

---

## 1. Visual Theme & Atmosphere

**Aurora Glass.** A near-black canvas with glassmorphism panels and a teal→sky→magenta
aurora gradient reserved for emphasis. The mood is precise, technical, and confident —
a dark control surface, not a playful consumer app. Dense with information but never
cluttered: whitespace and a single hairline border do the separating, not boxes-in-boxes.

- **Density:** Medium-high. Built for data, scorecards, and dashboards.
- **Philosophy:** One accent does the talking. Gradient is a spotlight, not wallpaper.
- **Avoid:** The generic-AI look — purple blob gradients, drop-shadowed white cards on
  grey, default Inter everywhere, rounded-everything.

---

## 2. Color Palette & Roles

| Token | Hex | Role |
|---|---|---|
| `--bg` | `#080b11` | Base canvas (page background) |
| `--bg-elev` | `#0f141d` | Elevated surface (cards, modals, nav) |
| `--glass` | `rgba(255,255,255,.04)` | Glass panel fill over canvas |
| `--line` | `rgba(255,255,255,.09)` | Hairline borders, dividers |
| `--ink` | `#eef2f7` | Primary text |
| `--soft` | `#aeb8c7` | Secondary text, captions |
| `--muted` | `#69748a` | Tertiary text, footnotes, page numbers |
| `--teal` | `#2dd4bf` | **Primary accent** — CTAs, links, active state, key numbers |
| `--sky` | `#38bdf8` | Secondary accent — info, secondary actions |
| `--magenta` | `#e879f9` | Tertiary accent — highlights, badges |
| `--amber` | `#f6b94b` | Warning / attention |
| Aurora gradient | `linear-gradient(135deg,#2dd4bf,#38bdf8,#e879f9)` | Hero headings, focus rings, top borders |

**Rule:** Teal is the only accent on a default screen. Sky/magenta/amber appear only to
differentiate ≥2 peer items (tabs, columns, statuses). Never use all four at once.

---

## 3. Typography Rules

- **Sans (UI + body):** `ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif`
- **Mono (labels/kickers/data):** `ui-monospace, "SF Mono", Menlo, monospace`

| Element | Size | Weight | Treatment |
|---|---|---|---|
| Display / H1 | 3.2rem | 800 | Aurora gradient text, letter-spacing −.02em, line-height 1.05 |
| H2 | 2rem | 800 | `--ink`, letter-spacing −.02em |
| H3 / eyebrow | 0.72rem | 400 | **Mono**, UPPERCASE, letter-spacing .22em, `--teal` |
| Body | 1rem (22px deck) | 400 | `--ink`, line-height 1.6 |
| Caption | 0.85rem | 400 | `--soft` |
| Stat number | 4–8rem | 800 | `--teal`, letter-spacing −.04em, line-height 1 |
| Data label | 0.72rem | 400 | Mono, UPPERCASE, letter-spacing .22em, `--muted` |

**Rule:** Mono uppercase = metadata (labels, kickers, tags, timestamps). Sans = content.
Gradient text only on the single largest heading per view.

---

## 4. Component Stylings

**Button — primary**
- Fill `--teal`, text `#080b11`, weight 600, radius 8px, padding 10px 20px.
- Hover: brightness 1.1 + glow `0 0 16px rgba(45,212,191,.4)`. Active: brightness .95.
- Focus: 2px ring `--teal` at 50% offset 2px.

**Button — secondary / ghost**
- Transparent fill, 1px `--line` border, text `--soft`. Hover: border `--teal`, text `--teal`.

**Card / panel**
- Fill `--glass`, 1px `--line` border, radius 12px, padding 24px 28px.
- Optional top accent: 3px aurora-gradient border-image.
- Hover (interactive): border `--teal`, subtle lift (see §6).

**Input / select**
- Fill `--bg-elev`, 1px `--line` border, radius 8px, text `--ink`, placeholder `--muted`.
- Focus: border `--teal` + ring `0 0 0 3px rgba(45,212,191,.15)`. Error: border `--amber`.

**Navigation**
- Bar fill `--bg-elev`, bottom 1px `--line`. Item rest `--soft`; active `--ink` with a
  2px `--teal` underline. Mono uppercase for nav labels is optional, not default.

**Pill / tag / badge**
- Mono 0.68rem UPPERCASE, padding 5px 14px, radius 999px, 1px border.
- Neutral: border `--line`, text `--soft`. Accent variants recolor border+text to teal/sky/magenta.

**List item**
- No bullets. Custom marker `→` in `--teal` mono, 1.4em hang. Line-height 1.6.

**Blockquote / pull quote**
- 4px left border `--teal` + glow `−4px 0 12px rgba(45,212,191,.4)`, italic, `--soft`.

---

## 5. Layout Principles

- **Spacing scale (px):** 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 80. Use multiples only.
- **Grid:** 12-col, 24px gutter, max content width ~1200px, centered.
- **Page padding:** 60–80px desktop, 24px mobile.
- **Whitespace philosophy:** Separate with space and one hairline, not nested boxes or
  shadows. One idea per panel. Let the canvas breathe around stat numbers.
- **Two-up layout:** equal columns split by a 1px gradient rule, not a gap alone.

---

## 6. Depth & Elevation

Depth comes from **surface lightness + hairlines + accent glow**, not heavy shadows.

| Level | Surface | Border | Shadow |
|---|---|---|---|
| 0 — canvas | `--bg` | — | none |
| 1 — panel | `--glass` | `--line` | none |
| 2 — card hover | `--glass` | `--teal` | `0 8px 24px rgba(0,0,0,.4)` |
| 3 — modal/popover | `--bg-elev` | `--line` | `0 16px 48px rgba(0,0,0,.6)` |

Accent glow (`0 0 16px rgba(45,212,191,.4)`) signals *interactive/active*, never decoration.

---

## 7. Do's and Don'ts

**Do**
- Keep teal as the lone accent on a default screen.
- Use mono-uppercase for metadata and sans for content.
- Reserve the aurora gradient for the one hero heading and top accents.
- Separate with hairlines (`--line`) and space.
- Make numbers exact and large — the stat is the hero.

**Don't**
- Don't use white/light cards on the dark canvas — use `--glass`.
- Don't stack 3+ accent colors in one view.
- Don't put gradient on body text or multiple headings.
- Don't add drop shadows for decoration — depth is surface + hairline + glow.
- Don't round everything; 8px controls / 12px panels / 999px pills only.

---

## 8. Responsive Behavior

- **Breakpoints:** mobile <640px · tablet 640–1024px · desktop >1024px.
- **Touch targets:** ≥44px. Buttons grow to 12px 24px padding on touch.
- **Collapse:** two-up columns stack vertically <768px; the 1px gradient rule becomes a
  horizontal divider. Nav collapses to a sheet. Page padding 80px → 24px.
- **Type:** Display H1 clamps `clamp(2.2rem, 6vw, 3.2rem)`; stat numbers `clamp(3rem, 12vw, 8rem)`.

---

## 9. Agent Prompt Guide

**Quick color reference**
```
canvas #080b11 · surface #0f141d · glass rgba(255,255,255,.04) · line rgba(255,255,255,.09)
ink #eef2f7 · soft #aeb8c7 · muted #69748a
TEAL #2dd4bf (primary) · sky #38bdf8 · magenta #e879f9 · amber #f6b94b
gradient 135deg #2dd4bf→#38bdf8→#e879f9
font sans: system-ui · mono: ui-monospace · radius 8/12/999 · spacing ×4
```

**Ready-to-use prompts**
- *"Build a dashboard card per DESIGN.md: glass panel, hairline border, mono-uppercase
  eyebrow, one large teal stat number, →-marker list. Teal is the only accent."*
- *"Style this form per DESIGN.md: bg-elev inputs, teal focus ring, amber error border,
  primary teal button with hover glow."*
- *"Apply Aurora Glass: near-black canvas, gradient only on the page H1, everything else
  ink/soft/muted. No white cards, no drop shadows."*

**Design verbs (shared vocabulary)** — shorthand harvested from Impeccable. Use as
*"<verb> this per DESIGN.md"* to direct a change without re-explaining the system:

| Verb | Means, in Aurora Glass terms |
|---|---|
| **bolder** | Commit harder — bigger stat number, stronger H1 gradient, more whitespace around the hero. Raise contrast, don't add color. |
| **quieter** | Drop to teal-only, remove extra accents/badges, thin to one hairline, kill decorative glow. |
| **distill** | Strip redundant chrome — collapse nested panels into one, delete boxes-in-boxes, cut anything not carrying information. |
| **harden** | Add the missing states: loading, empty, error (amber border), and overflow/long-content for every panel, list, and form. |
| **critique** | Structured pre-ship review against §7 Do's/Don'ts — name each violation and its fix; no vague praise. |
| **polish** | Final pass — align to the 4px scale, fix orphan words (`text-wrap: balance`), verify focus rings and 44px touch targets. |

---

### Sync notes
- **Slides:** same tokens live in the `neon` Marp theme (`~/.claude/skills/marp/SKILL.md`,
  `:root` block). Edit tokens in both to keep deck + app identical.
- **Tokens as CSS vars:** copy the §2 table into `:root {}` to wire this into any web app.
- **License:** original tokens (Aurora Glass), not a third-party brand — safe for client UI.
