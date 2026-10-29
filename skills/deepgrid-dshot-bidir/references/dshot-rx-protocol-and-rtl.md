# DShot Receive (RX) & Bidirectional Telemetry Protocol Specification

## 1. Timing Budget & Speed Classes (at 50 MHz / 20 ns per cycle)
| Speed Class | Bit Period | T0H (0-bit high) | T1H (1-bit high) | @50 MHz Period / T0H / T1H (cycles) | Decision Margin (T1H - T0H) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DShot150** | 6.67 µs | 2.50 µs | 5.00 µs | 333 / 125 / 250 cycles | 125 cycles (±1,250 ns) |
| **DShot300** | 3.33 µs | 1.25 µs | 2.50 µs | 167 / 62 / 125 cycles | 63 cycles (±630 ns) |
| **DShot600** | 1.67 µs | 0.625 µs | 1.25 µs | 83 / 31 / 62 cycles | 31 cycles (±310 ns) |
| **DShot1200** | 0.83 µs | 0.312 µs | 0.625 µs | 42 / 16 / 31 cycles | 15 cycles (±150 ns) |

**Recommendation**: DShot600 is the supported maximum in production. DShot1200 is best-effort due to sampling jitter (±1 cycle) and flight controller (FC) clock drift consuming up to one-third of the margin.

---

## 2. DShot Frame Formats & Mathematical Checksums

### Command Frame (FC $\to$ ESC, 16 bits, MSB first):
- Bits `[15:5]`: Throttle (11 bits, 0 to 2047).
- Bit `[4]`: Telemetry request flag.
- Bits `[3:0]`: CRC4 checksum.

#### CRC4 Calculation:
- **Normal Mode**:
  $$\text{crc} = n_0 \oplus n_1 \oplus n_2$$
  where $n_0 = \text{frame}[15:12]$, $n_1 = \text{frame}[11:8]$, $n_2 = \text{frame}[7:4]$.
- **Bidirectional Mode**:
  $$\text{crc} = \sim(n_0 \oplus n_1 \oplus n_2) \ \& \ \text{0xF}$$
  In bidirectional mode, the physical line is inverted (idle high, active-low pulses), and the inverted CRC indicates bidirectional capability to the receiver.

---

## 3. Bidirectional Telemetry Reply (ESC $\to$ FC, 21 bits)

### Reply Frame Sequence:
1. **Raw Payload (16 bits)**:
   - Bits `[15:4]`: eRPM period representation consisting of a 3-bit exponent $e = \text{val}[11:9]$ and a 9-bit mantissa $m = \text{val}[8:0]$.
     $$\text{period}\_\mu\text{s} = m \ll e$$
   - Bits `[3:0]`: CRC4 over the 12-bit period field:
     $$\text{crc} = \sim(v \oplus (v \gg 4) \oplus (v \gg 8)) \ \& \ \text{0xF}$$
2. **GCR 4b$\to$5b Encoding (20 bits)**:
   Each 4-bit nibble is mapped via the standard GCR lookup table:
   | Input (Hex) | GCR (5b Hex) | GCR Binary | Input (Hex) | GCR (5b Hex) | GCR Binary |
   | :--- | :--- | :--- | :--- | :--- | :--- |
   | `0x0` | `0x19` | `11001` | `0x8` | `0x1A` | `11010` |
   | `0x1` | `0x1B` | `11011` | `0x9` | `0x09` | `01001` |
   | `0x2` | `0x12` | `10010` | `0xA` | `0x0A` | `01010` |
   | `0x3` | `0x13` | `10011` | `0xB` | `0x0B` | `01011` |
   | `0x4` | `0x1D` | `11101` | `0xC` | `0x1E` | `11110` |
   | `0x5` | `0x15` | `10101` | `0xD` | `0x0D` | `01101` |
   | `0x6` | `0x16` | `10110` | `0xE` | `0x0E` | `01110` |
   | `0x7` | `0x17` | `10111` | `0xF` | `0x0F` | `01111` |
3. **Transition Encoding (21 bits)**:
   $$\text{out}[0] = 0$$
   $$\text{out}[i] = \text{out}[i-1] \oplus G[i-1] \quad \text{for } i \in [1, 20]$$
   A logic '1' in the GCR stream creates a physical state transition on the wire.
4. **Transmission Timing**:
   - Transmitted inverted at $\frac{5}{4}$ the command bit rate (e.g., at DShot600, rate is $750\text{ kbit/s} = 1.33\ \mu\text{s/bit} = 66.7\text{ cycles at } 50\text{ MHz}$).
   - Commences `TURNAROUND` cycles (~30 µs = 1500 cycles at 50 MHz) after the command frame's trailing edge.
   - Decoded on FC side via XOR differentiator: $G = s \oplus (s \gg 1)$.

---

## 4. Slot 0xC Memory Map & Register Architecture

Located at peripheral base `0x...C00` (slot 0xC). Existing registers `0x00–0x20` for TX remain unchanged.

| Address Offset | Register Name | Bit Range | Access | Function & Hardware Field Descriptions |
| :--- | :--- | :--- | :--- | :--- |
| `0x24` | `RXCTRL` | `[0]`<br>`[1]`<br>`[2]`<br>`[3]`<br>`[4]`<br>`[5]` | RW<br>RW<br>RW<br>RW<br>RW<br>RW | `RX_EN`: Enable all 4 channel receivers<br>`INVERT`: Invert input pulse sense (bidirectional mode)<br>`TELEM_EN`: Arm reply engine on frames with `telem=1`<br>`TELEM_ALWAYS`: Reply on every valid frame (Betaflight standard)<br>`IRQ_FRAME_EN`: Interrupt on any channel `VALID`<br>`IRQ_ERR_EN`: Interrupt on CRC/Overrun/Abort error |
| `0x28` | `RXTHRESH` | `[11:0]` | RW | High-time cycle threshold distinguishing 1 from 0. Defaults to `(T0H + T1H) / 2` when 0. |
| `0x2C` | `RXTIMEOUT` | `[11:0]` | RW | Line idle threshold to terminate and reset partial frame counter. Defaults to `2 * BITPERIOD`. |
| `0x30` | `RXFRAME0` | `[10:0]`<br>`[11]`<br>`[12]`<br>`[13]`<br>`[14]`<br>`[15]` | RO<br>RO<br>RO/W1C<br>RO/W1C<br>RO/W1C<br>RO/W1C | Channel 0 Received `THROTTLE`<br>`TELEM` request bit<br>`VALID`: Frame decoded, CRC good (W1C clear)<br>`CRC_ERR`: Checksum mismatch<br>`OVERRUN`: New frame received before `VALID` was cleared<br>`TEL_ABORT`: Telemetry reply aborted due to early FC edge |
| `0x34` | `RXFRAME1` | `[15:0]` | — | Channel 1 received frame and status |
| `0x38` | `RXFRAME2` | `[15:0]` | — | Channel 2 received frame and status |
| `0x3C` | `RXFRAME3` | `[15:0]` | — | Channel 3 received frame and status |
| `0x40` | `TURNAROUND`| `[15:0]` | RW | Delay in clock cycles from command edge to reply output enable (~1500 cycles = 30 µs). |
| `0x44` | `TELEMPERIOD`| `[11:0]`| RW | Bit period in clock cycles for reply transmitter. Defaults to `BITPERIOD * 4 / 5` (67 cycles). |
| `0x48` | `TELEM0` | `[11:0]` | RW | Channel 0 eRPM period payload `{e[2:0], m[8:0]}`. Hardware handles GCR, CRC, and transition coding. |
| `0x4C` | `TELEM1` | `[11:0]` | RW | Channel 1 eRPM period payload |
| `0x50` | `TELEM2` | `[11:0]` | RW | Channel 2 eRPM period payload |
| `0x54` | `TELEM3` | `[11:0]` | RW | Channel 3 eRPM period payload |
| `0x58` | `RXSTATUS` | `[3:0]`<br>`[7:4]`<br>`[11:8]`<br>`[15:12]`<br>`[19:16]` | RO | Multi-channel snapshot: `VALID[3:0]`, `CRC_ERR[3:0]`, `OVERRUN[3:0]`, `TEL_BUSY[3:0]`, `PAD_DIR[3:0]` (1 = driving). |
| `0x5C` | `RXIRQ` | `[0]`<br>`[1]` | RO/W1C | `FRAME`: Frame pending interrupt<br>`ERR`: Error pending interrupt |

> [!IMPORTANT]
> **Write-1-to-Clear (W1C) Lockstep Invariance**: In DG32, the lockstep checker mirrors bus transactions to the `CHECKER` core with a 2-cycle skew. A read-to-clear register would trigger side-effects during a single bus read that could create execution divergences. All status and interrupt flags in `dgrid_dshot_rx` are strictly W1C.
