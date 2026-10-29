---
name: deepgrid-dshot-bidir
description: Hardware DShot receive (RX) and bidirectional telemetry reply architecture for DeepGrid Semi's DG32 motor-control silicon, covering slot 0xC RTL extensions, GCR 4b→5b transition encoding, pad-ring reuse, and 28 KB vs 32 KB SRAM floorplan trade-offs.
---

# DeepGrid Semi — DG32 DShot Receive & Bidirectional Telemetry (dgrid_dshot_rx)

This skill provides an authoritative, un-hallucinated engineering reference for the hardware DShot receiver (`dgrid_dshot_rx`) and bidirectional telemetry reply engine (`dgrid_dshot_tel`) on DeepGrid Semi's DG32 RISC-V motor-control SoC, based on the engineering review specification dated 13 September 2026 (Author: DG32 engineering; Reviewer: Ayaz Khan).

## Core Architecture Highlights
1. **Why Hardware Decoding is Mandatory**:
   - Firmware bit-banging requires disabling interrupts for ~1,340 cycles at DShot600 (or ~2,700 cycles at DShot300), which violently collides with the 5 µs FOC control loop (250 cycles total).
   - In a dual-core lockstep system (`dgrid_lockstep_check`), firmware polling on asynchronous pad inputs creates branch-timing jitter and divergent store streams that trigger false lockstep faults.
   - Bidirectional reply requires dynamic direction switching (~30 µs turnaround), which firmware cannot perform on fixed output pads.
2. **In-Place Slot 0xC Extension**:
   - Reuses existing AXI-lite address decoder at slot 0xC (`0x24–0x5C`).
   - Adds `dgrid_dshot_rx` and `dgrid_dshot_tel` without modifying frozen bus decoder logic.
   - Shared bit-rate timers (`BITPERIOD`, `T0H`, `T1H`).
3. **Bidirectional Telemetry Protocol**:
   - Inverted line convention (idle high, low pulses) and inverted CRC4 (`crc = ~(n0 ^ n1 ^ n2) & 0xF`).
   - eRPM payload: 3-bit exponent $e$, 9-bit mantissa $m$ ($\text{period}\_\mu\text{s} = m \ll e$) + inverted CRC4.
   - GCR 4b$\to$5b encoding followed by transition encoding (`out[i] = out[i-1] ^ G[i-1]`).
   - Reply transmitted inverted at 5/4 bit rate (750 kbit/s for DShot600, 1.33 µs/bit = 66.7 cycles at 50 MHz).
   - Turnaround timing: ~30 µs (1500 cycles at 50 MHz); auto-abort within 1 cycle on incoming FC edge (`TEL_ABORT`).
4. **Pad-Ring & Safety Constraints**:
   - Reuses 4 PWM high-side pads (`io[26, 28, 30, 32]`) switching from `PC_OUT` to `PC_BIDIR` (`gpio_dm = 110`, dynamic `oeb`).
   - Low-side PWM pads (`io[27, 29, 31]`) remain strictly `PC_OUT` to prevent bridge shoot-through.
   - External board pull-up required (no internal weak pull in `PC_BIDIR`).
5. **SRAM Floorplan Lever (28 KB vs 32 KB)**:
   - 16 $\to$ 14 macros allows 2DOM's 17 macros to arrange into 3 columns $\times$ 6 rows instead of 3 $\times$ 7.
   - Deletes an entire macro row, doubling the full-width logic strip from 1.75 mm² to 3.40 mm² to fit the 2,900 µm OpenFrame wrapper slot.
   - Lite die is unaffected and preserves 32 KB SRAM.
