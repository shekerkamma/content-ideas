# INT8 Attention Engine & Clock-Domain Crossing Architecture

## 1. Engine Mathematical Pipeline (`dgrid_int8_attn`)

The hardware attention engine computes multi-head attention across a band of query rows end-to-end:
$$\text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

### Why INT8 Was Selected Over INT4:
- In early INT4 test runs with ~400 near-uniform keys ($N_K \approx 400$), a uniform attention weight is $\frac{1}{400} = 0.0025$.
- In INT4 quantization, this value rounds identically to **zero**, causing the entire attention output matrix to collapse to zero.
- **Structural Solution**: The INT8 engine maintains attention weights as **unsigned 15-bit integers (`u15`)** across the entire pipeline into a 40-bit accumulator numerator. Only the final output $O$ is saturated back to signed INT8, preventing mathematical collapse.

### Why a 40-Bit Signed Numerator Seat:
- With standard 32-bit signed integers (`int32`), the numerator overflow threshold is $2^{31} - 1$. At $N_K = 512$, maximum accumulated sum of products exceeds $2^{31}$, corrupting calculations.
- A 40-bit signed accumulator provides bit-exact precision up to **$N_K = 131,072$ keys**, ensuring absolute mathematical fidelity against the golden floating-point model for any programmable matrix shape.

### Pipeline Stages:
1. **$QK^T$ Matrix Multiplication**:
   - `LANES × (s16 × s9)` MAC array implemented in standard LUTs (`USE_DSP=no`).
   - Shared between $QK^T$ (reduced across head dimension $d$) and $E \cdot V$ (accumulated per-lane).
2. **Row Maximum & Exponential Table**:
   - Tracks running row maximum.
   - 256-entry `u15` lookup table (`EXP[0] = 32767`). Softmax weights are never quantized to lower precision.
3. **Normalization ($Z$) & Reciprocal**:
   - Accumulates $Z = \sum \text{EXP}$.
   - Evaluates $\frac{1}{Z}$ using a dedicated **48-step restoring hardware divider**.
4. **$E \cdot V$ Projection & Saturation**:
   - Multiplies normalized exponential weights by value matrix $V$.
   - Saturates 40-bit results into signed 8-bit output $O$.

---

## 2. On-Chip SRAM Residency & Analytic Cycle Cost

### Buffer Management:
- **K Buffer ($N_K \times K_D$)**: Dedicated sky130 SRAM macro (`dgrid_attn_buf`). Port 0 write, Port 1 read.
- **V Buffer ($N_K \times D_V$)**: Dedicated sky130 SRAM macro.
- **Residency Idiom**: Keys and Values are loaded once per attention kick via AXI burst DMA, then re-read locally per query row. Streaming $V$ per row over the main bus would generate **400× higher bus traffic**, completely starving the CPU of memory bandwidth. On-chip residency restricts bus occupancy to just ~1%.

### Analytic Execution Cost:
$$\text{Cycles per query row} = \frac{N_K \cdot K_D}{\text{LANES}} + \frac{N_K \cdot D_V}{\text{LANES}} + 48\text{ (divide)} + 11 \cdot D_V\text{ (requant)} + \text{writeback} + \text{drain}$$
At $\text{LANES}=16$, $K_D=32$, $D_V=64$, $N_K=400$:
$$\text{Cycles per row} \approx 3,242\text{ clock cycles on }\texttt{clk\_fast\_i}\text{ (114 MHz)}$$

---

## 3. Clock-Domain Crossing (CDC) Bridges (`dgrid_axi_cdc_*`)

The attention engine operates on `clk_fast_i` (114 MHz), while the CPU and safety core run on `clk_i` (50 MHz).

### 4-Phase Req/Ack Handshake (Level Synchronizers):
- Transaction rate across the boundary is intentionally decoupled (weights loaded once, outputs written back once per kick).
- A 4-phase level handshake with 2-FF synchronizers provides provable metastability immunity without the complexity and area of Gray-coded asynchronous FIFOs.
- Payloads are held perfectly stable across the handshake.
- Burst bridges (`dgrid_axi_cdc_burst_rd` and `dgrid_axi_cdc_burst_wr`) batch entire AXI bursts into a single crossing event, amortizing synchronization latency to near-zero.
- **Timing Isolation Invariant**: The frozen 50 MHz flight-control core is completely untouched; the 114 MHz domain cannot pull down CPU timing closure or introduce wait-state jitter into the 5 µs FOC control loop.
