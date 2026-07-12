# Agentic-AI Governance Market Deck

Status: `reviewed` for hybrid-editable PPTX.

## Source

- User-provided market brief: Agentic-AI Governance Market: Map and Position
- Build skill: `skills/genspark-branded-deck`

## Outputs

- Reviewed hybrid-editable PPTX: `build/agentic-ai-governance-market-hybrid-editable-reviewed.pptx`
- Desktop copy: `/mnt/c/Users/sheke/OneDrive/Desktop/agentic-ai-governance-market-hybrid-editable-reviewed.pptx`
- Image-based reviewed fallback: `build/agentic-ai-governance-market-image-reviewed.pptx`
- Source HTML: `deck.html`
- Theme: `theme.css`
- Rendered PNGs: `build/png/`
- QA contact sheets: `qa/contact-01.png`, `qa/contact-02.png`

## Deck Structure

1. Thesis: Do not sell governance software; operate governed agents
2. Answer: enter, but avoid the software trap
3. Market clusters: five competitive lanes
4. Platform gravity: governance bundled toward zero
5. Money vs. noise: software vs. operations
6. Execution gap: adoption vs. governance maturity
7. Whitespace: cross-runtime OT-adjacent governance
8. Offer design: Governed Agent Operations
9. Buyer shift: sell to risk and operations owners
10. Counterargument: neutral-control-plane story may be gone
11. Cheapest experiment: 90-day paid-pilot test
12. Decision rule: IP or collateral
13. Evidence base

## QA

- HTML rendered to 13 PNG slides at 2560x1440.
- Contact sheets reviewed: no obvious clipping, title/body collisions, or broken slide renders.
- PPTX package validation: both PPTX files open with `python-pptx` and contain 13 slides.
- Visible text scan passed for internal tool names, file paths, and production terms.
- Hybrid-editable render check completed through LibreOffice PDF export and PyMuPDF contact sheets.
- Hybrid extractor was adjusted to avoid duplicate slide-number spans and to respect source-list bullet gutters.

## Editability

- Reviewed deliverable: `hybrid-editable`, with native PowerPoint text boxes over rendered design backgrounds.
- Caveat: visual panels and complex diagram shapes are rendered backgrounds; slide text is editable.
