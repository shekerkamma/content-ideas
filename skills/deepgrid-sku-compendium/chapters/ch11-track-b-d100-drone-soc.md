# Chapter 11: Track B — D100 Drone SoC (Phase 2 Revenue-Now Silicon)

## Core Idea / Thesis
An integrated UAV system-on-chip combining deterministic real-time flight control (PX4 loop), 30 Hz Visual-Inertial Odometry (EKF VIO), and an optional 10-TOPS edge AI NPU with an isolated hardware failsafe island that guarantees airframe recovery during mission computer lockup or GPS denial.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 11 (Figure 19 in Plain Edition Whitepaper) — Drone SoC D100

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Process Node** | 130 nm CMOS @ 200 MHz fixed (Open-PDK SKY130 / IHP SG1302) |
| **Flight Control Subsystem** | Dual DGridRiscV Cores (RV32IM_Safety) running hard real-time PX4 / ArduPilot loops |
| **Visual-Inertial Odometry** | Dedicated VIO Hardware Engine running 6-DoF Extended Kalman Filter (EKF pose estimation @ 30 Hz) |
| **Camera & Sensor Inputs** | MIPI CSI-2 (2-lane, up to 1080p60) + Hardware Image Signal Processor (ISP) + Dual IMU/MAG/Baro |
| **AI Acceleration (Phase 2)** | Optional 10-TOPS NPU (INT8/INT4 MAC array with 2 MB on-chip SRAM) for YOLO-class target detection |
| **Hardware Failsafe Island** | **100% independent hardware watchdog & safe-state FSM** with isolated power domain, clock, and direct link to ESCs |
| **Memory / Host Storage** | LPDDR4 Interface (2 GB 32-bit) + eMMC / NAND Flash Controller |
| **Standards & Certification** | DGCA Type Certification path, STANAG 4586, MIL-STD-810H |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| FLIGHT CONTROL (Hard Real-Time): DGridRiscV x2 -> IMU/MAG/BARO -> ESC OUT (PWM/DShot)
+-----------------------------------------------------------------------------------+
| VISUAL-INERTIAL ODOMETRY: MIPI CSI-2 -> ISP -> FAST Feature -> EKF Pose Engine (30Hz)
+-----------------------------------------------------------------------------------+
| AI ACCELERATION: 10-TOPS INT8/INT4 NPU -> 2MB SRAM -> YOLO Object Detection Engine
+===================================================================================+
| FAILSAFE ISLAND (THE HARDWARE WEDGE):                                             |
|   Link Monitor (RC loss, GPS denial) -> Safe-State FSM -> Independent Path to ESCs|
|   *BYPASSES Flight Controller, VIO, and AI subsystems completely*                 |
+===================================================================================+
| PLATFORM FABRIC: AXI4 Crossbar (128-bit, 200 MHz) | LPDDR4 32b | GbE | USB3 | PMU |
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **The Failsafe Wedge in Hardware vs Firmware**: Why did DeepGrid implement the emergency safe-state FSM and link monitor as dedicated, isolated hardware rather than a software task inside the PX4 flight stack?
2. **GPS-Denied VIO Localization under Electronic Warfare**: In frontline combat zones (LoC / LAC) with active GPS jamming, how does the 30 Hz geometric EKF VIO maintain $<1\%$ drift per kilometer without requiring cloud or learned AI weights?
3. **Thermal Envelope on High-Speed Maneuvers**: How does the D100 SoC manage thermal dissipation in an enclosed carbon-fiber drone fuselage when running full 1080p ISP processing and flight control loops at +55°C ambient desert temperature?
4. **FPGA-to-ASIC Timing Closure**: The whitepaper notes: *"FPGA prototype validates; product is 130 nm at 200 MHz fixed."* How were critical timing paths in the 128-bit AXI crossbar optimized to meet 200 MHz on open-source PDKs?

## Policy, Market & Procurement Hook
- **Market Sizing & Backing**: India drone market expanding from **$1.2–1.3B to $2.7–3.2B by 2030–34**; SoC ASP band **$100–800**.
- **Domestic Demand**: ideaForge guided 340–450 units in Q4 FY26 alone. Zero indigenous Flight Control + VIO SoCs currently exist in India (critical sovereign vulnerability).
- **Silicon Node Path**: FPGA validates $\rightarrow$ 130 nm ASIC @ 200 MHz. Revenue-now anchor product.

## Connects To
- **Chapter 2 (SKU-1)**: ESC motor drivers controlled by the D100 flight datapath.
- **Chapter 8 (SKU-7)**: Radar sensor fusion for collision avoidance.
- **Chapter 13 (SiP Packaging)**: D100 compute module integrated into multi-die SiP.
