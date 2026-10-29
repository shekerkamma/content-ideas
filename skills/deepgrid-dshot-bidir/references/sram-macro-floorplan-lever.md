# SRAM Architecture: 28 KB vs 32 KB Floorplan Lever Analysis

## 1. The Core Dispute: Firmware Footprint vs Physical Floorplan

### Ayaz's Firmware Perspective:
> *"28 KB bare minimum, 32 KB with safety margin; the reusable buffer saves only 2 KB."*
- From a software engineering standpoint, memory sizing is driven by call stack headroom, RTOS task structures, FOC observer state buffers, and communication queues.
- Sizing firmware to 28 KB leaves minimal margin for field upgrades or diagnostic logging.

### The Physical Floorplan Reality (OpenFrame 2,900 µm Slot):
- The 28 KB proposal was conceived not as a firmware restriction, but as a **geometric floorplan lever** to make the DG32 dual-domain variant (2DOM) routable.
- **SRAM Macro Array Geometry**:
  - In the 32 KB configuration with 16 macros (plus 1 parity/auxiliary macro = 17 macros), macros must be arranged in **3 columns × 7 rows**.
  - A $3 \times 7$ grid occupies excessive vertical die height within the 2,900 µm wrapper boundary. It compresses the central full-width logic strip to just **1.75 mm²**, creating severe routing congestion and timing closure failure.
  - Reducing to 28 KB (14 macros + 1 parity macro) allows arranging the array into **3 columns × 6 rows**.
  - Deleting that single macro row increases the full-width logic placement area from **1.75 mm² to 3.40 mm²** (nearly double), providing the silicon real estate required for place-and-route to close at 50 MHz.

---

## 2. Empirical Resolution Plan
DeepGrid resolves architectural debates through automated EDA runs on the codex branch:
- **Test Run `2dom/13`**: Evaluates a keep-32 KB spread-floorplan configuration with custom macro placement. If `2dom/13` successfully routes and achieves static timing closure, the design retains the full 32 KB SRAM.
- **Test Run `2dom/12`**: Evaluates a reduced 24 KB / 28 KB configuration. If only reduced-macro runs close, the 28 KB floorplan is adopted, and firmware utilizes the 2 KB reusable buffer optimization.
- **Lite Die Invariance**: The DG32-LITE base die does not include the second domain and is unaffected by this congestion constraint; it remains fixed at **32 KB SRAM**.
