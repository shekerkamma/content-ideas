# Chapter 1: What India Buys, and Why Nobody Here Makes It

## Core Idea
India spends ~$9B annually importing mature-node (≥130nm) chips for industrial and defence applications not due to a design skill deficit, but because traditional semiconductor NRE economics ($2M–$5M setup cost) make low-volume, high-reliability sockets unviable without open-source EDA and shared silicon fabrication.

---

## Frameworks Introduced

### 1. The Realized Market Import Funnel
- **When to use**: Sizing addressable semiconductor opportunities in import-dependent sovereign markets.
- **How**:
  1. *Total IC Imports*: $23.4B (HS 8542 UN COMTRADE baseline).
  2. *Mature Node Filter (≥130nm)*: $9.0B (Divide by 2.6).
  3. *Nine Target Chip Classes*: $0.46B / ₹4,000 Cr (Divide by 19).
  4. *Addressable by FY31*: ₹1,000 Cr achievable revenue cap.
  5. *Live Contracted Revenue Today*: ₹2.88 Cr (Pre-ASIC board systems).

### 2. The Four-Tier Sovereign Procurement Stack
- **When to use**: Leveraging sovereign industrial policy to eliminate foreign incumbents.
- **How**:
  - **Tier 1: DAP-2020 Buy (Indian-IDDM)**: Grants top procurement priority to Indian-designed and manufactured products before price comparisons occur.
  - **Tier 2: Positive Indigenisation Lists (PIL 1–5)**: Enforces hard calendar bans on importing named sub-assemblies and LRUs.
  - **Tier 3: SRIJAN Portal Ingestion**: Direct pipeline of 37,000+ imported defence line items published by DPSUs seeking domestic suppliers.
  - **Tier 4: Make-II Development Protocol**: Industry-funded development where successful prototype trials guarantee production orders.

---

## Key Concepts
- **Mature Node (≥130nm)**: Proven semiconductor manufacturing processes utilizing larger transistor geometries; standard for high voltage, analog precision, and automotive/defence durability.
- **NRE (Non-Recurring Engineering)**: One-time setup expenses (mask sets, physical layout contracting, EDA tool licensing) required prior to fabricating silicon.
- **PDK (Process Design Kit)**: The proprietary file set provided by a foundry defining design rules, device models, and layout constraints (e.g., SkyWater `sky130`, IHP `SG13G2`).
- **Buy(Indian) vs Buy(Indian-IDDM)**: Buy(Indian) applies to Indian design fabricated in offshore foundries; Buy(Indian-IDDM) requires domestic fabrication value content (e.g., SCL Mohali).
- **LRU (Line-Replaceable Unit)**: Modular sub-system box inside military aircraft, tanks, or missiles that undergoes procurement indigenisation.

---

## Mental Models
- **Think of NRE as a Minimum Order Threshold**: At $2M–$5M NRE, a chip selling 10,000 units/year costs $200–$500/unit before fabrication. Cutting NRE 10x unlocks profitability on 10k-unit runs.
- **Use "Boxes, Not Chips" for Defence Entry**: Defence indigenisation lists specify LRU assemblies (swappable boxes), never bare chips. Entry requires designing into the sub-tier boards inside the listed box.

---

## Anti-patterns
- **Chasing Leading-Edge Nodes (3nm–7nm) for Industrial Sockets**: Attempting to put 28V/120V power circuits or high-voltage drivers on sub-28nm processes forces discrete off-chip components, increasing PCB footprint, failure points, and BOM costs.
- **Treating PIL List Entries as Direct Purchase Orders**: A PIL listing is legal permission and an eventual import ban, not a sales order. Orders take 2–4 years of qualification and trial testing.

---

## Reference Tables

### The Four Enablers of Modern Mature-Node Disruption
| Enabler | Historical State (Pre-2020) | Current State (2026) | Strategic Impact |
|---|---|---|---|
| **PDK Licensing** | Proprietary NDAs; university toys | Open-source foundry PDKs (`sky130`, `SG13G2`) | Zero NDA cost; instant design start |
| **EDA Tooling** | $500k–$1M/seat annual licenses | Open-source RTL-to-GDSII engines | Zero per-seat layout software cost |
| **Processor IP** | Proprietary ARM licenses + royalties | Open RV32IM RISC-V architectures | Zero licensing fees, zero royalties |
| **Procurement Law** | Price-preference for imports | Mandatory PIL import bans + Make-II | Incumbent removed from bidding |

---

## Worked Example: Overcoming the Low-Volume Defense Deadlock
```
Problem:
An Indian avionics sub-contractor needs 10,000 units/year of a 28V military-spec power sequencer.

Traditional Fabless Approach:
- Physical Design Layout Service: $1,500,000
- Proprietary EDA Licenses: $500,000
- Production Mask Set: $750,000
- Total Initial NRE: $2,750,000
- Amortized NRE per unit (over 1 year): $275/chip -> UNVIABLE (Customer budget: $80/chip).

DeepGrid Open-Flow Approach:
- In-House Automated Physical Design: ₹0 (Staff time only)
- Open EDA Toolchain (OpenROAD): ₹0
- MPW Shared Prototype Shuttle: ₹14.3 Lakhs ($14,950)
- MIL-STD-883 Qualification: ₹60 Lakhs
- Total NRE: ₹74.3 Lakhs (~$90,000)
- Amortized NRE per unit: ₹743 (~$9/chip) -> VIABLE at 65% Gross Margin.
```

---

## Key Takeaways
1. India's $9B mature-node import deficit is governed by cost structure barriers, not circuit engineering capability.
2. Positive Indigenisation Lists legally eliminate foreign incumbents once domestic alternatives clear Make-II trials.
3. Open-source PDKs and automated EDA flows eliminate four major cost lines, making 10k-unit specialized volumes highly profitable.

---

## Connects To
- **Ch 2**: Detailed line-by-line cost comparison and automated toolchain mechanics.
- **Ch 11**: Two-track sales process leveraging PIL/SRIJAN listings.
