# ECONOMIST LENS — market structure and incentives

Reasoning from general market structure rather than the run documents is tagged
**[STRUCTURAL]**.

## 1. Mandates pay the compliance minimum

BP-1A §7: after AIS-140, devices settled at ₹4,500–11,000 and value "migrated from
hardware to platform and SaaS stickiness" `SOURCED`; §6 cites EU tachograph/eCall,
where incumbents absorbed aftermarket share within ~18 months. **[STRUCTURAL]** A
mandate creates demand but not preference: willingness to pay is capped by the cost of
non-compliance, not the safety outcome, so price collapses to the certification floor and
value migrates to the recurring layer.

At ₹2.3L against a ₹15,000–40,000 box, DeepGrid is 5.75–15.3× the compliance
alternative and ~21–51× the AIS-140 anchor. That gap survives only where the spec is
written in performance terms the cheap box fails. **[STRUCTURAL]** That function is AEBS
(AIS-188) — radar, brake actuation, proving-ground homologation; LDW/BSD/DMS are
warning-only, exactly what a ₹30k camera box approximates. Neither document prices by
function.

## 2. The silicon advantage is real, but it is not a cost advantage

$3.876/die is a foundry quote **at 1M units** (sl.31). Peak-year volume is 72,000 units
(§8) and break-even is 174,908 chips **crossing FY2032** (sl.32) — the plan never reaches
the volume its headline cost assumes. Loaded: $3.17M
NRE over ~175,000 cumulative chips ≈ $18/die plus $3.876 variable ≈ **$22/die effective**,
~2.3× Mobileye's $50 reference, not 12.9×. Slides 4/31 and slide 32 cannot both drive the
pitch.

**[STRUCTURAL]** Incumbents amortise NRE over tens of millions of units; $50 is a margin
choice, not a cost floor, so their marginal cost sits below DeepGrid's loaded cost. BP-1A
moat #1 ("importers cannot follow down without destroying their margin stack") is
backwards. What DeepGrid owns is **cannibalisation immunity** — no global ASP to
defend. Cutting India ADAS silicon to $10 sets a reference price every OEM cites, hence
the stripped regional SKU response, i.e. BP-1A risk 10.

## 3. Channel margin is unaffordable before tapeout

At 20% of ASP a dealer earns ₹46,000 on the kit vs ₹6,000 on a ₹30k box — 7.7× the
rupees, and still better per bay-hour at 4–6 hours' fitment. Margin is not the constraint;
working capital is. Ten kits at cost tie up ₹18.4L vs ₹2.4L for ten boxes, and 60 days' carry
at the 11–13% BP-1A itself uses costs ~₹37,000 — 80% of one unit's margin. Kits are
carriable only on consignment or confirmed order; §6 is silent.

Affordability: 20% given away leaves ₹1.19L (52% GM) at ASIC phase — workable. At
FPGA phase it leaves ₹58,000, cutting GM 45%→25% and raising the opex-covering
volume from 400–600 kits to ~690–1,030 against an FY27 plan of **130**. The July deck's
direct, founder-led motion is right; BP-1A §6 making channel the primary near-term engine
is not — a live contradiction between the documents.

NBFCs are mis-ranked second. **[STRUCTURAL]** At 13% over four years, ₹2.3L of extra
principal yields ~₹67,000 interest at zero inventory or warranty risk — the dealer's whole
margin without the dealer's risk.

## 4. Insurer co-funding: right mechanism, wrong sizing, contradicted internally

BP-1A §6 makes insurer co-funding a primary near-term engine. The July deck scores
insurers **last** (2.15/5, 43.0%), labels them ANTI-ICP / "NEVER (SALES)", bans any
premium-reduction % (sl.6), and stop-lists insurer selling "ever". Both cannot go to an
investor. A subsidy S is rational where **P·L·δ·N ≥ S** (premium, loss ratio, claims reduction, years
retained), so δ ≥ S/(P·L·N). **[STRUCTURAL]** N is the killer: Indian commercial motor is
annual and price-churning, so at N=1 a ₹1.15L subsidy needs the kit to erase roughly a full
year's expected claims. It requires N≥3 — a multi-year fleet programme, organised
segment only. Three further conditions **[STRUCTURAL]**: exposure must be third-party
bodily-injury *severity* (uncapped in Indian law), making the pitch TP-tail relief rather than
premium discount; the delta must be attributable, which BP-1A's data-rights clause covers;
and the subsidy must book as claims cost, not acquisition expense, or it hits IRDAI
expense-of-management limits — absent from both documents.

Sizing: fleet-telematics programmes typically evidence 10–25% frequency reduction, so a
rational insurer funds ~20–30% — **₹40,000–70,000, not ₹1.15L** — taking the kit to
₹1.6–1.9L. That is a margin instrument for organised fleets, **not a bridge to the ₹30,000
anchor**, and BP-1A treats it as the latter. Cheapest fix: name an insurer as observer on
pilot one so the delta gets measured at zero cost.

## 5. Asymmetric capital buys design-ins, and the head-start claim is wrong

The deck says Netrasemi raised ₹125 Cr and "ships mid-2027 — a year behind us"
(sl.23/25). The ledger says **₹107 Cr** and A2000 **production-ready May 2026**, three
live OEM trials (E-03/E-04, CONFIRMED). The head start is misstated by ~12 months in the
direction that matters. The ratio is also worse than 107:55: of ₹55 Cr, ₹10 Cr is debt and
₹29.80 Cr tapeout NRE, leaving ~₹15 Cr discretionary — a **4–7× free-capital gap**.

**[STRUCTURAL]** With a closing design-in window the better-capitalised firm prices below
short-run cost, because an OEM socket is durable across a 5–7 year platform. DeepGrid
cannot answer symmetrically: gross profit per kit *is* the opex funding (400–600 kits ×
₹1.04L covers ₹4–6 Cr), so a 20% concession pushes that to ~690–1,030 kits against an
FY27 plan of 130. The 24-month outcome is therefore not a price war lost on price but a
**design-in race lost on timing, with price as the instrument** — concentrated in months
12–18, the AIS-162/188 window BP-1A calls its most important date. Second-order, a
better-funded production-ready peer compresses the Series A valuation the CCPS
conversion ratio is priced against: competitive and financing risk are one risk.

Where capital does not substitute: sovereign/defence — foreign silicon excluded, ₹1.01 Cr
contracted, and Netrasemi's A2000 aimed at IoT/healthcare/surveillance (E-05). Structure
favours the deck's defence-primary call over BP-1A's ADAS-primary build.
