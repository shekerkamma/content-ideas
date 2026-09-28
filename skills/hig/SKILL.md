---
name: hig
description: Use when designing, building or reviewing an app screen or a mobile web page against Apple's Human Interface Guidelines — "apply the HIG", "is this touch-friendly", "mobile screen", "iOS app screen", "tap targets", "Dynamic Type", "make it feel native on iPhone". Applies Apple's published numbers (text sizes, the iOS Dynamic Type table, control sizes, spacing, contrast, text scaling) as hard rules, maps points to CSS pixels for the web, and checks a page with e2e-qa-review's sweep at a 44 px target floor.
license: MIT
metadata:
  category: Design guidance
  version: '1.0'
  cost-tier: 'Haiku: the rules are numbers on the page; applying them needs no judgment beyond reading a layout.'
  sources: >-
    developer.apple.com/design/human-interface-guidelines: accessibility, typography (Specifications
    tables read from Apple's page data), layout. Read 2026-09-28.
---

# Apple Human Interface Guidelines, as rules

Apple publishes the numbers behind its interfaces. Used as rules instead of taste, they make any mobile
screen easier to read and tap, including a web page on an iPhone. Every number below is Apple's, from the
pages named in `sources`; none is rounded or remembered.

## When it applies

- A native iOS / iPadOS screen, or a design for one: all of it.
- A mobile web page or PWA: sizes, targets, spacing, contrast and text scaling. Not the native-only parts
  (SF Pro, Liquid Glass, SF Symbols, status bar), which a browser does not have.
- A desktop web page: contrast and the "more than colour alone" rule only. Desktop targets follow WCAG
  2.5.8 (24 CSS px), which e2e-qa-review already enforces.

## Points and CSS pixels

On an iPhone, one CSS pixel at `width=device-width` is one iOS point: an iPhone 14 is 390 × 844 pt and its
Safari viewport is 390 CSS px wide. So for a mobile web page, **read every pt below as CSS px**. This is not
true of print, PPTX or a desktop display; do not carry the mapping there.

## The numbers

**Text size** (accessibility and typography pages)

| Platform | Default | Minimum |
|---|---|---|
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

A thin custom font needs to be larger than these. Avoid Ultralight, Thin and Light weights for text.

**iOS Dynamic Type, Large (the default size)** (typography › Specifications)

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 34 | 41 | Bold |
| Title 1 | Regular | 28 | 34 | Bold |
| Title 2 | Regular | 22 | 28 | Bold |
| Title 3 | Regular | 20 | 25 | Semibold |
| Headline | Semibold | 17 | 22 | Semibold |
| Body | Regular | 17 | 22 | Semibold |
| Callout | Regular | 16 | 21 | Semibold |
| Subhead | Regular | 15 | 20 | Semibold |
| Footnote | Regular | 13 | 18 | Semibold |
| Caption 1 | Regular | 12 | 16 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

People can scale text: Apple asks for enlargement to **at least 200%** (140% on watchOS). Layouts must
survive it: stack inline items above or below text, reduce columns, keep truncation minimal, and keep the
most important content at the top.

**Controls** (accessibility › Mobility)

| Platform | Default | Minimum |
|---|---|---|
| iOS, iPadOS | 44 × 44 pt | 28 × 28 pt |
| macOS | 28 × 28 pt | 20 × 20 pt |
| tvOS | 66 × 66 pt | 56 × 56 pt |
| visionOS | 60 × 60 pt | 28 × 28 pt |
| watchOS | 44 × 44 pt | 28 × 28 pt |

Spacing counts as much as size: about **12 pt** of padding around elements with a bezel, about **24 pt**
around the visible edges of elements without one.

**Contrast** (accessibility › Vision; WCAG AA values)

| Text size | Weight | Minimum ratio |
|---|---|---|
| up to 17 pt | all | 4.5:1 |
| 18 pt | all | 3:1 |
| all | bold | 3:1 |

Check light and dark appearances both. Never carry meaning in colour alone: add a shape, icon or label.

**Layout** (layout page): group related items; put the most important content top and leading; respect
safe areas; on iOS avoid full-width buttons (inset them to the system margins); support both
orientations where you can, and if landscape-only, both rotations.

## Workflow

1. Say which platform the screen is for, and whether it is native or web (sets which rules apply).
2. Map the design's type scale onto the Dynamic Type table: body at 17, nothing under 11, headings from
   the table rather than invented sizes. For the web, emit these as tokens (`--text-body: 17px` …).
3. Size every tappable element to 44 × 44 (never below 28 × 28), with the padding above.
4. Check contrast against the table in both appearances.
5. Verify, don't eyeball. For a web page run e2e-qa-review's sweep at phone width with the HIG floor:
   `"minTarget": 44` in `qa/sweep.json` reports every control under 44 CSS px, and axe covers contrast.
   Zoom the page to 200% (or set the root font size to 200%) and confirm nothing truncates or overlaps.

## Judgment rules

- **Apple's number wins over a design's number** for text size, target size and contrast. A pinned brand
  look can change colour, typeface and shape, not these floors.
- **Default, then minimum.** Design at the default (44 pt, 17 pt); the minimum (28 pt, 11 pt) is a floor
  for dense secondary UI, never the plan.
- **Desktop web is not an iPhone.** Outside mobile, the WCAG 24 px target floor applies, not 44.
- **Re-read before relying on a number after an OS release.** Apple revises these pages; `sources` says
  when they were read.

## Gotchas

- The typography page's **Specifications** tables are tabbed by size (xSmall … xxxLarge, AX1–AX5). Only
  "Large (default)" is reproduced here; neighbouring tabs differ by 1–3 pt and are easy to copy by mistake.
- `pt` here is an iOS point. In PPTX, `pt` is a typographic point (1/72 in); the two are unrelated.

## Skill Relationships

| Skill | Pattern | Handoff |
|---|---|---|
| `e2e-qa-review` | Verifier | `minTarget: 44` in `qa/sweep.json`; its axe run covers contrast |
| `refero-design` | Complement | research and direction first; HIG sets the floors |
| `design-tokens` | Downstream | the type scale and target sizes land as tokens |
| `impeccable` | Complement | critique of hierarchy; HIG is the measurable floor |

## Host Compatibility

Plain Markdown with no scripts: works in Claude Code, Codex, DeepSeek Harness and OpenHands. Canonical at
`skills/hig/`, byte-identical mirror at `.agents/skills/hig/`.
