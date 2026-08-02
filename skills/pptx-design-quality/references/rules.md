# Native PPTX lint rules

| Rule ID | Severity | Meaning |
|---|---|---|
| `DECK_NO_SLIDES` | error | Presentation contains no slides |
| `DECK_ASPECT_RATIO` | error | Slide dimensions do not match the declared output ratio |
| `SLIDE_EMPTY` | error | A slide contains no visible or editable objects (a picture set as the slide background fill counts as content — e.g. Marp's `image-per-slide` export) |
| `SHAPE_OUT_OF_BOUNDS` | error | A shape extends beyond the slide canvas |
| `TEXT_BOX_OVERLAP` | error | Two non-empty text boxes overlap materially |
| `SLIDE_MISSING_TITLE` | warning | No title-like text appears in the upper slide region |
| `TEXT_OVERFLOW_RISK` | warning | Text density is unlikely to fit its box at the declared size |
| `TEXT_TOO_SMALL` | warning | Non-title text falls below the configured body/caption minimum |
| `TEXT_LOW_CONTRAST` | warning | Resolved text and available background colors miss the configured ratio |
| `IMAGE_LOW_DPI` | warning | Effective placed-image resolution is below the configured DPI |
| `SLIDE_WORD_COUNT` | warning | A slide exceeds the configured word budget |
| `SLIDE_SHAPE_COUNT` | warning | A slide exceeds the configured object budget |
| `DECK_FONT_COUNT` | warning | Resolved font-family count exceeds the configured maximum |
| `DECK_COLOR_COUNT` | warning | Resolved text and explicit fill color count exceeds the configured maximum |
| `LAYOUT_REPETITION` | warning | The same normalized shape layout repeats too many times |

The linter suppresses native-title and layout-repetition checks when
`deck.output_mode` is `image-per-slide`; the authored HTML route owns those checks.

Waive a false positive only by adding the exact rule ID to `qa.ignore_rules` and a
non-empty explanation under the matching `qa.waivers` key in `deck-design.json`.
