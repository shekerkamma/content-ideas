# Chapter 8: SKU-7 — 77 GHz MIMO Radar (SiGe Front End + CMOS Baseband)

## Core Idea / Thesis
A dual-die partitioned 4D imaging radar architecture utilizing ultra-fast Silicon-Germanium (SiGe HBT) for the 77 GHz millimeter-wave transceiver paired with a monolithic 130 nm CMOS digital baseband die for multi-channel ADC sampling, 2D/3D FFT acceleration, and CFAR target detection.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 8 (Figure 16 in Plain Edition Whitepaper) — 77 GHz MIMO Radar

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Process Node (RF)** | 130 nm BiCMOS / SiGe HBT ($f_T > 350\text{ GHz}, f_{max} > 450\text{ GHz}$) (IHP SG13G2 PDK) |
| **Process Node (Baseband)** | 130 nm CMOS (SkyWater SKY130 / SCL 180nm) @ 200 MHz |
| **RF Channels** | 2 Transmit (2TX) + 4 Receive (4RX) MIMO Array |
| **FMCW Sweep Bandwidth** | 4 GHz sweep (76 GHz to 81 GHz) $\rightarrow$ **3.75 cm range resolution** |
| **Baseband ADCs** | 4-channel 12-bit 40 MSPS Synchronized Pipeline/SAR ADCs |
| **Signal Processing Engine** | Hardware Range FFT (1024-pt radix-4, 20 µs/chirp) + Doppler FFT + CFAR Engine + Angle Estimation |
| **Target Tracker Capacity** | Real-time tracking of up to **64 distinct targets** per frame |
| **Interface to ECU** | High-Speed CAN-FD / 100BASE-T1 Automotive Ethernet / MIPI-CSI2 |
| **Standards Compliance** | MIL-STD-883K, DO-160G (Airborne), DO-254 DAL-B, ISO 26262 ASIL-B |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| SiGe HBT DIE (IHP SG13G2): CHIRP SYNTHESIS & TRANSMIT                             |
|   XTAL (40MHz) -> Ramp Gen -> Fractional-N PLL -> VCO (38.5GHz) -> x2 Mult (77GHz) -> PA x2
+-----------------------------------------------------------------------------------+
| SiGe HBT DIE: RECEIVE ARRAY (4 CHANNELS)                                          |
|   RX1..RX4 -> LNA (13dB NF) -> Active Mixer -> IF Amp -> Anti-Aliasing Filter -> [DIE BOUNDARY]
+===================================================================================+
| 130nm CMOS DIE: DIGITIZATION & ACCELERATION                                       |
|   4x 12-bit 40 Msps ADCs -> Windowing Engine (Hann/Blackman) -> Range FFT -> Doppler FFT
|   Range-Doppler SRAM Matrix (512 KB) -> CFAR Engine (CA-CFAR) -> Target Tracker (64)
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **The Die Boundary & Inter-Die RF Leakage**: Why is the ADC placed on the 130nm CMOS die rather than the SiGe die, and what high-frequency transmission line matching is required on the package substrate to prevent IF signal reflection?
2. **Chirp Linearity & Phase Noise**: How does the closed-loop PLL frequency ramp generator maintain $<50\text{ kHz rms}$ chirp error across a 4 GHz sweep without introducing non-linear ghost targets during Range-Doppler processing?
3. **Honesty on the Sheet — Silicon Risk**: The whitepaper explicitly states: *"The SiGe front end has no FPGA equivalent and is proven on silicon or not at all."* How does DeepGrid mitigate tapeout risk on IHP MPW cycles?
4. **Airborne DO-160 EMI/EMC Co-Existence**: When installed on a UAV mast alongside UHF/VHF communications, how does the 77 GHz antenna-on-package shielding prevent LO harmonic emissions from desensitizing military receivers?

## Policy, Market & Procurement Hook
- **Dual-Use Applications**: AD2 mirror-tower commercial automotive radar + defence perimeter security, counter-UAS tracking, and military vehicle active protection systems (APS).
- **Sole Dual-Domain Part**: The only SKU with simultaneous captive automotive OEM and DPSU defence contracts.
- **TAM & Pricing**: 2–8M units/yr India TAM @ **$8–25 ASP band** (~$0.15–0.40B market).
- **Silicon Node Path**: IHP SG13G2 MPW cycle $\rightarrow$ production integration.

## Connects To
- **Chapter 10 (SKU-9)**: Feeds target point clouds to the SDV Zonal Gateway.
- **Chapter 11 (D100)**: Provides obstacle detection and terrain-following for autonomous UAV flight.
