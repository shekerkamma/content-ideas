# Chapter 2: Our Costs, Line by Line

## Core Idea
By replacing outsourced physical design layout, proprietary EDA licensing suites, and full mask sets with an in-house automated open-source RTL-to-GDSII flow and Multi-Project Wafer (MPW) shared shuttles, total chip development cost drops from $2M–$5M down to ₹0.6–1.2 Cr ($70k–$140k).

---

## Frameworks Introduced

### 1. The 10x Semiconductor Cost Dismantling Ledger
- **When to use**: Auditing semiconductor NRE line items to eliminate deadweight margin drag.
- **How**:
  - Replace outsourced layout contractors with automated digital scripts (`OpenROAD`, `Yosys`).
  - Replace closed-source EDA licenses with open-source synthesis, place-and-route, extraction, and verification tools.
  - Utilize shared multi-project wafer (MPW) runs ($14,950 / ₹14.3 Lakhs for 100 packaged parts on `sky130`) instead of dedicated mask sets ($500k–$1M) during prototyping.

---

## Reference Tables

### Line-by-Line Cost Comparison Matrix
| Cost Item | Conventional Chip Company | DeepGrid Automated Flow | Economic Impact |
|---|---|---|---|
| **Physical Layout** | $1,000,000 – $2,000,000 (Outsourced) | In-house staff time only on open kits | Eliminates up to $2M cash outflow |
| **EDA Tool Licenses** | $500,000 – $1,000,000 / year | Free open-source toolchain | Zero annual software recurring cost |
| **Design Cycle Time** | 12–18 months per chip | RTL to GDSII in <30 days; silicon in 198d | Accelerates time-to-market by 3x–4x |
| **Prototype Masks** | $500,000 – $1,000,000 (Full set) | Shared MPW: ₹14.3L (`sky130`), ₹34–80L (`IHP`) | Prototyping cost reduced by 95% |
| **Testing & Qualification**| Rolled into untracked project overhead | ₹40–80 Lakhs (Explicitly budgeted) | Predictable, audited compliance |
| **TOTAL PER CHIP** | **$2,000,000 – $5,000,000** | **₹0.6 – 1.2 Crore ($75k–$145k)** | **~10x Lower Barrier to Entry** |

---

## The Open-Source EDA Toolchain Stack
- **Logic Synthesis**: `Yosys` (RTL elaboration and gate-level mapping)
- **Floorplanning & Placement**: `OpenROAD` (Automated macro placement and cell spreading)
- **Clock Tree Synthesis (CTS)**: `TritonCTS` (Balanced low-skew clock tree insertion)
- **Global & Detailed Routing**: `TritonRoute` (Design-rule-correct routing)
- **Parasitic Extraction (RCX)**: `OpenRCX` (Parasitic resistance and capacitance extraction)
- **Design Rule Checking (DRC) & LVS**: `Magic` and `KLayout` (Final sign-off verification)

---

## Code Example: Automated Flow Invocation
```tcl
# OpenROAD Automated Scripted Synthesis & Floorplan Pipeline
read_verilog dgrid_motor_core.v
synth -top dgrid_motor_core
read_liberty -min sky130_fd_sc_hd__min.lib -max sky130_fd_sc_hd__max.lib
initialize_floorplan -site unithd -die_area "0 0 1500 1500" -core_area "10 10 1490 1490"
place_pins -hor_layer met3 -ver_layer met2
global_placement -density 0.70
clock_tree_synthesis -root_clk sys_clk -buf_list "sky130_fd_sc_hd__clkbuf_16"
detailed_route -output_drc drc_violations.rpt
write_gds dgrid_motor_core.gds
```
- **What it demonstrates**: Deterministic, zero-touch headless digital flow executing complete layout in minutes without proprietary licensing tokens.

---

## Key Takeaways
1. A small team can build a wide 10-chip portfolio because iteration cost is staff time, not million-dollar layout invoices.
2. Low-volume chips (10,000 units/year) yield 60%–75% gross margins at ₹0.6–1.2 Cr NRE.
3. SkyWater `sky130` MPW shuttles provide ~15 mm² die area and 100 packaged parts for $14,950 (₹14.3 Lakhs).

---

## Connects To
- **Ch 5**: The 198-day loop turning automated GDSII into validated silicon.
- **Ch 13**: Seed round capital allocation across MPWs, mask sets, and qualification.
