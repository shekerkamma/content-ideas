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
  ul li.neg::before { content:'✕'; color:#e879f9; }
  ul li.pos::before { content:'✓'; color:#2dd4bf; }
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
  .stat-wrap { text-align:center; margin:1em auto; }
  .stat-num { font-size:7rem; font-weight:800; letter-spacing:-.04em; line-height:1; color:#2dd4bf; display:block; }
  .stat-label { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:#69748a; display:block; margin-bottom:.3em; }
  .stat-sub { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; display:block; margin-top:.3em; }
  .chapter-num { font-family:monospace; font-size:7rem; font-weight:800; line-height:1;
                 letter-spacing:-.04em; color:#2dd4bf; display:block;
                 text-shadow: 0 0 40px rgba(45,212,191,.5); }
  .principle { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
               border-left:3px solid #2dd4bf; border-radius:0 8px 8px 0;
               padding:14px 20px; margin-bottom:10px; }
  .principle-num { font-family:monospace; font-size:.65rem; letter-spacing:.2em;
                   text-transform:uppercase; color:#2dd4bf; margin-bottom:4px; }
  .principle-title { font-size:.98rem; font-weight:700; color:#eef2f7; margin:0; }
  .level-row { display:flex; align-items:center; gap:16px; padding:10px 0;
               border-bottom:1px solid rgba(255,255,255,.06); }
  .level-badge { font-family:monospace; font-size:.65rem; letter-spacing:.14em; text-transform:uppercase;
                 padding:4px 10px; border-radius:4px; background:rgba(45,212,191,.12);
                 border:1px solid rgba(45,212,191,.3); color:#2dd4bf; white-space:nowrap; }
  .level-badge.active { background:rgba(45,212,191,.25); border-color:#2dd4bf; }
  .level-desc { font-size:.9rem; color:#aeb8c7; line-height:1.4; }
---

<!-- _class: lead -->

<div class="kicker">Agentic AI · Workflow Design · 2025</div>

# From Chains to Autonomous Loops

<div class="subtitle">How AI automation evolved from fixed prompt pipelines to self-correcting, tool-calling agents — and what that unlocks for enterprise automation at L3 and beyond.</div>

---

### Chapter 01 · The Structural Shift

## Chains are Brittle. Loops are Alive.

Prompt chains are deterministic pipelines — each step feeds the next. Reliable, debuggable, limited. Autonomous loops add a feedback cycle: **perceive → plan → act → observe → iterate**. The agent evaluates its own output and decides whether to continue, retry, or branch. This single addition changes everything about what AI can do.

<br>

<span class="pill m">Chains — predictable, brittle</span>
<span class="pill t">Loops — adaptive, self-correcting</span>
<span class="pill s">Feedback — the key ingredient</span>

---

### Chapter 01 · The Structural Shift

## Chain vs Loop: What Actually Differs

<div class="cols">
  <div class="col">
    <div class="col-head">Prompt Chain</div>
    <div class="col-title">Deterministic Pipeline</div>
    <ul>
      <li class="neg">Fixed step order — no branching</li>
      <li class="neg">No self-correction on failure</li>
      <li class="pos">Easy to debug (linear trace)</li>
      <li class="neg">Low ceiling — only designed-for tasks</li>
      <li class="neg">One failed step breaks everything</li>
    </ul>
    <div class="col-tag m">Predictable but fragile</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Autonomous Loop</div>
    <div class="col-title">Feedback-Driven Agent</div>
    <ul>
      <li class="pos">Dynamic step selection</li>
      <li class="pos">Self-correction via tool feedback</li>
      <li class="neg">Non-linear traces — harder to debug</li>
      <li class="pos">High ceiling — handles unanticipated problems</li>
      <li class="pos">Retries and branches on failure</li>
    </ul>
    <div class="col-tag t">Robust and adaptive</div>
  </div>
</div>

---

<div style="font-family:monospace;font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:#69748a;">Chapter</div>
<div class="chapter-num">01</div>

## The Four Loop Patterns

---

### Chapter 01 · Loop Patterns

## Four Patterns Practitioners Use

<div class="principle">
  <div class="principle-num">ReAct Loop</div>
  <div class="principle-title">Alternate reasoning trace + tool call. Dominant pattern in production. Best for retrieval-augmented tasks.</div>
</div>
<div class="principle">
  <div class="principle-num">Plan-and-Execute</div>
  <div class="principle-title">Produce a multi-step plan first, then execute. Reduces wasted tool calls on long-horizon tasks (>10 steps).</div>
</div>
<div class="principle">
  <div class="principle-num">Reflection Loop</div>
  <div class="principle-title">A critic agent evaluates each cycle's output; main agent revises. Higher quality, higher latency. Used in Reflexion, GPT-Researcher.</div>
</div>
<div class="principle">
  <div class="principle-num">Multi-Agent Orchestration</div>
  <div class="principle-title">Specialized agents own domains (research, coding, QA); orchestrator routes. Used in OpenHands, CIOS architecture.</div>
</div>

---

### Chapter 01 · Loop Patterns

## The Tool Surface is the Ceiling

The set of available tools **is** the agent's action space — nothing outside it is reachable. Tool calling connects agents to the real world: discrete, observable, reversible steps that power monitoring and rollback.

<br>

<div class="cols">
  <div class="col">
    <div class="col-head">Narrow tool set</div>
    <div class="col-title">search + summarize</div>
    <ul>
      <li>Retrieve and compress information</li>
      <li>Cannot write, execute, or commit</li>
    </ul>
    <div class="col-tag m">Information agent only</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Full tool set (MCP)</div>
    <div class="col-title">read · write · run · commit</div>
    <ul>
      <li>Read and modify files</li>
      <li>Execute code in sandboxed runtime</li>
      <li>Commit, test, deploy autonomously</li>
    </ul>
    <div class="col-tag t">Software engineering agent</div>
  </div>
</div>

---

<div style="font-family:monospace;font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:#69748a;">Chapter</div>
<div class="chapter-num">02</div>

## The Autonomy Spectrum

---

### Chapter 02 · Autonomy Spectrum

## Where Are Enterprises Today?

<div class="level-row">
  <span class="level-badge">L0 Manual</span>
  <span class="level-desc">LLM advises. Human does everything.</span>
</div>
<div class="level-row">
  <span class="level-badge">L1 Copilot</span>
  <span class="level-desc">LLM suggests. Human approves each step.</span>
</div>
<div class="level-row">
  <span class="level-badge active">L2 Supervised ◀ most enterprises</span>
  <span class="level-desc">LLM executes. Human reviews outcomes.</span>
</div>
<div class="level-row">
  <span class="level-badge active">L3 Delegated ◀ leading edge</span>
  <span class="level-desc">LLM handles task class. Human handles exceptions only.</span>
</div>
<div class="level-row">
  <span class="level-badge">L4 Autonomous</span>
  <span class="level-desc">LLM runs 24/7. Human sets policy. Emerging in software engineering.</span>
</div>

---

### Chapter 02 · Autonomy Spectrum

## The L3→L4 Gap Is Not Capability — It's Trust

Most enterprises have the tools to reach L4 today. What blocks them is **governance**, not capability. The gap between supervised and autonomous is a trust and observability problem: can the organization verify what the agent did, why, and roll back if needed?

<br>

<span class="pill t">Step budgets (max N tool calls)</span>
<span class="pill s">Reversibility gates (destructive ops need approval)</span>
<span class="pill">Checkpointing (rollback to any state)</span>
<span class="pill m">Structured traces (every action logged)</span>

---

### Chapter 03 · The Emerging Frontier

## Swarms and Event-Driven Agents

<div class="cols">
  <div class="col">
    <div class="col-head">Agent Swarms · A2A Protocol</div>
    <div class="col-title">Parallel intelligence</div>
    <ul>
      <li>Many lightweight agents on sub-problems</li>
      <li>Orchestrator merges results</li>
      <li>Horizontal scaling of cognition</li>
      <li class="pos">30-min task → 3 min across 10 agents</li>
    </ul>
    <div class="col-tag s">Google A2A · OpenAI Swarm</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Event-Driven Agents · Headless</div>
    <div class="col-title">Ambient automation</div>
    <ul>
      <li>Wake on webhook / schedule / queue</li>
      <li>Persistent memory across events</li>
      <li>No human prompt required</li>
      <li class="pos">True background automation at machine time</li>
    </ul>
    <div class="col-tag t">OpenHands headless · Claude Code remote</div>
  </div>
</div>

---

### Chapter 03 · The Emerging Frontier

> "The future of agentic AI is not conversational. It is ambient, event-driven, and operating at machine time."

> <cite>Synthesis from OpenHands, Claude Code remote sessions, and A2A protocol design — 2025</cite>

---

<!-- _class: lead -->

<div class="kicker">The loop is the product</div>

# Build Loops, Not Chains.

<div class="subtitle">Design for feedback, not sequence. Give agents tools, not scripts. Move from L2 to L3 by building observability in — not bolting it on after. The organizations that close the trust gap first will operate at machine speed.</div>

<br>

<span class="chip">ReAct · Plan-Execute · Reflection</span>
<span class="chip">MCP Tool Surface</span>
<span class="chip">L3 → L4 Autonomy</span>
