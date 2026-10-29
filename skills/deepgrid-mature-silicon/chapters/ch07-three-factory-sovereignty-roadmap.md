# Chapter 7: One Method, Three Factories (Sovereignty Roadmap)

## Core Idea
DeepGrid’s design flow is portable across three sequential foundries: SkyWater (USA) for rapid proof-of-concept silicon, IHP (Germany) for ultra-high-frequency radar, and SCL Mohali (India) for sovereign defence compliance.

---

## The Three Foundries: Roles, Nodes, and Status

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       THE THREE-FOUNDRY SEQUENCING                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. PROVEN: SkyWater Technology (USA)                                        │
│ • Node: sky130 (130 nm Planar CMOS)                                         │
│ • Status: DONE — Physical working test chip fabricated & validated          │
│ • Role: Rapid, low-cost digital & mixed-signal commercial prototyping       │
│                                                                             │
│ 2. DIFFERENTIATED: IHP Leibniz Institute (Germany)                          │
│ • Node: SG13G2 (130 nm SiGe BiCMOS)                                         │
│ • Status: PLANNED — Target tapeout for 77 GHz RF radar                      │
│ • Role: High-frequency transistors (350 GHz fT) for radar & fast datalinks  │
│                                                                             │
│ 3. SOVEREIGN: SCL Mohali (Punjab, India)                                    │
│ • Node: 180 nm Military-Qualified CMOS                                      │
│ • Status: PLANNED — Indian defence sovereign manufacturing                  │
│ • Role: Buy(Indian-IDDM) compliance; complete domestic design & fab         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Porting Rules: What Moves vs. What Must Be Redesigned

### 1. Digital Logic (Portable via Scripting)
- **Retargets via Toolchain**: Digital Verilog/SystemVerilog RTL, testbenches, verification coverage plans, and processor cores port seamlessly between foundries by swapping standard-cell Liberty (`.lib`) files and re-running OpenROAD scripts.

### 2. Analog & High-Voltage (A Redesign, Not a Port)
- **Requires Manual Re-Engineering**:
  - Bandgap voltage references and current bias mirrors.
  - High-voltage LDMOS output stages and gate drivers.
  - On-chip non-volatile memory (NVM / EEPROM) macros.
  - ESD/EOS protection rings and pad frame geometries.
  - *Rule*: Never promise zero-cost analog migration between foundries; every analog block requires 1–2 shuttle cycles to recalibrate in new silicon.

---

## The Sovereign IDDM Imperative
- **Buy(Indian) vs Buy(Indian-IDDM)**:
  - Fabricating at SkyWater or IHP qualifies as **Buy(Indian)** because design and RTL are 100% Indian, beating pure imports under DAP-2020.
  - Qualifying at **SCL Mohali** unlocks **Buy(Indian-IDDM)** (Indigenously Designed, Developed, and Manufactured), granting absolute monopoly priority in sovereign defence tenders.

---

## Key Takeaways
1. SkyWater `sky130` proves digital designs cheaply; IHP `SG13G2` enables 77 GHz radar; SCL Mohali delivers sovereign defence lock-in.
2. Digital RTL is portable across foundries; analog circuits require layout re-engineering.
3. Domestic fabrication at SCL Mohali is a structural business requirement for Tier-1 defence procurement.

---

## Connects To
- **Ch 1**: Indian defence procurement law (DAP-2020 and PILs).
- **Ch 12**: Insulation against foreign competitors and domestic single-sourcing risks.
