---
marp: true
theme: default
paginate: true
style: |
  section { background:#1b2838; color:#ecf0f1; font-family:ui-sans-serif,system-ui,sans-serif;
             padding:55px 75px 75px; border-bottom:4px solid #3498db; font-size:22px; }
  h1 { font-size:2.9rem; font-weight:800; color:#ffffff; letter-spacing:-.02em; line-height:1.1; }
  h2 { font-size:1.8rem; font-weight:800; color:#ffffff; margin-bottom:.35em; }
  h3 { font-family:monospace; font-size:.68rem; letter-spacing:.22em; text-transform:uppercase; color:#3498db; font-weight:400; margin-bottom:.25em; }
  p  { color:#ecf0f1; line-height:1.6; }
  ul { list-style:none; padding-left:0; margin-top:.4em; }
  ul li { padding-left:1.4em; position:relative; color:#ecf0f1; line-height:1.55; margin-bottom:.38em; }
  ul li::before { content:'→'; position:absolute; left:0; color:#3498db; font-family:monospace; }
  blockquote { border-left:4px solid #3498db; padding:.75em 1.6em; margin:.8em 0 0; font-size:1.25rem; font-style:italic; color:#bdc3c7; }
  section::after { color:#7f8c8d; font-size:12px; letter-spacing:.2em; text-transform:uppercase; font-family:monospace; }
  .kicker { font-family:monospace; font-size:.78rem; letter-spacing:.22em; text-transform:uppercase; color:#3498db; margin-bottom:.55em; }
  .subtitle { color:#bdc3c7; line-height:1.6; font-size:1.02rem; max-width:58ch; margin-top:.55em; }
  .cols { display:grid; grid-template-columns:1fr 1px 1fr; gap:0; align-items:stretch; margin-top:.75em; }
  .col  { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.10);
          padding:18px 22px; display:flex; flex-direction:column; gap:7px; }
  .col:first-child { border-radius:10px 0 0 10px; border-right:none; }
  .col:last-child  { border-radius:0 10px 10px 0; border-left:none; }
  .col-rule { background:linear-gradient(180deg,transparent,#3498db 20%,#3498db 80%,transparent); width:1px; }
  .col-head { font-family:monospace; font-size:.62rem; letter-spacing:.22em; text-transform:uppercase; color:#3498db; }
  .col-title { font-size:1.1rem; font-weight:700; color:#ffffff; margin:0; }
  .col ul li::before { color:#3498db; }
  .col-tag { font-family:monospace; font-size:.62rem; letter-spacing:.14em; text-transform:uppercase;
             padding-top:9px; border-top:1px solid rgba(255,255,255,.10); margin-top:auto; color:#3498db; }
  .stat-num { font-size:6.5rem; font-weight:800; letter-spacing:-.04em; line-height:1; text-align:left; color:#3498db; }
  .stat-label { font-family:monospace; font-size:.68rem; letter-spacing:.22em; text-transform:uppercase;
                color:#7f8c8d; margin-bottom:.35em; }
  .verdict { display:inline-block; font-family:monospace; font-size:.72rem; letter-spacing:.18em;
             text-transform:uppercase; padding:5px 16px; border:2px solid #2ecc71;
             border-radius:999px; color:#2ecc71; margin-top:.5em; }
  .step-row { display:grid; grid-template-columns:1.8rem 3.2rem 1fr; gap:0 .7rem; margin-bottom:.5em; align-items:start; }
  .step-n { font-family:monospace; font-size:.85rem; font-weight:800; color:#3498db; padding-top:.12em; }
  .step-tag { font-family:monospace; font-size:.58rem; letter-spacing:.1em; text-transform:uppercase;
              padding:2px 6px; border-radius:4px; font-weight:700; margin-top:.15em; display:inline-block; }
  .tc { background:rgba(52,152,219,.25); color:#5dade2; }
  .react { background:rgba(46,204,113,.2); color:#58d68d; }
  .ms { background:rgba(155,89,182,.25); color:#bb8fce; }
  .step-text { color:#ecf0f1; line-height:1.5; font-size:.95rem; }
  .step-bold { font-weight:700; color:#ffffff; }
  table { width:100%; border-collapse:collapse; margin-top:.55em; font-size:.82rem; }
  th { background:#2c3e50; color:#3498db; font-family:monospace; font-size:.62rem; letter-spacing:.15em; text-transform:uppercase; padding:7px 11px; text-align:left; border-bottom:2px solid #3498db; }
  td { padding:6px 11px; border-bottom:1px solid rgba(255,255,255,.08); color:#ecf0f1; vertical-align:top; }
  .pill { display:inline-block; font-family:monospace; font-size:.6rem; letter-spacing:.1em;
          text-transform:uppercase; padding:3px 10px; border-radius:999px; margin:2px 4px 2px 0; }
  .pill-blue { border:1px solid #3498db; color:#3498db; }
  .pill-green { border:1px solid #2ecc71; color:#2ecc71; }
  .pill-purple { border:1px solid #9b59b6; color:#bb8fce; }
  .code-block { background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12); border-radius:8px;
                padding:14px 18px; font-family:monospace; font-size:.8rem; color:#a8d8f0; line-height:1.7; margin-top:.6em; }
  .next-action { background:rgba(52,152,219,.1); border:1px solid #3498db; border-radius:10px; padding:20px 24px; margin-top:.9em; }
  .na-label { font-family:monospace; font-size:.62rem; letter-spacing:.22em; text-transform:uppercase; color:#3498db; margin-bottom:.35em; }
  .na-text { color:#ffffff; font-size:1.02rem; line-height:1.6; }
---

<!-- _class: lead -->

<div class="kicker">Financial Services · Agent Workflow · Case Study</div>

# Intelligent Loan Underwriting

<div class="subtitle">
All three agent patterns in one workflow. 5–7 business days → under 2 minutes. Upstart runs at 91% auto-approval. The pattern is repeatable across every FS decisioning use case.
</div>

---

### THE PROBLEM THIS SOLVES

## Manual Underwriting Has Four Failure Modes

- **Speed** — 5–7 business days for a decision. Borrowers abandon at 40%+ rates during the wait.
- **Inconsistency** — two underwriters review the same file and reach different risk tiers 30% of the time.
- **Cost** — $4,000–$7,000 average cost to originate one mortgage. 60–70% is manual labor.
- **Bias risk** — unstructured human judgment creates fair-lending exposure. Regulators require explainable decisions.

AI agents solve all four at once — speed through automation, consistency through deterministic rules, cost through labor displacement, explainability through step-by-step reasoning logs.

> "The billing layer is almost pure intelligence. The rules are complex but they are rules."
> <cite>Sequoia Capital, March 2026</cite>

---

### THE WORKFLOW

## 6 Stages, 3 Patterns, One Underwriting Decision

<div class="step-row">
  <div class="step-n">1</div>
  <div class="step-tag">—</div>
  <div class="step-text"><span class="step-bold">Application ingested.</span> Form data + document uploads parsed. Agent triggered.</div>
</div>
<div class="step-row">
  <div class="step-n">2</div>
  <div class="step-tag tc">TC</div>
  <div class="step-text"><span class="step-bold">Identity & KYC.</span> Agent calls Experian Identity API + OFAC sanctions screen. Pass/fail in &lt;5 sec.</div>
</div>
<div class="step-row">
  <div class="step-n">3</div>
  <div class="step-tag tc">TC</div>
  <div class="step-text"><span class="step-bold">Credit score pull.</span> Agent calls Equifax/TransUnion API. Fraud score appended (TrueAccord). Single round-trip.</div>
</div>
<div class="step-row">
  <div class="step-n">4</div>
  <div class="step-tag tc">TC</div>
  <div class="step-text"><span class="step-bold">Income verification.</span> Agent calls Plaid for bank data + Ocrolus for pay stub OCR. Employment confirmed.</div>
</div>
<div class="step-row">
  <div class="step-n">5</div>
  <div class="step-tag react">ReAct</div>
  <div class="step-text"><span class="step-bold">Document completeness loop.</span> Agent checks for gaps. If missing: Thought → request doc → Observation → loop. Exits when complete.</div>
</div>
<div class="step-row">
  <div class="step-n">6</div>
  <div class="step-tag ms">M-S</div>
  <div class="step-text"><span class="step-bold">Risk assessment chain.</span> Step 1: DTI calc → Step 2: risk tier → Step 3: policy rules → Step 4: rationale. Decision emitted.</div>
</div>

<span class="pill pill-blue">TC = Tool Calling</span> <span class="pill pill-green">ReAct = loop until complete</span> <span class="pill pill-purple">M-S = Multi-step Reasoning</span>

---

### PATTERN 1 OF 3 · TOOL CALLING

## Stages 2–4: Three Tool Calls, Three External Systems

<div class="cols">
  <div class="col">
    <div class="col-head">What the Agent Calls</div>
    <div class="col-title">The Tool Registry</div>
    <ul>
      <li><strong>Experian API</strong> — identity match + address history</li>
      <li><strong>OFAC Sanctions API</strong> — real-time watchlist screen</li>
      <li><strong>Equifax/TransUnion</strong> — FICO + tradeline pull</li>
      <li><strong>Plaid</strong> — 90-day bank transaction history</li>
      <li><strong>Ocrolus</strong> — pay stub + W-2 OCR, 99.6% accuracy</li>
      <li><strong>Fraud Score API</strong> — synthetic identity detection</li>
    </ul>
    <div class="col-tag">6 tools · parallel where possible</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Why Tool Calling, Not RAG</div>
    <div class="col-title">Live Data, Not Stored Knowledge</div>
    <ul>
      <li>Credit data is real-time — a cached answer from yesterday is wrong</li>
      <li>Bank balances change daily — Plaid gives the current view</li>
      <li>OFAC watchlist updates continuously — stale data = regulatory breach</li>
      <li>Each call returns structured JSON → deterministic parsing, no hallucination risk</li>
    </ul>
    <div class="col-tag">Structured output · auditable · no LLM hallucination on facts</div>
  </div>
</div>

---

### PATTERN 2 OF 3 · ReAct FRAMEWORK

## Stage 5: The Document Chase Loop in Practice

The agent cannot move to risk assessment if documents are incomplete. It cannot know upfront which documents are missing — it discovers that dynamically.

<div class="code-block">
THOUGHT: "Income verification requires 2 months of bank statements.
         Applicant uploaded 1. Missing: February statement."

ACTION:  send_document_request(
           applicant_id="A-8821",
           doc_type="bank_statement",
           month="2026-02",
           channel="email"
         )

OBSERVATION: Document received (2026-06-20 14:32 UTC). Re-checking completeness.

THOUGHT: "All required documents now present. Proceeding to risk assessment."
→ EXIT LOOP
</div>

Max iteration guard: **5 loops** before escalating to human underwriter.

---

### PATTERN 3 OF 3 · MULTI-STEP REASONING

## Stage 6: Four Chained Steps, One Explainable Decision

| Step | What it does | Example output |
|---|---|---|
| **1 · DTI Calculation** | Monthly debt obligations ÷ gross monthly income | DTI = 31% (threshold: 43%) |
| **2 · Risk Tier Assignment** | FICO + DTI + LTV → tier A/B/C/D/Decline | Tier B — standard terms |
| **3 · Policy Rule Application** | Lender rules: max LTV 80%, min FICO 620, debt ceiling | All rules: PASS |
| **4 · Rationale Generation** | Plain-English decision summary, audit log entry | "Approved: FICO 724, DTI 31%, LTV 72%. Tier B rate applied." |

Each step's output becomes the next step's input context. Step 4 is what regulators require for fair-lending audits — the model must show its work.

> Multi-step is the only pattern that produces an inherently explainable decision chain. ReAct produces a trace. Tool Calling produces a result. Multi-step produces a **reasoned argument**.

---

### WHO IS BUILDING THIS

## Five Companies, Five Proof Points

| Company | Pattern Used | Key Metric | What They Displaced |
|---|---|---|---|
| **Upstart** | Multi-step + Tool Calling | 91% auto-approval rate; 75% of decisions in &lt;1 min | Bank credit officers |
| **Zest AI** | Multi-step Reasoning | +15% approvals at same loss rate | FICO-only decisioning |
| **Blend** | Tool Calling orchestration | $3.5B/day loan volume through platform | Manual origination stack |
| **Ocrolus** | Tool Calling (doc AI) | 99.6% accuracy on pay stubs + bank statements | Human document reviewers |
| **Better.com** | ReAct + Tool Calling | 2-min decisions, 24/7 availability | Loan officer appointments |

The pattern: Tool Calling handles data retrieval. Multi-step handles the decision logic. ReAct handles the edge cases. All three must be wired together for a production underwriting agent.

---

### THE RESULTS

## From 5 Business Days to Under 2 Minutes

<div class="cols">
  <div class="col">
    <div class="col-head">Before Agent Workflow</div>
    <div class="col-title">Manual Underwriting</div>
    <ul>
      <li>5–7 business days to decision</li>
      <li>$4,000–$7,000 cost per mortgage originated</li>
      <li>30% inter-rater inconsistency</li>
      <li>40%+ borrower abandonment during wait</li>
      <li>Fair-lending audit: subjective, slow</li>
    </ul>
    <div class="col-tag">Status quo · 2020</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">After Agent Workflow</div>
    <div class="col-title">Automated Underwriting</div>
    <ul>
      <li><strong>&lt;2 minutes</strong> end-to-end for clean applications</li>
      <li><strong>60–70% cost reduction</strong> in origination labor</li>
      <li><strong>100% consistent</strong> — same rules, every time</li>
      <li><strong>91% auto-approval</strong> (Upstart, no human review)</li>
      <li>Step-by-step rationale log — regulator-ready</li>
    </ul>
    <div class="col-tag">Upstart / Better / Blend · 2026</div>
  </div>
</div>

---

### WHERE TO START

## The FS Team's Replication Playbook

The loan underwriting pattern is the template. Every FS decisioning workflow maps to the same three layers.

| Your use case | Tool Calling layer | ReAct layer | Multi-step layer |
|---|---|---|---|
| Trade surveillance | Market data API, news feed | Chase related entities | Pattern → anomaly → SAR decision |
| KYC onboarding | ID verify, sanctions screen | Chase missing docs | Risk tier → policy → approval |
| Credit card fraud | Transaction API, device signal | Flag chain investigation | Fraud score → block/allow |
| Wealth rebalancing | Portfolio API, market prices | Resolve data gaps | Drift calc → trade list → execute |

<div class="next-action">
  <div class="na-label">First Move</div>
  <div class="na-text">Pick the highest-volume manual decisioning process. Map its data sources to Tool Calls, its edge-case loops to ReAct, and its approval logic to Multi-step. That is your pilot scope.</div>
</div>

---

<!-- _class: lead -->

### TAKEAWAY

## The Pattern Is the Product

<div class="subtitle">
Tool Calling fetches the facts. ReAct handles what you cannot predict. Multi-step reasons to a defensible decision. Any FS workflow that touches data → loop → judgment can be automated with these three patterns — and every major lender is already doing it.
</div>
