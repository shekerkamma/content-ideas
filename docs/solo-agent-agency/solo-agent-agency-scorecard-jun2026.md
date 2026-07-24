# Vertical Scorecard — Done-For-You Solo AI Agent Micro-Agency

**Date:** 2026-06-28 · **Framework:** Emergence/VC 7-dimension · **Analyst:** vertical-scorer (Exa-grounded)

```
VERTICAL SCORECARD: SOLO AI AGENT MICRO-AGENCY (Services-as-Software)
══════════════════════════════════════════════════════════════════════

  Dimension                Score   Signal
  ───────────────────────  ─────   ────────────────────────────────────────
  Intelligence Ratio       4/5     Work is high pattern-recognition (email triage,
                                   follow-ups, scheduling, doc gen, research). Clear
                                   copilot→autopilot path. Caveat: vertical judgment
                                   (legal clauses) breaks full autonomy.
  Outsourcing Readiness    5/5     Already a $92.4B back-office BPO market; buyer
                                   already pays VAs/fractional-ops for this exact work.
                                   SMB adoption 54–68% and fastest-growing cohort.
  TAM Accessibility        5/5     AaaS $15.7B (2025)→$73.9B (2030), SME 38.4% CAGR.
                                   Bain: $100B US agentic-coordination TAM, 90%+
                                   untapped. Solo operator needs only ~10 clients.
  Data Moat Potential      2/5     Structural weakness. Stack (Orgo/Hermes/Composio)
                                   is commoditizing; "wrapper" replicable. Moat is
                                   switching cost + per-client Obsidian context, NOT
                                   a defensible dataset. (See MonitorIntent moat erosion.)
  Regulatory Friction      4/5     Recommended verticals (real estate, agencies, mfg,
                                   wholesalers) are low-friction; model explicitly
                                   avoids healthcare/finance. Law/insurance add some.
  Incumbent Vulnerability  5/5     BPOs (Accenture, Teleperformance) won't serve SMBs
                                   <50 employees economically; VAs/agencies are
                                   manual. Sub-50-employee segment is green-field.
  Mirage PMF Risk          2/5     HIGH risk. Documented pattern: legal AI agent at
                                   $2–5K/mo to law firms CHURNED, pivoted to
                                   human-in-loop $8K/mo per-outcome. Services-with-
                                   software-veneer + customer concentration + inference
                                   margin compression killed ~40% of first-wave agents.
  ───────────────────────  ─────
  COMPOSITE SCORE          27/35

  VERDICT: CONDITIONAL  (24–29 band)
```

## Rationale
Demand, TAM, outsourcing-readiness, and incumbent-vulnerability are all exceptional — the buyer already pays humans for this work and the under-50-employee SMB is structurally abandoned by enterprise BPOs. **The two weak dimensions are the whole game: no data moat (2/5) and high mirage-PMF risk (2/5).** For a VC-scale startup that's fatal. For a *solo operator* it's manageable — you're not chasing a defensible product, you're cash-flowing 5–10 embedded relationships. A solopreneur at 8 clients × $5K = $40K/mo is a *win*; the same numbers killed a $12M-funded startup because the model couldn't scale to software multiples.

## Copilot → Autopilot path
1. **Copilot (month 1):** agent drafts, operator reviews every output via Loom. Trust-building.
2. **Supervised autopilot (month 2–3):** agent runs scoped tasks autonomously; watchdog + failure-alerts catch breaks before the client sees them.
3. **Autopilot (month 4+):** recurring workflows run unattended; operator only handles new requests + vertical-skill expansion. *High-judgment verticals (legal/insurance) stay copilot permanently — that's a feature, not a failure.*

## Key risk (load-bearing)
**Mirage PMF via the "consulting with a software veneer" trap.** Early clients pay for novelty, then churn when (a) the agent breaks, (b) inference cost compresses your margin, or (c) they realize the stack is DIY-able. Mitigations baked into the architecture: reliability layer (watchdog + alerts) defends against (a); model router defends against (b); deep per-client Obsidian context + 48h-to-value defends against (c) by making *switching cost* the moat. **Avoid >70% revenue from top-3 clients.**

## Sources
- [1] Mordor — Agent-as-a-Service Market ($15.7B→$73.9B, SME 38.4% CAGR), 2025-08
- [2] Bain & Co — $100B US agentic-coordination TAM, 90% untapped, 2026-05
- [3] Grand View — BPO $328.4B (2025); Stealth Agents — back-office $92.4B, SMB adoption 54–68%
- [4] Cryptopolitan/New Market Pitch — AI-agent funding $1.5B→$2.9B (2024→2025), 2026-06
- [5] AdExchanger — Mega $11.5M Series A, SMB AI marketing, 50%+ fully automated (proof point)
- [6] Interconnectd — legal AI agent post-mortem: $2–5K/mo churn → human-in-loop $8K/mo per-outcome (failure case)
- [7] AgentMarketCap — ~40% of first-wave agent startups dead; customer concentration + margin compression (failure pattern)
- [8] prabal.ca — MonitorIntent post-mortem: moat erosion / commoditization (data-moat failure case)
```
