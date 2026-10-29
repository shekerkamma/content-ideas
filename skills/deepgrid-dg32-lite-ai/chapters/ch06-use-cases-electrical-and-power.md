# Chapter 6: Use Cases — Electrical and Power Diagnostics

## Core Idea / Thesis
Motor Current Signature Analysis (MCSA) allows electrical machines to act as their own transducers. By analyzing phase currents already sampled by the FOC loop, DG32-LITE identifies rotor bar fractures, stator winding shorts, and power quality degradation without extra external sensors.

---

## The 8 Electrical & Power Use Cases

| # | Use Case | What It Detects | Physical Sensing Input | DSP Features Extracted | Classifier Model | Memory Budget | Latency @ 50 MHz | Max Rate |
|---|---|---|---|---|---|---|---|---|
| **9** | **Broken Rotor Bar Detection** | Twice-slip-frequency sidebands: $f_1(1 \pm 2ks)$ | Phase current ($\ge 12$-bit ADC with notch filter) | Goertzel algorithm (narrowband) | Linear Discriminant (LDA) | 0.7 KB | 0.13 ms | >1 kHz |
| **10** | **Air-Gap Eccentricity** | Static & dynamic eccentricity sidebands: $f_1 \pm m \cdot f_r$ | Phase current ($\ge 12$-bit ADC) | Goertzel algorithm (targeted bins) | Linear Discriminant (LDA) | 0.7 KB | 0.13 ms | >1 kHz |
| **11** | **Stator Inter-Turn Short** | Negative-sequence current unbalance index | 3-phase current + voltage | Park transform + RMS | Mahalanobis Distance | 2.0 KB | 0.14 ms | >1 kHz |
| **12** | **Phase Loss & Current Unbalance** | Symmetrical component sequence divergence | Phase current (already sampled in loop) | Park vector calculation | Logistic Regression | 0.7 KB | <0.01 ms | >1 kHz |
| **13** | **Arc-Fault & Partial Discharge** | High-frequency insulation breakdown signature | High-frequency current transformer + envelope | Envelope demodulation + 256-pt FFT | One-Class SVM | 6.9 KB | 0.97 ms | 840 Hz |
| **14** | **Power-Quality Events** | Voltage sag, swell, harmonic distortion (THD), flicker | Mains voltage & current (64 cycles window) | Goertzel harmonic bins | Linear Discriminant (LDA) | 0.7 KB | 0.13 ms | >1 kHz |
| **15** | **Battery State-of-Health (SoH)**| SoH degradation and SoC from charge/discharge curves | Slow voltage / current / temperature sequence | Statistical moments | MLP (32-16-8-4) | 0.7 KB | 0.19 ms | >1 kHz |
| **16** | **Winding Thermal Estimation** | Virtual temperature sensor replacing physical thermistors | Phase current history + ambient temperature | RMS integration over time | Extended Kalman Filter (EKF) | 2.0 KB | 0.11 ms | >1 kHz |

---

## Technical Insights on MCSA Implementation

### 1. The Dynamic Range Constraint (ISO 13373-2)
- Broken rotor bar sidebands sit **40 dB to 60 dB below the fundamental current** ($-40$ to $-60\text{ dBc}$).
- An 8-bit converter yields only 42 dB of theoretical dynamic range ($D = 6(N-1)\text{ dB}$).
- **Requirement**: MCSA diagnostics require either analog fundamental notch suppression or a **12-bit to 16-bit ADC** to avoid operating beneath the quantization noise floor.

### 2. The Goertzel Solution vs. 8 MB FFTs
- Sideband separation ($2 \cdot s \cdot f_1$) ranges from ~3 Hz at full rated load down to **0.5 Hz under light load**.
- Resolving a 0.5 Hz sideband directly via FFT requires records of 30–100 seconds with 0.01–0.05 Hz frequency resolution.
- A direct $2^{20}$-point FFT requires **8 MB of RAM**, exceeding microcontroller budgets by orders of magnitude.
- **DG32-LITE Architecture**: Compute targeted Goertzel filters strictly at the predicted physical sideband frequencies ($f_1(1 \pm 2ks)$). Execution takes **0.13 ms** and fits inside **0.7 KB** of RAM.
