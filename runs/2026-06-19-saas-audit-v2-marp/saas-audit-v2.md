---
marp: true
theme: default
paginate: true
style: |
  :root {
    --bg: #080b11; --bg-elev: #0f141d; --ink: #eef2f7;
    --soft: #aeb8c7; --muted: #69748a;
    --teal: #2dd4bf; --sky: #38bdf8; --magenta: #e879f9; --amber: #f6b94b;
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
  ul li { padding-left:1.4em; position:relative; color:#eef2f7; line-height:1.6; margin-bottom:.4em; }
  ul li::before { content:'→'; position:absolute; left:0; color:#2dd4bf; font-family:monospace; }
  blockquote { border-left:4px solid #2dd4bf; box-shadow:-4px 0 12px rgba(45,212,191,.4);
               padding:1em 2em; margin:0; font-size:1.35rem; font-style:italic; color:#aeb8c7; }
  .cols { display:grid; grid-template-columns:1fr 1px 1fr; gap:0; align-items:stretch; margin-top:1em; }
  .col  { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
          padding:24px 28px; display:flex; flex-direction:column; gap:8px; }
  .col:first-child { border-radius:12px 0 0 12px; border-right:none; }
  .col:last-child  { border-radius:0 12px 12px 0; border-left:none; }
  .col-rule { background:linear-gradient(180deg,transparent,#2dd4bf 20%,#2dd4bf 80%,transparent); }
  .col-head { font-family:monospace; font-size:.65rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .col-title { font-size:1.25rem; font-weight:700; color:#eef2f7; margin:0; }
  .col ul li { font-size:.9rem; }
  .col-tag { font-family:monospace; font-size:.65rem; letter-spacing:.14em; text-transform:uppercase;
             padding-top:10px; border-top:1px solid rgba(255,255,255,.09); margin-top:auto; }
  .col-tag.t { color:#2dd4bf; } .col-tag.m { color:#e879f9; } .col-tag.s { color:#38bdf8; } .col-tag.a { color:#f6b94b; }
  .kicker { font-family:monospace; font-size:.78rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .subtitle { color:#aeb8c7; line-height:1.65; font-size:1.1rem; max-width:58ch; }
  .stat-num { font-size:7rem; font-weight:800; letter-spacing:-.04em; line-height:1; text-align:center; color:#2dd4bf; }
  .stat-label { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:#69748a; text-align:center; margin-top:.3em; }
  table { width:100%; border-collapse:collapse; font-size:.82rem; margin-top:.8em; }
  th { font-family:monospace; font-size:.62rem; letter-spacing:.18em; text-transform:uppercase;
       color:#2dd4bf; border-bottom:1px solid rgba(45,212,191,.35); padding:8px 10px; text-align:left; }
  td { padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.05); color:#eef2f7; vertical-align:top; }
  tr:last-child td { border-bottom:none; }
  .verdict { font-family:monospace; font-weight:700; font-size:.78rem; }
  .v-replace { color:#2dd4bf; } .v-keep { color:#69748a; } .v-neg { color:#f6b94b; } .v-audit { color:#e879f9; } .v-cons { color:#38bdf8; }
  .math-box { background:rgba(45,212,191,.06); border:1px solid rgba(45,212,191,.2); border-radius:10px;
              padding:18px 22px; font-family:monospace; font-size:.82rem; color:#aeb8c7; line-height:1.8; margin-top:.8em; }
  .math-box .highlight { color:#2dd4bf; font-weight:700; }
  .savings { font-size:2rem; font-weight:800; color:#2dd4bf; }
---

<!-- _class: lead -->

# $30,500 is sitting<br>in your SaaS stack

<div class="kicker">SaaS Replacement Audit · 15 tools · $33,288/yr</div>
<div class="subtitle">$16,318 of your annual SaaS spend is replaceable or renegotiable. Here's the exit plan — month by month, with the math.</div>

---

### THE PROBLEM

## You're paying $1,360/mo for things you could own

Every month these tools renew, you're renting infrastructure that a weekend sprint could eliminate. The cost isn't just the invoice — it's the compounding: 10% price increases baked into every renewal, forever.

- Retool: $600/mo to display a table your engineers built in a day
- Zapier: $199/mo for 10 HTTP calls between services you own
- Airtable: $240/mo for a spreadsheet masquerading as a CRM
- Mixpanel: $89/mo for data you're already paying Segment to collect

> "You don't have a SaaS problem. You have a build-vs-buy decision you never made."

---

### 15 TOOLS · 5 VERDICTS

## Only 5 tools actually earn their invoice

<table>
  <tr><th>Tool</th><th>$/mo</th><th>Verdict</th><th>One-line reason</th></tr>
  <tr><td>Retool</td><td>$600</td><td><span class="verdict v-replace">REPLACE</span></td><td>Paying $600/mo to host a table with a search bar. Own it for $8,700 once.</td></tr>
  <tr><td>Airtable</td><td>$240</td><td><span class="verdict v-replace">REPLACE</span></td><td>Spreadsheet as CRM. A Supabase schema and an afternoon.</td></tr>
  <tr><td>Zapier</td><td>$199</td><td><span class="verdict v-replace">REPLACE</span></td><td>10 HTTP calls between services you own. n8n, $5/mo VPS, 3 days.</td></tr>
  <tr><td>Segment</td><td>$120</td><td><span class="verdict v-replace">REPLACE</span></td><td>200 lines of code + Supabase insert. You're paying $120/mo for a pipe.</td></tr>
  <tr><td>Typeform</td><td>$59</td><td><span class="verdict v-replace">REPLACE</span></td><td>50 lines of React and a Supabase insert. Nothing earns $59/mo here.</td></tr>
  <tr><td>Intercom</td><td>$299</td><td><span class="verdict v-neg">NEGOTIATE</span></td><td>Crisp exists at $25/mo. One call saves $718/yr.</td></tr>
  <tr><td>Datadog</td><td>$410</td><td><span class="verdict v-neg">NEGOTIATE</span></td><td>Vercel + Supabase covers 80% of what you're monitoring. Push for startup tier.</td></tr>
  <tr><td>Mixpanel</td><td>$89</td><td><span class="verdict v-cons">CONSOLIDATE</span></td><td>Paying twice for event tracking. Cancel this week — no migration needed.</td></tr>
  <tr><td>Algolia</td><td>$500</td><td><span class="verdict v-keep">KEEP</span></td><td>Search is core. Supabase FTS breaks at 50K rows. This one earns it.</td></tr>
</table>

---

### REPLACE · RANKED BY SAVINGS

## 3 builds. $26,839 back over 3 years.

<table>
  <tr><th>#</th><th>Replace</th><th>Annual SaaS</th><th>Build cost</th><th>Break-even</th><th>3-yr savings</th></tr>
  <tr>
    <td><strong>1</strong></td><td>Retool → Next.js admin panel</td>
    <td>$7,200</td><td>$8,700</td><td>Month 17</td>
    <td><strong style="color:#2dd4bf; font-size:1.1em">$15,132</strong></td>
  </tr>
  <tr>
    <td><strong>2</strong></td><td>Zapier → n8n self-hosted</td>
    <td>$2,388</td><td>$1,380</td><td><strong style="color:#2dd4bf">Month 8</strong></td>
    <td><strong style="color:#2dd4bf; font-size:1.1em">$6,524</strong></td>
  </tr>
  <tr>
    <td><strong>3</strong></td><td>Airtable → Supabase CRM</td>
    <td>$2,880</td><td>$4,350 → $1,500*</td><td>Month 22 → <strong style="color:#2dd4bf">Month 7*</strong></td>
    <td><strong style="color:#2dd4bf; font-size:1.1em">$5,183</strong></td>
  </tr>
</table>

*Build #3 alongside #1 — shared scaffold cuts $2,850 off the cost and moves break-even to month 7.

---

### THE MATH · BUILD #2

## Zapier → n8n: $6,524 back, break-even month 8

<div class="math-box">
3-Year SaaS:   $199 × 12 = $2,388  →  × 1.10 = $2,627  →  × 1.10 = $2,890  →  <span class="highlight">Total: $7,905</span>

Build cost:    n8n VPS ($5/mo × 36) = $180
               Migration (8hr × $150) = $1,200
               <span class="highlight">Total: $1,380</span>

Break-even:    $1,380 ÷ ($199 − $5/mo) = <span class="highlight">7.1 months</span>
After month 8: Zapier never touches your bank account again.
</div>

> "This is the fastest money in the stack. Three days of work. Ship it this week."

---

### THE MATH · BUILD #1

## Retool → Next.js admin panel: $15,132 back

<div class="math-box">
3-Year SaaS:   $600 × 12 = $7,200  →  × 1.10 = $7,920  →  × 1.10 = $8,712  →  <span class="highlight">Total: $23,832</span>

Build cost:    40hr × $150/hr = $6,000 one-time
               Maintenance (15%/yr × 3yr) = $2,700
               Hosting: $0 (existing Vercel deployment)
               <span class="highlight">Total: $8,700</span>

Break-even:    $8,700 ÷ ($600 − $75/mo maint) = <span class="highlight">Month 17</span>
After month 17: you own this forever.
</div>

Stack: Next.js 14 + Supabase RLS + shadcn/ui + NextAuth admin role · 2 weeks · 1 engineer

---

### BUILD PLAN #1

## What the Retool replacement actually ships

<div class="cols">
  <div class="col">
    <div class="col-head">What ships in 30 days</div>
    <div class="col-title">The 3 things CS actually uses</div>
    - User list — search, filter, impersonate
    - Subscription management — plan, status, cancel
    - Activity log — what they did, when
    <div class="col-tag t">NOT THE 10 RETOOL APPS. THE 3 THAT GET USED.</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Migration plan</div>
    <div class="col-title">4 steps, no data loss</div>
    - Audit: which Retool apps get opened weekly
    - Build: replicate those 2–3, nothing else
    - Shadow: run both for 2 weeks
    - Cancel: CS signs off → Retool gone
    <div class="col-tag m">DAY 1: AUDIT. MONTH 2: CANCEL.</div>
  </div>
</div>

---

### QUICK WINS · ZERO CODE

## $4,450/yr in this month — no engineers required

Five moves. Every one is a phone call, an email, or a click.

- **Cancel Mixpanel this week** — Segment already has this data. $1,068/yr gone immediately, no migration.
- **Downgrade Postman to free** — email support@postman.com. If someone objects, buy them one seat ($49/yr vs $588/yr). Save $539.
- **Call Intercom** — say Crisp costs $25/mo. They will negotiate. Target: $239/mo. Save $718/yr.
- **Call Datadog** — say you're evaluating Grafana Cloud. Target: 30% reduction. Save $1,476/yr.
- **Migrate to Resend** — or call SendGrid and threaten to. Save $600/yr either way.

<div class="stat-label">QUICK WIN TOTAL — NO CODE, THIS MONTH</div>
<div class="stat-num" style="font-size:3.5rem">$4,450<span style="font-size:1.8rem;color:#69748a">/yr</span></div>

---

### THE FULL PICTURE

## From $33,288 to $16,370 — in 12 months

<table>
  <tr><th>Month</th><th>The move</th><th>Tool</th><th>Saves</th></tr>
  <tr><td><strong>This week</strong></td><td>Cancel. No migration.</td><td>Mixpanel</td><td>$1,068/yr</td></tr>
  <tr><td><strong>Week 2</strong></td><td>One email to support.</td><td>Postman</td><td>$588/yr</td></tr>
  <tr><td><strong>Month 1</strong></td><td>One call each. Name the competitor price.</td><td>Intercom + Datadog</td><td>$2,194/yr</td></tr>
  <tr><td><strong>Months 2–3</strong></td><td>Migrate to n8n. 3 days. Fastest money here.</td><td>Zapier</td><td>$2,388/yr from mo 4</td></tr>
  <tr><td><strong>Months 3–7</strong></td><td>Build Next.js admin panel.</td><td>Retool</td><td>$7,200/yr from mo 8</td></tr>
  <tr><td><strong>Months 4–7</strong></td><td>Build Supabase CRM alongside it (shared scaffold).</td><td>Airtable</td><td>$2,880/yr from mo 8</td></tr>
  <tr><td><strong>Months 8–12</strong></td><td>Build event pipeline when admin panel ships.</td><td>Segment</td><td>$1,440/yr from mo 12</td></tr>
</table>

---

<!-- _class: lead -->

# Start with Zapier.<br>This week.

<div class="kicker">Next Action · SaaS Replacement Audit</div>
<div class="subtitle">3 days. $1,380 total cost. $6,524 back over 3 years. Break-even: month 8.<br>n8n on a $5/mo Hetzner VPS. One Docker command. The rest is just recreating HTTP calls you already own.</div>
