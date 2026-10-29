# Chapter 3: The Model Catalogue (The Nineteen That Fit)

## Core Idea / Thesis
Inference costs on the DG32-LITE scalar core are strictly deterministic. Nineteen proven lightweight model architectures fit entirely within the 16.5 KB RAM budget and execute within acceptable loop latencies.

---

## The Master 19-Model Parametric Table

*Note: All figures represent inference cost only. Feature extraction (FFT, CORDIC envelope, Goertzel) is costed separately in Chapter 4. Memory footprint accounts for weights plus peak working state buffers.*

| # | Model Architecture | Primary Operational Role | Clock Cycles @ 50 MHz | Inference Latency | Memory (Weights + State) | Maximum Sampling Rate |
|---|---|---|---|---|---|---|
| **1** | **Random Forest (100×d8)** | Primary fault classifier | 3,200 | 0.06 ms | 20.0 KB | >1 kHz |
| **2** | **Gradient Boosting (200×d4)** | Primary multi-class classifier | 3,200 | 0.06 ms | 12.0 KB | >1 kHz |
| **3** | **Isolation Forest** | Unlabelled novelty / outlier detection | 3,200 | 0.06 ms | 8.0 KB | >1 kHz |
| **4** | **Linear Discriminant Analysis (LDA)** | Fast binary / multi-class classifier | 128 | <0.01 ms | 0.7 KB | >1 kHz |
| **5** | **Logistic Regression** | Primary boundary classifier | 128 | <0.01 ms | 0.7 KB | >1 kHz |
| **6** | **Naive Bayes** | Operating regime identification | 512 | 0.01 ms | 0.5 KB | >1 kHz |
| **7** | **PCA + Hotelling $T^2$** | Industrial condition-monitoring standard | 1,024 | 0.02 ms | 2.0 KB | >1 kHz |
| **8** | **Mahalanobis Distance** | Single scalar multivariate anomaly score | 4,096 | 0.08 ms | 2.0 KB | >1 kHz |
| **9** | **One-Class SVM** | Non-linear anomaly decision boundary | 12,800 | 0.26 ms | 6.9 KB | >1 kHz |
| **10** | **k-NN (200 Prototypes)** | Field-adaptable instance classifier | 25,600 | 0.51 ms | 6.4 KB | >1 kHz |
| **11** | **Nearest Centroid** | On-device baselining (no backprop pass) | 1,024 | 0.02 ms | 1.0 KB | >1 kHz |
| **12** | **Gaussian Mixture Model (GMM)** | Multi-modal regime identification | 2,048 | 0.04 ms | 2.0 KB | >1 kHz |
| **13** | **Hidden Markov Model (8-State)**| Discrete sequence & state tracking | 3,072 | 0.06 ms | 2.0 KB | >1 kHz |
| **14** | **Extended Kalman Filter (EKF)** | Non-linear observer (flux, thermal) | 2,400 | 0.05 ms | 2.0 KB | >1 kHz |
| **15** | **MLP (32-16-8-4)** | Compact non-linear classifier / regressor | 2,688 | 0.05 ms | 0.7 KB | >1 kHz |
| **16** | **MLP Autoencoder** | Unsupervised physical drift detection | 22,016 | 0.44 ms | 5.5 KB | >1 kHz |
| **17** | **MLP (128-64-32-8)** | High-capacity non-linear regression | 41,984 | 0.84 ms | 10.5 KB | 970 Hz |
| **18** | **GRU (16 Units)** | Short sequence temporal forecasting | 147,456 | 2.95 ms | 1.6 KB | 270 Hz |
| **19** | **1D-CNN (8/16/32)** | End-to-end raw-waveform classification | 512,000 | 10.24 ms | 14.0 KB | 80 Hz |

---

## Key Performance Insights
1. **The Sub-Millisecond Majority**: 16 of the 19 models execute in under **0.5 ms**, leaving ample headroom for control loop execution.
2. **Dense Network Ceiling**: An MLP scaled to 128-64-32-8 represents the practical ceiling for dense networks on DG32-LITE without dropping below 1 kHz loop frequencies (41,984 cycles, 0.84 ms).
3. **Sequential & Convolutional Bounds**:
   - The **16-unit GRU** takes 2.95 ms, bounding temporal sequence forecasting to a maximum update rate of **270 Hz**.
   - The **1D-CNN** takes 10.24 ms, bounding raw waveform inference to **80 Hz**.
