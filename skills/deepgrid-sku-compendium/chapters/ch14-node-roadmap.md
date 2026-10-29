# Chapter 14: Node & SKU 3-Phase Roadmap & Arithmetic Check

## Core Idea / Thesis
A rigorous, arithmetic-checked 3-phase technology and SKU scaling roadmap that establishes the physical necessity of shrinking logic-bound blocks (90/55/45nm in Phase 2; 28nm in Phase 3) while keeping analog, power, and I/O rings permanently anchored in robust 130nm/180nm silicon.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 14 (Roadmap & Arithmetic Check) — Node & SKU Roadmap

## 3-Phase Technology Scaling Matrix
| Phase | Time Horizon | Process Nodes | Target Product Class & Drivers | Silicon Boundary Statement |
|---|---|---|---|---|
| **Phase 1** | **2026–2027** | **130 nm / 180 nm** | SKU 1–10 Catalogue: Motors, PMICs, Metrology, Supervisors, Transceivers, Zonal Gateway | Ships the core foundation; 100% mature-node |
| **Phase 2** | **2028–2029** | **90 nm / 55 nm / 45 nm** | Logic-bound shrinks: Military GNSS Baseband, SDR Transceiver (SiGe+CMOS), Drone Nav Co-processor | **Shrink for channel count and DSP throughput — NOT speed vanity.** Analog I/O stays 130nm. |
| **Phase 3** | **2030+** | **28 nm and below** | Multi-TOPS AI NPUs, Object detection, Central SDV multi-GHz compute, UAV swarm coordination | **"Everything above is a sub-10 nm problem. 28 nm buys some of it. None of it is claimable on 130 nm, at any clock."** |

## The Arithmetic Check (Self-Correcting Diligence)
The whitepaper figure explicitly performs a transparent audit of its own catalogue projections:
- **Draft Error Caught**: Early strategy drafts claimed *"10 new SKUs every year and over 1,000 active SKUs by Year 5."*
- **Mathematical Reality**: 10 SKUs/yr $\times$ 5 yrs = **50 SKUs**. A 1,000-SKU catalogue would require 200 tapeouts/year—a 20x error.
- **Corrected Canon**: DeepGrid officially commits to a **~50-SKU mature-node catalogue by Year 5**, maintaining single-number discipline before institutional investors and DPSU auditors.

## Deep Engineering Questions & Failure Modes
1. **Why Shrink at All (Phase 2 Drivers)**: Why does a multi-channel GNSS baseband or SDR transceiver require 90nm/55nm while its RF front-end and ESD protection ring remain on 130nm?
2. **The 28nm "Honest Boundary"**: Why does DeepGrid explicitly state that central cockpit infotainment compute and autonomous driving LLMs cannot be claimed on mature silicon?
3. **Mask Cost vs Volume Breakeven Across Nodes**: At what annual volume does porting a 130nm design ($150K mask) to 55nm ($600K mask) or 28nm ($2.5M mask) break even in silicon area savings?
4. **Defence Share Ramp**: As the catalogue expands from Phase 1 to Phase 3, how does the revenue mix balance high-margin, low-volume defence contracts (60–75% GM) with high-volume, lower-margin commercial smart meter/motor sockets?

## Policy, Market & Procurement Hook
- **Institutional Diligence Ready**: Demonstrates rare engineering and financial honesty, eliminating inflated TAM projections and ungrounded fab claims.
- **Sovereign Capability Growth**: Matches India's domestic foundry roadmap (SCL 180nm modernization, Tata Electronics Dholera 28nm fab).

## Connects To
- **Chapter 1 (Overview)**: Concludes the 14-sheet architectural portfolio.
- **Chapter 13 (SiP Integration)**: Integrates Phase 1 mature dies with Phase 3 28nm compute.
