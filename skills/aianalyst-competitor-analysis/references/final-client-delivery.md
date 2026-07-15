# Final Client Delivery Contract

Use this after the evidence ledger, story-architect pack, artifact traceability, and quality gates are ready. This is the final packaging contract for AI Analyst competitor-analysis runs.

## Required Final Artifacts

A complete client-ready run must include both:

1. **Branded PPTX deck**
   - recreated through `genspark-branded-deck` from validated content and the final slide spine
   - built from owned `deck.html`, `theme.css`, and `deck.css`
   - rendered to PPTX as editable slides: use `genspark-branded-deck` hybrid-editable output at minimum, or `branded-pptx-deck` for fully native editable PowerPoint shapes/charts
   - image-only PPTX exports are draft/reference artifacts only, not final delivery
   - all visible numbers come from upstream AI Analyst dataset artifacts and carry the required source/caveat label
   - QA'd through contact sheets and OfficeCLI or an explicitly documented equivalent

2. **Self-contained HTML artifact**
   - saved at `client-package/site/index.html`
   - publishable without a backend
   - contains the same executive answer, evidence-backed storyline, competitor matrix, proof gaps, and next actions as the deck
   - includes inline or local CSS/JS/assets so it can be copied to GitHub Pages as a static artifact
   - validated with browser/Playwright checks before publishing

The deck alone is not final delivery. The HTML page alone is not final delivery unless the user explicitly cancels PPTX.

## Slide Tool Chain

Use the slide tools in this order when hosted Genspark is part of the workflow:

1. `genspark-slides`
   - use for hosted Genspark AI Slides generation, expansion, and editable viewer/project creation
   - recover/capture the generated slides
   - use recovered output as a content/design reference, not as the final package by itself

2. Evidence cleanup
   - scan recovered text for unsupported datapoints
   - plug supported numbers into the final content
   - remove unsupported numbers
   - record cleanup in QA notes or delivery manifest

3. `genspark-branded-deck`
   - recreate the final deck from validated content in owned HTML/CSS
   - use the repo template and brand tokens
   - render contact sheets
   - build PPTX using the hybrid-editable path for final delivery
   - run final PPTX QA

Do not stop at a Genspark AI Slides URL, recovered HTML, or image export when the requested delivery is a client-ready final package.

## Branded Deck Requirements

The `client-package/genspark-deck/` folder or equivalent must include:

```text
client-package/genspark-deck/
├── deck.html
├── theme.css
├── deck.css
├── build/
│   ├── png/
│   ├── qa/
│   └── <name>-draft.pptx
└── qa/
```

Rules:

- `deck.html` is the source-editable slide document.
- final slide titles must be assertion titles from the story-architect pack
- every visible quantitative claim must be from the allowed-number list
- allowed numbers must trace to upstream AI Analyst artifacts: `evidence-ledger.csv`, `metric-definitions.md`, `data-quality-report.md`, `scoring-model.md`, `competitor-brief.md`, or `story-architect-pack.md`
- no unsupported Genspark-generated datapoints may be carried into `deck.html`
- no internal tool/process labels should appear on client slides unless the user asks for an audit appendix
- final PPTX must be editable; if hybrid-editable path is used, declare that text is editable but complex visual shapes may remain rendered backgrounds
- if the user needs fully editable/re-layoutable shapes and charts, rebuild with `branded-pptx-deck` rather than shipping image-only slides

## Self-Contained HTML Requirements

The HTML artifact must be a real standalone report, not a slide screenshot dump.

Minimum sections:

- executive answer / BLUF
- competitor arena map
- evidence coverage and confidence
- threat matrix or scorecard
- target differentiation
- incumbent compression risk
- proof gaps
- recommended moves / 30-60-90 roadmap
- references or source notes

Implementation requirements:

- one `index.html` can carry inline CSS/JS, or reference only local files copied into the same site folder
- no external build step required after publication
- no broken external assets
- no private file paths
- no API keys or credentials
- tables and charts must be readable on desktop and mobile
- tabs/filters/interactive sections must work after static publication

## GitHub Pages Publishing

When the user asks for a shareable URL, team URL, public URL, GitHub Pages, or final client delivery that includes a URL:

1. Copy or maintain the self-contained HTML artifact at `client-package/pages/<slug>/index.html`.
2. Use the `github-pages-publisher` skill or run `scripts/publish-static-page.sh --source <path> --slug <slug>`.
3. Let the publisher detect whether the repo uses legacy `gh-pages` or Actions Pages; do not guess from a feature-branch workflow file.
4. Verify the live URL with a cache-busting query string.
5. Save the public URL and commit SHA in `client-package/delivery-manifest.json`.

If publication is blocked, keep the HTML local path ready and mark URL status `blocked` with the exact reason.

## Delivery Manifest Additions

The manifest must include:

- branded deck source path: `client-package/genspark-deck/deck.html`
- branded deck PPTX path and slide count
- branded deck editability: `hybrid_editable` or `native_powerpoint`
- self-contained HTML local path
- GitHub Pages publish source path
- public URL and verification status when requested
- hosted Genspark project URL when used upstream
- whether hosted Genspark, branded deck, and HTML are in sync

## Final Status Rule

Use `reviewed` only when:

- evidence gates pass
- story-architect pack is locked
- branded deck has been recreated through `genspark-branded-deck`
- final PPTX is editable, not image-only
- visible deck numbers trace to upstream AI Analyst dataset artifacts
- deck contact-sheet QA passes
- PPTX QA passes or an accepted equivalent is documented
- self-contained HTML validates locally
- GitHub Pages URL is verified when requested

Otherwise use `draft` or `blocked`.
