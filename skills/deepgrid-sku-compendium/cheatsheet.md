# DeepGrid Semi — Silicon Architecture & Decision Cheatsheet

## 1. Process Node Selection & Physics Boundary Rules
| Subsystem Function | Target Process Node | Physics / Architectural Rationale |
|---|---|---|
| **High Voltage Power & Drivers** (5V – 120V) | **130nm / 180nm BCD** | Sub-28nm cannot support >3.3V without thick oxide breakdown; BCD integrates power DMOS on-die. |
| **Precision Analog & References** | **180nm CMOS / BiCMOS** | 10–12 ppm/°C Brokaw bandgap and 24-bit $\Sigma\Delta$ ADCs require low $1/f$ flicker noise and large matched poly resistors. |
| **Millimeter-Wave RF Front-End** (77 GHz) | **130nm BiCMOS (SiGe HBT)** | $f_T > 350\text{ GHz}$ required for 77 GHz radar FMCW chirp; standard CMOS lacks transconductance margin. |
| **Logic & DSP Baseband** (100–200 MHz) | **130nm CMOS** | Ultra-low mask cost ($100K–150K), zero static leakage, high thermal reliability at 125°C. |
| **Multi-Channel GNSS / SDR** | **90nm / 55nm / 45nm** | Shrink required for channel count and DSP throughput—**NOT speed vanity**. Analog I/O stays 130nm. |
| **Edge AI Acceleration** (10–50 TOPS) | **28nm FD-SOI / FinFET** | Multi-TOPS INT8 MAC arrays require dense standard-cell logic; cannot be implemented on 130nm. |
| **Central Cockpit / HPC Compute** | **Sub-10nm FinFET** | Multi-GHz Linux host + GPU/NPU + LPDDR5. **Explicitly outside DeepGrid's mature-node scope.** |

---

## 2. Decision Rules & Architectural Thresholds
1. **The Substrate Guard-Ring Rule**: When co-locating 120V motor drivers with 16-bit ADCs on a single BCD die, enforce $\ge 50\text{ µm}$ deep-trench isolation rings with dedicated analog and power ground pinouts.
2. **The 2-Cycle Skew Rule**: In ASIL-D safety cores, always delay the redundant pipeline by exactly 2 clock cycles to guarantee common-mode transient voltage immunity.
3. **The Sourcing Moat Rule**: When designing for Indian Defence PSUs (BEL, HAL, BDL), prioritize SKUs listed on the Ministry of Defence Positive Indigenisation Lists (PIL-1 through PIL-5) to secure sole-source procurement status.
4. **The "Boxes, Not Chips" Rule**: Sell pre-integrated modules (SiP, rugged daughterboards) with full MIL-STD-883 qualification rather than bare unpackaged silicon dies to bypass DPSU component-level resistance.

---

## 3. Standard Qualification Reference Matrix
| Target Standard | Domain | Key Test Requirements | Primary DeepGrid SKU |
|---|---|---|---|
| **MIL-STD-883K Class B** | Defence / Aerospace | 1000-hr burn-in @ 125°C, thermal shock (-55°C to +150°C), hermeticity | SKU-3 (PMIC), SKU-6 (Supervisor) |
| **DO-160G Section 16/17** | Civil/Military Avionics | 100V voltage surge, lightning-induced transient susceptibility | SKU-3 (PMIC), SKU-7 (Radar) |
| **AEC-Q100 Grade 0** | Automotive Powertrain | Operating junction temperature -40°C to +150°C | SKU-1 (BLDC Motor Controller) |
| **ISO 26262 ASIL-D** | Automotive Safety | SPFM > 99%, LFM > 90%, PMHF < 10 FIT, dual-core lockstep | SKU-4 (Lockstep MCU), SKU-9 (Gateway) |
| **PIL-5 MoD Mandate** | DPSU Procurement | 100% domestic IP ownership, import ban effective Dec 2027 | SKU-8 (BEL 17" Display Driver) |
