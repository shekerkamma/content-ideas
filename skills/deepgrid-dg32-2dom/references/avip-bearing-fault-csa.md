# AVIP Bearing-Fault Classifier & Motor Current Signature Analysis (CSA)

## 1. Application Overview & Model Architecture

The DG32-2DOM attention engine was created specifically to run edge AI diagnostics such as **AVIP** (Adaptive Vibration & Inference Processor, `dgrid-a8w8`), an INT8 multimodal bearing-fault classifier.

### Topology:
- **Multimodal Inputs**:
  - Time-domain branch: Small convolutional stack + gated recurrent unit (GRU) cell.
  - FFT-domain branch: Frequency features + gated recurrent cell.
- **Attention Fusion**:
  - Two Self-Attention blocks (`sa`, `sb`): $QKV$ projection + $\text{Softmax}(QK^T)V$ per head.
  - One Cross-Attention block (`cx`): Fuses time-domain and frequency-domain representations into a unified representation.
  - Per-class classification head.

### Model Sizing & Inference Latency on `clk_fast_i` (114 MHz):
| Model Variant | Parameters | Positions | Kicks | Conv Cycles | Inference Latency (@ 114 MHz) | Accuracy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CWRU Shipped Model** | 47,076 params | 143,377 | 228,229 | 3,794,371 | **46.7 ms** | 94–95% held-out-load accuracy (INT8 = FP32) |
| **Full AVIP Model** | 478,277 params | 169,821 | 231,657 | 4,429,355 | **54.5 ms** | Comprehensive multi-defect coverage |

**Compute Scaling**: While Full AVIP contains 10× more parameters, it requires only **1.2× more compute** (54.5 ms vs 46.7 ms) because capacity is added via deeper, narrower layers at reduced spatial resolutions. Running on `clk_fast_i` ensures that running a 50 ms inference consumes **zero execution cycles** from the 50 MHz flight-control CPU.

---

## 2. Current-Signature Front End (Zero-Accelerometer Diagnostics)

Standard bearing research assumes two external accelerometers (drive-end and fan-end). DG32-2DOM eliminates external vibration sensors entirely by utilizing Motor Current Signature Analysis (MCSA).

### The Physical Principle:
A physical bearing defect (inner race BPFI, outer race BPFO, or ball defect BSF) creates mechanical airgap eccentricities that modulate the motor's stator current:
$$f_{\text{fault\_sidebands}} = f_e \pm k \cdot f_{\text{defect}}$$
The current envelope carries the exact same mechanical fault signature as an external accelerometer.

### Front-End Pipeline (`fw/avip_csa`):
1. **Synchronous Sampling**: The on-die differential SAR ADC (`0xDB`) is triggered by `sample_trig` from the PWM unit at the current-ripple null ($cnt == 0$).
2. **Channel Derivation**: Derives two orthogonal diagnostic streams from a single phase-current ADC:
   - Channel 1: Raw fundamental carrier.
   - Channel 2: Amplitude-Modulated (AM) fault envelope.
3. **Dual Operational Outputs**:
   - **Classical Fault Indicator**: Computes BPFO/BPFI/BSF sideband energy into an 8-bit score ($0..255$). Footprint is ~9 KB; runs continuously inside the DG32-LITE base variant without an accelerator.
   - **Neural Recurrence Tensor**: Generates a $(35, 20, 20, 2)$ INT8 recurrence matrix streamed to the external memory arena for execution on the DG32-2DOM attention engine.
