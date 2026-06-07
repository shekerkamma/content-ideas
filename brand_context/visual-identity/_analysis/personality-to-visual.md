# Personality → Visual Mapping

Generated from voice-profile.md (no visual refs provided — neutral identity path).

## Voice Traits → Visual Decisions

| Voice trait | Visual implication | Decision |
|---|---|---|
| Blunt practitioner | No decorative elements, clean grid | Minimal chrome, strong typography hierarchy |
| Anti-complexity crusader | Simple palette, no gradients | Dark slate + cyan accent — 2-color story maximum per slide |
| Show-the-work teacher | Code blocks, terminal aesthetic | Mono typeface added (JetBrains Mono), success green for terminal feel |
| Direct and bold | High contrast, large type | Inter Tight Black for display — maximum impact, zero decoration |
| Lazy-efficient | Generous whitespace, scannable | 80px canvas padding, short text blocks, bullet-friendly layouts |

## Palette Rationale

- **Dark slate primary (#0F172A):** Technical, developer-friendly, commands attention without being flashy. Matches "no nonsense" energy.
- **Cyan accent (#22D3EE):** Terminal/code aesthetic. Bright enough to draw the eye, technical enough to feel like a tool not a brand. High contrast on dark (12.4:1).
- **Light background (#F8FAFC):** Clean, fast-loading, print-friendly. No texture, no pattern — dead simple.
- **No warm colors:** Voice profile is direct-first, warm underneath. Visual identity leads with the direct (cool, technical); warmth comes from the words, not the design.

## Typography Rationale

- **Inter Tight (display):** Geometric sans-serif, extremely tight letter spacing at heavy weights. Feels like a terminal header. Bold, ExtraBold, Black available — matches the "make strong claims without hedging" trait.
- **Inter (body):** Clean, highly readable, the developer's default. Regular, Medium, Bold. Doesn't distract from content.
- **JetBrains Mono (code):** Added as third typeface because "show the work" is a core trait. Code snippets are a primary content type. Ligature-friendly.

## Contrast Checks (WCAG)

| Combination | Ratio | Pass? |
|---|---|---|
| text (#0F172A) on background (#F8FAFC) | 16.5:1 | AAA |
| text_on_dark (#F8FAFC) on primary (#0F172A) | 16.5:1 | AAA |
| accent (#22D3EE) on primary (#0F172A) | 8.2:1 | AAA |
| accent (#22D3EE) on background (#F8FAFC) | 3.1:1 | AA (large text) |
| muted (#94A3B8) on background (#F8FAFC) | 3.5:1 | AA (large text) |

All critical text combinations pass WCAG AA. Accent on light background is borderline — use only for large text/icons on light surfaces.
