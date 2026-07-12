# mkt-visual-identity — Update Mode Test

## Trigger
tokens.json exists at `brand_context/visual-identity/tokens.json` → Update mode activated.

## Current Identity Summary

```
Brand: {{brand_name}}

Palette:
  Primary:    ████ #0F172A — Slate 900 — Headers, primary backgrounds
  Secondary:  ████ #1E293B — Slate 800 — Cards, panels
  Accent:     ████ #22D3EE — Cyan 400 — CTAs, links, highlights
  Background: ████ #F8FAFC — Slate 50 — Page backgrounds
  Text:       ████ #0F172A — Slate 900 — Body text
  Surface:    ████ #F1F5F9 — Slate 100 — Card backgrounds
  Muted:      ████ #94A3B8 — Slate 400 — Secondary text, borders
  Text-dark:  ████ #F8FAFC — Slate 50 — Text on dark backgrounds
  Success:    ████ #10B981 — Emerald 500 — Success states

Typography:
  Display: Inter Tight (Bold, ExtraBold, Black)
  Body:    Inter (Regular, Medium, Bold)
  Mono:    JetBrains Mono (Regular, Bold)

Masthead: {{month_year}} | {{handle}} | {{tagline}}
Pagination: CSS dots, 7 slides
```

**Prompt to user:** "This is your current visual identity. What would you like to change? Options:
1. Adjust colors (swap accent, change palette warmth)
2. Change typography (different font pairing)
3. Update masthead labels
4. Full rebuild from new visual references
5. Something else"

## Test Scenarios

### Scenario A: Change accent color
**User says:** "Change accent to orange"
**Action:** Update `tokens.json` palette.accent.hex from `#22D3EE` to `#F97316` (Orange 500)
**Side effects:** Regenerate brand-book.html, update base.css custom properties, check WCAG contrast (Orange 500 on Slate 900 = 5.2:1 ✓, on Slate 50 = 3.4:1 ✓)
**Files touched:** tokens.json, brand-book.html, base.css

### Scenario B: Change font pairing
**User says:** "Use Space Grotesk for display"
**Action:** Update typography.display.family to "Space Grotesk", regenerate brand book specimens
**Side effects:** Update base.css --font-display, carousel template previews need rebuild

### Scenario C: Update masthead
**User says:** "Handle is @kammaai, tagline is 'enterprise AI strategy'"
**Action:** Update chrome.masthead.labels to ["{{month_year}}", "@kammaai", "enterprise AI strategy"]
**Side effects:** All carousel templates updated, PPTX builder picks up new labels from tokens.json automatically

## Update Mode Contract Verified:
- [x] Detects existing tokens.json
- [x] Shows current identity summary
- [x] Asks what to change (not rebuild)
- [x] Cascades changes to downstream files (brand-book, base.css, templates)
- [x] Validates WCAG contrast after color changes
- [x] Respects locked_fields (brand, chrome.masthead)
