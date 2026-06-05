# Validation Report — Pre-Sales Copilot

_Generated: 2026-06-05_

## Verdict
**Strong**

The pain is real, frequent, and expensive. The founder has an unfair advantage that would take a competitor months to replicate — a working, battle-tested skill chain used on live enterprise deals. The main risk is differentiation: the AI pre-sales tooling space is heating up fast, and the window to establish a brand before larger players (Clay, Gong AI, generic GPT wrappers) crowd in is 6-12 months. Proceed to Plan, but validate willingness-to-pay with 5 real consultants before writing code.

## Scorecard
| Area | Score | Read |
|---|---:|---|
| Pain intensity | 5/5 | 4-8 hours per deal, 3 deals/week = 12-24 hours of unbillable pre-sales work. Consultants feel this acutely. |
| Buyer clarity | 4/5 | Solo AI consultants selling $20K-$100K engagements. Clear persona, but "AI consultant" is a broad label — may need to narrow to a vertical (manufacturing, fintech, healthcare). |
| Urgency | 4/5 | Every week without the tool is another 12-24 hours of manual prep. But consultants are used to the pain — urgency comes from competitive pressure (the consultant who preps better wins the deal), not crisis. |
| Differentiation | 3/5 | The depth of the chain (6-skill pipeline with quality gates) is genuinely hard to replicate. But from the outside, "AI generates my sales deck" sounds like what 50 other tools claim. The differentiation is real but hard to communicate in a headline. |
| Speed to validate | 5/5 | The skills exist. A concierge version (founder runs the pipeline manually for 5 clients) can launch this week. No code to write for v0. |
| Founder advantage | 5/5 | Built the pipeline, uses it daily, has enterprise client relationships proving it works. This is the strongest axis. |

## Core Assumption
AI consultants selling $20K-$100K enterprise engagements will pay $200-$500/month for a tool that cuts deal-prep time from 4-8 hours to 30 minutes, if the output quality is high enough to use with minimal editing.

## Fatal Flaws
| Risk | Severity | Why It Matters | Fast Test |
|---|---|---|---|
| Output quality perception | High | If the generated deck or brief feels "AI-generated" to the prospect, it damages the consultant's credibility — worse than no tool at all. The bar is "looks like I spent hours on this," not "looks AI-generated." | Run the pipeline for 3 real prospects. Show the output to 2 consultants cold. Ask: "Would you present this as-is, edit it, or trash it?" If >50% say trash, the quality bar isn't met. |
| Willingness to pay vs. DIY | Medium | Power users (the target audience) are exactly the people most likely to build their own version with Claude Code skills. If the target user can replicate 80% of the value in a weekend, the product has no moat beyond convenience. | Ask 5 AI consultants: "How do you prep for enterprise sales calls today?" and "Would you pay $300/month for [description]?" Listen for enthusiasm vs. polite interest. Polite interest = vitamin. |
| Data accessibility for research | Medium | Account briefings depend on publicly available company data. For large enterprises (Hyundai, BMW) this is fine. For mid-market prospects (Series B SaaS companies, regional manufacturers), public data may be too thin to generate useful research. | Run the account-briefing skill against 10 mid-market companies. Score each output 1-5 on "useful without manual supplementation." If median < 3, the research stage needs a data enrichment source. |

## Problem Reality
- **Pain:** "I spend more time prepping for the meeting than I do in the meeting. By the time I've researched the company, written a deck, thought through objections, and rehearsed my positioning, I've burned half a day — and I have two more prospects to prep for this week." Frequency: 3x/week. Cost: 12-24 hours/week of unbillable time. Intensity: high (directly impacts close rate and revenue).
- **Early adopter:** A solo AI consultant with 2-5 years of experience, selling AI strategy/pilot engagements to mid-market companies ($50M-$500M revenue). They use Claude Code or similar tools for coding but still do pre-sales manually. They're active on LinkedIn, probably follow AI influencers, and have a small network of similar consultants they share war stories with. They close 1-2 deals/month at $30K-$60K average.
- **Vitamin or painkiller:** Painkiller. The pain is real, frequent, and directly tied to revenue. But there's a nuance: the "minimal editing" promise is what makes it a painkiller vs. a vitamin. If the output requires 2 hours of rework, it's a vitamin (saves 2-6 hours instead of 4-8). If it requires 15 minutes of review, it's a painkiller.

## Competition
- **Current behavior:** Manual process — Google the company, skim their LinkedIn, check Crunchbase, open a blank slide deck, write bullets, format slides, think through objections in their head or a notes app. Some use ChatGPT to draft sections, then paste into their own templates. A few have built partial automations (a research script, a deck template) but nothing end-to-end.
- **Real enemy:** The consultant's own confidence that they can "do it fast enough" manually. The switching cost isn't monetary — it's trust. They have to trust the tool's output enough to present it to a prospect without line-by-line review. That trust takes 3-5 successful uses to build.
- **Differentiation needed:** Not "AI generates slides" (everyone claims that). The differentiation is **depth and specificity**: a 6-stage pipeline that produces industry-specific strategy briefs, branded decks with action titles and use-case realization slides, and objection scripts grounded in the prospect's actual competitive landscape — not generic templates with the company name swapped in.

## First 10 Customers
1. **AI consultant communities on LinkedIn/Twitter.** Post a before/after: "Here's what my deal-prep looked like before vs. after I automated it" with screenshots of a real (anonymized) output. DM the 10 people who engage most thoughtfully. Ask for a 15-minute call to show them the output for their next prospect. Success: 3 conversations booked.
2. **Nate Herk's AI Automation Society (School community).** 390K+ members, many are AI consultants or aspiring ones. Share the grill-me → deal-prep chain as a case study. Offer to run the pipeline for 5 members' real prospects for free. Success: 5 people hand you a prospect name and you deliver a package.
3. **Personal network of consultants from past projects.** Reach out to 5 people you've worked with or alongside. Offer a free concierge run: "Give me your next prospect, I'll prep the full package in 24 hours." Success: 2 say yes, 1 becomes a recurring user.

## MVP
- **Build:** Concierge MVP — the founder runs the existing skill chain manually for each customer. No product to build. Customer submits a prospect name via a simple form (Typeform or DM). Founder runs `/presales-deal-prep`, `/ai-strategy-brief`, `/branded-pptx-deck`. Delivers the package within 24 hours. This tests the core assumption (quality + willingness to pay) without writing any product code.
- **Cut:** User-facing dashboard, self-service onboarding, Stripe billing, template customization, CRM integrations, team features, analytics. None of these test the core assumption.
- **2-week test:** Run the concierge for 5 consultants (from First 10 Customers above). After each delivery, ask two questions: (1) "Did you use this in your meeting?" and (2) "Would you pay $300/month for this every week?" If 3/5 used it and 3/5 would pay, the assumption holds. If <3 used it, dig into why — quality issue or trust issue? The pivot if it fails: narrow to a single vertical (e.g., "Pre-Sales Copilot for AI consultants selling to manufacturers") where the founder's domain knowledge makes the output dramatically better than generic.

## Edits Applied to product-idea.md
- **Risky assumptions** — replaced with the three from the validation report (output quality perception, willingness to pay vs. DIY, data accessibility)
- **Target user** — tightened the revenue range to $30K-$60K average deal size based on early adopter profile
- No other fields changed — the idea was already well-scoped from the Idea phase

## Next Step
Proceed to `/plaid` (Plan) — the idea holds up. Keep one eye on the differentiation score (3/5): the 2-week concierge test should include a "would you switch from your current process?" question to validate that the depth advantage lands with real users.
