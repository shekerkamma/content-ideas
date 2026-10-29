# Chapter 12: DG SDV Platform Reference Architecture

## Core Idea / Thesis
DeepGrid's unified system platform architecture unifying a secure root-of-trust enclave, a triple-core lockstep safety domain, a 64-bit multi-core Linux host processor (RV64GCH), and vector/integer accelerator clusters across a coherent 64-bit AXI4 crossbar with AXI-REALM Quality-of-Service (QoS) regulation.

## Authentic Vector Reference
- **Document Source**: DeepGrid Semi SKU Architecture Compendium v3
- **Sheet Reference**: Page 12 (Track B Reference Architecture) — DG SDV Platform

## Physical & Electrical Specifications
| Domain | Processor / Subsystem Architecture | Security / Safety Level |
|---|---|---|
| **DG Secure Domain** | Dual-Lockstep DGI-RV32 Cores + Hardware Crypto DSAs (AES-256, SHA-3, SM4, HMAC) + OTP/BootROM | EVITA-Full / Common Criteria EAL5+ |
| **DG Safe Domain** | **Triple-Core Lockstep (TMR)** DGCV32-RT Cores with Private DSPM/ISPM + ECC | ISO 26262 ASIL-D / IEC 61508 SIL-3 |
| **DG Host Domain** | Multi-Core 64-bit RISC-V Linux Host (DGCVA6RT RV64GCH) with L1 D$/I$ + MMU + Hardware FPU | ASIL-B / POSIX Compliant |
| **DG Accelerators** | Vector Multi-Core (DG RVV) + Integer Multi-Core (DGCV32 Clusters) with Interleaved TCDM Scratchpads | Hardware Acceleration Pipeline |
| **System Interconnect** | 64-bit AXI4 Bus Matrix with **AXI-REALM real-time monitoring and bus bandwidth QoS regulation** | Low-latency, bounded latency |

## Subsystem Block Architecture
```
+-----------------------------------------------------------------------------------+
| DG SECURE DOMAIN: Dual Lockstep DGI-RV32 | Crypto DSAs | OTP | Always-On Power    |
+-----------------------------------------------------------------------------------+
| DG SAFE DOMAIN: Triple-Core Lockstep DGCV32-RT | Private DSPM/ISPM + ECC          |
+-----------------------------------------------------------------------------------+
| DG HOST DOMAIN (Linux): Multi-Core RV64GCH (DGCVA6RT) | FPU | MMU | L1 D$/I$      |
+===================================================================================+
| SYSTEM BUS (64-bit AXI4 Matrix with AXI-REALM QoS Monitor):                       |
|   Connects Host, Safety Island, Secure Enclave, Dynamic SPM, and Accelerators     |
+===================================================================================+
| DG ACCELERATOR DOMAIN:                                                            |
|   Vector Multi-Core (DG RVV)  <-> Low-Latency TCDM Bus <-> Interleaved SPM Banks  |
|   Integer Multi-Core Clusters <-> Dynamic Address Switch <-> Heterogeneous Engs   |
+-----------------------------------------------------------------------------------+
```

## Deep Engineering Questions & Failure Modes
1. **AXI-REALM QoS & Deterministic Latency**: How does the AXI-REALM regulation unit prevent Linux host memory thrashing on the 64-bit crossbar from starving the triple-lockstep real-time safety domain?
2. **Dynamic Scratchpad Memory (SPM) Partitioning**: What arbitration mechanism reconfigures interleaved TCDM SRAM banks between vector processing and integer clusters without requiring cache flush penalties?
3. **Triple-Lockstep Majority Voting Delay**: What is the gate-level voting latency when three DGCV32-RT cores execute with asynchronous branch predictors under transient single-event upsets?
4. **Platform Unification Across SKUs**: How does this platform architecture scale down to SKU-9 (zonal gateway), adapt to the D100 (airborne compute), and interface with SKU-3 (power) and SKU-6 (supervision)?

## Policy, Market & Procurement Hook
- **One Architecture, Many Dies**: Sits as the master architectural reference that standardizes IP block reuse across all 10 DeepGrid SKUs.
- **Strategic Impact**: Establishes an open, sovereign RISC-V compute stack eliminating ARM royalties and foreign vendor lock-in for India's automotive and defence Tier-1s.

## Connects To
- **Chapter 5 (SKU-4)**: Downscaled dual-core derivative of the safe domain.
- **Chapter 10 (SKU-9)**: Implements the zonal vehicle interface for this platform.
- **Chapter 13 (SiP Packaging)**: Assembles platform components into a single multi-die package.
