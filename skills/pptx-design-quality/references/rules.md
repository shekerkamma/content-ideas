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

## Motion rules (`lint_motion.py`)

These fire only when `deck-design.json` declares a `motion` block. Without one the
motion linter reports nothing, so decks that predate the contract are unaffected.

| Rule ID | Severity | Meaning |
|---|---|---|
| `MOTION_EXIT_BREAKS_REST_STATE` | error | A slide carries exit animations, so its resting frame is missing content that PDF export, contact sheets, and Office render QA all inspect |
| `MOTION_TRANSITION_OFF_CONTRACT` | warning | A slide transition is outside `motion.allowed_transitions` |
| `MOTION_TRANSITION_TOO_LONG` | warning | A transition exceeds `motion.max_transition_ms` |
| `MOTION_TRANSITION_MISSING` | warning | `motion.require_transition` is set but the slide declares none |
| `MOTION_EFFECT_CLASS_OFF_CONTRACT` | warning | A slide uses an animation class outside `motion.allowed_effect_classes` |
| `MOTION_BUILD_TOO_LONG` | warning | A slide exceeds `motion.max_build_steps_per_slide` |

`MOTION_EXIT_BREAKS_REST_STATE` is the rule that keeps animation compatible with the
existing delivery gate: every other QA surface reads a resting frame, so a deck whose
meaning depends on mid-animation state is unreviewable. Permit exits deliberately by
adding `"exit"` to `motion.allowed_effect_classes` — not by waiving the rule, which is
an error and therefore not waivable.

The linter suppresses native-title and layout-repetition checks when
`deck.output_mode` is `image-per-slide`; the authored HTML route owns those checks.

Waive a false positive only by adding the exact rule ID to `qa.ignore_rules` and a
non-empty explanation under the matching `qa.waivers` key in `deck-design.json`.
