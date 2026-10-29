---
name: deepgrid-architecture
description: "Compounded architecture compiler bridging DeepGrid Semi mature-node silicon intelligence with multi-modal architecture generation. Compiles any DeepGrid SKU, subsystem, or whitepaper chapter into a 5-artifact deliverable suite: Draw.io component diagram (.drawio), technical specification (.md), executive PPTX (.pptx), instant browser-rendered 16:9 presentation deck (-deck.html), and interactive telemetry & fault injection cockpit (-workflow.html)."
---

<!-- argument-hint: [sku name, subsystem, or whitepaper chapter] -->

# DeepGrid Architecture Compiler (Silicon Intelligence → Multi-Modal Suite)

An automated orchestrator that extracts domain-grounded semiconductor parameters from `deepgrid-sku-compendium` and `deepgrid-mature-silicon`, then compiles them through the `architecture-to-everything` multi-modal pipeline into **5 synchronized deliverables**.

---

## How to Use This Skill

- **With SKU name**: 
  - `/deepgrid-architecture "SKU-1 BLDC Motor"`
  - `/deepgrid-architecture "SKU-3 Hi-Rel PMIC"`
  - `/deepgrid-architecture "SKU-4 Lockstep MCU"`
  - `/deepgrid-architecture "SKU-7 77GHz Radar"`
  - `/deepgrid-architecture "SKU-9 Zonal Gateway"`
  - `/deepgrid-architecture "D100 Drone SoC"`
  - `/deepgrid-architecture "DG SDV Platform"`
- **With Chapter or System Topic**:
  - `/deepgrid-architecture "198-Day Silicon Shuttle Loop"` (ch02 / ch05)
  - `/deepgrid-architecture "Three-Factory Sovereignty Roadmap"` (ch07)
  - `/deepgrid-architecture "DGridRiscV Core Architecture"` (ch08)
  - `/deepgrid-architecture "Organic SiP Multi-Die Packaging"` (ch06 / ch13)

---

## The 5-Deliverable Output Contract

Every invocation of `/deepgrid-architecture` must deterministically produce the following files in the project root:

| # | Format | File Pattern | Mandated Architectural Requirements |
|---|---|---|---|
| **1** | **Draw.io Diagram** | `<slug>-architecture.drawio` | • Component-flow structure (strictly **NO swimlanes**).<br>• Labeled functional zones with dashed boundaries.<br>• Numbered directional bus arrows (`[1]`, `[2]`).<br>• Explicit power rails (5V–120V BCD) and clock domains. |
| **2** | **Technical Spec** | `<slug>-architecture.md` | • Exhaustive engineering specification doc.<br>• Exact physical process parameters (130nm, 180nm BCD, 28nm flip-chip).<br>• Sovereign regulatory moats (DAP-2020 Buy Indian-IDDM, Make-II).<br>• Standards mapping: MIL-STD-810H, MIL-STD-461G, ISO 26262 ASIL-D, AEC-Q100. |
| **3** | **Executive Deck** | `<slug>-architecture.pptx` | • 10-slide executive presentation generated via `python-pptx`.<br>• Widescreen 16:9 layout (`Inches(13.333) x Inches(7.5)`).<br>• McKinsey/Accenture assertive claim titles.<br>• Aerospace consulting palette: Navy (`#0A192F`), Cyan (`#06B6D4`), Slate (`#F8FAFC`). |
| **4** | **Browser Deck** | `<slug>-deck.html` | • **Mandatory Companion**: Eliminates system PATH/PowerPoint viewer friction.<br>• Pure-vector responsive HTML slide renderer.<br>• Keyboard navigation (<kbd>→</kbd>/<kbd>Space</kbd> next, <kbd>←</kbd> prev).<br>• Slide counter, fullscreen toggle, dark/light cards. |
| **5** | **Interactive Cockpit** | `<slug>-workflow.html` | • Self-contained, zero-dependency interactive HTML5 visualizer.<br>• Clickable silicon blocks updating real-time telemetry drawer.<br>• Live mode/simulation pills (Nominal vs Jammed/Fault vs Safe-State).<br>• Integrated fault injector (e.g., bit-flip, link loss, or fuse trip). |

---

## Execution Pipeline

### Step 1: Ingestion & Parameter Locking
1. Inspect chapter sources using cross-platform path resolution (relative POSIX paths):
   - Check `.agent/skills/deepgrid-sku-compendium/chapters/` (or `.agents/skills/...`).
   - Check `.agent/skills/deepgrid-mature-silicon/chapters/` (or `.agents/skills/...`).
2. Extract the exact pinouts, bus widths, operating voltages, foundries (SkyWater, IHP, SCL Mohali), and failure modes.
3. Lock these parameters into memory. **Never hallucinate silicon specs.**

### Step 2: Generate Stage 1 Diagram (`.drawio`)
- Construct an XML component-flow model with clear zones:
  - *Zone A: External Environment & Sensors*
  - *Zone B: Multi-Die Organic Packaging & Substrate Traces*
  - *Zone C: Real-Time Safety / Control Cores (Lockstep / Cacheless)*
  - *Zone D: High-Speed Compute & Crossbar Matrix*
  - *Zone E: Zonal Actuation & Power Distribution Tree*

### Step 3: Write Stage 2 Technical Spec (`.md`)
- Author the formal architectural specification covering:
  - The sovereign military/industrial problem ($9B mature node import funnel).
  - Physical & electrical characteristics table.
  - Subsystem block specifications with register-level detail.
  - Failure modes & Socratic falsification criteria.
  - Multi-die packaging details (why organic substrate without UCIe).
  - Qualification & test methodology (MIL-883, JSS-55555, ATE lines).

### Step 4: Compile Slide Decks (`.pptx` + `-deck.html`)
1. Generate and run a compilation script using `python-pptx` to produce `<slug>-architecture.pptx`.
   - **Cross-Platform Python Execution**:
     - *Windows Native*: `python <script>.py` or `py -3 <script>.py`
     - *WSL / Linux*: `python3 <script>.py` or `uv run --with python-pptx python3 <script>.py`
     - The script must use `pathlib.Path` or `os.path.join`, UTF-8 encoding, and standard LF (`\n`) line endings.
2. Generate `<slug>-deck.html` containing all 10 widescreen slides in pure HTML/CSS.
3. **Cross-Platform Reveal & Activation**:
   - **Browser Deck**: Use `select_page` or `navigate_page` (Chrome DevTools MCP) to immediately display `<slug>-deck.html` in the user's active browser. CLI fallback: `Start-Process <slug>-deck.html` (Windows) or `wslview <slug>-deck.html` / `explorer.exe "$(wslpath -w <slug>-deck.html)"` (WSL).
   - **Explorer File Highlight**:
     - *Windows Native*: `explorer.exe /select,"<slug>-architecture.pptx"`
     - *WSL*: `explorer.exe /select,"$(wslpath -w <slug>-architecture.pptx)"` (translates Linux `/mnt/...` path to Windows drive path so Explorer resolves correctly).

### Step 5: Build Interactive Cockpit (`-workflow.html`)
- Author a responsive, dark-mode single-file HTML cockpit with:
  - Real-time signal bus flow indicator.
  - Node telemetry drawer displaying node, clock, voltage, power, and safety standards.
  - Simulation switcher pills allowing the user to inject faults and verify hardware recovery.

---

## SKU Parametric Grounding Table (Quick Reference)

| SKU / System | Primary Node & Foundry | Key Architectural Moat | Sockets & Standards |
|---|---|---|---|
| **SKU-1: BLDC Motor** | 130nm BCD (5–120V Rail) | FOC CORDIC PID (<1 µs loop latency) | BEE 5-Star Fans, EV 2-Wheelers |
| **SKU-2: Smart Meter** | 130nm CMOS | 24-bit $\Sigma\Delta$ ADC, <2 µW RTC | Class 0.5S, 250M National Meter Rollout |
| **SKU-3: Hi-Rel PMIC** | 180nm BCD (5–120V) | Brokaw bandgap (12 ppm/°C), DICE FSM | DO-160, MIL-STD-461, SRIJAN |
| **SKU-4: Lockstep MCU** | 130nm CMOS | Dual DGridRiscV with 2-cycle temporal skew | ISO 26262 ASIL-D, $\le 2$-cycle FAULTn |
| **SKU-5: Transceiver** | 130nm Thick-Oxide HV | 5V LDMOS, $\pm 15$ kV HBM ESD protection | CAN-FD (5 Mbps), RS-485 |
| **SKU-6: Supervisor** | 180nm CMOS | Chopper-stabilized comparator, 8 µs deglitch | Brownout detection & Master RESETn |
| **SKU-7: 77GHz Radar** | IHP SG13G2 BiCMOS (350GHz) | 4D Imaging MIMO, 3.75 cm resolution | DO-160G Airborne, Automotive ADAS |
| **SKU-8: Display Driver** | 130nm High-Voltage | 0–12V Column Amps, 1280x10b DACs | BEL 17" Rugged SXGA, PIL-5 #5 |
| **SKU-9: Zonal Gateway** | 130nm + 180nm BCD | 16x Smart e-Fuses, Gigabit TSN, CAN-XL | Software-Defined Vehicles, EV Platforms |
| **Track B: D100 Drone** | 130nm + 28nm Compute | 30 Hz EKF VIO + Hardware Failsafe Island | DGCA Type Cert, Indian Army Drones |
| **DG SDV Platform** | 28nm + 130/180nm SiP | 64-bit AXI4 Crossbar + AXI-REALM QoS + TMR | ISO 26262 ASIL-D, EVITA-Full HSM |
| **198-Day Silicon Loop** | OpenLane/Yosys/OpenROAD | 30d digital sprint + 168d fab shuttle | $14.3K MPW runs vs $1M proprietary EDA |
| **3-Factory Sovereignty**| SkyWater $\rightarrow$ IHP $\rightarrow$ SCL | Geopolitical insulation from US/EU bans | DAP-2020 Buy (Indian-IDDM) 100% IC |
