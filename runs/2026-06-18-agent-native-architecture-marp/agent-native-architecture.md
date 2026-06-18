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
  h2 { font-size: 2rem; font-weight: 800; letter-spacing:-.02em; color:#eef2f7; margin-bottom:.4em; }
  h3 { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; font-weight:400; margin-bottom:.3em; }
  p  { color:#eef2f7; line-height:1.6; max-width:64ch; }
  ul { list-style:none; padding-left:0; }
  ul li { padding-left:1.6em; position:relative; color:#eef2f7; line-height:1.6; margin-bottom:.4em; }
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
  .col ul li { font-size:.92rem; margin-bottom:.3em; }
  .col ul li::before { color:#2dd4bf; }
  .col ul li.neg::before { content:'✕'; color:#e879f9; }
  .col ul li.pos::before { content:'✓'; color:#2dd4bf; }
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
  .stat-wrap { text-align:center; margin:1.2em auto; }
  .stat-num { font-size:8rem; font-weight:800; letter-spacing:-.04em; line-height:1; color:#2dd4bf; display:block; }
  .stat-label { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:#69748a; display:block; margin-bottom:.4em; }
  .stat-sub { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; display:block; margin-top:.4em; }
  .chapter-num { font-family:monospace; font-size:7rem; font-weight:800; line-height:1;
                 letter-spacing:-.04em; color:#2dd4bf; display:block;
                 text-shadow: 0 0 40px rgba(45,212,191,.5); }
  .principle { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
               border-left:3px solid #2dd4bf; border-radius:0 8px 8px 0;
               padding:14px 20px; margin-bottom:12px; }
  .principle-num { font-family:monospace; font-size:.65rem; letter-spacing:.2em;
                   text-transform:uppercase; color:#2dd4bf; margin-bottom:4px; }
  .principle-title { font-size:1rem; font-weight:700; color:#eef2f7; margin:0; }
---

<!-- _class: lead -->

<div class="kicker">Systems Design · Agentic AI · 2025</div>

# The Agent-Native Shift

<div class="subtitle">Most AI projects bolt agents onto existing architectures. Agent-native design inverts the premise — agents are the primary user, and humans are the secondary interface.</div>

---

### Chapter 01 · The Core Distinction

## Bolt-on vs Agent-Native

The difference is not about capability — it is about **who the architecture assumes** will be operating it. Bolt-on AI wraps agents around human-shaped systems. Agent-native systems expose tool surfaces, observable state, and execution feedback as first-class contracts from day one.

<br>

<span class="pill m">Bolt-on: agents as plugins</span>
<span class="pill t">Agent-native: agents as operators</span>
<span class="pill s">Humans as secondary interface</span>

---

### Chapter 01 · The Core Distinction

## Bolt-on AI vs Agent-Native

<div class="cols">
  <div class="col">
    <div class="col-head">Traditional / Bolt-on</div>
    <div class="col-title">Agent as Plugin</div>
    <ul>
      <li class="neg">UI built for humans, agent scrapes it</li>
      <li class="neg">No structured tool surface — LLM guesses actions</li>
      <li class="neg">State is implicit, buried in session/DOM</li>
      <li class="neg">No execution feedback loop — agent flies blind</li>
      <li class="neg">Observability bolted on as an afterthought</li>
    </ul>
    <div class="col-tag m">Fragile. Opaque. Fails at scale.</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Agent-Native</div>
    <div class="col-title">Agent as Operator</div>
    <ul>
      <li class="pos">Structured tool surface with typed inputs/outputs</li>
      <li class="pos">Every action a human can take, an agent can take</li>
      <li class="pos">Observable state machine — agents read current state</li>
      <li class="pos">Execution feedback: success, failure, partial</li>
      <li class="pos">Observability built into the contract</li>
    </ul>
    <div class="col-tag t">Composable. Auditable. Scales.</div>
  </div>
</div>

---

### Chapter 01 · The Core Distinction

<div class="stat-wrap">
  <span class="stat-label">UI actions with no agent-callable equivalent</span>
  <span class="stat-num">~80%</span>
  <span class="stat-sub">In a typical enterprise app at first audit</span>
</div>

If a human can click it but an agent cannot call it, the system is not agent-native. The audit starts here: map every user action to a tool. Whatever has no tool equivalent is a gap.

---

<div style="font-family:monospace;font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:#69748a;">Chapter</div>
<div class="chapter-num">02</div>

## Five Principles of Agent-Native Design

---

### Chapter 02 · Design Principles

## The Five Principles

<div class="principle">
  <div class="principle-num">01</div>
  <div class="principle-title">Tool Parity — every human action has an agent-callable equivalent</div>
</div>
<div class="principle">
  <div class="principle-num">02</div>
  <div class="principle-title">Observable State — agents can read current system state without side effects</div>
</div>
<div class="principle">
  <div class="principle-num">03</div>
  <div class="principle-title">Structured Feedback — every tool call returns success, failure, or partial with reason</div>
</div>
<div class="principle">
  <div class="principle-num">04</div>
  <div class="principle-title">Idempotent Operations — retrying a tool call is safe; agents will retry on failure</div>
</div>
<div class="principle">
  <div class="principle-num">05</div>
  <div class="principle-title">Audit Trail — every agent action is logged, attributed, and reversible</div>
</div>

---

### Chapter 02 · Design Principles

## Human-in-Loop vs Agent-in-Loop

<div class="cols">
  <div class="col">
    <div class="col-head">Human-in-Loop (Legacy)</div>
    <div class="col-title">Agent assists human</div>
    <ul>
      <li>Agent suggests — human approves every step</li>
      <li>Bottleneck: human attention span</li>
      <li>Latency: human review time (hours to days)</li>
      <li class="pos">Good for: high-stakes irreversible decisions</li>
      <li class="neg">Bad for: high-volume, repetitive, time-sensitive work</li>
    </ul>
    <div class="col-tag s">Copilot model</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Agent-in-Loop (Native)</div>
    <div class="col-title">Human sets policy</div>
    <ul>
      <li>Agent executes — human reviews outcomes, not steps</li>
      <li>Bottleneck: tool surface quality</li>
      <li>Latency: milliseconds to seconds</li>
      <li class="pos">Good for: high-volume, well-defined, reversible work</li>
      <li class="neg">Bad for: novel judgment calls with no precedent</li>
    </ul>
    <div class="col-tag t">Autopilot model</div>
  </div>
</div>

---

### Chapter 02 · Design Principles

## The Tool Surface is the Architecture

In agent-native systems, the tool surface **is** the product. It is not an API layer built for developers — it is the primary interface through which all actors (human, agent, or orchestrator) interact with the system.

- Tools are typed, versioned, and documented like public APIs
- Tool schemas are the source of truth for what the system can do
- Human UIs are generated from tool definitions — not the other way around
- Agents can discover available tools at runtime via `tools/list`

<br>

<span class="pill t">MCP-compatible</span>
<span class="pill s">OpenAPI-backed</span>
<span class="pill">Tool-first design</span>

---

### Chapter 03 · Patterns

> "An agent-native architecture is one where removing the human from any workflow does not require changing the system — only changing the policy."

> <cite>Emerging pattern from Claude Code, OpenHands, and agentic framework design — 2025</cite>

---

<!-- _class: lead -->

<div class="kicker">The architecture is the policy</div>

# Design for Agents First. Humans Will Follow.

<div class="subtitle">Build tool surfaces, not UIs. Expose state, don't hide it. Make every action observable, structured, and reversible — and agents become operators on day one, not years from now.</div>

<br>

<span class="chip">Tool Parity</span>
<span class="chip">Observable State</span>
<span class="chip">Structured Feedback</span>
<span class="chip">Audit Trail</span>
