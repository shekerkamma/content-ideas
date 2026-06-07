# Body Numeral Textured — Usage Guide

## What this template is for
Numbered content slides in a LinkedIn carousel. Shows a large step number, heading, body text, and optional code snippet.

## How to customize

### Content areas (marked with `<!-- EDIT -->` in template.html):
1. **Numeral** (`.numeral`) — Two-digit step number: 01, 02, 03, etc.
2. **Heading** (`.slide-heading`) — 3-6 word section title.
3. **Body** (`.slide-body`) — 2-3 short sentences. Keep direct — no hedging.
4. **Code block** (`.code-block`) — Optional. Remove the div entirely if not needed. Use `<span class="keyword">`, `<span class="string">`, `<span class="comment">` for syntax highlighting.

### Pagination
Update `pagination__dot--active` to match the current slide position.

## Design tokens used
- `--color-primary` → canvas background
- `--color-secondary` → numeral color (subtle, large)
- `--color-accent` → accent bar, code keywords, numeral shadow
- `--color-text-on-dark` → heading text
- `--color-muted` → body text, masthead
- `--font-display` → numeral, heading
- `--font-body` → body text, masthead
- `--font-mono` → code block

## Rendering
Open `template.html` in a browser at 1080px width. Screenshot at 1080x1350.
