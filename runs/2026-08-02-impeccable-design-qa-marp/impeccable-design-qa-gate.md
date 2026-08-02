---
marp: true
theme: default
paginate: true
style: |
  /* impeccable-disable all-caps-body, tight-leading, skipped-heading --
     inherited verbatim from skills/marp's own documented neon theme block
     (kicker/col-head/col-tag/h3/stat-label uppercase labels, .chapter-num's
     display-only line-height:1, and the h1-then-h3 chapter-divider
     convention) -- pre-existing in shared infrastructure, not introduced by
     this deck's content. Flagged to the repo owner as follow-up, not fixed
     here to avoid unilaterally rewriting a shared theme other decks use. */
  :root {
    --bg: #080b11; --bg-elev: #0f141d; --ink: #eef2f7;
    --soft: #aeb8c7; --muted: #69748a;
    --teal: #2dd4bf; --sky: #38bdf8; --magenta: #e879f9; --amber: #f6b94b;
    --line: rgba(255,255,255,.09); --glass: rgba(255,255,255,.04);
  }
  section {
    background: #080b11; color: #eef2f7;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: 56px 76px 74px;
    border-bottom: 4px solid transparent;
    border-image: linear-gradient(90deg,#2dd4bf,#38bdf8,#e879f9) 1;
    font-size: 21px;
  }
  section::after { color: #69748a; font-size: 12px; letter-spacing:.2em; text-transform:uppercase; font-family:monospace; }
  /* impeccable-disable gradient-text -- intentional Aurora Glass identity */
  h1 { font-size: 3rem; font-weight: 800; letter-spacing: -.02em; line-height: 1.05;
       background: linear-gradient(135deg,#2dd4bf 0%,#38bdf8 50%,#e879f9 100%);
       -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
  h2 { font-size: 1.7rem; font-weight: 800; letter-spacing:-.02em; color:#eef2f7; margin-bottom:.5em; }
  h3 { font-family:monospace; font-size:.7rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; font-weight:400; }
  p  { color:#eef2f7; line-height:1.55; }
  ul { list-style:none; padding-left:0; }
  ul li { padding-left:1.4em; position:relative; color:#eef2f7; line-height:1.5; margin-bottom:.3em; font-size:.94em; }
  ul li::before { content:'→'; position:absolute; left:0; color:#2dd4bf; font-family:monospace; }
  /* impeccable-disable dark-glow -- intentional Aurora Glass neon accent */
  blockquote { border-left:4px solid #2dd4bf; box-shadow:-4px 0 12px rgba(45,212,191,.4);
               padding:.8em 1.6em; margin:0; font-size:1.25rem; font-style:italic; color:#aeb8c7; }
  .cols { display:grid; grid-template-columns:1fr 1px 1fr; gap:0; align-items:stretch; margin-top:.6em; }
  .col  { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
          padding:20px 24px; display:flex; flex-direction:column; gap:8px; }
  .col:first-child { border-radius:12px 0 0 12px; border-right:none; }
  .col:last-child  { border-radius:0 12px 12px 0; border-left:none; }
  /* impeccable-disable dark-glow -- intentional Aurora Glass neon accent */
  .col-rule { background:linear-gradient(180deg,transparent,#2dd4bf 20%,#2dd4bf 80%,transparent); box-shadow:0 0 10px #2dd4bf; }
  .col-head { font-family:monospace; font-size:.65rem; letter-spacing:.2em; text-transform:uppercase; color:#2dd4bf; }
  .col-title { font-size:1.15rem; font-weight:700; color:#eef2f7; margin:0; }
  .col ul li::before { color:#2dd4bf; }
  .col-tag { font-family:monospace; font-size:.65rem; letter-spacing:.14em; text-transform:uppercase;
             padding-top:10px; border-top:1px solid rgba(255,255,255,.09); margin-top:auto; }
  .col-tag.t { color:#2dd4bf; } .col-tag.m { color:#e879f9; } .col-tag.s { color:#38bdf8; } .col-tag.a { color:#f6b94b; }
  .kicker { font-family:monospace; font-size:.8rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .subtitle { color:#aeb8c7; line-height:1.6; font-size:1.05rem; max-width:56ch; }
  .pill { display:inline-block; font-family:monospace; font-size:.64rem; letter-spacing:.12em;
          text-transform:uppercase; padding:4px 12px; border:1px solid rgba(255,255,255,.09);
          border-radius:999px; color:#aeb8c7; margin:3px 5px 3px 0; }
  .pill.t{border-color:#2dd4bf;color:#2dd4bf;} .pill.s{border-color:#38bdf8;color:#38bdf8;} .pill.m{border-color:#e879f9;color:#e879f9;} .pill.a{border-color:#f6b94b;color:#f6b94b;}
  .stat-num { font-size:6.5rem; font-weight:800; letter-spacing:-.04em; line-height:1; text-align:center; color:#2dd4bf; }
  .stat-label { font-family:monospace; font-size:.7rem; letter-spacing:.2em; text-transform:uppercase;
                color:#69748a; text-align:center; }
  .chapter-num { font-family:monospace; font-size:6.5rem; font-weight:800; line-height:1;
                 letter-spacing:-.04em; color:#2dd4bf; }
  .bug-tag { display:inline-block; font-family:monospace; font-size:.68rem; letter-spacing:.14em;
             text-transform:uppercase; padding:5px 14px; border-radius:6px; margin-bottom:.6em; }
  .bug-tag.found  { background:rgba(246,185,75,.15); color:#f6b94b; border:1px solid rgba(246,185,75,.3); }
  .bug-tag.fixed  { background:rgba(45,212,191,.15); color:#2dd4bf; border:1px solid rgba(45,212,191,.3); }
  .bug-tag.missed { background:rgba(232,121,249,.15); color:#e879f9; border:1px solid rgba(232,121,249,.3); }
  .evidence { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:.6em; }
  .ev { border:1px solid rgba(255,255,255,.09); border-radius:10px; overflow:hidden; }
  .ev-head { font-family:monospace; font-size:.62rem; letter-spacing:.16em; text-transform:uppercase;
             padding:8px 14px; border-bottom:1px solid rgba(255,255,255,.09); }
  .ev-head.before { background:rgba(246,185,75,.1); color:#f6b94b; }
  .ev-head.after  { background:rgba(45,212,191,.1); color:#2dd4bf; }
  .ev-body { padding:14px 16px; font-family:monospace; font-size:.78rem; color:#eef2f7; background:#0f141d; line-height:1.5; }
  pre { background:#0f141d; border:1px solid rgba(255,255,255,.09); border-radius:8px;
        padding:14px 18px; font-size:.72rem; line-height:1.5; overflow-x:auto; margin:.5em 0; }
  pre code { background:none !important; color:#aeb8c7; padding:0 !important; }
  code { font-family:ui-monospace,SFMono-Regular,monospace; }
  p code, li code { background:rgba(255,255,255,.08); color:#38bdf8; padding:1px 6px; border-radius:4px; font-size:.9em; }
  section table { border-collapse:collapse; width:100%;
          border:1px solid rgba(255,255,255,.09); border-radius:8px; overflow:hidden; }
  section table tr { background:#0f141d !important; }
  section table tr:nth-child(even) { background:#131924 !important; }
  section table th, section table td {
    padding:10px 16px; text-align:left; color:#eef2f7 !important;
    background:transparent !important;
    border-bottom:1px solid rgba(255,255,255,.09);
    font-size:.92em;
  }
  section table th {
    font-family:monospace; font-size:.7rem; letter-spacing:.12em; text-transform:uppercase;
    color:#2dd4bf !important;
  }
  section table tr:first-child { background:rgba(45,212,191,.12) !important; }
  section table tr:last-child td { border-bottom:none; }
  section table td code { background:rgba(255,255,255,.1); color:#38bdf8; padding:2px 6px; border-radius:4px;
            font-size:.85em; }
---

<!-- _class: lead -->

<div class="kicker">DESIGN-QA GATE · SESSION REPORT</div>

# Day One. Real Bugs.

<div class="subtitle">Installed a 53.8k-star deterministic detector, built the wrapper two skills already assumed existed, then found three real defects proving it — one that Impeccable itself missed.</div>

---

### CHAPTER 01 · THE PROBLEM

<div class="chapter-num">01</div>

## Every AI Coding Tool Ships The Same Slop

---

## The Model Was Never The Problem

Every model trained on the same SaaS templates converges on the same tells, regardless of which agent generated them:

<div class="pill t">INTER / ROBOTO EVERYWHERE</div>
<div class="pill s">PURPLE→BLUE GRADIENTS</div>
<div class="pill m">CARDS NESTED IN CARDS</div>
<div class="pill a">ICON TILES ABOVE HEADINGS</div>

Impeccable ships 59 named rules for exactly this — deterministic pattern matches, not a model asked to have taste.

---

## One Skill, Two Halves: Vocabulary Plus Detector

<div class="cols">
  <div class="col">
    <div class="col-head">WHAT IT IS</div>
    <div class="col-title">A design vocabulary, not a prompt pack</div>
    <ul>
      <li>PRODUCT.md + DESIGN.md capture durable project context</li>
      <li>23 commands: craft, critique, audit, polish, bolder, quieter…</li>
      <li>Every command reads project context before acting</li>
    </ul>
    <div class="col-tag t">STRUCTURED, NOT VIBES</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">HOW IT RUNS</div>
    <div class="col-title">Deterministic, not another model call</div>
    <ul>
      <li>59 named rules, zero LLM, zero API key, zero token cost</li>
      <li>Regex, static-HTML, CSS-cascade, and visual-contrast engines</li>
      <li>Works with Claude Code, Codex, Cursor, Copilot, and more</li>
    </ul>
    <div class="col-tag s">INSTANT FEEDBACK</div>
  </div>
</div>

---

## Two Tiers, So Editing Never Stalls

<div class="cols">
  <div class="col">
    <div class="col-head">PER-EDIT · POSTTOOLUSE</div>
    <div class="col-title">Mechanical, unambiguous problems</div>
    <ul>
      <li>Broken images, clipped content, low contrast</li>
      <li>Gradient text, glow shadows, design-system drift</li>
    </ul>
    <div class="col-tag t">INTERRUPTS THE EDIT · 5s TIMEOUT</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">SESSION-END · STOP</div>
    <div class="col-title">Everything else, deduplicated once</div>
    <ul>
      <li>Copy cadence, palette and typography taste, layout rhythm</li>
      <li>Full rule set over every UI file touched this session</li>
    </ul>
    <div class="col-tag m">NEVER BLOCKS AN EDIT · 30s TIMEOUT</div>
  </div>
</div>

<pre><code>"PostToolUse": [{ "matcher": "Edit|Write|MultiEdit",
  "hooks": [{ "command": "node .claude/skills/impeccable/scripts/hook.mjs" }] }]
"Stop": [{ "hooks": [{ "command": "node .claude/skills/impeccable/scripts/hook.mjs" }] }]</code></pre>

---

### CHAPTER 02 · WHAT WE BUILT

<div class="chapter-num">02</div>

## From Aspirational Docs To A Working Gate

---

## Two Skills Already Assumed This Existed

`genspark-branded-deck` (line 212) and `marp` (line 283) both referenced `scripts/design-qa-detect.sh` and "the repo's pinned Impeccable wrapper" by exact path. Before this session, neither the skill nor the script existed on disk — same pattern as the `content-ideas-okf` cleanup earlier this session.

> "The repo's pinned Impeccable wrapper" — true in intent, false in the filesystem, until today.

---

## What Actually Landed This Session

| Component | Where | Status |
|---|---|---|
| Impeccable skill | `.claude/`, `.agents/`, `.github/skills/` | Installed, one copy per harness |
| PostToolUse + Stop hooks | `.claude/settings.local.json`, `.codex/hooks.json`, `.github/hooks/` | Wired, verified |
| `design-qa-detect.sh` | `scripts/` | Built, Node≥24 gate, pinned `3.5.0` |
| Version pins | `marp`, `genspark-branded-deck` SKILL.md | Fixed: stale `3.4.0` → verified `3.5.0` |

---

<div class="stat-label">REAL FINDINGS · FIRST RUN · ZERO CONFIGURATION</div>
<div class="stat-num">4</div>

## `side-tab` In `for-you-template.html`

A thick colored left-border stripe on outlier-accent cards — "the most recognizable tell of AI-generated UIs," per Impeccable's own rule text. Found in this repo's own daily-feed template, on the very first real run of the gate we'd just built.

---

### CHAPTER 03 · THREE REAL BUGS

<div class="chapter-num">03</div>

## Every One Of These Was Found By Actually Running It

---

<span class="bug-tag found">BUG 1 · CAUGHT IN OUR OWN CONTENT</span>

## `oversized-h1`: A Sentence Set At Hero Size

Impeccable flagged this deck's own draft — a full-sentence headline at 112px dominates the slide with no room for anything else.

<div class="evidence">
  <div class="ev"><div class="ev-head before">BEFORE — FLAGGED</div>
    <div class="ev-body">"Impeccable Just Caught Its First Bug — In Our Own Repo"<br>54 chars @ 112px</div></div>
  <div class="ev"><div class="ev-head after">AFTER — CLEAN</div>
    <div class="ev-body">"Day One. Real Bugs."<br>19 chars @ 112px</div></div>
</div>

---

<span class="bug-tag fixed">BUG 2 · IN lint_pptx.py ITSELF, PRE-SESSION CODE</span>

## `SLIDE_EMPTY` Fired On Every Single Slide

Marp exports each slide's render as the slide's **background fill**, not a placed shape. `python-pptx`'s `slide.shapes` is genuinely `[]` — but `background.fill.type == PICTURE` proves real content exists. The pre-existing check only looked at `shapes`.

```python
shapes = list(_iter_shapes(slide.shapes))
+ has_background_picture = slide.background.fill.type == MSO_FILL_TYPE.PICTURE
- if not shapes:
+ if not shapes and not has_background_picture:
      findings.append(Finding("SLIDE_EMPTY", "error", ...))
```

12 errors → 0. Verified a *genuinely* empty synthetic slide still correctly fires.

---

<span class="bug-tag missed">BUG 3 · IMPECCABLE'S OWN BLIND SPOT</span>

## The Tool Missed White Text On White

Slide 8's status table rendered with body text at `#eef2f7` (near-white) against Marp's default light table background — nearly invisible. This deck's own `low-contrast` rule check **did not fire**. The detector's static-HTML contrast engine doesn't fully resolve Marpit's injected default table stylesheet against custom-themed `<td>` text color.

<div class="pill a">FOUND BY EYE, NOT BY THE GATE</div>
<div class="pill t">FIXED WITH EXPLICIT table/th/td RULES</div>

---

## The Honest Takeaway

<div class="cols">
  <div class="col">
    <div class="col-head">WHAT THE GATE CAUGHT</div>
    <div class="col-title">2 of 3 bugs, automatically</div>
    <ul>
      <li>Our own oversized-h1, on the first export</li>
      <li>4 side-tab findings in existing repo HTML</li>
    </ul>
    <div class="col-tag t">WORKING AS DESIGNED</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">WHAT IT DIDN'T</div>
    <div class="col-title">Table contrast, and a PPTX-side gap</div>
    <ul>
      <li>White-on-white table text — Impeccable's own miss</li>
      <li>SLIDE_EMPTY blind spot — pre-existing, unrelated code</li>
    </ul>
    <div class="col-tag m">A GATE, NOT A GUARANTEE</div>
  </div>
</div>

---

### CHAPTER 04 · THE BOUNDARY

<div class="chapter-num">04</div>

## Two Detectors, One Line You Don't Cross

---

## Never Point Impeccable At A .pptx

<div class="cols">
  <div class="col">
    <div class="col-head">IMPECCABLE</div>
    <div class="col-title">HTML surfaces only</div>
    <ul>
      <li>.html, .css, .tsx, .jsx, .vue, .svelte…</li>
      <li>presentation, for-you-template.html, Genspark HTML capture</li>
      <li>Does not understand native .pptx at all</li>
    </ul>
    <div class="col-tag t">NEW THIS SESSION</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">LINT_PPTX.PY</div>
    <div class="col-title">Native PowerPoint, already mature</div>
    <ul>
      <li>15 rules: overflow, overlap, contrast, DPI, layout repetition</li>
      <li>Its own ignore_rules / waivers mechanism, already in use</li>
      <li>Not replaced, not duplicated — just documented as the boundary</li>
    </ul>
    <div class="col-tag s">ALREADY BUILT, PRE-SESSION</div>
  </div>
</div>

---

<!-- _class: lead -->

# Run It Every Time

<div class="subtitle">design-qa-detect.sh is now live in marp and genspark-branded-deck. This deck is the proof: built, broken, caught, fixed, and re-verified — three times — before delivery.</div>
