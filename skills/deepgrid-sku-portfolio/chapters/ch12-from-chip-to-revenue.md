# Chapter 12: From working chip to revenue
*Whitepaper §10–11.3*

## Core Idea
Working silicon is not a product and an approved chip is not revenue. Deepgrid budgets approval, testing and supplier qualification as explicit lines, sells the same approved chip through two very different routes, and releases build money only to chips whose buyer has a name.

## Frameworks Introduced
- **What approval actually buys (₹40–80 L per chip, commercial grade)**:
  1. Characterisation across process, voltage and temperature on enough units for real datasheet limits.
  2. Reliability: high-temperature life, temperature cycling, humidity, ESD and latch-up.
  3. Defence screening: burn-in, electrical test at temperature extremes, package seal leak test, MIL-883 / JSS / CEMILAC paperwork.
  - Five of eight screened-chip steps are calendar-bound; money does not shorten them.
  - Approval needs material from more than one wafer batch; for analog screened chips that means extra factory runs. Hence four approvals funded, not seven.
- **Testing becomes the bottleneck before design does**: test programmes, test boards and machine time are outside the approval budget; now a separate ₹1.2 Cr line. In a multi-die package test time multiplies, and every die must be tested before assembly (KGD).
- **The customer approves the supplier, not the chip**: an AVL listing is granted to a company after an audit: ISO 9001 or AS9100, approved-supplier records, ESD controls, wafer-level traceability, a change-notification process, and a second source or last-time-buy policy. Cheap next to a mask set, but it takes calendar time and an owner.
- **Two ways to sell the same chip** (same approved silicon, prices 10–100x apart):
  - **Commercial (self-service)**: datasheet → engineer decides fit in ten minutes → buys an evaluation board by credit card → running in a week → commercial terms. Any missing item stops the process; a part not in stock or findable in search does not exist.
  - **Defence (relationship-led, law-protected)**: find the item on SRIJAN or a PIL → technical discussion with the defence company → trial units → Make-II or direct order → approved-vendor list. Small companies win at the trial stage.
- **Lists name boxes, not chips**: reading PIL-5 (346 items, OCR'd) and DMA lists 1, 2, 3 and 5 directly found no chip-level items; entries are LRUs, assemblies and spares. Entry is one level down: the silicon inside a listed box.
- **No buyer, no build**: a chip gets build money only when its buyer has a name: Deepgrid's own product needs it, a government make-in-India list names it, a defence filing names it, a tender asks for it, or a customer signs a letter. Nothing else counts, "not enthusiasm, not a market report, not a deadline".
- **Three buyer clocks** (mixing them up is how forecasts lie):
  - **A list entry**: permission, not an order; ban on the list date, orders trickle over 2–4 years; never counted in this year's number.
  - **A defence filing**: file, build a sample at own cost, pass trials (~15–18 months), then the order is assured by rule; the only path revenue is counted on.
  - **A tender win**: the fast clock (meters, fans); hidden step, vendor registration takes 6–12 months.

## Key Concepts
- **AVL**: approved-vendor list; being on it lets a buyer purchase from you.
- **KGD**: known-good die; per-die testing before package assembly.
- **LRU**: line-replaceable unit.
- **Scoreboard (Sept 2026)**: 11 chips may spend (1 Airgap, 3, 4 MCEME, 5, 6, 7, 8 BEL Dec 2027, 10 Chakravayu CPDL, the security chip, the drone-navigation helper); 4 wait on one signature (chip 2 Ripple's letter, chip 9 a vehicle maker's pilot, the cockpit display controller riding chip 8's buyer, the avionics power part opening when chip 3 passes screening); 8 on hold including V2X SKUs 21–22.
- **Support-engineer bottleneck**: 50 chips × 5–10 design-ins each ≈ 300 customers in support at once; measured 25–35 customers per engineer; next round funds 10–12 support engineers.
- **Sales and working capital**: ₹1.0 Cr for datasheets, evaluation kits, distributor setup and stock.

## Mental Models
- Think **"size of the door, not our order"** when quoting third-party order books.
- Use **"which clock is this buyer on?"** before putting any number in a forecast year.
- Treat **quality-system readiness as a precondition of the defence route**, not a later polish.

## Anti-patterns
- **Pitching a listed box as if you will build it**: supply the silicon inside it.
- **Counting list entries as orders**.
- **Hiding test cost inside approval** or ignoring KGD in a SiP plan.
- **Assuming AVL status follows good silicon** without an audited quality system.

## Reference Tables

| List | Item | Owner / platform | Due | Deepgrid match |
|---|---|---|---|---|
| PIL-5 | BLDC motor with encoder | anti-tank missile | Dec 2025 | chip 1 |
| PIL-5 | DC-DC converter, 4 A, 16–40 V in | BEL · tank | Dec 2026 | chip 3 |
| PIL-5 | DC-DC converter 12 V | BEL · tank | Dec 2028 | chip 3 |
| PIL-5 | Isolation amplifier | BEL · tank | Dec 2028 | nearby |
| PIL-5 | Digital receiver (SDC V2) | BEL · electronic warfare | Dec 2026 | chip 7 family |
| PIL-5 | Synthesizer | BEL · electronic warfare | Dec 2026 | chip 7 family |
| PIL-5 | 17-inch rugged display | BEL · Defence Electronics | Dec 2027 | chip 8 |
| PIL-5 | Radio altimeter | HAL · Dornier | Dec 2025 | chip 7 variant |
| PIL-5 | Magnetometer | HAL · LCH | Dec 2025 | nearby |
| DMA | Radar warning receiver | Su-30 MKI, Mi-17 | Dec 2025 | chip 7 family |
| DMA | Weapon-locating / battlefield radar | Army | 2022–26 | chip 7 family |
| DMA | Power amplifiers 10 W, 2–4 kW | Air Force | Dec 2021 | IHP SiGe |
| DMA | Manpack SDR | all services | Dec 2022 | future |
| DMA | IRNSS receiver; GNSS jammer; spoofing | Navy / Air Force | Dec 2022 | future |
| DMA | Proximity fuze, 76/62 SRGM | Navy | — | future |

| Buyer facts, Sept 2026 (door size, not Deepgrid orders) | |
|---|---|
| Smart meters | 20.33 Cr sanctioned; 7.24 Cr installed by June 2026; ~5 Cr in live tenders (Haryana, MP, Punjab, Tamil Nadu); scheme to March 2028; Genus order book ₹24,020 Cr (18 M meters/yr plant); Adani Energy >4.7 Cr meters |
| Defence | 6th import-ban list Aug 2026: 405 items, ~₹3,070 Cr; >33,000 SRIJAN items; ₹7,572 Cr orders already placed with Indian vendors |
| Drones | Army origin teardowns; ₹137 Cr and ₹105 Cr ideaForge orders; ₹40,000 Cr emergency procurement |
| EVs | 14 lakh e2W in FY26 (+22%); >2 lakh in July 2026; controller makers TVS, Bajaj, Ather, Hero Vida, Ola |

## Worked Example
**Classifying three buyer signals before forecasting:**
- "Chip 8 matches PIL-5's BEL rugged display, due Dec 2027." → List entry: permission; the buyer is named so chip 8 may spend under no-buyer-no-build, but no revenue is counted from the list itself.
- "A defence company wants trial units of chip 3 for a tank converter." → Defence filing path: ~15–18 months to an assured order; eligible for revenue counting once trials pass.
- "Ripple Metering is in discussion for chip 2." → Tender/commercial path, waiting on one signature; masks do not start until the signed letter (stop rule S1, ch13).

## Key Takeaways
1. Budget approval, testing and supplier qualification as three separate lines.
2. Build a quality management system alongside the first factory run.
3. Sell one approved chip twice: self-service commercial and relationship-led defence.
4. Target the silicon inside listed boxes, not the boxes.
5. Spend only on chips with a named buyer, and forecast each buyer on its own clock.

## Connects To
- **ch05**: time from silicon to product.
- **ch08–ch11**: per-chip anchors and hooks.
- **ch13**: stop rules and the self-audit that produced "permission mistaken for orders".
- **ch14**: testing line, sales line and the packaging-partner gap.
