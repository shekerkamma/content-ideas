# Chapter 13: System-in-Package (SiP) Multi-Die Composition

## Core Idea / Thesis
A cost-effective, high-yield packaging architecture that integrates six mature-node wire-bonded dies (power, transceiver, supervisor, MCU, driver, AFE) with a single flip-chip 28 nm high-speed compute die on a 4-layer organic BGA substrate, deliberately avoiding expensive UCIe/silicon interposer packaging.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 13 (System-in-Package Architecture) — How the Dies Compose

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Package Format** | BGA 15x15 mm (Ball Grid Array) on a **4-Layer Organic Substrate** |
| **Die Count & Bonding** | **6x Wire-Bonded Mature Dies (130nm/180nm)** + **1x Flip-Chip 28 nm Compute Die** |
| **Integrated Dies** | SKU-3 (PMIC), SKU-1 (Motor Driver), SKU-5 (Transceiver), SKU-6 (Supervisor), SKU-4 (MCU), DG-AFE, 28nm AI Die |
| **Inter-Die Interconnect** | Standardized substrate trace routing: SPI / UART / GPIO / Direct Power Tree (**Deliberately NOT UCIe**) |
| **Power Distribution** | Centralized power tree distributed directly from on-package SKU-3 Hi-Rel PMIC |
| **System Supervision** | Single on-package SKU-6 monitors all inter-die voltage rails and asserts master system `RESETn` |
| **Wave 2 Scaling** | High-performance 28 nm AI-compute die (D100 Core) joins after ₹50 Cr capital raise on identical substrate |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| SiP: SIX MATURE DIES + ONE 28nm COMPUTE DIE ON ONE 4-LAYER ORGANIC SUBSTRATE     |
| (= SDV Domain Controller / D100 UAV Compute Module)                               |
+===================================================================================+
| Inter-Die Bus: Substrate SPI / UART / GPIO | Central Power Tree from SKU-3 PMIC    |
+-----------------------------------------------------------------------------------+
|  [SKU-3 PMIC]  [SKU-1 DRV]  [SKU-5 XCVR]  [SKU-6 SUP]  [SKU-4 MCU]  [AFE]  [28nm AI]|
|     (Wire)        (Wire)       (Wire)        (Wire)       (Wire)    (Wire) (Flip-Chip)
+-----------------------------------------------------------------------------------+
| 4-LAYER ORGANIC SUBSTRATE: Power Delivery Network (PDN) + Escape Routing          |
+-----------------------------------------------------------------------------------+
| BGA 15x15 mm BALL ARRAY (Solder Balls to Carrier PCB)                             |
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **Why "Deliberately Not UCIe"**: Why did DeepGrid reject UCIe (Universal Chiplet Interconnect Express) and silicon interposers in favor of standard wire-bonded SPI/UART/GPIO on organic substrates for mature-node defence systems?
2. **Thermal Expansion & Warpage (CTE Mismatch)**: How does the 4-layer organic substrate handle differential thermal expansion coefficients between thick silicon dies (130nm wire-bonded) and the thin 28nm flip-chip die across -55°C to +125°C thermal cycling?
3. **Substrate PDN Impedance & Voltage Droop**: What decoupling capacitor strategy is embedded on the 15x15 BGA package to keep high-frequency dynamic current transients from the 28nm AI core from causing voltage droop on sensitive analog AFE rails?
4. **KGD (Known Good Die) Testing Flow**: How does DeepGrid test and screen each individual die before SiP assembly to prevent compounding package yield losses?

## Policy, Market & Procurement Hook
- **Mature-Node Packaging at Mature-Node Cost**: Eliminates dependencies on advanced Taiwanese/US packaging foundries (TSMC CoWoS, Intel EMIB).
- **Module Deliverable**: Provides Indian defence systems integrators (DRDO, BEL, ideaForge) with a complete plug-and-play SDV domain controller or UAV compute brick.

## Connects To
- **Chapter 4 (SKU-3)**: Generates all sequenced voltage rails inside the package.
- **Chapter 7 (SKU-6)**: Provides package-level brownout and fault latching.
- **Chapter 11 (D100)**: Serves as the physical packaging standard for the tactical drone brain.
