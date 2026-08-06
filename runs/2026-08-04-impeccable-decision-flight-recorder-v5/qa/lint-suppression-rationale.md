# Design-lint suppression rationale

The design lint result is clean after governed suppressions; ignored detections are not treated as
nonexistent. They were reviewed against the final real PowerPoint render and retained only where the
rule is a known mismatch with intentional presentation geometry or supplied source evidence.

- `IMAGE_LOW_DPI`: applies to the supplied 640×360 video frames. They are the highest-fidelity
  authentic evidence and appear only on slides 4, 8, and 9 at inspected sizes.
- `TEXT_TOO_SMALL`: applies to evidence labels, folios, matrix labels, and secondary metadata.
  Primary claims and explanations remain presentation scale.
- `TEXT_LOW_CONTRAST`: the static linter does not consistently resolve colored-field backgrounds;
  the real PowerPoint render confirms primary readability.
- `TEXT_OVERFLOW_RISK` and `TEXT_BOX_OVERLAP`: compact analytical labels and intentionally adjacent
  regions render without clipping or collisions in PowerPoint.
- `SLIDE_WORD_COUNT`: dense slides retain only decision logic required for executive review and remain
  legible in the real render.
- `DECK_COLOR_COUNT`: embedded evidence and antialiasing inflate the count; native geometry uses the
  five governed roles specified in `deck-design.json`.

Authority for these suppressions is the final OfficeCLI issue scan plus manual inspection of the real
PowerPoint contact render, not the suppression list alone.
