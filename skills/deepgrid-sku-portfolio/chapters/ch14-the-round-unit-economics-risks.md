# Chapter 14: The ₹10 Cr round, unit economics and risks
*Whitepaper §13–15*

## Core Idea
The ₹10 Cr round is sized to end the "design story": seven chips in silicon, four approved, two in volume production, and revenue measured rather than modelled. The document breaks its FY31 scenario into per-chip rows, checks its own arithmetic, names what does not hold, and lists the seven fixes that come first.

## Frameworks Introduced
- **Size the round to a state change, not the end goal**: the round is not sized to reach FY31; it is sized to reach the point where an institutional round is priced on evidence instead of a story.
- **Fund a production batch inside a seed round**: a prototype chip costs ~₹14,300 (₹14.3 L / 100); a production chip carries only ₹120–260 of mask cost spread across the batch. No volume makes more prototype runs better than one mask set. "The prototype run proves the chip. Only the mask set can sell it."
- **Break one number into ten arguable rows**: the FY31 ₹1,000 Cr is split per chip so a reader can challenge any single row.
- **Check your own split**: divide each chip's FY31 share by its price to get units and market share needed. The total holds (capping every chip at 30% share still carries ₹1,324 Cr) but the split does not: 70% of FY31 sits on two chips. Rebalance toward chips 9, 7 and 4 before the institutional round. Caveat: reading volume bands as target inside larger categories gives 11–30% shares; concentration survives either reading.
- **Fix the tightest link by sequencing, not money**: chips arrive 3 March 2027 (CI2609) and 25 May 2027 (CI2612), leaving ~4 months to production by September 2027. Put chips 1 and 2 on CI2609.
- **Show the small team the budget can buy**: 5–7 engineers (1 senior, 3 mid, 2 junior, of whom 2 analog) on ₹2.4 Cr over 24 months, founder pay partly deferred. Thin against four analog-heavy chips, which is why the round funds four approvals, not seven, and schedules chips 5, 7 and 8 later.
- **Seven fixes in order of value** (five doable in 60 days, none needing the round):
  1. Publish what the 130 nm test chip actually cost and what was on it (did it contain analog?).
  2. Run and publish the sky130 timing analysis per chip (turns 200 MHz from target to fact).
  3. Get the production price quote in writing.
  4. Get the BEL electronic-warfare specification (settles SiGe vs CMOS for chip 7's family).
  5. Replace target numbers with measured ones when the first batch returns.
  6. Name the packaging and testing partners.
  7. Publish the TinyTapeout 6 project link.
- **What we are asking you to believe**: not out-engineering TI; not FY31 as a forecast. Only that an older process, free kit and automated method take ~10x out of low-volume chip cost; that silicon exists; that the law created a buyer who cannot use imports; that ₹10 Cr puts seven chips into approved silicon. The technology risk is mostly retired; the production risk (free-kit design through a full run and dedicated mask set to an approved, listed part) is what the round buys.

## Key Concepts
- **The instrument**: ₹10 Cr angel/seed on a simple convertible, capped below the institutional round; D100 ring-fenced.
- **Runway**: 24 months; average ~₹41 L/month, early-weighted to engineering, late to masks and approval.
- **Production output**: 94,000–165,000 chips from production masks and first wafer batches for chips 1 and 2, worth ₹2–9 Cr at stated prices; FY27 needs 100,000 units at $4.50 average (covered); FY28 needs 707,000 units (~11 more batches per chip, working capital, not in this round).
- **Wafer arithmetic inputs**: 200 mm wafer, 3 mm edge exclusion, 90% usable after scribe lanes, 85% yield, 25 wafers per batch; chip 1 at 8–15 mm², chip 2 at 6–10 mm² (the sensitive input).
- **Two genuinely unresolved risks**: the 200 MHz timing analysis, and no named packaging and testing partner. Everything else has a controllable fix.
- **Data room (ready now)**: sky130 manufacturing files and TinyTapeout 6 project, generated processor RTL, FPGA timing and utilisation reports, three signed customer contracts, scanned government lists, and the source files for every drawing.

## Mental Models
- Think of **the seed as buying the first invoice**: a round that stops at prototypes yields 600 unsellable chips and a forced re-raise.
- Use **"one approval, two prices, two markets"** to explain why FY31 coverage is plausible.
- Treat **a total that holds with a split that does not** as a rebalancing task, not a failure.

## Anti-patterns
- **Funding prototypes only**.
- **Presenting FY31 as a forecast** rather than a scenario.
- **Quoting a team size the budget cannot pay**.
- **Leaving the two unresolved risks off the first page of diligence**.

## Reference Tables

| Allocation | ₹ Cr | Buys |
|---|---|---|
| Factory runs and masks | 3.6 | ₹0.86 Cr six sky130 runs + ₹0.48 Cr IHP SiGe = ₹1.34 Cr prototypes; ₹2.26 Cr two production mask sets and first wafer batches |
| Engineering | 2.4 | design, verification and layout staff |
| Approval | 1.8 | four approvals incl. one MIL-883 first-through |
| Testing | 1.2 | test programmes, boards, machine time |
| Sales and working capital | 1.0 | datasheets, evaluation kits, distributor setup, stock |

| Milestone / revenue scenario | When |
|---|---|
| All 6 prototypes made and tested | Mar 2027 |
| Commercial production (motor + meter first) | Sep 2027 |
| ₹4 Cr (₹2.88 Cr already live) | FY27 |
| ₹28 Cr; defence batches enter screening | FY28 |
| ₹140 Cr; 3–4 more chips; meter volume ramps | FY29 |
| ₹410 Cr; AVL listings build; screened prices | FY30 |
| ₹1,000 Cr: meters 480, motors 220, defence 200, drone-related 100 | FY31 |

| Chip | Price | FY29 units → ₹ Cr | FY31 units → ₹ Cr | Margin |
|---|---|---|---|---|
| 1 Motor controller | $3–8 | ~1.0 M → 40 | ~5.5 M → 220 | 30–40% |
| 2 Smart-meter chip | $2–5 | ~2.4 M → 60 | ~19 M → 480 | 35–45% |
| 3 Power chip (28 V) | $50–200 screened | ~8K → 8 | ~45K → 55 | 60–75% |
| 4 Safety processor | $4–12 | ~60K → 5 | ~0.35 M → 40 | 45–65% |
| 5 Line driver | $0.5–1 | ~0.2 M → 3 | ~1.4 M → 22 | 40–70% |
| 6 Voltage watchdog | $0.2–0.8 | ~0.5 M → 2 | ~3 M → 13 | 40–70% |
| 7 Radar front end | $35–60/set | ~5K → 4 | ~75K → 30 | 50–65% |
| 8 Display driver | $70–110 | ~6K → 5 | ~55K → 40 | 55–70% |
| 9 Vehicle gateway | $6–20 | ~50K → 3 | ~0.7 M → 35 | 35–50% |
| 10 Drone brain (D100) | $60–100 | ~15K → 10 | ~110K → 65 | 45–55% |
| **Total** | | **140** | **1,000** | |

All cells ESTIMATED. One-time cost per chip ₹0.6–1.2 Cr (radar ₹1.4–1.8 Cr). Every chip except 5 and 6 earns back its one-time cost in its first year of sales.

## Worked Example
**Reproducing the FY31 split check for chip 2 (method; the percentages are the source's, the unit arithmetic is a reconstruction):**
1. FY31 row: ₹480 Cr. Convert at ₹95.39/$: ≈ $50.3 M.
2. Mid price ($3.50) → ≈ 14.4 M units. Against the midpoint of the 10–30 M/yr band (20 M) that is ≈ 72%, the figure the source states. The motor chip, run the same way, needs 42%.
3. Top of both bands: the source gives 34% (meter) and 19% (motor).
4. Stress test: cap every chip at 30% share and the nine chips still carry ₹1,324 Cr. The total holds; the split does not: 70% of FY31 sits on two chips, while chips 9, 7 and 4 are planned at under a tenth of theirs.
5. Reading caveat the source adds: treating the bands as targets inside larger categories (category sizes exist for only five chips) gives 11–30% of category instead of 42–72% of market. Concentration survives either reading, so rebalance before the institutional round.

## Key Takeaways
1. The round buys production masks for chips 1 and 2; prototypes alone cannot invoice.
2. Split the headline number per chip and test each row against price and share.
3. Sequence revenue-critical chips onto the earliest shuttle.
4. Show the team the budget pays for, and scope approvals to it.
5. Lead diligence with the two unresolved risks and the seven fixes.

## Connects To
- **ch02–ch03**: cost and evidence claims fix 1 and fix 2 make verifiable.
- **ch05**: shuttle dates behind the tightest link.
- **ch12**: testing and packaging partner gaps.
- **ch13**: crash case and stop rules that travel with this forecast.
