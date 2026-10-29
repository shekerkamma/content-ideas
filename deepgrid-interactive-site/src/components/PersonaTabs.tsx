import { Reveal, Badge, Card, Button, Container, cn, ArrowRightIcon, DownloadIcon, CalendarIcon, GithubIcon, CheckIcon, ShieldIcon, ZapIcon, LockIcon, GlobeIcon, CpuIcon, UsersIcon, CubeIcon, ExternalLink } from './common';
import { motion } from 'framer-motion';
import { useState } from 'react';

/* === Persona Data === */
const personas = [
  {
    id: 'investor',
    label: 'Investor',
    icon: ShieldIcon,
    color: '#1ba271',
    tagline: '₹10 Cr seed → ₹1,000 Cr FY31 | 10x NRE advantage | Legal moats | Live revenue',
    cta: 'Download Data Room Pack',
    ctaVariant: 'primary' as const,
    sections: [
      {
        title: 'Unit Economics',
        items: [
          'NRE per chip: ₹0.6–1.2 Cr vs $2–5M conventional (10x reduction)',
          'Gross margins: 60–75% at 10k units (defence), 30–45% (commercial)',
          'Open-source EDA: $0 licensing (Yosys/OpenROAD/TritonCTS)',
          'RISC-V DGridRiscV: Zero ARM royalties',
          'MPW shuttles: ₹14.3L for 100 parts vs $500K–$1M dedicated masks',
        ],
      },
      {
        title: 'TAM & Revenue Build',
        items: [
          'India mature-node imports: $23.4B total → $9B (≥130nm) → ₹4,000 Cr addressable',
          'FY27: ₹4 Cr (₹2.88 Cr live contracted)',
          'FY28: ₹28 Cr | FY29: ₹140 Cr | FY30: ₹410 Cr | FY31: ₹1,000 Cr',
          'Blended GM: ~48% at scale',
          'Smart Meter (₹480 Cr) + Motor (₹220 Cr) = 70% of FY31',
        ],
      },
      {
        title: 'Structural Moats',
        items: [
          'DAP-2020 Buy(Indian-IDDM): Absolute monopoly in defence tenders',
          'PIL 1–5: 346+ line items with hard import ban deadlines',
          'SRIJAN: 37,000+ imported LRUs seeking domestic sources',
          'Three-factory sovereignty: SkyWater → IHP → SCL Mohali',
          '1,000 silicon-validated IP blocks compounding across 50 SKUs',
        ],
      },
      {
        title: 'Risk Management (Stop Rules)',
        items: [
          'S1: Anchor LOI gate — no signature by shuttle cutoff = pause chip',
          'S2: MIL-STD-883 fail-safe — Chip 6 failure = 12-month defence delay',
          'S3: Chinese price crash exit — FY29 commodity price check',
          'S4: SCL Mohali slip pivot — 2-cycle delay = public disclosure + SkyWater/IHP pivot',
          'Stress test: Chinese dumping → ₹750 Cr floor (defence ₹200 Cr untouched)',
        ],
      },
      {
        title: 'Use of Funds (₹10 Cr)',
        items: [
          'Factory Runs & Mask Sets: ₹3.60 Cr (36%) — 6× SkyWater MPW, 1× IHP, 2× production masks',
          'Engineering Staff: ₹2.40 Cr (24%) — 5–7 engineers × 24 months',
          'Qualification & Screening: ₹1.80 Cr (18%) — 4 pathfinder chips',
          'ATE Test Engineering: ₹1.20 Cr (12%) — test vectors, load boards',
          'GTM & Working Capital: ₹1.00 Cr (10%) — eval kits, reference designs',
        ],
      },
    ],
  },
  {
    id: 'engineer',
    label: 'Engineer',
    icon: CpuIcon,
    color: '#04b3c7',
    tagline: '200 MHz cacheless RISC-V | 39-cycle fault isolation | 100 kHz FOC | Open RTL',
    cta: 'Clone SDK Repository',
    ctaVariant: 'primary' as const,
    sections: [
      {
        title: 'DGridRiscV Architecture',
        items: [
          'ISA: RV32IM_Zicsr (misa=0x40001100), Machine mode only',
          'Pipeline: 8-stage (2 Fetch, 6 Execute), single-issue, in-order',
          'No caches, no branch predictor, no FPU, no RVC — deterministic by design',
          'PMP regions for safety isolation (10× less area than MMU)',
          'Dual 32-bit AXI4 ports (cacheless, fixed TCM), 200 MHz target',
          'Multiplier/Divider: Fully unrolled single-cycle hardware blocks',
        ],
      },
      {
        title: 'FOC Pipeline (Measured on sky130A A3)',
        items: [
          'Phase Current Sample (SAR ADC): 177 cycles (3.54 µs) — PWM-triggered at ripple null',
          'Clarke/Park Transform (HW CORDIC): 53–58 cycles per operation',
          'PI Regulators (CPU): ~8 cycles/instruction (fetch-bound from SRAM)',
          'Inverse Park (HW CORDIC): 53–58 cycles per operation',
          'SVPWM Update: Zero software wait-states (shadow registers at center count)',
          'Total Fixed Hardware: ~300 cycles (~6 µs) per control period',
        ],
      },
      {
        title: 'Headroom at Loop Rates',
        items: [
          '10 kHz: 5,000 cycles → 4,700 free (>90%) — full FOC + speed loop + observers',
          '20 kHz: 2,500 cycles → 2,200 free (88%) — FOC + field weakening',
          '50 kHz: 1,000 cycles → 700 free (70%) — high-speed inner current loop only',
          'Sensor-to-PWM latency: ~5 µs acquisition + ~5 µs compute = 100 kHz bandwidth',
        ],
      },
      {
        title: 'DG32-2DOM Dual-Clock Architecture',
        items: [
          'clk_i: 50 MHz CPU & control domain (timing closed to 54 MHz)',
          'clk_fast_i: 114 MHz fast accelerator domain (INT8 attention)',
          '4-phase req/ack CDC bridges with 2-FF synchronizers (dgrid_axi_cdc_*)',
          'Timing isolation: 114 MHz domain cannot pull down 50 MHz CPU closure',
          'CPU PMA whitelist: fault = !(addr[31] | addr[31:28] == 0x1)',
          'Unmapped accesses complete with SLVERR (never hangs CPU)',
        ],
      },
      {
        title: 'INT8 Attention Engine (dgrid_int8_attn @ 0xE000_0000)',
        items: [
          'Executes QK^T, row max, 256-entry u15 EXP, Z, E·V, per-row reciprocal, saturate to int8',
          '40-bit signed numerator datapath — exact up to N_K = 131,072 (int32 breaks at 512)',
          'Softmax weights never quantized (u15 preserved into 40-bit accumulator)',
          '48-step restoring hardware divider for per-row reciprocal',
          'On-chip K/V buffers (SRAM macros) — loaded once, re-read per row',
          'Bus occupancy ~1% vs 400× if streamed per row',
        ],
      },
      {
        title: 'AVIP Bearing-Fault Classifier',
        items: [
          'CWRU model: 47,076 params, 46.7 ms @ 114 MHz, 94–95% held-out accuracy (INT8 = FP32)',
          'Full AVIP: 478,277 params, 54.5 ms @ 114 MHz, comprehensive multi-defect coverage',
          'Zero external accelerometers — MCSA via on-die SAR ADC (0xDB) at PWM ripple null',
          'Current envelope carries exact same mechanical fault signature as accelerometer',
          'Dual-channel: raw fundamental + AM fault envelope from single phase current',
        ],
      },
      {
        title: 'DShot Bidirectional Telemetry',
        items: [
          'Slot 0xC RTL extension — reuses existing AXI-lite decoder',
          'GCR 4b→5b transition encoding, inverted line convention',
          'eRPM payload: 3-bit exponent, 9-bit mantissa, inverted CRC4',
          'Pad-ring reuse: 4 PWM high-side pads switch PC_OUT → PC_BIDIR dynamically',
          'Low-side pads remain PC_OUT (prevents shoot-through)',
          'SRAM floorplan: 28 KB (14 macros) vs 32 KB enables 3×6 column arrangement',
        ],
      },
      {
        title: 'Pinout & Package',
        items: [
          'QFN-64, 5–120V BCD process, power sequencing spec',
          'Register maps: 21-slave AXI fabric decoded via addr[31:28] + addr[27:24]',
          'Peripherals: 7-ch PWM, 16-bit ADC×3, CAN-FD, UART×2, SPI, I2C, GPIO, Timers',
          'Fault CSR @ 0xD600_0000: sticky latch, MAGIC-locked injection (0xDEAD_5AFE)',
          'Supervisor/wWDT @ 0xD700_0000: windowed watchdog + rail guard',
        ],
      },
    ],
  },
  {
    id: 'procurement',
    label: 'Procurement',
    icon: CubeIcon,
    color: '#d7720b',
    tagline: 'BOM comparison | Qualification status | Supply continuity | PIL/DAP mapping',
    cta: 'Request Qualification Samples',
    ctaVariant: 'primary' as const,
    sections: [
      {
        title: 'BOM Comparison (DeepGrid vs TI/ADI/Microchip)',
        items: [
          'Chip 1 (BLDC): $3–8 vs $15–25 (TI DRV83xx + MCU two-chip set)',
          'Chip 2 (Smart Meter): $2–5 vs $8–15 (ADI ADE9153 + MCU)',
          'Chip 4 (Lockstep MCU): $4–12 vs $25–50 (Renesas RH850 / Infineon AURIX)',
          'Chip 6 (Supervisor): $0.20–0.80 vs $1–3 (TI/Maxim)',
          'Volume threshold: DeepGrid profitable at 10k units; incumbents need 10M+',
        ],
      },
      {
        title: 'Qualification Tracker',
        items: [
          'Chip 1 (Motor): Commercial qualification Q2 FY28 — AEC-Q100 Grade 0',
          'Chip 2 (Meter): Commercial qualification Q2 FY28 — Class 0.5S metrology',
          'Chip 3 (PMIC): DO-160 / MIL-STD-461 Q3 FY28 — avionics grade',
          'Chip 4 (Lockstep): ISO 26262 ASIL-D Q4 FY28 — functional safety',
          'Chip 6 (Supervisor): MIL-STD-883 pathfinder Q1 FY28 — screening learning',
        ],
      },
      {
        title: 'Supply Continuity',
        items: [
          'Three foundries: SkyWater (USA), IHP (Germany), SCL Mohali (India)',
          'Two countries + domestic = geopolitical redundancy',
          'MPW → dedicated mask → volume production flow per SKU',
          '20–30 year longevity guarantees on mature 130nm masks',
          'KGD (Known-Good-Die) wafer probing mandatory for SiP assembly',
        ],
      },
      {
        title: 'PIL / DAP Mapping (Defence Line Items)',
        items: [
          'PIL-5 Anti-Tank Missile Actuator → Chip 1 (Integrated FOC BLDC)',
          'BEL Tank DC-DC Converter (4A, 16–40V) → Chip 3 (28V Hi-Rel PMIC)',
          'BEL EW Receiver & Synthesizer → Chip 7 Family (SiGe RF + Digital)',
          'BEL 17-inch Rugged Cockpit Display → Chip 8 (HV Display Driver)',
          'Su-30 MKI / Mi-17 Radar Warning Receiver → Chip 7 Variant',
        ],
      },
      {
        title: 'Quality Systems (Year 1 Target)',
        items: [
          'ISO 9001 / AS9100 certification — audited by DRDO/BEL/HAL before AVL',
          'Documented ECN (Engineering Change Notification) procedures',
          'Strict ESD/EOS facility handling controls',
          '10–20 year LTB (Last-Time-Buy) supply policies',
          'Full lot traceability for screened defence parts',
        ],
      },
    ],
  },
  {
    id: 'partner',
    label: 'Partner',
    icon: UsersIcon,
    color: '#60a5fa',
    tagline: 'SDK | Reference designs | Reference boards | Support SLAs | Training',
    cta: 'Join Partner Program',
    ctaVariant: 'primary' as const,
    sections: [
      {
        title: 'SDK Contents',
        items: [
          'Bare-metal HAL + FreeRTOS port',
          'CORDIC math library: sin/cos/atan2/mag in 53–58 cycles',
          'FOC framework: PID, Clarke/Park, SVPWM, observer templates',
          'DG32-LITE: 30 use case model zoo (RF, LDA, GB, EKF, HMM, MLP, Isolation Forest)',
          'DG32-2DOM: INT8 attention driver, AVIP model loader, CDC bridge API',
          'Open-source toolchain: Yosys + OpenROAD + GCC RISC-V',
        ],
      },
      {
        title: 'Reference Boards',
        items: [
          'DGS001 / DGFP4 demonstration boards (FPGA-based, 81.25 MHz validated)',
          'Production eval boards: $50 target, 1-week bring-up',
          'Breakout boards for each SKU with sensor interfaces',
          'Debug probes: JTAG + SWO + UART console',
        ],
      },
      {
        title: 'Reference Designs',
        items: [
          'BLDC motor drive: Star/Delta reconfig, 5–120V, sensorless + sensored',
          'Smart meter metrology: Class 0.5S, hardware tamper detection, LoRaWAN',
          'Safety MCU: ASIL-D lockstep, fault injection test suite, FMEDA templates',
          'Zonal gateway: 16 smart e-fuses, TSN switch, CAN-XL, EVITA-Full HSM',
        ],
      },
      {
        title: 'Support SLAs',
        items: [
          'Community: GitHub issues, Discord, monthly office hours (free)',
          'Professional: 48-hr response, design review, bring-up assistance (paid tier)',
          'Enterprise: Dedicated FAE, custom RTL modifications, co-qualification support',
        ],
      },
      {
        title: 'Training Program',
        items: [
          'Monthly "Silicon Office Hours" webinars (technical deep-dives)',
          'Quarterly 2-day bring-up workshops (Hyderabad / Bangalore)',
          'Custom on-site training for volume partners',
          'Certification program: DG32 Certified Integration Engineer',
        ],
      },
    ],
  },
];

/* === PersonaTabs Component === */
export function PersonaTabs() {
  const [activePersona, setActivePersona] = useState('investor');

  return (
    <section id="personas" className="personas-section" aria-labelledby="personas-heading">
      <Container size="wide">
        <div className="personas-header" style={{ marginBottom: 'var(--space-12)' }}>
          <Reveal delay={0.1}>
            <span className="section-kicker">Choose Your Path</span>
          </Reveal>
          <Reveal delay={0.2}>
            <h2 id="personas-heading" className="section-title">
              Deep Dives Tailored to Your Role
            </h2>
          </Reveal>
          <Reveal delay={0.3}>
            <p className="section-subtitle">
              Each path curates the same technical truth through a different lens — pick yours.
            </p>
          </Reveal>
        </div>

        {/* Persona Tabs */}
        <div className="persona-tabs" role="tablist" aria-label="Persona selection">
          {personas.map((persona, i) => (
            <button
              key={persona.id}
              role="tab"
              aria-selected={activePersona === persona.id}
              aria-controls={`panel-${persona.id}`}
              id={`tab-${persona.id}`}
              className={cn('persona-tab', activePersona === persona.id && 'active')}
              onClick={() => setActivePersona(persona.id)}
              style={{ '--persona-color': persona.color } as React.CSSProperties}
            >
              <persona.icon className="tab-icon" />
              <span className="tab-label">{persona.label}</span>
            </button>
          ))}
        </div>

        {/* Active Panel */}
        <motion.div
          id={`panel-${activePersona}`}
          role="tabpanel"
          aria-labelledby={`tab-${activePersona}`}
          className="persona-panel"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
        >
          {personas.map((persona) => (
            persona.id === activePersona && (
              <PersonaPanel key={persona.id} persona={persona} />
            )
          ))}
        </motion.div>
      </Container>
    </section>
  );
}

/* === PersonaPanel Component === */
function PersonaPanel({ persona }: { persona: typeof personas[0] }) {
  return (
    <div className="persona-panel-content" style={{ '--persona-color': persona.color } as React.CSSProperties}>
      <div className="panel-header">
        <div className="panel-icon" style={{ background: `${persona.color}20`, color: persona.color } as React.CSSProperties}>
          <persona.icon />
        </div>
        <div>
          <h3 className="panel-title">{persona.label} Deep Dive</h3>
          <p className="panel-tagline">{persona.tagline}</p>
        </div>
        <Button
          variant={persona.ctaVariant}
          size="lg"
          rightIcon={<ArrowRightIcon />}
          className="panel-cta"
        >
          {persona.cta}
        </Button>
      </div>

      <div className="panel-sections">
        {persona.sections.map((section, i) => (
          <motion.div
            key={section.title}
            className="panel-section"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.05 * i, ease: [0.22, 1, 0.36, 1] }}
          >
            <h4 className="section-heading">{section.title}</h4>
            <ul className="section-list">
              {section.items.map((item, ii) => (
                <li key={ii} className="list-item">
                  <CheckIcon className="list-check" style={{ color: persona.color }} />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </motion.div>
        ))}
      </div>

      <div className="panel-secondary-ctas">
        <Button variant="outline" leftIcon={<DownloadIcon />}>
          Download Master Whitepaper (71 pages)
        </Button>
        <Button variant="ghost" leftIcon={<CalendarIcon />}>
          Schedule Technical Call
        </Button>
        <Button variant="ghost" leftIcon={<GithubIcon />}>
          View SDK on GitHub
        </Button>
      </div>
    </div>
  );
}

/* === CSS for PersonaTabs === */
export const personaStyles = `
.personas-section {
  padding: var(--section-padding-y-lg) 0;
  background: var(--color-bg);
}

.personas-header {
  text-align: center;
  max-width: 56rem;
  margin: 0 auto var(--space-12);
}

.persona-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  justify-content: center;
  margin-bottom: var(--space-12);
  background: var(--color-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-2);
}

.persona-tab {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-text-muted);
  background: transparent;
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.persona-tab:hover {
  color: var(--color-text);
  background: var(--color-card);
}

.persona-tab.active {
  color: var(--color-text-inverse);
  background: var(--persona-color);
  box-shadow: 0 4px 16px var(--persona-color);
}

.persona-tab:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.tab-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.persona-panel {
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.persona-panel-content {
  padding: var(--space-8);
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-6);
  flex-wrap: wrap;
}

.panel-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.panel-icon svg {
  width: 32px;
  height: 32px;
}

.panel-title {
  font-size: var(--text-2xl);
  font-weight: 800;
  color: var(--color-text);
  margin-bottom: var(--space-1);
}

.panel-tagline {
  font-size: var(--text-base);
  color: var(--color-text-muted);
  line-height: 1.5;
}

.panel-cta {
  flex-shrink: 0;
  white-space: nowrap;
}

.panel-sections {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.panel-section {
  padding: var(--space-5);
  background: var(--color-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  border-left: 3px solid var(--persona-color);
}

.section-heading {
  font-size: var(--text-base);
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--space-3);
}

.section-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.list-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  font-size: var(--text-sm);
  line-height: 1.6;
  color: var(--color-text-muted);
}

.list-check {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  margin-top: 2px;
}

.panel-secondary-ctas {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border);
  justify-content: center;
}

@media (max-width: 768px) {
  .persona-panel-content {
    padding: var(--space-5);
  }

  .panel-header {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }

  .panel-icon {
    margin: 0 auto;
  }

  .panel-cta {
    width: 100%;
    justify-content: center;
  }

  .panel-secondary-ctas {
    flex-direction: column;
  }

  .panel-secondary-ctas button {
    width: 100%;
    justify_content: center;
  }
}
`;