---
marp: true
theme: default
paginate: true
style: |
  :root {
    --bg: #080b11; --ink: #eef2f7; --soft: #aeb8c7; --muted: #69748a;
    --teal: #2dd4bf; --sky: #38bdf8; --magenta: #e879f9; --amber: #f6b94b; --red: #f87171;
  }
  section {
    background: #080b11; color: #eef2f7;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: 58px 78px 78px;
    border-bottom: 4px solid transparent;
    border-image: linear-gradient(90deg,#2dd4bf,#38bdf8,#e879f9) 1;
    font-size: 21px;
  }
  section::after { color: #69748a; font-size: 11px; letter-spacing:.2em; text-transform:uppercase; font-family:monospace; }
  h1 { font-size: 3.1rem; font-weight: 800; letter-spacing: -.025em; line-height: 1.05;
       background: linear-gradient(135deg,#2dd4bf 0%,#38bdf8 50%,#e879f9 100%);
       -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
  h2 { font-size: 1.9rem; font-weight: 800; letter-spacing:-.02em; color:#eef2f7; line-height:1.2; }
  h3 { font-family:monospace; font-size:.70rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; font-weight:400; margin-bottom:.3em; }
  p  { color:#eef2f7; line-height:1.6; }
  ul { list-style:none; padding-left:0; }
  ul li { padding-left:1.4em; position:relative; color:#eef2f7; line-height:1.55; margin-bottom:.32em; }
  ul li::before { content:'→'; position:absolute; left:0; color:#2dd4bf; font-family:monospace; }
  blockquote { border-left:4px solid #2dd4bf; box-shadow:-4px 0 12px rgba(45,212,191,.35);
               padding:.75em 1.6em; margin:.6em 0; font-size:1.25rem; font-style:italic; color:#aeb8c7; }
  blockquote cite { font-size:.78rem; font-style:normal; font-family:monospace; color:#69748a; display:block; margin-top:.4em; }
  .kicker { font-family:monospace; font-size:.78rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; margin-bottom:.5em; }
  .subtitle { color:#aeb8c7; line-height:1.65; font-size:1.05rem; max-width:58ch; margin-top:.55em; }
  .pill { display:inline-block; font-family:monospace; font-size:.66rem; letter-spacing:.14em;
          text-transform:uppercase; padding:4px 13px; border:1px solid rgba(255,255,255,.1);
          border-radius:999px; color:#aeb8c7; margin:3px 5px 3px 0; }
  .pill.t{border-color:#2dd4bf;color:#2dd4bf;} .pill.s{border-color:#38bdf8;color:#38bdf8;}
  .pill.m{border-color:#e879f9;color:#e879f9;} .pill.a{border-color:#f6b94b;color:#f6b94b;}
  .pill.r{border-color:#f87171;color:#f87171;}
  .cols { display:grid; grid-template-columns:1fr 1px 1fr; gap:0; align-items:stretch; margin-top:.85em; }
  .col  { background:rgba(255,255,255,.035); border:1px solid rgba(255,255,255,.09);
          padding:22px 26px; display:flex; flex-direction:column; gap:9px; }
  .col:first-child { border-radius:12px 0 0 12px; border-right:none; }
  .col:last-child  { border-radius:0 12px 12px 0; border-left:none; }
  .col-rule { background:linear-gradient(180deg,transparent,#2dd4bf 20%,#2dd4bf 80%,transparent); box-shadow:0 0 8px #2dd4bf; width:1px; }
  .col-head { font-family:monospace; font-size:.64rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .col-title { font-size:1.15rem; font-weight:700; color:#eef2f7; }
  .col ul li { font-size:.93rem; margin-bottom:.28em; }
  .col-tag { font-family:monospace; font-size:.64rem; letter-spacing:.14em; text-transform:uppercase;
             padding-top:10px; border-top:1px solid rgba(255,255,255,.09); margin-top:auto; }
  .col-tag.t{color:#2dd4bf;} .col-tag.m{color:#e879f9;} .col-tag.s{color:#38bdf8;}
  .stat-num { font-size:7rem; font-weight:800; letter-spacing:-.04em; line-height:1; color:#2dd4bf; }
  .stat-label { font-family:monospace; font-size:.7rem; letter-spacing:.22em; text-transform:uppercase; color:#69748a; }
  .chapter-num { font-family:monospace; font-size:6.5rem; font-weight:800; line-height:1; letter-spacing:-.04em; color:#2dd4bf; }
  .map-grid { display:grid; grid-template-columns:1fr auto 1fr; gap:0 1rem; align-items:center; margin-top:.9em; }
  .map-cell { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09); border-radius:9px; padding:13px 17px; }
  .map-cell.code { border-color:rgba(56,189,248,.3); }
  .map-cell.skill { border-color:rgba(45,212,191,.35); background:rgba(45,212,191,.07); }
  .map-label { font-family:monospace; font-size:.6rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:.25em; }
  .map-label.c { color:#38bdf8; } .map-label.s { color:#2dd4bf; }
  .map-name { font-weight:700; font-size:.98rem; color:#eef2f7; }
  .map-sub  { font-size:.82rem; color:#aeb8c7; margin-top:.15em; }
  .map-arrow { color:#2dd4bf; font-size:1.5rem; text-align:center; font-family:monospace; }
  .breach-row { display:grid; grid-template-columns:1fr 1fr 1fr; gap:13px; margin-top:.85em; }
  .breach-card { border:1px solid rgba(248,113,113,.3); border-radius:10px; padding:17px 19px; background:rgba(248,113,113,.05); }
  .breach-type { font-family:monospace; font-size:.62rem; letter-spacing:.2em; text-transform:uppercase; color:#f87171; margin-bottom:.3em; }
  .breach-title { font-weight:700; color:#fca5a5; font-size:1rem; margin-bottom:.35em; }
  .breach-body { font-size:.88rem; color:#aeb8c7; line-height:1.5; }
  .breach-stat { font-family:monospace; font-size:.72rem; letter-spacing:.12em; color:#f87171; margin-top:.55em; border-top:1px solid rgba(248,113,113,.2); padding-top:.45em; }
  .practice-block { background:rgba(255,255,255,.035); border:1px solid rgba(255,255,255,.09); border-radius:10px; padding:18px 22px; margin-bottom:.65em; }
  .practice-block.active { border-color:#2dd4bf; background:rgba(45,212,191,.08); }
  .pb-top { display:flex; align-items:baseline; gap:.75rem; margin-bottom:.4em; }
  .pb-n { font-family:monospace; font-size:1rem; font-weight:800; color:#2dd4bf; }
  .pb-head { font-weight:700; font-size:1.05rem; color:#eef2f7; }
  .pb-sub { font-size:.88rem; color:#aeb8c7; line-height:1.5; }
  .pb-tag { font-family:monospace; font-size:.6rem; letter-spacing:.18em; text-transform:uppercase; color:#2dd4bf; margin-top:.5em; }
  .timeline { display:flex; align-items:stretch; gap:0; margin-top:1em; }
  .tstep { flex:1; background:rgba(45,212,191,.07); border:1px solid rgba(45,212,191,.25); border-radius:8px;
           padding:14px 12px; text-align:center; }
  .tstep-n { font-family:monospace; font-size:.58rem; letter-spacing:.18em; text-transform:uppercase; color:#2dd4bf; }
  .tstep-label { font-size:.88rem; font-weight:700; color:#eef2f7; margin-top:.25em; }
  .tarrow { color:#2dd4bf; font-family:monospace; padding:0 5px; display:flex; align-items:center; font-size:1.1rem; }
  .verdict-box { background:rgba(45,212,191,.07); border:1px solid rgba(45,212,191,.4); border-radius:12px; padding:20px 26px; margin-top:1em; }
  .verdict-label { font-family:monospace; font-size:.64rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; margin-bottom:.3em; }
  .verdict-text { font-size:1.02rem; color:#eef2f7; line-height:1.6; }
  .chaos-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:13px; margin-top:.85em; }
  .chaos-card { border-radius:10px; padding:17px 19px; }
  .chaos-card.s1 { background:rgba(45,212,191,.07); border:1px solid rgba(45,212,191,.25); }
  .chaos-card.s2 { background:rgba(246,185,75,.07); border:1px solid rgba(246,185,75,.3); }
  .chaos-card.s3 { background:rgba(248,113,113,.06); border:1px solid rgba(248,113,113,.3); }
  .chaos-n { font-family:monospace; font-size:.6rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:.3em; }
  .chaos-n.s1{color:#2dd4bf;} .chaos-n.s2{color:#f6b94b;} .chaos-n.s3{color:#f87171;}
  .chaos-title { font-weight:700; font-size:1rem; margin-bottom:.35em; }
  .chaos-title.s1{color:#2dd4bf;} .chaos-title.s2{color:#f6b94b;} .chaos-title.s3{color:#fca5a5;}
  .chaos-body { font-size:.87rem; color:#aeb8c7; line-height:1.5; }
  .chaos-tag { font-family:monospace; font-size:.6rem; letter-spacing:.15em; text-transform:uppercase; margin-top:.55em; padding-top:.4em; border-top:1px solid rgba(255,255,255,.08); }
  .chaos-tag.s1{color:#2dd4bf;} .chaos-tag.s2{color:#f6b94b;} .chaos-tag.s3{color:#f87171;}
  .sl { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09); border-radius:9px; padding:11px 17px; display:flex; justify-content:space-between; align-items:center; margin-bottom:7px; }
  .sl.hl { background:rgba(45,212,191,.08); border-color:rgba(45,212,191,.5); }
  .sl-left { flex:1; }
  .sl-name { font-weight:700; font-size:.95rem; color:#eef2f7; }
  .sl-name.t { color:#2dd4bf; }
  .sl-desc { font-size:.81rem; color:#aeb8c7; margin-top:.1em; }
  .sl-badge { font-family:monospace; font-size:.58rem; letter-spacing:.14em; text-transform:uppercase; padding:3px 9px; border-radius:999px; flex-shrink:0; margin-left:12px; }
  .sl-badge.s { border:1px solid #38bdf8; color:#38bdf8; }
  .sl-badge.t { border:1px solid #2dd4bf; color:#2dd4bf; }
  .load-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:13px; margin-top:.85em; }
  .load-card { border-radius:10px; padding:20px 22px; }
  .load-card.a { background:rgba(56,189,248,.07); border:1px solid rgba(56,189,248,.3); }
  .load-card.b { background:rgba(45,212,191,.07); border:1px solid rgba(45,212,191,.3); }
  .load-card.c { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09); }
  .load-type { font-family:monospace; font-size:.62rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:.35em; }
  .load-type.a { color:#38bdf8; } .load-type.b { color:#2dd4bf; } .load-type.c { color:#69748a; }
  .load-title { font-weight:700; font-size:1rem; color:#eef2f7; margin-bottom:.35em; }
  .load-body { font-size:.9rem; color:#aeb8c7; line-height:1.55; }
  .load-tag { font-family:monospace; font-size:.6rem; letter-spacing:.14em; text-transform:uppercase; margin-top:.55em; padding-top:.4em; border-top:1px solid rgba(255,255,255,.08); }
  .load-tag.a { color:#38bdf8; } .load-tag.b { color:#2dd4bf; } .load-tag.c { color:#69748a; }
  .decay-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:13px; margin-top:.85em; }
  .decay-card { border:1px solid rgba(246,185,75,.3); border-radius:10px; padding:17px 19px; background:rgba(246,185,75,.06); }
  .decay-type { font-family:monospace; font-size:.62rem; letter-spacing:.2em; text-transform:uppercase; color:#f6b94b; margin-bottom:.3em; }
  .decay-title { font-weight:700; color:#fcd34d; font-size:1rem; margin-bottom:.35em; }
  .decay-body { font-size:.88rem; color:#aeb8c7; line-height:1.5; }
  .decay-stat { font-family:monospace; font-size:.72rem; letter-spacing:.12em; color:#f6b94b; margin-top:.55em; border-top:1px solid rgba(246,185,75,.2); padding-top:.45em; }
---

<!-- _class: lead -->

<div class="kicker">Engineering Rigor · Agent Development · 2026</div>

# Skills Are the<br>New Code

<div class="subtitle">
We spent 50 years making code safe to ship: lint it, test it, scan it, version it, observe it. Now agents run on skills — and we are applying none of that. The result is AI that drifts.
</div>

<div style="margin-top:1.4em;">
<span class="pill t">Guy Podjarny · Tessl · AI DevCon 2026</span>
</div>

---

### EXECUTIVE SUMMARY

## The Argument in One Page

<div class="cols" style="margin-top:.8em;">
  <div class="col">
    <div class="col-head">What changed</div>
    <div class="col-title">Agents run on context, not code</div>
    <ul>
      <li>Skills are reusable context that programs agent behaviour</li>
      <li>2M+ skills on GitHub — from ~zero at the start of 2026</li>
      <li>Most enterprise skills are unreviewed, untested, unversioned</li>
    </ul>
    <div class="col-tag t">The paradigm shifted. The practices haven't.</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">What must change</div>
    <div class="col-title">Apply 50 years of software engineering to skills</div>
    <ul>
      <li><strong>Lint</strong> before it loads — static analysis for skill files</li>
      <li><strong>Eval</strong> before it ships — evals are the new unit tests</li>
      <li><strong>Scan</strong> the supply chain — 16.9% of skills expose secrets</li>
      <li><strong>Version</strong> every change — skills compose; drift is compounding</li>
      <li><strong>Observe</strong> in production — runtime logs are your best eval data</li>
    </ul>
    <div class="col-tag m">The fix is not new. The urgency is.</div>
  </div>
</div>

---

### THE HISTORICAL PARALLEL

## We Solved This Before. It Took 30 Years.

Early software had no linters, no test suites, no package managers. Shipping meant copying files. Debugging meant guessing. Trust was personal, not systematic.

The practices we now call obvious — unit testing, static analysis, CI/CD, SCA — were each contested, slow to adopt, and justified only after enough production failures.

<div class="verdict-box">
<div class="verdict-label">The parallel</div>
<div class="verdict-text">Agent skills are where source code was in the early 1990s. No standard review gate. No reproducible test. No dependency inventory. The failures are already happening. The practices that fix them already exist.</div>
</div>

> "Within those skills are the new code, and we should treat them that way — and give them the right tools for it."
> <cite>Guy Podjarny, CEO Tessl · AI DevCon Spring 2026</cite>

---

### WHAT SKILLS ACTUALLY ARE

## Context Is What Programs the Model

Skills are not prompts. They are reusable, structured context that agents load on demand — the libraries of the agent era.

<div class="cols" style="margin-top:.85em;">
  <div class="col">
    <div class="col-head">What skills carry</div>
    <div class="col-title">The agent's institutional knowledge</div>
    <ul>
      <li><strong>Policies & practices</strong> — security rules, API design standards, coding conventions the team agreed on</li>
      <li><strong>Specs</strong> — definitions of what is being built, which APIs are available, what exists in the codebase</li>
      <li><strong>Workflows</strong> — how to do incident response, how to review code, step-by-step process context</li>
    </ul>
    <div class="col-tag t">Reusable · structured · loaded on demand</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Why this is code</div>
    <div class="col-title">Skills change what the model computes</div>
    <ul>
      <li>Context goes directly into the model's inference — it modifies the output</li>
      <li>A wrong skill causes wrong behaviour, exactly like a bug</li>
      <li>A missing skill causes missing capability, exactly like a missing function</li>
      <li>Skills compose: a skill can call tools, call other skills, trigger harnesses</li>
    </ul>
    <div class="col-tag m">If it can break an agent, it needs engineering rigour</div>
  </div>
</div>

---

### THE AGENT STACK · CHAPTERS 2 & 3

## The Stack Has Five Layers. Skills Sit in the Middle.

Tools extend what agents CAN do. Harnesses enforce what they WILL do. Skills program what they SHOULD do. Bad skills corrupt every layer above them.

<div class="sl"><div class="sl-left"><div class="sl-name">05 · Factory Lines</div><div class="sl-desc">Orchestration — how agents are triggered, routed, and run at production scale</div></div><span class="sl-badge s">Operate</span></div>
<div class="sl"><div class="sl-left"><div class="sl-name">04 · Harnesses</div><div class="sl-desc">Deterministic enforcement — output guards, rate limits, scope constraints that override agent judgment regardless of what any skill says</div></div><span class="sl-badge s">Constrain</span></div>
<div class="sl hl"><div class="sl-left"><div class="sl-name t">03 · Context & Skills &nbsp;← the programmable layer</div><div class="sl-desc">Reusable instructions that shape every decision the layers above take. The only layer humans actively author and maintain.</div></div><span class="sl-badge t">Programme</span></div>
<div class="sl"><div class="sl-left"><div class="sl-name">02 · Tools</div><div class="sl-desc">APIs and functions the model may call — structured, auditable access to external systems and data</div></div><span class="sl-badge s">Extend</span></div>
<div class="sl"><div class="sl-left"><div class="sl-name">01 · Models</div><div class="sl-desc">Base intelligence — swappable; the same skills must run reliably across model versions and vendors</div></div><span class="sl-badge s">Foundation</span></div>

---

### CONTEXT LOADING MODES · CHAPTER 4

## Not All Context Loads the Same

Context enters the agent through three gates. Each has a different failure mode.

<div class="load-grid">
<div class="load-card a">
<div class="load-type a">Rules</div>
<div class="load-title">Always loaded</div>
<div class="load-body">Pushed into every agent, every session, without exception — security policies, hard stops. The agent cannot opt out.</div>
<div class="load-tag a">Failure: stale rules silently govern everything</div>
</div>
<div class="load-card b">
<div class="load-type b">Skills</div>
<div class="load-title">Loaded on demand</div>
<div class="load-body">Triggered when the task matches. The programmable layer — most skill engineering effort lives here. Version contracts matter most here.</div>
<div class="load-tag b">Failure: wrong version loads; no one knows</div>
</div>
<div class="load-card c">
<div class="load-type c">Passive docs</div>
<div class="load-title">Discoverable</div>
<div class="load-body">Available but not pushed. The agent searches when it decides it needs them. Least governed, most likely out of date.</div>
<div class="load-tag c">Failure: agent finds and uses a deprecated doc</div>
</div>
</div>

> Skills are the only gate where "on demand" means version contracts matter — you cannot know which agent loads which version in which context without a registry.

---

### THE SCALE OF THE PROBLEM

## 2M+ Skills. No Quality Gate.

<div class="cols" style="margin-top:.85em;">
  <div class="col">
    <div class="col-head">Public ecosystem</div>
    <div class="stat-label">GitHub · June 2026</div>
    <div class="stat-num">2M+</div>
    <ul>
      <li>From approximately zero at the start of 2026</li>
      <li>Across 44,000+ public repositories</li>
      <li>Growth curve vertical — no sign of plateau</li>
    </ul>
    <div class="col-tag t">No standard lint, no test requirement, no security scan</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Inside the enterprise</div>
    <div class="col-title">Growing faster than public, governed less</div>
    <ul>
      <li>Teams write the same skill independently — six versions, none canonical</li>
      <li>No shared registry, no version contract between teams</li>
      <li>Skills conflict silently between agents built by different groups</li>
      <li>No way to audit what is loaded into which agent in production</li>
    </ul>
    <div class="col-tag m">Most skill action happens inside organisations, not in public</div>
  </div>
</div>

---

### HOW IT BREAKS

## Every Unengineered Codebase Eventually Collapses

A fast-growing unicorn — 1,699 engineers — attempted to scale skills across its agent platform.

<div class="chaos-grid" style="margin-top:.9em;">
<div class="chaos-card s1">
<div class="chaos-n s1">Stage 01</div>
<div class="chaos-title s1">Everyone builds their own</div>
<div class="chaos-body">Each team writes the skill they need. Fast, local, solves the immediate problem. Coordination overhead is zero.</div>
<div class="chaos-tag s1">VELOCITY · NO GOVERNANCE</div>
</div>
<div class="chaos-card s2">
<div class="chaos-n s2">Stage 02</div>
<div class="chaos-title s2">A shared repo is created</div>
<div class="chaos-body">Someone rationalises. PRs flood in from all teams. No review standard. No deprecation path. Forks diverge silently.</div>
<div class="chaos-tag s2">ORGANISED · BUT NOT GOVERNED</div>
</div>
<div class="chaos-card s3">
<div class="chaos-n s3">Stage 03</div>
<div class="chaos-title s3">It becomes a mess</div>
<div class="chaos-body">Duplicates everywhere. Cross-agent breakage. PRs stall — no one knows what is safe to change or delete.</div>
<div class="chaos-tag s3">DRIFT · TRUST BREAKDOWN</div>
</div>
</div>

This is not a people problem. It is the inevitable result of treating skills as afterthoughts — the same outcome early software teams hit before version control, code review, and CI existed.

---

### THE MAINTENANCE PROBLEM · CHAPTER 6

## Unmaintained Skills Don't Stay Neutral. They Instruct.

A forgotten skill is not a quiet artifact. It is an active instruction to every agent that loads it — until it is reviewed, updated, or explicitly removed.

<div class="decay-grid">
<div class="decay-card">
<div class="decay-type">Model drift</div>
<div class="decay-title">The model changed. The skill didn't.</div>
<div class="decay-body">A skill tuned for one model misfires on the next. Prompting patterns shift between versions. Instructions that once produced correct output now produce subtly wrong output. No one ran evals at upgrade time.</div>
<div class="decay-stat">Fix: gate every model upgrade with skill regression evals</div>
</div>
<div class="decay-card">
<div class="decay-type">Codebase drift</div>
<div class="decay-title">The API moved. The spec didn't.</div>
<div class="decay-body">A spec skill describing endpoints that were refactored six months ago tells the agent to call dead routes. The skill is factually wrong — and it loads confidently, every time.</div>
<div class="decay-stat">Fix: version skills with the codebase; same repo, same PR</div>
</div>
<div class="decay-card">
<div class="decay-type">Policy drift</div>
<div class="decay-title">The rule changed. The practice skill didn't.</div>
<div class="decay-body">A practices skill encoding last year's security policy leaves every agent running last year's rules. The team updated the handbook. The agent didn't get the memo.</div>
<div class="decay-stat">Fix: skills on a review cadence — not a "when broken" cadence</div>
</div>
</div>

---

### THE SECURITY REALITY

## Bad Skills Break Things. Malicious Skills Break Everything.

Skills are executed by the agent — with its full tool access. There is no sandbox between a skill and a production database.

<div class="breach-row" style="margin-top:.85em;">
<div class="breach-card">
<div class="breach-type">Malicious</div>
<div class="breach-title">Backdoor via skill</div>
<div class="breach-body">A ClawHub CLI skill installs a hidden backdoor during agent setup. The agent executes it without question — the skill said to.</div>
<div class="breach-stat">Supply chain attack vector · zero user intent required</div>
</div>
<div class="breach-card">
<div class="breach-type">Negligent</div>
<div class="breach-title">Scope never constrained</div>
<div class="breach-body">Replit agent wipes a production database following a skill whose destructive scope was never limited. No guardrail written. None enforced.</div>
<div class="breach-stat">$0 of damage if the skill had a scope constraint</div>
</div>
<div class="breach-card">
<div class="breach-type">Vulnerable</div>
<div class="breach-title">Secrets in plain text</div>
<div class="breach-body">16.9% of ClawHub skills expose API keys, credentials, or internal endpoints embedded directly in skill content.</div>
<div class="breach-stat">16.9% · ClawHub ecosystem audit · 2026</div>
</div>
</div>

---

<!-- _class: lead -->

<div class="chapter-num">→</div>

## The Code Analogy Is Exact

For every engineering practice we apply to code, there is a direct equivalent for skills. The tools differ. The discipline is identical.

<div style="margin-top:1.2em;">
<span class="pill t">Lint → Static analysis</span>
<span class="pill s">Test → Eval</span>
<span class="pill m">SCA → Skill scanning</span>
<span class="pill a">npm → Skill registry</span>
<span class="pill">APM → Skill observability</span>
</div>

---

### THE MAPPING · PRACTICE 01

## Lint Before It Loads

Static analysis for skills borrows directly from code tooling — the same vendors, applied one layer up.

<div class="map-grid" style="margin-top:.85em;">
<div class="map-cell code"><div class="map-label c">In code</div><div class="map-name">ESLint / Bit</div><div class="map-sub">Style, obvious bugs, formatting</div></div>
<div class="map-arrow">→</div>
<div class="map-cell skill"><div class="map-label s">In skills</div><div class="map-name">tessl lint</div><div class="map-sub">Shape, structure, format compliance</div></div>
</div>
<div class="map-grid">
<div class="map-cell code"><div class="map-label c">In code</div><div class="map-name">Snyk test</div><div class="map-sub">Security, dependency vulnerabilities</div></div>
<div class="map-arrow">→</div>
<div class="map-cell skill"><div class="map-label s">In skills</div><div class="map-name">snyk-review</div><div class="map-sub">Credential exposure, permission scope</div></div>
</div>
<div class="map-grid">
<div class="map-cell code"><div class="map-label c">In code</div><div class="map-name">CodeRabbit / PR review</div><div class="map-sub">Judgment, intent, correctness</div></div>
<div class="map-arrow">→</div>
<div class="map-cell skill"><div class="map-label s">In skills</div><div class="map-name">tessl-review</div><div class="map-sub">Pluggable model — "good skill" threshold</div></div>
</div>

---

### THE MAPPING · PRACTICE 02

## Eval Before It Ships

Tests prove code works. Evals prove skills work. The testing pyramid has a direct skills equivalent.

<div class="cols" style="margin-top:.85em;">
  <div class="col">
    <div class="col-head">Code testing pyramid</div>
    <div class="col-title">Deterministic pass/fail</div>
    <ul>
      <li><strong>Unit</strong> — one function, one behaviour</li>
      <li><strong>Integration</strong> — components working together</li>
      <li><strong>E2E</strong> — user-facing flow, end to end</li>
    </ul>
    <div class="col-tag s">Same input → same output, every time</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Skill eval pyramid</div>
    <div class="col-title">Probabilistic — scored, not binary</div>
    <ul>
      <li><strong>Skill evals</strong> — does this skill behave as intended under adversarial input?</li>
      <li><strong>Project evals</strong> — does it hold across codebases and contexts?</li>
      <li><strong>New model evals</strong> — does it survive the next model version?</li>
    </ul>
    <div class="col-tag t">Target score, confidence interval, regression detection</div>
  </div>
</div>

> "Tests prove code works. Evals prove skills work." The bar for shipping is the same. The measurement is different.

---

### THE MAPPING · PRACTICE 03 & 04

## Scan the Supply Chain. Version Every Change.

<div class="cols" style="margin-top:.85em;">
  <div class="col">
    <div class="col-head">Practice 03 · Security tooling</div>
    <div class="col-title">Three required layers</div>
    <ul>
      <li><strong>Static scan</strong> — secrets, scope, known-bad patterns before deploy</li>
      <li><strong>Dynamic test</strong> — red-team the skill at runtime; can it be jailbroken?</li>
      <li><strong>Supply chain audit</strong> — skills compose; a trusted skill may call an unreviewed one</li>
    </ul>
    <div class="col-tag m">Security is not a step. It is a layer at every stage.</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Practice 04 · Dependency management</div>
    <div class="col-title">npm, but for skills</div>
    <ul>
      <li><strong>Registry</strong> — discoverable, tagged, quality-rated</li>
      <li><strong>Version pinning</strong> — know exactly what is running in each agent</li>
      <li><strong>Install manifest</strong> — <code style="font-size:.8rem;color:#aeb8c7;">tessl install workspace/plugin-name</code></li>
      <li><strong>Compatibility contracts</strong> — cross-agent, cross-model guarantee</li>
    </ul>
    <div class="col-tag a">Dependency management is a pain. That is why it must be systematic.</div>
  </div>
</div>

---

### THE MAPPING · PRACTICE 05

## Observe in Production. Production Is Your Best Lab.

You can only get so far in the lab. Real behaviour happens when real agents meet real users.

<div class="cols" style="margin-top:.85em;">
  <div class="col">
    <div class="col-head">What to monitor</div>
    <div class="col-title">Three signal sources</div>
    <ul>
      <li><strong>Agent logs</strong> — where skills fail or misfire in practice</li>
      <li><strong>Recent PRs</strong> — repeated patterns that should become skills</li>
      <li><strong>Production logs</strong> — real-world behaviour and drift signals</li>
    </ul>
    <div class="col-tag t">Runtime signal converts lag indicators into leading ones</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">What observability unlocks</div>
    <div class="col-title">Maintenance becomes optimisation</div>
    <ul>
      <li>Real failures become eval test cases — the loop closes</li>
      <li>Log patterns surface skills that are missing or redundant</li>
      <li>Agent proposes updates, new skills, and removals automatically</li>
      <li>Without observability, drift is invisible until it causes an incident</li>
    </ul>
    <div class="col-tag s">Unmonitored skills drift. Observed skills improve.</div>
  </div>
</div>

---

### THE NEW LIFECYCLE

## Leave the SDLC to the Agents. Humans Own the CDL.

The software development lifecycle was built for code. A context development lifecycle is needed for skills.

<div class="timeline" style="margin-top:1em;">
<div class="tstep"><div class="tstep-n">01</div><div class="tstep-label">Generate</div></div>
<div class="tarrow">→</div>
<div class="tstep"><div class="tstep-n">02</div><div class="tstep-label">Evaluate</div></div>
<div class="tarrow">→</div>
<div class="tstep"><div class="tstep-n">03</div><div class="tstep-label">Optimise</div></div>
<div class="tarrow">→</div>
<div class="tstep"><div class="tstep-n">04</div><div class="tstep-label">Distribute</div></div>
<div class="tarrow">→</div>
<div class="tstep"><div class="tstep-n">05</div><div class="tstep-label">Consume</div></div>
<div class="tarrow">→</div>
<div class="tstep"><div class="tstep-n">06</div><div class="tstep-label">Observe</div></div>
<div class="tarrow">↻</div>
</div>

<div class="verdict-box" style="margin-top:.95em;">
<div class="verdict-label">What this changes</div>
<div class="verdict-text">Agents own implementation. Humans own the context that guides it. Every hour spent writing better skills compounds — a well-engineered skill improves every agent that loads it, every run it takes, across every model it will survive.</div>
</div>

---

<!-- _class: lead -->

<div class="kicker">The Verdict</div>

# Crafted With Intention.<br>Tested Against Reality.<br>Versioned With the Project.

<div class="subtitle">
Treating skills as an afterthought is not a shortcut. It is the difference between AI that ships and AI that drifts. The practices exist. The analogy is exact. The time to apply them is before the first incident, not after.
</div>

<div style="margin-top:1.5em;">
<span class="pill t">Lint before it loads</span>
<span class="pill s">Eval before it ships</span>
<span class="pill m">Scan the supply chain</span>
<span class="pill a">Version every change</span>
<span class="pill">Observe in production</span>
</div>
