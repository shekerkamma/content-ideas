# Agentic Wedge Dossiers: Alignment Stress-Test
Date: 2026-06-26 · Goal: Pressure-test whether the 25 saas-gap-analyzer wedge dossiers actually serve the user's real objective — not just whether they're well-constructed.

## Structured context
- **Topic type**: strategy
- **Topic string**: "Alignment of 25 agentic-wedge OSINT dossiers with the user's real go-to-market objective"
- **Entities**: saas-gap-analyzer skill, Agent_Use_Cases.md (25-use-case taxonomy), Exa OSINT, DataStaqAI / done-for-you AI engineering micro-agency, pipeline-runner, vertical-scorer, OpenHands
- **Prospect/account**: n/a (this is the user's own GTM ammunition, not a named deal yet)
- **Target buyer**: TBD (depends on intended use of dossiers)
- **Verticals**: 11 industries spanned by the taxonomy
- **Open decisions**: (1) what the dossiers are FOR; (2) whether "proven wedge" requirement was met; (3) depth vs breadth; (4) competitive-landscape gap; (5) next step / chaining

## Deliverable under review
- 25 dossiers + `_INDEX.md` at `/mnt/d/New folder/Antigravity-test/antigravity-skills/wedge_dossiers/`
- Format per dossier: Target SaaS → OSINT source map → verbatim friction → psychographics → Agentic Wedge → buyer trigger
- 105 unique source URLs, 237 verbatim-quote lines, ~118 KB
- Verdict spread: REPLACE 10 · RENEGOTIATE 9 · KEEP 6
- 25/25 passed pain threshold, 0 discarded

## REFINED GOAL (user, Q3)
> "All we are doing is identifying prospects with competitive edge."
The deliverable = **named prospects**, each paired with the agentic-wedge thesis that gives DataStaqAI a differentiated way into the account. Dossiers built so far = the EDGE half (documented pain + wedge + buyer trigger). Missing = the PROSPECT half (attributed leads + huntable ICP). The grill's job is done: alignment verdict + fix path below.

## ALIGNMENT VERDICT
- **80% aligned.** Dossiers are best-in-class DEMAND-PROOF + competitive-edge talk-track. They are NOT yet a prospect list.
- **Three gaps, in priority order:**
  1. **Leads discarded inside the evidence** — 105 cited complaint URLs each trace to a company/role; dossiers kept the quote, dropped the attribution. (highest leverage)
  2. **No huntable ICP / buying-signal layer** — no firmographics or observable triggers to source a list.
  3. **No build-vs-partner call** — for a delivery agency, "do we build it or wire an existing tool" is unanswered (OSINT often surfaced the tool by accident).
- **Non-gap (don't fix):** breadth of 25 is correct for a hunt GTM; depth-per-dossier is sufficient as edge ammo.

## Summary / key decisions
- **Q3 — Sourcing = (a) re-mine cited complaint URLs for company+role+dated-pain (warm leads), backfilled by (c) intent signals (job posts, EOS/renewal events, tech-stack tells). User: "go ahead with your recommendations."**
- **Q1 — Purpose = (B) pre-sales/pipeline ammunition, primary; (C) returnable catalog as free backstop. NOT (A) build-it-yourself.** Recommended by assistant; user asked assistant to decide. → Implication: breadth (25) is correct, but dossiers are strong DEMAND-PROOF and incomplete DEAL-PREP. Two known gaps to close: (1) no named target account, (2) no competitive map / build-vs-partner call per wedge.

- **Q2 — Activation = wedge-first / HUNT-for-accounts (user corrected assistant's "account-first").** GTM motion = wedge+pain is the thesis, then go hunt accounts experiencing it. → Implication: dossiers need a TARGET-ACCOUNT HUNTING layer (firmographic ICP + observable buying signals + how to source a list). Current dossiers have buyer-trigger + psychographics but NOT firmographics/sourcing — that's the gap.

## Q&A log
### Q3 — Account-sourcing mechanism for the hunt?
- Asked: (a) re-mine cited complaints for attribution, (b) firmographic list-building, (c) intent signals?
- Captured: **(a)-led + (c) backfill**, assistant to execute. User reframed the entire goal: "All we are doing is identifying prospects with competitive edge." → deliverable is prospects; wedge = the edge.
- Flags: confirm execution scope (all 25 vs top-N first) -> user

### Q2 — Account-first or wedge-first?
- Asked: Does a dossier become a deal by matching to an existing target list (account-first) or by ranking wedges then hunting accounts (wedge-first)?
- Captured: User corrected to **hunt-for-accounts**. "GTM need to hunt for accounts, that makes sense." So wedge-first leaning: the dossier's pain thesis drives a prospecting hunt. Gap confirmed: dossiers lack a huntable ICP + signal layer.
- Flags: each activated dossier needs a "Target Account Profile + Buying Signals + Sourcing" section -> assistant to design

### Q1 — What are the dossiers for?
- Asked: Are these (A) startup blueprints, (B) pre-sales/pipeline ammunition, or (C) a market-map artifact?
- Captured: User deferred to assistant. **Decision: (B) primary + (C) backstop.** Rationale: user's model is a done-for-you AI engineering micro-agency (sells delivery), with pipeline-runner / vertical-scorer / OpenHands kit already built — (A) would contradict the whole stack. 25-wide is right for matching wedges to incoming prospects. Gap identified: dossiers are excellent demand-proof but thin deal-prep (no named account, no build-vs-partner call).
- Flags: confirm (B) with user if they later push back -> user

## GOAL CORRECTION (user, post-prospect-detour)
> "We do not have to identify named accounts. We are interested in what use cases these organizations are pursuing, how we can pitch and position ourselves. That is the reason I told you about use cases."
**TRUE GOAL = use-case-driven POSITIONING & PITCH for DataStaqAI's done-for-you AI engineering offer.** The 25 use cases = the market demand map. Named companies = evidence only, NOT targets. Prospect-hunting (prospects.csv / _PROSPECTS_top6.md) was a MISDIRECTION — keep as evidence appendix, not the deliverable.
**Right deliverable = a Positioning & Pitch Card per use case:** what the market is doing + the pain + our POV/positioning + our packaged offer + the pitch hook + why-us-vs-alternatives. Show as filled copy, NOT instructions (user dislikes instructional output).

## EXECUTION (post-grill)
- User chose scope = **Top 6 highest-signal first**. Built `_PROSPECTS_top6.md` in wedge_dossiers/.
- 6 Prospect Packs (CPQ, SOAR, SIEM, Legal, Low-code, IDP/OCR AP): each = ICP + buying signals + REAL named entities (tagged ✅ live / ⚪ already-switched / ◻ anonymized) + build-vs-partner call + edge talk-track + sourcing next step.
- Sourced via 6 intent-focused Exa hunts. No hallucinated prospects — every name traces to a cited source.
- **Key findings:**
  - Hottest live signals: SIEM = SOC-analyst hiring posts (e.g., ZainTECH Managed SOC, live 2026-06-25); Legal = Hanson Bridgett openly re-evaluating Harvey/Legora vs Claude.
  - Build-vs-partner: **5 of 6 are PARTNER/INTEGRATE plays; only Low-code (#5) is a true BUILD play** = best fit for the done-for-you engineering agency's core competency.
  - Discipline: ⚪ "already switched" names = proof/persona maps, NOT call list; hunt the ✅/◻ profiles still in pain.

## Open flags (pending input)
- Purpose (B) was assistant-decided; user can still veto -> user
- Remaining 19 wedges have no Prospect Pack yet (scope = top 6 first) -> user decides when to scale
- Lead names beyond those in sources must be sourced via list tool / job-board scrape -> downstream prospecting run
