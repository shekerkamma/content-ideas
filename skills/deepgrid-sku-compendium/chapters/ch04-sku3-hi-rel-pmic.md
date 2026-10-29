# Chapter 4: SKU-3 — Hi-Rel PMIC (28 V Avionics Rail Tree)

## Core Idea / Thesis
A true high-voltage analog power management IC designed for military avionics and vetronics 28V bus standards (DO-160, MIL-STD-461, MIL-STD-1275), featuring a peak-current-mode pre-buck regulator, four sequenced rails with foldback current limit, and a radiation-mitigated (DICE + TMR) state machine.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 4 (Figure 12 in Plain Edition Whitepaper) — Power Management

## Physical & Electrical Specifications
| Parameter | Value / Specification |
|---|---|
| **Process Node** | 180 nm BCD / 130 nm 20V Extended (SCL Mohali 180 nm Production) |
| **Input Bus Tolerances** | 4.5 V to 40 V continuous (28 V nominal military bus, 80 V surge tolerant, 100 V spike) |
| **Pre-Regulator Stage** | Synchronous Buck (PWM peak-current-mode, Type-III compensation, 500 kHz - 2 MHz) |
| **Voltage Rails Generated** | 4x Sequenced Regulators (Buck 5V @ 2A, Buck 3.3V @ 3A, LDO 1.8V @ 500mA, LDO 1.2V/0.9V @ 300mA) |
| **Bandgap Accuracy** | Curvature-corrected Brokaw bandgap: **12 ppm/°C** across -55°C to +125°C |
| **Telemetry & Diagnostics** | Built-in 10-bit 500 kSPS SAR ADC monitoring voltage, current, and die temperature via SPI |
| **Single-Event Upset (SEU)** | Dual Interlocked Storage Cell (DICE) latches + Triple Modular Redundancy (TMR) on Sequencer FSM |
| **Standards Compliance** | DO-160 Section 16/17, MIL-STD-704F, MIL-STD-1275D, MIL-STD-461G, MIL-STD-883 Class B |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| 28V AIRCRAFT BUS: Input Conditioning (EMI + TVS, Ideal Diode, Inrush, UVLO/OVLO)  |
+-----------------------------------------------------------------------------------+
| PRE-REGULATOR: Error Amp (Type-III) | PWM Comp | Gate Driver | Power Stage (30V)  |
+-----------------------------------------------------------------------------------+
| RAIL GENERATION:                                                                  |
|   5.0V Buck (2.0A)   -> Window Monitor -> Overcurrent Limit -> Power Good (PG)    |
|   3.3V Buck (3.0A)   -> Window Monitor -> Overcurrent Limit -> Power Good (PG)    |
|   1.8V LDO  (500mA)  -> Window Monitor -> Overcurrent Limit -> Power Good (PG)    |
|   1.2V LDO  (300mA)  -> Window Monitor -> Overcurrent Limit -> Power Good (PG)    |
+-----------------------------------------------------------------------------------+
| REFERENCE & TELEMETRY: Brokaw Bandgap (12 ppm/C) | Telemetry SAR ADC (10-bit)     |
| SUPERVISION: Programmable 4-Step Sequencer FSM (TMR) | Watchdog | SEU Hardened    |
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **MIL-STD-1275 100V Surge Withstand**: When an airborne electrical bus experiences a 100V / 50ms inductive load dump surge, how does the input stage clamp voltage without triggering catastrophic thermal runaway in the integrated pass FETs?
2. **Type-III Error Amplifier Stability**: How does the PMIC preserve a phase margin $>60^\circ$ and gain margin $>10\text{ dB}$ across ceramic vs tantalum output filter capacitors over the full military temperature range (-55°C to +125°C)?
3. **Cross-Rail Coupling & Noise Rejection (PSRR)**: What is the power supply ripple rejection (PSRR) from the high-current 3.3V switching rail back through the internal reference to ensure the 1.2V ADC core supply maintains $<5\text{ mV}$ peak-to-peak ripple?
4. **DICE/TMR Single-Event Latchup Immunity**: What physical layout spacing is enforced between TMR state bits to guarantee that a heavy-ion strike cannot corrupt two voting nodes simultaneously?

## Policy, Market & Procurement Hook
- **Replaces**: Texas Instruments / Analog Devices (Linear Tech) QML-certified discrete power trees in defence Line Replaceable Units (LRUs), missile seekers, and vetronics.
- **Strategic Policy Moat**: SRIJAN NSG-5962 military power IC category; small volume (10–50K units/yr in India) but high margin (**60–75% Gross Margin** @ $50–200 screened ASP).
- **Silicon Node Path**: sky130 20V devices $\rightarrow$ SCL 180 nm production. Cycle-1 MPW.

## Connects To
- **Chapter 5 (SKU-4)**: Supplies sequenced power to the lockstep core and memory rails.
- **Chapter 7 (SKU-6)**: External voltage supervisor cross-checking PMIC power good signals.
