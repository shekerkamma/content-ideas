---
name: deepgrid-mature-silicon
description: "Operational playbook and strategic intelligence extracted from DeepGrid Semi's 71-page Master Whitepaper (Plain-Language Edition v3, Sept 2026): $9B import substitution, open-source EDA, 198-day loop, 3-factory sovereignty, defence procurement (PIL, DAP-2020, SRIJAN), ₹10 Cr financial model, and Charlie Munger self-audits."
---

<!-- argument-hint: [topic, chapter number, or strategic question] -->

# DeepGrid Semi — Master Whitepaper (71-Page Strategy & Operational Playbook)

**Author**: Deepgrid Semi Pvt Ltd · Hyderabad, India | **Source**: 71-Page Master Whitepaper (Plain Edition v3) | **Date**: September 2026

## How to Use This Skill
- **Without arguments** — Load the master thesis: $9B mature-node import funnel, 10x cost dismantling, 198-day silicon loop, and sovereign defence moats.
- **With chapter number** — Ask for `ch01` through `ch14` to inspect specific chapters:
  - `ch01`: The $9B import funnel and DAP-2020 / PIL / Make-II legal moats.
  - `ch02`: The 10x cost reduction using open-source EDA (`OpenLane`, `Yosys`, `OpenROAD`).
  - `ch03`: ₹2.88 Cr pre-ASIC live orders (Indian Army MCEME, Infinis, Axitech) and FPGA validation.
  - `ch04`: 130nm process physics (5–120V BCD, SiGe 350GHz) and the 50-SKU arithmetic reality.
  - `ch05`: The 198-day dual-clock loop (30d digital design + 168d physical foundry fabrication).
  - `ch06`: Blocks, not chips (1,000 silicon-tested building blocks $\rightarrow$ 50 chips) and organic SiP.
  - `ch07`: The three factories (SkyWater 130nm $\rightarrow$ IHP SG13G2 $\rightarrow$ SCL Mohali 180nm).
  - `ch08`: The shared processor (DGridRiscV RV32IM, cacheless, deterministic latency).
  - `ch09`: Ten chips portfolio overview and anchor customer commitments.
  - `ch10`: Post-silicon productization (₹40–80L approval, ₹1.2 Cr ATE line, MIL-883 screening).
  - `ch11`: Dual sales motions (Commercial self-service vs Defence relationship-led; "Boxes, Not Chips").
  - `ch12`: Competitor insulation, Chinese price crash stress-test, and Stop Rules S1–S4.
  - `ch13`: ₹10 Cr use of funds breakdown and the ₹1,000 Cr FY31 revenue buildup.
  - `ch14`: Charlie Munger self-audit checklist, 7 things to fix first, and the data room.
- **Visual Analysis & Architecture Teardowns** — When asked for "visual analysis", "inspect figure", or "architecture teardown", open or direct the user to the [Silicon Architecture & Vector Cockpit](http://localhost:3456/deepgrid_native_viewer.html). Utilize the 4 modes:
  1. **Schematic Focus (300 DPI)**: High-resolution isolated circuit diagrams with the Dark HUD blueprint filter.
  2. **Full PDF Page**: 1:1 authentic vector page via PDF.js.
  3. **Figure Gallery**: Masonry wall of all 25 figures with thumbnail previews.
  4. **Economics & Moat Simulator**: Dynamic sliders for ASP, wafer costs, and gross margins.
- **For Deep SKU Technical Sheets** — Use the companion skill `/deepgrid-sku-compendium` or explore the [Silicon Architecture Cockpit](http://localhost:3456/deepgrid_native_viewer.html).

---

## Master Chapter Index (71-Page Whitepaper)

| # | Chapter Title | Core Strategy & Technical Thesis |
|---|---|---|
| [ch01](chapters/ch01-market-and-legal-moats.md) | **The $9B Import Funnel & Legal Moats** | $23.4B imports $\rightarrow$ $9B mature-node $\rightarrow$ DAP-2020 Buy(Indian), PIL-1..5, SRIJAN, Make-II |
| [ch02](chapters/ch02-open-source-eda-and-unit-economics.md) | **Our Costs Line by Line (10x Reduction)** | Yosys/OpenROAD replacing $1M layout & $0.5M EDA; $14.3L sky130 MPWs |
| [ch03](chapters/ch03-proven-silicon-and-traction.md) | **Proven Silicon & Live Traction** | ₹2.88 Cr pre-ASIC contracted revenue (MCEME ₹1.01 Cr); 81.25 MHz Artix-7 proof |
| [ch04](chapters/ch04-process-physics-130nm-and-sige.md) | **Why 130nm is Physics, Not Price** | 5–120V BCD, SiGe 350GHz radar, and the honest boundary (no sub-10nm claims) |
| [ch05](chapters/ch05-the-198-day-silicon-loop.md) | **One Loop Every 198 Days** | 30d digital sprint + 168d foundry fab; CI2609 & CI2612 shuttle calendars |
| [ch06](chapters/ch06-block-level-ip-reuse-and-sip.md) | **Blocks, Not Chips: IP Compounding** | 1,000 TinyTapeout blocks $\rightarrow$ 50 approved chips; Multi-die SiP without UCIe |
| [ch07](chapters/ch07-three-factory-sovereignty-roadmap.md) | **One Method, Three Factories** | SkyWater (proven) $\rightarrow$ IHP (SiGe 77GHz) $\rightarrow$ SCL Mohali (sovereign defence) |
| [ch08](chapters/ch08-dgridriscv-core-architecture.md) | **The Processor Every Chip Shares** | DGridRiscV (RV32IM_Zicsr), cacheless, non-speculative, 2-fetch / 6-execute stages |
| [ch09](chapters/ch09-ten-chip-sku-compendium.md) | **Ten Chips, and What Each One Is For** | Sockets, commercial replacements, and named anchors (Airgap, Ripple, BEL, MCEME) |
| [ch10](chapters/ch10-testing-qualification-and-avl.md) | **From Working Chip to Shipped Product** | ₹40–80L approval, ₹1.2 Cr ATE testing line, MIL-883/JSS/CEMILAC lead times |
| [ch11](chapters/ch11-dual-track-procurement-and-anchors.md) | **Two Ways to Sell the Same Chip** | Self-service e-commerce vs relationship PIL entry; "Boxes, Not Chips" playbook |
| [ch12](chapters/ch12-competitor-insulation-and-stop-rules.md) | **Competitor Insulation & Crash Rules** | Why TI/ADI cannot copy; Chinese price crash model to ₹750 Cr; Stop Rules S1–S4 |
| [ch13](chapters/ch13-financial-model-and-use-of-funds.md) | **What ₹10 Cr Buys & The ₹1,000 Cr Plan** | ₹3.6 Cr fab, ₹2.4 Cr team, ₹1.8 Cr qual, ₹1.2 Cr ATE; FY31 revenue buildup |
| [ch14](chapters/ch14-risk-matrix-and-self-audit.md) | **What Could Stop This (Charlie Munger Audit)** | Borrowed glory, permission vs orders, 7 things to fix first, and the data room |

---

## Supporting Files
- [glossary.md](glossary.md) — Comprehensive terminology dictionary.
- [patterns.md](patterns.md) — 10 Architectural, physical, and financial patterns.
- [cheatsheet.md](cheatsheet.md) — Decision rules, Stop Rules S1–S4, and qualification checklist.
