# Chapter 9: SKU-4 lockstep MCU, SKU-5 interface transceiver, SKU-6 voltage supervisor
*Whitepaper §9.4–9.6; Compendium sheets SKU-4 to SKU-6*

## Core Idea
These three are the portfolio's safety and attach parts: a productised, fault-injection-tested lockstep core that other chips reuse; a transceiver that wins through obsolescence and sourcing rules; and the simplest die, deliberately sent first through military screening to carry that process for everything behind it.

## Frameworks Introduced
- **Productise a block that already exists**: SKU-4's lockstep RTL exists and is fault-injection tested from the D100 programme; the comparator then underpins SKU-9's safety island and D100's backup (ch06 compounding).
- **The obsolescence wedge (SKU-5)**: replacing a discontinued part is the fastest defence conversation, because the part is already designed into a system that can no longer buy it. The need is an exact electrical match, not a new design win.
- **The qualification pathfinder (SKU-6)**: send the simplest die (one comparator chain, short test list) through MIL-883 first so screening surprises appear on a supervisor, not a four-rail power chip. It also fills the highest socket count (every LRU, every D100 module).
- **Timing budget over raw bitrate (SKU-5)**: skew budget, not data rate, sets node count and cable length; design to it.
- **Deglitch as the design story (SKU-6)**: ignore switching noise without slowing real fault response beyond 8 µs.

## Key Concepts
- **SKU-4 Lockstep MCU** (ISO 26262 ASIL-D path): two DGridRiscV cores running the same program two clock cycles apart (2-cycle skew); bus and retire comparators raise FAULTn within two cycles; ECC end-to-end on the AHB. Flash shown (1 MB ECC) maps to an SCL eNVM variant; the open-PDK v1 uses ROM + SRAM + XTS-QSPI.
- **ASIL-D**: highest ISO 26262 automotive safety integrity level.
- **SKU-5 Interface Transceiver** (RS-485 + CAN-FD): thick-oxide 5 V LDMOS output stages; 30 mV hysteresis receivers; failsafe idle-recessive bias; ±15 kV HBM ESD; common-mode per ISO 11898-2; HV bus-fault variant on SCL or IHP.
- **FSC-5962 sourcing bar**: defence sourcing category that blocks imports of this part class.
- **SKU-6 Voltage Supervisor** (quad-rail, latched fault): chopper-stabilised comparators; 0.1%-matched poly ladders; 8 µs deglitch; curvature-corrected bandgap 10 ppm/°C; windowed watchdog; ±1% accuracy −40 °C to +125 °C.
- **Screened grade pricing**: 10–100x commercial price for individually screened parts.

## Mental Models
- Think of **lockstep as area spent, not speed lost**: older nodes make duplicating the core affordable.
- Use **"attach volume"**: a transceiver ships with every bus node; a supervisor sits on nearly every board.
- Treat **the first screened part as a process probe**, chosen for simplicity rather than revenue.

## Anti-patterns
- **Leading SKU-5 with a new-design pitch to defence**: they need a drop-in electrical match for a discontinued part.
- **Designing a transceiver for headline bitrate** instead of the line-timing budget.
- **Sending the most complex analog chip through MIL-883 first**.
- **Calling the MCEME contract chip revenue** without the §3 qualifier that current revenue is FPGA board revenue.

## Reference Tables

| | SKU-4 Lockstep MCU | SKU-5 Transceiver | SKU-6 Supervisor |
|---|---|---|---|
| Replaces | Microchip / Renesas functional-safety MCUs | TI / ADI / Renesas interface parts | TI / Maxim supervisors |
| Market (ESTIMATED) | 3–10 M units/yr India at $4–12 | 20–60 M/yr attach volume; $0.4–1.5 commercial (§13.5 table: $0.5–1); screened 10–100x | 30–80 M/yr; $0.2–0.8 commercial; screened 10–100x |
| Uses | EV BMS, motor-safety supervision, braking/steering, robot joints, FOC brain beside SKU-1, D100 redundancy | every node on every RS-485/CAN bus | every avionics LRU, every D100 module |
| Why mature node | duplication costs area, not speed; SEU protection cheap enough to keep | newer nodes lack a 5 V-tolerant thick-oxide ring | trimmed reference and matched resistors |
| Status & path | FPGA 81.25 MHz validation → 130 nm at 200 MHz | cycle-2 MPW; HV variant SCL/IHP | sky130 → SCL; cycle 1 or 2; first through MIL-883 |
| Anchor | MCEME, ₹1.01 Cr contracted (₹23.01 L delivered, ₹78.39 L L1) DONE (board revenue per §3) | none named | none named |
| FY31 row (ESTIMATED) | ~0.35 M → ₹40 Cr; 45–65% margin; <1 in 10 of India's safety-chip sales | ~1.4 M → ₹22 Cr; 40–70%; rides with chips 3 and 4 | ~3 M → ₹13 Cr; 40–70%; small money on purpose |

## Worked Example
**Why chip 6 goes through MIL-883 before chip 3 (sequencing walk-through):**
1. The approval clock (MIL-883, JSS, CEMILAC) adds 9–12 months that money cannot shorten; five of eight screened-chip steps are calendar-bound.
2. Unknowns in the screening process are likeliest on the first part through it.
3. Chip 6 has one comparator chain and a short test list; chip 3 has an input stage, LDMOS stage, four rails and a hardened FSM.
4. A surprise found on chip 6 costs a supervisor's schedule; the same surprise on chip 3 would stall the highest-margin defence part and everything queued behind it.
5. Chip 6 also has the highest socket count, so the first screened part is also a broadly useful one.
6. Guard rail: stop rule S2 (ch13) moves defence revenue out 12 months if chip 6 fails screening twice.

## Key Takeaways
1. SKU-4 productises proven lockstep RTL and seeds reuse across SKU-9 and D100.
2. SKU-5 sells on obsolescence and sourcing bars: exact match, not innovation.
3. SKU-6 is chosen first for screening because it is simplest, not most lucrative.
4. Attach parts earn little per unit but carry the defence door for the family.
5. Keep the board-versus-chip revenue distinction on the MCEME anchor.

## Connects To
- **ch06**: lockstep comparator reuse.
- **ch07**: DGridRiscV and fixed-point determinism.
- **ch10**: SKU-9's lockstep island.
- **ch12**: approval steps and calendar time.
- **ch13**: stop rule S2.
