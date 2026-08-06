# HISTORIAN lens — precedent in mandate-created hardware markets

## 1. The EU tachograph / eCall precedent (BP-1A §6) — directionally right, mechanically wrong

**Tachograph.** The incumbency claim holds. Continental (VDO), Stoneridge and Actia together hold
roughly 63% of global tachograph hardware revenue; Stoneridge alone 18–22%; the top five >80% of
the European market. But the *mechanism* is not "relationships beat cheap entrants" — it is type
approval. Only type-approved units may be installed, and the same approved suppliers serve both
line-fit and workshop replacement, so there is no independent aftermarket to absorb. BP-1A also
omits the counter-case: **Intellic** (spun out of Austria's Efkon) *did* enter post-mandate, won
smart-tachograph approval and sold into 25 countries — then exited by acquisition to **ZF in
January 2023**, not by scaling independently.

**eCall.** Closer to wrong. eCall applied to new type approvals (M1/N1, March 2018) — line-fit
only; there was never a meaningful aftermarket segment to "absorb". And the largest share of the
eCall-driven TCU market went to **LG (>25%)**, ahead of Continental, Harman, Bosch and Denso — a
consumer-electronics entrant that owned the connectivity module, not the deepest Tier-1 relationship.

**The "~18 months" figure is unsupported.** I found no source for it in either market — drop it.
BP-1A's own alternative (3–5 years mandate→stable incumbent share) is defensible, and the tachograph
cadence (digital 2006 → smart 2019 → Gen2v2 2023) gives the better lesson: mandates create
*repeated* re-entry windows at each generation, not one closing door.

## 2. AIS-140 — the domestic precedent, and it is not encouraging

**Timeline.** Buses were to comply by April 2018; postponed to 1 Jan 2019; effective April 2019;
pre-Jan-2025 registrations given until 31 Oct 2025; enforcement rules *still* being updated in
2026 — and enforcement was explicitly gated on state backend readiness (Delhi and Kerala first).
Call it ~8 years from notification to broad enforcement. That is the most load-bearing precedent
against the deck's 12–24 month design-in window, and it makes BP-1A's "slow case" the base case.

**Pricing and structure.** Seven years on, AIS-140 VLTDs still sell at **₹3,500–₹12,000** (quotes
to ₹14,000), 3–4× spreads between vendors all claiming the same compliance, and no consolidation
into an oligopoly. Nobody built a hardware franchise from AIS-140.

**Did value migrate to platform/SaaS?** Yes — BP-1A is right, but too generous to itself. Value
went to whoever held the *recurring compliance relationship* (Vahan linkage, SIM, certification
renewal, state backend integration, uptime), not to whoever built the better box or chip. The
renewable asset is the service, not the silicon.

## 3. Base rate for a fabless startup winning an automotive design-in

- **Mobileye**: founded 1999, EyeQ1 sampled 2004, first OEM wins (BMW, GM, Volvo) 2007 — ~8 years.
- **Horizon Robotics**: founded 2015; joint AI lab with Changan 2018; Journey 2 announced Aug 2019;
  mass production on Changan UNI-T June 2020 — ~5 years, the fastest verified case, requiring both
  a domestic OEM under a national self-reliance push and a *two-year joint lab* before the win.

I have no rigorous denominator of attempts, so this is a pattern, not a computed base rate: 5–8
years founding→SOP, with 2–3 years of relationship *preceding* the design-in. DeepGrid's 12–24
month assumption is roughly half the fastest verified case — and that case had state-directed
demand plus a relationship DeepGrid concedes it lacks (§10 risk 10).

## 4. How durable is sovereign preference?

**China's EV battery whitelist**: 57 domestic makers listed 2015, foreign suppliers cut off from
subsidy eligibility, **abolished June 2019** — a ~4-year window, which CATL and BYD used to reach
scale and then survive open competition.

**India's Public Procurement (Preference to Make in India) Order 2017** is real but leaky: waivers
where the technology is unavailable domestically, urgency waivers, and — the key mechanism — local
assembly converts foreign incumbents into Class-I local suppliers. DPIIT tightened the local-content
calculus in 2024 (excluding imported items merely *sourced* locally) precisely because that loophole
was being used. Bosch and Continental already manufacture in India; BP-1A §7 concedes this. That is
the erosion path, and it is fast.

**Tejas Networks** is the Indian survival case: ~20 years sustained by PSU/BSNL demand and
trusted-source policy, reaching scale only after Tata took control (2021) and the ~$900M BSNL
4G/5G contract. **Signalchip** is the cautionary case: India's first indigenous 4G/5G modem chips,
unveiled Feb 2019 after eight years of R&D — I could not verify any subsequent commercial
deployment, and the absence of visible design wins seven years on is itself the finding.

Sovereign preference is therefore not a moat. It is a subsidy on *time* — 3–5 years — and the
payoff needs a balance-sheet sponsor before it expires.

## 5. Best-fit analogue

Structurally the closest is **CATL under the 2015–19 whitelist** — but DeepGrid lacks CATL's
conditions: the whitelist gated subsidies for the *entire* domestic OEM base, whereas Atmanirbhar
excludes foreign silicon only from government and defence fleets, a small fraction of the N2/N3
base. The protected window is far narrower.

On the resources DeepGrid actually has, the best fit is a **Tejas Networks + Intellic composite**:
survive on sovereign/PSU demand while the commercial mandate clock slips, then exit into a balance
sheet (Tata for Tejas, ZF for Intellic) rather than out-lasting Bosch and Continental alone. What
both had to do as the window closed: hold a certified, differentiated product; keep non-mandate
revenue paying the bills; and accept an acquirer's distribution instead of building one.

**Where the two DeepGrid documents disagree, history favours the July deck.** Its Tier-1-gated
posture (no direct OEM spend until Uno Minda / Spark Minda / Bosch India signs a binding co-dev)
matches the Horizon–Changan and Intellic–ZF patterns. BP-1A §6's "pursue OEM engagement
opportunistically from month one" does not.

---
Sources (retrieved 5 Aug 2026): researchandmarkets.com Europe tachograph market · marketgrowthreports.com
digital tachograph system market · press.zf.com release_50112 (ZF/Intellic, Jan 2023) ·
counterpointresearch.com global TCU market 2018–22 (LG >25%) · blog.fleetx.ai AIS-140 device price
India 2026 · loconav.com AIS-140 notifications timeline / "Is India really ready" ·
intangles.ai AIS-140 compliance 2026 · autonews.gasgoo.com Horizon Journey 2 / Changan UNI-T ·
mobileye.com about-history; handwiki Company:Mobileye · chinadaily.com.cn 2019-07-01 battery
white-list abolished; news.cgtn.com 2019-06-25 · dpiit.gov.in PPP-MII Order 2017 + 2024 revision;
outlookbusiness.com local-content rule change · lightreading.com / datacenterdynamics.com Tejas–BSNL
$900M · pib.gov.in relid=188979 (Signalchip, Feb 2019).
