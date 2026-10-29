---
name: deepgrid-sku-compendium
description: "Technical architecture compendium for DeepGrid Semi's 10 SKUs, D100 Drone SoC, DG SDV reference platform, and multi-die organic SiP packaging based on the 14-page Technical Annex v3 (2026)."
---

<!-- argument-hint: [sku name, subsystem, or chapter number] -->

# DeepGrid Semi — SKU Architecture Compendium (Technical Annex v3)

**Author**: Deepgrid Semi Pvt Ltd | **Source**: 14-Page SKU Compendium Annex | **Chapters**: 14 | **Generated**: 2026-09-14

## How to Use This Skill
- **Without arguments** — Load the SKU architecture index, process boundaries, and multi-die packaging rules.
- **With SKU name** — Ask for `BLDC Motor`, `Smart Meter`, `Hi-Rel PMIC`, `Lockstep MCU`, `Transceiver`, `Supervisor`, `Radar`, `Display Driver`, `Zonal Gateway`, or `D100 Drone`.
- **With chapter number** — Ask for `ch01` through `ch14` to inspect pinouts, bus architectures, and Socratic physics trade-offs.
- **Interactive Visual Cockpit** — Launch or inspect via [Silicon Architecture & Vector Cockpit](http://localhost:3456/deepgrid_native_viewer.html) for isolated 300 DPI vector schematics, Dark HUD blueprint filters, and interactive C register maps.

---

## Chapter Index (14 SKU & System Modules)

| # | Chapter Title | Key Subsystem & Node | Sockets & Standards |
|---|---|---|---|
| [ch01](chapters/ch01-overview.md) | **Compendium Overview** | 130nm/180nm Scope Boundary | 9 SKUs + D100 + DG SDV Platform |
| [ch02](chapters/ch02-sku1-bldc-motor.md) | **SKU-1: BLDC Motor Controller** | 130nm BCD, 5–120V Rail, DGridRiscV | FOC CORDIC (<1 µs), AEC-Q100, BEE Fans |
| [ch03](chapters/ch03-sku2-smart-meter.md) | **SKU-2: Smart-Meter SoC** | 130nm, 24-bit $\Sigma\Delta$, <2 µW RTC | Class 0.5S Metrology, 250M Meter Rollout |
| [ch04](chapters/ch04-sku3-hi-rel-pmic.md) | **SKU-3: Hi-Rel PMIC (28V)** | 180nm BCD, Brokaw (12 ppm/°C), DICE FSM | DO-160 / MIL-STD-461, SRIJAN NSG-5962 |
| [ch05](chapters/ch05-sku4-lockstep-mcu.md) | **SKU-4: Lockstep Safety MCU** | 130nm, Dual DGridRiscV (2-cycle skew) | ISO 26262 ASIL-D, $\le 2$-cycle FAULTn Latch |
| [ch06](chapters/ch06-sku5-interface-transceiver.md) | **SKU-5: Interface Transceiver** | 130nm Thick-Oxide 5V LDMOS | RS-485 + CAN-FD, $\pm$15 kV HBM ESD |
| [ch07](chapters/ch07-sku6-voltage-supervisor.md) | **SKU-6: Quad-Rail Voltage Supervisor** | 130nm / 180nm, Chopper, 8 µs Deglitch | MIL-STD-883K Qualification Pathfinder |
| [ch08](chapters/ch08-sku7-77ghz-radar.md) | **SKU-7: 77 GHz MIMO Radar** | 130nm BiCMOS (SiGe $f_T$ 350GHz) + CMOS | 4D Imaging, 3.75 cm Res, DO-160G Airborne |
| [ch09](chapters/ch09-sku8-display-driver.md) | **SKU-8: Rugged Display Driver** | 130nm HV (0–12V Amps), 1280x10b DACs | BEL 17" SXGA Display, PIL-5 Item #5 |
| [ch10](chapters/ch10-sku9-sdv-zonal-gateway.md) | **SKU-9: SDV Zonal Gateway** | 130nm, ASIL-D Island, TSN Switch | 16x Smart Fuses, EVITA-Full HSM, CAN-XL |
| [ch11](chapters/ch11-track-b-d100-drone-soc.md) | **Track B: D100 Drone SoC** | 130nm, PX4 Loop + 30 Hz EKF VIO | Hardware Failsafe Island, DGCA Type Cert |
| [ch12](chapters/ch12-dg-sdv-platform.md) | **DG SDV Platform Reference** | 64-bit AXI4 Matrix + AXI-REALM QoS | Triple-Lockstep Safe Domain + RV64 Linux |
| [ch13](chapters/ch13-sip-integration.md) | **SiP Multi-Die Packaging** | 4-layer Organic Substrate BGA 15x15 | 6 Wire-Bond Mature Dies + 1 Flip-Chip 28nm |
| [ch14](chapters/ch14-node-roadmap.md) | **Node & SKU 3-Phase Roadmap** | 130/180nm $\rightarrow$ 90/55/45nm $\rightarrow$ 28nm | Arithmetic Check (~50 SKUs by Year 5) |

---

## Supporting Files
- [glossary.md](glossary.md) — Acronyms, electrical parameters, and bus interfaces.
- [patterns.md](patterns.md) — Circuit design patterns (CORDIC PID, 2-cycle lockstep, organic SiP).
- [cheatsheet.md](cheatsheet.md) — SKU parametric reference and qualification matrix.
