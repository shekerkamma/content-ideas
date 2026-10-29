import { Reveal, Badge, Card, Container, cn, CheckIcon, ChevronDown, ChevronRight } from './common';
import { motion, useInView } from 'framer-motion';
import { useRef, useState } from 'react';

/* === Use Cases Data === */
const useCaseDomains = [
  {
    id: 'rotating',
    title: 'Rotating Machinery',
    subtitle: '8 defect models — bearings, gearboxes, pumps, fans, compressors',
    icon: '🔧',
    color: '#e06767',
    useCases: [
      { id: 1, name: 'Bearing Fault Classification', model: 'RF 100×d8', latency: '0.92 ms', rate: '890 Hz', standard: 'ISO 13373-2' },
      { id: 2, name: 'Bearing Severity Trending', model: 'LDA', latency: '0.14 ms', rate: '>1 kHz', standard: 'ISO 20816' },
      { id: 3, name: 'Gearbox / Mesh Faults', model: 'RF 100×d8', latency: '1.69 ms', rate: '480 Hz', standard: 'ISO 10816' },
      { id: 4, name: 'Pump Cavitation & Dry-Run', model: 'GB 200×d4', latency: '0.82 ms', rate: '>1 kHz', standard: 'Hydraulic Inst.' },
      { id: 5, name: 'Fan / Blower Imbalance', model: 'LDA', latency: '0.76 ms', rate: '>1 kHz', standard: 'ISO 21940' },
      { id: 6, name: 'Compressor Valve Faults', model: 'RF 100×d8', latency: '0.78 ms', rate: '>1 kHz', standard: 'API 670' },
      { id: 7, name: 'Belt Slip & Misalignment', model: 'Logistic Reg', latency: '0.62 ms', rate: '>1 kHz', standard: '—' },
      { id: 8, name: 'Shaft Misalignment / Looseness', model: 'RF 100×d8', latency: '0.82 ms', rate: '>1 kHz', standard: 'ISO 10816' },
    ],
  },
  {
    id: 'electrical',
    title: 'Electrical & Power',
    subtitle: '8 diagnostics — rotor bars, eccentricity, stator shorts, arc faults, power quality',
    icon: '⚡',
    color: '#d7720b',
    useCases: [
      { id: 9, name: 'Broken Rotor Bar Detection', model: 'Goertzel (2sf1) → LDA', latency: '0.13 ms', rate: '>1 kHz', standard: 'IEEE 112' },
      { id: 10, name: 'Air-Gap Eccentricity', model: 'Goertzel (f1±m·fr) → LDA', latency: '0.13 ms', rate: '>1 kHz', standard: '—' },
      { id: 11, name: 'Stator Inter-Turn Short', model: 'Park + RMS → Mahalanobis', latency: '0.14 ms', rate: '>1 kHz', standard: '—' },
      { id: 12, name: 'Phase Loss & Unbalance', model: 'Park Vector → Logistic Reg', latency: '<0.01 ms', rate: '>1 kHz', standard: '—' },
      { id: 13, name: 'Arc-Fault & Partial Discharge', model: 'Envelope + FFT-256 → OCSVM', latency: '0.97 ms', rate: '840 Hz', standard: 'UL 1699' },
      { id: 14, name: 'Power-Quality Events', model: 'Goertzel Bins → LDA', latency: '0.13 ms', rate: '>1 kHz', standard: 'IEC 61000' },
      { id: 15, name: 'Battery State-of-Health (SoH)', model: 'Moments → MLP 32-16-8-4', latency: '0.19 ms', rate: '>1 kHz', standard: '—' },
      { id: 16, name: 'Winding Thermal Estimation', model: 'RMS History → EKF', latency: '0.11 ms', rate: '>1 kHz', standard: '—' },
    ],
  },
  {
    id: 'control',
    title: 'Control & Motion',
    subtitle: '8 real-time models — sensorless EKF, plausibility, regime, friction, stall, torque ripple',
    icon: '🎯',
    color: '#04b3c7',
    useCases: [
      { id: 17, name: 'Sensorless Rotor Position', model: 'HW Park → EKF', latency: '0.05 ms', rate: '>1 kHz', standard: '—' },
      { id: 18, name: 'Learned Sensor Plausibility', model: 'HW Park → Nearest Centroid', latency: '0.02 ms', rate: '>1 kHz', standard: '—' },
      { id: 19, name: 'Operating-Mode Classification', model: 'RMS Velocity → GMM', latency: '0.10 ms', rate: '>1 kHz', standard: '—' },
      { id: 20, name: 'Duty-Cycle & State Tracking', model: 'HW Timers → HMM 8-state', latency: '0.06 ms', rate: '>1 kHz', standard: '—' },
      { id: 21, name: 'Adaptive Friction Compensation', model: 'HW Park → MLP 32-16-8-4', latency: '0.06 ms', rate: '>1 kHz', standard: '—' },
      { id: 22, name: 'Kickback & Stall Detection', model: 'RMS Current Slope → GB 200×d4', latency: '0.12 ms', rate: '>1 kHz', standard: '—' },
      { id: 23, name: 'Load Estimation & Torque Ripple', model: 'FFT-256 → Logistic Reg', latency: '0.62 ms', rate: '>1 kHz', standard: '—' },
      { id: 24, name: 'Multivariate Anomaly Scoring', model: 'Moments → Mahalanobis IRQ', latency: '0.22 ms', rate: '>1 kHz', standard: '—' },
    ],
  },
  {
    id: 'degradation',
    title: 'Degradation & RUL',
    subtitle: '6 trend models — RUL regression, drift detection, forecasting, CNN, isolation forest',
    icon: '📈',
    color: '#60a5fa',
    useCases: [
      { id: 25, name: 'Remaining Useful Life (RUL)', model: '64-step History → MLP 128-64-32-8', latency: '0.84 ms', rate: '970 Hz', standard: 'ISO 13374' },
      { id: 26, name: 'Unsupervised Drift Detection', model: 'Moments → MLP Autoencoder', latency: '0.58 ms', rate: '>1 kHz', standard: '—' },
      { id: 27, name: 'Short-Horizon Forecasting', model: 'Normalized Vector → GRU 16', latency: '2.95 ms', rate: '270 Hz', standard: '—' },
      { id: 28, name: 'Raw-Waveform Classification', model: 'Decimate → 1D-CNN 8/16/32', latency: '10.32 ms', rate: '79 Hz', standard: '—' },
      { id: 29, name: 'Novelty Detection (Unlabelled)', model: 'Moments → Isolation Forest', latency: '0.20 ms', rate: '>1 kHz', standard: '—' },
      { id: 30, name: 'Per-Machine Baselining', model: 'Moments → k-NN (200 proto)', latency: '0.65 ms', rate: '>1 kHz', standard: '—' },
    ],
  },
];

/* === DomainCard Component === */
function DomainCard({ domain, index }: { domain: typeof useCaseDomains[0]; index: number }) {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <div ref={ref} className="domain-wrapper">
      <motion.div
        initial={{ opacity: 0, y: 32 }}
        animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 32 }}
        transition={{ duration: 0.6, delay: 0.1 + index * 0.1, ease: [0.22, 1, 0.36, 1] }}
      >
        <Card
          variant="interactive"
          padding="lg"
          className={cn('domain-card', isOpen && 'open')}
          onClick={() => setIsOpen(!isOpen)}
        >
          <div className="domain-header">
            <div className="domain-icon" style={{ background: `${domain.color}20`, color: domain.color }}>
              <span style={{ fontSize: 'var(--text-2xl)' }}>{domain.icon}</span>
            </div>
            <div className="domain-title-group">
              <h3 className="domain-title">{domain.title}</h3>
              <p className="domain-subtitle">{domain.subtitle}</p>
            </div>
            <div className="domain-meta">
              <Badge variant="accent" size="sm">
                {domain.useCases.length} Use Cases
              </Badge>
              <ChevronDown className={cn('domain-chevron', isOpen && 'rotated')} />
            </div>
          </div>

          <div
            className="domain-content"
            style={{
              height: isOpen ? 'auto' : 0,
              opacity: isOpen ? 1 : 0,
              overflow: 'hidden',
              transition: 'height 0.4s ease, opacity 0.3s ease',
            }}
          >
            <div className="use-cases-table">
              <div className="table-header">
                <span className="col col-name">Use Case</span>
                <span className="col col-model">Model</span>
                <span className="col col-latency">Latency</span>
                <span className="col col-rate">Rate</span>
                <span className="col col-standard">Standard</span>
              </div>
              {domain.useCases.map((uc) => (
                <div key={uc.id} className="table-row">
                  <span className="col col-name">
                    <CheckIcon className="row-check" />
                    {uc.name}
                  </span>
                  <span className="col col-model"><code>{uc.model}</code></span>
                  <span className="col col-latency"><code>{uc.latency}</code></span>
                  <span className="col col-rate"><code>{uc.rate}</code></span>
                  <span className="col col-standard"><code>{uc.standard}</code></span>
                </div>
              ))}
            </div>

            <div className="domain-footnote">
              <p>All models execute on DG32-LITE 50 MHz scalar core (12.5 MMAC/s, 16.5 KB budget). Tree ensembles dominate — 0 multiplies, 95–100% accuracy vs deep nets. CORDIC envelope demodulation + Goertzel tone extraction outperform raw moments 4–5×.</p>
            </div>
          </div>
        </Card>
      </motion.div>
    </div>
  );
}

/* === UseCasesAccordion Component === */
export function UseCasesAccordion() {
  return (
    <section id="usecases" className="usecases-section" aria-labelledby="usecases-heading">
      <Container size="wide">
        <div className="usecases-header" style={{ marginBottom: 'var(--space-12)' }}>
          <Reveal delay={0.1}>
            <span className="section-kicker">30 Industrial Use Cases</span>
          </Reveal>
          <Reveal delay={0.2}>
            <h2 id="usecases-heading" className="section-title">
              Edge AI Without an Accelerator — Mathematical Hierarchy Over Capacity
            </h2>
          </Reveal>
          <Reveal delay={0.3}>
            <p className="section-subtitle">
              On a 50 MHz RV32IM scalar core, intelligence comes from signal conditioning, not parameter depth.
              Four domains, 30 production-ready models — all validated against CWRU benchmarks and ISO standards.
            </p>
          </Reveal>
        </div>

        <div className="domains-grid" role="list">
          {useCaseDomains.map((domain, i) => (
            <DomainCard key={domain.id} domain={domain} index={i} />
          ))}
        </div>

        <Reveal className="usecases-cta" style={{ marginTop: 'var(--space-12)', textAlign: 'center' }}>
          <a href="#engineer" className="cta-link">
            View Technical Deep Dive →
            <ChevronRight />
          </a>
        </Reveal>
      </Container>
    </section>
  );
}

/* === CSS for UseCasesAccordion === */
export const useCasesStyles = `
.usecases-section {
  padding: var(--section-padding-y-lg) 0;
  background: var(--color-bg);
}

.usecases-header {
  text-align: center;
  max-width: 56rem;
  margin: 0 auto var(--space-12);
}

.domains-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-5);
}

@media (min-width: 768px) {
  .domains-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .domains-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.domain-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  border-left: 4px solid transparent;
  transition: all var(--transition-base);
}

.domain-card:hover {
  border-left-color: var(--color-accent);
}

.domain-card.open {
  border-left-color: var(--color-accent);
  box-shadow: var(--shadow-lg);
}

.domain-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-3);
}

.domain-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.domain-title-group {
  flex: 1;
  min-width: 0;
}

.domain-title {
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 4px;
}

.domain-subtitle {
  font-size: var(--text-xs);
  color: var(--color-text-dim);
  line-height: 1.4;
}

.domain-meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-shrink: 0;
}

.domain-chevron {
  width: 20px;
  height: 20px;
  color: var(--color-text-dim);
  transition: transform var(--transition-base);
}

.domain-chevron.rotated {
  transform: rotate(180deg);
}

.domain-content {
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border);
}

.use-cases-table {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1.5fr 1fr 1fr 1.5fr;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: var(--color-panel);
  border-radius: var(--radius-md);
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-text-dim);
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1.5fr 1fr 1fr 1.5fr;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
  transition: background var(--transition-fast);
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background: var(--color-panel);
}

.col {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.row-check {
  width: 14px;
  height: 14px;
  color: var(--color-success);
  flex-shrink: 0.
}

.col code {
  font-size: var(--text-xs).
  background: transparent.
  padding: 0.
  color: var(--color-text).
}

.domain-footnote {
  margin-top: var(--space-4).
  padding-top: var(--space-4).
  border-top: 1px solid var(--color-border).
}

.domain-footnote p {
  font-size: var(--text-xs).
  color: var(--color-text-dim).
  line-height: 1.6.
}

.usecases-cta {
  font-size: var(--text-base).
}

.cta-link {
  display: inline-flex.
  align-items: center.
  gap: var(--space-2).
  font-weight: 600.
  color: var(--color-accent).
  padding: var(--space-3) var(--space-6).
  border: 1px solid var(--color-accent).
  border-radius: var(--radius-full).
  transition: all var(--transition-fast).
}

.cta-link:hover {
  background: var(--color-accent).
  color: var(--color-text-inverse).
}

.cta-link svg {
  width: 18px.
  height: 18px.
  transition: transform var(--transition-fast).
}

.cta-link:hover svg {
  transform: translateX(4px).
}

@media (max-width: 768px) {
  .table-header {
    display: none.
  }

  .table-row {
    display: flex.
    flex-direction: column.
    gap: var(--space-1).
    padding: var(--space-3).
  }

  .col {
    display: flex.
    justify-content: space-between.
    align-items: center.
  }

  .col::before {
    content: attr(data-label).
    font-size: var(--text-xs).
    text-transform: uppercase.
    letter-spacing: 0.06em.
    color: var(--color-text-dim).
  }

  .col.col-name::before { content: 'Use Case'; }
  .col.col-model::before { content: 'Model'; }
  .col.col-latency::before { content: 'Latency'; }
  .col.col-rate::before { content: 'Rate'; }
  .col.col-standard::before { content: 'Standard'; }

  .col.col-name {
    justify-content: flex-start.
  }
}
`;