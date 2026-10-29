# Quick Reference Cheatsheet: DG32-LITE AI

## The 30 Industrial Use Cases at a Glance

```
CATEGORY 1: ROTATING MACHINERY (8 Defect Models)
01. Bearing Fault Classification: Envelope + FFT-256 + Moments -> Random Forest 100xd8 [20 KB, 0.92 ms, 890 Hz]
02. Bearing Severity Trending: Decimate + RMS -> LDA [0.7 KB, 0.14 ms, >1 kHz]
03. Gearbox / Mesh Faults: Envelope + FFT-512 + Moments -> Random Forest 100xd8 [20 KB, 1.69 ms, 480 Hz]
04. Pump Cavitation & Dry-Run: FFT-256 + Moments -> Gradient Boosting 200xd4 [12 KB, 0.82 ms, >1 kHz]
05. Fan / Blower Imbalance: FFT-256 + Moments -> LDA [0.7 KB, 0.76 ms, >1 kHz]
06. Compressor Valve Faults: Envelope + FFT-256 -> Random Forest 100xd8 [20 KB, 0.78 ms, >1 kHz]
07. Belt Slip & Misalignment: FFT-256 -> Logistic Regression [0.7 KB, 0.62 ms, >1 kHz]
08. Shaft Misalignment / Looseness: FFT-256 + Moments -> Random Forest 100xd8 [20 KB, 0.82 ms, >1 kHz]

CATEGORY 2: ELECTRICAL & POWER (8 Diagnostics)
09. Broken Rotor Bar Detection: Goertzel (2sf1 sidebands) -> LDA [0.7 KB, 0.13 ms, >1 kHz]
10. Air-Gap Eccentricity: Goertzel (f1 +/- m*fr) -> LDA [0.7 KB, 0.13 ms, >1 kHz]
11. Stator Inter-Turn Short: Park + RMS -> Mahalanobis Score [2 KB, 0.14 ms, >1 kHz]
12. Phase Loss & Unbalance: Park Vector -> Logistic Regression [0.7 KB, <0.01 ms, >1 kHz]
13. Arc-Fault & Partial Discharge: Envelope + FFT-256 -> One-Class SVM [6.9 KB, 0.97 ms, 840 Hz]
14. Power-Quality Events: Goertzel Bins -> LDA [0.7 KB, 0.13 ms, >1 kHz]
15. Battery State-of-Health (SoH): Statistical Moments -> MLP 32-16-8-4 [0.7 KB, 0.19 ms, >1 kHz]
16. Winding Thermal Estimation: RMS History Integration -> EKF [2 KB, 0.11 ms, >1 kHz]

CATEGORY 3: CONTROL, MOTION & SENSING (8 Real-Time Models)
17. Sensorless Rotor Position: Hardware Park Transform -> EKF [2 KB, 0.05 ms, >1 kHz]
18. Learned Sensor Plausibility: Hardware Park Transform -> Nearest Centroid [1 KB, 0.02 ms, >1 kHz]
19. Operating-Mode Classification: RMS Velocity -> Gaussian Mixture Model [2 KB, 0.10 ms, >1 kHz]
20. Duty-Cycle & State Tracking: Hardware Timers -> HMM (8-state) [2 KB, 0.06 ms, >1 kHz]
21. Adaptive Friction Compensation: Hardware Park Transform -> MLP 32-16-8-4 [0.7 KB, 0.06 ms, >1 kHz]
22. Kickback & Stall Detection: RMS Current Slope -> Gradient Boosting 200xd4 [12 KB, 0.12 ms, >1 kHz]
23. Load Estimation & Torque Ripple: FFT-256 -> Logistic Regression [0.7 KB, 0.62 ms, >1 kHz]
24. Multivariate Anomaly Scoring: Statistical Moments -> Mahalanobis IRQ [2 KB, 0.22 ms, >1 kHz]

CATEGORY 4: SLOWER-RATE & SEQUENCE (6 Trend Models)
25. Remaining-Useful-Life (RUL): 64-Step History -> MLP 128-64-32-8 [10.5 KB, 0.84 ms, 970 Hz]
26. Unsupervised Drift Detection: Statistical Moments -> MLP Autoencoder [5.5 KB, 0.58 ms, >1 kHz]
27. Short-Horizon Forecasting: Normalized Vector -> GRU 16 units [1.6 KB, 2.95 ms, 270 Hz]
28. Raw-Waveform Classification: Decimate -> 1D-CNN 8/16/32 [14 KB, 10.32 ms, 79 Hz]
29. Novelty Detection (Unlabelled): Statistical Moments -> Isolation Forest [8 KB, 0.20 ms, >1 kHz]
30. Per-Machine Baselining: Statistical Moments -> k-NN (200 Prototypes) [6.4 KB, 0.65 ms, >1 kHz]
```

## The 9 DSP Front-End Execution Times @ 50 MHz
- **256-pt FFT**: 0.61 ms (30,720 cycles)
- **512-pt FFT**: 1.38 ms (69,120 cycles)
- **Envelope Demodulation**: 0.10 ms (5,000 cycles, CORDIC)
- **Goertzel (8 bins)**: 0.12 ms (6,144 cycles)
- **Statistical Moments**: 0.14 ms (7,000 cycles)
- **Broadband RMS**: 0.06 ms (3,000 cycles)
- **Haar Wavelet**: 0.30 ms (15,000 cycles)
- **Park / Clarke**: <0.01 ms (120 cycles, Hardware CORDIC)
- **Decimation / Bandpass**: 0.08 ms (4,000 cycles)
