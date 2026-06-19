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
               padding:1em 2em; margin:0; font-size:1.5rem; font-style:italic; color:#aeb8c7; }
  .cols { display:grid; grid-template-columns:1fr 1px 1fr; gap:0; align-items:stretch; margin-top:1em; }
  .col  { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
          padding:24px 28px; display:flex; flex-direction:column; gap:10px; }
  .col:first-child { border-radius:12px 0 0 12px; border-right:none; }
  .col:last-child  { border-radius:0 12px 12px 0; border-left:none; }
  .col-rule { background:linear-gradient(180deg,transparent,#2dd4bf 20%,#2dd4bf 80%,transparent); box-shadow:0 0 10px #2dd4bf; }
  .col-head { font-family:monospace; font-size:.68rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .col-title { font-size:1.3rem; font-weight:700; color:#eef2f7; margin:0; }
  .col ul li::before { color:#2dd4bf; }
  .col-tag { font-family:monospace; font-size:.68rem; letter-spacing:.14em; text-transform:uppercase;
             padding-top:12px; border-top:1px solid rgba(255,255,255,.09); margin-top:auto; }
  .col-tag.t { color:#2dd4bf; } .col-tag.m { color:#e879f9; } .col-tag.s { color:#38bdf8; }
  .kicker { font-family:monospace; font-size:.8rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .subtitle { color:#aeb8c7; line-height:1.6; font-size:1.1rem; max-width:52ch; }
  .pill { display:inline-block; font-family:monospace; font-size:.68rem; letter-spacing:.14em;
          text-transform:uppercase; padding:5px 14px; border:1px solid rgba(255,255,255,.09);
          border-radius:999px; color:#aeb8c7; margin:4px 6px 4px 0; }
  .pill.t{border-color:#2dd4bf;color:#2dd4bf;} .pill.s{border-color:#38bdf8;color:#38bdf8;} .pill.m{border-color:#e879f9;color:#e879f9;}
  .chip { display:inline-block; font-family:monospace; font-size:.68rem; letter-spacing:.14em;
          text-transform:uppercase; padding:5px 14px; border:1px solid #2dd4bf;
          border-radius:999px; color:#2dd4bf; margin:4px 6px 4px 0; }
  .stat-num { font-size:8rem; font-weight:800; letter-spacing:-.04em; line-height:1; text-align:center; color:#2dd4bf; }
  .stat-label { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase;
                color:#69748a; text-align:center; }
  .chapter-num { font-family:monospace; font-size:7rem; font-weight:800; line-height:1;
                 letter-spacing:-.04em; color:#2dd4bf; }
  table { width:100%; border-collapse:collapse; font-size:.85rem; margin-top:.8em; }
  th { font-family:monospace; font-size:.65rem; letter-spacing:.18em; text-transform:uppercase;
       color:#2dd4bf; border-bottom:1px solid rgba(45,212,191,.4); padding:8px 12px; text-align:left; }
  td { padding:8px 12px; border-bottom:1px solid rgba(255,255,255,.06); color:#eef2f7; }
  tr:last-child td { border-bottom:none; }
  .badge-replace { color:#2dd4bf; font-family:monospace; font-size:.7rem; font-weight:700; }
  .badge-keep    { color:#69748a; font-family:monospace; font-size:.7rem; }
  .badge-neg     { color:#f6b94b; font-family:monospace; font-size:.7rem; }
  .badge-audit   { color:#e879f9; font-family:monospace; font-size:.7rem; }
  .savings-big { font-size:2.4rem; font-weight:800; color:#2dd4bf; }
---

<!-- _class: lead -->

# SaaS Replacement Audit

<div class="kicker">Founder's Build Stack · Cost Intelligence</div>
<div class="subtitle">15 tools · $33,288/yr current spend · $29,500 in 3-year savings identified</div>

---

### CHAPTER 01 · THE PROBLEM

## You're renting infrastructure you should own

Most early-stage SaaS stacks carry 40–60% replaceable spend — tools doing jobs your own codebase could handle in a weekend sprint.

- Average Series A startup: **$2,500–$5,000/mo** in SaaS tools
- Of that, **30–45%** is replaceable with owned code in under 30 days
- The remainder: negotiable, consolidatable, or simply unaudited

> "You don't have a SaaS problem. You have a build-vs-buy decision you never made."

---

### CHAPTER 01 · THE STACK

## 15 tools audited · $2,774/mo

<div class="cols">
  <div class="col">
    <div class="col-head">Tools Reviewed</div>
    <div class="col-title">15 Tools</div>
    - Retool, Airtable, Zapier, Segment
    - Intercom, Datadog, Mixpanel, Postman
    - Loom, Notion, Linear, Calendly
    - Algolia, SendGrid, Typeform
    <div class="col-tag t">$33,288 / YR</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Verdict Distribution</div>
    <div class="col-title">5 Buckets</div>
    - REPLACE: 5 tools
    - KEEP: 4 tools
    - NEGOTIATE: 3 tools
    - CONSOLIDATE: 1 tool
    - AUDIT USAGE: 1 tool
    <div class="col-tag m">Action on 10 of 15</div>
  </div>
</div>

---

### CHAPTER 02 · CLASSIFICATION

## 5-Bucket Framework

<table>
  <tr><th>Bucket</th><th>Criteria</th><th>Tools</th></tr>
  <tr><td><span class="badge-replace">REPLACE</span></td><td>Build cost &lt; 3-yr SaaS AND complexity ≤ medium</td><td>Retool, Zapier, Airtable, Segment, Typeform</td></tr>
  <tr><td><span class="badge-keep">KEEP</span></td><td>Strategic, deeply integrated, or cheap enough to ignore</td><td>Algolia, Linear, Notion, Loom, Calendly</td></tr>
  <tr><td><span class="badge-neg">NEGOTIATE</span></td><td>Overpriced for usage; cheaper alternatives exist</td><td>Datadog, Intercom, SendGrid</td></tr>
  <tr><td><span class="badge-audit">CONSOLIDATE</span></td><td>Overlapping functionality with another tool</td><td>Mixpanel → drop, use Segment</td></tr>
  <tr><td><span class="badge-audit">AUDIT USAGE</span></td><td>Unclear if actively used; no clear owner</td><td>Postman (free tier likely enough)</td></tr>
</table>

---

### CHAPTER 02 · REPLACE CANDIDATES

## Top 3 by 3-Year Savings

<table>
  <tr><th>Rank</th><th>Tool</th><th>Annual SaaS</th><th>Build Cost</th><th>Break-even</th><th>3-Yr Savings</th></tr>
  <tr><td><strong>#1</strong></td><td>Retool</td><td>$7,200</td><td>$8,700</td><td>16.6 mo</td><td><strong style="color:#2dd4bf">$15,132</strong></td></tr>
  <tr><td><strong>#2</strong></td><td>Zapier</td><td>$2,388</td><td>$1,380</td><td>7.1 mo</td><td><strong style="color:#2dd4bf">$6,524</strong></td></tr>
  <tr><td><strong>#3</strong></td><td>Airtable</td><td>$2,880</td><td>$4,350</td><td>21.4 mo</td><td><strong style="color:#2dd4bf">$5,183</strong></td></tr>
</table>

Intercom reclassified → NEGOTIATE (build cost exceeds 3-yr SaaS at current complexity)

---

### CHAPTER 03 · REPLACEMENT PLAN 1

## Retool → Custom Next.js Admin Panel

<div class="cols">
  <div class="col">
    <div class="col-head">The Build</div>
    <div class="col-title">Next.js + Supabase + shadcn/ui</div>
    - User list + impersonation
    - Subscription management
    - NextAuth admin role guard
    - Deploy on existing Vercel project
    <div class="col-tag t">2 WEEKS · 1 ENGINEER</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">The Math</div>
    <div class="col-title">$15,132 saved over 3 years</div>
    - 3-yr SaaS cost: $23,832
    - Build cost: $8,700 one-time
    - Break-even: month 17
    - Hosting: $0 (existing Vercel)
    <div class="col-tag m">HIGHEST VALUE BUILD</div>
  </div>
</div>

---

### CHAPTER 03 · REPLACEMENT PLAN 2

## Zapier → n8n Self-Hosted

<div class="cols">
  <div class="col">
    <div class="col-head">The Migration</div>
    <div class="col-title">n8n on $5/mo Hetzner VPS</div>
    - Docker install: 1 hour
    - 10 zaps → n8n workflows: 3 days
    - 1-week parallel shadow run
    - Cancel Zapier on day 8
    <div class="col-tag t">3 DAYS · 0 NEW CODE</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">The Math</div>
    <div class="col-title">$6,524 saved over 3 years</div>
    - 3-yr SaaS cost: $7,904
    - Total migration cost: $1,380
    - Break-even: month 8
    - Fastest payback in the stack
    <div class="col-tag s">FASTEST WIN · 7.1 MO PAYBACK</div>
  </div>
</div>

---

### CHAPTER 03 · REPLACEMENT PLAN 3

## Airtable → Supabase CRM

<div class="cols">
  <div class="col">
    <div class="col-head">The Build</div>
    <div class="col-title">Supabase Schema + Admin Views</div>
    - contacts / companies / deals / activities tables
    - Pipeline view in the admin panel (synergistic with #1)
    - CSV import from Airtable export
    - RLS: sales team sees only their deals
    <div class="col-tag t">1 WEEK · SHARED WITH PLAN #1</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">The Math</div>
    <div class="col-title">$5,183 saved over 3 years</div>
    - 3-yr SaaS cost: $9,533
    - Build cost: $4,350 (→ $1,500 if done with Plan #1)
    - Break-even: month 22 (→ month 7 with shared scaffold)
    <div class="col-tag m">SYNERGISTIC WITH PLAN #1</div>
  </div>
</div>

---

### CHAPTER 04 · QUICK WINS

## Negotiate + Consolidate First (Months 1–3)

No code required. Pure negotiation and cancellation.

- **Postman** → downgrade to free tier · save **$588/yr**
- **Mixpanel** → cancel, use Segment data in Supabase queries · save **$1,068/yr**
- **Datadog** → push for SMB tier or migrate to Vercel observability · save **$1,476/yr**
- **Intercom** → benchmark Crisp, push for 20% reduction · save **$718/yr**
- **SendGrid** → migrate to Resend (5× cheaper) or negotiate · save est. **$600/yr**

<div class="stat-label">QUICK WIN TOTAL</div>
<div class="stat-num" style="font-size:4rem">$4,450<span style="font-size:2rem; color:#69748a">/yr</span></div>

---

### CHAPTER 05 · ROADMAP

## 12-Month Action Plan

<table>
  <tr><th>Month</th><th>Action</th><th>Tool</th><th>Annual Savings</th></tr>
  <tr><td>1</td><td>Audit + downgrade to free</td><td>Postman</td><td>$588</td></tr>
  <tr><td>1</td><td>Cancel (consolidate)</td><td>Mixpanel</td><td>$1,068</td></tr>
  <tr><td>2</td><td>Negotiate -20%</td><td>Intercom + Datadog</td><td>$2,194</td></tr>
  <tr><td>3–4</td><td>Migrate to n8n self-hosted</td><td>Zapier</td><td>$2,388</td></tr>
  <tr><td>4–7</td><td>Build custom admin panel</td><td>Retool</td><td>$7,200</td></tr>
  <tr><td>5–8</td><td>Build Supabase CRM (with #1)</td><td>Airtable</td><td>$2,880</td></tr>
  <tr><td>9–12</td><td>Build event pipeline</td><td>Segment</td><td>$1,440</td></tr>
</table>

---

### CHAPTER 06 · SUMMARY

## The Numbers

<div class="cols">
  <div class="col">
    <div class="col-head">Before</div>
    <div class="col-title">$33,288 / year</div>
    - 15 tools, $2,774/mo
    - 5 redundant / replaceable
    - 3 overpriced
    - 1 possibly unused
    <div class="col-tag m">CURRENT STATE</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">After (Year 3)</div>
    <div class="col-title">$16,970 / year</div>
    - 3 tools replaced with owned code
    - 3 negotiated down
    - 1 consolidated, 1 cancelled
    - Stack is leaner + you own the moat
    <div class="col-tag t">$29,500 SAVED OVER 3 YEARS</div>
  </div>
</div>

---

<!-- _class: lead -->

# Start with Zapier.

<div class="kicker">Founder's Build Stack · Next Action</div>
<div class="subtitle">7.1-month payback. 3 days of work. n8n self-hosted on a $5/mo VPS. Ship it this week — then tackle Retool in month 4.</div>
