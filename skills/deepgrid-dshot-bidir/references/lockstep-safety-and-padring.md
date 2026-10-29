# Lockstep Safety & OpenFrame Pad-Ring Mechanics

## 1. Why Firmware Bit-Banging Collides with DG32 Architecture

### A. The 5 µs FOC Loop Collision
- On DG32 running at 50 MHz, a 5 µs Field-Oriented Control (FOC) cycle is exactly 250 clock cycles.
- DShot600 requires 1,340 clock cycles per 16-bit frame; DShot300 requires ~2,700 cycles.
- Decoding DShot edges in firmware requires polling in a tight busy-wait loop with interrupts disabled. A single frame would stall the CPU for 5.3× to 10.8× the entire FOC control period, causing catastrophic loss of motor current regulation and acoustic/thermal failure.

### B. The 2-Cycle Lockstep Compare Window
- DG32 incorporates dual RV32IM cores in hardware lockstep (`dgrid_lockstep_check`).
- The `CHECKER` core executes identical instructions trailing the `MAIN` core by exactly 2 clock cycles.
- In firmware bit-banging, branching depends directly on reading asynchronous external pad levels. Asynchronous sampling causes timing jitter between the two cores on branch evaluation and bus store commits. The hardware lockstep comparator will interpret this branch-timing divergence as a silicon fault and trip `FAULTn` within 2 cycles, halting the motor.
- **Hardware RX Resolution**: `dgrid_dshot_rx` decodes pulses entirely in hardware and latches the completed, CRC-checked 16-bit word into memory-mapped registers. Reading a synchronous bus register presents identical data to both cores across the 2-cycle bus mirror without jitter.

---

## 2. Pad-Ring Configuration & OpenFrame Constraints

### Pad Budget Reality:
The DG32 QFN-64 package utilizes 44 dedicated functional I/O signals with exactly 0 spare pads. No dedicated pins exist for DShot reception. The RX path must reuse the existing 4 PWM high-side pads.

| Signal Name | OpenFrame Pad Index | Original Pad Class | New Pad Class | OpenFrame Control Ties | Function in PWM Role (`PINMUX[0]=0`) | Function in DShot Role (`PINMUX[0]=1`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `P_PWM_AH` | `io[26]` | `PC_OUT` | `PC_BIDIR` | `gpio_dm = 110`, `gpio_inp_dis = 0` | Phase A High-Side Output | DShot Ch 0 Bidirectional I/O |
| `P_PWM_AL` | `io[27]` | `PC_OUT` | `PC_OUT` (Untouched) | `gpio_dm = 110`, `gpio_inp_dis = 1` | Phase A Low-Side Output | Untouched (Never muxed) |
| `P_PWM_BH` | `io[28]` | `PC_OUT` | `PC_BIDIR` | `gpio_dm = 110`, `gpio_inp_dis = 0` | Phase B High-Side Output | DShot Ch 1 Bidirectional I/O |
| `P_PWM_BL` | `io[29]` | `PC_OUT` | `PC_OUT` (Untouched) | `gpio_dm = 110`, `gpio_inp_dis = 1` | Phase B Low-Side Output | Untouched (Never muxed) |
| `P_PWM_CH` | `io[30]` | `PC_OUT` | `PC_BIDIR` | `gpio_dm = 110`, `gpio_inp_dis = 0` | Phase C High-Side Output | DShot Ch 2 Bidirectional I/O |
| `P_PWM_CL` | `io[31]` | `PC_OUT` | `PC_OUT` (Untouched) | `gpio_dm = 110`, `gpio_inp_dis = 1` | Phase C Low-Side Output | Untouched (Never muxed) |
| `P_PWM_TRIG`| `io[32]` | `PC_OUT` | `PC_BIDIR` | `gpio_dm = 110`, `gpio_inp_dis = 0` | Sample Trigger Output | DShot Ch 3 Bidirectional I/O |

### Half-Bridge Shoot-Through Safety:
The low-side pads (`io[27, 29, 31]`) are never routed to the DShot peripheral or multiplexers. They remain strictly hardwired output drivers (`PC_OUT`). Even in the event of an invalid software configuration or corrupted register state, high-side and low-side power FETs cannot be simultaneously enabled, eliminating shoot-through risk.

### Board-Side Pull-Up Requirement:
In the OpenFrame I/O library, the `PC_BIDIR` class (`gpio_dm = 110`) does not include internal weak pull-up resistors (pull modes `010` and `011` are static input-only classes). Bidirectional DShot idles high. Therefore:
- The system mandates an external board-side pull-up resistor (typically 1kΩ–4.7kΩ to 3.3V) on the FC/ESC line.
- When `rst_n_i` is low, `pad_oe` is deasserted (pads float as inputs) so the resetting SoC never drives an active line.
