---
name: deepgrid-dg32-lite-ai
description: "Edge AI and predictive diagnostics playbook for DeepGrid Semi's DG32-LITE scalar RISC-V core without hardware accelerators: 30 industrial use cases, 19 lightweight model architectures, DSP feature extraction, CWRU benchmark audits, and ISO 13373/20816/20958 sensing constraints."
---

<!-- argument-hint: [use case name, model type, dsp stage, or chapter number] -->

# DeepGrid Semi — DG32-LITE AI Playbook (Thirty Use Cases, No Accelerator)

**Author**: Deepgrid Semi Pvt Ltd · Base Variant | **Source**: 12-Page DG32-LITE AI Technical Annex | **Date**: September 2026

## Core Architectural Thesis
On a 50 MHz RV32IM scalar core with a hardware CORDIC unit and no neural accelerator, edge intelligence is not achieved by shoehorning heavy transformers or deep CNNs. It is achieved through **mathematical hierarchy and signal conditioning**:
1. **Model Hierarchy**: Tree ensembles (Random Forest, Gradient Boosting), linear discriminants (LDA), and statistical distance metrics (Mahalanobis, PCA + Hotelling $T^2$) provide 95%+ accuracy at 50–500× lower cycle cost than neural nets.
2. **Signal Conditioning Over Capacity**: Band selection, envelope demodulation, and Goertzel filters evaluated at known physical fault frequencies outrank raw moments by 4–5×.
3. **Hard Envelope**: 12.5 MMAC/s scalar throughput, 16.5 KB model budget (29.5 KB with mask ROM runtime), 82% free CPU cycles (10 kHz FOC loop), supporting 24 of 30 use cases above 1 kHz.

---

## How to Use This Skill
- **Without arguments** — Load the compute envelope, model hierarchy, and master use case index.
- **With use case name** — Query any of the 30 specific industrial use cases:
  - *Rotating Machinery*: `Bearing Fault Classification`, `Bearing Severity Trending`, `Gearbox Faults`, `Pump Cavitation`, `Fan Imbalance`, `Compressor Valve`, `Belt Slip`, `Shaft Misalignment`.
  - *Electrical & Power*: `Broken Rotor Bar`, `Air-Gap Eccentricity`, `Stator Inter-Turn Short`, `Phase Loss`, `Arc-Fault Discharge`, `Power Quality`, `Battery SoH`, `Winding Thermal`.
  - *Control & Motion*: `Sensorless Rotor Position (EKF)`, `Sensor Plausibility`, `Operating Regime`, `Duty Cycle Tracking`, `Adaptive Friction`, `Stall Detection`, `Torque Ripple`, `Multivariate Anomaly`.
  - *Slow-Rate & Sequence*: `Remaining Useful Life (RUL)`, `Unsupervised Drift`, `Short-Horizon Forecast`, `Raw Waveform CNN`, `Isolation Forest Novelty`, `k-NN Baselining`.
- **With chapter number** — Ask for `ch01` through `ch10` to inspect cycle budgets, memory footprint, and DSP stages:
  - `ch01`: The Compute Envelope (12.5 MMAC/s, 16.5 KB budget, 82% free cycles, CORDIC).
  - `ch02`: Algorithm Choice on Scalar Cores (Why trees dominate neural nets, CWRU benchmark reality).
  - `ch03`: The Nineteen Models that Fit (Cycles, latency, memory, max sampling rate).
  - `ch04`: Feature Extraction & DSP (FFT, CORDIC envelope demodulation, Goertzel, wavelets, kurtosis warning).
  - `ch05`: Rotating Machinery Use Cases (8 mechanical vibration/current diagnostics).
  - `ch06`: Electrical & Power Diagnostics (8 motor current signature & thermal models).
  - `ch07`: Real-Time Control & Motion Observers (8 low-latency FOC & closed-loop models).
  - `ch08`: Sequence, Drift & Forecasting (6 slow-rate trend & autoencoder models).
  - `ch09`: Sensing & Analog Front-End Constraints (ISO 13373-2 dynamic range, Goertzel vs FFT, accelerometer bandwidth).
  - `ch10`: Basis, Verification & Falsification (CWRU data leakage trap, pre-silicon advisory role).

---

## Master Chapter Index

| # | Chapter Title | Core Engineering Findings |
|---|---|---|
| [ch01](chapters/ch01-envelope-and-compute-budget.md) | **The Compute Envelope** | 12.5 MMAC/s scalar rate, 16.5 KB memory ceiling, 82% free cycles at 10 kHz FOC loop. |
| [ch02](chapters/ch02-algorithm-choice-scalar-core.md) | **Where a Scalar Core is Strong** | Tree ensembles require 0 multiplies (0.06 ms); SVM/RF match deep nets (95–100%). |
| [ch03](chapters/ch03-model-catalogue-nineteen-models.md) | **The Nineteen Models That Fit** | Exact cycle, memory, and latency costs for 19 ML architectures on RV32IM. |
| [ch04](chapters/ch04-feature-extraction-and-dsp.md) | **Feature Extraction, Costed** | CORDIC envelope demodulation (0.10 ms), Goertzel (0.12 ms), kurtosis non-monotonicity. |
| [ch05](chapters/ch05-use-cases-rotating-machinery.md) | **Use Cases: Rotating Machinery** | 8 mechanical defect detectors: bearings (44% of failures), gearboxes, pumps, fans. |
| [ch06](chapters/ch06-use-cases-electrical-and-power.md) | **Use Cases: Electrical & Power** | 8 MCSA diagnostics: broken rotor bars, air-gap eccentricity, stator shorts, arc-faults. |
| [ch07](chapters/ch07-use-cases-control-motion-sensing.md) | **Use Cases: Control & Motion** | 8 real-time observers: EKF sensorless flux, sensor plausibility, stall detection. |
| [ch08](chapters/ch08-use-cases-slower-rate-and-sequence.md) | **Use Cases: Slow-Rate & Sequence** | 6 trend estimators: RUL regression, autoencoder drift, GRU forecasting, k-NN baselining. |
| [ch09](chapters/ch09-sensing-constraints-and-afe.md) | **What the Sensing Supports** | Why current needs >8 bits (ISO 13373-2), Goertzel vs 8MB FFT, Tier 1/2 sensors. |
| [ch10](chapters/ch10-basis-methodology-and-benchmarks.md) | **Basis, Benchmarks & Limits** | CWRU data leakage debunking (85.8% → 69.5%), advisory role under lockstep monitor. |

---

## Supporting Files
- [patterns.md](patterns.md) — Architectural patterns: DSP before capacity, envelope demodulation, Goertzel vs FFT, non-monotonic kurtosis.
- [glossary.md](glossary.md) — Technical terminology: MMAC/s, MCSA, CWRU, Goertzel, Hotelling T², kurtosis, ISO 20816.
- [cheatsheet.md](cheatsheet.md) — The complete 30-use-case table, 19-model catalogue, and DSP cost matrix.
