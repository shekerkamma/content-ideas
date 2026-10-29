# Chapter 8: The Processor Every Chip Shares: DGridRiscV

## Core Idea
Seven of the ten SKUs embed an identical custom RV32IM RISC-V processor core (`DGridRiscV`). Every omitted microarchitectural feature (no cache, no branch prediction, no FPU, no compressed instructions) is a deliberate engineering decision designed to guarantee deterministic, sub-microsecond real-time control latency and zero silicon waste.

---

## The Verifiable Hardware Architecture Specs

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DGridRiscV PROCESSOR CORE SPECIFICATIONS                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Instruction Set Architecture │ RV32IM_Zicsr (misa = 0x40001100)              │
│ Privilege Levels            │ Machine Mode Only (Bare-metal / RTOS)         │
│ Pipeline Stages             │ 8-stage (2 Fetch, 6 Execute stages)           │
│ Dispatch & Issue Width      │ Single-issue, strict in-order execution       │
│ Multiplier & Divider        │ Fully unrolled single-cycle hardware blocks   │
│ Shifter Unit                │ Single-cycle barrel shifter                   │
│ Memory Protection           │ Physical Memory Protection (PMP) regions      │
│ Instruction / Data Buses    │ Dual 32-bit AXI4 ports (Cacheless, fixed TCM) │
│ Target Operating Frequency  │ 200 MHz fixed on 130nm ASIC                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Architectural Rationale: Every Missing Feature Is a Decision

| Omitted Feature | Why Conventional CPUs Have It | Why DeepGrid Deliberately Omitted It |
|---|---|---|
| **L1/L2 Caches** | Maximizes average throughput | Caches miss unpredictably; deterministic control loops require guaranteed worst-case latency (<1 µs). |
| **Branch Predictor** | Hides deep pipeline stalls | Control loops are short and computation-heavy; branch logic wastes valuable chip area and introduces jitter. |
| **Floating-Point Unit (FPU)** | General-purpose decimal math | Fixed-point math arithmetic is smaller, faster, and produces identical bit-for-bit output across all SKUs. |
| **Compressed Instructions (RVC)**| Saves external memory | Memory is on-chip SRAM; omitting decompression simplifies fetch alignment and critical timing paths. |
| **Full MMU (Virtual Memory)** | Multi-tenant OS paging | Replaced with compact hardware PMP regions, providing safety isolation for bare-metal firmware at 10x less area. |

---

## The Control Plane vs. Compute Plane Paradigm
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ON-CHIP SYSTEM TOPOLOGY                           │
│                                                                             │
│   ┌───────────────────────────┐         ┌────────────────────────────────┐  │
│   │    CONTROL PLANE (CPU)    │         │     DATA PLANE (HARDWARE)      │  │
│   │        DGridRiscV         │         │ Dedicated Acceleration Blocks  │  │
│   │    • System setup & boot  │         │ • FOC Motor Control Pipeline   │  │
│   │    • Fault & error triage │ ◄─────► │ • 24-bit Power Metrology Chain │  │
│   │    • Host communications  │         │ • 2048-pt Radar FFT & CFAR     │  │
│   │    • Fixed 200 MHz bus    │         │ • 3,840-col Display TCON       │  │
│   └───────────────────────────┘         └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```
- **Principle**: The CPU is a *controller*, not an execution bottleneck. Heavy algorithmic operations run in dedicated parallel hardware datapaths; the CPU simply handles orchestration, housekeeping, and safety monitoring.

---

## Key Takeaways
1. The DGridRiscV processor is written, simulated, and verified once, amortizing software tools and toolchains across the entire catalog.
2. Omitting caches and branch predictors guarantees sub-microsecond response times for motor drives and safety supervisors.
3. Dedicated hardware accelerators perform math pipelines, freeing the 200 MHz core for system supervisory tasks.

---

## Connects To
- **Ch 6**: Block-level IP reuse across 7 of the 10 SKUs.
- **Ch 9**: Per-SKU architectural integration.
