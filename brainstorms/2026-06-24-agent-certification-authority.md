# Agent Certification Authority: Brainstorm / Discovery Notes
Date: 2026-06-24 · Goal: Harden Thesis A into a defensible, sales-ready positioning narrative (beachhead, ICP, wedge, rejectable counterparty, pricing, moat, GTM, risks). Self-interview mode — Claude answers as founder.

## Structured context
- **Topic type**: positioning
- **Topic string**: "Independent certification & assurance authority for enterprise AI agents — the UL/SOC-2 for agents"
- **Entities**: Thesis A; patterns E2 (Auditable Operator) + E1 (trust rails) + benchmark authorship; scorecard use cases #1 support, #5 chatbot, #19 doc-AI, #23 SecOps auto-remediation, #10 HR; incumbents Braintrust/Arize/Patronus/Lakera; foundation labs (OpenAI/Anthropic/Google)
- **Prospect/account**: n/a (pre-company)
- **Target buyer**: CFO / Chief Risk Officer / Head of Procurement (buyer-side, not developer)
- **Verticals**: candidate beachheads — financial services, healthcare, SecOps-heavy enterprises
- **Open decisions**: beachhead industry; certification vs continuous-assurance sequencing; standard/benchmark ownership model; build vs partner for the eval engine

## Summary / key decisions
- **What we are:** the **independent validation & assurance authority for enterprise AI agents** — "the agent-native Model Risk Management layer." Not an eval tool for devs; an examiner-ready assurance product for the risk owner.
- **Beachhead:** **Financial Services**, entering through the **Model Risk Management (MRM) / SR 11-7** mandate — a budgeted, legally-required *independent validation* function that already buys third-party validation and has no agent-native tooling.
- **First agents certified:** (a) customer-facing **support/chatbot agents** (#1/#5) and (b) **document-AI agents** for KYC/onboarding/lending (#19) — both fall under regulatory validation + have catastrophic downside.
- **Buyer:** Head of Model Risk Management / Chief Risk Officer (economic buyer); internal champion = MRM validator; user = the line-of-business deploying the agent.
- **The counterparty who can reject our certification:** the **bank examiner/regulator** (OCC, Fed, CFPB, FCA) + the internal independent validator + board risk/audit committee. Our artifact must survive examination — this is the bar that makes us credible and is itself the moat.
- **Wedge / first product:** pre-deployment **agent validation dossier** (examiner-ready) at go-live decision point → land-and-expand into **continuous assurance subscription**.
- **Moat (compounds):** cross-bank failure corpus + FS Agent Validation Benchmark (we author the standard) + examiner/regulator acceptance + structural INDEPENDENCE (eval vendors & labs can't credibly certify their own ecosystem) + embedded-in-MRM-workflow switching cost.
- **Build vs partner:** BUILD the FS benchmark + validation methodology + adversarial/red-team suite + failure corpus (the IP); OEM commodity tracing/eval plumbing (OpenTelemetry/Phoenix). Independence forbids reselling any builder's tool.
- **Pricing:** fixed-fee per-agent validation engagement (audit-budget line) + annual per-agent continuous-assurance subscription + premium examiner-support. Buyer-funded = pricing power.
- **Verdict:** sharper and more defensible than a generic horizontal "agent certification platform." MRM is the unlock — a mandated, budgeted, independence-requiring buyer.

## Q&A log

### Q1 — Category definition (what exactly are we, in one sentence?)
- Asked: Are we a horizontal "agent QA platform," or something narrower with a named buyer? Recommended: narrow to an independent ASSURANCE authority, not dev tooling.
- Decided: **"The independent validation & assurance authority for enterprise AI agents."** We sell certification/assurance to the risk owner, not eval tooling to the builder. Framing analog: UL / SOC-2 / Moody's — an independent third party whose stamp the market trusts.
- Reasoning: selling to the buyer (not the dev) is where pricing power lives (PlatoSeed "sell trust to the CFO"); independence is the one thing eval vendors and foundation labs structurally cannot claim.

### Q2 — Beachhead industry (which of the 11?)
- Asked: Horizontal, or pick one regulated vertical first? Recommended: pick one with a mandated independent-validation function already budgeted.
- Decided: **Financial Services**, specifically via **Model Risk Management (SR 11-7 / SS1/23)**.
- Reasoning: MRM is a legally-mandated, budgeted function whose entire job is *independent validation of models* — and AI agents are now "models" it must validate with zero agent-native tooling. We're not creating a budget line; we're filling an existing, regulator-forced one. FS also has catastrophic downside + clear risk-owner buyer + objective-enough measurement to make certification credible.

### Q3 — First agent use cases to certify (which scorecard rows?)
- Asked: Which deployed agent types first? Recommended: the regulated, measurable, already-deployed ones.
- Decided: **(a) customer-facing support/chatbot agents (#1/#5)** — huge deployed FS volume, conduct/fair-lending/complaint risk; **(b) document-AI agents (#19)** for KYC/onboarding/lending — high determinism, objective ground truth, BSA/AML + lending-compliance exposure.
- Reasoning: #19 is the *easiest to certify objectively* (extraction accuracy vs ground truth) → builds credibility; #1/#5 is the *highest-volume/highest-visibility* → builds pipeline. Lead demos with #19's hard numbers, sell breadth with #1/#5.

### Q4 — Exact ICP / buyer / signer
- Asked: Who is the economic buyer and who signs? Recommended: CRO/MRM, not the dev or the LOB.
- Decided: Economic buyer = **Head of Model Risk Management / Chief Risk Officer**. Champion = MRM validator (their job gets impossible without us). User = the LOB/eng team deploying the agent (must comply to ship). Three-persona sale; risk owner holds the budget and the pen.
- Reasoning: the risk owner feels personal/regulatory liability and already pays for independent validation. The LOB *wants* a fast path to go-live; we're the gate that lets them ship safely.

### Q5 — The one counterparty who can reject our agent's certification
- Asked: Whose "no" kills the value? Recommended: the regulator/examiner.
- Decided: the **bank examiner/regulator (OCC, Fed, CFPB / FCA)**, plus the internal independent validator and board risk/audit committee. Our validation dossier must survive examination.
- Reasoning: this is the forcing function for rigor AND the moat — if our artifact reliably survives exams, switching to anyone unproven is unthinkable. "Examiner-ready" becomes the category-defining claim.

### Q6 — Wedge / first product + sequencing
- Asked: Pre-deploy certification or continuous assurance first? Recommended: pre-deploy first (decision moment), then expand.
- Decided: Lead with **pre-deployment validation dossier** delivered at the go-live decision (where the risk owner is already blocked and motivated) → land-and-expand into **continuous-assurance subscription** (drift monitoring, re-validation on model/prompt change, exam support).
- Reasoning: pre-deploy is the acute pain and the natural entry; continuous assurance is the recurring-revenue annuity. Same playbook as how penetration-test → continuous-security-monitoring evolved.

### Q7 — What "certification" concretely is (the artifact)
- Decided: a structured **Agent Validation Dossier** mapped to the SR 11-7 lifecycle: (1) conceptual soundness (design, data, guardrails, escalation), (2) outcome testing vs our FS Agent Validation Benchmark + adversarial/red-team suite, (3) ongoing monitoring thresholds, (4) counterfactual provenance logs ("why it did X, and why it didn't do the near-miss"), (5) control attestations (data handling, human-in-loop, fair-lending). Output = examiner-ready report + live assurance dashboard + a time-boxed "Validated" mark that expires and must be renewed.
- Reasoning: regulators already know the SR 11-7 shape; mapping to it makes us instantly legible and hard to argue with.

### Q8 — Build vs partner (the engine)
- Decided: **BUILD** the FS Agent Validation Benchmark, the validation methodology, the adversarial/red-team suite, and the cross-customer failure corpus (this is the defensible IP). **OEM/partner** the commodity tracing/observability plumbing (OpenTelemetry / Phoenix open standards). We never resell a builder's eval tool — independence is the product.
- Reasoning: rebuilding tracing is undifferentiated; the benchmark + methodology + corpus + independence are the moat. Open-standard plumbing also reassures buyers about lock-in.

### Q9 — The moat (how it compounds + defensibility)
- Decided: five layers — (1) **cross-bank failure corpus** + benchmark (no single bank or lab has the cross-customer view); (2) **regulator/examiner acceptance** (relationship + track record of surviving exams); (3) **the standard itself** (we author "what good looks like" for FS agents = category authority, Harvey-LAB playbook); (4) **structural independence** (eval vendors/labs can't certify their own ecosystem credibly); (5) **workflow + board-reporting embedding** (switching cost once we're in MRM's process and board packs).
- Reasoning: this is a trust/data/standard flywheel, not a feature — exactly the "moat is never the model" pattern.

### Q10 — Pricing
- Decided: **fixed-fee per-agent validation engagement** (sits in the audit/MRM budget line, $X0k like an external validation) + **annual per-agent continuous-assurance subscription** + **premium examiner-support** during exams. Optional outcome-aligned SLA (assurance holds up in exam or fees rebated).
- Reasoning: mirrors how banks already pay for external model validation and audit — we slot into an existing buying motion at a familiar price shape, with a recurring annuity layered on.

### Q11 — GTM / first 10 customers
- Decided: target **super-regional + mid-tier banks** (real regulatory pressure, faster cycles than money-center). Channel: (1) co-deliver with **model-risk consultancies + Big 4** (arm the channel rather than fight it — they refer/resell our tooling); (2) **publish the FS Agent Validation Benchmark** as thought leadership → inbound + standard-setting; (3) the regulators' own AI guidance is the demand driver. First 10 = banks that already shipped support/KYC agents and are now getting MRM/exam pushback.
- Reasoning: the Big 4 will otherwise be the competitor — better to be the tooling/standard they deliver on top of. Benchmark publication is both marketing and moat.

### Q12 — Why now + why us
- Decided: **Why now** — agents entering regulated production (2025–26); regulators applying model-risk/AI guidance; SR 11-7 explicitly spans AI; 40%+ agentic-project cancellation = the trust gap is acute; no agent-native MRM tooling exists yet. **Why us** — independence + benchmark authorship need no proprietary-data incumbency; the moat accumulates as we operate; a small team can author a standard and win design partners before incumbents productize.
- Reasoning: the window (mid-2026 → mid-2027) is the standard-setting land-grab.

### Q13 — Biggest risks + kill criteria
- Decided: Risks — (a) Big 4 / MRM consultancies build it → mitigate by arming them as channel + out-productizing; (b) buyers treat it as a checkbox / regulators accept self-attestation → focus on catastrophic-downside use cases where assurance is genuinely valued; (c) eval vendors move in (Patronus is already compliance-first) → differentiate on independence + examiner-acceptance + FS depth; (d) labs ship native guardrails → we certify cross-vendor & independent. **Kill criteria:** if after ~5 design partners no bank will pay for pre-deploy validation as a budgeted line, OR regulators clearly signal self-attestation suffices → pivot to Thesis C.
- Reasoning: name the failure conditions up front so we can fail fast.

### Q14 — Name / tagline (flagged)
- Decided (provisional): tagline = **"Examiner-ready validation & assurance for enterprise AI agents."** Working names parked (Attestn / Vouchsafe / Vellum-style). Naming = later flag.

## Open flags (pending input)
- Final company name / brand → founder decision later
- Exact first-design-partner bank targets → needs warm intros / outreach list
- Whether to anchor the standard to an existing body (NIST AI RMF, ISO/IEC 42001) vs author proprietary → decide during benchmark design
- Pricing magnitude ($ per validation, subscription tiers) → validate with 2-3 MRM buyers
- Build sequencing: #19 doc-AI benchmark first vs #1/#5 support → lean #19 for objective credibility
