# Chapter 10: Basis, Methodology, and Accuracy Boundaries

## Core Idea / Thesis
All latency and execution numbers in this specification are mathematically derived from verified physical constants. DeepGrid enforces strict intellectual honesty: theoretical benchmark claims must not be quoted as production specifications, and safety integrity remains governed by deterministic hardware.

---

## 1. Mathematical Derivations & Constants

- **Hardware Origin**: Core configuration, memory sizing, peripheral sets, and CORDIC math blocks are verified against the **DG32-LITE Tape-in Block Diagrams (10 Sept 2026)** and the **Capability Assessment (11 Sept 2026)**.
- **Latency Derivation**:
  $$\text{Latency} = \frac{\text{Feature Extraction Cycles} + \text{Model Cycles (at 4 cycles/int8 MAC)}}{0.82 \times 50\text{ MHz}}$$
  *Note: This constant is back-solved from design specs and will be cycle-measured on physical silicon during first-silicon bring-up.*
- **Third-Party Verification**: Primary reference studies, 12-feature rankings, kurtosis non-monotonicity curves, and signal limits were cross-checked against **IEEE, MDPI, the PHM Society**, and official **ISO catalog standards (ISO 13373-1, 13373-2, 20958, 20816-3)**.

---

## 2. On Accuracy Expectations: The CWRU Benchmark Trap

> [!CAUTION]
> **Do not carry published 99% academic bearing benchmark accuracies into production industrial specifications.**

- **The Data Leakage Reality**: An audit of 41 published studies evaluating the standard Case Western Reserve University (CWRU) bearing dataset revealed that **40 of the 41 studies used train/test splits contaminated by data leakage** (e.g., slicing adjacent time windows from the same continuous physical run).
- **Leakage-Free Validation**: When evaluated under a rigorous, leakage-free bearing-wise split, **classifier accuracy immediately dropped from 85.8% down to 69.5%**.
- **The Physical Physics Limit**: Extensive research by Smith and Randall proved that a meaningful fraction of records in the CWRU dataset are **not physically diagnosable by bearing kinematics at all** due to load-induced slip and non-stationary rotational speeds.
- **Realistic Production Expectation**: Expected accuracy on unseen physical industrial bearings is **65% to 80%**, not 99%.

---

## 3. What is NOT Claimed (Socratic Boundaries)

1. **Pre-Silicon Status**: No workload in this document has been compiled onto or measured on fabricated DG32-LITE silicon (the chip rides the September 2026 shuttle).
2. **No Safety Integrity Overwrite**: **No inference result carries an ISO 26262 ASIL or IEC 61508 safety claim.** The machine learning classifier operates in an **advisory role only**. The dual-core hardware lockstep comparator and deterministic trip logic hold absolute authority over the power bridge and fault pins.
3. **Algorithm Suitability, Not Pre-Trained Weights**: The documented model configurations represent mathematically appropriate architectures for scalar execution, not static pre-trained universal weight sets.
