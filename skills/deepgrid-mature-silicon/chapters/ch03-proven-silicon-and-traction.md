# Chapter 3: What We Have Already Made (Traction & Proof)

## Core Idea
DeepGrid separates verified silicon and signed commercial contracts from forward-looking forecasts, anchoring its claims on a manufactured 130nm test chip, a public TinyTapeout 6 multi-project die, and ₹2.88 Cr in pre-ASIC FPGA hardware revenue.

---

## The Verifiable Evidence Scoreboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       EVIDENCE LEVEL DEFINITIONS                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ [DONE]      : A physical chip exists, or a legal contract/order is signed.  │
│ [DESIGNED]  : Circuit RTL exists and runs validated on FPGA test hardware. │
│ [PLANNED]   : A scheduled milestone with fixed foundry shuttle dates.       │
│ [ESTIMATED] : Internal financial modeling without third-party audit.        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. Fabricated Silicon Proofs [DONE]
- **SkyWater 130nm Test Chip**: Fabricated via in-house automated flow; working silicon verified floating-point operations and digital standard cell libraries.
- **TinyTapeout 6 Multi-Project Chip**: Public design sharing a 15×15 mm `sky130` die with ~500 projects, proving standard tile compliance and packaging interfaces.

### 2. Pre-ASIC Hardware Revenue [DONE]: ₹2.88 Cr
- **Indian Army (via MCEME)**: **₹1.01 Cr** under formal contract (₹23.01 Lakhs delivered, ₹78.39 Lakhs in execution).
- **Infinis Agritech**: **₹1.25 Cr** for 50 specialized precision agriculture kits (40% advance cleared).
- **Axitech Solar**: **₹0.62 Cr** for 25 tracker controller kits.
- *Honest Boundary*: This revenue is derived from FPGA-based prototype systems (e.g. `DGS001` / `DGFP4` demonstration boards). It proves execution, procurement qualification, and customer relationship credibility, but does not prove raw bare-die chip demand.

### 3. RTL Tested on Silicon Emulation [DESIGNED]
- Lockstep dual-core processor with automated fault-injection comparators.
- FOC (Field-Oriented Control) BLDC motor control datapath.
- 24-bit 6-channel electrical power metrology filter chain.
- Supervisor voltage/window sensing and deglitch state machine.
- Drone inertial visual-odometry position estimation engine.
- *Emulation Baseline*: All synthesized and verified on Xilinx Artix-7 FPGA at **81.25 MHz**.

---

## The Single Biggest Open Technical Claim
- **200 MHz on 130nm ASIC Target**:
  - The 81.25 MHz FPGA speed is an FPGA look-up table routing constraint, not an ASIC limit.
  - The target ASIC product clock is **200 MHz fixed**.
  - *Unproven Gate*: Full Static Timing Analysis (STA) on `sky130` across worst-case PVT corners (Process, Voltage, Temperature) must be published before claiming measured silicon speed.

---

## Key Takeaways
1. Traction is established prior to ASIC fabrication through paid FPGA system contracts.
2. Differentiate FPGA hardware board revenue from bare-die component volume.
3. Treat unverified clock speed targets as technical hypotheses requiring published STA reports.

---

## Connects To
- **Ch 8**: DGridRiscV processor architecture running at 200 MHz.
- **Ch 14**: The 7 immediate credibility fixes, starting with published STA reports.
