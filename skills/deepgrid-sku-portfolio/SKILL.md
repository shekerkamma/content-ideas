---
name: deepgrid-sku-portfolio
description: "Knowledge base from Deepgrid Semi's \"Mature-Node Silicon for India's Defence and Industrial Base\" (plain-language whitepaper v3, September 2026) and its SKU Architecture Compendium v3. Use when applying Deepgrid's frameworks for mature-node chip strategy, the 10x cost model, the 198-day tapeout loop, blocks-not-chips, qualification and supplier approval, defence and commercial go-to-market, stop rules, or when referencing the nine SKUs, the D100 drone SoC and the DG SDV platform."
---

<!-- argument-hint: [topic, SKU number, framework name, or chapter number] -->

# Deepgrid Semi: Mature-Node Silicon and the SKU Portfolio
**Sources**: DeepGrid Whitepaper, Plain-Language Edition v3 (71 pp, Sept 2026, ₹10 Cr angel/seed) + SKU Architecture Compendium v3 (14 sheets, investor and DPSU diligence annex) | **Chapters**: 14 | **Generated**: 2026-09-13

**Published with the owner's authorization.** Both source documents were marked Confidential; this skill is a synthesized summary released with Deepgrid's approval. Figures are the sources' own and mostly ESTIMATED; keep the claim labels when reusing them.

## How to Use This Skill

- **Without arguments**: load the core frameworks below
- **With a topic**: ask about `stop rules`, `IDDM`, `198-day loop`, `SKU-7`; I read the matching chapter first
- **With a chapter**: ask for `ch09`; I load that file
- **Browse**: ask what chapters exist

For anything not covered below, read the chapter file before answering. Quote figures with their claim label (DONE, DESIGNED, PLANNED, ESTIMATED).

---

## Core Frameworks & Mental Models

**1. The thesis, and the word that carries it: "cannot".** An older process (130/180 nm), a free PDK and an automated open flow cut the cost of a finished, tested, low-volume chip about 10x: ₹0.6–1.2 Cr all-in versus $2–5 M the normal way. The claim is not "cleverer than TI"; it is that four bills on TI's list are not on Deepgrid's (outsourced layout $1–2 M, tool licences $0.5–1 M/yr, a full mask set $0.5–1 M, 12–18 months of design). That makes 10,000-unit/yr programmes profitable at 60–75% gross margin, and Indian procurement law then keeps the customer. Use this framing; never argue Deepgrid wins at 10 M units (it would lose). → ch02

**2. Label every claim.** DONE = a chip exists or an order is signed. DESIGNED = circuit code works on test hardware. PLANNED = a tracked date, not a claim. ESTIMATED = Deepgrid's own number with no outside source. Volumes, prices and curves are ESTIMATED unless a source is named. → ch03

**3. Argue with the bottom number, not the top one.** The import funnel: $23.4 bn chip imports (UN COMTRADE HS 8542) → $9 bn made on ≥130 nm → $0.46 bn in the nine chip kinds Deepgrid builds → ₹1,000 Cr FY31 scenario → ₹2.88 Cr live orders today. Lead a sizing conversation from the bottom. → ch01

**4. The law created a buyer imports cannot serve.** DAP-2020 Buy (Indian-IDDM) ranks Indian products first; Positive Indigenisation Lists (PILs) ban named imports after a date; SRIJAN lists items defence companies want replaced; Make-II guarantees an order after successful trials. Caveat Deepgrid raises itself: foreign wafers mean Buy(Indian), not Buy(Indian-IDDM), until SCL Mohali production is real. So SCL is a business need. → ch01

**5. 130 nm for physics, not price.** Thick-oxide and LDMOS devices handle 5–120 V on the same die as a 200 MHz core; bigger transistors resist single-event upsets (design-level protection only, no rad-hard claim); older processes match analog parts better; line drivers need a 5 V-tolerant ring newer nodes lack. Hard limits: 77 GHz needs IHP SiGe; AI accelerators, central SDV compute and swarm control are sub-10 nm problems, partly 28 nm, never 130 nm. → ch04

**6. One loop every 198 days = ≤30 days design + 168 days silicon.** Design is bounded by engineer count; silicon cannot be repeated, so enforce the design-complete gate before the factory window. Two speeds: mostly-digital chips (1, 2, 4, 8, 9) need one cycle plus 6–9 months; mostly-analog chips (3, 5, 6, 7) need 2–3 silicon cycles plus approval. Silicon in hand is not a product: +6–9 months commercial, +9–12 months MIL-883/JSS/CEMILAC for screened parts. → ch05

**7. Blocks, not chips.** Say "1,000 silicon-tested building blocks, combining into about 50 approved chips, 10–20 in volume", never "1,000 chips". Three validation levels, each ~1,000x the cost of the one before: shared-die tile ($100–500, proves a digital block) → shared factory run (₹14.3 L sky130, ₹34–80 L IHP, proves the chip meets spec) → dedicated mask set (₹1 Cr+, proves volume). Analog and high-voltage blocks cannot enter at level 1. The compounding asset is the silicon-tested library. → ch06

**8. One method, three factories, one processor.** sky130/SkyWater (proven, DONE), IHP SG13G2 (radar, PLANNED), SCL Mohali 180 nm (Indian origin and screening, PLANNED). Seven of ten chips share DGridRiscV (RV32IM_Zicsr, machine mode, no cache, no branch prediction, no FPU, no compressed instructions): every omission buys a guaranteed worst case. 200 MHz is a processor target, not a measured or per-chip number. → ch07

**9. Commercial first; simplest chip first through qualification.** The motor controller (chip 1) and meter chip (chip 2) go first and carry early revenue; defence versions follow on the same approved silicon at 10–100x prices. The voltage supervisor (chip 6) is the qualification pathfinder, so MIL-883 surprises land on the simplest die. → ch08, ch09

**10. No buyer, no build.** A chip gets build money only when its buyer has a name: Deepgrid's own product, a government list, a defence filing, a tender requirement, or a signed customer letter. Three buyer clocks: a list entry is permission, not an order (2–4 years of trickle); a defence filing is the real order path (~15–18 months, the only path revenue is counted on); a tender win is the fast clock (plus 6–12 months of vendor registration). → ch12

**11. Two routes, one chip.** Commercial: datasheet → ten-minute fit decision → evaluation board on a credit card → running in a week → terms; any missing item stops the sale. Defence: SRIJAN/PIL item → technical discussion → trial units → Make-II or direct order → approved-vendor list. The lists name boxes, not chips, so the entry is the silicon inside a listed box. → ch12

**12. The customer approves the supplier, not the chip.** An AVL listing needs ISO 9001/AS9100, supplier records, ESD control, wafer traceability, change notification and a second-source or last-time-buy policy. Testing, not design, becomes the bottleneck (₹1.2 Cr line); multi-chip packages need known-good die. → ch12

**13. A crash case travels with every forecast, and stop rules are written in advance.** FY31 re-priced for a Chinese price crash: ₹1,000 Cr → ~₹750 Cr, with the import-banned defence row untouched. Stop rules S1–S4 (meter letter, screening failures, FY29 Chinese price check, SCL delays) have dates and no exceptions. → ch13

**14. The round buys the end of the design story.** ₹10 Cr convertible: six parallel factory runs, four approvals, production masks and first wafer batches for chips 1 and 2, testing, sales. Target state: seven chips in silicon, four approved, two in volume, revenue measured rather than modelled. The D100 is ring-fenced in a separate ₹50 Cr revenue-gated round. → ch14

**15. Say the weakness before diligence finds it.** The sources repeatedly name their own gaps: the unpublished 200 MHz timing analysis, no packaging/test partner, no quality system yet, no tested analog library in a free PDK, a thin 5–7 person team. Adopt the same move when writing for Deepgrid. → ch03, ch14

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-import-gap-and-policy.md) | The import gap, and the law that created a buyer | Import funnel, stacked procurement law, IDDM caveat, why now |
| [ch02](chapters/ch02-cost-model.md) | The 10x cost model, line by line | Four missing bills, "cannot", protected low-end entry |
| [ch03](chapters/ch03-evidence-and-claim-labels.md) | What is done, and how claims are labelled | DONE/DESIGNED/PLANNED/ESTIMATED, board ≠ chip revenue, biggest unproven claim |
| [ch04](chapters/ch04-why-130nm-and-node-roadmap.md) | Why 130 nm, its limits, and the node roadmap | Physics case, free-PDK analog gap, three-phase node plan, 50-SKU arithmetic |
| [ch05](chapters/ch05-198-day-loop.md) | One loop every 198 days | Design/silicon split, two speeds, production supplier, silicon ≠ product |
| [ch06](chapters/ch06-blocks-not-chips-and-sip.md) | Blocks, not chips; and the SiP | Three validation levels, change of word, precedent, compounding library, SiP |
| [ch07](chapters/ch07-factories-and-shared-processor.md) | Three factories and the shared processor | Factory sequence, DGridRiscV, every missing feature is a decision |
| [ch08](chapters/ch08-skus-1-3-motor-meter-power.md) | SKU-1 motor controller, SKU-2 meter SoC, SKU-3 hi-rel PMIC | Sheet anatomy, commercial-first, analog-heavy PMIC |
| [ch09](chapters/ch09-skus-4-6-lockstep-transceiver-supervisor.md) | SKU-4 lockstep MCU, SKU-5 transceiver, SKU-6 supervisor | Lockstep reuse, obsolescence wedge, qualification pathfinder |
| [ch10](chapters/ch10-skus-7-9-radar-display-zonal.md) | SKU-7 radar, SKU-8 display driver, SKU-9 zonal controller | Die boundary at the ADC, named PIL socket, scope honesty |
| [ch11](chapters/ch11-d100-and-dg-sdv-platform.md) | D100 drone SoC and the DG SDV platform | Hardware failsafe island, Track B ring-fence, one architecture many dies |
| [ch12](chapters/ch12-from-chip-to-revenue.md) | From working chip to revenue | Approval steps, testing bottleneck, supplier approval, two routes, no buyer no build, three clocks |
| [ch13](chapters/ch13-competition-crash-case-stop-rules.md) | Competition, the crash case and stop rules | Three blocked answers, low-end trap, crash table, S1–S4, Munger self-audit |
| [ch14](chapters/ch14-the-round-unit-economics-risks.md) | The ₹10 Cr round, unit economics and risks | Allocation, per-chip earn table, wafer arithmetic, tightest link, seven fixes |

## Topic Index

- **198-day loop, 168-day silicon** → ch05
- **200 MHz (target, unproven)** → ch03, ch07, ch14
- **81.25 MHz FPGA figure** → ch03
- **Anchor customers (Airgap, Ripple, MCEME, Chakravayu CPDL)** → ch08, ch09, ch11, ch12
- **Approval / qualification (MIL-883, JSS, CEMILAC)** → ch05, ch12
- **AVL, supplier approval, ISO 9001/AS9100** → ch12
- **Buy(Indian) vs Buy(Indian-IDDM)** → ch01, ch14
- **Claim labels** → ch03
- **Crash case, Chinese prices** → ch13
- **D100 drone SoC** → ch11
- **DAP-2020, PIL, SRIJAN, Make-II** → ch01, ch12
- **DG SDV platform** → ch11
- **DGridRiscV processor** → ch07
- **Die boundary at the ADC (radar)** → ch10
- **FY31 ₹1,000 Cr scenario and split check** → ch01, ch13, ch14
- **Free PDK analog-library gap** → ch04, ch14
- **Government lists: confirmed matches** → ch12
- **IHP SG13G2 SiGe** → ch02, ch04, ch07, ch10
- **Import funnel** → ch01
- **Known-good die (KGD), packaging** → ch06, ch12, ch14
- **Lockstep** → ch07, ch09, ch10, ch11
- **Node roadmap (130/180 → 90/55/45 → 28 nm)** → ch04
- **No buyer, no build; scoreboard** → ch12
- **Production mask set and wafer arithmetic** → ch05, ch14
- **SCL Mohali 180 nm** → ch01, ch05, ch07
- **SiP integration** → ch06, ch11
- **sky130 MPW price** → ch02
- **Stop rules S1–S4** → ch13
- **Support-engineer bottleneck** → ch12
- **Team, runway, use of funds** → ch14
- **Three buyer clocks** → ch12
- **Three validation levels (tile, MPW, mask set)** → ch06
- **TinyTapeout 6** → ch03, ch06
- **Two sales routes** → ch12
- **V2X SKUs 21–22** → ch11

## Supporting Files

- [glossary.md](glossary.md): every key term with definitions
- [patterns.md](patterns.md): reusable techniques (funnel sizing, stop rules, sequencing, partitioning)
- [cheatsheet.md](cheatsheet.md): decision rules, thresholds and tells

---

## Scope & Limits

Covers the two source documents only, as of September 2026. Figures are the sources' own and mostly ESTIMATED; nothing here is measured silicon beyond the 130 nm test chip.

**Known inconsistencies in the sources: check before quoting.**
- Import funnel: ₹1,000 Cr → ₹2.88 Cr is described as "a factor of 35"; the arithmetic is about 347.
- SRIJAN: "37,696 items" (§1.2) versus "over 33,000 items" (§11.3).
- D100 node: the compendium sheet says the product is 130 nm at 200 MHz; the whitepaper puts D100 on TSMC 28 nm as Track B. The whitepaper is the more detailed and newer framing.
- Prices differ between the §9 chip profiles and the §13.5 unit-economics table: display driver $3–12 vs $70–110; radar $8–25 vs $35–60/set; line driver $0.4–1.5 vs $0.5–1.
- Meter-chip share: "72% of our stated volume band" (§13) versus "78 of every 100 meters" (§13.5 table).
- MCEME ₹1.01 Cr is shown as chip-4's contracted anchor, while §3 states all current revenue is FPGA board revenue, not chip revenue.
- §5.3 still says "180 days ends with silicon" after §5 corrected the cycle to 198 days.
- The 200 MHz product clock is a design target. Deepgrid's separate DG32-LITE architecture documents report the lockstep core at ~55–62 MHz post-route with a 50 MHz die clock; reconcile before quoting 200 MHz anywhere.
