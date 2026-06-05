# Product Idea — Pre-Sales Copilot

## One-liner
An AI-powered pre-sales automation tool that takes a prospect name and delivers a complete deal-prep package — account briefing, strategy brief, branded deck, and objection scripts — in minutes instead of hours, for AI consultants selling enterprise engagements.

## Background
The founder runs an AI strategy consulting practice focused on enterprise manufacturers (automotive, heavy industry). Over months of real client work, he built a chain of Claude Code skills that automate the entire pre-sales workflow: prospect research, strategy analysis, vertical scoring, branded deck generation, and objection scripting. This product idea is the natural extraction of that battle-tested internal toolchain into a standalone product for other consultants facing the same pain.

## The problem
Solo AI consultants and small firms (2-10 people) selling $20K-$100K AI strategy and pilot engagements spend 4-8 hours per deal on manual pre-sales work: researching the prospect, writing strategy briefs, building client-facing decks, and preparing objection responses. At 3 active deals per week, pre-sales prep alone is a full-time job — time that can't be billed and doesn't scale. Most consultants either cut corners (generic decks, shallow research) or burn out.

## Target user
Solo AI consultants and boutique AI consulting firms (2-10 people) who sell $20K-$100K AI strategy, pilot, or implementation engagements to mid-market and enterprise companies. They're technically strong but time-poor, and their close rate depends directly on the quality of their pre-meeting preparation.

## Proposed solution
Input a prospect name (and optionally a use case or vertical). The system runs a multi-stage pipeline:

1. **Account research** — pulls company context, recent news, industry position, AI maturity signals
2. **Strategy brief** — generates a one-page AI opportunity brief tailored to the prospect's industry and challenges
3. **Branded deck** — builds a polished, editable .pptx with action titles, use-case realization slides, competitive positioning, and pricing options
4. **Objection scripts** — prepares responses to the 5 most likely pushback themes with coaching notes
5. **Discovery agenda** — generates the meeting's question framework based on the prospect's profile

**Magic moment:** Type a company name, get a complete deal-prep package you'd be proud to walk into a meeting with. Review and edit in 15 minutes instead of building from scratch in 4 hours.

## Why you
The founder built and uses this exact pipeline daily on real enterprise deals. Every component is a battle-tested Claude Code skill (presales-deal-prep, ai-strategy-brief, branded-pptx-deck, 00-account-briefing) refined through actual client engagements. The depth of the chain — and the quality gates built into each stage — would take a competitor months to replicate.

## Candidates considered

| # | Idea | Unfair Advantage | Pain Level | Reachability | MVP Feasibility | Differentiation |
|---|------|-----------------|------------|--------------|-----------------|-----------------|
| 1 | AI Pilot-in-a-Box (packaged use-case → pilot tool for manufacturers) | 🟢 Built it | 🟢 $50K+ pilots | 🟡 Enterprise = slow | 🟡 4-6 weeks | 🟢 Nobody packages this |
| 2 | **Pre-Sales Copilot** (prospect → full deal-prep package) | 🟢 Daily user | 🟢 Hours/deal | 🟢 LinkedIn + community | 🟢 Skills exist | 🟡 Crowding fast |
| 3 | Skill OS Marketplace (share/install/chain Claude Code skills) | 🟢 First ecosystem | 🟡 Nice-to-have | 🔴 Tiny market today | 🔴 Platform = hard | 🟢 Nobody does this |
| 4 | Factory Intelligence Dashboard (predictive quality for automotive) | 🟡 One client | 🟢 $M losses | 🔴 Enterprise only | 🟢 Fork exists | 🟡 Competing w/ Siemens |
| 5 | Content-to-Pipeline Engine (competitor content → deal pipeline) | 🟢 Built it | 🟡 Medium pain | 🟢 Your audience | 🟢 Running now | 🟡 Niche |

**Selected: Candidate 2** — strongest across all five axes. Skills already exist as working code, audience is reachable, and pain is acute.

## Risky assumptions
1. **Willingness to pay:** AI consultants will pay for pre-sales automation vs. building their own skill chains or using generic tools (ChatGPT + manual editing)
2. **Output quality bar:** The generated briefs, decks, and scripts are good enough to use with minimal editing — if they require 2 hours of rework, the value prop collapses
3. **Data accessibility:** Sufficient prospect/company information is publicly accessible (or via affordable APIs) to generate meaningful account research without manual input

## Next step
Run `/plaid validate` to pressure-test the idea before planning, or `/plaid` to jump straight into the Plan intake. The product-idea.md above will pre-fill much of your product vision.
