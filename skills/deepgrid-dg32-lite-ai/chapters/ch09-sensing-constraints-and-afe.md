# Chapter 9: What the Sensing Supports (Analog Front-End Constraints)

## Core Idea / Thesis
Compute and memory are **not** the binding constraints on these thirty use cases. The true binding constraint is the **Analog Front End (AFE)**: converter resolution, signal dynamic range, and sensor bandwidth.

---

## 1. Why Motor Current Sensing Requires >8 Bits

Under ISO 13373-2, usable dynamic range ($D$) is defined as:
$$D = 6(N - 1)\text{ dB}$$
where $N$ is the number of effective ADC bits.

- For an **8-bit ADC**, $D = 6(8 - 1) = 42\text{ dB}$.
- According to **ISO 20958**, broken rotor bar sidebands sit **100 to 1,000 times below the fundamental current**—a range of **$-40\text{ dBc}$ to $-60\text{ dBc}$**.
- **The Physical Problem**: The entire diagnostic signature sits directly at or beneath the quantization noise floor of an 8-bit converter.
- **The Engineering Solution**: Detection of broken rotor bars, eccentricity, and stator inter-turn shorts requires:
  1. Either an active analog fundamental notch filter and pre-gain stage, OR
  2. A native **12-bit to 16-bit high-resolution ADC**.

---

## 2. Sensor Tiering Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 1: SINGLE ACCELEROMETER (The Highest-Value Addition)             │
│ • Bearings represent 44% of motor failures, yet are the weakest fault   │
│   class for current-only sensing. (Rotor bars = only 8–10%).          │
│ • Sensor Requirement: ≥5 kHz usable flat bandwidth.                   │
│   (Low-cost MEMS parts rolling off at 1–3 kHz miss the high-frequency  │
│   bearing resonance band, rendering envelope analysis useless).        │
│ • Mechanical Mounting Requirement: Stud mounting per ISO 13373-1       │
│   (Magnetic mounts or adhesives attenuate high-frequency shock pulses).│
├────────────────────────────────────────────────────────────────────────┤
│ TIER 2: THREE-PHASE CURRENT + VOLTAGE (Instantaneous Power)            │
│ • Unlocks negative-sequence detection of stator inter-turn shorts and  │
│   Park's vector trajectory analysis per ISO 20958 Annex A.             │
│ • Requires a multi-channel synchronized ADC.                           │
├────────────────────────────────────────────────────────────────────────┤
│ WHAT WORKS TODAY ON DG32-LITE UNCHANGED:                               │
│ • Vibration-based classification (with external digital accelerometer)  │
│ • Sensorless rotor position observation (EKF)                          │
│ • Sensor plausibility verification (Nearest Centroid)                  │
│ • Operating regime identification (GMM)                                │
│ • Multivariate anomaly scoring & duty tracking                         │
│ -> These depend on relative changes rather than absolute small-signal  │
│    resolution, operating cleanly on standard 10-bit/12-bit peripherals.│
└────────────────────────────────────────────────────────────────────────┘
```
