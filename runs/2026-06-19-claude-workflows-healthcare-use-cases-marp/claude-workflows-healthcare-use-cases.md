---
marp: true
theme: default
paginate: true
style: |
  :root {
    --bg: #080b11; --bg-elev: #0f141d; --ink: #eef2f7;
    --soft: #aeb8c7; --muted: #69748a;
    --teal: #2dd4bf; --sky: #38bdf8; --magenta: #e879f9; --amber: #f6b94b;
    --line: rgba(255,255,255,.09); --glass: rgba(255,255,255,.04);
  }
  section {
    background: #080b11; color: #eef2f7;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: 60px 80px 80px;
    border-bottom: 4px solid transparent;
    border-image: linear-gradient(90deg,#2dd4bf,#38bdf8,#e879f9) 1;
    font-size: 22px;
  }
  section::after { color: #69748a; font-size: 12px; letter-spacing:.2em; text-transform:uppercase; font-family:monospace; }
  h1 { font-size: 3.2rem; font-weight: 800; letter-spacing: -.02em; line-height: 1.05;
       background: linear-gradient(135deg,#2dd4bf 0%,#38bdf8 50%,#e879f9 100%);
       -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
  h2 { font-size: 2rem; font-weight: 800; letter-spacing:-.02em; color:#eef2f7; }
  h3 { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; font-weight:400; }
  p  { color:#eef2f7; line-height:1.6; }
  ul { list-style:none; padding-left:0; }
  ul li { padding-left:1.4em; position:relative; color:#eef2f7; line-height:1.6; margin-bottom:.35em; }
  ul li::before { content:'→'; position:absolute; left:0; color:#2dd4bf; font-family:monospace; }
  blockquote { border-left:4px solid #2dd4bf; box-shadow:-4px 0 12px rgba(45,212,191,.4);
               padding:1em 2em; margin:0; font-size:1.45rem; font-style:italic; color:#aeb8c7; line-height:1.4; }
  blockquote p { color:#aeb8c7; max-width:100%; }
  blockquote cite { display:block; margin-top:.8em; font-family:monospace; font-size:.68rem;
                    letter-spacing:.2em; text-transform:uppercase; color:#69748a; font-style:normal; }
  .cols { display:grid; grid-template-columns:1fr 1px 1fr; gap:0; align-items:stretch; margin-top:1em; }
  .col  { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
          padding:24px 28px; display:flex; flex-direction:column; gap:10px; }
  .col:first-child { border-radius:12px 0 0 12px; border-right:none; }
  .col:last-child  { border-radius:0 12px 12px 0; border-left:none; }
  .col-rule { background:linear-gradient(180deg,transparent,#2dd4bf 20%,#2dd4bf 80%,transparent); box-shadow:0 0 10px #2dd4bf; }
  .col-head { font-family:monospace; font-size:.65rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; margin-bottom:4px; }
  .col-title { font-size:1.25rem; font-weight:700; color:#eef2f7; margin:0 0 8px; }
  .col ul { margin:0; }
  .col ul li { font-size:.9rem; margin-bottom:.3em; }
  .col-tag { font-family:monospace; font-size:.65rem; letter-spacing:.14em; text-transform:uppercase;
             padding-top:12px; border-top:1px solid rgba(255,255,255,.09); margin-top:auto; }
  .col-tag.t { color:#2dd4bf; } .col-tag.m { color:#e879f9; } .col-tag.s { color:#38bdf8; }
  .kicker { font-family:monospace; font-size:.8rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; margin-bottom:.5em; }
  .subtitle { color:#aeb8c7; line-height:1.65; font-size:1.1rem; max-width:56ch; margin-top:.5em; }
  .pill { display:inline-block; font-family:monospace; font-size:.68rem; letter-spacing:.14em;
          text-transform:uppercase; padding:5px 14px; border:1px solid rgba(255,255,255,.09);
          border-radius:999px; color:#aeb8c7; margin:4px 8px 4px 0; }
  .pill.t{border-color:#2dd4bf;color:#2dd4bf;} .pill.s{border-color:#38bdf8;color:#38bdf8;} .pill.m{border-color:#e879f9;color:#e879f9;}
  .chip { display:inline-block; font-family:monospace; font-size:.68rem; letter-spacing:.14em;
          text-transform:uppercase; padding:5px 14px; border:1px solid #2dd4bf;
          border-radius:999px; color:#2dd4bf; margin:4px 8px 4px 0; }
  .stat-num { font-size:7rem; font-weight:800; letter-spacing:-.04em; line-height:1; text-align:center; color:#2dd4bf; display:block;
              text-shadow: 0 0 40px rgba(45,212,191,.5); }
  .stat-label { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase;
                color:#69748a; text-align:center; display:block; margin-bottom:.3em; }
  .stat-sub { font-family:monospace; font-size:.72rem; letter-spacing:.18em; text-transform:uppercase;
              color:#2dd4bf; text-align:center; display:block; margin-top:.5em; }
  .chapter-num { font-family:monospace; font-size:7rem; font-weight:800; line-height:1;
                 letter-spacing:-.04em; color:#2dd4bf; display:block;
                 text-shadow: 0 0 40px rgba(45,212,191,.5); }
  .compliance-row { display:flex; align-items:baseline; gap:24px; padding:10px 0;
                    border-bottom:1px solid rgba(255,255,255,.09); }
  .compliance-row:last-child { border-bottom:none; }
  .c-badge { font-family:monospace; font-size:.65rem; letter-spacing:.14em; text-transform:uppercase;
             padding:4px 10px; border-radius:4px; background:rgba(45,212,191,.1);
             border:1px solid rgba(45,212,191,.3); color:#2dd4bf; white-space:nowrap; flex-shrink:0; min-width:120px; }
  .c-desc { font-size:.9rem; color:#eef2f7; line-height:1.45; }
---

<!-- _class: lead -->

<div class="kicker">Claude AI · Healthcare Workflow Automation · 2025</div>

# Claude in Healthcare

<div class="subtitle">Ten workflow use cases across providers, payers, and life sciences — where long-context AI eliminates the $950B administrative burden blocking clinical time.</div>

<br>

<span class="pill t">Providers</span>
<span class="pill s">Payers</span>
<span class="pill m">Life Sciences</span>
<span class="pill">HIPAA · CMS · FDA · ONC</span>

---

### Chapter 00 · The Constraint

## 35–55% of Physician Time Goes to Documentation, Not Care

Prior authorization alone consumes 13 hours per physician per week — forms, not care. Healthcare's core problem is not clinical capability. It is administrative throughput. That is exactly what Claude solves.

<br>

<span class="pill t">13 hrs/week on prior authorization</span>
<span class="pill s">35–55% EHR documentation burden</span>
<span class="pill m">$950B US healthcare admin spend</span>
<span class="pill">$500K+ cost per burned-out physician</span>

---

### Chapter 00 · Revenue at Risk

## US Healthcare Revenue Lost to Coding Errors

<div class="stat-label">Denied or underpaid claims annually — Change Healthcare 2023</div>
<div class="stat-num">$262B</div>
<div class="stat-sub">40–60% of denials overturned on appeal when properly documented</div>

Medical coding errors and improperly documented procedures flow directly to denied claims. 3–5% of provider revenue is lost to denials — and Claude automates the documentation that fixes them.

---

<div class="chapter-num">01</div>

## Provider Workflows

Four use cases that return physician time, reduce readmissions, and structure clinical data — all under HIPAA Business Associate Agreement coverage Anthropic provides for enterprise customers.

<br>

<span class="chip">Ambient Scribing</span>
<span class="chip">Prior Authorization</span>
<span class="chip">Discharge Summaries</span>
<span class="chip">Care Navigation</span>

---

### Chapter 01 · Provider Workflows

## The Two Biggest Time Sinks — Both Automatable

<div class="cols">
  <div class="col">
    <div class="col-head">Use Case 01</div>
    <div class="col-title">Clinical Documentation & Ambient Scribing</div>
    <ul>
      <li>Post-processes ASR transcripts into SOAP notes</li>
      <li>Extracts ICD-10 / CPT codes from visit content</li>
      <li>Flags spoken-plan vs documented-order discrepancies</li>
    </ul>
    <div class="col-tag t">$75K–$110K/yr per clinician recovered</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Use Case 02</div>
    <div class="col-title">Prior Authorization Automation</div>
    <ul>
      <li>Ingests clinical note + labs in one 200K-context pass</li>
      <li>Cross-references payer policy and drafts justification letter</li>
      <li>Eliminates 13 hrs/physician/week</li>
    </ul>
    <div class="col-tag s">$37K/physician/year recovered · CMS-9115-F Jan 2027</div>
  </div>
</div>

---

### Chapter 01 · Provider Workflows

## Poor Discharge Summaries Cost $26B in Preventable Readmissions

15% of patients are readmitted within 30 days — traceable to unclear instructions and medication reconciliation gaps. Claude generates patient-readable (≤6th grade) and PCP-readable handoff from the same inpatient chart, flagging every open medication and pending lab result automatically.

<br>

<span class="pill t">15% 30-day readmission rate nationally</span>
<span class="pill s">HL7 FHIR R4/R5 structured output</span>
<span class="pill m">2 outputs per chart · one ingest</span>

---

<div class="chapter-num">02</div>

## Payer Workflows

Revenue cycle integrity from coding to claim recovery. Claude's 200K context ingests the full patient encounter in one pass — surfacing missed diagnoses and automating denial appeals that succeed 40–60% of the time.

<br>

<span class="chip">Medical Coding</span>
<span class="chip">Revenue Cycle</span>
<span class="chip">Denial Management</span>
<span class="chip">Appeals Automation</span>

---

### Chapter 02 · Payer Workflows

## Revenue Recovery at Both Ends of the Claim Lifecycle

<div class="cols">
  <div class="col">
    <div class="col-head">Use Case 04</div>
    <div class="col-title">Medical Coding & Revenue Cycle</div>
    <ul>
      <li>Auto-suggests ICD-10 / CPT codes from clinical notes</li>
      <li>Identifies missed secondary diagnoses that increase reimbursement</li>
      <li>Addresses $262B/year in denied or underpaid claims</li>
    </ul>
    <div class="col-tag t">200K context · full encounter in one pass</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Use Case 05</div>
    <div class="col-title">Denial Management & Appeals</div>
    <ul>
      <li>Classifies denial by reason code (clinical / admin / auth)</li>
      <li>Drafts appeal citing CPT codes + clinical guidelines</li>
      <li>40–60% appeal success when properly documented</li>
    </ul>
    <div class="col-tag m">3–5% of provider revenue recoverable</div>
  </div>
</div>

---

<div class="chapter-num">03</div>

## Life Sciences Workflows

From trial recruitment to FDA submission packages. Claude compresses documentation timelines that cost $10–30M per NDA and take 12–18 months to author — with structured output that maps directly to regulatory schemas.

<br>

<span class="chip">Trial Eligibility</span>
<span class="chip">Pharmacovigilance</span>
<span class="chip">Regulatory Submissions</span>

---

### Chapter 03 · Life Sciences

## Accelerating the Drug Development Timeline

<div class="cols">
  <div class="col">
    <div class="col-head">Use Case 08</div>
    <div class="col-title">Clinical Trial Eligibility Screening</div>
    <ul>
      <li>Parses 30–100 inclusion/exclusion criteria per protocol</li>
      <li>Screens patient charts — structured match/no-match report</li>
      <li>Addresses 30% average trial under-enrollment</li>
    </ul>
    <div class="col-tag t">2–3× screening speed · TriNetX · Mendel.ai</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Use Case 09</div>
    <div class="col-title">Pharmacovigilance & Drug Safety</div>
    <ul>
      <li>Parses adverse event free text from EHR + call centers</li>
      <li>Extracts structured MedWatch 3500A fields automatically</li>
      <li>Classifies severity per ICH E2A — FDA 15-day window met</li>
    </ul>
    <div class="col-tag s">FDA AI/ML Action Plan 2024 · ICH E2A</div>
  </div>
</div>

---

### Chapter 04 · Compliance Framework

## Every Use Case Has a Governing Framework

<div class="compliance-row">
  <span class="c-badge">HIPAA BAA</span>
  <span class="c-desc">All PHI processing requires BAA — Anthropic provides enterprise coverage for Claude deployments.</span>
</div>
<div class="compliance-row">
  <span class="c-badge">CMS-9115-F</span>
  <span class="c-desc">Mandates electronic prior authorization by January 2027 — regulatory tailwind for PA automation.</span>
</div>
<div class="compliance-row">
  <span class="c-badge">CMS Info Block</span>
  <span class="c-desc">Requires patient-accessible summaries — Claude generates them at ≤6th grade reading level.</span>
</div>
<div class="compliance-row">
  <span class="c-badge">FDA AI/ML 2024</span>
  <span class="c-desc">Supports AI-assisted pharmacovigilance with human oversight.</span>
</div>
<div class="compliance-row">
  <span class="c-badge">ONC CDS Rules</span>
  <span class="c-desc">Explainability required for clinical AI — admin workflows (PA, coding, appeals) can fully automate.</span>
</div>

---

### Chapter 04 · Market Timing

> "The organizations that move from L2 (supervised) to L3 (delegated) automation in 2025–2026 will operate ahead of CMS mandate deadlines — not scrambling to comply with them."

> <cite>Healthcare AI Synthesis · Claude Workflow Use Cases Research · 2025</cite>

<br>

<span class="pill t">L2 Supervised — most enterprises today</span>
<span class="pill s">L3 Delegated — 2025–26 target</span>
<span class="pill m">L4 Autonomous — emerging in PA, coding</span>

---

<!-- _class: lead -->

<div class="kicker">The window is open now</div>

# Build for L3. The Mandate Clock Is Ticking.

<div class="subtitle">$950B in US healthcare administrative spend. CMS-9115-F enforcement arrives January 2027. Claude's 200K context, HIPAA BAA coverage, and structured output make it purpose-built for every workflow in this deck.</div>

<br>

<span class="chip">10 Use Cases</span>
<span class="chip">3 Segments</span>
<span class="chip">5 Compliance Frameworks</span>
