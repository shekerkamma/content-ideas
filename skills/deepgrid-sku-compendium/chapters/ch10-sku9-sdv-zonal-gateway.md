# Chapter 10: SKU-9 — SDV Zonal Controller + Gateway

## Core Idea / Thesis
A dedicated 130 nm automotive zonal gateway bridging high-speed in-vehicle networking (CAN-FD, CAN-XL, LIN, FlexRay, 100BASE-T1 Ethernet TSN) to local actuator loads and 16-channel smart electronic fuses, featuring an ASIL-D lockstep safety island and an EVITA-Full Hardware Security Module (HSM).

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 10 (Figure 18 in Plain Edition Whitepaper) — Software Defined Vehicle Zonal Controller

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Process Node** | 130 nm CMOS / BCD (SkyWater SKY130 / IHP SG1302) @ 200 MHz |
| **Safety Island** | Dual DGridRiscV Cores in 2-cycle lockstep (ISO 26262 ASIL-D certified) |
| **Security Subsystem** | EVITA-Full HSM with hardware AES-256, Elliptic Curve (ECC-256), True RNG, and Secure Boot / OTA |
| **Real-Time TSN Switch** | Integrated Time-Sensitive Networking switch supporting IEEE 802.1Qbv (traffic shaping) and 802.1AS (PTP time sync) |
| **In-Vehicle Networking** | 8x CAN-FD, 1x CAN-XL, 8x LIN Masters, 1x FlexRay, 2x 100BASE-T1 Automotive Ethernet |
| **Zonal Power / Smart Fuses** | **16x Smart Electronic Fuses** with programmable current trip limits, $I^2t$ thermal modeling, and diagnostic ADC |
| **Scope Honesty on Sheet** | **130 nm @ 200 MHz owns the ZONAL edge layer only.** Central multi-GHz compute (GPU/NPU/LPDDR5) is sub-10nm and explicitly NOT claimed. |
| **Standards Compliance** | ISO 26262 ASIL-D, AUTOSAR Classic 4.4, EVITA Full, AEC-Q100 Grade 1 |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| SAFETY ISLAND (ASIL-D): DGridRiscV x2 (2-cycle skew) -> Comparator -> Freedom From Interference
+-----------------------------------------------------------------------------------+
| SECURITY & OTA: EVITA-Full HSM | Secure Boot Engine | Dynamic OTA Swap Bank       |
+-----------------------------------------------------------------------------------+
| REAL-TIME CONTROL: TSN Switch (802.1Qbv) | PTP Engine (802.1AS) | Service Router   |
+-----------------------------------------------------------------------------------+
| AXI CROSSBAR MATRIX (64-bit, 200 MHz ASIC Fabric):                                |
|   IN-VEHICLE NETWORKS: 100BASE-T1 x2 | CAN-FD x8 | CAN-XL | LIN x8 | FlexRay      |
|   ZONAL POWER & SMART I/O: Smart Fuse x16 | High-Side Drivers x8 | PWM x12 | ADC 12b
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **Zonal Architecture vs Central HPC Boundary**: Why is 130nm the optimal node for the zonal gateway and smart fuse layer, while central SDV compute must sit on sub-10nm FinFET silicon?
2. **Deterministic TSN Traffic Scheduling**: How does the 802.1Qbv time-aware shaper guarantee $<10\text{ µs}$ bounded latency for critical brake-by-wire messages when bulk infotainment data is simultaneously traversing the 100BASE-T1 port?
3. **Smart Electronic Fuse ($I^2t$) Response vs Pyro-Fuse**: How do the 16 on-chip smart fuses execute microsecond-level solid-state overcurrent cutoffs without suffering avalanche breakdown from wiring harness inductance?
4. **Freedom From Interference (FFI)**: What Memory Protection Unit (MPU) and bus firewall rules isolate non-critical LIN lighting commands from the ASIL-D steering control registers?

## Policy, Market & Procurement Hook
- **Replaces**: Bulky automotive relay boxes, copper wiring harnesses, and discrete NXP/Infineon body control ECUs as OEMs transition to 4-zone zonal architectures.
- **TAM & Addressable Market**: 4–12M units/yr India zonal sockets @ **$6–20 ASP band** (~$0.3–0.7B addressable market).
- **Architectural Link**: Bridges commercial commercial-vehicle ADAS systems and the DG SDV platform.

## Connects To
- **Chapter 5 (SKU-4)**: Leverages the core ASIL-D lockstep design pattern.
- **Chapter 6 (SKU-5)**: Transceiver interfaces for physical bus wiring.
- **Chapter 12 (DG SDV Platform)**: Sits as the zonal edge node of the multi-core SDV reference platform.
