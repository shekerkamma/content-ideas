# Chapter 11: D100 drone SoC and the DG SDV platform
*Whitepaper §9.10 (Track B), §11.2 hold list; Compendium sheets D100 and DG SDV Platform*

## Core Idea
The D100 integrates flight control, visual-inertial odometry and optional AI with a hardware failsafe island no chip company sells, but it is ring-fenced as Track B with separate, revenue-gated money. The DG SDV platform is the reference architecture that ties every die together: "one architecture, many dies".

## Frameworks Introduced
- **The hardware failsafe island (the D100 wedge)**: link monitor → safe-state FSM → independent path direct to the ESC, with isolated power and clock, bypassing flight control, VIO and AI.
  - Why it works: return-to-home becomes a silicon guarantee independent of the mission stack; it is on a DGCA type-certification path.
  - How to de-risk: the block can be built at 130 nm, so prove it on the mature-node chips before committing it to a 28 nm mask set.
- **Track B ring-fence**: D100 is not part of the ₹10 Cr round. It is a separate ₹50 Cr institutional round, gated on revenue, with first silicon targeted early 2027 after that round. "The nine older-process chips fund it. It does not take money from them."
- **Geometry, not learned perception**: VIO is geometric (EKF pose at 30 Hz), so it survives GPS jamming, the LoC/LAC use case.
- **One architecture, many dies (DG SDV)**: the platform reference is secure + safe (triple-lockstep) + Linux host (RV64GCH) + vector and integer accelerator domains on a 64-bit AXI4 matrix with AXI-REALM QoS. SKU-9 is its mature-node zonal edge; D100 its airborne sibling; SKU-3 powers, SKU-6 supervises, SKU-5 connects.
- **A chip on hold is the rule working**: new SKUs without a mandate (V2X SKUs 21–22) wait and spend nothing.

## Key Concepts
- **D100 functions**: PX4/ArduPilot flight-control loop; VIO with EKF pose at 30 Hz; optional 10-TOPS NPU; transformer attention in hardware using integer maths (~70% less power than a general AI accelerator, ESTIMATED); lockstep RISC-V on a DO-254 path; chip cost target under $3.
- **Process**: whitepaper places D100 on TSMC 28 nm (Track B). The compendium sheet says "product is 130 nm at 200 MHz fixed"; treat the whitepaper as authoritative and flag the conflict.
- **Competitor**: Qualcomm QRB5165, the only integrated imported competitor; others do AI or flight control, not both.
- **Indian alternatives**: VyomChakra (flight control only); C-DAC VEGA (research programme).
- **Country-of-origin rules**: components from countries bordering India blocked outright; the Army tears drones down to verify part origin.
- **RV64GCH**: 64-bit RISC-V with hypervisor extension, the platform's Linux host.
- **AXI-REALM**: QoS and isolation on the AXI matrix.
- **V2X SKUs 21–22 (on hold)**: 5.9 GHz RF front end on IHP's RF 130 nm process plus an LTE-class road-safety modem on its digital side, with a message-signing engine from chip 15's block, hosted by chips 4 or 9; 5G V2X is a finer-node problem and not claimed; no Indian V2X mandate yet.

## Mental Models
- Think of **D100 as proof-by-reuse**: its safety block and lockstep core are proven first on cheaper silicon.
- Use **"separate money, separate clock"** whenever D100 appears in a mature-node conversation.
- Treat **the SDV platform as the map** that explains why SKUs 3, 5, 6 and 9 belong together.

## Anti-patterns
- **Drawing D100 spend from the ₹10 Cr round**.
- **Claiming learned perception or swarm control** on this silicon.
- **Presenting ideaForge's volumes or orders as Deepgrid demand**: they size the door, not Deepgrid's orders.
- **Committing an unproven safety block straight to a 28 nm mask set**.

## Reference Tables

| D100 market (sheet and §9.10) | Value |
|---|---|
| India drone market | $1.2–1.3 B (2025) → $2.7–3.2 B by 2030–34 |
| SoC ASP | FC + position tracking $100–300; with AI $500–800 (sheet range $100–800) |
| Demand signal | ideaForge guided 340–450 units in Q4 FY26 |
| Recent Army orders (door size) | ₹137 Cr then ₹105 Cr to ideaForge, only for origin-verified platforms |
| Emergency procurement cycle | ₹40,000 Cr |
| Anchor | Chakravayu CPDL, first external buyer; Deepgrid's own module flies it first (PLANNED) |
| FY31 row (ESTIMATED) | ~110K units at $60–100 → ₹65 Cr; 45–55% margin |

| DG SDV platform role | Die |
|---|---|
| Zonal edge (mature node) | SKU-9 |
| Airborne sibling | D100 |
| Power | SKU-3 |
| Supervision | SKU-6 |
| Connectivity | SKU-5 |

## Worked Example
**Keeping D100 inside the funding boundary in a pitch (reconstructed):**
1. State the opportunity: no Indian chip combines flight control and position tracking; the only integrated competitor is imported.
2. State the wedge: hardware-isolated return-to-home as a chip feature, which no chip company sells.
3. State the money boundary twice: "not part of the ₹10 Cr round; a separate ₹50 Cr institutional round, gated on revenue".
4. State the de-risking path: prove the failsafe island at 130 nm on the mature-node chips first.
5. Label: market figures cited from the sheet; ~70% power saving and <$3 chip cost are ESTIMATED; Chakravayu CPDL anchor is PLANNED.

## Key Takeaways
1. D100's differentiator is the hardware failsafe island, not the NPU.
2. Track B money is separate and revenue-gated; say so every time.
3. Prove shared safety blocks on mature-node silicon before 28 nm.
4. The DG SDV platform explains how the dies compose into one system.
5. Resolve the 130 nm versus 28 nm D100 statement before external use.

## Connects To
- **ch04**: why AI compute is a 28 nm track.
- **ch06**: SiP Wave 2 adds the 28 nm D100 core.
- **ch09**: lockstep reuse from SKU-4.
- **ch10**: SKU-9 as the zonal edge.
- **ch12**: drone buyer facts and the no-buyer-no-build scoreboard.
