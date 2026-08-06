# QA summary

- **Deck status:** draft
- **PPTX structural validation:** passed (12 slides)
- **Deck context:** passed
- **Template profile:** passed
- **Presentation contracts:** passed with file checks
- **Claim/evidence scan:** clean
- **Design lint:** clean after documented waivers; 0 unresolved errors and 0 unresolved warnings
- **Lightweight contact-sheet inspection:** passed after shortening overflowing action titles
- **Embedded screenshot presence:** confirmed in the PPTX package
- **Real Office render:** unavailable on this host
- **Promotion gate:** blocked until the draft is rendered in PowerPoint, LibreOffice, Google Slides, or OfficeCLI and the embedded evidence crops are inspected

## Template integrity finding

The documented host fallback `/home/sheke/.claude/templates/branded-template.pptx` exists as a 1,853,794-byte file but starts with NUL bytes and is not a valid ZIP/PPTX package. It was rejected. The valid repo-local branded workflow template at `skills/branded-pptx-deck/resources/template.pptx` was profiled and used as the delivery authority.

## Waiver rationale

Small text is confined to editorial labels, source captions, and footers; low-contrast teal is confined to secondary labels; the authentic 640×360 evidence source is below the configured 120-DPI target at its placed size; the editable nine-check scorecard intentionally exceeds the generic shape-count threshold. All remain subject to the missing real-render gate.
