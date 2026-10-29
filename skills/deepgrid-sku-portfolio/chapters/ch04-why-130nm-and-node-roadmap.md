# Chapter 4: Why 130 nm, its limits, and the node roadmap
*Whitepaper §4–4.1; Compendium "Node & SKU Roadmap" sheet*

## Core Idea
130 and 180 nm are the right processes for this chip class for physical reasons: high voltage, radiation tolerance from transistor size, analog matching and 5 V-tolerant I/O. The same honesty requires naming what the process cannot do, and moving only logic-bound parts to finer nodes when channel count demands it.

## Frameworks Introduced
- **The physics case for 130 nm**:
  - **High voltage works**: thick-oxide and LDMOS devices handle 5–120 V, so a 28 V aircraft rail, a 120 V motor supply and a 0.9 V digital core share one die. On newer nodes the power circuits move back onto the board.
  - **Radiation tolerance from size**: larger transistors need more charge to flip; DICE latches and TMR cost area, which older nodes have spare. On chip 3 the hardened sequencer costs a few percent of the die.
  - **Analog works better**: accurate resistors, good capacitors, well-matched transistors (chip 6 claims ±1% from −40 °C to +125 °C).
  - **Line drivers need it**: a 5 V-tolerant thick output ring with strong ESD protection; newer processes lack it, which is why every major interface part is still mature-node.
- **The hard physical limit**: 77 GHz cannot be built on sky130 at all. IHP SG13G2 SiGe HBTs (~350 GHz) are the real 77 GHz radar transistor, so the radar splits into two dies at the ADC (ch10), and its front end cannot be prototyped on an FPGA.
- **The free-PDK problem**: the process is capable, the parts library is not. Free kits have no tested analog blocks (references, rated ESD cells, memory), so chip 5's ±15 kV ring, chip 3's temperature-stable reference and chip 1's memory are targets with no example to copy. Budgeted as its own risk line, larger than the 200 MHz question.
- **What 130 nm cannot do**: high-performance AI accelerators, video-rate object recognition, a central car computer with multi-GHz CPUs and fast memory, drone swarm control. 28 nm gets some; none at 130 nm at any clock. Hence D100 on a separate track and chip 9 limited to the zonal layer.
- **Three-phase node roadmap** (compendium sheet): 130/180 nm ships the catalogue now; 90/55/45 nm takes logic-bound parts from 2028; 28 nm takes compute from 2030.
  - Phase 2 is driven by **channel count and DSP throughput, not speed vanity**: GNSS baseband (90/55 nm), SDR transceiver (SiGe + CMOS), drone navigation co-processor (55/45 nm). Analog I/O rings stay 130 nm where voltage and ESD demand it.
  - Phase 3 boundary, printed on the roadmap: "Everything above is a sub-10 nm problem. 28 nm buys some of it. None of it is claimable on 130 nm, at any clock."

## Key Concepts
- **LDMOS / thick oxide**: high-voltage transistor types available on older processes.
- **DICE latch / TMR**: area-costly protections against single-event upsets.
- **Design-level radiation protection**: the only claim made; no dose figure, no latch-up data, no rad-hard approval.
- **IHP SG13G2**: free 130 nm SiGe process with ~350 GHz HBTs.
- **Analog library gap**: tested analog building blocks missing from free PDKs.
- **Channel-count scaling**: the reason to shrink is parallel lanes and DSP throughput, not clock frequency.
- **50-SKU ramp**: what "10 new SKUs per year" produces over five years.

## Mental Models
- Think **"newer is worse" for power, analog and I/O**; newer is better only for logic density.
- Use **"four chips exist because of the process"**: chip 1 (5–120 V converter beside a 200 MHz core), chip 3 (aircraft input stage + LDMOS + four rails), chip 5 (5 V-tolerant ring), chip 8 (0–12 V into 3,840 outputs).
- Treat **a free PDK as a process without a component shelf**.

## Anti-patterns
- **"Radiation tolerant" as a vague phrase in a defence conversation**: state design-level protection only.
- **Scheduling the radar as if FPGA testing reduced its risk**.
- **"1,000 SKUs by Year 5" alongside "10 new SKUs per year"**: inconsistent by 20x; 10/yr × 5 yr = 50; 1,000 would need 200 tapeouts a year.
- **Claiming central SDV compute or AI acceleration on 130 nm**.

## Reference Tables

| Phase | Node | Parts | Driver |
|---|---|---|---|
| 1 (now) | 130/180 nm | the nine-chip catalogue | voltage, analog, ESD, cost |
| 2 (from 2028) | 90/55/45 nm | GNSS baseband, SDR transceiver, drone nav co-processor | channel count, DSP throughput |
| 3 (from 2030) | 28 nm | compute (D100 core) | performance; sub-10 nm still out of reach |

| Chip | Physical reason it needs a mature node |
|---|---|
| 1 Motor controller | 5–120 V buck/boost beside the core |
| 3 Hi-rel PMIC | DO-160 input, LDMOS stage, four rails, SEU-hardened FSM |
| 5 Transceiver | 5 V-tolerant thick-oxide ring, ±15 kV |
| 6 Supervisor | matched ladders, curvature-corrected bandgap |
| 7 Radar | 77 GHz needs SiGe HBTs (hard limit) |
| 8 Display driver | 0–12 V HV amplifiers, 24 V level shift |

## Worked Example
**The roadmap's self-correction (arithmetic check printed on the figure):**
1. Draft strategy said "10 new SKUs every year" and "over 1,000 active SKUs by Year 5".
2. Check: 10 per year × 5 years = 50. The two figures differ by 20x.
3. Feasibility: 1,000 SKUs would need ~200 tapeouts a year, impossible for a company this size.
4. Decision: show the ~50-SKU ramp and pair it with "1,000 silicon-tested blocks" (ch06), which is the believable version of the same ambition.
5. Principle: "one number, before an investor finds two".

## Key Takeaways
1. Justify 130 nm by physics: voltage, radiation margin, analog matching, I/O.
2. State the hard limits in the same breath as the advantages.
3. The free-PDK analog library gap is a bigger technical risk than 200 MHz.
4. Shrink only when channel count or DSP throughput demands it; keep analog rings at 130 nm.
5. Check your own roadmap arithmetic before publishing it.

## Connects To
- **ch06**: blocks-not-chips replaces the 1,000-SKU claim.
- **ch10**: the radar die partition and chip 9's scope limit.
- **ch11**: D100 as the 28 nm compute track.
- **ch14**: the analog-library risk line.
