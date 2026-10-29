import { Reveal, Card, Badge, ArrowRightIcon, ShieldIcon, ZapIcon, LockIcon, cn, Container, CheckIcon, Button, GlobeIcon, CpuIcon, ShieldCheckIcon, fadeUpChild } from './common';
import { useState, useRef } from 'react';
import { motion } from 'framer-motion';

/* === Pillar Data === */
const pillars = [
  {
    id: 'sovereign',
    icon: GlobeIcon,
    title: 'Sovereign Silicon',
    hook: "India's only sovereign motor-control SoC — dual-foundry, DAP-2020 compliant, 198-day loop",
    metric: { value: '3', label: 'Factories' },
    expanded: [
      {
        title: 'Three-Factory Sovereignty',
        items: [
          'SkyWater 130nm (USA) — Proven digital & mixed-signal prototyping',
          'IHP SG13G2 SiGe (Germany) — 350 GHz fT for 77 GHz radar',
          'SCL Mohali 180nm (India) — Buy(Indian-IDDM) defence monopoly',
        ],
      },
      {
        title: 'DAP-2020 & PIL Legal Moats',
        items: [
          'Buy(Indian-IDDM): Absolute priority in defence tenders',
          'PIL 1–5: 346+ line items with import ban deadlines',
          'SRIJAN: 37,000+ imported LRUs seeking domestic sources',
          'Make-II: Industry-funded dev → guaranteed production orders',
        ],
      },
      {
        title: '10x Cost Dismantling',
        items: [
          'Open-source EDA: Yosys + OpenROAD + TritonCTS = $0 licensing',
          'RISC-V DGridRiscV: Zero ARM royalties',
          'MPW shuttles: ₹14.3L vs $500K–$1M dedicated masks',
          'Per-chip NRE: ₹0.6–1.2 Cr vs $2–5M conventional',
        ],
      },
    ],
    cta: 'Explore Sovereignty Roadmap',
  },
  {
    id: 'deterministic',
    icon: CpuIcon,
    title: 'Deterministic Control',
    hook: '100 kHz loop in hardware, 0 jitter — CORDIC FOC in 6 µs, 82% CPU free',
    metric: { value: '300', label: 'Cycles Fixed HW' },
    expanded: [
      {
        title: 'FOC Pipeline (Measured on sky130A)',
        items: [
          'Phase Current Sample (SAR ADC): 177 cycles (3.54 µs)',
          'Clarke/Park Transform (HW CORDIC): 53–58 cycles',
          'PI Regulators (CPU): ~8 cycles/instruction',
          'Inverse Park (HW CORDIC): 53–58 cycles',
          'SVPWM Update: Zero software wait-states',
          'Total Fixed Hardware: ~300 cycles (~6 µs)',
        ],
      },
      {
        title: 'Headroom at Loop Rates',
        items: [
          '10 kHz: 5,000 cycles → 4,700 free (>90%)',
          '20 kHz: 2,500 cycles → 2,200 free (88%)',
          '50 kHz: 1,000 cycles → 700 free (70%)',
          'Sensor-to-PWM latency: ~5 µs + ~5 µs = 100 kHz bandwidth',
        ],
      },
      {
        title: 'DGridRiscV Architecture',
        items: [
          'RV32IM_Zicsr, 8-stage pipeline, cacheless, non-speculative',
          '200 MHz target on 130nm ASIC',
          'Physical Memory Protection (PMP) regions',
          'Dual 32-bit AXI4 ports (cacheless, fixed TCM)',
          'CORDIC Engine: 95.5 MHz Fmax, 53–58 cycles sin/cos/atan2/mag',
        ],
      },
    ],
    cta: 'View Technical Deep Dive',
  },
  {
    id: 'safety',
    icon: ShieldCheckIcon,
    title: 'Hardware Lockstep Safety',
    hook: '39-cycle fault-to-bridge-off — no firmware in the safety path',
    metric: { value: '39', label: 'Cycles to Safe' },
    expanded: [
      {
        title: 'Dual-Core Lockstep Architecture',
        items: [
          '2× DGridRiscV cores with 2-cycle temporal skew',
          'Hardware comparator asserts FAULTn in ≤2 cycles',
          'Async PWM brake response ≤2 cycles from fault',
          'Total fault-to-bridge-off: ≤39 cycles (measured)',
          'End-to-end ECC on all buses and SRAM',
        ],
      },
      {
        title: 'Safety Standards Target',
        items: [
          'ISO 26262 ASIL-D',
          'IEC 61508 SIL-3',
          'DO-254 DAL-A',
          'AEC-Q100 Grade 1',
        ],
      },
      {
        title: 'Zero Firmware in Safety Path',
        items: [
          'Hardwired comparator → PWM brake, zero software',
          'Fault CSR: Latches first mismatch cause stickily',
          'MAGIC-locked test injection (0xDEAD_5AFE)',
          'Supervisor/wWDT: Windowed watchdog + rail guard',
        ],
      },
    ],
    cta: 'View Safety Architecture',
  },
];

/* === PillarCard Component === */
function PillarCard({ pillar, index }: { pillar: typeof pillars[0]; index: number }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const expandedRef = useRef<HTMLDivElement>(null);

  return (
    <Card variant="interactive" padding="xl" className="pillar-card h-full">
      <div className="pillar-header">
        <div className="pillar-icon-wrapper">
          <pillar.icon />
        </div>
        <div className="pillar-meta">
          <span className="pillar-metric">
            <span className="metric-value">{pillar.metric.value}</span>
            <span className="metric-label">{pillar.metric.label}</span>
          </span>
          <Badge variant="accent" size="sm">Click to expand</Badge>
        </div>
      </div>

      <h3 className="pillar-title">{pillar.title}</h3>
      <p className="pillar-hook">{pillar.hook}</p>

      {/* Expanded Content */}
      <div
        ref={expandedRef}
        className="pillar-expanded"
        style={{
          height: isExpanded ? 'auto' : 0,
          opacity: isExpanded ? 1 : 0,
          overflow: 'hidden',
          transition: 'height 0.4s ease, opacity 0.3s ease',
        }}
      >
        <div className="pillar-expanded-content">
          {pillar.expanded.map((section, si) => (
            <div key={section.title} className="pillar-section">
              <h4 className="pillar-section-title">{section.title}</h4>
              <ul className="pillar-section-list">
                {section.items.map((item, ii) => (
                  <li key={ii} className="pillar-section-item">
                    <CheckIcon className="item-check" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}

          <Button
            variant="outline"
            size="md"
            rightIcon={<ArrowRightIcon />}
            className="pillar-cta w-full"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            {isExpanded ? 'Collapse' : pillar.cta}
          </Button>
        </div>
      </div>
    </Card>
  );
}

/* === Pillars Section === */
export function Pillars() {
  return (
    <section id="pillars" className="pillars-section" aria-labelledby="pillars-heading">
      <Container size="wide">
        <div className="pillars-header" style={{ marginBottom: 'var(--space-16)' }}>
          <Reveal delay={0.1}>
            <span className="section-kicker">Core Pillars</span>
          </Reveal>
          <Reveal delay={0.2}>
            <h2 id="pillars-heading" className="section-title">
              Why DeepGrid Exists: Three Unbreakable Foundations
            </h2>
          </Reveal>
          <Reveal delay={0.3}>
            <p className="section-subtitle">
              Each pillar represents a structural advantage that compounds across our entire portfolio — not features, but foundations.
            </p>
          </Reveal>
        </div>

        <div className="pillars-grid" role="list">
          {pillars.map((pillar, i) => (
            <motion.div
              key={pillar.id}
              role="listitem"
              className="pillar-wrapper"
              initial={{ opacity: 0, y: 32 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-100px' }}
              transition={{ duration: 0.6, delay: 0.1 + i * 0.1, ease: [0.22, 1, 0.36, 1] }}
            >
              <PillarCard pillar={pillar} index={i} />
            </motion.div>
          ))}
        </div>
      </Container>
    </section>
  );
}

/* === CSS for Pillars === */
export const pillarsStyles = `
.pillars-section {
  padding: var(--section-padding-y-lg) 0;
  background: var(--color-bg);
}

.pillars-header {
  text-align: center;
  max-width: 48rem;
  margin: 0 auto var(--space-16);
}

.section-kicker {
  display: inline-block;
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-accent);
  margin-bottom: var(--space-3);
  padding-bottom: var(--space-2);
  border-bottom: 1px solid var(--color-accent);
}

.section-title {
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1.15;
  font-weight: 800;
  margin-bottom: var(--space-4);
  color: var(--color-text);
}

.section-subtitle {
  font-size: var(--text-lg);
  line-height: var(--leading-relaxed);
  color: var(--color-text-muted);
  max-width: 56ch;
  margin: 0 auto;
}

.pillars-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-6);
}

@media (min-width: 768px) {
  .pillars-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .pillars-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.pillar-wrapper {
  height: auto;
}

.pillar-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.pillar-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.pillar-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: var(--color-accent-muted);
  border: 1px solid rgba(4, 179, 199, 0.3);
  border-radius: var(--radius-lg);
  color: var(--color-accent);
  flex-shrink: 0;
}

.pillar-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--space-1);
}

.pillar-metric {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.metric-value {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 800;
  color: var(--color-accent);
  line-height: 1;
}

.metric-label {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-dim);
}

.pillar-title {
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--space-2);
}

.pillar-hook {
  font-size: var(--text-sm);
  line-height: 1.5;
  color: var(--color-text-muted);
  margin-bottom: var(--space-6);
}

.pillar-expanded-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border);
}

.pillar-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.pillar-section-title {
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-accent);
}

.pillar-section-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.pillar-section-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  font-size: var(--text-sm);
  line-height: 1.5;
  color: var(--color-text-muted);
}

.item-check {
  width: 16px;
  height: 16px;
  color: var(--color-success);
  flex-shrink: 0;
  margin-top: 2px;
}

.pillar-cta {
  margin-top: var(--space-2);
  justify-content: center;
}

@media (max-width: 768px) {
  .pillar-card {
    padding: var(--space-5);
  }

  .pillar-icon-wrapper {
    width: 48px;
    height: 48px;
  }

  .metric-value {
    font-size: var(--text-lg);
  }
}
`;