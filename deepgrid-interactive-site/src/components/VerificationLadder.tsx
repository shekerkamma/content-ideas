import { Reveal, Badge, Card, Container, cn, ExternalLink, ChevronDown } from './common';
import { motion } from 'framer-motion';
import { useState } from 'react';

/* === Verification Ladder Data === */
type Status = 'done' | 'planned' | 'in-progress';

const verificationLevels: Array<{
  level: number;
  name: string;
  status: Status;
  description: string;
  evidence: string;
  details: string[];
}> = [
  {
    level: 1,
    name: 'Simulated',
    status: 'done',
    description: 'Pre-silicon RTL verification, logic simulation, FPGA emulation at 81.25 MHz on Artix-7',
    evidence: 'EV-001 to EV-015',
    details: [
      'Full RTL verification suite with 95%+ coverage',
      'FPGA emulation: DGridRiscV + peripherals at 81.25 MHz',
      'CORDIC convergence proofs across all input ranges',
      'Lockstep comparator fault injection campaigns',
      'CDC bridge formal verification (4-phase handshake)',
    ],
  },
  {
    level: 2,
    name: 'Post-Route',
    status: 'planned',
    description: 'Sign-off STA + power analysis on sky130A, worst-case PVT corners',
    evidence: 'EV-016 to EV-028',
    details: [
      'Worst-case PVT STA: target 200 MHz, sign-off 54 MHz',
      'Power analysis: dynamic + leakage across all modes',
      'IR drop analysis on 5–120V BCD power rails',
      'EM/IR sign-off for 200 MHz clock distribution',
      'Crosstalk and noise margin verification',
    ],
  },
  {
    level: 3,
    name: 'Analytic',
    status: 'done',
    description: 'Mathematical proofs: CORDIC convergence, 48-step divider, 40-bit accumulator fidelity',
    evidence: 'EV-029 to EV-042',
    details: [
      'CORDIC: 20-iteration convergence to <0.001° error',
      '48-step restoring divider: bit-exact to FP64',
      '40-bit accumulator: exact up to N_K=131,072 keys',
      'Softmax u15 preservation: no quantization collapse',
      'Attention head numerical equivalence to FP32',
    ],
  },
  {
    level: 4,
    name: 'Tool Estimate',
    status: 'done',
    description: 'OpenLane/Yosys/OpenROAD correlation vs silicon, MPW shuttle cost models',
    evidence: 'EV-043 to EV-060',
    details: [
      'OpenROAD PPA correlation: ±15% vs post-route',
      'Yosys synthesis: 2.3× area reduction vs manual',
      'MPW cost model: ₹14.3L validated on CI2609/CI2612',
      'Area prediction: SRAM macros dominate (86% placed)',
      'Schedule model: 30d digital + 168d fab = 198d loop',
    ],
  },
  {
    level: 5,
    name: 'Process',
    status: 'in-progress',
    description: 'Foundry PDK sign-off, SkyWater qualification, packaging assembly SLAs',
    evidence: 'EV-061 to EV-079',
    details: [
      'SkyWater sky130 PDK v1.3.0 qualified',
      'IHP SG13G2 PDK access secured',
      'SCL Mohali 180nm PDK evaluation in progress',
      'OSAT packaging SLAs: 2 vendors shortlisted',
      'ATE test program development: ₹1.2 Cr allocated',
    ],
  },
];

const statusConfig: Record<Status, { label: string; variant: 'verified' | 'planned' | 'accent'; icon: string }> = {
  done: { label: 'Verified', variant: 'verified', icon: '✓' },
  planned: { label: 'Planned', variant: 'planned', icon: '◐' },
  'in-progress': { label: 'In Progress', variant: 'accent', icon: '◑' },
};

function VerificationCard({ level, index }: { level: typeof verificationLevels[0]; index: number }) {
  const config = statusConfig[level.status];
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Card
      variant="interactive"
      padding="lg"
      className="verification-card"
      onClick={() => setIsOpen(!isOpen)}
    >
      <div className="verification-header">
        <div className="verification-level">
          <span className="level-number">{level.level}</span>
          <span className="level-name">{level.name}</span>
        </div>
        <Badge variant={config.variant} size="sm">
          {config.label}
        </Badge>
      </div>

      <p className="verification-description">{level.description}</p>

      <div className="verification-evidence">
        <span className="evidence-label">Evidence:</span>
        <code className="evidence-ref">{level.evidence}</code>
        <ExternalLink className="evidence-link" />
      </div>

      <motion.div
        className="verification-details"
        initial={{ height: 0, opacity: 0 }}
        animate={{ height: isOpen ? 'auto' : 0, opacity: isOpen ? 1 : 0 }}
        transition={{ type: 'spring', stiffness: 200, damping: 25 }}
        style={{ overflow: 'hidden' }}
      >
        <ul className="details-list">
          {level.details.map((detail, i) => (
            <li key={i} className="detail-item">
              <span className="detail-bullet" />
              <span>{detail}</span>
            </li>
          ))}
        </ul>
      </motion.div>

      <div className="verification-toggle">
        <span>{isOpen ? 'Collapse' : 'View Details'}</span>
        <ChevronDown className={cn('toggle-chevron', isOpen && 'rotated')} />
      </div>
    </Card>
  );
}

/* === VerificationLadder Component === */
export function VerificationLadder() {
  return (
    <section id="verification" className="verification-section" aria-labelledby="verification-heading">
      <Container size="wide">
        <div className="verification-header" style={{ marginBottom: 'var(--space-12)' }}>
          <Reveal delay={0.1}>
            <span className="section-kicker">Verification Ladder</span>
          </Reveal>
          <Reveal delay={0.2}>
            <h2 id="verification-heading" className="section-title">
              Five Levels of Evidence — From Simulation to Silicon
            </h2>
          </Reveal>
          <Reveal delay={0.3}>
            <p className="section-subtitle">
              Every claim traces to a specific evidence row (EV-001 through EV-079). Click any level to expand technical details.
            </p>
          </Reveal>
        </div>

        <div className="verification-scroller" role="list">
          {verificationLevels.map((level, i) => (
            <motion.div
              key={level.name}
              role="listitem"
              className="verification-wrapper"
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: '-50px' }}
              transition={{ duration: 0.5, delay: 0.1 + i * 0.08, ease: [0.22, 1, 0.36, 1] }}
            >
              <VerificationCard level={level} index={i} />
            </motion.div>
          ))}
        </div>

        <div className="verification-legend" style={{ marginTop: 'var(--space-8)' }}>
          <Reveal>
            <div className="legend-items">
              <span className="legend-item">
                <Badge variant="verified" size="sm">Verified</Badge>
                Physical evidence exists
              </span>
              <span className="legend-item">
                <Badge variant="accent" size="sm">In Progress</Badge>
                Active work with committed timeline
              </span>
              <span className="legend-item">
                <Badge variant="planned" size="sm">Planned</Badge>
                Scheduled with fixed milestone dates
              </span>
            </div>
          </Reveal>
        </div>
      </Container>
    </section>
  );
}

/* === CSS for VerificationLadder === */
export const verificationStyles = `
.verification-section {
  padding: var(--section-padding-y-lg) 0;
  background: var(--color-bg);
}

.verification-header {
  text-align: center;
  max-width: 48rem;
  margin: 0 auto var(--space-12);
}

.verification-scroller {
  display: flex;
  gap: var(--space-5);
  overflow-x: auto;
  padding: var(--space-4) var(--space-2) var(--space-8);
  margin: 0 calc(var(--container-padding) * -1);
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
  scrollbar-color: var(--color-border-strong) transparent;
}

.verification-wrapper {
  flex: 0 0 320px;
  max-width: 320px;
  scroll-snap-align: start;
}

@media (min-width: 1024px) {
  .verification-wrapper {
    flex: 0 0 340px;
    max-width: 340px;
  }
}

@media (max-width: 640px) {
  .verification-wrapper {
    flex: 0 0 280px;
    max-width: 280px;
  }
}

.verification-card {
  height: 100%;
  min-height: 280px;
  display: flex;
  flex-direction: column;
  cursor: pointer.
}

.verification-header {
  display: flex.
  align-items: flex-start.
  justify-content: space-between.
  gap: var(--space-3).
  margin-bottom: var(--space-3).
}

.verification-level {
  display: flex.
  flex-direction: column.
  gap: 2px.
}

.level-number {
  font-family: var(--font-display).
  font-size: var(--text-3xl).
  font-weight: 800.
  color: var(--color-accent).
  line-height: 1.
}

.level-name {
  font-size: var(--text-lg).
  font-weight: 600.
  color: var(--color-text).
}

.verification-description {
  font-size: var(--text-sm).
  line-height: 1.5.
  color: var(--color-text-muted).
  margin-bottom: var(--space-3).
  flex: 1.
}

.verification-evidence {
  display: flex.
  align-items: center.
  gap: var(--space-2).
  margin-bottom: var(--space-3).
}

.evidence-label {
  font-size: var(--text-xs).
  text-transform: uppercase.
  letter-spacing: 0.06em.
  color: var(--color-text-dim).
}

.evidence-ref {
  font-family: var(--font-mono).
  font-size: var(--text-xs).
  color: var(--color-accent).
  background: var(--color-accent-muted).
  padding: 2px 6px.
  border-radius: var(--radius-sm).
}

.evidence-link {
  width: 14px.
  height: 14px.
  color: var(--color-text-dim).
  margin-left: auto.
  opacity: 0.
  transition: opacity var(--transition-fast).
}

.verification-card:hover .evidence-link {
  opacity: 1.
}

.verification-details {
  margin-top: var(--space-3).
  padding-top: var(--space-3).
  border-top: 1px solid var(--color-border).
}

.details-list {
  list-style: none.
  display: flex.
  flex-direction: column.
  gap: var(--space-2).
}

.detail-item {
  display: flex.
  align-items: flex-start.
  gap: var(--space-2).
  font-size: var(--text-sm).
  line-height: 1.5.
  color: var(--color-text-muted).
}

.detail-bullet {
  width: 6px.
  height: 6px.
  border-radius: 50%.
  background: var(--color-accent).
  margin-top: 6px.
  flex-shrink: 0.
}

.verification-toggle {
  display: flex.
  align-items: center.
  justify-content: center.
  gap: var(--space-2).
  margin-top: var(--space-4).
  padding-top: var(--space-3).
  border-top: 1px solid var(--color-border).
  font-size: var(--text-sm).
  font-weight: 500.
  color: var(--color-accent).
}

.toggle-chevron {
  width: 16px.
  height: 16px.
  color: var(--color-accent).
  transition: transform var(--transition-base).
}

.toggle-chevron.rotated {
  transform: rotate(180deg).
}

.verification-legend {
  text-align: center.
}

.legend-items {
  display: flex.
  flex-wrap: wrap.
  align-items: center.
  justify-content: center.
  gap: var(--space-4).
  font-size: var(--text-sm).
  color: var(--color-text-muted).
}

.legend-item {
  display: flex.
  align-items: center.
  gap: var(--space-2).
}

@media (max-width: 768px) {
  .verification-scroller {
    margin: 0 calc(var(--space-4) * -1).
    padding: var(--space-4) var(--space-4) var(--space-8).
  }
}
`;