---
name: deepgrid-dg32-2dom
description: System architecture, register maps, CDC bridges, INT8 attention engine, and AVIP bearing-fault diagnostics for DeepGrid Semi's DG32-2DOM dual-domain SoC on chipIgnite CI2612 (sky130A 130 nm, 3400 x 4500 um die).
---

# DeepGrid Semi — DG32-2DOM System Architecture & Attention Variant

This skill provides an authoritative, un-hallucinated engineering reference for the **DG32-2DOM attention variant** (`dg32_2dom`, `INCLUDE_ATTN=1`) taped out on the chipIgnite CI2612 shuttle (sky130A 130 nm, 3400 × 4500 µm die, A3 revision).

## Key Architectural Constants & Specifications
- **Silicon Envelope**: 3400 × 4500 µm die (15.30 mm² total; placed cell+macro area is 5.93 mm²).
- **Dual Clock Domains**:
  - `clk_i`: 50 MHz CPU & control peripheral domain (timing closed to 54 MHz; core post-route $f_{\max}$ is 55–62 MHz).
  - `clk_fast_i`: 114 MHz fast accelerator domain for the INT8 attention engine.
  - Crossings handled via 4-phase req/ack level handshakes with 2-FF synchronizers (`dgrid_axi_cdc_*`).
- **CPUs & Memory Architecture**:
  - 2× RV32IMC DGridRiscV cores in lockstep (`dgrid_lockstep_core` + `dgrid_lockstep_check`).
  - Checker core utilizes private 16 KB DMEM (8 macros) with outputs discarded to guarantee isolation.
  - Main data memory: 32 KB AXI SRAM at `0x9000_0000` (16 sky130 1rw1r macros, 512×32 each). The idle second read port enables contention-free DMA/attention feeding.
  - Dedicated 64 KB baked std-cell Boot ROM (fetch port is private slave; LSU is sole shared-bus master).
  - CPU PMA whitelist: `fault = !(addr[31] | addr[31:28] == 0x1)`.
- **21-Slave Top-Level AXI Fabric**:
  - Decoded via `addr[31:28]` and `addr[27:24]`.
  - Unmapped accesses complete with `SLVERR` (never hangs, preventing CPU LSU bus bricks).
- **INT8 Attention Engine (`dgrid_int8_attn`, 0xE000_0000)**:
  - Executes $QK^T$, row max, 256-entry u15 EXP, $Z$, $E \cdot V$, per-row reciprocal, saturate to int8.
  - 40-bit signed numerator datapath (exact up to $N_K = 131,072$; int32 breaks at $N_K = 512$).
  - Softmax weights never quantized (u15 preserved into 40-bit accumulator).
  - 48-step restoring divider for per-row reciprocal calculation.
  - On-chip K buffer ($N_K \times K_D$) and V buffer ($N_K \times D_V$) SRAM macros loaded once per kick, re-read per row.
- **AVIP Bearing-Fault Application**:
  - Multimodal classifier (47,076 params CWRU model; 478,277 params full model) running in 46.7 ms on `clk_fast_i`.
  - Stator Current Signature Analysis (CSA) via on-die SAR ADC (0xDB) sampled at PWM ripple null — **requires zero external vibration probes or accelerometers**.
- **FOC Control-Loop Budget**:
  - Fixed hardware cost: ~300 cycles (~6 µs) at 50 MHz (ADC sample 177 cycles, CORDIC transforms 53-58 cycles, PWM write).
  - At 10 kHz loop rate (5,000 cycles), leaves 4,700 cycles (>90% headroom) for software observers and state machines.
