# Chapter 1: SKU Compendium Overview & Scope Boundary

## Core Idea / Thesis
Mature-node silicon (130nm/180nm) is the linchpin of India's defence and industrial sovereignty, capturing the high-reliability, mixed-signal, and high-voltage sockets where sub-10nm nodes are physically unsuited or cost-prohibitive.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3 (Technical Annex)
- **Sheet Reference**: Page 1 Overview — Nine SKUs + D100 Drone SoC + DG SDV Platform

## Physical & Electrical Scope Boundary
| Domain | Mature Node (130nm / 180nm) | Sub-28nm / Sub-10nm Boundary |
|---|---|---|
| **Voltage Rails** | 5V – 120V High Voltage & BCD | Sub-1.0V Core Logic Only |
| **Mixed-Signal** | 24-bit $\Sigma\Delta$ ADC, 10-bit Column DACs, SiGe 77GHz RF | Digital baseband only, external AFE required |
| **Harsh Environment** | -55°C to +125°C, MIL-STD-883K, AEC-Q100 Grade 0 | Limited thermal margin, susceptible to SEU |
| **Mask / Tapeout Cost** | $50K – $200K per MPW run | $5M – $50M+ per mask set |
| **Primary Sockets** | Gate pre-drivers, PMICs, Transceivers, Supervisors, Zonal Edge | Central Cockpit AI compute, Autonomous Driving HPC |

## Subsystem Architectural Portfolio
- **Industrial & Mobility Motion**: SKU-1 BLDC Motor Controller (FOC CORDIC, 120V pre-drivers)
- **Infrastructure Metrology**: SKU-2 Smart-Meter SoC (Class 0.5S 24-bit AFE, <2 µW RTC)
- **Avionics & Vetronics Power**: SKU-3 Hi-Rel PMIC (28V input, DO-160, SEU-hardened FSM)
- **Functional Safety Core**: SKU-4 Lockstep Safety MCU (ISO 26262 ASIL-D, 2-cycle temporal skew)
- **Robust Field Bus**: SKU-5 Transceiver (RS-485 + CAN-FD, 5V thick-oxide, $\pm$15 kV HBM)
- **System Integrity**: SKU-6 Quad-Rail Voltage Supervisor (Chopper comparators, 8 µs deglitch)
- **Radar Perception**: SKU-7 77 GHz 4D MIMO Radar (IHP SG13G2 SiGe Front-End + 130nm CMOS Baseband)
- **Rugged Visuals**: SKU-8 Display Driver (BEL 17" SXGA line-item, 0–12V column DACs, TCON)
- **Automotive Backbone**: SKU-9 SDV Zonal Gateway (ASIL-D island, TSN switch, 16x smart fuses)
- **Tactical Autonomous Drone**: Track B D100 SoC (PX4 loop, 30 Hz EKF VIO, isolated hardware failsafe)

## Deep Engineering Questions & Failure Modes
1. **ASIC vs FPGA Boundary**: Why does DeepGrid enforce that analog/mixed-signal blocks (SiGe 77 GHz, 120V pre-drivers) have zero FPGA equivalent and must be validated on MPW silicon directly?
2. **Foundry Portability**: How does DeepGrid de-risk supply-chain embargos across SkyWater 130nm (USA), IHP Microelectronics (Germany), and SCL Mohali (India)?
3. **Packaging Thermals**: What are the thermal dissipation limits of a 15x15 BGA organic substrate containing 6 mature dies and 1 high-speed compute die under 100°C ambient engine bay conditions?

## Key Takeaways
1. 130nm/180nm owns the physical interface to sensors, actuators, and high-voltage power rails.
2. Central compute belongs at sub-10nm, but every central processor requires 5–10 mature satellite chips to interact with the real world.
3. Domestic sourcing moats (Make-II, PIL, NSG-5962) protect mature-node silicon from generic commodity displacement.
