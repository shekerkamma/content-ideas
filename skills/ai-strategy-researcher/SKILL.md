---
name: ai-strategy-researcher
preamble-tier: 3
version: 1.0.0
description: |
  Research and generate comprehensive AI business strategy reports as Word documents.
  Covers market signals, VC theses, vertical analysis, competitive landscape, unit economics,
  and operational playbooks. Use when asked for "AI strategy", "market intelligence",
  "strategy document", or "business planning". Proactively suggest when the user discusses
  AI market positioning or competitive analysis. (gstack)
argument-hint: "[topic or vertical -- e.g., 'AI-native insurance brokerage', 'enterprise AI deployment']"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - Agent
  - AskUserQuestion
---

# AI Strategy Researcher

Research AI market signals and generate comprehensive business strategy documents as Word (.docx) files.

## Task

Given a topic, vertical, or strategic question, conduct deep research across multiple sources and produce a professional Word document with full references.

## Research Framework

Execute research in this order, running parallel searches where possible:

### Phase 1: Market Signals (parallel searches)
1. **VC Theses** -- Search for latest investment theses from Sequoia, Emergence Capital, a16z, Bessemer, Y Combinator related to the topic
2. **Major Moves** -- Search for recent fundraises, acquisitions, JVs, and strategic partnerships (OpenAI, Anthropic, Google, Microsoft)
3. **Market Sizing** -- Search for TAM/SAM estimates from analyst reports, investor decks, and industry publications

### Phase 2: Competitive Intelligence (parallel searches)
4. **Proof Points** -- Search for companies already winning in the space (ARR, valuation, growth metrics)
5. **Competitive Landscape** -- Map incumbents, startups, and model providers entering the space
6. **Failure Analysis** -- Search for companies that failed or pivoted, and why

### Phase 3: Operational Intelligence (parallel searches)
7. **Unit Economics** -- Gross margins, revenue per employee, pricing models, COGS structure
8. **Go-to-Market** -- How successful companies acquired customers, partnership strategies
9. **Playbooks** -- Operational frameworks from VCs and successful founders

### Phase 4: Framework Application
10. Apply Sequoia's **Copilot vs. Autopilot** framework to the topic
11. Apply Emergence Capital's **Intelligence vs. Judgement** framework to identify AI readiness
12. Identify the **Mirage PMF** risk specific to this vertical/topic
13. Define a **North Star Metric** appropriate to the vertical

## Key Sources to Check

Always search these authoritative sources:

| Source | What to look for |
|--------|-----------------|
| Sequoia Capital blog | "Services: The New Software" thesis, vertical analysis |
| Emergence Capital | AI-Native Services Playbook, portfolio companies |
| Y Combinator | Request for Startups, batch companies in the space |
| Bessemer Venture Partners | Cloud/AI indices, pricing playbooks |
| a16z | Market maps, industry analyses |
| OpenAI blog | Deployment Company updates, Frontier Alliances |
| Anthropic blog | Enterprise JV updates, partner announcements |
| TechCrunch | Funding rounds, startup coverage |
| Fortune | Executive interviews, strategic analysis |
| Bloomberg | Financial data, deal structures |

## Document Generation

After research is complete, generate a Word document using `python-docx`:

### Required Sections
1. **Cover Page** -- Title, subtitle, date, source attribution
2. **Table of Contents** -- All sections and subsections
3. **Executive Summary** -- 5 key findings with market signals
4. **Market Signal Analysis** -- What just happened and why it matters
5. **Macro Thesis** -- VC frameworks applied to the topic
6. **Market Sizing & Vertical Analysis** -- TAM with tables
7. **Proof Points** -- Companies already winning with metrics
8. **Operational Playbook** -- How to build/execute
9. **Unit Economics** -- Margins, pricing, key metrics
10. **Competitive Moats** -- Defensibility framework
11. **Risk Analysis** -- Mirage PMF and failure modes
12. **Strategic Framework** -- Decision matrix for the user
13. **Competitive Landscape** -- Positioning map
14. **References & Sources** -- ALL URLs organized by category

### Document Standards
- Use `Calibri` font, `Pt(11)` body, colored headings
- Professional tables using `Light Grid Accent 1` style
- Block quotes for key insights (italic, indented)
- Bullet points with bold prefixes for scanability
- All references include source name, article title, URL, and date
- Minimum 30 referenced URLs across categories

### File Output
- Save to project root as: `{topic-slug}-strategy-{month}{year}.docx`
- Example: `ai-native-insurance-strategy-may2026.docx`
- Clean up the Python generator script after document creation

## Python Dependencies

The document generator requires `python-docx`. Install if needed:
```bash
pip install python-docx
```

## Quality Checklist

Before delivering the document, verify:
- [ ] All 13 sections present
- [ ] 15+ formatted tables with data
- [ ] 30+ referenced URLs with source attribution
- [ ] Copilot vs. Autopilot framework applied
- [ ] Intelligence vs. Judgement analysis included
- [ ] Mirage PMF risks identified
- [ ] North star metric defined
- [ ] Cover page with date and source attribution
- [ ] Professional formatting throughout

## Notes

- Always run parallel WebSearch calls where possible to minimize research time
- Prefer primary sources (VC blogs, company announcements) over news aggregators
- Include both successful and failed companies for balanced analysis
- Convert all relative dates to absolute dates in the document
- The document should be investor-ready and presentable to stakeholders
