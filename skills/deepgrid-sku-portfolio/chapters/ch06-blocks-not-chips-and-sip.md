# Chapter 6: Blocks, not chips; and the SiP
*Whitepaper §6–6.5; Compendium "SiP Integration" sheet*

## Core Idea
A shared die like TinyTapeout proves building blocks, not chips. Changing that one word turns an unbelievable "1,000 chips" into a credible compounding strategy: a silicon-tested block library feeding ~50 approved chips, later composed into multi-die packages.

## Frameworks Introduced
- **What a shared die can and cannot do**: TinyTapeout tiles (~0.02 mm², a few hundred to a few thousand gates, one design active at a time) cannot provide: space for a sellable chip; analog or high voltage (digital-only wrapper); many simultaneous pins; datasheet measurements (noise, PSRR, accuracy over temperature).
- **The change of word**: a tile is a building block, not a chip. A chip means a datasheet, an approval, a test programme and an AVL place.
  - Say: "1,000 silicon-tested building blocks, combining into about 50 approved chips, 10–20 of them in volume."
  - Never say: "1,000 chips in five years."
- **Three validation levels** (each ~1,000x apart in cost; spend hundreds of dollars to learn what would cost ₹1 Cr):
  1. Shared die (TinyTapeout type): digital block, $100–500, proves the block works in silicon; 5-yr count 1,000.
  2. Shared factory run: full chip, ₹14.3 L sky130 / ₹34–80 L IHP, proves the chip meets spec; 5-yr count 50.
  3. Dedicated mask set: production chip, ₹1 Cr+, proves volume shipment; 5-yr count 10–20.
- **Two entry routes**: digital blocks enter at level 1; analog and high-voltage blocks cannot and must enter at level 2 as their own test chips. Any plan putting the PMIC or radar front end on a shared tile is wrong.
- **Facing the precedent**: the shared-run programme that popularised sky130 produced several hundred designs over four years with major corporate funding and no commercial range of approved chips. Three stated differences: those runs were almost all level 1; they had no protected demand; Deepgrid sells approved chips, not runs. If unconvinced, this is the weakest part of the plan on past evidence, which is why the round must prove levels 2 and 3.
- **The compounding library**: a block proven once is reused everywhere; the lockstep comparator tested for chip 4 makes chip 9's safety island and D100's backup system believable. The five-year asset is the library, not the tile count.
- **Two self-critiques**: custom die-to-die links (deliberately not UCIe) save area and power but prevent selling bare dies, so the standard must be chosen now if dies may ever be sold; packaging is a supply chain not yet in the plan.

## Key Concepts
- **Tile**: ~0.02 mm² slot on a shared die.
- **Building block**: a reusable digital function (motor datapath, tuning loop, meter filter, fault table, noise filters, lockstep comparator, display timing generator, network shaper, crypto cores, memory controller, radar processing control).
- **SiP**: system in package; the goal is six chips in one package (power, motor drive, comms, safety, control, analog), with the 28 nm AI die joining later.
- **KGD**: known-good die; test each die before assembly or one bad die scraps the package.
- **UCIe**: industry chiplet standard, deliberately not used.

## Mental Models
- Use **"learn at the cheapest level that can answer the question"**.
- Think of **the library as the moat**: a competitor needs the same five years to copy it.
- Treat **a well-known precedent as something to address first**, before the reader raises it.

## Anti-patterns
- **Calling a tile a chip**: an informed investor rejects it immediately and then discounts every other number.
- **Putting analog or HV blocks on a shared tile**.
- **Choosing a custom die interface without deciding whether dies will ever be sold**.
- **Planning a multi-die package without per-die testing**.

## Reference Tables

| SiP attribute (compendium) | Value |
|---|---|
| Substrate | 4-layer organic |
| Package | BGA 15 × 15 |
| Die attach | wire-bond × 6 mature dies + flip-chip × 1 (28 nm compute) |
| Die-to-die | SPI / UART / GPIO over substrate, deliberately not UCIe |
| Power | tree from SKU-3 |
| Supervision | SKU-6 supervises the package |
| Wave 2 | 28 nm AI-compute die (D100 core) joins after the ₹50 Cr round; same substrate, one SDV/UAV module |

## Worked Example
**Routing a block to its validation level:**
- Lockstep comparator (digital) → level 1 shared tile to prove it in silicon → reused in chip 4, chip 9's safety island and D100's failsafe.
- ±15 kV ESD ring for chip 5 (analog/HV) → cannot use a tile → level 2 dedicated test chip with its own pins and supplies → only then a datasheet number.
- Chip 1 production → level 3 mask set once a named buyer exists (ch12) → volume.

## Key Takeaways
1. Blocks are proven on shared dies; chips on shared runs; volume on mask sets.
2. Replace "1,000 chips" with the three-number block/chip/volume statement.
3. Analog and HV blocks start at level 2.
4. Address the sky130 shuttle precedent head-on.
5. Decide the die-interface standard and add KGD testing before committing to a SiP.

## Connects To
- **ch04**: the 50-SKU arithmetic correction.
- **ch09**: lockstep comparator reuse.
- **ch11**: the SDV platform and D100 die that the SiP composes.
- **ch12**: KGD as a cost and schedule line.
