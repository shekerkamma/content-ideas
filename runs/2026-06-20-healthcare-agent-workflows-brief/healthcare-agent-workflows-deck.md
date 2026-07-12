---
marp: true
theme: default
paginate: true
style: |
  section { background:#1b2838; color:#ecf0f1; font-family:ui-sans-serif,system-ui,sans-serif;
             padding:60px 80px 80px; border-bottom:4px solid #3498db; font-size:22px; }
  h1 { font-size:3.0rem; font-weight:800; color:#ffffff; letter-spacing:-.02em; line-height:1.1; }
  h2 { font-size:1.85rem; font-weight:800; color:#ffffff; margin-bottom:.4em; }
  h3 { font-family:monospace; font-size:.70rem; letter-spacing:.22em; text-transform:uppercase; color:#3498db; font-weight:400; margin-bottom:.3em; }
  p  { color:#ecf0f1; line-height:1.6; }
  ul { list-style:none; padding-left:0; margin-top:.5em; }
  ul li { padding-left:1.4em; position:relative; color:#ecf0f1; line-height:1.6; margin-bottom:.4em; }
  ul li::before { content:'→'; position:absolute; left:0; color:#3498db; font-family:monospace; }
  blockquote { border-left:4px solid #3498db; padding:.8em 1.8em; margin:1em 0 0; font-size:1.35rem; font-style:italic; color:#bdc3c7; }
  section::after { color:#7f8c8d; font-size:12px; letter-spacing:.2em; text-transform:uppercase; font-family:monospace; }
  .kicker { font-family:monospace; font-size:.8rem; letter-spacing:.22em; text-transform:uppercase; color:#3498db; margin-bottom:.6em; }
  .subtitle { color:#bdc3c7; line-height:1.6; font-size:1.05rem; max-width:56ch; margin-top:.6em; }
  .cols { display:grid; grid-template-columns:1fr 1px 1fr; gap:0; align-items:stretch; margin-top:.8em; }
  .col  { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.10);
          padding:20px 24px; display:flex; flex-direction:column; gap:8px; }
  .col:first-child { border-radius:10px 0 0 10px; border-right:none; }
  .col:last-child  { border-radius:0 10px 10px 0; border-left:none; }
  .col-rule { background:linear-gradient(180deg,transparent,#3498db 20%,#3498db 80%,transparent); width:1px; }
  .col-head { font-family:monospace; font-size:.65rem; letter-spacing:.22em; text-transform:uppercase; color:#3498db; }
  .col-title { font-size:1.15rem; font-weight:700; color:#ffffff; margin:0; }
  .col ul li::before { color:#3498db; }
  .col-tag { font-family:monospace; font-size:.65rem; letter-spacing:.14em; text-transform:uppercase;
             padding-top:10px; border-top:1px solid rgba(255,255,255,.10); margin-top:auto; color:#3498db; }
  .stat-num { font-size:7rem; font-weight:800; letter-spacing:-.04em; line-height:1; text-align:center; color:#3498db; }
  .stat-label { font-family:monospace; font-size:.68rem; letter-spacing:.22em; text-transform:uppercase;
                color:#7f8c8d; text-align:center; margin-bottom:.4em; }
  .chapter-num { font-size:6rem; font-weight:800; line-height:1; letter-spacing:-.04em; color:#3498db; font-family:monospace; }
  .verdict { display:inline-block; font-family:monospace; font-size:.75rem; letter-spacing:.18em;
             text-transform:uppercase; padding:6px 18px; border:2px solid #2ecc71;
             border-radius:999px; color:#2ecc71; margin-top:.6em; }
  .step-row { display:grid; grid-template-columns:2rem 1fr; gap:0 1rem; margin-bottom:.55em; align-items:start; }
  .step-num { font-family:monospace; font-size:.85rem; font-weight:800; color:#3498db; padding-top:.15em; }
  .step-text { color:#ecf0f1; line-height:1.5; font-size:.95rem; }
  .step-bold { font-weight:700; color:#ffffff; }
  table { width:100%; border-collapse:collapse; margin-top:.6em; font-size:.82rem; }
  th { background:#2c3e50; color:#3498db; font-family:monospace; font-size:.65rem; letter-spacing:.15em; text-transform:uppercase; padding:8px 12px; text-align:left; border-bottom:2px solid #3498db; }
  td { padding:7px 12px; border-bottom:1px solid rgba(255,255,255,.08); color:#ecf0f1; vertical-align:top; }
  tr:last-child td { border-bottom:none; }
  .highlight-row td { color:#ffffff; font-weight:600; }
  .next-action { background:rgba(52,152,219,.12); border:1px solid #3498db; border-radius:10px; padding:24px 28px; margin-top:1em; }
  .na-label { font-family:monospace; font-size:.65rem; letter-spacing:.22em; text-transform:uppercase; color:#3498db; margin-bottom:.4em; }
  .na-text { color:#ffffff; font-size:1.05rem; line-height:1.6; }
---

<!-- _class: lead -->

<div class="kicker">Executive Brief · June 2026</div>

# Agent Workflows for Healthcare

<div class="subtitle">
Prior authorization AI agents can cut processing time 60% and recover $800K/year in admin labor — and the CMS ePA API mandate makes 2027 the compliance deadline, not an aspirational target.
</div>

---

### CHAPTER 01 · THE PROBLEM

## Prior Auth Burns 25% of Clinical Admin Labor — on Rules, Not Judgment

Healthcare organizations lose $300B+ annually to administrative waste. Prior authorization is the highest-friction, highest-volume example:

- A clinician submits a PA request. A human reviewer checks eligibility, reads policy PDFs, verifies ICD-10 codes, and routes for approval — all manually.
- Average PA turnaround: 3–7 business days. For complex medications: weeks.
- 88% of physicians say PA causes care delays. 34% say it causes serious adverse events (AMA 2023).

The work is **rules-based, auditable, and structured** — exactly where AI agents win.

---

### CHAPTER 01 · THE SIGNAL

## Two Healthcare Platforms Opened to AI Agents in 30 Days

- **May 19, 2026 — Commure** raises $70M at a **$7B valuation** (Sequoia, General Catalyst). Explicit target: the $800B–$1T annual U.S. healthcare administrative labor market.
- **May 29, 2026 — Cognizant TriZetto Unify** opens to AI agents, starting with Electronic Prior Authorization. Reason cited: CMS Interoperability and Prior Authorization Final Rule — payer compliance 2026; ePA API mandates **effective 2027**.

Two of the largest healthcare IT platforms declared the same AI-agent category in 30 days. Organizations that wait 6 months lose compliance runway and cede first-mover cost advantage.

---

### CHAPTER 01 · THE MARKET

## $155B Opportunity, $3.4B in VC Raised Through Q3 2025 Alone

- **$155B** — annual revenue opportunity in healthcare services AI agents (PitchBook Q4 2025)
- **$300B+** — administrative waste addressable by AI agents in U.S. healthcare
- **$50–80B** — outsourced revenue cycle (Sequoia, March 2026): "healthcare billing is almost pure intelligence… the rules are complex but they are rules"

> "Companies doing so will be able to start tapping into labor budgets vs. IT budgets — an order of magnitude more scale."
> <cite>a16z Big Ideas in Tech 2025</cite>

---

### CHAPTER 02 · THE EXAMPLE

## How a PA Agent Cuts 163 Questions to a 48-Hour Approval

**PrescriberPoint deployment — weight management practice, 1,289 PA submissions:**

<div class="step-row"><div class="step-num">01</div><div class="step-text"><span class="step-bold">Auth check:</span> Agent queries payer via HL7 FHIR — "Is PA required for this script?"</div></div>
<div class="step-row"><div class="step-num">02</div><div class="step-text"><span class="step-bold">Doc scoping:</span> Retrieves payer-specific documentation requirements in real time.</div></div>
<div class="step-row"><div class="step-num">03</div><div class="step-text"><span class="step-bold">Auto-population:</span> Reads clinical records, answers up to <strong>163 payer questions</strong> without clinician input.</div></div>
<div class="step-row"><div class="step-num">04</div><div class="step-text"><span class="step-bold">Confidence routing:</span> High-confidence cases auto-submit. Complex cases escalate with full reasoning intact.</div></div>
<div class="step-row"><div class="step-num">05</div><div class="step-text"><span class="step-bold">Result:</span> <strong>94.5% clinician acceptance rate.</strong> Therapy initiation in <strong>48 hours</strong> vs. weeks.</div></div>

---

### CHAPTER 02 · DESIGN PATTERN

## "Auto-Approve, Never Auto-Deny" Is the Governance Standard

<div class="cols">
  <div class="col">
    <div class="col-head">What the Agent Owns</div>
    <div class="col-title">Routine Approvals</div>
    <ul>
      <li>Eligibility verification via FHIR API</li>
      <li>Policy-to-ICD-10 matching (rules, not judgment)</li>
      <li>Documentation population from EHR records</li>
      <li>Auto-submission for high-confidence cases</li>
    </ul>
    <div class="col-tag">Agent-autonomous</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">What Humans Own</div>
    <div class="col-title">Denials & Edge Cases</div>
    <ul>
      <li>Clinical necessity disputes</li>
      <li>Novel or experimental treatments</li>
      <li>Appeals requiring narrative judgment</li>
      <li>Final sign-off on submitted PA</li>
    </ul>
    <div class="col-tag">Human-in-the-loop</div>
  </div>
</div>

*Innovaccer Galaxy UM: "only auto-approve, never auto-deny" — clinical oversight preserved, human bottleneck removed from routine approvals.*

---

### CHAPTER 03 · COMPETITIVE LANDSCAPE

## Three Companies Already at Enterprise Scale

| Company | Valuation | Key Metric | Edge |
|---|---|---|---|
| **Commure** | $7B | HCA ($100B biller) partner; self-improving overnight claims models | Full-stack: RCM + ambient doc + voice |
| **Abridge** | $5.3B | $117M ARR; 150+ health systems | Epic integration; a16z Series E |
| **Hippocratic AI** | $3.5B | 115M patient interactions; 0 safety issues | Safety architecture; 50 large health systems |
| **Anterior** | $64M raised | 90% PA workflow automation | Sequoia-backed; clinical AI brain across full health plan ops |
| **Autonomize AI** | Cigna-backed | 3 of 5 largest U.S. health enterprises in prod | 55% faster clinical reviews; pre-built governed agents |

---

### CHAPTER 04 · THE RISK

## Mirage PMF: Deploying a General LLM Is Not a PA Agent

The failure mode is not the AI — it is deploying without governance.

- **Wrong-patient chart entries** caused by hallucination = HIPAA breach event, not a UX bug. HHS now mandates AI be included in Security Risk Analyses.
- **48% of healthcare orgs have no AI approval process** (HIMSS 2025 survey). Pilots without audit trails create liability before they create savings.
- **General-purpose LLMs lack payer-specific FHIR integrations and clinical tuning.** Anterior embeds engineers and clinicians directly with customers for exactly this reason.

**The governance design pattern exists and is proven. Use it.**

---

### CHAPTER 04 · FRAMEWORK FIT

## GO — Prior Auth Is the Autopilot Wedge Sequoia Named by Name

<div class="cols">
  <div class="col">
    <div class="col-head">Copilot → Autopilot</div>
    <div class="col-title">Moving Fast</div>
    <ul>
      <li>Today: AI assists human PA reviewer</li>
      <li>2026: AI auto-approves; human reviews denials only</li>
      <li>2027: CMS ePA API mandate forces structured workflow</li>
    </ul>
    <div class="col-tag">Transition underway</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Intelligence Ratio</div>
    <div class="col-title">High Confidence</div>
    <ul>
      <li>Rules-based: ICD-10 codes + payer policy = deterministic</li>
      <li>Structured workflow: FHIR-auditable end-to-end</li>
      <li>Clinical judgment lives in the denial layer only</li>
    </ul>
    <div class="col-tag">High fit for automation</div>
  </div>
</div>

<div class="verdict">VERDICT: GO</div>

---

<!-- _class: lead -->

### NEXT ACTION

## CMO + VP Revenue Cycle: Decide by July 11

<div class="next-action">
  <div class="na-label">Named Owner · Date · Success Gate</div>
  <div class="na-text">
    Approve <strong>$200K pilot budget by July 11, 2026.</strong> Shortlist Anterior and Autonomize AI. Assign clinical informatics lead by July 18. Pilot close: September 30, 2026. Success gate: <strong>50%+ PA processing time reduction</strong> on pilot cohort — tracked against current baseline before kickoff.
  </div>
</div>

<div class="subtitle" style="margin-top:1.4em;">
  Rejected alternative: build in-house on a general LLM. 18-month timeline misses the 2027 CMS deadline and lacks payer FHIR integrations out of the box.
</div>
