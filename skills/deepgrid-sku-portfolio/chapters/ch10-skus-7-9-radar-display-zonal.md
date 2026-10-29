# Chapter 10: SKU-7 77 GHz radar, SKU-8 rugged display driver, SKU-9 SDV zonal controller
*Whitepaper §9.7–9.9; Compendium sheets SKU-7 to SKU-9*

## Core Idea
The last three SKUs show three kinds of honesty on the sheet itself: a radar whose process choice is physics and whose risk is printed on the figure, a display driver with the closest thing to a named government socket and date, and a zonal controller that explicitly disclaims the central car computer.

## Frameworks Introduced
- **Partition at the ADC (SKU-7)**: put the RF (chirp synthesiser, PAs, four LNA/mixer/IF chains) on an IHP SiGe HBT die and everything digital from the ADC onward on a 130 nm CMOS die. Gen-1 automotive partitioning.
  - When to use: any mixed RF/digital part where the RF needs a specialist process.
  - Why it works: each die uses the cheapest process that meets its physics; the digital half can be FPGA-validated.
  - Failure mode: scheduling the chip as if FPGA testing reduced RF risk. "The SiGe front end has no FPGA equivalent and is proven on silicon or not at all."
- **The named socket with a date (SKU-8)**: PIL-5 lists a BEL 17-inch rugged SXGA (1280 × 1024) display due December 2027, the most direct hit on any chip in the lists.
- **Reuse made real (SKU-8)**: the cockpit display variant is the same chip with a wider-temperature colour table and a higher-voltage output ring.
- **Scope honesty on the sheet (SKU-9)**: 130 nm at 200 MHz owns the zonal layer (gateway, smart I/O, safety and security edge). Central SDV compute (multi-GHz CPUs, GPU/NPU, LPDDR5) is sub-10 nm and explicitly not claimed.
- **Channels and predictability over clock speed (SKU-9)**: a gateway's limits are channel count and bounded switch delay set by the network standard, not processor MHz.

## Key Concepts
- **SKU-7 77 GHz MIMO radar**: 2TX/4RX; IHP SG13G2 HBTs (ft 350 GHz); 4 GHz sweep → 3.75 cm range resolution; 77 and 24 GHz; CMOS die with 12-bit 40 Msps ADCs, range/Doppler FFT, CFAR, beamforming and tracker.
- **CFAR**: constant false-alarm rate target detection.
- **SKU-8 rugged display driver** (TFT source driver + TCON): LVDS / MIPI DSI in; SXGA at 60 Hz; 1280 × 10-bit column DACs (3,840 column outputs); 0–12 V HV amplifiers; 24 V gate-driver level shift; temperature-compensated gamma; colour chain reverse gamma → colour correction → gamma → dither; frame-freeze BIST (ASIL-B capable); charge-sharing precharge cuts driver power ~40%.
- **SKU-9 SDV zonal controller + gateway**: ASIL-D lockstep island; EVITA-full HSM; secure boot with two slots for rollback, OTA engine; TSN switch (802.1Qbv / 802.1AS); CAN-FD × 8, CAN-XL, LIN × 8, FlexRay (six network types in total); smart fuse × 16.
- **EVITA-full HSM**: automotive hardware security module profile.
- **Zonal architecture**: replaces relay-and-harness boxes; the OEM argues the cost and weight case for you.

## Mental Models
- Use **"the only SKU with simultaneous captive automotive and defence sockets"** for SKU-7: AD2 mirror-tower radar (captive), defence perimeter and counter-UAS, automotive AEB.
- Think of **the highest-value list match as the least specified**: BEL's EW digital receiver and synthesizer (PIL-5, Dec 2026) give no band or dynamic range, and that one answer decides SiGe versus CMOS, one die or two.
- Treat **a disclaimer printed on the figure** as a credibility feature.

## Anti-patterns
- **FPGA-derisking claims for an RF front end**.
- **Claiming central SDV compute at 130 nm**.
- **Desk research instead of a customer conversation** when a spec gates the architecture (action 4: get the BEL EW specification).
- **Quoting SKU-8 or SKU-7 prices without noting the two sources differ** ($3–12 vs $70–110; $8–25 vs $35–60/set).

## Reference Tables

| | SKU-7 Radar | SKU-8 Display driver | SKU-9 Zonal controller |
|---|---|---|---|
| Replaces | imported 77 GHz RF front ends and companion digital chips | Novatek/Himax-class TCON + source drivers (defence MFDs, industrial HMI, rail PIS, auto clusters) | imported zonal controllers and CAN/LIN-to-Ethernet gateways |
| Market (ESTIMATED) | 2–8 M units/yr at $8–25 (§9); FY31 table $35–60/set | 2–6 M/yr at $3–12 (§9); FY31 table $70–110 | 4–12 M/yr at $6–20; ~$0.3–0.7 B addressable, zonal layer only |
| Hook | DMA: RWR for Su-30 MKI and Mi-17, weapon-locating radar, battlefield surveillance (10 and 30 km), shipborne 3D, precision approach radar; PIL-5 BEL EW receiver and synthesizer | PIL-5 BEL 17-inch rugged SXGA display, Dec 2027 | zonal migration away from relay-and-harness |
| Why this process | physics: SiGe HBTs for 77 GHz | HV amplifiers (0–12 V) and 24 V level shift | channel count and predictable timing |
| Status | IHP MPW FY28; separate SiGe test chip required | cycle-3 MPW | waits on a vehicle maker's pilot letter |
| One-time cost | ₹1.4–1.8 Cr (two dies) | ₹0.6–1.2 Cr | ₹0.6–1.2 Cr |
| FY31 row (ESTIMATED) | ~75K → ₹30 Cr; 50–65%; own radar product first | ~55K → ₹40 Cr; 55–70%; buyer and date named | ~0.7 M → ₹35 Cr; 35–50% |

## Worked Example
**Checking the radar resolution claim and partition:**
1. Range resolution = c / (2 × sweep bandwidth) = 3×10⁸ m/s / (2 × 4×10⁹ Hz) = 0.0375 m = 3.75 cm. The sheet's figure is consistent.
2. Which blocks need SiGe? Anything at 77 GHz: chirp synthesiser, PAs, LNAs, mixers, IF chains.
3. Where to cut? At the ADC: 12-bit 40 Msps converters and all DSP (FFT, CFAR, beamforming, tracking) move to 130 nm CMOS.
4. Validation plan: FPGA covers the CMOS half; the SiGe half needs its own test chip; budget ₹1.4–1.8 Cr, not ₹0.6–1.2 Cr.
5. Open question that could change the plan: the BEL EW band and dynamic range may push that family to CMOS or keep it on SiGe.

## Key Takeaways
1. Split RF and digital at the ADC; never let FPGA results stand in for RF silicon.
2. SKU-8 has the clearest government socket and date in the lists.
3. SKU-9 claims the zonal edge only; say what it does not do.
4. The biggest defence opportunity is gated by one unanswered specification.
5. Reconcile the two price sets before quoting SKU-7 or SKU-8.

## Connects To
- **ch04**: SiGe as the one hard process limit.
- **ch11**: SKU-9 as the mature-node edge of the DG SDV platform.
- **ch12**: confirmed government-list matches.
- **ch14**: action 4 (BEL EW specification) and revenue rebalancing toward chips 9, 7 and 4.
