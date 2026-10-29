# Chapter 6: How a Product Range Builds Up: Blocks, Not Chips

## Core Idea
A small semiconductor startup scales to 50 active SKUs not by taping out hundreds of bespoke chips, but by building and compounding a library of 1,000 silicon-validated digital and mixed-signal IP building blocks that are reassembled across multiple products and System-in-Package (SiP) modules.

---

## The 3-Tier IP Validation Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       THE THREE TIERS OF SILICON VALIDATION                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 1: Shared Die Tile (TinyTapeout-class)                                │
│ • Cost: $100 – $500 per tile                                                │
│ • Proves: Digital logic sub-blocks work in silicon                          │
│ • 5-Year Volume: ~1,000 digital building blocks verified                    │
│                                                                             │
│ TIER 2: Full-Chip MPW Shuttle (SkyWater / IHP)                              │
│ • Cost: ₹14.3 Lakhs (sky130) to ₹34–80 Lakhs (IHP)                          │
│ • Proves: Complete chip meets full electrical and datasheet specifications  │
│ • 5-Year Volume: ~50 approved product dies                                  │
│                                                                             │
│ TIER 3: Dedicated Production Mask Set                                       │
│ • Cost: ₹1.0 – ₹2.5 Crore+                                                  │
│ • Proves: High-volume manufacturing and cost scaling                        │
│ • 5-Year Volume: 10–20 high-volume commercial revenue drivers               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### What a Shared Tile (TinyTapeout) Can and Cannot Do
- **Capabilities**: Proves digital RTL, finite state machines, DSP filters, encryption engines, and memory decoders inside a small 0.02 mm² footprint.
- **Hard Limitations**:
  1. *No Analog / High Voltage*: Cannot host bandgap references, 120V power stages, or 77 GHz RF.
  2. *Shared Pinning*: Cannot test multi-channel outputs (e.g., 3,840 display columns or 6-phase motor gates) simultaneously.
  3. *No Datasheet Characterization*: Cannot measure temperature coefficient, PSRR (Power Supply Rejection Ratio), or analog noise.

---

## Compounding IP Reuse Across the Ten SKUs

| Silicon-Validated IP Block | Origin SKU | Secondary & Tertiary Reuse SKUs | Strategic Impact |
|---|---|---|---|
| **DGridRiscV Processor Core** | Universal | SKUs 1, 2, 3, 4, 7, 8, 9 | Written & verified once; shared across 7 chips |
| **Lockstep Comparator & Fault Matrix** | SKU 4 (ASIL-D MCU) | SKU 9 (Car Zonal), D100 (Drone Backup) | Instant aerospace safety compliance |
| **FOC Math Engine (CORDIC/SVM)** | SKU 1 (Motor Controller)| Robot Joint Actuators, Drone ESCs | Zero-latency motor tuning loop |
| **AES-256 / SHA-256 Crypto Cores** | SKU 2 (Smart Meter) | SKU 9 (EVITA HSM), Secure Boot Element | Hardware tamper and cybersecurity moat |
| **Thick-Oxide 5V I/O Output Ring** | SKU 5 (Transceiver) | SKUs 1, 8, 9 | Proven ESD and noise immunity |

---

## System-in-Package (SiP) Scaling Strategy
- **The Ultimate Vision**: Integrating 6 discrete mature-node dies (Power, Motor Driver, Comms Transceiver, Safety Core, Analog Metrology, Control) alongside a 28nm AI accelerator into a single sealed multi-chip package.
- **The KGD (Known-Good Die) Rule**: If one die in a 6-chip SiP is defective, the entire assembly is scrapped. Therefore, 100% wafer-level probe testing and dedicated ATE screening are mandatory prior to packaging.

---

## Key Takeaways
1. Frame the portfolio as "1,000 silicon-proven blocks reassembled into 50 SKUs", not 1,000 separate chip tapeouts.
2. Low-cost TinyTapeout tiles validate digital sub-blocks for a few hundred dollars, saving crores in full-mask debugging.
3. IP blocks compound over time, allowing the company to release 10 new SKUs per year with a fixed engineering team.

---

## Connects To
- **Ch 8**: Universal DGridRiscV processor architecture.
- **Ch 9**: Architectural mapping across the ten specific SKUs.
