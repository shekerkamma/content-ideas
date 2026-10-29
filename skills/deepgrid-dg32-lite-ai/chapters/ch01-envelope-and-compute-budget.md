# Chapter 1: The Compute Envelope (DG32-LITE Base Variant)

## Core Idea / Thesis
Every algorithmic and diagnostic capability on the DG32-LITE base variant derives from four physical parameters: **12.5 MMAC/s** scalar throughput, a **16.5 KB** model memory ceiling, **82%** free CPU cycles (assuming a 10 kHz FOC loop), and hardware assistance from an integrated **CORDIC** block.

---

## The Four Fundamental Constants

| Parameter | Specification | Physical / Architectural Derivation |
|---|---|---|
| **Scalar Throughput** | **12.5 MMAC/s** | RV32IM core at 50 MHz clock; int8 arithmetic well-blocked (4 cycles per int8 multiply-accumulate). Back-solved from design docs, not measured on silicon. |
| **Model Memory Budget** | **16.5 KB** | Weights plus peak activation buffer. Can expand to **29.5 KB** if the inference runtime library is pre-burned into mask ROM. |
| **Free CPU Cycles** | **82 %** | At a 10 kHz field-oriented control (FOC) rate, the dedicated hardware peripherals handle ADC sampling, Park/Clarke, and PWM edges in ~300 cycles (~6 µs), leaving 82% of core cycles for firmware and diagnostics. |
| **Hardware Help** | **CORDIC Engine** | Pre-existing hardware pipeline computing $\sin$, $\cos$, $\text{atan2}$, and polar magnitude in under 20 clock cycles without CPU intervention. |

---

## What the Missing Attention Engine Costs

DG32-2DOM features an isolated 114 MHz INT8 attention engine; DG32-LITE omits it.
- **Speed on one specific operator, not capability**: An attention kernel configured at 64/32/32 dimensions requires **0.26 MMAC**, which translates to approximately **21 ms** in pure software on the 50 MHz RV32IM core.
- **Why it does not bind**: None of the thirty industrial predictive maintenance and control tasks require self-attention. The machine-learning algorithms that natively suit a scalar core (Random Forest, Gradient Boosting, LDA, PCA/Mahalanobis) are **30× to 300× cheaper** than a transformer while achieving statistically indistinguishable accuracy on physical sensor streams.

---

## Cycle & Memory Budgets Across Sampling Rates

The mathematical limit on MAC operations per inference tick is:
$$\text{MAC Budget per Inference} = \frac{12.5 \times 10^6}{\text{Sample Rate (Hz)}}$$

- **At 10 Hz (Slow Process Diagnostics)**: 1.25 MMAC per inference.
- **At 100 Hz (Sub-Harmonic Mechanical)**: 0.125 MMAC (125 kMAC) per inference.
- **At 1 kHz (Real-Time Control Loop)**: 12.5 kMAC per inference.

The second gating constraint is memory:
$$\text{Weights} + \text{Peak Working State Activation} \le 16.5\text{ KB}$$

### Real-World Clearance
- Across the thirty use cases documented, the absolute worst-case latency is **10.3 ms** (1D-CNN) and peak memory is **20 KB** (100-tree Random Forest).
- **24 of the 30 use cases run comfortably above 1 kHz**.
- **The actual binding constraint**: The bottleneck in edge motor diagnostics is almost never compute or RAM—it is the **Analog Front End (AFE)** dynamic range and bandwidth (covered in Chapter 9).
