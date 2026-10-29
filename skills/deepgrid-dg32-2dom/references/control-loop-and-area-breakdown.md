# FOC Control-Loop Budget, Measured Fmax & Physical Area Breakdown

## 1. Field-Oriented Control (FOC) Cycle Cost & Headroom

All cycle counts are empirically measured in gate-level simulation and static timing on the sky130A A3 silicon.

### Measured Costs per FOC Current Loop Stage:
| Stage | Hardware Mechanism | Measured Cycle Cost (at 50 MHz / 20 ns) | Note |
| :--- | :--- | :--- | :--- |
| **Phase Current Sample** | On-die 8-bit differential SAR ADC | **177 cycles** (~3.54 µs) | PWM-triggered at ripple null; replaces ~1.9 µs external SPI transfer. |
| **Clarke / Park Transform**| Hardware CORDIC engine | **53–58 cycles** per op | Fixed-latency pipeline; rotation mode. |
| **PI Regulators ($d, q$)** | VexiiRiscv CPU (plain C) | **~8 cycles / instruction** | Fetch-bound core from SRAM; plain-C int8 MAC costs 54 cycles (vs 6 with I-cache). |
| **Inverse Park Transform**| Hardware CORDIC engine | **53–58 cycles** per op | Sized for FOC angle resolution. |
| **SVPWM Update** | PWM shadow registers | Applied at next center count | Zero software wait-states; $\text{Period} = 2 \times (\text{PERIOD} + 1)$. |
| **Fault Verification** | Lockstep comparator | **Continuous (0 wait)** | Latches fault cause in $\le 39$ cycles from fault injection. |

### Headroom Budget across Loop Rates:
- **Total Fixed Hardware Overhead**: $\approx \mathbf{300\text{ cycles}}$ (~6 µs) per control period.
| Loop Frequency | Total Cycles @ 50 MHz | Fixed Hardware Cycles | Free CPU Budget | Workload Capacity |
| :--- | :--- | :--- | :--- | :--- |
| **10 kHz** | 5,000 cycles | ~300 cycles | **~4,700 cycles (>90%)** | Full FOC current + speed loop + Luenberger / EKF observer. |
| **20 kHz** | 2,500 cycles | ~300 cycles | **~2,200 cycles (88%)** | FOC with field-weakening and state observers. |
| **50 kHz** | 1,000 cycles | ~300 cycles | **~700 cycles (70%)** | High-speed inner current loop only. |

The total sensor-to-PWM closed loop measures **~5 µs acquisition plus ~5 µs compute**, achieving a **100 kHz closed-loop control bandwidth**.

---

## 2. Measured Block Fmax (Post-Route on sky130A)

The dual-core lockstep processor is the limiting path; peripheral blocks harden far beyond core requirements:
- **Lockstep Core (VexiiRiscv)**: **55–62 MHz measured** (sets the 50 MHz target; sign-off over-constrained to 54 MHz to recover top-assembly WNS).
- **Supervisor / wWDT**: **91.1 MHz**.
- **CORDIC Engine**: **95.5 MHz**.
- **Lockstep Checker Comparator**: **123.6 MHz**.
- **QSPI Controller / 3-Phase PWM**: **171.6 MHz / 167.8 MHz**.
- **DShot ESC Engine / GPIO**: **172.9 MHz / 173.6 MHz** (>3× the 50 MHz target!).

---

## 3. Physical Silicon Area Breakdown (3400 × 4500 µm Die)

- **Total Die Area**: $3.400 \times 4.500\text{ mm} = \mathbf{15.30\text{ mm}^2}$.
- **Placed Cell + Macro Footprint**: $5.93\text{ mm}^2$.
- **Power Distribution (PDN), Halos, and Channels**: $9.37\text{ mm}^2$.

### Standard-Cell Logic Subtotal: $0.751\text{ mm}^2$
- Lockstep CPU Cores (2× VexiiRiscv): $0.3297\text{ mm}^2$ ($0.1648\text{ mm}^2$ each).
- CDC Burst Bridges (Read + Write): $0.1580\text{ mm}^2$.
- INT8 Attention Engine Logic: $0.0694\text{ mm}^2$.
- Lockstep Comparator: $0.0397\text{ mm}^2$.
- CORDIC Trigonometric Accelerator: $0.0208\text{ mm}^2$.
- SRAM Controller Logic: $0.0156\text{ mm}^2$.
- Peripherals (PWM, DMA, DShot, SPI, Encoder, I2C, UART, Timers, Supervisor, ADC Wrapper): $0.1178\text{ mm}^2$.

### Hard Macro Footprint: $5.177\text{ mm}^2$ (86% of Placed Area!)
- **16× Main 2 KB SRAM Macros** (`sky130_sram_2kbyte_1rw1r_32x512_8`): **$4.5527\text{ mm}^2$** ($0.2845\text{ mm}^2$ each).
- **Attention K Buffer Macro**: $0.2845\text{ mm}^2$.
- **Attention V Buffer Macro**: $0.2845\text{ mm}^2$.
- **SAR ADC Hard Macro**: $0.0540\text{ mm}^2$.
- **Baked Boot ROM**: $0.0010\text{ mm}^2$ (sparse std-cells).

> [!IMPORTANT]
> **Silicon Macro Reality**: SRAM macros dominate the silicon area (86%). Standard-cell logic, including both 32-bit RISC-V cores, occupies only 0.75 mm². Sizing main SRAM (e.g. dropping 2 macros to save 0.57 mm²) is the primary physical floorplan lever.
