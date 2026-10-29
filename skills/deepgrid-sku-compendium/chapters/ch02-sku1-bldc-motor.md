# Chapter 2: SKU-1 — BLDC Motor Controller SoC

## Core Idea / Thesis
Collapses a two-chip discrete solution (MCU + DRV83xx pre-driver) into a single monolithic 130 nm BCD die with hardware-accelerated sub-microsecond Field-Oriented Control (FOC) and runtime star/delta switching.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 2 (Figure 10 in Plain Edition Whitepaper) — BLDC Controller

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Process Node** | 130 nm BCD / HV CMOS (SkyWater SKY130 / IHP SG13G2 / SCL Fallback) |
| **High Voltage Rail** | 5 V to 120 V Buck-Boost Integrated Pre-Driver Rail |
| **Core Architecture** | Custom DGridRiscV (RV32IM) @ 200 MHz (No license fee) |
| **Memory Subsystem** | 32 KB SRAM (expandable to 256 KB) + 256 KB ReRAM (up to 1 MB) |
| **Current / Phase ADCs** | 16-bit Synchronized ADC (Phase/Bus/Temp) + 3x Current Sense Amps (CSA) |
| **FOC Hardware Engine** | Hardware PID (<1 µs latency) + CORDIC Rect-to-Polar + Clarke/Park Inverse |
| **PWM & Gate Drivers** | 7-channel PWM (up to 200 kHz, 6-bridge + 1 aux) with clock gating per phase |
| **Target Compliance** | AEC-Q100 Grade 0, UL94, ISO 26262 ASIL-B/C |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| 5V - 120V HV POWER PATH: B-B Converter -> PWM x7 -> Pre-Drivers (R/Y/B) -> Star/Delta |
+-----------------------------------------------------------------------------------+
| MIXED SIGNAL: 16-bit ADC (Phase/Bus/Temp) | DAC x4 | Temp Sense | CSA x3          |
+-----------------------------------------------------------------------------------+
| HOST / CONTROL PLANE: DGridRiscV 200MHz | Timers | WDT | I2C/UART/SPI/CAN-FD/JTAG |
+-----------------------------------------------------------------------------------+
| FOC DATAPATH: PID Tuner (<1µs) -> CORDIC -> D,Q->3-Phase -> Sine/Trapezoid Lookup |
+-----------------------------------------------------------------------------------+
| SENSOR FEEDBACK: Hall/Quad/Encoder -> Omega Angle Engine -> Instant Current Amp   |
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **Mixed-Signal Substrate Isolation**: What guard-ring architecture and deep trench isolation (DTI) structures are required to prevent high-voltage inductive switching transients ($dV/dt > 10\text{ V/ns}$ on the 120V half-bridge) from injecting substrate noise into the 16-bit SAR ADC comparator?
2. **Real-Time FOC Bus Contention**: How does the hardware CORDIC datapath arbitrate DMA access to SRAM over the 200 MHz AXI bus while the DGridRiscV core executes background CAN-FD communication without exceeding the <1 µs PID loop deadline?
3. **ReRAM Endurance under Thermal Extremes**: ReRAM retention degrades exponentially at junction temperatures ($T_j > 125^\circ\text{C}$). How does the memory controller implement SECDED ECC and background scrubbing during continuous fan/actuator operation?
4. **Gate Driver Cross-Conduction Protection**: What is the dead-time insertion granularity in the 7-channel PWM engine to ensure zero shoot-through across external MOSFET half-bridges under extreme temperature-induced gate threshold drift?

## Policy, Market & Procurement Hook
- **Replaces**: TI DRV83xx + external MCU two-chip sets in appliances, fans, 2W/3W EV powertrains, robotics, and ASWA defence actuator joints.
- **Policy Anchor**: BEE Star-Rating energy efficiency mandate pushing all ceiling and industrial fans to brushless DC motors (₹250–550 Cr/yr market in fans alone).
- **Target Volume & ASP**: 5–15M units/yr India TAM @ $3–8 ASP band (~$0.4–0.6B market).
- **Silicon Node Path**: FPGA prototype (Artix-7 @ 81.25 MHz) $\rightarrow$ 130 nm ASIC @ 200 MHz. Cycle-1 MPW.

## Connects To
- **Chapter 5 (SKU-4)**: Lockstep MCU for high-safety ASIL-D motor supervision.
- **Chapter 11 (D100)**: Actuator ESC drive for drone flight surfaces.
