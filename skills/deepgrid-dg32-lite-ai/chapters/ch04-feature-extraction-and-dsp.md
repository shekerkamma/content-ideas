# Chapter 4: Feature Extraction, Costed

## Core Idea / Thesis
Every practical edge AI pipeline pairs one or two digital signal processing (DSP) front-end stages with a lightweight model. Because DG32-LITE integrates a hardware CORDIC unit that already executes Park, Clarke, polar magnitude, and $\text{atan2}$ for the motor-control loop, the diagnostic front-end reuses what the hardware has already computed for free.

---

## The 9 Costed DSP Front-End Stages

| Stage / Algorithm | Cycles @ 50 MHz | Execution Time | Output / What It Yields |
|---|---|---|---|
| **256-Point Real FFT** | 30,720 | 0.61 ms | Band energies, spectral peaks, harmonic ratios |
| **512-Point Real FFT** | 69,120 | 1.38 ms | Finer spectral resolution for gear-mesh and sideband work |
| **Envelope Demodulation** | 5,000 | 0.10 ms | CORDIC magnitude (20 iterations) — the bearing-fault front end |
| **Goertzel Algorithm (8 Bins)** | 6,144 | 0.12 ms | Targeted narrowband tone detection at predicted physical fault frequencies |
| **Statistical Moments** | 7,000 | 0.14 ms | RMS, kurtosis, crest factor, skewness (ISO 20816 baseline) |
| **Broadband RMS Velocity** | 3,000 | 0.06 ms | ISO 20816 vibration severity zone classification (Zone A/B/C/D) |
| **Haar Wavelet (256 Samples)** | 15,000 | 0.30 ms | Multi-scale time-frequency features for impact and transient faults |
| **Park / Clarke Transform** | 120 | <0.01 ms | CORDIC-accelerated; already computed by the motor control loop |
| **Decimation & Bandpass** | 4,000 | 0.08 ms | IIR biquad filtering ahead of envelope or raw-waveform models |

---

## Why Feature Extraction Matters More Than Model Capacity

A comprehensive feature-ranking study across twelve diagnostic features demonstrated that **demodulated features evaluated at the exact physical fault frequency outrank raw statistical moments by a factor of 4 to 5**:
- **Hilbert-Huang Amplitude** at the outer-race bearing fault frequency scored **225.9**.
- **Raw Peak-to-Peak Amplitude** scored only **51.8**.

### The Cheap Envelope Extraction Pipeline
Instead of running a 100,000-parameter deep network over raw signals, the optimal microcontroller pipeline is:
1. Digital bandpass filter around the bearing mechanical resonance.
2. Full-wave rectify or Hilbert transform.
3. Low-pass filter.
4. **Decimate down to 1–2 kS/s**.
5. Execute a modest 256-point FFT or Goertzel filter.

> **Memory Rule**: Perform decimation **before** buffering. When decimated ahead of storage, the entire DSP working set never exceeds **a few kilobytes**.

---

## Critical Engineering Warning: The Kurtosis Trap

> [!WARNING]
> **Kurtosis is non-monotonic across defect progression.**

- **Early Defect Stage**: Incipient localized spalls cause sharp, impulsive shockwaves that dramatically spike the kurtosis value far above the Gaussian baseline of 3.0.
- **Advanced Defect Stage**: As spalling spreads and defect surfaces become rough and continuous, impacts merge into widespread random vibration. The vibration signal becomes Gaussian again, and **kurtosis drops back to normal baseline levels**.
- **RMS Behavior**: Root-Mean-Square (RMS) vibration velocity exhibits the exact opposite behavior: it is stable and monotonically increases as damage escalates, but is completely blind to early incipient micro-cracks.
- **Operational Rule**: Always trend **both** Kurtosis and RMS velocity simultaneously. **Never trigger an automated shutdown or critical alarm based on kurtosis alone.**
