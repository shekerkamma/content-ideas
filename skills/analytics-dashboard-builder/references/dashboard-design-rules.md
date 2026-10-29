# Dashboard design rules

A one page reference for building a business dashboard someone will actually open every morning.

None of this is taste. Every rule here comes from a page that looked fine in a screenshot and got rejected the moment somebody read it, usually one of ours. Where a rule has a number in it, the number is there because a vaguer version of the rule got ignored.

Built by Ben AI. It is the same reference the `analytics-dashboard-builder` skill works to.

---

## Start with the cut test

Before anything visual. For every number you are thinking of putting on the page, ask one question:

**Would you do something differently because it moved?**

If not, it does not get a slot. That single test is what separates a dashboard from a wall of tiles. Five to fifteen numbers is a dashboard. Forty is a report nobody reads, and a report nobody reads cannot be filtered down later, because by then everything on it looks equally load-bearing.

---

## The look to aim for

A modern developer-platform dashboard. The Vercel dashboard is the reference: near-neutral greys, hairline borders, one accent used sparingly, thin geometric icons, tight consistent spacing, interactions that feel immediate.

Clean and technical. An instrument panel, not a poster.

Concretely:

- Hairline borders, 1px at low contrast. A thick outline reads as a sticker
- Elevation by background lift, not by shadow. A card sits above the page because it is a step lighter or darker
- One radius everywhere, 6px or 8px. Cards, chips, pills, tooltips, all the same
- Five neutrals and one accent will build the whole page
- One spacing scale: 4, 8, 12, 16, 24, 32. No other numbers

Your brand sits on top of this as a layer, not instead of it. Apply brand character in light mode at the quietest setting that still reads as your brand, and keep the grid, the spacing and the icon weight underneath it.

---

## The fourteen things that get a page rejected

1. **Text below 14px.** Anywhere. Not labels, not notes, not axis text, not tooltips. If it does not fit at 14px, the words are too long or the box is too small
2. **A rule line under or beside a section name.** The thin line trailing off a heading is the single most recognisable sign a machine built the page. Use space instead
3. **Any decorative divider.** No `<hr>`, no gradient hairline, no border under a heading. Borders enclose things
4. **Transparent cards.** Solid fill that differs from the page ground, plus a visible border. Floating text reads as unfinished
5. **A small grey subtitle beside a section heading.** "Acquisition *coming in*". Delete it. The heading is the label
6. **Freshness text in the header.** One icon with the detail on hover. Not a string listing every source and its timestamp
7. **Narration on a card.** "The month where the machine is spinning" is a sentence a person writes. Cards carry a noun label, a number, a delta, one factual note
8. **Badge spam.** Two status pills on the whole page, maximum
9. **An info marker on every title.** Four per page, maximum. By the fifth it is wallpaper
10. **An empty box.** Content pinned top and bottom with a void between is worse than a smaller card. Fill the box or shrink the box
11. **No logo.** Your logo goes in the header. Real vendor marks where the data comes from
12. **Italics.** Not for vendor names, not for units, not for emphasis. Use weight or colour
13. **A serif.** Including one you reach by accident. See Fonts below, because this one is nearly always an accident
14. **A hard offset shadow on a dark ground.** It reads as a double edge. Dark mode separates surfaces with lift and a hairline border

---

## The mistake that causes most of the others

**Do not force the page into one viewport height.**

`overflow: hidden` with flex rows looks like discipline. It is the root cause of nearly every other fault: labels shrink to unreadable sizes, bars compress to slivers, and cards develop voids because a flex row stretched a box with nothing to fill it.

Size the content properly and let the page be as tall as it needs. A page and a half of scroll is fine.

---

## Fonts

The rule people miss, and it fails silently.

**Your font stack has to resolve to a face that is actually there.** If the page cannot make external requests, and your brand font is not installed on the machine viewing it, the stack falls through to whatever is last. We shipped a test build where a brand stack ended in Georgia, and the entire dashboard rendered as a serif. It passed every other check and looked like a printed quarterly report.

So: embed the brand font as a data URI when the licence allows, which open licensed fonts do. Otherwise append a system sans before any serif fallback. Never leave a serif at the end of a stack.

Then check what actually rendered rather than what you asked for. A stack is a wish. The computed value is the fact.

---

## Type

| Role | Size | Weight |
|---|---|---|
| Hero number | 48 to 60px | 600 to 700, monospace |
| Section header | 20 to 24px | 600 to 700 |
| Card title | 15px | 600, uppercase |
| Card value | 28 to 36px | 600 to 700, monospace |
| Delta | 15px | 700 |
| Note | 14px | 400 |
| Chart labels and axes | 14px | 400 to 600 |

Three sizes per card, no more. Five sizes reads as a ransom note.

**Monospace for every numeral.** Numbers in a proportional font change width as they change value, which makes a refreshing dashboard visibly jitter.

**Contrast, not just size.** Grey around `#999` measures about 2.8:1 on white and fails accessibility even at a readable size. Use `#666` as the floor.

The honest cost of the 14px floor: axis labels at 14px need a wide category gutter, and that width comes out of your bars. Buy it back by shortening the label text, never by shrinking the type.

---

## Cards

- Uniform heights inside every row. Ragged boxes are the loudest visual complaint there is
- Pin the note line to the bottom so cards with different content still align
- Label, value, delta, one note. No subtitles
- A single number in a big box reads as empty. Give counting metrics two or three windows: 24 hours, 7 days, 30 days
- When a metric genuinely has one window, fill the box with factual key and value rows. Never invent a second window to fill space
- The window belongs at the top of the card, at title size. Not at the bottom in small grey text
- Definitions go in a tooltip on the title, not on the face of the tile

---

## Charts

| The question | The mark |
|---|---|
| How does this compare across categories | Horizontal bars, sorted, values at the end |
| How has this moved over time | Line, or area for a single series |
| What is the composition of a whole | Stacked bar. A donut only for two or three well-separated parts |
| How does this sit against a target | Progress bar or meter with the target marked |
| Where in a range do things sit | Histogram with real bands |

- A part-to-whole mark asserts the parts sum to the whole. Two independent rates do not, so they are bars
- Value labels sit outside the end of the bar, always. Never inside for some bars and outside for others
- Time axes run in date order, with dates. An axis of "age in days" reads backwards
- Draw missing data as a hatch or a dashed outline, never as a colour. A gap must never look like a real low value
- Draw chart text at real pixels. A `viewBox` with `width: 100%` silently rescales your 14px text below the floor

---

## Colour

- **Direction, not sign.** Every metric declares whether up is good, up is bad, or neutral. Churn rising is bad even though the number rose
- A confounded comparison renders neutral, with the reason on the card
- Two categories that are not good and bad get an accent and a neutral, not green and red
- One accent hue. Status colours are a separate small set. A gradient across a progress bar is decoration
- If your brand hands you four pale tints, use one as the card fill on every card and move the rest to section identity. Four tints across the cards reads as colour coding whether you meant it or not: a pink card beside a green one looks like bad beside good
- Check every pair sharing a chart stays distinguishable under the common colour-vision deficiencies. Ours did not, the first time

---

## Light and dark

Ship both. Same data, same structure, same geometry, same spacing, same icon set.

**Elevation is the one thing that changes.** Light mode can carry a soft or hard shadow. Dark mode separates surfaces with background lift and a hairline border, and no offset shadow. A light hard-edged shadow behind a dark card looks like a rendering fault.

Sectioning in dark should be subtle. If you can clearly see where the separation comes from, it is too strong.

Dark is the mode people keep open, so check your data ink there specifically. A pale tint that works on white often falls below contrast on near-black.

---

## Interactions

Cheap, and it is the difference between a product and a screenshot.

- Hover state and a visible focus ring on everything interactive. Nothing on things that do nothing, because that promises an action that is not there
- Transitions of 120 to 160ms, on colour and opacity only. Never on width, height or position
- Tabs get a sliding indicator, not a jumping one
- Nothing animates on page load. An entrance animation delays the first number by exactly as long as it runs

---

## The eight checks that stop a wrong number shipping

The design rules decide whether the page gets used. These decide whether it can be trusted.

1. **Never invent a number.** A missing figure renders as a card saying what is missing and why. A blank prompts a fix; a plausible wrong number prompts a decision
2. **Numerator and denominator come from the same population.** The most common cause of a wrong rate. Cancelled *people* over open *subscriptions* is meaningless and looks fine
3. **Flows have to close.** Customers at period start, plus new, plus reactivated, minus churned, equals customers today. This catches more errors than every other check combined
4. **State the population on every card.** "667 members" and "756 subscriptions" for the same business is fine if both say which. It is a bug if neither does
5. **Recompute every supplied ratio from its own inputs.** They disagree more often than you would think. Show one figure, never both
6. **Check the definition, not just the arithmetic.** A rate can recompute perfectly and still use the wrong denominator. Churn over customers at period *end* is not churn over customers at period *start*
7. **Check significance before calling something a finding.** Two rates a few points apart on samples in the low hundreds are noise. Drawing noise in red and green asserts a conclusion the data cannot support
8. **Never age a number forward.** If a source will not answer, leave the card as not tracked with the reason. A stale figure presented as current is the failure mode that actually costs money, because it is the one that gets acted on

---

## Before you publish

Screenshot the page and read the screenshot.

Every fault in the list of fourteen is visible in a screenshot and invisible in the source. That is why every one of them shipped: the person who built the page read their intention instead of the pixels.

Better still, have someone else check it. A reviewer who does not know what you were going for sees what is actually there.

---

Credits where they are due: the density principle is IBCS **Condense**. The mistakes list owes a lot to Stephen Few's work on dashboard design, and the data-ink thinking to Tufte. Everything else we learned by getting our own dashboard wrong and fixing it.

**Ben AI** . [benai.co](https://benai.co)
