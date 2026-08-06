# PPTX QA summary

- Deck status: `draft`
- Slides: 13
- Editability: all diagrams, scorecards, metrics, titles, and body copy are PowerPoint-native editable objects
- PPTX structural validation: passed; package reopens with `python-pptx`
- Deck context and template-profile validation: passed
- Presentation evidence, slide-plan, and visual-spec contracts: passed with file checks
- Design lint: clean; 0 unresolved errors and 0 unresolved warnings after documented waivers
- Bounds and visible-text scan: passed; 0 out-of-bounds shapes and 0 internal workflow terms
- Lightweight rendered contact sheets: inspected; no visible clipping or collisions
- Real Office render: blocked because the installed OfficeCLI wrapper exits 126 (`Exec format error`) and no LibreOffice renderer is available
- Promotion gate: remains `draft` until a real PowerPoint, OfficeCLI, LibreOffice, or Google Slides render is inspected

## Template integrity

The configured host fallback `/home/sheke/.claude/templates/branded-template.pptx` is 1,853,794 NUL bytes and is not a valid ZIP/PPTX package. It was rejected. The valid governed repo-local template at `skills/branded-pptx-deck/resources/template.pptx` supplied the theme/master package.

## Research provenance

The deck uses the completed research run: GBrain recall, You.com native Livecrawl, You.com discovery followed by Exa fresh extraction for Level 2, and primary-company verification. Vendor specifications are labeled as such in the deck.
