---
marp: true
theme: default
paginate: true
backgroundColor: #F7F6F2
style: |
  section {
    font-family: Inter, Aptos, Arial, sans-serif;
    color: #111827;
  }
  h1 {
    font-size: 44px;
    letter-spacing: 0;
  }
  h2 {
    font-size: 31px;
    letter-spacing: 0;
  }
  p, li {
    font-size: 22px;
    line-height: 1.28;
  }
  strong {
    color: #92400E;
  }
  .kicker {
    color: #6B7280;
    font-size: 18px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
  .small {
    font-size: 17px;
    color: #4B5563;
  }
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 28px;
  }
  .box {
    border-left: 6px solid #D97706;
    padding-left: 18px;
  }
  table {
    font-size: 18px;
  }
---

<!-- _paginate: false -->

# The 10-Skill Operator Stack for 30-Day Agentic MVPs

### A repeatable system for validating, scoping, architecting, shipping, and iterating agentic opportunities

<br>

**The 52 reviewed opportunities prove breadth. The 10-skill stack proves execution discipline.**

---

## This Is Not a Blueprint Deck

The miss to avoid: leading with "we have implementation blueprints."

The stronger claim:

**We have a full operator system that replaces the traditional dev-shop journey from diagnostic through post-launch iteration.**

The use cases are proof.  
The operating stack is the product.

---

## The Old Way Burns Budget Before Proof

Traditional dev-shop discovery often charges heavily before the MVP has earned the right to exist.

| Phase | Source-backed replacement target |
|---|---:|
| Diagnostic | $10K-$15K |
| Scope document | $15K-$25K |
| Architecture | $20K-$40K |
| Build vs buy analysis | ~$30K hidden in SOW |
| Market scan | $15K |
| Shipping definition / QA | $20K-$35K |

---

## The New Way Is a Gated Operating System

Validate -> Scope -> Architect -> Build/Buy -> ROI -> Teardown -> QA -> Data -> Deploy -> Iterate

<br>

Each skill produces a concrete artifact.  
Each skill has a human operator gate.  
Each gate exists because raw AI output can look confident while missing the real risk.

---

## Skill #1: Problem-Solution Fit Validation

<div class="grid">
<div>

**Job**

Stop the founder from spending 30 days building the wrong thing.

**Artifact**

A 0-30 scored verdict:

- Problem realness
- Solution fit
- Buying signal + reachability

</div>
<div class="box">

**Operator Gate**

Check whether the 3 named users are representative, whether "I'd use it" is actually a buying signal, and whether regulatory or distribution constraints kill the 30-day assumption.

</div>
</div>

---

## Skill #2: 30-Day Scope Definition

<div class="grid">
<div>

**Job**

Turn a validated problem into a build contract.

**Artifact**

A 1.5-2 page scope:

- Core hypothesis
- 5-7 in-scope features
- 10+ out-of-scope cuts
- Weekly milestones
- Risks and acceptance test

</div>
<div class="box">

**Operator Gate**

Cut founder feature creep, challenge integration optimism, and calibrate the plan to real weekly velocity.

</div>
</div>

---

## Skill #3: Tech Stack + Architecture Design

<div class="grid">
<div>

**Job**

Create the technical ground truth for a 30-day MVP.

**Artifact**

Stack, database schema, RLS, auth flow, API surface, integration plan, folder structure, env vars, and critical design decisions.

</div>
<div class="box">

**Operator Gate**

Override generic stack advice when context demands it, catch RLS leaks, and protect the migration path from v1 to v2.

</div>
</div>

---

## Skill #4: Build vs Buy Decision Matrix

<div class="grid">
<div>

**Job**

Decide what to build, what to buy, and what to hybridize.

**Artifact**

Feature-by-feature matrix:

- Build cost
- 3-year SaaS cost
- Lock-in risk
- Verdict
- Payback period

</div>
<div class="box">

**Operator Gate**

Price in SaaS creep, niche workflow misfit, and lock-in that looks harmless in year 1 but expensive in year 3.

</div>
</div>

---

## Skill #5: MVP ROI Business Case

<div class="grid">
<div>

**Job**

Gate whether the MVP economics justify proceeding.

**Available Source Artifact**

The current source preserves one hard rule:

**If breakeven is past month 36 in the base case, the MVP is not viable solo.**

</div>
<div class="box">

**Operator Gate**

Do not let excitement about the build outrun the payback logic.

<br>

<span class="small">Source note: the complete Skill #5 prompt is missing from the local stack. This deck does not fabricate it.</span>

</div>
</div>

---

## Skill #6: Competitor Product Teardown

<div class="grid">
<div>

**Job**

Name the incumbents and expose where a focused MVP can win.

**Artifact**

5-10 competitor profiles:

- Positioning
- Pricing
- Features
- Onboarding
- Strengths
- Weaknesses
- Copy / avoid / exploit list

</div>
<div class="box">

**Operator Gate**

Find the competitors that do not show up in obvious searches, read positioning instead of feature lists, and flag unverifiable pricing.

</div>
</div>

---

## Skill #7: Acceptance Criteria + Test Plan

<div class="grid">
<div>

**Job**

Define what "shipped" means before anyone declares victory.

**Artifact**

Per feature:

- User story
- 3-5 testable acceptance criteria
- Edge cases
- Not-in-scope list
- Manual test steps

</div>
<div class="box">

**Operator Gate**

Test the failure modes that happen across features: signup plus payment, slow APIs, duplicate clicks, auth boundaries, and launch-night surprises.

</div>
</div>

---

## Skill #8: Data Architecture Lite

<div class="grid">
<div>

**Job**

Make data and analytics part of v1, not cleanup after launch.

**Artifact**

Sources, storage, source of truth, sync mechanism, conflict resolution, top 5 analytics questions, events, and data quality guardrails.

</div>
<div class="box">

**Operator Gate**

Surface the real data stores: spreadsheets, Notion docs, manual refunds, support notes, and any place where truth can drift.

</div>
</div>

---

## Skill #9: Deployment Sequencing

<div class="grid">
<div>

**Job**

Turn launch into a sequence with rollback, not a button press.

**Artifact**

Pre-deploy checklist, staging setup, production sequence, smoke test, and rollback plan.

</div>
<div class="box">

**Operator Gate**

Verify env vars, production webhook secrets, redirect URLs, real payment flow, session persistence, and User A/User B data isolation before announcement.

</div>
</div>

---

## Skill #10: Post-Launch Iteration Plan

<div class="grid">
<div>

**Job**

Keep the founder from reacting chaotically after launch.

**Artifact**

Three metrics:

- Activation
- Retention
- Revenue or willingness to pay

Plus feedback triage, four-week plan, and pivot signals.

</div>
<div class="box">

**Operator Gate**

No new features in week 1. Bugs and quick wins only. Then talk to active users and build one feature that should move retention.

</div>
</div>

---

## The Operator Gate Is the Moat

Raw AI can generate documents.

The operator system asks the sharper questions:

- Is the buyer real?
- Is the scope honest?
- Is the architecture safe?
- Is SaaS lock-in priced?
- Is competitor data verified?
- Is "done" testable?
- Is data truth protected?
- Is launch reversible?
- Is post-launch learning disciplined?

---

## The 52-Opportunity Portfolio Proves Breadth

The prior run contains **52 implementation-reviewed opportunity blueprints**.

That portfolio matters because it shows the same stack can apply across:

support, HR, compliance, security, legal, finance, healthcare, retail, logistics, marketing, product, and operations.

The deck should not become a catalog.  
The catalog is proof that the operating system repeats.

---

## What We Can Claim Now

**Strong claim**

We have a complete 10-skill operator stack and 52 implementation-reviewed opportunities that demonstrate repeatability.

**Careful claim**

Competitor teardown is a required Skill #6 gate. External publication should attach source-backed incumbent/pricing evidence per use case before claiming every market map is complete.

---

## The Market-Facing Offer

We do not sell vague AI transformation.

We do not start by selling a build.

We bring the full operating system to the table:

**Validate the problem. Cut the scope. Architect the build. Decide build vs buy. Gate ROI. Map incumbents. Define QA. Wire data. Deploy safely. Iterate with discipline.**

---

<!-- _paginate: false -->

# Closing Thesis

The 52 opportunities prove market surface.

The 10 skills prove execution discipline.

The human operator gates prove why this is more than prompt automation.
