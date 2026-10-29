# DG32-2DOM AXI Fabric, Memory Map & Decoded Slaves

## 1. Top-Level Interconnect & Design Premises

The DG32-2DOM interconnect is a decoded AXI fabric centered on an LSU master with a private Boot ROM fetch path:
- **Fetch Port**: Private slave to the 64 KB baked std-cell Boot ROM. Instruction fetch never arbitrates with data access, eliminating fetch/LSU contention bug classes.
- **LSU Master**: Sole shared-bus master on the 21-slave decoded AXI fabric.
- **CPU PMA Whitelist**: Hardwired whitelist in the VexiiRiscv core:
  $$\text{fault} = \neg(\text{addr}[31] \ | \ \text{addr}[31:28] == \text{0x1})$$
  Any transaction that does not set bit 31 or reside in `0x1xxxxxxx` generates an internal CPU PMA load fault before reaching the bus.
  - SRAM placed at `0x9000_0000` (bit 31 set).
  - External Flash XIP window at `0x1000_0000`.
  - Peripherals at `0xC000_0000`, `0xD000_0000` to `0xDF00_0000`, and `0xE000_0000`.
- **Address Decode & Handshake Hold**: `ar_addr` is valid only for 1 cycle at handshake; the decoded target is latched into `arsel_q` / `arsel_v` across the read response to prevent misrouting.
- **Error Slave**: Any access to an unmapped address completes cleanly with `SLVERR`. Because OpenFrame has no debugger and CPU halts are fatal, bus hangs are prevented structurally.

---

## 2. Comprehensive 21-Slave Base Address Map

Decoded via `addr[31:28]`, with the `0xD` page sub-decoded via `addr[27:24]`.

| Base Address | Block Name | Domain | Function & Architectural Role |
| :--- | :--- | :--- | :--- |
| `0x1000_0000` | `QSPI-XIP` | `clk_i` (50 MHz) | Data read window on external NOR flash (loads only; not instruction fetch). |
| `0x9000_0000` | `SRAM` | `clk_i` (50 MHz) | 32 KB main data memory (16 sky130 1rw1r macros, 512×32 each); idle second port free for DMA. |
| `0xC000_0000` | `dgrid_dshot` | `clk_i` (50 MHz) | 4-channel DShot ESC engine, pin-muxed onto high-side PWM pads. |
| `0xD000_0000` | `UART0` | `clk_i` (50 MHz) | 8N1 serial console; carries boot banner (115,200 baud @ 50 MHz = 434 clocks/bit). |
| `0xD100_0000` | `UART1` | `clk_i` (50 MHz) | 8N1 telemetry streaming to companion processor. |
| `0xD200_0000` | `SPI Master` | `clk_i` (50 MHz) | CPOL/CPHA programmable master SPI up to 25 MHz; 0.64 µs per 16-bit word. |
| `0xD300_0000` | `GPIO` | `clk_i` (50 MHz) | 14-16 general I/O pins with 2-FF input synchronizers and atomic `SET` / `CLR` registers. |
| `0xD400_0000` | `TIMER0` | `clk_i` (50 MHz) | General down-counter timer; dedicated to RTOS system tick. |
| `0xD500_0000` | `TIMER1` | `clk_i` (50 MHz) | General down-counter timer; dedicated to control-loop period or one-shot timing. |
| `0xD600_0000` | `Fault CSR` | `clk_i` (50 MHz) | Latches first lockstep mismatch cause stickily; MAGIC-locked (`0xDEAD_5AFE`) test injection. |
| `0xD700_0000` | `Supervisor / wWDT` | `clk_i` (50 MHz) | Windowed watchdog (`WDTMIN` to `WDTMAX`) and rail guard; arms only via software `A_CTRL`. |
| `0xD800_0000` | `PWM` | `clk_i` (50 MHz) | 3-phase center-aligned complementary PWM; dead-time (up to 5.1 µs); async brake ($\le$2 cycles). |
| `0xD900_0000` | `I2C Master` | `clk_i` (50 MHz) | 7-bit master at 100/400 kHz with clock stretching and true open-drain pad drive. |
| `0xDA00_0000` | `Encoder` | `clk_i` (50 MHz) | Decodes A/B/Z quadrature and 3 Hall lines; 32-bit free-running timestamp on edges for velocity. |
| `0xDB00_0000` | `SAR ADC` | `clk_i` (50 MHz) | 8-bit differential OpenFASOC macro (~200 kSa/s); triggered at PWM current-ripple null. |
| `0xDC00_0000` | `DMA` | `clk_i` (50 MHz) | Single-beat AXI block mover; ~7.1 cycles/word using the SRAM idle read port. |
| `0xDD00_0000` | `SYSCTL` | `clk_i` (50 MHz) | Device identification and peripheral clock-gating registers. |
| `0xDE00_0000` | `CORDIC` | `clk_i` (50 MHz) | Q1.31 rotation and vectoring (sin, cos, atan2, magnitude) in fixed 53–58 cycles. |
| `0xDF00_0000` | `IRQ Aggregator` | `clk_i` (50 MHz) | 16-source masked interrupt controller (TMR0/1, PWM, ADC, DMA, I2C, Fault, SW, Attention). |
| `0xE000_0000` | `dgrid_int8_attn` | `clk_fast_i` (114 MHz) | Hardware INT8 attention engine; crosses via CDC bridges (returns `SLVERR` if disabled). |

---

## 3. Peripheral Register Map Offsets & Bitfields

### Fault CSR (`0xD600_0000`)
- `0x0 STATUS` (RO): `[0]` Poison flag; `[3:1]` Cause code (`001` = `DATA_MISMATCH`). Sticky-first latch.
- `0x4 INJECT` (WO): Write `0xDEAD_5AFE` to corrupt lockstep pulses for 32 cycles. Reads return 0.
- `0x8 EVENTS` (RO): Counter of matched lockstep-compare retirement events.
- `0xC ID` (RO): `0xD632_0001`.

### Supervisor & Windowed Watchdog (`0xD700_0000`)
- `0x04 CTRL` (RW): `[0]` `global_en`; `[1]` `wdt_en`; `[7:4]` `rail_en[3:0]`.
- `0x08 DEGLITCH` (RW): Filter clock cycles (default 8).
- `0x10 WDTMIN` (RW): Minimum watchdog kick window (default 100 cycles). Kick too early faults.
- `0x14 WDTMAX` (RW): Maximum watchdog kick window (default 50,000 cycles). Kick too late faults.
- `0x18 KICK` (WO): Write `0xA5A5` to service watchdog.

### 3-Phase Complementary PWM (`0xD800_0000`)
- `0x04 PERIOD` (RW): Up/down counter top: $\text{Period} = 2 \times (\text{PERIOD} + 1)$ clock cycles.
- `0x08 DEADTIME` (RW): 8-bit dead-time insertion for all 3 half-bridge phases (max 255 cycles = 5.1 µs).
- `0x0C/10/14 DUTY_A/B/C` (RW): Shadow-loaded phase duty cycles applied at center count (`cnt == 0`).
- `0x18 STATUS` (RO): `[0]` `BRAKED` sticky status.
- `0x1C BRAKE_CLR` (WO): Write 1 to clear brake once external `brake_i` pin is low.

### CORDIC Trigonometric Accelerator (`0xDE00_0000`)
- `0x00 CTRL` (RW): `[0]` `START`; `[1]` `MODE` (`0` = rotation/trig, `1` = vectoring/polar).
- `0x04/08/0C XIN/YIN/ZIN` (RW): Q1.31 fixed-point inputs.
- `0x10 XOUT` (RO): Q1.31 $\cos$ (rotation) or magnitude/$K$ (vectoring). $K = \text{0x4DBA76D4}$.
- `0x14 YOUT` (RO): Q1.31 $\sin$ (rotation).
- `0x18 ZOUT` (RO): Q1.31 angle $\text{atan2}/\pi$.
