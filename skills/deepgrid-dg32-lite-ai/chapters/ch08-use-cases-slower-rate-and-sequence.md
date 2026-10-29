# Chapter 8: Use Cases — Slower-Rate and Sequence Tracking

## Core Idea / Thesis
Not every diagnostic task must execute at kilohertz frequencies. Long-term degradation, mechanical drift, Remaining Useful Life (RUL), and novelty detection operate on hourly or minute-scale horizons, fitting comfortably within the DG32-LITE memory and scalar execution envelope.

---

## The 6 Slower-Rate & Sequence Use Cases

| # | Use Case | What It Detects | Physical Sensing Input | DSP Features Extracted | Classifier Model | Memory Budget | Latency @ 50 MHz | Max Rate |
|---|---|---|---|---|---|---|---|---|
| **25** | **Remaining-Useful-Life (RUL)** | Long-term degradation trajectory & failure horizon | 64 hourly feature snapshots | None (history buffer) | MLP (128-64-32-8) | 10.5 KB | 0.84 ms | 970 Hz |
| **26** | **Unsupervised Drift Detection** | Reconstruction error against baseline healthy manifold | Any fused sensor set | Statistical moments | MLP Autoencoder | 5.5 KB | 0.58 ms | >1 kHz |
| **27** | **Short-Horizon Forecasting** | Predicts critical process variables a few steps into the future | Any slow scalar variable (64-step history) | None (normalized vector) | GRU (16 Units) | 1.6 KB | 2.95 ms | 270 Hz |
| **28** | **Raw-Waveform Fault Classification**| End-to-end classification directly from raw sampled window | Accelerometer or phase current | Decimation only | 1D-CNN (8/16/32) | 14.0 KB | 10.32 ms | 79 Hz |
| **29** | **Novelty Detection Without Labels** | Outlier score for unprecedented machine failure states | Any fused multi-sensor feature set | Statistical moments | Isolation Forest | 8.0 KB | 0.20 ms | >1 kHz |
| **30** | **Per-Machine Baselining** | On-device prototype clustering without backward-pass learning | Any fused multi-sensor feature set | Statistical moments | k-NN (200 Prototypes) | 6.4 KB | 0.65 ms | >1 kHz |

---

## Architectural Analysis: When to Use Deep vs. Statistical Models
- **Autoencoder Drift Detection (5.5 KB, 0.58 ms)**: Encodes multi-sensor normal states into a compressed latent bottleneck. When mechanical wear or loose mountings introduce subtle deviations, the reconstruction error spikes, providing unsupervised health indexing without labelled defect data.
- **The Raw-Waveform 1D-CNN Trade-off (14 KB, 10.32 ms, 79 Hz)**:
  - Consumes **512,000 clock cycles**—the heaviest workload in the catalog.
  - While it fits within the 16.5 KB memory ceiling and executes in 10.3 ms, it bounds sampling rates to **79 Hz**.
  - **Engineering Guideline**: Only deploy 1D-CNN if classical DSP feature engineering (envelope demodulation, Goertzel) provably misses non-linear wavepacket interactions.
- **Zero-Backprop Field Baselining**: k-NN with 200 prototypes allows a machine to learn its own installation baseline after commissioning by updating centroid coordinates without requiring on-chip gradient descent or matrix inversions.
