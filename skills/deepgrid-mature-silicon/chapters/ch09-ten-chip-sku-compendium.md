# Chapter 9: The Ten SKU Product Architecture Compendium

## Core Idea
DeepGrid’s portfolio addresses ten specific, high-volume sockets currently filled exclusively by foreign imports. Commercial SKUs roll out first to generate cash flow and operational credibility, followed by high-margin defence-screened counterparts sharing identical silicon.

---

## The Master Ten-SKU Architecture Matrix

| SKU | Product Description | Target Process | What It Replaces | Anchor Buyer / Demand Hook | ASP / Volume Target |
|---|---|---|---|---|---|
| **Chip 1** | **BLDC Motor Controller** | 130 nm CMOS (5–120V) | TI DRV83xx + Discrete MCU | **Airgap Technology** (EV Powertrains), PIL-5 Anti-Tank Missile Actuators | $3–$8 (5–15M units/yr) |
| **Chip 2** | **Smart-Meter SoC** | 130 nm CMOS | Analog Devices ADE9153 + MCU | **Ripple Metering** (250M National Smart Meter Program) | $2–$5 (10–30M units/yr) |
| **Chip 3** | **28V High-Rel PMIC** | `sky130` → SCL 180 nm | TI/ADI Military Power Chips | SRIJAN NSG-5962; BEL Tank DC-DC Converters | $50–$200 Screened (10k–50k/yr) |
| **Chip 4** | **Lockstep ASIL-D MCU** | 130 nm CMOS | Microchip / Renesas Safety MCUs | **MCEME (Indian Army)**; EV Battery Management | $4–$12 (3–10M units/yr) |
| **Chip 5** | **Interface Transceiver** | 130 nm (5V Ring) | TI SN65HVD / Discontinued Bus ICs | High-attach industrial comms (RS-485, CAN-FD) | $0.40–$1.50 (20–60M units/yr) |
| **Chip 6** | **Voltage Supervisor** | `sky130` → SCL 180 nm | TI / Maxim Supply Monitors | Simplest SKU — Pathfinder for MIL-883 screening | $0.20–$0.80 (30–80M units/yr) |
| **Chip 7** | **4D Radar Front-End** | IHP SG13G2 SiGe + CMOS | Imported 77 GHz Automotive Radar | Radar Warning Receivers (Su-30, Mi-17), ADAS | $35–$60 / set (2–8M sets/yr) |
| **Chip 8** | **High-Voltage Display Driver** | 130 nm (0–12V Swing) | Imported Rugged Display TCONs | **BEL 17-inch Rugged Display** (PIL-5 direct match) | $70–$110 Screened (2–6M units/yr)|
| **Chip 9** | **Car Zonal Controller** | 130 nm CMOS | Discrete Relay & Harness Modules | EV Zonal Gateway; EVITA Hardware Security | $6–$20 (4–12M units/yr) |
| **Track B**| **D100 Drone AI SoC** | TSMC 28 nm (Separate Round)| Qualcomm QRB5165 | **Chakravayu CPDL**, ideaForge drone platforms | $60–$100 (100k–300k units/yr) |

---

## Detailed SKU Architectural Highlights

### 1. Chip 1: BLDC Motor Controller (Monolithic High-Voltage Driver)
- **Architecture**: DGridRiscV core (200 MHz) + Hardware CORDIC FOC math datapath + 7 PWM drive channels + 5–120V integrated buck converter + 16-bit sensor ADC.
- **Key Advantage**: Replaces a 2-chip set (separate driver + MCU) with one monolithic die; supports software dynamic motor winding reconfiguration (Star/Delta).

### 2. Chip 2: Smart-Meter Class 0.5S Measurement SoC
- **Architecture**: 6-channel 24-bit Sigma-Delta ADC front-end with OSR 256 + Metrology computation engine (15th harmonic analysis) + Hardware AES/SHA security engines + Sub-2µW RTC.
- **Key Advantage**: Built-in hardware tamper detection mandated by Indian national utility tenders.

### 3. Chip 3: 28V High-Reliability Avionics Power Management
- **Architecture**: DO-160 / MIL-STD-461 compliant input conditioning + LDMOS power stage + 4 sequenced output rails + Bandgap reference (12 ppm/°C) + TMR/DICE latches.
- **Key Advantage**: Radiation-tolerant power sequencing directly from 28V avionics bus without external pre-regulators.

### 4. Chip 4: Lockstep Microcontroller (ISO 26262 ASIL-D)
- **Architecture**: Dual DGridRiscV cores running 2 clock cycles skewed + Hardware comparator raising bus faults within 2 cycles + End-to-end ECC across all buses and SRAM.

### 5. Chip 7: 4D 77 GHz Radar Front-End (SiGe + CMOS Split)
- **Architecture**: IHP SiGe RF IC (2 TX / 4 RX, 350 GHz $f_T$ HBTs) + SkyWater 130nm Digital Baseband (Range/Doppler FFT, CFAR target detection, Angle estimation DSP).

---

## Strategic Sequencing: Why Commercial SKUs Precede Defence
```
CYCLE 1: Commercial Volume Launch ──► Cash Flow & Factory Credibility
(Chip 1 Motor + Chip 2 Meter)        (Establishes tapeout track record)
                                                    │
                                                    ▼
CYCLE 2: Pathfinder Screening Launch ──► Low-Risk Qualification Learning
(Chip 6 Simple Voltage Supervisor)       (Uncovers MIL-883 bottlenecks early)
                                                    │
                                                    ▼
CYCLE 3: High-Margin Defence SKUs ──► 10x–100x Price Realization
(Chips 3, 4, 7, 8 on Proven Silicon)  (Monopoly pricing behind PIL barriers)
```

---

## Key Takeaways
1. Every chip targets an existing socket currently dominated by foreign catalog parts.
2. Commercial chips (Motors & Smart Meters) generate rapid volume; defence chips generate high gross margins (60%–75%).
3. Chip 6 acts as the low-cost pathfinder for military MIL-STD-883 screening.

---

## Connects To
- **Ch 11**: Anchor customer mappings and procurement list line items.
- **Ch 13**: FY27–FY31 unit and revenue build-up per SKU.
