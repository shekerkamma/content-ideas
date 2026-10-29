# Chapter 7: SKU-6 — Quad-Rail Voltage Supervisor (Latched Fault)

## Core Idea / Thesis
A precision analog monitoring IC that supervises four independent power supply rails using chopper-stabilized comparators and 0.1%-matched polysilicon resistor ladders, featuring an 8 µs digital deglitch counter and serving as DeepGrid's MIL-STD-883 qualification pathfinder.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 7 (Figure 15 in Plain Edition Whitepaper) — Voltage Supervisor

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Process Node** | 130 nm CMOS / 180 nm BCD (SkyWater SKY130 $\rightarrow$ SCL Mohali Production) |
| **Monitored Rails** | 4 Channels: VIN1 (5.0V), VIN2 (3.3V), VIN3 (1.8V), VIN4 (1.2V / 0.9V adjustable) |
| **Comparator Topology** | Chopper-stabilized precision comparators with sub-millivolt input offset voltage ($V_{os} < 500\text{ µV}$) |
| **Threshold Accuracy** | 0.1%-matched polysilicon resistor divider network with OTP trim |
| **Deglitch Architecture** | **8 µs digital deglitch filter counter** (blocks high-frequency power supply noise without slowing real fault response) |
| **Voltage Reference** | Curvature-corrected bandgap generator: **10 ppm/°C** temperature coefficient |
| **Watchdog Function** | Independent windowed watchdog timer (WDT) with adjustable timeout (100 ms – 1.6 s) |
| **Outputs** | Latched `FAULTn` output (open-drain) + delayed system `RESETn` (200 ms timeout) |
| **Standards Compliance** | MIL-STD-883K Class B / Space Class V Screening Flow |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| SENSE CHAINS (x4):                                                                |
|   VIN1 -> Resistor Divider (0.1% match) -> Chopper Comp -> Deglitch (8µs) ->\     |
|   VIN2 -> Resistor Divider (0.1% match) -> Chopper Comp -> Deglitch (8µs) ---> [FAULT
|   VIN3 -> Resistor Divider (0.1% match) -> Chopper Comp -> Deglitch (8µs) --->  MATRIX]
|   VIN4 -> Resistor Divider (0.1% match) -> Chopper Comp -> Deglitch (8µs) ->/     |
+-----------------------------------------------------------------------------------+
| REFERENCE & TIMEBASE: Curvature-Corrected Bandgap (10 ppm/C) | OTP Trim | Osc (1MHz)
+-----------------------------------------------------------------------------------+
| WATCHDOG: Window Logic (WDI input) -> Timeout Gen -> Fault Assert                 |
+-----------------------------------------------------------------------------------+
| OUTPUT STAGE: RESETn (200ms Delay) | FAULTn (Latched Open-Drain) | MRn (Manual Reset)
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **The Deglitch Design Story**: How does the 8 µs digital counter provide immunity against switching noise from DC-DC buck converters without exceeding the maximum allowable fault detection latency before MCU memory corruption?
2. **Chopper Residual Ripple Filtering**: Chopper stabilization eliminates DC offset but creates high-frequency modulation ripple at the chopping frequency. What low-pass filtering is integrated before the fault latch?
3. **Resistor Ladder Matching & Aging**: Over a 20-year deployment in high-temperature military avionics, how does polysilicon resistance drift impact the 0.1% divider ratio?
4. **Qualification Pathfinder Strategy**: Why did DeepGrid select SKU-6 as the first chip through MIL-STD-883 environmental and screening flows, and how does this establish the baseline for all subsequent SKUs?

## Policy, Market & Procurement Hook
- **Replaces**: Texas Instruments, Maxim Integrated, and Analog Devices supervisor ICs.
- **Socket Penetration**: Present on nearly every PCB; universal attach part (30–80M units/yr attach volume in India).
- **Pricing**: $0.20–0.80 commercial ASP; **$20–80 screened MIL-STD-883 grade** (10–100x pricing multiplier).
- **Silicon Node Path**: Simplest die in the portfolio $\rightarrow$ fast-tracks SCL Mohali fabrication. Cycle-1 MPW.

## Connects To
- **Chapter 4 (SKU-3)**: Cross-monitors all rails produced by the Hi-Rel PMIC.
- **Chapter 5 (SKU-4)**: Holds the Lockstep Safety MCU in reset until voltages stabilize.
