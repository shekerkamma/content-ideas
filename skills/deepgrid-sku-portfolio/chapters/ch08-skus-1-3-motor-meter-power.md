# Chapter 8: SKU-1 motor controller, SKU-2 smart-meter SoC, SKU-3 hi-rel PMIC
*Whitepaper §9 intro, §9.1–9.3; Compendium sheets SKU-1 to SKU-3*

## Core Idea
The first three sheets show the portfolio logic: two mostly-digital commercial chips (motor and meter) go first and carry the revenue, while a genuinely analog, radiation-hardened-by-design power chip earns defence margins on small volume. Each sheet pairs block architecture with a named socket, a policy hook and an FPGA-to-ASIC boundary.

## Frameworks Introduced
- **The SKU sheet anatomy** (every compendium sheet): block architecture, timing behaviour, characteristic curves, market panel (flagged internal estimate), "Replaces", "Socket & policy hook", "Status & node path". Curves are example shapes against targets, not measurements.
- **Two ordering decisions**: commercial chips first (they sell fastest and build credibility; defence versions follow on the same approved silicon at 10–100x prices); the simplest chip goes through approval first (chip 6, ch09).
- **Replace a two-chip set with one die**: SKU-1 and SKU-2 both collapse an imported driver/AFE plus a separate MCU into one chip.
- **Real analog, not a digital wrapper**: SKU-3's credibility rests on genuine analog design (Brokaw bandgap, type-III compensation, telemetry SAR).

## Key Concepts
- **SKU-1 BLDC Motor Controller** (AEC-Q100 · ISO 26262 ASIL-B/C): DGridRiscV at 200 MHz; hardware PID responding in <1 µs; full FOC datapath; PWM × 7; 16-bit ADC; 5–120 V buck/boost rail; ReRAM 256 KB–1 MB non-volatile memory; runtime star/delta switching.
- **SKU-2 Smart-Meter SoC** (Class 0.5S metrology): DG-AFE6 six-channel 24-bit ΣΔ; sinc³ OSR-256; P/Q/S and THD to the 15th harmonic; AES-256 and SHA-256; <2 µW always-on RTC domain; multilayer AHB (4 masters / 9 slaves); tamper-backed RTC.
- **SKU-3 Hi-Rel PMIC** (28 V avionics rail tree): DO-160 / MIL-STD-461 front end; peak-current-mode pre-buck; four sequenced rails with foldback current limiting; Brokaw bandgap 12 ppm/°C; type-III compensation; telemetry SAR; SEU-hardened sequencer FSM (DICE + TMR).
- **No embedded flash on free PDKs**: SKU-2 uses ROM + ECC SRAM + encrypted QSPI; SCL eNVM variant for sealed meters.
- **ReRAM path (SKU-1)**: sky130 experimental module, SCL eNVM fallback.

## Mental Models
- Use **"guaranteed demand + commercial volume"**: SKU-1 is captive in every ASWA robot joint and D100 module, and commercial in EV two/three-wheelers, industrial motors and BLDC fans.
- Think of **tamper detection as a tender requirement, not a feature**: silicon must do it; software cannot add it later.
- Treat **small volume at 60–75% margin, AVL-locked for decades** as a valid product (SKU-3).

## Anti-patterns
- **Counting a PIL match on a whole unit as a chip order**: PIL-5's "BLDC motor with encoder" for an anti-tank missile lists the motor unit, not the chip inside.
- **Claiming rad-hard for SKU-3**: SEU hardening by design (DICE, TMR) only; no dose or latch-up data.
- **Ignoring price exposure on SKU-1**: needs ~1 in 3 such chips sold in India; the most exposed row to Chinese price attack (−40% in the crash case).

## Reference Tables

| | SKU-1 Motor controller | SKU-2 Meter SoC | SKU-3 Hi-rel PMIC |
|---|---|---|---|
| Replaces | DRV83xx-class driver + external MCU (fans, appliances, EV 2W/3W, robotics, ASWA joints) | ADE9153 / V9203-class AFE + separate meter MCU | TI/ADI QML power parts in avionics and vetronics LRUs |
| Market (ESTIMATED) | 5–15 M units/yr at $3–8; BEE fan push ₹250–550 Cr/yr of driver demand | ~250 M meter rollout; 10–30 M/yr at peak; $2–5 | 10–50K units/yr at $50–200 screened; 60–75% GM |
| Policy / demand hook | PIL-5 BLDC motor with encoder, anti-tank missile, Dec 2025 (unit-level) | tamper detection mandated in tenders | SRIJAN NSG-5962; PIL-5 BEL tank DC-DC converters (16–40 V in, 4 A, Dec 2026; 12 V, Dec 2028) |
| Why mature node | 5–120 V natively beside the core | accurate R, C and matched transistors for 24-bit | 28 V input and 0.9 V core on one die; SEU margin from size |
| Status & path | Artix-7 81.25 MHz validation only → 130 nm ASIC at 200 MHz; MPW cycle 1 | FPGA-validated blocks → 130 nm at 200 MHz; cycle 1 with SKU-1 | sky130 20 V devices → SCL 180 nm production; MIL-883 screening |
| Anchor | Airgap Technology (EV motors/powertrains) PLANNED | Ripple Metering (LoRaWAN meters) PLANNED; masks wait for signed letter | none named |
| FY31 row (ESTIMATED) | ~5.5 M units → ₹220 Cr; 30–40% margin | ~19 M → ₹480 Cr; 35–45% | ~45K → ₹55 Cr; 60–75% |

## Worked Example
**Turning the SKU-1 sheet into one labelled pitch paragraph:**
"SKU-1 replaces today's two-chip motor set (a DRV83xx-class driver plus an MCU) with one 130 nm die that carries a 5–120 V converter beside the processor, which a newer process cannot do. Demand is captive in our ASWA joints and D100 modules, and our estimate for Indian EV and industrial motors is 5–15 million units a year at $3–8 (ESTIMATED). The FPGA version at 81.25 MHz is validation only; the product targets 200 MHz on 130 nm, first MPW in cycle 1 (PLANNED). Airgap Technology is the first named buyer (PLANNED)."
Note what is left out on purpose: no unlabelled volume, no FPGA speed as performance, no PIL unit listing presented as a chip order.

## Key Takeaways
1. SKU-1 and SKU-2 are mostly digital, commercial and first: they carry early revenue.
2. SKU-2's masks wait on Ripple's signed letter; the rule is visible on the biggest revenue line.
3. SKU-3 proves real analog capability and earns screened margins on small volume.
4. Free PDKs lack flash: plan ROM + ECC SRAM + encrypted QSPI, SCL eNVM later.
5. Always label market panels as internal estimates.

## Connects To
- **ch04**: why each needs a mature node.
- **ch09**: SKU-4 sits beside SKU-1 as the FOC brain.
- **ch12**: no buyer, no build; unit-level PIL matches.
- **ch13**: SKU-1 and SKU-2 in the crash case and stop rule S1.
- **ch14**: SKU-1 and SKU-2 production masks in the round.
