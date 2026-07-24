# research-to-deck run log
date: 2026-06-19
topic: Claude AI Workflow Use Cases in Healthcare
style: neon (Aurora Glass)
kb: /home/shekerk/test-kb

## Stage results
- Stage 1 Research:  ✓ claude-workflows-healthcare-use-cases-research.md (~1,100 words, 8 sources)
- Stage 2 Compile:   ✓ compiled to /home/shekerk/test-kb (openkb add — LiteLLM logging TimeoutError was benign/non-blocking)
- Stage 3 Synthesis: ✓ claude-workflows-healthcare-use-cases-synthesis.md (5 questions answered)
- Stage 4 Deck:      ✓ 14 slides, style=neon — via /openkb-deck-neon skill
- Stage 5 QA:        ✓ no patches needed — deck passed all checklist items clean
- Stage 6 PPTX:      skipped (--pptx flag not set)

## Deliverables
- Research brief: runs/2026-06-19-claude-workflows-healthcare-use-cases-research-deck/claude-workflows-healthcare-use-cases-research.md
- Synthesis:      runs/2026-06-19-claude-workflows-healthcare-use-cases-research-deck/claude-workflows-healthcare-use-cases-synthesis.md
- Deck (draft):   runs/2026-06-19-claude-workflows-healthcare-use-cases-research-deck/claude-workflows-healthcare-use-cases-deck-draft.html
- Deck (final):   runs/2026-06-19-claude-workflows-healthcare-use-cases-research-deck/claude-workflows-healthcare-use-cases-deck.html
- KB output:      /home/shekerk/test-kb/output/decks/claude-workflows-healthcare-use-cases/index.html

## Slide sequence
1.  cover    — "Claude in Healthcare: From Admin Burden to Clinical Intelligence"
2.  thesis   — Physicians spend more time on paperwork than patients
3.  data     — $262B in denied/underpaid claims annually
4.  chapter  — 01: Provider Workflows
5.  compare  — Clinical Documentation vs Prior Authorization
6.  thesis   — Poor discharge summaries cost $26B in preventable readmissions
7.  chapter  — 02: Payer Workflows
8.  compare  — Medical Coding vs Denial Management & Appeals
9.  chapter  — 03: Life Sciences Workflows
10. compare  — Clinical Trial Eligibility vs Pharmacovigilance
11. data     — $10–30M per NDA/BLA submission · Claude compresses by 30–50%
12. compare  — Compliance framework (HIPAA BAA / CMS-9115-F / FDA / ONC / ICH)
13. quote    — "The organizations that move from L2 to L3 now..."
14. closing  — "Build for L3. The mandate clock is ticking."

## Research coverage
- 3 market segments: Providers, Payers, Life Sciences
- 10 use cases: PA automation, ambient scribing, discharge summaries, care navigation, medical coding, denial management, trial screening, pharmacovigilance, report structuring, regulatory submissions
- 5 compliance frameworks: HIPAA BAA, CMS-9115-F, CMS Info Blocking, FDA AI/ML 2024, ONC CDS rules
- Key ROI figures: $37K/physician/year (PA), $75K–$110K/year (clinical docs), $262B (coding errors), $26B (readmissions), $10–30M per NDA

## QA notes
- CSS specificity: clean — no slide modifier classes conflict with display property
- Self-containment: clean — no external links, fonts, or images
- Navigation: ← → arrow keys + click + F fullscreen + P print
- Slide type sequence: no run of 3+ same type
- LiteLLM TimeoutError during Stage 2 compile is a known benign side-effect of openkb logging; [OK] confirmation was received
