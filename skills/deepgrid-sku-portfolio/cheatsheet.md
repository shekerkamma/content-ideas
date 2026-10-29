# Cheatsheet: deciding the way Deepgrid would

## Decision rules
- When a number is stated, **tag it** DONE / DESIGNED / PLANNED / ESTIMATED, because unlabelled estimates read as facts.
- When sizing a market, **lead with ₹2.88 Cr live and walk up**, because the top line invites disbelief.
- When a buyer is unnamed, **do not spend build money**, because enthusiasm, reports and deadlines are not buyers.
- When a list names a box, **pitch the silicon inside it**, because no PIL/DMA entry is a chip.
- When forecasting a signal, **ask which clock**: list (not counted), defence filing (counted, ~15–18 mo), tender (+6–12 mo registration).
- When a block is analog or high-voltage, **start at a dedicated test chip**, because shared dies are digital-only.
- When a part needs 77 GHz, **use IHP SiGe and cut at the ADC**; never schedule RF risk as FPGA-reduced.
- When choosing the first part through MIL-883, **pick the simplest die** (SKU-6).
- When a chip's buyer letter misses its factory-order date, **apply S1**: wait a cycle, move money to chips 1 and 3.
- When quoting speed, **say 200 MHz is an unmeasured processor target**, never a per-chip spec; 81.25 MHz is FPGA-only.
- When asked about radiation, **claim design-level SEU protection only**.
- When asked about central car compute, AI acceleration or swarms, **say not at 130 nm, at any clock**.
- When D100 comes up, **state Track B: separate ₹50 Cr revenue-gated round**, twice.
- When a claim is weak, **disclose it in the evidence section** before diligence finds it.

## Which validation level?
| Question to answer | Level | Cost |
|---|---|---|
| Does this digital block work in silicon? | Shared die tile | $100–500 |
| Does the full chip meet spec? | Shared factory run | ₹14.3 L sky130 · ₹34–80 L IHP |
| Can we ship volume? | Dedicated mask set | ₹1 Cr+ |

## Which factory?
| Need | Factory |
|---|---|
| Cheap first silicon, proven flow | sky130 (SkyWater) |
| 77/24 GHz radar, fast links | IHP SG13G2 |
| "Where is it made?", IDDM, screening in India | SCL Mohali 180 nm |
| Camera sensor | TowerJazz TS13 (paid exception) |

## Thresholds and defaults
| Item | Value |
|---|---|
| Cycle | 30 design + 168 silicon = 198 days |
| After silicon | +6–9 mo commercial; +9–12 mo screened |
| Analog attempts | 2–3 silicon cycles |
| One-time cost per chip | ₹0.6–1.2 Cr (radar ₹1.4–1.8 Cr) |
| Approval per chip | ₹40–80 L (commercial grade) |
| Gross margin, protected low volume | 60–75% |
| Screened price premium | 10–100x |
| Yield / wafer / batch | 85% · 200 mm · 25 wafers |
| Support load | 25–35 customers per support engineer |
| Catalogue ramp | ~50 approved chips by Year 5; 10–20 in volume; ~1,000 blocks |
| Crash case | FY31 ₹1,000 Cr → ~₹750 Cr |
| Share cap test | 30% per chip still carries ₹1,324 Cr |

## Tells and smells
- A forecast that sums to the same total in every revision: **protecting the number**.
- Someone else's order book in your pitch: **borrowed glory**; relabel as door size.
- "1,000 chips": **tile mistaken for chip**.
- Board revenue offered as chip demand: **category error**.
- Every force pushing "build more, faster": **the warning itself**.
- A verbal supplier yes on production: **a hope with a next action**, not a line item.
- A PMIC or radar on a shared tile: **plan is wrong**.
- 70% of a scenario on two chips: **rebalance** toward chips 9, 7, 4.

## Source conflicts to resolve before quoting
Funnel "×35" (actually ~×347) · SRIJAN 37,696 vs >33,000 · D100 130 nm (sheet) vs TSMC 28 nm (whitepaper) · display $3–12 vs $70–110 · radar $8–25 vs $35–60/set · meter share 72% vs 78% · MCEME as chip revenue vs board revenue · 200 MHz vs DG32 docs' 50 MHz die clock.
