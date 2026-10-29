# Chapter 5: SKU-4 — Lockstep Safety MCU (ISO 26262 ASIL-D Path)

## Core Idea / Thesis
A dual-core RISC-V microcontroller operating in a 2-cycle temporal diversity lockstep configuration with end-to-end ECC on the bus fabric, providing instant hardware fault detection ($\le 2$ cycles) for mission-critical automotive, aerospace, and robotics control.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 5 (Figure 13 in Plain Edition Whitepaper) — Lockstep Microcontroller

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Process Node** | 130 nm CMOS (SkyWater SKY130 / IHP SG1302 / SCL eNVM) |
| **CPU Architecture** | Dual DGridRiscV Cores (RV32IM_Safety) running at 200 MHz |
| **Lockstep Skew** | 2-cycle temporal delay on Core 1 (prevents common-mode voltage/EMI glitching) |
| **Comparator Latency** | Hardware bus + retire comparator asserts `FAULTn` within **2 clock cycles** |
| **Memory Subsystem** | 1 MB Flash (SECDED ECC) / 256 KB ECC SRAM + XTS-AES QSPI interface |
| **Interconnect** | AHB-Lite 32-bit with end-to-end parity & ECC protection @ 200 MHz |
| **Safety Peripherals** | Redundant Timers (PWM/IC/OC), Windowed Safety Watchdog, CRC-32 Engine |
| **Communications** | 2x CAN-FD with dedicated message RAM, 2x SPI, 4x UART, JTAG Boundary Scan |
| **Standards Compliance** | ISO 26262 ASIL-D, IEC 61508 SIL-3, DO-254 DAL-A, AEC-Q100 Grade 1 |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| LOCKSTEP SAFETY DOMAIN (ASIL-D):                                                  |
|   DGridRiscV Core 0 (Primary)   --> [Pipeline & Retire Stage] --\                 |
|   DGridRiscV Core 1 (+2 cycles) --> [Delay Buffers / Retire]  ---> [COMPARATOR] -> FAULTn
+-----------------------------------------------------------------------------------+
| MEMORY WITH END-TO-END ECC:                                                       |
|   1 MB eFlash (ECC) | 256 KB SRAM (SECDED) | AHB-Lite 32-bit Bus with Parity      |
+-----------------------------------------------------------------------------------+
| SYSTEM & DEBUG: PLIC (64 interrupts) | DMA (8-ch) | Dual JTAG + Safety Watchdog   |
+-----------------------------------------------------------------------------------+
| COMMUNICATIONS & ANALOG: CAN-FD x2 | SPI x2 | 12-bit 2Msps SAR ADC x2 | Timers    |
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **Temporal Delay Buffer Synchronization**: How does the 2-cycle delay pipeline buffer memory load/store operations to ensure both cores see identical read data when accessing asynchronous AHB peripherals without causing pipeline stalls?
2. **Single-Point Fault Metric (SPFM) > 99%**: What internal built-in self-test (LBIST / MBIST) routines are executed during power-on and periodic runtime windows to achieve ISO 26262 ASIL-D certification?
3. **Interrupt Jitter & Asynchronous Events**: How are external asynchronous interrupts synchronized to the 2-cycle skewed cores so that both pipelines take the trap vector on the exact matching logical cycle?
4. **Fail-Safe Actuator Isolation**: When `FAULTn` is asserted by the comparator, what hardware interlock forces external PWM gate signals into a high-impedance safe state without relying on software intervention?

## Policy, Market & Procurement Hook
- **Replaces**: Microchip SAM-DA1, Renesas RH850, and Infineon AURIX ASIL-D functional-safety microcontrollers in EV battery management systems (BMS), motor-safety supervision, brake-by-wire, and drone autopilots.
- **TAM & Pricing**: 3–10M units/yr India TAM @ $4–12 ASP band (~$0.3–0.5B addressable market).
- **Silicon Node Path**: FPGA 81.25 MHz validation $\rightarrow$ 130 nm ASIC @ 200 MHz. Open-PDK v1 uses ROM+SRAM+XTS-QSPI; SCL eNVM for monolithic flight parts.

## Connects To
- **Chapter 2 (SKU-1)**: Acts as the ASIL-D safety monitor for high-power BLDC motor drives.
- **Chapter 11 (D100)**: Serves as the primary flight-critical controller in the D100 drone platform.
