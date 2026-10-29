# Chapter 3: What is done, and how claims are labelled
*Whitepaper §3–3.1 and the claim-label key*

## Core Idea
Every claim carries one of four labels, and the evidence section draws its own line between what is proven (a 130 nm chip on the automated flow, ₹2.88 Cr of board orders) and what is not (chip demand, the 200 MHz product clock).

## Frameworks Introduced
- **The four claim labels**:
  - **DONE**: a chip exists, or an order is signed.
  - **DESIGNED**: the circuit code works on test hardware.
  - **PLANNED**: a tracked date, not a claim.
  - **ESTIMATED**: Deepgrid's own number with no outside source.
  - When to use: on every figure in any Deepgrid document, deck or pitch.
  - How: tag the number where it appears, not in a footnote; volumes, prices and performance curves default to ESTIMATED.
- **Board revenue is not chip demand**: ₹2.88 Cr proves Deepgrid can specify, build, sell and deliver a system to an Indian defence or industrial customer. It does not prove anyone will buy its chips (different customer, price and approval process).
- **Name the biggest unproven claim in the evidence section**: the 200 MHz product clock has no published timing analysis, and the PDK it was run against is unclear. Put that disclosure where a diligent reader would look for evidence.
- **Draw the line yourself**: "We would rather you find these on this page than in diligence."

## Key Concepts
- **130 nm test chip (DONE)**: made at SkyWater on Deepgrid's own automated flow; real design file, accepted by a real factory, working silicon returned. Carries the floating-point maths work. Every speed and cost claim rests on it.
- **TinyTapeout 6 design (DONE)**: one of ~500 designs on a 15 × 15 mm sky130 die; public, but the project link is not yet published (action 7 in ch14).
- **₹2.88 Cr revenue (DONE)**: Indian Army via MCEME ₹1.01 Cr under contract (₹23.01 L delivered, ₹78.39 L in progress); Infinis Agritech ₹1.25 Cr for 50 kits (40% advance received); Axitech Solar ₹0.62 Cr for 25 kits. All FPGA-based hardware.
- **DGS001 / DGFP4 board (DONE)**: demonstration hardware sold today.
- **FPGA-validated RTL (DESIGNED)**: lockstep MCU with fault testing, motor-control datapath, meter measurement chain, supervisor sensing chain, drone position engine, on Artix-7 at 81.25 MHz.
- **81.25 MHz**: an FPGA limit reached after eighteen builds with the maths engines included; proves the code is correct and buildable, says nothing about the ASIC.
- **PLANNED dates**: IHP port; SCL Mohali production; all six main prototypes to manufacture by March 2027; commercial production from September 2027.

## Mental Models
- Use **"proves / does not prove" pairs** for every piece of evidence.
- Think of **FPGA speed as a correctness proof, not a performance claim**.
- Treat **an unpublished proof as a claim**: the TinyTapeout link and the timing report are assertions until shown.

## Anti-patterns
- **Presenting ₹2.88 Cr as proof of chip demand**: "the easiest way to mislead you".
- **Quoting 81.25 MHz or 200 MHz as measured chip performance**: the first is an FPGA limit, the second a target.
- **Unlabelled numbers**: an estimate without its label reads as a fact and collapses trust when found.
- **Burying the weakest claim in a risk appendix**: put it where the evidence is.

## Reference Tables

| Status | Item |
|---|---|
| DONE | 130 nm test chip at SkyWater on own flow (floating-point engine on it) |
| DONE | TinyTapeout 6 shared-die design (link to be published) |
| DONE | ₹2.88 Cr orders: MCEME ₹1.01 Cr, Infinis ₹1.25 Cr, Axitech ₹0.62 Cr (board revenue) |
| DONE | DGS001 / DGFP4 demonstration board sold |
| DESIGNED | Lockstep MCU + FI, motor datapath, meter chain, supervisor chain, drone position engine on Artix-7 at 81.25 MHz |
| PLANNED | IHP port; SCL production; six prototypes by Mar 2027; commercial production Sep 2027 |
| UNPROVEN | 200 MHz product clock: timing analysis unpublished, PDK unclear |

## Worked Example
**Stating the revenue line honestly (reconstructed from §3):**
- Fact: "₹2.88 Cr of real orders before any chip exists. DONE."
- Qualifier in the same breath: "This is board revenue built around FPGAs, not chip revenue."
- What it proves: "We can specify, build, sell and deliver a system to Indian defence and industrial customers."
- What it does not: "It does not prove chip demand; a board buyer is a different customer, price and approval process."
- Result: the number keeps its force and loses its capacity to mislead.

## Key Takeaways
1. Tag every figure DONE, DESIGNED, PLANNED or ESTIMATED where it appears.
2. Pair each proof with what it does not prove.
3. The 130 nm test chip is the load-bearing evidence for every speed and cost claim.
4. 81.25 MHz is FPGA-bound; 200 MHz is a target with no published timing report.
5. Disclose the biggest unproven claim inside the evidence section.

## Connects To
- **ch07**: the 200 MHz target and what it is not.
- **ch09**: MCEME shown as chip-4's anchor; reconcile with "board revenue".
- **ch14**: the seven first fixes, starting with publishing the test-chip cost and the timing report.
