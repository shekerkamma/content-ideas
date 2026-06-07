# Cover Portrait CTA — Usage Guide

## What this template is for
The opening slide of a LinkedIn carousel. Dark background, large headline, subtitle hook, and swipe CTA.

## How to customize

### Content areas (marked with `<!-- EDIT -->` in template.html):
1. **Headline** (`.cover-title`) — 2-4 words per line, max 2 lines. Use `<br>` for line breaks.
2. **Subtitle** (`.cover-subtitle`) — 1 sentence hook. Keep under 15 words.
3. **CTA** (`.cta-text`) — Action text next to the arrow. Default: "Swipe to learn how"

### Masthead labels
Update the three `<span class="masthead__label">` elements:
- First: current month/year
- Second: your handle
- Third: your topic

### Pagination
Set the correct total dot count and mark the first as active (`pagination__dot--active`).

## Design tokens used
- `--color-primary` → background
- `--color-text-on-dark` → headline text
- `--color-accent` → accent bar, CTA arrow background
- `--color-muted` → subtitle, masthead labels
- `--font-display` → headline
- `--font-body` → subtitle, CTA, masthead

## Rendering
Open `template.html` in a browser at 1080px width. Screenshot at 1080x1350 for LinkedIn.
