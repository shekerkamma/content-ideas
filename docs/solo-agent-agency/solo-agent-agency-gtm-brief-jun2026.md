# GTM Strategy Brief — Solo AI Agent Micro-Agency

**Date:** 2026-06-28 · **Verdict:** CONDITIONAL GO (27/35) · **Decision:** Launch, but engineer around the two weak dimensions (no data moat, high mirage-PMF risk) from day one.

---

## The one-line thesis
The under-50-employee SMB is structurally abandoned by enterprise BPOs and can't hire AI engineers — sell them a **managed digital employee** at a flat seat fee, and make **switching cost (not technology) the moat.**

## The wedge
Don't sell "AI agents." Sell **one named digital employee that owns a painful, recurring executive workflow** in one vertical. Start where you have proof, then niche down (diverge → converge). Recommended entry verticals (low regulatory friction, high pain, people-heavy): **marketing agencies, real estate, insurance agencies, manufacturers/wholesalers.** Avoid healthcare/finance.

## Offer architecture
| | |
|---|---|
| **Format** | Productized service — flat **$5K/mo** (→ $10K for premium/Hermes-grade), no usage talk, no "tokens/credits" |
| **Promise** | First agent live in **<48h**; abundance framing (unlimited requests, capped to 1–2 / 48h operationally via Trello) |
| **Value frame** | Business *outcomes* (revenue, hours reclaimed, response time), never "time saved" |
| **Anti-churn** | Reliability SLA (watchdog + failure-alerts) + weekly improvement cadence — the agent gets better every week |

## GTM motion (in priority order)
1. **Content as the funnel.** Operator posts the build-in-public proof (the live Orgo desktop demo *is* the asset). Inbound + warm > cold. "Content is overpowered."
2. **AI Transformation Audit (free).** Analyze the prospect's ops, show one workflow an agent saves $X/yr. Proof-of-concept → recurring fee. (This is the documented highest-converting SwaS motion.)
3. **Case study → referral loop.** First 1–2 clients free or discounted to manufacture case studies; the vertical is small and word-of-mouth compounds.

## Unit economics (per client/mo)
- Revenue **$5,000**
- COGS: Orgo VM ~$150 + inference (GPT-5.5, token-light) ~$300–600 + Composio/Agent Mail ~$100 ≈ **$600–900**
- **Gross margin ~82–88%** (consistent with the 75%+ services-as-software benchmark)
- **Break-even ≈ 1 client.** Target **8 clients = $40K/mo (~$34K gross).** Capacity ceiling per solo operator ≈ 10–15 because the control-plane agent absorbs setup labor.

## 30 / 60 / 90
- **Day 0–30:** Stand up control plane (Orgo + Orgo MCP + setup-context MCPs). Pick 1 vertical. Land 1–2 pilots via audit. Ship the executive-template agent.
- **Day 31–60:** Convert pilots to paid. Publish 2 case studies. Layer first vertical-specific skill. Wire reliability (watchdog + alerts). Reach 3–4 clients.
- **Day 61–90:** Systematize onboarding into a reusable skill so the meta-agent provisions new clients near-autonomously. Niche down to the sub-vertical that pulled hardest. Reach 6–8 clients.

## Defending the two weak scores (this is the strategy)
| Weak dimension | Mitigation (engineered into the architecture) |
|---|---|
| **No data moat (2/5)** | Moat = **switching cost**, not tech. Deep per-client **Obsidian context vault** + embedded workflows make replacement painful. Own the relationship and the context, not the model. |
| **High mirage-PMF (2/5)** | (a) **Reliability layer** so the agent rarely visibly breaks; (b) **model router** so inference price cuts don't crush margin; (c) **<48h-to-value + weekly gains** so perceived value stays ahead of DIY temptation; (d) **diversify** — no >70% revenue from top-3 clients; (e) keep high-judgment verticals **human-in-the-loop** (the $8K/mo per-outcome legal pivot proves clients pay *more* for assurance). |

## What would change the verdict to a full GO
Two embedded clients renewing past month 3 at >85% gross margin with <10% monthly churn. That retires the mirage-PMF risk empirically and earns the GO.

## Provenance
Scored in `solo-agent-agency-scorecard-jun2026.md`; architecture in `SOLUTION-ARCHITECTURE.md` + diagram. Persisted to GBrain (`research/solo-agent-agency-architecture`). Aligns to existing positioning theses (deployed proof + autonomous execution + liability-bearing operator) and the `openhands-niche-agency` model.
