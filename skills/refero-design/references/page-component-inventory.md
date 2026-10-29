# Page component inventory

A coverage checklist for a marketing or product page: which blocks the page
needs, not how they should look. Run it against a draft to find the block you
forgot, then design that block from the subject — never from this list.

This is deliberately **visual-language-free**. Companion to
[reference-galleries.md](./reference-galleries.md) (where to look) and
[anti-ai-slop.md](./anti-ai-slop.md) (what not to copy).

## The blocks

| # | Block | Exists to |
|---|---|---|
| 1 | Pill label / eyebrow | Say what kind of page this is before the headline does |
| 2 | Buttons, with modifiers | Separate the primary action from every other one |
| 3 | Hero / cover | Hold one idea |
| 4 | Hero stat strip | Put the proof beside the claim, not three screens below it |
| 5 | Section wrapper | Give every section the same edges, so rhythm reads as intent |
| 6 | Problem cards | Name the reader's problem in their words |
| 7 | Before / after grid | Show the delta rather than asserting it |
| 8 | Numbered product cards | Carry a sequence when order actually matters |
| 9 | Feature cards with icon | Scan-read a capability set |
| 10 | Do / don't columns | Encode a judgement the reader will otherwise get wrong |
| 11 | Timeline | Answer "how long and in what order" |
| 12 | Commitment stat strip | Big numbers, once, where they carry the argument |
| 13 | Testimonial slab | Attributed proof — or omit the block entirely |
| 14 | Pricing card | Price, what's included, what isn't |
| 15 | Final CTA | One action, restated after the case is made |
| 16 | Footer | The part nobody designs; see Footer.design |
| 17 | Form fields | Intake without abandonment |
| 18 | Option cards | Replace a radio group when the choice deserves weight |
| 19 | Form progress | Tell a long form's reader where they are |
| 20 | Logo bar | Social proof — only with permission and real logos |

## How to use it

**As a coverage check, not a template.** A page needing eight of these should
have eight. Shipping all twenty because the list has twenty is how pages become
interchangeable.

**Question every block before including it.** A numbered card set implies a real
sequence. A timeline implies real dates. A testimonial implies a real customer.
A structural device that encodes nothing true is decoration.

**Blocks 13 and 20 carry a factual duty.** Testimonials and logo bars assert
things about other people. Real, attributed and permitted, or absent.

## Craft rules worth keeping

- **Paste tokens, never hand-type them.** A hand-typed hex is a divergence
  waiting to happen. Read them from the token file.
- **No placeholder copy.** Every sentence specific, or the block is not ready.
  Filler survives to production more often than anyone admits.
- **State your breakpoints as a pair and hold them.** Reflow the content; do not
  shrink the desktop composition.
- **Run an after-build checklist**, and make it about substance — token match,
  real copy, responsive behaviour — rather than a list of your own preferences.

## Provenance

Adapted from the component inventory and build rules in BenAI's `instant-ui`
skill (from the Fable 5.1 Toolkit page, retrieved 2026-09-09), which was **not
installed**. Applying this repo's evidence rule — split what transfers from what
exists only because that project is what it is — the inventory and the four
craft rules above transfer. The rest did not, and was deliberately dropped:

- Its visual identity (cream `#fffef8`, 3px borders, 6px hard shadows,
  weight-900 headings, a blue/green/amber stripe, a brand SVG) is one company's
  brand, and `instant-ui`'s stated goal is reproducing it **1:1**. That is the
  opposite of what `artifact-design` asks for here.
- Its `~/Desktop/builds/benai/` output path violates this repo's
  configurable-path rule.
- Its "system font plus SF Mono, no Google Fonts" constraint contradicts
  `artifact-design`, where Google Fonts is the one permitted font host.
- `design-tokens` already owns the token contract here **and** gates it with ten
  WCAG 2.2 render checks. `instant-ui` ships a fixed token set with no
  accessibility gate.
