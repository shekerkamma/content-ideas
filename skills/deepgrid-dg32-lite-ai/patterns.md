# Architectural & Engineering Patterns (DG32-LITE AI)

## Pattern 1: Signal Conditioning Before Model Capacity
- **Problem**: Attempting to deploy large neural networks (CNNs, Transformers) on a 50 MHz microcontroller to classify noisy mechanical sensor data.
- **Solution**: Spend execution cycles on band selection, envelope demodulation, and operating-condition normalisation instead of parameter depth. A 100-tree random forest evaluated on five well-conditioned features reaches 95.6% accuracy at 50–500× lower cycle cost than a deep network.
- **Rules**: Decimate before buffering; extract features evaluated at known physical kinematic frequencies.

## Pattern 2: CORDIC-Accelerated Envelope Demodulation
- **Problem**: Bearing defect shock pulses are high-frequency and low-amplitude, easily obscured by motor harmonics and structural vibration.
- **Solution**: High-frequency bandpass filter -> CORDIC polar magnitude (20 iterations, 5,000 cycles) -> lowpass filter -> decimate to 1–2 kS/s -> 256-point FFT or Goertzel tone extraction.
- **Gain**: Demodulated features score 4–5× higher in Fisher criterion and random forest importance than raw statistical moments.

## Pattern 3: Goertzel Algorithm vs. Large-Scale FFT
- **Problem**: Detecting small sideband splits (0.5 to 3 Hz) around the 50 Hz fundamental requires 30–100 second records. A direct FFT requires $2^{20}$ points (8 MB of RAM), completely impossible on microcontrollers.
- **Solution**: Compute discrete Goertzel recurrence filters strictly at the exact predicted sideband frequencies: $f = f_1(1 \pm 2ks)$.
- **Gain**: Replaces an 8 MB FFT with 0.7 KB of state and executes in 0.13 ms (6,144 cycles).

## Pattern 4: Dual-Metric Kurtosis & RMS Monitoring
- **Problem**: Relying solely on kurtosis or solely on RMS velocity for bearing health alarms.
- **Trap**: Kurtosis is non-monotonic—it spikes for early spalls, then drops back to Gaussian baselines as defect spalling spreads. RMS is monotonic but blind to early micro-pitting.
- **Solution**: Trend both simultaneously. Use kurtosis for early detection warnings and RMS velocity for ISO 20816 absolute shutdown thresholds. Never alarm on kurtosis alone.

## Pattern 5: Advisory ML Under Deterministic Lockstep
- **Problem**: Safety-critical drive systems cannot tolerate uncertified, non-deterministic AI inference in the primary actuator shutdown path.
- **Solution**: All machine learning and diagnostic models run in an advisory monitoring role. The hardware lockstep comparator (evaluating 2-cycle delayed redundant execution) retains exclusive, hardwired control over the `FAULTn` trip pin and power bridge disable.
