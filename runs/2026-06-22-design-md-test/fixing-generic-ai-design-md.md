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
  .col ul { margin:6px 0 0; }
  .col ul li::before { color:#2dd4bf; }
  .col-rule { background:linear-gradient(180deg,transparent,#2dd4bf 20%,#2dd4bf 80%,transparent); box-shadow:0 0 10px #2dd4bf; }
  .col-head { font-family:monospace; font-size:.68rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .col-title { font-size:1.3rem; font-weight:700; color:#eef2f7; margin:0; }
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
---

<!-- _class: lead -->

<div class="kicker">Build log · 2026-06-22</div>

# Fixing the generic AI aesthetic with DESIGN.md

<div class="subtitle">One markdown file turned a default-looking app into an on-brand product — and we proved it on a live dashboard, charts and all.</div>

---

### The real diagnosis

## The model isn't the problem. Missing design context is.

Every AI-built UI converges on the same look:

- Same-looking cards
- Random gradients
- Inconsistent buttons
- Weak spacing
- "AI startup" sameness everywhere

The agent designs in a vacuum. Give it "make it modern" and it averages the internet.

---

### The fix

## DESIGN.md is design-as-text the agent reads first

A plain markdown file in the project root — Google Stitch's spec. Coding agents read `AGENTS.md` for *how to build*; design agents read `DESIGN.md` for *how it should look*.

- Color tokens — exact hex, not "a nice blue"
- Typography, spacing, components, states
- Hard do/don't guardrails that kill the slop

> "Instead of 'make it modern,' you hand the agent a system it can actually follow."

---

### The libraries

## Two catalogs exist. One is bigger; both are borrowed.

<div class="cols">
  <div class="col">
    <div class="col-head">getdesign.md</div>
    <div class="col-title">~75 ready files</div>
    <ul>
      <li>Built on MIT <code>awesome-design-md</code> (90k★)</li>
      <li>Public catalog is free</li>
      <li>Drop-in static DESIGN.md</li>
    </ul>
    <div class="col-tag t">FREE · SIMPLE</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Refero</div>
    <div class="col-title">2,000+ styles · 132k screens</div>
    <ul>
      <li>MCP studies real screens at build time</li>
      <li>Free <code>refero-design</code> skill (installed)</li>
      <li>Full library needs paid Pro</li>
    </ul>
    <div class="col-tag s">DEEPER · PRO-GATED</div>
  </div>
</div>

---

### The distinction that matters

## Owned beats borrowed for anything you ship

<div class="cols">
  <div class="col">
    <div class="col-head">Borrowed</div>
    <div class="col-title">Make it feel like Linear</div>
    <ul>
      <li>Great for inspiration</li>
      <li>Scraped from public sites</li>
      <li>Not a clone license</li>
    </ul>
    <div class="col-tag m">INSPIRATION ONLY</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Owned</div>
    <div class="col-title">Your identity, in your repo</div>
    <ul>
      <li>Safe for client work</li>
      <li>Slides + app share one token set</li>
      <li>Fixes the five symptoms</li>
    </ul>
    <div class="col-tag t">SHIP THIS</div>
  </div>
</div>

---

<!-- _class: lead -->

<div class="chapter-num">02</div>

## Does it actually hold? We tested it.

---

### Test one · synthetic

## One DESIGN.md held across four different surfaces

Dashboard, landing page, internal tool, and slide deck — built from the *same* `tokens.css` + `components.css`.

- Teal stayed the lone accent on every screen
- Glass cards on dark — zero white-on-grey
- Buttons, inputs, pills, tables byte-identical

<div class="chip">Different use cases</div><div class="chip">Identical identity</div><div class="chip">Test passed</div>

---

### Test two · the real app

## Before → after on the live Summit Realty dashboard

<div class="cols">
  <div class="col">
    <div class="col-head">Before</div>
    <div class="col-title">Generic light SaaS</div>
    <ul>
      <li>Light-gray canvas</li>
      <li>Indigo accent</li>
      <li>Looks like every AI demo</li>
    </ul>
    <div class="col-tag s">DEFAULT</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">After</div>
    <div class="col-title">One token remap</div>
    <ul>
      <li>Whole system flipped from one CSS edit</li>
      <li>Every variable-driven surface followed</li>
      <li>No component rewrites</li>
    </ul>
    <div class="col-tag t">DESIGN.md APPLIED</div>
  </div>
</div>

---

### The lesson that only the real app taught

## A restyle is 80% one edit — and 20% hunting the leaks

The token remap flips everything that *reads* the tokens. Two surfaces bypassed them and stayed light:

- **CopilotKit React UI** — ships its own light theme; override its `--copilot-kit-*` vars
- **Hardcoded `bg-white`** — utility colors that ignore the system

> "Hardcoded values and third-party themes are what keep the generic look alive."

---

### Any brand, same plumbing

## Rebranded to Summit Estate — and the charts proved it

Swapped Aurora Glass teal for warm charcoal + brushed gold. Same `:root` mechanism, a completely different identity — premium real-estate, not generic-AI.

<div class="cols">
  <div class="col">
    <div class="col-head">KPI cards</div>
    <div class="col-title">Gold figures, live data</div>
    <ul>
      <li>47 listings · 2.8% · $18.4M · 24 DOM</li>
    </ul>
    <div class="col-tag t">ON-BRAND</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Chart ramp</div>
    <div class="col-title">Earthy, not rainbow</div>
    <ul>
      <li>Gold · evergreen · slate · terracotta · sage</li>
    </ul>
    <div class="col-tag m">5-COLOR SYSTEM</div>
  </div>
</div>

---

### We wrote it down

## The lessons are codified, not buried in a chat

So the next session inherits them automatically:

- `marp` skill — "Design-system sync" links its themes to DESIGN.md
- Project `CLAUDE.md` — read DESIGN.md first; the CopilotKit leak rule
- Memory + GBrain — the owned-vs-borrowed workflow and resources

<div class="pill t">2 commits, 1 branch</div><div class="pill s">main untouched</div><div class="pill m">fully reversible</div>

---

<!-- _class: lead -->

<div class="kicker">The first move</div>

# Give the agent a system, not a vibe

<div class="subtitle">Drop a DESIGN.md in the repo root, map its tokens to your theme, and the "generic AI look" stops being the model's fault — because it finally has context to follow.</div>
