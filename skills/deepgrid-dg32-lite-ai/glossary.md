# Glossary: DG32-LITE AI & Predictive Diagnostics

| Term | Definition & Engineering Context |
|---|---|
| **12.5 MMAC/s** | Mega Multiply-Accumulates per second. Scalar throughput achieved by the 50 MHz RV32IM core executing 4-cycle int8 MAC instructions. |
| **16.5 KB Budget** | Standard SRAM footprint allocated for ML model weights and peak activation buffers on DG32-LITE (expands to 29.5 KB with mask ROM runtime). |
| **82% Free Cycles** | Remaining execution headroom available on the 50 MHz core when running a 10 kHz Field-Oriented Control (FOC) current loop. |
| **AFE** | Analog Front End. The analog amplification, filtering, and ADC conversion stages ahead of digital processing. |
| **BPFI / BPFO** | Ball Pass Frequency Inner race / Ball Pass Frequency Outer race. Characteristic kinematic impact frequencies of rolling element bearings. |
| **CORDIC** | COordinate Rotation DIgital Computer. Hardware trigonometric engine computing sine, cosine, arctangent, and vector magnitude in under 20 cycles. |
| **CWRU Benchmark** | Case Western Reserve University bearing vibration dataset. Standard academic benchmark known for widespread data leakage across splits. |
| **Envelope Demodulation** | Signal processing technique that rectifies and low-pass filters high-frequency resonance signals to extract low-frequency defect repetition rates. |
| **Goertzel Algorithm** | Efficient IIR filter structure that computes the discrete Fourier transform for a single chosen frequency bin with $O(N)$ complexity and tiny RAM usage. |
| **Hotelling $T^2$** | Statistical metric measuring the distance of a multi-dimensional sample from the multivariate mean in Principal Component Analysis (PCA) space. |
| **ISO 13373** | International standard governing condition monitoring and diagnostics of machine systems (Part 1: General procedures, Part 2: Data processing). |
| **ISO 20816** | International standard specifying broadband vibration measurement and evaluation zones (Zone A: Good, Zone B: Acceptable, Zone C: Alert, Zone D: Trip). |
| **ISO 20958** | International standard defining condition monitoring of three-phase electrical machines via Motor Current Signature Analysis (MCSA). |
| **Kurtosis** | Fourth statistical moment measuring impulsiveness. Peaks during early localized spalling, then drops back to Gaussian values (~3.0) as wear generalizes. |
| **Mahalanobis Distance** | Scale-invariant metric that evaluates multivariate anomaly distance by accounting for correlations between distinct sensor channels. |
| **MCSA** | Motor Current Signature Analysis. Diagnostic technique detecting mechanical and electrical defects via phase current modulation sidebands. |
| **Slip ($s$)** | Normalized difference between synchronous magnetic field speed and mechanical rotor speed: $s = (n_s - n)/n_s$. Governs broken rotor bar sidebands ($2sf_1$). |
