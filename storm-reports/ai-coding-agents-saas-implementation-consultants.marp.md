---
marp: true
theme: corporate
paginate: true
style: |
  section { font-size: 22px; }
  section.lead { display:flex; flex-direction:column; justify-content:center; }
  section.lead h1 { font-size: 3.0rem; line-height: 1.05; }
  section.lead .subtitle { font-size: 1.08rem; max-width: 48ch; margin-top: 0.85rem; }
  h2 { font-size: 2rem; line-height: 1.08; }
  h3 { margin-bottom: 0.2rem; }
  p, li { line-height: 1.45; }
  ul { margin-top: 0.2rem; }
  blockquote { font-size: 1.45rem; }
  .kicker { font-family: monospace; font-size: 0.78rem; letter-spacing: 0.18em; text-transform: uppercase; opacity: .8; }
  .subtitle { color: #c9d4e1; line-height: 1.5; }
  .cols { display:grid; grid-template-columns:1fr 1px 1fr; gap:0; align-items:stretch; margin-top:1rem; }
  .col  { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.10); padding:22px 24px; display:flex; flex-direction:column; gap:10px; }
  .col:first-child { border-radius:12px 0 0 12px; border-right:none; }
  .col:last-child  { border-radius:0 12px 12px 0; border-left:none; }
  .col-rule { background:linear-gradient(180deg,transparent,#3498db 20%,#3498db 80%,transparent); }
  .col-head { font-family: monospace; font-size: .72rem; letter-spacing: .16em; text-transform: uppercase; color: #8ec8ff; }
  .col-title { font-size: 1.2rem; font-weight: 700; color: #fff; }
  .col-tag { font-family: monospace; font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; margin-top: auto; padding-top: 10px; border-top: 1px solid rgba(255,255,255,.10); }
  .tag-green { color: #8bffb5; }
  .tag-amber { color: #ffcf7a; }
  .tag-red { color: #ff9f9f; }
---

<!-- _class: lead -->
# AI coding agents will compress SaaS implementation work, not replace consultants
<div class="kicker">Storm research briefing</div>
<div class="subtitle">The strongest evidence points to a jagged frontier: agents help with bounded build tasks, but implementation value remains anchored in validation, accountability, adoption, and cutover risk.</div>

---

## The core bottleneck is accountability, not typing

- AI agents reduce the cost of producing code, configs, tests, and docs.
- SaaS implementations fail on semantics, permissions, integrations, data quality, and acceptance.
- The consultant’s durable job is to own whether the work is correct, safe, and deployable.

> The agent lowers artifact cost. The consultant owns outcome risk.

---

## The evidence points to a jagged frontier

<div class="cols">
  <div class="col">
    <div class="col-head">Where agents help</div>
    <div class="col-title">Bounded, testable, repetitive work</div>
    <ul>
      <li>Narrow coding tasks</li>
      <li>Migration scaffolds</li>
      <li>Test generation</li>
      <li>Documentation and triage</li>
    </ul>
    <div class="col-tag tag-green">High leverage</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Where agents stall</div>
    <div class="col-title">Mature, context-heavy implementations</div>
    <ul>
      <li>Business rule translation</li>
      <li>Security and governance</li>
      <li>UAT and rollback planning</li>
      <li>Stakeholder acceptance</li>
    </ul>
    <div class="col-tag tag-amber">Human gates stay</div>
  </div>
</div>

---

## The exposed work is the commodity layer

- First-pass configuration and integration glue are the easiest to automate.
- Straightforward API migrations are exposed.
- The remaining human value sits in semantics, exceptions, and sign-off.
- That means junior build hours shrink before senior advisory work does.

---

## The historical pattern is substitution at the edge, not wipeout

- CASE tools, 4GLs, ERP, RPA, and cloud self-service all reduced manual labor.
- None eliminated implementation work; they shifted it into modeling, governance, data migration, and operations.
- AI agents look similar, but faster and wider in scope.

---

## Leaders should repackage delivery now

1. Sell outcome ownership, not raw build hours.
2. Use agents for first-pass artifacts, not unbounded delivery ownership.
3. Build reusable implementation playbooks and validation packs.
4. Price for risk reduction, milestone certainty, and acceptance.
5. Train consultants as agent supervisors and business translators.

---

## The question that could change the answer is buyer tolerance

If buyers accept lighter human assurance, the consultant role shrinks faster. If regulated or high-stakes buyers keep demanding human accountability, the role changes more than it disappears.

---

<!-- _class: lead -->
# The consultant survives where someone must own the risk
<div class="kicker">Closing judgment</div>
<div class="subtitle">Agents will cut implementation cost, compress junior labor, and raise delivery speed. They do not remove the need for a human who can verify the work and stand behind the result.</div>
