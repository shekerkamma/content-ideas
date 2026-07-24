# Office Hours Design Doc — Agent Validation & Assurance Authority (Thesis A)
Date: 2026-06-24 · Mode: Startup (pre-product) · Self-run YC diagnostic

## Problem Statement
Banks are deploying AI agents (customer support, KYC/lending doc-AI) into regulated production. Model Risk Management (MRM) functions are legally required (SR 11-7 / SS1/23) to independently validate these "models" before go-live and monitor them after — but they have no agent-native validation method or tooling. Result: blocked go-lives, exam risk, or unvalidated rubber-stamps.

## Demand Evidence (HONEST — this is the weak link)
- **Direct demand: NONE yet.** No named MRM/CRO has said "I'm blocked and would pay."
- **Structural signal (not demand):** SR 11-7 mandate is real, funded, legally required; AI is explicitly in scope. Big 4 already bill six figures for manual model validations. Gartner: 40%+ agentic projects cancelled by 2027. Patronus (compliance-first evals) is funded.
- **YC verdict:** "interest in the space" ≠ demand. **Must convert to behavior: a budgeted pilot or a panic.** This gates everything.

## Status Quo (the real competitor)
MRM teams today: force-fit statistical-model validation processes onto agents, block the deployment, or rubber-stamp. Big 4 do bespoke manual validations. Costs: slow go-lives, OCC/Fed MRAs, consulting spend. The workaround is expensive and real → problem is plausibly painful.

## Target User & Narrowest Wedge
- **User:** Head of Model Risk Management at a $20–80B-asset super-regional bank. Fired by: exam finding on an unvalidated AI model / a deployed agent causing fair-lending/conduct violation. Kept up by: business shipping agents faster than MRM can validate.
- **Wedge (paid this week):** one fixed-fee validation engagement on ONE deployed KYC doc-AI agent → ONE examiner-ready validation dossier. No-setup variant: paid benchmark teardown ("how your agent scores vs our FS Agent Validation Benchmark").

## Premises (must hold)
1. MRM teams genuinely lack an agent-native validation method today — agree (to verify via observation).
2. The risk owner (MRM/CRO), not the developer, holds budget and decision — agree.
3. An independent third-party validation is more credible to examiners than a builder's self-attestation — agree (core bet).
4. Regulators will tighten, not relax, AI-agent validation expectations — agree (the ratchet thesis; primary risk if wrong).
5. We can author a benchmark examiners will accept without being an incumbent — UNPROVEN (biggest execution risk).

## Founder Signals (self-assessed)
- Real problem: YES (mandate + expensive workaround). · Named users: PARTIAL (role precise, no real name yet — GAP). · Pushback/conviction: YES (challenged own premises). · Domain expertise: PARTIAL — **we lack an MRM/banking insider; this is the #1 hire/advisor gap.** · Taste/agency: positioning is sharp but no artifact built yet.

## Approaches Considered
**APPROACH A — Validation-as-a-Service (minimal viable)**
  Summary: pure services — manually validate one agent at one bank, produce examiner-ready dossier.
  Effort: S/M · Risk: Low · Pros: fastest revenue + learning, no product risk, builds the failure corpus · Cons: low early moat, services margins, doesn't scale yet · Reuses: consulting/audit motion.

**APPROACH B — Agent Validation Platform (ideal architecture)**
  Summary: productized validation mapped to SR 11-7 + the FS Agent Validation Benchmark as IP; services→subscription.
  Effort: L · Risk: Med · Pros: recurring revenue, compounding data moat, defensible · Cons: longer build, needs design partners first · Reuses: A's engagements as training data.

**APPROACH C — Benchmark-First / "Moody's for agents" (creative/lateral)**
  Summary: publish the FS Agent Validation Benchmark as an open standard, become category authority first, monetize certification + assurance after.
  Effort: M · Risk: Med/High · Pros: strongest positioning/moat, inbound, standard-setting · Cons: slow direct revenue, standard-acceptance risk · Reuses: thought-leadership GTM.

## RECOMMENDED APPROACH
**Services-led, benchmark-amplified, platform-destined: A → B, with C's benchmark published in parallel as the marketing/moat wedge.** Start with paid validation engagements (earn + learn + build the failure corpus), publish the benchmark to set the standard and drive inbound, then productize into the platform/subscription. This de-risks the "no demand evidence" hole by forcing paid pilots immediately.

## Open Questions / Flags
- Convert structural signal → real demand: get 5 MRM/CRO discovery calls; find one who is blocked NOW.
- Domain credibility: recruit an MRM/banking-insider co-founder or advisor (#1 gap).
- Standard anchor: NIST AI RMF / ISO 42001 vs proprietary benchmark.
- Will examiners actually accept a startup's validation artifact? (premise 5)
- Pricing magnitude per engagement + subscription.

## Success Criteria (next 90 days)
1. 5 MRM/CRO discovery conversations; ≥1 names a current blocked agent deployment.
2. 1 paid validation pilot (fixed fee) signed with a design-partner bank.
3. v0 of the FS Agent Validation Benchmark drafted + 1 examiner/ex-examiner reviews it.
4. MRM-insider advisor/co-founder onboarded.

## Distribution Plan
Co-deliver with model-risk consultancies / Big 4 (arm the channel); publish benchmark for inbound; target super-regional + mid-tier banks already running support/KYC agents.

## Dependencies
MRM/banking domain advisor; an examiner/ex-regulator reviewer; access to a deployed bank agent for the first validation.

## THE ASSIGNMENT (one concrete next action)
Get **5 conversations with Heads of Model Risk Management / CROs at super-regional banks** in the next 2 weeks. One question to validate: *"When the business hands you an AI agent to put in production, what do you do today, and what does it cost you?"* Find one who is blocked right now. Until a real MRM head says "I'm stuck on this," everything else is theory.
