# Chapter 5: Use Cases — Rotating Machinery

## Core Idea / Thesis
Rotating mechanical assets (bearings, gearboxes, pumps, fans, compressors) represent the largest category of industrial downtime. Bearings alone account for **44% of all motor failures**. DG32-LITE executes 8 dedicated mechanical defect classifiers directly on the drive microcontroller without external processing hardware.

---

## The 8 Rotating Machinery Use Cases

| # | Use Case | What It Detects | Physical Sensing Input | DSP Features Extracted | Classifier Model | Memory Budget | Latency @ 50 MHz | Max Rate |
|---|---|---|---|---|---|---|---|---|
| **1** | **Bearing Fault Classification** | Inner race (BPFI), outer race (BPFO), ball (BSF), cage (FTF) defects | Accelerometer ($\ge 5\text{ kHz}$ bandwidth) | Envelope demodulation + 256-pt FFT + moments | Random Forest (100×d8) | 20.0 KB | 0.92 ms | 890 Hz |
| **2** | **Bearing Severity Trending** | ISO 20816 Zone A/B/C/D severity from broadband RMS velocity | Accelerometer | Decimation + RMS velocity | Linear Discriminant (LDA) | 0.7 KB | 0.14 ms | >1 kHz |
| **3** | **Gearbox & Gear-Mesh Faults** | Broken/chipped teeth, mesh-frequency sideband growth | Accelerometer, order-tracked on encoder | Envelope + 512-pt FFT + moments | Random Forest (100×d8) | 20.0 KB | 1.69 ms | 480 Hz |
| **4** | **Pump Cavitation & Dry-Run** | Disentangles cavitation bubbles from dry-running and high load | Motor phase current + pressure transducer via SPI | 256-pt FFT + statistical moments | Gradient Boosting (200×d4) | 12.0 KB | 0.82 ms | >1 kHz |
| **5** | **Fan & Blower Imbalance** | Aerodynamic blade damage, $1\times$ and $2\times$ rotational unbalance | Accelerometer + optical tachometer | 256-pt FFT + statistical moments | Linear Discriminant (LDA) | 0.7 KB | 0.76 ms | >1 kHz |
| **6** | **Compressor Valve Faults** | Valve reed leakage and flutter correlated against crank angle | Accelerometer + crank angle reference | Envelope demodulation + 256-pt FFT | Random Forest (100×d8) | 20.0 KB | 0.78 ms | >1 kHz |
| **7** | **Belt Slip & Misalignment** | Dual-encoder phase differential or vibration harmonic distortion | Dual encoders or single accelerometer | 256-pt FFT spectrum | Logistic Regression | 0.7 KB | 0.62 ms | >1 kHz |
| **8** | **Shaft Misalignment & Looseness** | $1\times$, $2\times$, $3\times$ shaft harmonic distortion patterns | Single accelerometer | 256-pt FFT + statistical moments | Random Forest (100×d8) | 20.0 KB | 0.82 ms | >1 kHz |

---

## Architectural Notes & Execution Rules
- **Bearing Diagnostics**: Uses CORDIC-accelerated envelope demodulation (5,000 cycles) + 256-point FFT (30,720 cycles) + Random Forest (3,200 cycles). Total cycle cost is ~46,000 cycles (0.92 ms), allowing execution at **890 Hz**.
- **Gear-Mesh Analysis**: Requires finer spectral resolution (512-point FFT) to resolve tight sideband clusters around the tooth meshing frequency ($f_m = z \cdot f_r$). Total latency is 1.69 ms, bounding maximum continuous analysis to **480 Hz**.
- **Cavitation Separation**: Motor Current Signature Analysis (MCSA) alone struggles with light cavitation; pairing motor phase current with a digitized SPI pressure sensor yields robust gradient boosting classification in **0.82 ms**.
