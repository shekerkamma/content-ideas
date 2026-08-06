# SKEPTIC LENS — DeepGrid Semi client-acquisition strategy

Posture: every company-sourced number is wrong until it reconciles. Five findings below; two claims survive.

## 1. The three gross margins do not reconcile. The taxonomy is post-hoc.

The story is "84% = board, 72% = kit, 88% = blend." Three denominators, one narrative. It fails on arithmetic.

**A blend cannot exceed its best component.** FY32 mix (BP-1A §8): software ₹50 Cr (3.6%) at 90%+; everything else ₹1,338 Cr (96.4%) is hardware. Ceiling, using the *retracted* 84% as the hardware best case:
`0.036(0.90) + 0.964(0.84) = 84.2%` — below the claimed 88.4%. Using the kit-level 72% the plan says it uses "in every downstream calculation": `(1,338×0.72 + 50×0.90)/1,388 = 72.7%`. The 88.4% overshoots by 16 points.

**Reverse-solve it.** 88.4% on ₹1,388 Cr requires GP ₹1,227 Cr, i.e. total COGS ₹161 Cr. The AD2 kit alone (₹450 Cr @ 72%) burns ₹126 Cr. That leaves ₹35 Cr of COGS for ₹938 Cr of remaining revenue — **96.3% gross margin on 54,000 sensor pods, 80 AGVs, radar/thermal modules, defence AUGVs and merchant die.**

**The AD0 line is negative.** Smart Mirror: 54,000 units at ₹0.50L ASP. The AD2 kit's own "sensors, pod and installation" COGS is ₹62,000 — above the mirror's entire ASP, for a pod BP-1A specs at 3×8MP GMSL2 + 4D radar + thermal. ₹270 Cr (19.5% of company revenue) plausibly carries negative gross margin. Nobody has costed it.

**84% is internally false in the IM.** Same page: "$30 cost, sell $200 → 84% GM" and "at ₹2.5L kit price, gross margin reaches 84%." ₹2.5L ≈ $3,000. $30 against $3,000 is 99%, not 84%. Two mutually exclusive derivations of one number, on one page.

**72% survives — barely.** ₹2.30L − (₹1,750 + ₹62,000) = ₹1.6625L → 72.3%. ✓ But BP-1A §8 says the model prices at ₹2.50L, not ₹2.30L (→74.5%), and the ₹1,750 compute COGS is ~30% below the July deck's own $30 (₹2,499) board. Substituting the deck's figure gives 71.9% — sensors dominate, so the claim is robust. **72% holds.**

## 2. 12.9× fixes the arithmetic and keeps the fallacy.

$50 ÷ $3.876 = 12.90. ✓ But it divides Mobileye's **ASP** (a price, carrying ~70% vendor margin, certified software, homologation, field data) by DeepGrid's **die COGS**. The retracted 774× was $2,400 ÷ ~$3.10 — the identical price÷cost category error. The correction changed the numerator and preserved the fallacy.

Like-for-like: Mobileye GM ~70% → EyeQ COGS ≈ $15 → **3.9×**. Fully loaded at the company's own break-even volume (NRE $3.17M ÷ 174,908 = $18.12/die) → $22.00 → **2.3×**.

Worse, the IM's ASIC-scale economics sell the compute node at **$200**. Against a $50 Mobileye node, DeepGrid is **4× more expensive**, not 12.9× cheaper.

And slide 18's implied 92–93% margin is exactly `(50 − 3.876)/50 = 92.2%` — pricing at the incumbent's ASP. You cannot claim a 12.9× buyer-facing advantage *and* a margin computed on the assumption you don't pass it on. Finally: **$50 has no evidence-ledger entry.** `allowed-numbers.yaml` carries Mobileye at ₹5–8L. The "honest number" fails the deck's own evidence rubric.

## 3. Break-even 174,908 is falsified by the plan's own volumes — twice.

FY32 units: 18,000 + 54,000 + 30 + 100 + 50 = 72,180. Scaling by ADAS revenue (₹2.55/24.96/94.36/239/487/914 Cr) gives cumulative FY27–FY32 ≈ **139,000 chips** — ~36,000 short. Break-even crosses **FY2033**, not FY2032.

The fatal one: BP-1A shows net income positive **FY2029** at +₹19.85 Cr, on ~9,600 cumulative chips. The July deck asserts break-even at 174,908 chips. **An 18× contradiction, in the same deck, six slides apart** (sl.2/sl.32). Meanwhile BP-1A's live figure — "400–600 kits/yr, the real break-even volume" — is 290–437× smaller and is *not* in the Corrections Ledger. Four break-even numbers circulate; one was retracted. 174,908 is quoted to six significant figures off a six-year forecast: false precision, and not reproducible from any published input.

## 4. The ₹1 Cr is not what the July deck says it is. BP-1A already says so.

BP-1A §3 and §9, verbatim: `GEMC-511687794620175 · Robot Training · ₹23.01L · delivered` and `GEM/2026/R/672471 · Robotics Assistant · ₹78.39L · L1, under execution`. Then: *"sits in Deepgrid Datacentre Pvt Ltd… IP on the delivered contract is MCEME-owned (Clause 27); **none of it is trucking/ADAS revenue**."*

So: (a) 78% is **L1** — lowest-bidder status, not an award, not revenue; (b) delivered revenue is **₹23.01L**, not ₹1 Cr; (c) it is **robot training services**, not silicon; (d) it is in a **different legal entity** — the company being funded has zero revenue; (e) DeepGrid **does not own the IP**.

The July deck calls this "booked… Real revenue. Real customer," scores Defense 5/5 on Evidence *and* 5/5 on Budget-verified, and narrows the open question to "commercial sale vs grant vs R&D subsidy" — a trichotomy that omits every actual defect. Even a clean answer to Condition 1 leaves the claim broken. Slide 36's own collapse math is also wrong: 5% weight × 4 points = 0.20, giving 3.76, not the stated ~3.20.

Demand: CA-certified revenue certificate for Deepgrid Semi (not Datacentre); the GeM award letter vs bid-comparison sheet; GSTR-1 outward-supply lines (a grant generates none — settles the question in minutes); bank statements for the ₹23.01L; Clause 27 IP text; the inter-company execution agreement.

## 5. The unwritten killer: the two-track sequence cannot produce the evidence it exists to produce.

Slide 14's load-bearing claim is that Defense-first is *"the fastest way to generate the missing Fleet evidence."* It cannot be. Sovereign UGV and border-surveillance data is classified and non-releasable to a 3PL buyer; the duty cycle of a border UGV has zero transfer validity to an N3 truck on NH-48; and the delivered work is MCEME-IP-owned, so it cannot even be shown. The sequence has no mechanism. Strip it and the plan is a defence services company asking for chip money.

Second, deleted rather than retracted: BP-1A §7 states *"against the device that actually wins mandated volume in India we are twenty times more expensive"* (₹15,000–40,000 compliance boxes; ₹4,500–11,000 VLTD anchor — the latter SOURCED). That paragraph does not appear anywhere in the July deck; slides 21–25 benchmark only Aurora/Kodiak/Gatik and declare the quadrant "empty by construction." First silicon at month 14–18 from an unclosed raise lands **after** the Jan 2028 enforcement date, into a market where retrofit is a once-per-vehicle purchase already made — from the ₹15k box.

**Meta-finding: the Corrections Ledger is a credibility instrument.** It retracts five arithmetically embarrassing numbers and, in the same document, silently drops the two commercially fatal disclosures BP-1A had made honestly. The July deck is a regression on evidence, dressed as a correction.
