# Chapter 3: SKU-2 — Smart-Meter SoC (Class 0.5S Metrology)

## Core Idea / Thesis
An integrated single-die metrology and communications SoC combining a high-dynamic-range 24-bit $\Sigma\Delta$ analog front end with hardware tamper detection, cryptographic security, and an ultra-low-power (<2 µW) always-on RTC domain.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 3 (Figure 11 in Plain Edition Whitepaper) — Smart Meter SoC

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Process Node** | 130 nm CMOS (SkyWater SKY130 / IHP SG1302 / SCL eNVM fallback) |
| **Metrology Engine** | DG-AFE6: 6-channel 24-bit $\Sigma\Delta$ ADC with sinc³ filter (OSR-256) |
| **Accuracy Class** | Class 0.5S Metrology ($P, Q, S$ active/reactive/apparent power + THD-15 harmonic analysis) |
| **Compute Core** | Custom DGridRiscV (RV32IM_SEU) @ 200 MHz |
| **Bus Fabric** | AHB-Lite Multilayer 32-bit (4 masters / 9 slaves @ 200 MHz) |
| **Always-On Power Domain** | PMU + RTC domain consuming **<2 µW** (32.768 kHz crystal, 2.2V - 3.6V backup battery) |
| **Cryptographic Security** | DG-SE: Hardware AES-256, SHA-254 engine with Secure Boot and Tamper Key Erase |
| **Peripherals** | DLMS/COSEM UART, Segment LCD driver (4x40 seg), Optical Port, Case-Open Tamper Logic |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| METROLOGY: DG-AFE6 (6-ch 24b Sigma-Delta) -> Decimator (sinc3 OSR-256) -> Metro Eng |
+-----------------------------------------------------------------------------------+
| COMPUTE & SECURITY: DGridRiscV Core | DMA (4-ch) | DG-SE (AES-256/SHA-254)         |
+-----------------------------------------------------------------------------------+
| ALWAYS-ON DOMAIN (<2uW): Ultra-low-power PMU + RTC (32.768 kHz) + Tamper Sense   |
+-----------------------------------------------------------------------------------+
| AHB-LITE MULTILAYER MATRIX: 32-bit, 4 Masters / 9 Slaves, 200 MHz                 |
+-----------------------------------------------------------------------------------+
| PERIPHERALS: Segment LCD (4x40) | DLMS/COSEM UART | Tamper Case Switch | Timers   |
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **$\Sigma\Delta$ Chopper Noise & Offset Drift**: How does the DG-AFE6 maintain Class 0.5S active power accuracy across a 1000:1 dynamic current range without temperature calibration drift over the 15-year meter lifespan?
2. **Neutral Tamper Immunity**: When an external magnetic field (>0.5 Tesla) or DC current injection is applied to defeat metrology, how does the AFE detect phase/neutral imbalance and switch to single-wire Rogowski coil measurement?
3. **Always-On Power Gating & Battery Retention**: What is the leakage current through the isolation cells separating the 200 MHz core domain from the <2 µW RTC domain during a 30-day grid blackout?
4. **eFlash vs eNVM Constraints**: How does DeepGrid handle non-volatile memory on open-PDK 130nm where embedded flash is unavailable (using ROM + ECC SRAM + encrypted QSPI vs SCL eNVM)?

## Policy, Market & Procurement Hook
- **Replaces**: Analog Devices ADE9153 / Vango V9203 AFE + external STMicroelectronics meter MCU two-chip architecture.
- **National Mandate**: India National Smart Metering Programme (RDSS) rolling out **~250 Million smart prepaid meters** (10–30M units/yr peak).
- **ASP & TAM**: $2–5 ASP band; domestic tender requirement mandating tamper detection and indigenous cryptographic trust.
- **Silicon Node Path**: FPGA-validated blocks $\rightarrow$ 130 nm ASIC @ 200 MHz. Cycle-1 MPW alongside SKU-1.

## Connects To
- **Chapter 6 (SKU-5)**: RS-485 transceiver for wired RS-485 meter bus.
- **Chapter 7 (SKU-6)**: Voltage supervisor for brownout protection.
