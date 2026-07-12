# Done-For-You AI Agent Micro-Agency — Solution Architecture

**Source signal:** Greg Isenberg × Nick (Orgo) — *"The $1M+ Solo AI Agent Business (Full Course)"* (watched 2026-06-28).
**Model:** one operator runs a control-plane agent that builds and manages per-client agents. Sell a *digital employee*, not an agent. **$5K–$10K / client / month**, flat.

Diagram: `solo-agent-agency-architecture.drawio` (editable) · `.drawio.png` · `.svg` · preview `.png`.

---

## Architecture at a glance

Seven layers, top → bottom = request → delivery → orchestration → runtime → capability → inference → reliability.

| # | Layer | Role | Key components |
|---|-------|------|----------------|
| ① | Clients & Channels | Where the executive reaches the agent | Telegram/WhatsApp/iMessage, Email, Voice (Limitless), Content (inbound) |
| ② | Delivery & Client Ops | Productized service surface | Trello (Kanban, capped requests), Granola→MCP, Loom, Calendly, Superhuman, Asana |
| ③ | **Control Plane** | Operator + one meta-agent that builds/runs the rest | You (Claude Code/Codex), **Orgo-Claw control agent**, Orgo MCP, setup-context MCPs |
| ④ | Per-Client Agent Runtime | Isolated cloud computer per client | Orgo workspaces, agent VMs (Hermes/OpenClaw), 1 connector → all |
| ⑤ | Agent Capabilities & Context | Installed into every agent | Composio (1 MCP→1000s apps + auth), Agent Mail, **Obsidian vault**, Skills/sub-agents |
| ⑥ | Model Router | Model-agnostic; swap on price/capability | GPT-5.5 (default), GLM-5.1/Kimi (cheap), Opus 4.7+Claude Code (long coding) |
| ⑦ | Reliability & Observability | The moat: fix before the client notices | Watchdog, alert emails, sandbox isolation, SLA + self-evolve |

---

## Primary data flows

1. **Request path (①→②→③→④):** Client drops a request (chat/email or a Trello card). Granola meeting notes auto-sync to Trello. Scoped work (1–2 reqs / 48h) reaches the control plane; the control agent provisions or reconfigures the client's VM via **Orgo MCP**.
2. **Execution path (④→⑤→⑥):** The client's agent VM uses Composio connectors + Agent Mail + its Obsidian context to do the work, calling the model router for inference.
3. **Reliability loop (④→⑦→③):** Runtime emits health/telemetry; a watchdog auto-restarts crashed gateways; on cron/skill failure the agent **emails the operator** so it's fixed before client impact.
4. **Inbound loop (① content → leads):** Content is the top-of-funnel; the same agent stack fulfills, so 1 post → warm lead → 48h-to-live agent.

---

## Why each non-obvious choice

- **Control-plane agent ("more agents is the answer").** You don't hand-configure clients. One meta-agent (Hermes or Claude Code in a VM) installs/repairs the client agents. This is what makes it *one-person*.
- **Cloud VMs over Mac minis.** Remote-manage from anywhere, delete/re-spin in <1s, sandboxed blast radius, and the live desktop is itself the demo that sells trust.
- **Composio as the auth choke-point.** Auth is "by far the biggest time sink." One connector handles tool-calling + credentials → portable across any agent, no emailed passwords.
- **Obsidian as the context layer (not Notion).** Markdown wiki the agent reads natively → durable per-client memory; "this is what personal AGI feels like."
- **Model-agnostic harness.** Never marry a model. GPT-5.5 default for token-light tool-calls; Opus 4.7 only for long-horizon coding. Model cost is *your* margin lever, invisible to the client.
- **Flat pricing, no "tokens/credits."** Usage talk "ruins the magic" and slows time-to-yes. Sell unlimited; reality is 1–3 agents per client.

---

## Build sequence (48h to first client agent)

1. **Pick a vertical** — legacy, people-heavy, AI-curious: law, insurance, real estate, manufacturing, agencies, wholesalers. Avoid healthcare/finance (regulatory). Niche by geo or sub-type.
2. **Stand up the control plane** — Orgo workspace + Orgo MCP wired into your operator agent; add setup-context MCPs (Perplexity/Exa/Context7/X) for current install docs.
3. **Provision client workspace** — spin an Orgo VM, install harness (Hermes preferred) via the control agent.
4. **Install the capability baseline** — Composio connectors, Agent Mail identity, seed the Obsidian vault, attach reusable + vertical skills.
5. **Wire reliability** — watchdog on gateways + failure-alert emails to you.
6. **Ship the executive template** — solve the universal exec pain (too many emails/meetings/follow-ups) first, then layer vertical skills (e.g. demand letters for a law firm).

---

## Risk / decision register

| Risk | Mitigation in this architecture |
|------|--------------------------------|
| Gateway crashes (esp. OpenClaw) | Watchdog auto-restart; prefer Hermes (self-evolving) |
| Credential leakage | Composio-managed auth, per-client sandboxed VM, no shared creds |
| Scope creep / fulfillment overload | Trello request cap (1–2 / 48h); one meta-agent absorbs setup labor |
| Model price/availability shifts | Model router; swap without re-platforming |
| Single-operator key-person risk | Everything reproducible from the control agent + skills; VMs re-spin in <1s |
| Vendor lock (Orgo) | Harness + Composio + Obsidian are portable; Orgo is the compute substrate, swappable for Hostinger/VPS |

---

## How this maps to your pipeline

This is the **delivery architecture** behind the `openhands-niche-agency` model you already track (memory: *done-for-you AI engineering team, $2K–$5K/mo per SMB*). It aligns to your positioning theses in GBrain (`research/our-positioning-thesis`, `research/emerging-positioning-patterns`): deployed proof + autonomous execution + liability-bearing operator. Substitute OpenHands for Hermes/OpenClaw as the harness and the layers are identical.
