# Product Vision — DealForge

## Vision & Mission

**Vision:** Every AI consultant walks into every meeting fully prepared — not because they spent hours prepping, but because their tools did.

**Mission:** Automate the 4-8 hours of manual pre-sales work that AI consultants do for every deal, delivering a complete, high-quality deal-prep package in under 5 minutes.

**Founder's Why:** Built this pipeline for himself over months of real enterprise consulting. Watched the same 4-hour prep cycle repeat for every prospect. Turned it into battle-tested skills. Now packaging it so other consultants don't have to build it from scratch.

**Core Values:**
- **Output speaks for itself** — Quality is measured by whether the consultant uses the output in the meeting, not by feature count
- **Depth over breadth** — A 5-stage pipeline that does one workflow exceptionally well, not a platform that does 20 things generically
- **Honest about limitations** — If the data isn't good enough for a prospect, say so instead of generating confident-sounding garbage
- **Consultant-grade, not template-grade** — Every output should look like a senior consultant produced it, not like a template with names swapped in

---

## User Research

### Primary Persona — "The Solo AI Strategist"

**Name:** Alex  
**Role:** Independent AI strategy consultant  
**Experience:** 3 years in AI consulting after 5+ years in data science/ML engineering  
**Revenue:** $30K-$60K per engagement, 1-2 deals/month  
**Context:** Left a corporate ML role to start consulting. Technically excellent — can architect and build AI systems. But pre-sales is a second job: every prospect requires hours of research, deck building, and objection preparation. Billing rate is $250-$400/hr, so every hour of unbillable prep directly reduces effective income.

**Daily workflow:**
1. Get intro to prospect (LinkedIn DM, referral, inbound from content)
2. Research company: website, LinkedIn, Crunchbase, recent news, AI signals
3. Draft strategy brief: what AI opportunities exist for this company
4. Build deck: 10-15 slides, branded, with use-case details and pricing
5. Prep objections: what will they push back on? pricing, timeline, risk, internal capabilities
6. Walk into meeting

Steps 2-5 take 4-8 hours per prospect. Alex does this 2-3 times per week.

### Secondary Personas

1. **BD Lead at a small AI firm** — Does deal prep for a team of 3-5 consultants. Same pain, multiplied by team size. Would value template consistency across consultants.
2. **Enterprise solution architect** — At a systems integrator (Accenture, Deloitte, Wipro). Preps AI proposals for specific clients but has less flexibility — needs to work within corporate templates and approval processes.
3. **ML engineer transitioning to consulting** — Technically strong but lacks pre-sales structure. Doesn't know what a "good" deal-prep package looks like. Needs the framework as much as the automation.

### Jobs to Be Done

- **When** I get an intro to a new prospect, **I want to** quickly understand their business context and AI readiness **so that** I can have an informed first conversation instead of asking basic questions.
- **When** I'm preparing for a strategy presentation, **I want to** generate a polished, branded deck with industry-specific content **so that** I look prepared and credible without spending half a day on slides.
- **When** I'm anticipating pushback, **I want to** have pre-built responses to common objections **so that** I don't freeze or improvise poorly in the meeting.

### Pain Points

1. **Time sink is unbillable:** 12-24 hrs/week of prep that can't be billed. At $300/hr, that's $3,600-$7,200/week of lost revenue.
2. **Quality vs. speed tradeoff:** Cutting corners on prep (generic deck, shallow research) directly reduces close rate.
3. **No workflow integration:** Research in one tool, briefs in another, decks in another, objection prep in their head. No single flow.
4. **Generic AI outputs:** Using ChatGPT to draft slides produces output that "sounds AI" — prospects notice, credibility drops.

### Current Alternatives

| Alternative | Strengths | Weaknesses |
|---|---|---|
| Manual process (Google + blank deck) | Full control, personal touch | 4-8 hours per deal, doesn't scale |
| ChatGPT/Claude for drafting | Fast for individual sections | Generic, no pipeline, no branding, no quality gate |
| Pitch deck tools (Beautiful.ai, Gamma) | Pretty slides fast | No research, no strategy, no objection prep |
| CRM enrichment (Clay, Apollo) | Good prospect data | Data only — no strategy, no deliverables |
| Hiring a VA/researcher | Delegated | Expensive, training overhead, quality inconsistent |

### Key Assumptions to Validate

1. Consultants will pay $300/month for this (not build their own)
2. Output quality is high enough to use with <15 min editing
3. Sufficient public data exists for mid-market prospect research

### User Journey Map

```
Awareness → Trial → First Use → Habit → Advocate
   |           |         |          |         |
LinkedIn    Free      First      Weekly     Refers
post      concierge  real deal   pipeline   peers
           run       package     runs
```

---

## Product Strategy

### Product Principles

1. **One input, complete output.** A company name should be enough to generate a full package.
2. **Editable, not locked.** Every output is a standard format (.pptx, .md, .pdf) the consultant owns and can edit.
3. **Quality gate at every stage.** Each pipeline stage validates its output before the next stage runs.
4. **Transparent when uncertain.** If prospect data is thin, say so — don't hallucinate confidence.

### Market Differentiation

Not "AI slides" — a **5-stage consulting-grade pipeline** that connects prospect research to industry strategy to branded deliverables to objection prep in one flow. The output quality bar is "looks like a senior consultant spent 4 hours on this."

### Magic Moment

Type a company name. 90 seconds later, open a branded deck that looks like you spent hours on it — with the prospect's industry challenges, a tailored AI strategy, and talking points you'd actually use.

**This must be achievable in the MVP.**

### MVP Definition

**In scope:**
- [ ] Prospect name input → account research
- [ ] Strategy brief generation (1-page AI opportunity brief)
- [ ] Branded deck generation (10-12 slides, editable .pptx)
- [ ] Objection script generation (top 5 objections + responses)
- [ ] Download package (zip: briefing + deck + objection doc)

**Explicitly out of scope (v1):**
- CRM integration
- Team/org features
- Template customization
- Analytics/tracking
- Meeting scheduling
- Follow-up automation
- Mobile app

### Feature Priority (MoSCoW)

| Priority | Feature |
|---|---|
| **Must** | Account research pipeline, strategy brief gen, deck gen, objection scripts, download |
| **Should** | Custom branding upload, industry vertical selection, prospect history |
| **Could** | Discovery agenda gen, competitive battle card, pricing calculator |
| **Won't (v1)** | CRM sync, team features, template editor, meeting recording analysis |

### Core User Flows

1. **New Deal Prep:** Enter prospect name → pipeline runs → review outputs → download package → edit deck → walk into meeting
2. **Re-run with edits:** Select previous prospect → modify inputs (add context, change vertical) → re-generate → download updated package
3. **Template setup (once):** Upload brand assets (logo, colors) → set default pricing tiers → save as profile

### Success Metrics

| Metric | Target (90 days) | Target (6 months) |
|---|---|---|
| Paying customers | 5 | 50 |
| MRR | $1,500 | $15,000 |
| Output usage rate | >70% of packages used in actual meetings | >80% |
| Time saved per deal | >3 hours | >3.5 hours |
| NPS | >40 | >50 |

### Risks

| Risk | Mitigation |
|---|---|
| Output feels "AI-generated" | Quality gates + industry-specific prompts + branded templates |
| Prospect data too thin for mid-market | Graceful degradation: flag thin data, offer manual enrichment |
| Target users build their own | Move faster on UX/convenience; depth of pipeline is the moat |
| Solo founder bandwidth | Start concierge (no code); automate only what's validated |

---

## Brand Strategy

### Positioning Statement

For AI consultants who sell $20K-$100K engagements, **DealForge** is the pre-sales copilot that turns a prospect name into a complete deal-prep package in minutes. Unlike generic AI writing tools, DealForge runs a 5-stage consulting-grade pipeline that delivers industry-specific strategy, branded decks, and objection scripts — the same depth a senior consultant would apply manually.

### Brand Personality

**Archetype:** The Master Craftsman  
Competent, direct, quietly confident. Like a senior partner who prepares flawlessly but doesn't brag about it. Professional without being corporate.

### Voice & Tone Guide

| DO | DON'T |
|---|---|
| "Your deal package is ready" | "We've leveraged AI to optimize your workflow" |
| "Data was thin for this prospect — flagged sections need your input" | "Our cutting-edge algorithms have generated insights" |
| "This deck is yours to edit — it's a .pptx, not a locked PDF" | "Experience the power of AI-generated presentations" |
| Use numbers: "saves 4 hours per deal" | Use vague claims: "dramatically improve efficiency" |

### Messaging Framework

**Headline:** Stop prepping. Start closing.  
**Subhead:** DealForge turns a prospect name into a complete deal-prep package — account briefing, strategy deck, objection scripts — in 90 seconds.  
**Proof point:** Built by a consultant who got tired of spending more time prepping than meeting.

### Elevator Pitches

**5 seconds:** "DealForge automates the 4-hour pre-sales prep that AI consultants do for every deal."

**30 seconds:** "AI consultants spend 4-8 hours prepping for every sales meeting — researching the prospect, writing strategy briefs, building decks, and preparing for objections. DealForge does all of that in 90 seconds. Enter a company name, get a complete deal-prep package: account briefing, branded deck, and objection scripts. It's the pipeline I built for my own consulting practice, now available to every AI consultant."

**2 minutes:** "Every AI consultant I know has the same problem: the meeting is 60 minutes, but the prep takes 4-8 hours. You research the company, write a strategy brief, build a deck, think through objections, and by the time you're ready, half your day is gone — and none of that time is billable. I built DealForge because I was doing this 3 times a week and realized I'd automated the whole pipeline with Claude Code skills over 6 months of real client work. Now it's a product: enter a prospect name, and 90 seconds later you have a complete package — an account briefing grounded in real company data, a branded deck with industry-specific AI strategy and use-case slides, and objection scripts with coaching notes. The output looks like a senior consultant spent 4 hours on it. You review it in 15 minutes, make your edits, and walk into the meeting prepared. My early users are saving 3-4 hours per deal. At $300/hour billing rates, that's $900-$1,200 of recovered revenue per prospect."

### Competitive Differentiation Narrative

"Most AI tools help you write faster. DealForge helps you **sell** faster. The difference is pipeline depth: we don't just generate slides — we research the prospect, map their industry challenges to AI opportunities, structure a strategy, render it into a branded deck with the polish of a Big 4 deliverable, and prep you for the pushback. That's 5 stages with quality gates, not a prompt that says 'make me a sales deck.'"

---

*For visual design (colors, typography, spacing, components, motion), see `docs/design.md`. If it doesn't exist, run `/plaid design` with image references.*
