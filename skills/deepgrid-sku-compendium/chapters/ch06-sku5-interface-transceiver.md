# Chapter 6: SKU-5 — Interface Transceiver (RS-485 + CAN-FD)

## Core Idea / Thesis
A ruggedized dual-channel physical layer transceiver implementing RS-485 and ISO 11898-2 CAN-FD on a single 130 nm thick-oxide LDMOS die with $\pm$15 kV HBM ESD protection and tight line-timing skew budgeting for maximum cable run lengths.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 6 (Figure 14 in Plain Edition Whitepaper) — Interface Transceiver

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Process Node** | 130 nm Thick-Oxide 5V LDMOS (SkyWater SKY130 / IHP SG13G2 / SCL Fallback) |
| **Channels** | Channel 1: Full/Half-Duplex RS-485/RS-422; Channel 2: High-Speed CAN-FD (up to 5 Mbps) |
| **Output Stage** | 5 V Thick-Oxide LDMOS push-pull drivers with slew-rate limiting and thermal shutdown |
| **Receiver Sensitivity** | Differential input with **30 mV hysteresis** and true failsafe idle/open/shorted circuit bias |
| **Common-Mode Range** | -7 V to +12 V (RS-485) / -12 V to +12 V (CAN-FD), extending to $\pm$36 V with fault-protection variant |
| **ESD Robustness** | **$\pm$15 kV Human Body Model (HBM)** on bus pins (A, B, CANH, CANL) |
| **Line-Timing Budget** | Symmetric driver and receiver propagation delay ($\Delta t_{skew} < 5\text{ ns}$) |
| **Standards Compliance** | TIA/EIA-485-A, ISO 11898-2:2016 (CAN-FD), MIL-STD-883 Method 3015 |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| CHANNEL 1: RS-485 TRANSCEIVER                                                     |
|   Logic Interface (TXD, RXD, DE/REn) -> Pre-Driver -> Output Stage (5V LDMOS) -> [A, B]
|   Receiver (30mV hysteresis) <- Failsafe Bias & ESD+EMC Clamping Array (±15kV)    |
+-----------------------------------------------------------------------------------+
| CHANNEL 2: CAN-FD TRANSCEIVER                                                     |
|   Logic Interface (TXD, RXD, EN/STB) -> Pre-Driver -> Output Stage (LDMOS) -> [CANH, CANL]
|   Dominant/Recessive Receiver <- Dominant Time-Out + ESD Clamping Ring (±15kV)     |
+-----------------------------------------------------------------------------------+
| SHARED: Local Supply (5V & 3.3V I/O) | Clock Generator | Bus Fault Logic          |
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **Why 130nm Thick-Oxide Beats Advanced Nodes**: Why are advanced FinFET nodes (sub-16nm) physically incapable of directly implementing $\pm$15 kV ESD-hardened, 5V-tolerant line drivers without massive external protection arrays?
2. **CAN-FD Asymmetric Propagation Delay & Bit Slicing**: At 5 Mbps data phase, loop delay asymmetry ($t_{loop,rec} - t_{loop,dom}$) eats into the receiver sample point. How does the internal pre-driver maintain $<10\text{ ns}$ delay delta across temperature (-40°C to +125°C)?
3. **Bus Fault Latch-Up & Ground Shift**: When an RS-485 node experiences a $\pm$7V ground potential difference between industrial motor drives, how does the internal substrate tap prevent parasitic SCR latch-up?
4. **Dominant Timeout Protection (TXD Clamping)**: If an upstream microcontroller hangs with TXD driven low, what hardware watchdog timer inside the transceiver forces the bus driver into recessive mode within 1.5 ms?

## Policy, Market & Procurement Hook
- **Replaces**: Texas Instruments, Analog Devices, and Renesas interface transceivers (the classic FSC-5962 military sourcing-bar wedge).
- **High-Volume Attach Socket**: Ships with every node on every industrial and defence bus (20–60M units/yr attach volume in India).
- **Unit Economics**: $0.40–1.50 ASP band; indispensable "attach part" that locks in system-level BOM wins.
- **Silicon Node Path**: 130 nm thick-oxide $\rightarrow$ SCL/IHP. Cycle-2 MPW.

## Connects To
- **Chapter 3 (SKU-2)**: Provides the RS-485 communication link for smart meter networks.
- **Chapter 10 (SKU-9)**: Interfaces with the CAN-FD/CAN-XL network on software-defined vehicles.
