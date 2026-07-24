# Consulting Template Freeze: Brainstorm / Discovery Notes
Date: 2026-06-24 · Goal: Freeze the exact consulting/Genspark template constraints before regenerating the YC agentic AI Reddit validation deck.

## Structured context
- **Topic type**: strategy
- **Topic string**: Freeze a client-ready consulting deck template and Genspark prompt pattern for YC agentic AI market evidence synthesis.
- **Entities**: Genspark AI Slides, Printing Press YC CLI, reddit-new-factcheck, branded PowerPoint template, YC agentic AI companies
- **Prospect/account**: n/a
- **Target buyer**: investor / strategy partner / executive sponsor
- **Verticals**: agentic AI, property management, construction, healthcare, finance/accounting, mortgage, insurance, lending
- **Open decisions**: exact template source and non-negotiable slide design rules -> user confirmation

## Summary / key decisions
- Session opened because the previous Genspark / PPTX attempts drifted from the agreed consulting template.
- The next generation should freeze the saved template constraints before any new Genspark run.

## Q&A log
### Q1 — Template source freeze
- Asked: Confirm whether to freeze on `/home/shekerk/.claude/templates/branded-template.pptx` as the saved branded template, with Genspark instructed to follow top-tier consulting exhibit style.
- Captured: User redirected from template path confirmation to structure review: "how the structure looks like, use grill-me skill to review again." The immediate need is to freeze the consulting deck structure before any Genspark/PPTX generation.
- Flags: exact template path still open -> user; deck structure approval now upstream -> user

### Q2 — Deck structure freeze
- Asked: Approve a proposed 30-slide consulting structure.
- Captured: User rejected it strongly: "It is junk... it is consultingstyle - you have made mess." The structure was too mechanical and did not reflect real consulting market-research slide flow. User explicitly asked to search for what market research slide content looks like from consulting firms and then use grill-me to finalize.
- Flags: Need external reference scan of consulting market-research slide structures before the next proposed outline -> assistant

### Q3 — Research-backed structure reset
- Asked: User asked to search for what market research slide content looks like from consulting firms and use grill-me to finalize.
- Captured: External scan indicates the prior structure was wrong because it centered internal artifacts ("Reddit evidence pack", "YC extraction") instead of a market-research argument. Consulting market research decks generally move answer-first through market definition, segmentation, growth/attractiveness, customer pain/needs, competitive landscape, whitespace/prioritization, proof gaps, and recommended next moves. Relevant observed patterns: McKinsey State of AI opens with key findings and then uses exhibits/methodology to support the answer; McKinsey Technology Trends explains trend selection and evidence vectors; market segmentation/profit-pool literature emphasizes actionable segment selection and attractiveness, not raw source narration.
- Flags: Need user approval on a revised market-research storyline that puts Reddit/YC evidence in the appendix/method layer rather than as the main slide spine -> user

### Q4 — Structure approval
- Asked: Approve the revised 30-slide market-research storyline or shift toward investor-thesis orientation.
- Captured: User approved the revised market-research deck structure and said "go ahead." Frozen structure: executive answer -> market definition -> segment attractiveness -> customer pain/evidence -> competitive/white-space view -> recommendations/appendix. Reddit/YC evidence is support, not the story spine.
- Flags: none for structure; proceed to Genspark generation using frozen structure and consulting-template constraints.

### Q5 — Missing differentiation layer
- Asked: User reviewed the generated storyboard direction and said it is still incomplete: "what makes them unique, I mean what business problems they are addressing differently? The story board does not look good at all."
- Captured: The approved structure is insufficient because it explains evidence status and market segments, but does not explain company-level uniqueness or the distinct business problem each startup addresses. The next storyboard must add a differentiation layer: problem anatomy, why the legacy workflow breaks, what each company does differently, and why that wedge might win. The deck should not simply say "property management" or "construction"; it should explain the specific business problem and distinctive approach.
- Flags: Revise storyboard around differentiated business problems and uniqueness before regenerating -> assistant

### Q6 — Scope reset to one company
- Asked: User rejected the expanding storyboard and clarified: "We are talking about market research for one specific company no, reddit, no bullshit stories."
- Captured: The correct scope is one specific company market research deck. Exclude Reddit validation as a story spine. Exclude YC-list comparison. Exclude broad agentic AI thesis. The deck should research one company's market, customer problem, buyers, alternatives, competitive landscape, positioning, risks, and diligence questions.
- Flags: Need user to confirm the one company to research -> user

### Q7 — Deck style constraint
- Asked: Confirm company scope and deck type.
- Captured: User emphasized the output should use the grill-me process and be a consulting-style slide deck. Hard constraint: the deliverable is a consulting kind of slide deck, not a generic narrative, Reddit validation deck, or source-dump deck.
- Flags: Single company target remains unconfirmed -> user

## Open flags (pending input)
- Confirm exact template source and whether Genspark should generate against that style directly or only synthesize copy for branded PPTX rendering -> user
- Approve or revise the consulting deck structure before generation -> user
- Replace rejected deck structure with a research-backed consulting market-research structure -> assistant
- Approve revised market-research storyline: market definition -> segmentation -> attractiveness -> competitive/white-space -> evidence validation -> recommendations -> user
- Add company uniqueness / business-problem differentiation lens to frozen storyboard -> assistant
- Confirm single company target for market research -> user
