# Chapter 9: SKU-8 — Rugged Display Driver (TFT Source Driver + TCON)

## Core Idea / Thesis
A high-voltage mixed-signal display driver integrating a Timing Controller (TCON) and 1280-channel 10-bit source driver on a single 130 nm HV die with temperature-compensated gamma curves and frame-freeze Built-In Self-Test (BIST) for military multi-function displays (MFDs) and industrial cockpits.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 9 (Figure 17 in Plain Edition Whitepaper) — Display Driver

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Process Node** | 130 nm HV CMOS (0–12V High-Voltage Output Amps, 24V Gate-Driver Level Shift) |
| **Display Resolution** | SXGA (1280 x 1024) @ 60 Hz / WXGA / Full HD Cockpit Displays |
| **Column Outputs** | **1280 x 10-bit Column DACs** with charge-sharing precharge (cuts driver power by ~40%) |
| **High-Voltage Amplifiers** | 0 to 12 V rail-to-rail high-speed analog output amplifiers |
| **Video Interfaces** | Dual-channel LVDS Receiver (655 Mbps/lane) / MIPI DSI / Parallel RGB |
| **Gamma Calibration** | 14-bit programmable Gamma Look-Up Table (LUT) with temp-sensor feedback |
| **Functional Safety** | Frame-Freeze BIST (ASIL-B capable, detects frozen display frames in flight cockpits) |
| **Standards Compliance** | MIL-STD-810G, MIL-STD-883K, DEF-STAN 00-35, ISO 26262 ASIL-B |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| VIDEO INPUT: LVDS RX (dual-ch) | DSI RX (4-lane) -> Line Buffer (4 lines x 1280 x 24b)
+-----------------------------------------------------------------------------------+
| PIXEL PIPELINE: De-Gamma -> Colour Space Conversion -> Gamma LUT (14b) -> Dither  |
+-----------------------------------------------------------------------------------+
| TIMING & SAFETY: TCON (programmable porches) -> Frame-Freeze BIST -> PLL (100MHz) |
+-----------------------------------------------------------------------------------+
| HIGH VOLTAGE COLUMN DRIVERS:                                                      |
|   1280x 10-bit DAC Bank -> 0-12V Output Amplifiers -> 1280 Column Lines to Panel  |
+-----------------------------------------------------------------------------------+
| ROW & BACKLIGHT INTERFACE: Gate Driver Level Shift (24V) | VCOM Gen | Ambient LED |
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **Why 130nm Wins for Display Drivers**: Why are sub-28nm digital nodes incapable of integrating the 0–12V thick-oxide high-voltage amplifiers and 24V level shifters needed to drive rugged cockpit LCD panels directly?
2. **Charge-Sharing Pre-Charge Power Reduction**: How does the charge-sharing scheme between adjacent column lines recover energy and reduce dynamic power consumption by 40% during full-screen video refresh?
3. **Flight Safety & Frame Freeze Detection**: In a military fighter jet or combat vehicle, how does the frame-freeze BIST logic compare successive frame CRC signatures to alert the pilot within 2 frames if the display graphics freeze?
4. **Sunlight Contrast & Temperature-Compensated Gamma**: At cockpit ambient temperatures (+85°C in direct desert sunlight), how does the on-chip temperature sensor dynamically adjust the 14-bit Gamma LUT to maintain optical contrast?

## Policy, Market & Procurement Hook
- **Direct DPSU Policy Anchor**: **PIL-5 Line Item #5**: Bharat Electronics Limited (BEL) 17-inch rugged SXGA display due December 2027 (named socket directly on the Ministry of Defence Positive Indigenisation List).
- **Replaces**: Novatek, Himax, and Sitronix imported TCON + source driver chipsets in military MFDs, naval consoles, train Passenger Information Systems (PIS), and automotive digital clusters.
- **TAM & Pricing**: 2–6M units/yr @ **$3–12 ASP band**. Cycle-3 MPW.

## Connects To
- **Chapter 4 (SKU-3)**: PMIC generates the sequenced analog voltages for display bias.
- **Chapter 10 (SKU-9)**: Interfaces with the vehicle graphics pipeline.
