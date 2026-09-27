---
name: web-design-guidelines
description: "Review UI code and web interfaces for compliance with Vercel Labs Web Interface Guidelines (accessibility, focus states, forms, animation, typography, content handling, images, performance). Outputs terse file:line violations."
---

# Web Interface Guidelines

Review codebases, components, and web interfaces for strict compliance with the **Vercel Labs Web Interface Guidelines**.

## How It Works

1. **Rule Retrieval:** Uses the standard normative ruleset from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`.
2. **File Scope:** Inspects target source files (`.tsx`, `.jsx`, `.vue`, `.svelte`, `.html`, `.css`) or user-specified paths.
3. **Automated & Semantic Audit:** Checks code against all accessibility, interaction, animation, and typography rules.
4. **Terse Reporting:** Outputs findings in high signal-to-noise `file:line` format.

---

## The Rulebook

### 1. Accessibility (a11y)
- **Buttons & Actions:**
  - Icon-only buttons MUST have an explicit `aria-label`.
  - Use `<button>` for actions and `<a>`/`<Link>` for navigation. Never `<div onClick={...}>`.
  - Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`).
- **Form Controls:**
  - Form controls MUST have an associated `<label>` (via `htmlFor` or wrapping) or `aria-label`.
  - Checkboxes/radios: label + control share a single hit target without dead zones.
- **Media & Decorative Elements:**
  - `<img>` must have `alt` (or `alt=""` if strictly decorative).
  - Decorative icons must have `aria-hidden="true"`.
  - Meaningful audio/video requires transcripts, captions, or descriptive alternatives.
- **Semantic Structure:**
  - Use semantic HTML (`<button>`, `<a>`, `<label>`, `<table>`) before reaching for ARIA attributes.
  - Headings must follow a strict hierarchy (`<h1>` through `<h6>`).
  - Heading anchors must include `scroll-margin-top` to avoid sticky header clipping.
  - Include a skip link (`<a href="#main" className="sr-only focus:not-sr-only">Skip to content</a>`).
- **Live Updates:**
  - Async state updates (toast notifications, validation messages, streaming outputs) need `aria-live="polite"`.

---

### 2. Focus States
- **Visibility:** Interactive elements MUST have visible focus states (`focus-visible:ring-*` or equivalent).
- **No Naked Outlines:** Never use `outline-none` or `outline: none` without a custom focus replacement.
- **Focus Pseudo-classes:**
  - Prefer `:focus-visible` over `:focus` to prevent awkward focus rings on pointer clicks.
  - Use `:focus-within` for composite controls and input groups.
- **Sticky Elements:** Sticky headers, footers, and floating overlays must not obscure the currently focused element.

---

### 3. Forms
- **Attributes:** Inputs need `autocomplete` and meaningful `name` attributes.
- **Input Types:** Use appropriate `type` (`email`, `tel`, `url`, `number`) and `inputmode`.
- **Paste Preservation:** Never block pasting (`onPaste` + `preventDefault()` is prohibited).
- **Typo & Spellcheck:** Disable spellcheck on email addresses, tokens, and usernames (`spellCheck={false}`).
- **Submissions:**
  - Submit buttons stay enabled until the network request begins; display a spinner/loading state during in-flight requests.
  - Errors must render inline next to fields; automatically focus the first invalid field upon validation failure.
  - Placeholders end with `…` and show an example pattern.

---

### 4. Animation & Motion
- **Reduced Motion:** ALWAYS honor `@media (prefers-reduced-motion: reduce)`. Provide static alternatives or disable looping motion.
- **Compositor Friendly:** Animate `transform` and `opacity` only.
- **No Global Transitions:** Never use `transition: all`. Explicitly enumerate transition properties.
- **Transform Origin:** Set explicit `transform-origin` and for SVGs use `transform-box: fill-box; transform-origin: center`.
- **Interruptibility:** Animations must be interruptible and respond immediately to mid-flight user input.
- **Autoplay Controls:** Any autoplaying motion lasting >5 seconds must have pause, stop, or hide controls.

---

### 5. Typography
- **Punctuation:** Use proper ellipsis character `…` instead of triple dots `...`.
- **Quotes:** Use curly quotes `“` `”` / `‘` `’` instead of straight quotes `"` / `'`.
- **Non-breaking Spaces:** Use non-breaking spaces between quantities and units: `10&nbsp;MB`, `300&nbsp;cycles`, `114&nbsp;MHz`, `⌘&nbsp;K`.
- **Tabular Figures:** Apply `font-variant-numeric: tabular-nums` to numbers in tables, metrics, counters, and registers.
- **Widow Prevention:** Apply `text-wrap: balance` or `text-pretty` on all headings and lead paragraphs.

---

### 6. Content Handling & Containers
- **Overflow:** Long text containers must handle overflow with `truncate`, `line-clamp-*`, or `break-words`.
- **Flex Shrinking:** Flex children containing text need `min-w-0` to allow ellipsis truncation.
- **Empty States:** Gracefully handle empty arrays or null responses without rendering broken layout frames.

---

### 7. Images & Assets
- **CLS Prevention:** `<img>` elements need explicit `width` and `height` attributes or aspect-ratio boxes to prevent layout shift.
- **Lazy Loading:** All below-the-fold images must specify `loading="lazy"`.
- **Critical Images:** Above-the-fold hero assets should use `fetchpriority="high"`.

---

### 8. Performance
- **Virtualization:** Virtualize lists with more than 50 items.
- **Layout Thrashing:** Do NOT perform layout reads (`getBoundingClientRect`, `offsetHeight`, `scrollTop`) inside rendering loops. Batch DOM reads and writes.

---

## Output Format

When auditing files, output findings in terse `file:line` format:

```text
app/components/DieExplorer.tsx:42: Icon button missing aria-label
app/components/Waveform.tsx:18: Unbounded loop missing prefers-reduced-motion check
app/page.tsx:88: Straight quotes used instead of curly quotes
app/dr.css:124: "transition: all" used instead of explicit transform/opacity
```
