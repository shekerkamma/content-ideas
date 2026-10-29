# Chapter 7: Use Cases — Control, Motion and Sensing

## Core Idea / Thesis
By embedding lightweight state estimators directly into the inner control loop, DG32-LITE achieves sensorless operation, detects mechanical stalls in under a millisecond, and validates sensor plausibility without adding external BOM cost.

---

## The 8 Control & Motion Use Cases

| # | Use Case | What It Detects | Physical Sensing Input | DSP Features Extracted | Classifier Model | Memory Budget | Latency @ 50 MHz | Max Rate |
|---|---|---|---|---|---|---|---|---|
| **17** | **Sensorless Rotor Position** | Replaces physical Hall/encoder sensors with high-speed flux tracking | Motor phase current (CORDIC-assisted) | Hardware Park transform | Extended Kalman Filter (EKF) | 2.0 KB | 0.05 ms | >1 kHz |
| **18** | **Learned Sensor Plausibility** | Cross-validates Encoder vs. Hall vs. Back-EMF signals | Existing peripherals (no added BOM) | Hardware Park transform | Nearest Centroid | 1.0 KB | 0.02 ms | >1 kHz |
| **19** | **Operating-Mode Classification**| Identifies active duty regime (idle, acceleration, steady, braking) | Encoder, Hall, current, temperature | RMS velocity & amplitude | Gaussian Mixture (GMM) | 2.0 KB | 0.10 ms | >1 kHz |
| **20** | **Duty-Cycle & State Tracking** | Starts, dwell times, thermal recovery, regime transitions | Existing hardware timers and flags | None (discrete events) | Hidden Markov Model (8-State) | 2.0 KB | 0.06 ms | >1 kHz |
| **21** | **Adaptive Friction Compensation**| Learns mechanical cogging and Coulomb/viscous friction feedforward | Optical/magnetic encoder + phase current | Hardware Park transform | MLP (32-16-8-4) | 0.7 KB | 0.06 ms | >1 kHz |
| **22** | **Kickback & Stall Detection** | Distinguishes normal transient load spikes from hard mechanical jams | Phase current | RMS current slope | Gradient Boosting (200×d4) | 12.0 KB | 0.12 ms | >1 kHz |
| **23** | **Load Estimation & Torque Ripple**| Resolves parasitic cogging and load torque harmonic components | Phase current | 256-pt FFT spectrum | Logistic Regression | 0.7 KB | 0.62 ms | >1 kHz |
| **24** | **Multivariate Anomaly Scoring** | Single aggregated novelty scalar raised as an interrupt (IRQ) | Any fused multi-sensor feature vector | Statistical moments | Mahalanobis Distance | 2.0 KB | 0.22 ms | >1 kHz |

---

## Architectural Highlights
- **Zero-Latency Sensorless Control**: The EKF rotor observer executes in **0.05 ms (2,400 cycles)**, allowing sensorless field-oriented control loops to run at rates exceeding **10 kHz** with zero auxiliary processing cores.
- **Sensor Plausibility (ASIL-D Functional Safety)**: Compares measured encoder position against predicted back-EMF state. If a physical wire snaps or noise corrupts the optical track, Nearest Centroid flags the mismatch within **0.02 ms**, allowing safe-state entry before power bridge damage.
- **Hardware Interrupt on Anomaly**: Multivariate Mahalanobis distance condenses multi-sensor streams into a single statistical scalar metric. If the scalar crosses a programmable confidence boundary, an internal hardware IRQ fires within **0.22 ms**.
