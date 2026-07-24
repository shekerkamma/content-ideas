---
marp: true
paginate: true
size: 16:9
title: The Agent Validation & Assurance Authority
style: |
  :root {
    --bg:#0a0e14; --panel:#121826; --ink:#e8eef7; --muted:#8a99b3;
    --teal:#22d3ee; --sky:#38bdf8; --magenta:#e879f9; --amber:#fbbf24; --green:#34d399; --red:#fb7185;
  }
  section {
    background: radial-gradient(1200px 600px at 80% -10%, rgba(56,189,248,.10), transparent 60%),
                radial-gradient(900px 500px at -10% 110%, rgba(232,121,249,.10), transparent 60%), var(--bg);
    color: var(--ink); font-family: -apple-system, "Segoe UI", Inter, system-ui, sans-serif;
    padding: 56px 64px; font-size: 22px; letter-spacing:.2px;
  }
  h1 { color:#fff; font-size:40px; line-height:1.1; margin:0 0 .3em; }
  h2 { color:var(--teal); font-size:30px; line-height:1.15; margin:0 0 .5em; font-weight:700; }
  h3 { color:var(--sky); font-size:22px; margin:.2em 0; }
  strong { color:#fff; }
  em { color:var(--amber); font-style:normal; }
  a { color:var(--sky); }
  table { font-size:18px; border-collapse:collapse; width:100%; background:transparent; }
  section table th { color:var(--teal) !important; text-align:left; border-bottom:1px solid rgba(255,255,255,.22); padding:7px 10px; background:transparent !important; }
  section table td { border-bottom:1px solid rgba(255,255,255,.10); padding:7px 10px; background:transparent !important; }
  section table tbody tr td:not(.x) { color:#eaf1fb !important; }
  section table tbody tr:nth-child(even) td:not(.x) { background:rgba(255,255,255,.05) !important; }
  section table tbody tr td:not(.x) strong { color:var(--amber) !important; }
  section table thead tr th:not(.x) { color:var(--teal) !important; }
  ul { line-height:1.5; } li { margin:.18em 0; }
  code { color:var(--amber); background:rgba(255,255,255,.06); padding:1px 6px; border-radius:5px; }
  section::after { color:var(--muted); }
  .lead { font-size:30px; color:#fff; line-height:1.25; }
  .tag { color:var(--magenta); font-weight:700; letter-spacing:1px; font-size:16px; text-transform:uppercase; }
  blockquote { border-left:3px solid var(--magenta); color:#fff; font-size:26px; padding-left:18px; margin:.4em 0; }
---

<!-- _paginate: false -->
<span class="tag">Positioning thesis · v1 · 2026-06-24</span>

# The Agent Validation & Assurance Authority

## The UL / SOC-2 for autonomous AI agents

Independent validation that lets a regulated enterprise put an AI agent into production — and survive the exam.

*Beachhead: U.S. super-regional banks. Vertical 2: automotive captive finance + OEM agent fleets.*

---

## Agents are shipping faster than anyone can trust them

- Every Fortune 500 is deploying agents into production in 2025–26 — **support, decisioning, SecOps, supply chain.**
- **40%+ of agentic AI projects will be cancelled by 2027** (Gartner) — killed by trust, not capability.
- Klarna publicly reversed its AI-first support after quality tanked.
- The blocker is the same everywhere: *nobody can prove the agent is safe to run.*
- That proof is a market. We sell it.

---

## The market moved from "can we build an agent" to "can we trust one"

- 2023–24: the race was capability — frameworks, models, demos.
- 2026: capability is commoditized; **the model is no longer the moat.**
- The new question is operational: predict it, audit it, roll it back.
- Non-determinism breaks the old QA playbook — same prompt, two different actions.
- *Trust is now an infrastructure problem before it is a product feature.*

---

## April 17, 2026: regulators handed agentic AI back to the banks

- **SR 26-2** (OCC / Fed / FDIC) replaced SR 11-7 — the 15-year model-risk rulebook.
- One sentence defines the moment: *"Generative AI and agentic AI models… are not within the scope of this guidance."*
- Translation: banks own agentic-AI governance with **no playbook** — and an AI rulemaking is coming.
- Examiners still ask: *"What is your monitoring framework? What is your effective challenge?"*
- > "Can you name the person whose name should be on the examination finding?"

---

## The pain is deployed, not hypothetical — and it is failing

- **Wendy's FreshAI** takes drive-thru orders end-to-end; **Mercedes MBUX**, **Home Depot Magic Apron** run live.
- **SOAR auto-remediation** agents touch production infra without a human.
- These handle **80%+ of volume** — then break in ways no one tested for.
- Manual QA covers ~100 scenarios; real users trigger millions.
- The gap between "deployed" and "validated" is where we live.

---

## Nobody independent can grade the agents — the labs grade themselves

- Foundation labs ship native guardrails — but they cannot certify their own ecosystem.
- Eval vendors (Braintrust, Arize, Patronus) sell tooling to the **builder**, not assurance to the **buyer**.
- The Big 4 do bespoke manual reviews at six figures — slow, unrepeatable, no standard.
- Internal model-risk teams have no agent-native method.
- *The one thing none of them can claim is independence. That is our wedge.*

---

## 9 ways to position an agent company — 8 are already taken

- **Taken (8):** Adapter → Glean · New primitive → LangChain · Services-as-software → Sierra · Sub-vertical → EvenUp · Replacement → Devin · Data moat → Harvey · Interface → Lovable · Industrial layer → Skild.
- **Open — pattern 7: Trust. Certify the agent.** *Nobody owns it.*
- That is our lane: the independent referee for the other eight.
- Every taken lane builds or runs an agent. **We grade them — and the grader can't also be a player.**

---

## Where defensible money lives: KEEP, not REPLACE

- A 25-use-case scorecard sorts every deployed agent by moat.
- **REPLACE = low moat** → commoditizing; labs and incumbents win; wrappers die.
- **RENEGOTIATE = medium moat** → co-exist, drop the bolt-on seats.
- **KEEP = high moat** → proprietary data compounds; the defensible zone.
- We don't build an agent in any zone. **We certify the agents others ship — and own the standard.**

---

## Our position: certify the autonomous agent before it ships

- Package agent assurance as a **hiring bar for the agent**: *"passed before you deployed it."*
- Sell to the risk owner, not the developer — that is where pricing power lives.
- Architecture: supervised validation + adversarial red-team + counterfactual provenance.
- Output the buyer can show a regulator, a board, or a court.
- *We are the referee, not another player.*

---

## What we are: the UL / SOC-2 for AI agents

- An **independent authority** whose stamp the market trusts.
- We do not build agents. We do not resell a builder's tool.
- We validate, certify, and continuously assure autonomous agents in regulated production.
- We **author the benchmark** that defines what "safe to deploy" means.
- Independence is not a feature — it is the entire product.

---

## The product: an examiner-ready Agent Validation Dossier

1. **Conceptual soundness** — design, data, guardrails, escalation paths.
2. **Outcome testing** — vs our domain benchmark + adversarial / red-team suite.
3. **Monitoring thresholds** — drift, re-validation triggers on prompt/model change.
4. **Counterfactual provenance** — why it acted, and why it didn't do the near-miss.
5. **Control attestations** — data handling, human-in-loop, fair-lending.

Deliverable: a report the buyer hands their examiner + a live assurance dashboard + a time-boxed "Validated" mark.

---

## Beachhead: the SR 26-2 vacuum in financial services

- Banks must self-determine agentic-AI controls — and have nothing.
- The buyer and budget already exist: **model risk / AI governance** is a mandated function.
- We slot in as the independent validation that function is required to obtain.
- The regulatory vacuum is the opening; the coming AI RFI is the deadline.
- *First mover authors the standard before the rulebook lands.*

---

## We don't certify chatbots — we validate the agents MRM can't

- Skip the BAU: generic support bots and OCR are solved, low-stakes, vendor-benchmarked.
- Lead with **novel autonomy + high stakes + no validation method**:
- **Advisory / action-taking** customer agents → suitability, UDAAP, fair-lending.
- **Agentic decisioning** → credit, underwriting, collections, adverse-action (ECOA).
- **AML / fraud investigation** agents → SAR quality. **SecOps auto-remediation** → audit risk.

---

## Sell to the CRO; the examiner is the judge

- **Economic buyer:** Head of Model Risk / Chief Risk Officer — holds budget and personal liability.
- **Champion:** the AI-governance lead whose job is impossible without us.
- **User:** the line-of-business that must pass our gate to ship.
- **The rejectable counterparty:** the **bank examiner** — our dossier must survive exams.
- That bar is the forcing function and the moat: survive exams once, become un-switchable.

---

## The dossier maps to exactly what examiners already ask

- SR 26-2 keeps three validation pillars: **conceptual soundness, outcomes analysis, ongoing monitoring.**
- We mirror that structure — instantly legible, hard to argue with.
- Add the agentic layer SR 26-2 omits: tool-call safety, autonomy bounds, multi-agent error propagation.
- Anchor to NIST AI RMF + ISO/IEC 42001 so it reads as standard, not startup.
- *We give examiners the artifact they're about to demand.*

---

## Pricing: paid pilot first, assurance subscription forever

- **Pilot:** fixed-fee validation of one agent → examiner-ready dossier. Priced like an external model validation (5-figure).
- **Subscription:** annual per-agent continuous assurance — drift, re-validation, exam support.
- Buyer-funded, sits in the audit/MRM budget line — not a new category to justify.
- Pilot proves demand; subscription is the annuity.
- Same arc as pen-test → continuous security monitoring.

---

## The moat compounds 5 ways — and none of them is the model

1. **Cross-customer failure corpus** — what breaks, that no single bank or lab sees.
2. **The benchmark we author** — we define "good," like Harvey's Legal Agent Benchmark.
3. **Examiner acceptance** — a track record of surviving exams.
4. **Structural independence** — labs and eval vendors structurally cannot copy it.
5. **Workflow + board-reporting lock-in** — embedded in MRM's process.

---

## GTM: services-led, benchmark-amplified, platform-destined

- **Phase 0:** 5+ discovery calls → 1 paid teardown. Buy demand evidence with real fees.
- **Phase 1:** paid pilots seed the failure corpus + reference logos.
- **Phase 2:** productize into a platform; publish the benchmark to set the standard.
- Channel: co-deliver with Big 4 / model-risk consultancies — arm them, don't fight them.
- Build nothing reusable before pilot #1 is paid.

---

## Demand is already moving: KeyBank, Fifth Third, Regions

- **KeyBank ($189B):** 40 AI POCs; hired an AI Risk Advisor; an AI Security Architect role names *"controlled autonomy of AI agents."*
- **Fifth Third ($210B):** building *"governance, kill switches"* for the agents it's shipping; *"third part is agentic execution."*
- **Regions ($160B):** AI-integrated lending platform launches **Q2 2026** — decisioning is our wedge.
- All three: active agents **and** a named model-risk function. Qualified, now.
- *GTM owns who to call — research handed over the accounts and the signals.*

---

## Vertical 2: automotive captive finance is the same buyer

- **Toyota Financial Services / TMCC** and **Nissan Motor Acceptance / NMAC** are regulated lenders.
- Same fair-lending, adverse-action, model-risk, agentic-validation need. Same SR 26-2 vacuum.
- This is Thesis A's first expansion — **not a new company.**
- Buyer logic is identical: Chief Risk / Model Risk at the captive arm.
- One thesis, two regulated doors.

---

## Vertical 2b: OEM agent fleets need a referee, not another agent

- **TMNA** runs a "system of agents" + a Cube Command Center; dealer agent serves **2,300 dealers, 7,000+ interactions/mo.**
- Toyota already bakes legal disclaimers into the dealer agent — wrong spec/price/**recall info = liability.**
- Dealer-chat agents (Impel, PureCars, Cerence) are crowded BAU — avoid that lane.
- The open layer: **govern + validate the fleet** — brand safety, legal compliance, multi-agent provenance.
- Same thesis, applied above the commoditizing apps.

---

## Why now: a 12-month window to author the standard

- SR 26-2 created the vacuum on April 17, 2026; the AI RFI is next.
- Analysts peg the window to own a vertical position at **mid-2026 → mid-2027.**
- After that, markets consolidate to 2–3 players per vertical.
- The standard-setter is decided in that window — by whoever publishes first and survives exams.
- Move now, or validate someone else's standard later.

---

## Why us: independence you can't fake, no data moat required

- We need **no pre-existing proprietary data** — the moat accrues as we operate.
- The auditor cannot be the builder — that's our permanent structural edge.
- A small team can author a benchmark and win design partners before incumbents productize.
- Founding requirement, stated plainly: an **ex-MRM / ex-examiner** on the cap table — credibility is the product.
- Everything else is reversible; that hire is not.

---

## Competition: Big 4, Patronus, the labs — and why we win

- **Big 4 / MRM consultancies** — bespoke manual reviews → we productize the work and arm them as channel.
- **Patronus / eval vendors** — sell evals to the *builder* → we sell assurance to the *buyer*.
- **Foundation labs** — ship native guardrails → they can't certify their own ecosystem.
- **In-house MRM** — first-line build → lacks our independence and cross-bank failure corpus.

---

## The honest risks — and the gates that kill or fund us

- **No demand** (existential) → 5 discovery calls must surface one *blocked, paying* buyer.
- **No insider** (existential) → no ex-MRM/ex-examiner = don't approach banks.
- **Self-attestation blessed by regulators** → kill signal; pivot.
- **Services trap** → every engagement must templatize into the product, or stop.
- Pass all three gates in 90 days → release platform funding. Fail → pivot, cheaply.

---

## Two golden rules that keep us honest

- **GR1 — Paid pilots force demand.** Every conversation drives to a *paid* validation pilot. No free pilots. Politeness isn't demand.
- **GR2 — GTM owns outreach.** Research hands over qualified accounts, signals, and scripts. GTM names and contacts the humans.
- These are not slogans — they are the discipline that prevents building on a hypothesis.
- Break either and we're back to slideware with no buyer.

---

## 90 days: 5 calls, 1 paid pilot, 1 insider

- **Weeks 1–4:** 5+ MRM/CRO discovery calls; find one *currently blocked* autonomous agent.
- **Weeks 1–8:** sign 1 paid "Agent Validation Teardown."
- **Weeks 1–8:** commit an ex-MRM / ex-examiner advisor or co-founder.
- **Parallel:** draft the FS Agent Validation Benchmark v0 — the teardown spine.
- Every milestone is observable, not aspirational.

---

<!-- _class: lead -->
## Next action

**Run the 5 discovery calls. Sign one paid pilot. Land one insider.**

Everything in this deck waits behind those three. The vacuum is open now — the standard gets written by whoever moves first and survives the exam.

*Let's go get the first paid pilot.*

---

<!-- _paginate: false -->
## Appendix — the evidence base

- **Pattern library** (9 patterns) + **emerging patterns** (E1–E9) — `research/agentic-positioning-pattern-library`, `research/emerging-positioning-patterns`
- **10-company dossiers** (Harvey live; Sierra, Cursor, Cognition, LangChain, Browserbase, OpenEvidence, Glean, Braintrust, Skild queued)
- **Use-case alignment** to the 25-use-case scorecard — `research/pattern-usecase-alignment`
- **GTM packages:** FS bank targets + SR 26-2 reframe; automotive (captive finance + OEM fleets)
- **Discipline:** CEO kill-gates + two golden rules — `research/ceo-verdict-thesis-a-gates`, `research/golden-rules`
