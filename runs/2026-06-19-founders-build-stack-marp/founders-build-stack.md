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
  ul li { padding-left:1.4em; position:relative; color:#eef2f7; line-height:1.6; margin-bottom:.35em; }
  ul li::before { content:'→'; position:absolute; left:0; color:#2dd4bf; font-family:monospace; }
  blockquote { border-left:4px solid #2dd4bf; box-shadow:-4px 0 12px rgba(45,212,191,.4);
               padding:1em 2em; margin:0; font-size:1.4rem; font-style:italic; color:#aeb8c7; }
  .cols { display:grid; grid-template-columns:1fr 1px 1fr; gap:0; align-items:stretch; margin-top:1em; }
  .col  { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
          padding:24px 28px; display:flex; flex-direction:column; gap:10px; }
  .col:first-child { border-radius:12px 0 0 12px; border-right:none; }
  .col:last-child  { border-radius:0 12px 12px 0; border-left:none; }
  .col-rule { background:linear-gradient(180deg,transparent,#2dd4bf 20%,#2dd4bf 80%,transparent); box-shadow:0 0 10px #2dd4bf; }
  .col-head { font-family:monospace; font-size:.68rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .col-title { font-size:1.3rem; font-weight:700; color:#eef2f7; margin:0; }
  .col-tag { font-family:monospace; font-size:.68rem; letter-spacing:.14em; text-transform:uppercase;
             padding-top:12px; border-top:1px solid rgba(255,255,255,.09); margin-top:auto; }
  .col-tag.t { color:#2dd4bf; } .col-tag.m { color:#e879f9; } .col-tag.s { color:#38bdf8; }
  .kicker { font-family:monospace; font-size:.8rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .subtitle { color:#aeb8c7; line-height:1.6; font-size:1.1rem; max-width:56ch; }
  .pill { display:inline-block; font-family:monospace; font-size:.68rem; letter-spacing:.14em;
          text-transform:uppercase; padding:5px 14px; border:1px solid rgba(255,255,255,.09);
          border-radius:999px; color:#aeb8c7; margin:4px 6px 4px 0; }
  .pill.t{border-color:#2dd4bf;color:#2dd4bf;} .pill.s{border-color:#38bdf8;color:#38bdf8;} .pill.m{border-color:#e879f9;color:#e879f9;}
  .stat-num { font-size:7rem; font-weight:800; letter-spacing:-.04em; line-height:1; text-align:center; color:#2dd4bf; }
  .stat-label { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase;
                color:#69748a; text-align:center; margin-top:.4em; }
  .chapter-num { font-family:monospace; font-size:6rem; font-weight:800; line-height:1;
                 letter-spacing:-.04em; color:#2dd4bf; }
  .timeline { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-top:1.2em; }
  .tblock { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
            border-radius:10px; padding:18px 20px; }
  .tblock-week { font-family:monospace; font-size:.65rem; letter-spacing:.2em; text-transform:uppercase; color:#2dd4bf; margin-bottom:8px; }
  .tblock-title { font-size:.95rem; font-weight:700; color:#eef2f7; margin-bottom:8px; }
  .tblock ul { margin:0; }
  .tblock ul li { font-size:.82rem; color:#aeb8c7; margin-bottom:.2em; }
  .tblock ul li::before { color:#69748a; }
  .stack-row { display:flex; gap:12px; flex-wrap:wrap; margin-top:1em; }
  .stack-chip { background:rgba(45,212,191,.08); border:1px solid rgba(45,212,191,.3);
                border-radius:8px; padding:10px 18px; font-family:monospace;
                font-size:.78rem; color:#2dd4bf; letter-spacing:.08em; }
  table { width:100%; border-collapse:collapse; font-size:.85rem; margin-top:.8em; }
  th { font-family:monospace; font-size:.65rem; letter-spacing:.18em; text-transform:uppercase;
       color:#2dd4bf; border-bottom:1px solid rgba(45,212,191,.4); padding:8px 12px; text-align:left; }
  td { padding:8px 12px; border-bottom:1px solid rgba(255,255,255,.06); color:#eef2f7; }
  tr:last-child td { border-bottom:none; }
  .score-bar { display:flex; align-items:center; gap:12px; margin:.4em 0; }
  .score-fill { height:6px; border-radius:3px; background:linear-gradient(90deg,#2dd4bf,#38bdf8); }
  .score-val { font-family:monospace; font-size:.75rem; color:#2dd4bf; min-width:2.5em; }
  code { background:rgba(255,255,255,.06); border-radius:4px; padding:2px 6px;
         font-family:monospace; font-size:.82em; color:#2dd4bf; }
---

<!-- _class: lead -->

# Freelance Designer<br>Client Portal

<div class="kicker">Founder's Build Stack · Product Brief · June 2026</div>
<div class="subtitle">From email chaos to a branded client experience — brief → feedback → invoice → paid. Built in 30 days on Next.js + Supabase + Stripe.</div>

---

### CHAPTER 01 · THE PROBLEM

## Freelancers run client work on duct tape

Every active project lives across 6 different tools — none of them built for this workflow.

- Client briefs arrive in email threads with no structure
- Deliverable feedback is scattered across Loom links, Slack DMs, PDF markups
- Invoices go out as manual Stripe payment links copy-pasted into Gmail
- The "system" is a folder of forwarded emails and a Notion page nobody reads

> "I spend 4 hours a week just tracking down approvals and chasing payments. That's a full billable day gone."

---

### CHAPTER 01 · THE MARKET

## The tools that exist are built for agencies, not solos

<div class="cols">
  <div class="col">
    <div class="col-head">Existing Options</div>
    <div class="col-title">HoneyBook · Dubsado · 17hats</div>
    - $200–$400/mo
    - Built for 5-person agencies
    - Onboarding takes a week
    - 80% of features unused by solos
    <div class="col-tag m">OVERKILL + OVERPRICED</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">The Gap</div>
    <div class="col-title">$29/mo · 3 features · done</div>
    - Brief intake
    - Deliverable feedback
    - Invoice + payment
    - Nothing else
    <div class="col-tag t">THE PRODUCT WE'RE BUILDING</div>
  </div>
</div>

---

### CHAPTER 02 · VALIDATION

## Problem Validator · 25 / 30 · VALIDATED

<div style="margin-top:1.2em">
  <div class="score-bar"><span style="min-width:10em;color:#aeb8c7;font-size:.9rem">Problem realness</span><div class="score-fill" style="width:54%"></div><span class="score-val">9/10</span></div>
  <div class="score-bar"><span style="min-width:10em;color:#aeb8c7;font-size:.9rem">Solution fit</span><div class="score-fill" style="width:48%"></div><span class="score-val">8/10</span></div>
  <div class="score-bar"><span style="min-width:10em;color:#aeb8c7;font-size:.9rem">Buying signal</span><div class="score-fill" style="width:48%"></div><span class="score-val">8/10</span></div>
</div>

- 3 named designers confirmed they would pay right now
- Existing alternatives (HoneyBook) solve the wrong problem at the wrong price
- Founder is a freelance designer — dog-fooding from day 1
- Distribution: Hexagon Slack + Dribbble Discord — trusted peer-to-peer channels

---

### CHAPTER 02 · ICP

## Ideal Customer · 93 / 100

<table>
  <tr><th>Criterion</th><th>Score</th><th>Profile</th></tr>
  <tr><td>Industry / vertical</td><td style="color:#2dd4bf">20/20</td><td>Solo freelance designer</td></tr>
  <tr><td>Company size + revenue</td><td style="color:#2dd4bf">18/20</td><td>1–2 person studio, $5K–$12K/mo</td></tr>
  <tr><td>Decision-maker</td><td style="color:#2dd4bf">15/15</td><td>They sign their own checks</td></tr>
  <tr><td>Trigger event</td><td style="color:#38bdf8">13/15</td><td>Just lost a client to messy comms OR just hit 8+ active clients</td></tr>
  <tr><td>Budget / WTP</td><td style="color:#38bdf8">13/15</td><td>Pays $29–49/mo if it saves 3+ hrs/week</td></tr>
  <tr><td>Cultural fit</td><td style="color:#2dd4bf">14/15</td><td>Uses Figma, Notion, Linear — early adopter</td></tr>
</table>

---

### CHAPTER 03 · SCOPE

## What ships in v1 · What doesn't

<div class="cols">
  <div class="col">
    <div class="col-head">TIER 1 · Ships Day 30</div>
    <div class="col-title">6 features</div>
    - Brief intake form (client fills)
    - Deliverable file upload
    - Client feedback on deliverables
    - Stripe invoicing + payment
    - Email notifications (Resend)
    - Designer dashboard + client magic-link
    <div class="col-tag t">FULL LOOP IN 30 DAYS</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">TIER 2 · Post-launch</div>
    <div class="col-title">Deferred</div>
    - Revision count tracking
    - Project timeline / Gantt view
    <div class="col-head" style="margin-top:1em">TIER 3 · Cut</div>
    <div class="col-title">Removed</div>
    - In-app chat (email handles it)
    <div class="col-tag m">SCOPE DISCIPLINE = ON-TIME SHIP</div>
  </div>
</div>

---

### CHAPTER 03 · BUILD VS BUY

## Only pay for what you can't build

<table>
  <tr><th>Component</th><th>Decision</th><th>Tool</th><th>Monthly Cost</th></tr>
  <tr><td>File storage</td><td style="color:#2dd4bf">BUILD</td><td>Supabase Storage</td><td style="color:#2dd4bf">$0</td></tr>
  <tr><td>Auth</td><td style="color:#2dd4bf">BUILD</td><td>Supabase Auth</td><td style="color:#2dd4bf">$0</td></tr>
  <tr><td>Email</td><td style="color:#38bdf8">BUY ($0)</td><td>Resend free tier</td><td style="color:#2dd4bf">$0</td></tr>
  <tr><td>Payments</td><td style="color:#38bdf8">BUY (no alt)</td><td>Stripe Connect Express</td><td>2.9% + 30¢</td></tr>
  <tr><td>Forms</td><td style="color:#2dd4bf">BUILD</td><td>Custom React (4hr)</td><td style="color:#2dd4bf">$0</td></tr>
  <tr><td>Database</td><td style="color:#2dd4bf">BUILD</td><td>Supabase Postgres</td><td style="color:#2dd4bf">$0</td></tr>
</table>

**Total infra cost for first 3 months: $0 + Stripe transaction fees**

---

### CHAPTER 04 · ARCHITECTURE

## Stack · Key Decisions

<div class="stack-row">
  <div class="stack-chip">Next.js 14 App Router</div>
  <div class="stack-chip">Supabase Postgres + Auth + Storage</div>
  <div class="stack-chip">Vercel</div>
  <div class="stack-chip">Stripe Connect Express</div>
  <div class="stack-chip">Resend</div>
</div>

<div style="margin-top:1.4em">

- **No client accounts** — magic token per project (link = access, zero signup friction)
- **Stripe Connect Express** — money flows directly to designer, no money transmitter risk
- **Signed URLs** — deliverable files private; client gets 1-hour URL via API only
- **Service role key server-only** — client components never touch privileged data
- **Append-only versioning** — upload v2, client sees v1 + v2 in sequence, no deletes

</div>

---

### CHAPTER 04 · DATA MODEL

## Schema in 5 tables

<table>
  <tr><th>Table</th><th>Key Columns</th><th>Notes</th></tr>
  <tr><td><code>designers</code></td><td>id, slug, stripe_account_id</td><td>Linked to Supabase Auth user</td></tr>
  <tr><td><code>projects</code></td><td>status, magic_token, client_email</td><td>Status machine: brief_pending → active → paid</td></tr>
  <tr><td><code>briefs</code></td><td>answers (jsonb)</td><td>Client fills; triggers designer notification</td></tr>
  <tr><td><code>deliverables</code></td><td>file_path, version</td><td>Supabase Storage; append-only</td></tr>
  <tr><td><code>feedback</code></td><td>comment, deliverable_id</td><td>Timestamped; linked to deliverable version</td></tr>
  <tr><td><code>invoices</code></td><td>amount_cents, status, stripe_payment_link</td><td>Idempotent webhook on paid</td></tr>
</table>

---

### CHAPTER 05 · ROADMAP

## 30 Days to Launch

<div class="timeline">
  <div class="tblock">
    <div class="tblock-week">Week 1 · Days 1–5</div>
    <div class="tblock-title">Foundation</div>
    <ul>
      <li>Supabase schema + RLS</li>
      <li>Auth + magic-link</li>
      <li>Brief intake form</li>
    </ul>
  </div>
  <div class="tblock">
    <div class="tblock-week">Week 2 · Days 6–12</div>
    <div class="tblock-title">Core Loop</div>
    <ul>
      <li>File upload (Storage)</li>
      <li>Feedback UI</li>
      <li>Designer dashboard</li>
    </ul>
  </div>
  <div class="tblock">
    <div class="tblock-week">Week 3 · Days 13–19</div>
    <div class="tblock-title">Revenue</div>
    <ul>
      <li>Stripe Connect Express</li>
      <li>Invoice creation</li>
      <li>Email notifications</li>
    </ul>
  </div>
  <div class="tblock">
    <div class="tblock-week">Week 4 · Days 20–30</div>
    <div class="tblock-title">Ship</div>
    <ul>
      <li>Mobile QA (375px)</li>
      <li>Prod deploy</li>
      <li>3 beta users onboarded</li>
    </ul>
  </div>
</div>

---

### CHAPTER 05 · CHECKPOINTS

## 5 Gates Between Idea and Launch

<div style="margin-top:.8em">

| Day | Gate | Pass Criteria |
|-----|------|---------------|
| 5 | Client access | Client receives magic link → views project page |
| 12 | Full loop | Brief → upload → feedback works end-to-end |
| 19 | Revenue | First real Stripe payment processed |
| 26 | Polish | All TIER1 features shipped, zero known blockers |
| 30 | Launch | 3 beta users onboarded, first invoice paid |

</div>

---

### CHAPTER 06 · GO-TO-MARKET

## How the first 10 customers arrive

- **Day 1:** Post in Hexagon Slack + Dribbble Discord — "built this for myself, want beta?"
- **Week 1:** Founder uses it on their own active client work — screenshot the experience
- **Week 2:** 3 beta users onboarded free — get raw feedback before charging
- **Week 4:** First paid plan activated ($29/mo) — use as social proof for wider launch
- **Month 2:** Product Hunt launch + "how I built this in 30 days" Twitter thread

> Distribution advantage: you're selling to your own community. Designers trust designers, not SaaS companies.

---

### CHAPTER 06 · REVENUE MODEL

## Simple. Predictable. Scalable.

<div class="cols">
  <div class="col">
    <div class="col-head">Pricing</div>
    <div class="col-title">$29/mo per designer</div>
    - Unlimited projects
    - Unlimited clients
    - All features included
    - No per-client seats
    <div class="col-tag t">$348 ARR PER CUSTOMER</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Milestones</div>
    <div class="col-title">Path to $10K MRR</div>
    - Month 1: 3 beta users (free)
    - Month 2: 10 paid ($290/mo)
    - Month 6: 50 paid ($1,450/mo)
    - Month 12: 350 paid ($10,150/mo)
    <div class="col-tag s">350 SOLO DESIGNERS = $10K MRR</div>
  </div>
</div>

---

### CHAPTER 07 · AI ROADMAP

## Two AI features queued for post-launch

- **Auto-invoice generator** — reads brief answers (scope, deadline, budget) → suggests invoice amount. Built with `/ai-feature-integrator`: Claude Haiku, <$0.001/call, rate-limited to 10/user/day
- **Feedback sentiment summary** — after client leaves comments, surfaces: "Client is happy with direction / has concerns about typography." Saves designer from reading 12 comments before a call

Both pass the 4-test gate: need AI ✅ · output verifiable ✅ · economics work ✅ · fallback defined ✅

---

<!-- _class: lead -->

# Ship it in 30 days.

<div class="kicker">Founder's Build Stack · Next Step</div>
<div class="subtitle">Schema is designed. Stack is chosen. First week's code is drafted. Day 1 starts with `npx create-next-app` and a Supabase project. The rest follows the plan.</div>
