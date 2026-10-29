# Chapter 11: Two Ways to Sell the Same Chip (Procurement Capture)

## Core Idea
The same physical silicon die is monetized through two completely divergent commercial motions: a frictionless, self-service developer adoption funnel for high-volume commercial markets ($2–$8 ASP), and a relationship-led, Make-II sovereign qualification funnel for defence and aerospace platforms ($50–$200+ ASP).

---

## The Dual-Motion Commercial Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMMERCIAL MOTION (Self-Service Velocity)                │
│                                                                             │
│  Datasheet Download  ──►  $50 Eval Board  ──►  1-Week Bring-up  ──► Design-In │
│     (Weeks 0–2)             (Weeks 2–6)          (Weeks 6–14)        (Week 14+)│
├─────────────────────────────────────────────────────────────────────────────┤
│                     DEFENCE MOTION (Sovereign Mandates)                     │
│                                                                             │
│   SRIJAN / PIL Match  ──► DPSU Tech Review ──► Make-II Trial PO ──► AVL List │
│     (Government)           (Spec Lock)         (Custom Sample)     (10-Yr Moat)│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## What Government Indigenisation Lists Actually Contain
- **The "Boxes, Not Chips" Discovery**:
  - Scanning the Defence Ministry's 5th Positive Indigenisation List (PIL-5, 346 items) and DMA lists reveals they specify *swappable assemblies, LRUs, and mechanical parts* (e.g., pumps, fuzes, display boxes, converters), **never bare chip part numbers**.
  - *Winning Strategy*: Meet the Tier-1 DPSU (BEL, HAL, BDL) holding the LRU mandate and pitch: *"You must indigenise this box by December 2027. Here is the Indian silicon that powers the circuit board inside it."*

---

## Real PIL & SRIJAN Matches Across the Range

| Defence Platform / Box Listing | Mandating Entity | Deadline | DeepGrid Silicon Solution |
|---|---|---|---|
| **BLDC Motor with Encoder (Anti-Tank Missile)** | Indian Army / BDL | Dec 2025 | **Chip 1** (Integrated FOC BLDC Controller) |
| **DC-DC Converter (4A, 16–40V, Tank Electronics)**| BEL | Dec 2026 | **Chip 3** (28V High-Rel Power Management) |
| **Digital Receiver & Synthesizer (Electronic Warfare)**| BEL | Dec 2026 | **Chip 7 Family** (SiGe RF + Digital Baseband) |
| **17-inch Rugged Cockpit Display Unit** | BEL Defence Electronics | Dec 2027 | **Chip 8** (High-Voltage Display Column Driver) |
| **Radar Warning Receiver (Su-30 MKI, Mi-17 Aircraft)**| HAL / IAF | Dec 2025 | **Chip 7 Variant** (Wideband Radar Receiver) |

---

## Named Anchor Customers Today
1. **Commercial Electric Powertrains**: **Airgap Technology** (Anchor buyer for Chip 1 BLDC Controller across EV 2/3-wheelers).
2. **National Smart Metering**: **Ripple Metering** (Anchor buyer for Chip 2 Smart Meter SoC on LoRaWAN networks).
3. **Military & Safety Microcontrollers**: **MCEME / Indian Army** (₹1.01 Cr contracted for Chip 4 Lockstep safety architecture).
4. **Autonomous Drones**: **Chakravayu CPDL** (Anchor buyer for D100 drone platform).

---

## The Three Clocks of Semiconductor Buyers
- **The List Entry (Slow Clock - 2–4 Years)**: Import ban date approaches; orders ramp gradually as legacy inventory depletes.
- **The Defence Filing (Predictable Clock - 15–18 Months)**: Make-II sample built at supplier expense; passing official field trials guarantees production contracts by rule.
- **The Commercial Tender (Fast Clock - 6–12 Months)**: High-volume utility and automotive rollouts (Smart meters, EV motor drives).

---

## Key Takeaways
1. Sell the same physical chip to commercial buyers for volume and defence buyers for high margins.
2. Defence lists name LRU boxes, not chips; position silicon as the core enabler for DPSU box compliance.
3. Anchor customers (Airgap, Ripple, MCEME, Chakravayu) de-risk production tapeouts before manufacturing spend.

---

## Connects To
- **Ch 1**: Indian defence procurement law (DAP-2020 and PILs).
- **Ch 12**: The "No Buyer, No Build" governance rule.
