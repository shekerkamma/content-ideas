# Chapter 2: Where a Scalar Core is Strong (Algorithm Hierarchy)

## Core Idea / Thesis
The absence of a specialized hardware MAC array reverses traditional deep-learning algorithm rankings. On a scalar CPU, conditional branches, comparisons, and lookups cost virtually nothing, while matrix multiplies dominate execution time.

---

## Why Tree Ensembles Win on Scalar Silicon

Tree ensembles provide the highest accuracy per clock cycle on microcontrollers:
- A **100-tree random forest** evaluated at depth 8 requires roughly **800 comparison instructions and zero multiplications**.
- Total execution time is **0.06 ms** (3,200 clock cycles at 50 MHz), comfortably executing at sample rates exceeding **1 kHz**.
- By comparison, an equivalent neural network matching the same classification accuracy on bearing defects or power-quality events consumes **50× to 500× more clock cycles**.

### The CWRU Bearing Benchmark Proof
This architectural preference is not a low-compute compromise; physical mechanical systems do not require deep representation learning:
- On the benchmark Case Western Reserve University (CWRU) bearing dataset, a random forest evaluated over just **five time-domain features** achieves **95.6% accuracy**.
- Reducing the feature set from nine dimensions down to five costs only **0.1%** in accuracy.
- A meta-review of 42 published academic papers showed classical Support Vector Machines (SVM) achieving **95%–100% accuracy** versus deep neural architectures achieving **97%–100%**—a statistically indistinguishable delta in production environments.

> **Key Takeaway**: Model capacity is not the bottleneck on physical vibration and current tasks. **Signal conditioning is.**

---

## The Algorithmic Priority Hierarchy

When designing machine learning workloads for DG32-LITE, follow this strict four-tier ranking:

```
┌────────────────────────────────────────────────────────────────────────┐
│ FIRST CHOICE: SUB-MILLISECOND, ZERO-MULTIPLY, INSPECTABLE              │
│ • Tree Ensembles (Random Forest, Gradient Boosting, Isolation Forest) │
│ • Linear Discriminants (LDA, Logistic Regression)                      │
│ • Statistical Distance (PCA + Hotelling T², Mahalanobis score)         │
│ -> Runs >1 kHz, 128 to 3,200 cycles, fully inspectable in the field.   │
├────────────────────────────────────────────────────────────────────────┤
│ SECOND CHOICE: SHALLOW NON-LINEAR BOUNDARIES                           │
│ • Small Dense Multi-Layer Perceptrons (MLP 32-16-8-4, 2,688 cycles)    │
│ • Compact MLP Autoencoders (Unsupervised drift, 22,016 cycles)         │
│ -> Only deploy where a non-linear decision surface is strictly required│
├────────────────────────────────────────────────────────────────────────┤
│ REACH FOR LAST: RECURRENT & CONVOLUTIONAL SEQUENCES                    │
│ • Gated Recurrent Units (GRU 16 units: 2.95 ms, 147k cycles)           │
│ • 1D Convolutional Networks (1D-CNN: 10.24 ms, 512k cycles)            │
│ -> Only deploy where raw waveforms contain high-frequency features     │
│    that hand-engineered DSP stages provably miss.                      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## The Iron Design Rule
> **Spend effort on band selection, envelope demodulation, and operating-condition normalisation BEFORE spending it on model capacity.**
