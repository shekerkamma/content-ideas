import { Reveal, Badge, Card, Button, Container, cn, ArrowRightIcon, ExternalLink, ChevronDown, CheckIcon } from './common';
import { motion } from 'framer-motion';
import { useState } from 'react';

/* === Product Data === */
interface Product {
  id: string;
  name: string;
  category: 'Commercial' | 'Defence' | 'Track B' | 'Platform';
  status: string;
  node: string;
  keySpecs: string[];
  highlights: string[];
  anchor: string;
  asp: string;
  tam: string;
  color: string;
  badge: string;
}

const products: Product[] = [
  {
    id: 'dg32-lite',
    name: 'DG32-LITE',
    category: 'Commercial',
    status: 'Taped Out (CI2609)',
    node: '130nm SkyWater',
    keySpecs: ['50 MHz RV32IM', '32 KB SRAM', 'CORDIC Engine', '7-ch PWM', '16-bit ADC×3'],
    highlights: ['FOC <1 µs', '30 AI use cases', 'Zero NRE licensing'],
    anchor: 'Airgap, Infinis, Axitech',
    asp: '$3–8',
    tam: '5–15M/yr',
    color: '#04b3c7',
    badge: 'Production Track',
  },
  {
    id: 'dg32-2dom',
    name: 'DG32-2DOM',
    category: 'Commercial',
    status: 'Taped Out (CI2612)',
    node: '130nm SkyWater',
    keySpecs: ['50/114 MHz Dual-Clock', 'Lockstep RV32IM', 'INT8 Attention', '32 KB SRAM', 'SAR ADC'],
    highlights: ['39-cycle fault-off', '47K-param AVIP', 'DShot bidirectional'],
    anchor: 'MCEME (Army)',
    asp: '$4–12',
    tam: '3–10M/yr',
    color: '#60a5fa',
    badge: 'Production Track',
  },
  {
    id: 'pmic',
    name: '28V Hi-Rel PMIC',
    category: 'Defence',
    status: 'Design Complete',
    node: '180nm SCL / SkyWater',
    keySpecs: ['28V input', 'Brokaw 12ppm/°C', 'DO-160 / MIL-STD-461', '4 sequenced rails', 'TMR/DICE latches'],
    highlights: ['Radiation tolerant', 'SRIJAN NSG-5962', 'BEL tank DC-DC'],
    anchor: 'BEL, SRIJAN',
    asp: '$50–200',
    tam: '10–50k/yr',
    color: '#d7720b',
    badge: 'Defence Track',
  },
  {
    id: 'lockstep',
    name: 'Lockstep ASIL-D MCU',
    category: 'Defence',
    status: 'Design Complete',
    node: '130nm SkyWater / SCL',
    keySpecs: ['Dual RV32IM', '2-cycle skew', 'End-to-end ECC', 'ISO 26262 ASIL-D', '2× CAN-FD'],
    highlights: ['≤2-cycle comparator', 'Async brake ≤2 cycles', 'EV BMS, drone autopilot'],
    anchor: 'MCEME',
    asp: '$4–12',
    tam: '3–10M/yr',
    color: '#d7720b',
    badge: 'Defence Track',
  },
  {
    id: 'transceiver',
    name: 'Interface Transceiver',
    category: 'Commercial',
    status: 'Design Complete',
    node: '130nm 5V Ring',
    keySpecs: ['RS-485 + CAN-FD', '±15 kV HBM ESD', '5V thick-oxide I/O', '130nm CMOS'],
    highlights: ['High-attach industrial', 'Discontinued bus IC replacement', '20–60M units/yr'],
    anchor: 'Industrial OEMs',
    asp: '$0.40–1.50',
    tam: '20–60M/yr',
    color: '#04b3c7',
    badge: 'Volume Track',
  },
  {
    id: 'supervisor',
    name: 'Voltage Supervisor',
    category: 'Defence',
    status: 'Design Complete',
    node: '130/180nm',
    keySpecs: ['Quad-rail', 'Chopper comparator', '8 µs deglitch', 'MIL-STD-883 pathfinder'],
    highlights: ['Simplest SKU', 'Pathfinder for screening', '30–80M units/yr'],
    anchor: 'Qualification learning',
    asp: '$0.20–0.80',
    tam: '30–80M/yr',
    color: '#1ba271',
    badge: 'Pathfinder',
  },
  {
    id: 'radar',
    name: '77 GHz 4D Radar',
    category: 'Defence',
    status: 'Planned',
    node: 'IHP SG13G2 SiGe + 130nm CMOS',
    keySpecs: ['2TX / 4RX', '350 GHz fT HBTs', '3.75 cm resolution', 'DO-160G airborne'],
    highlights: ['Su-30/Mi-17 RWR', 'ADAS automotive', 'Split SiGe/CMOS architecture'],
    anchor: 'HAL/IAF, ADAS',
    asp: '$35–60/set',
    tam: '2–8M/yr',
    color: '#60a5fa',
    badge: 'Radar Track',
  },
  {
    id: 'display',
    name: 'HV Display Driver',
    category: 'Defence',
    status: 'Design Complete',
    node: '130nm HV (0–12V)',
    keySpecs: ['1280×10b DACs', 'BEL 17" SXGA', 'PIL-5 direct match', 'TCON integration'],
    highlights: ['Rugged cockpit display', 'PIL-5 Item #5', '2–6M units/yr'],
    anchor: 'BEL Defence',
    asp: '$70–110',
    tam: '2–6M/yr',
    color: '#d7720b',
    badge: 'Defence Track',
  },
  {
    id: 'zonal',
    name: 'SDV Zonal Gateway',
    category: 'Commercial',
    status: 'Design Complete',
    node: '130nm CMOS',
    keySpecs: ['16× Smart e-Fuses', 'Gigabit TSN', 'CAN-XL', 'EVITA-Full HSM', 'ASIL-D island'],
    highlights: ['Software-Defined Vehicles', 'EV platforms', '4–12M units/yr'],
    anchor: 'EV OEMs',
    asp: '$6–20',
    tam: '4–12M/yr',
    color: '#04b3c7',
    badge: 'Auto Track',
  },
  {
    id: 'd100',
    name: 'D100 Drone SoC',
    category: 'Track B',
    status: 'Separate Round',
    node: 'TSMC 28nm',
    keySpecs: ['PX4 loop + 30Hz EKF VIO', 'HW Failsafe Island', 'DGCA Type Cert', '64-bit compute'],
    highlights: ['Chakravayu CPDL', 'ideaForge platforms', '100–300k units/yr'],
    anchor: 'Chakravayu, ideaForge',
    asp: '$60–100',
    tam: '100–300k/yr',
    color: '#a78bfa',
    badge: 'Track B',
  },
  {
    id: 'dg-sdv',
    name: 'DG SDV Platform',
    category: 'Platform',
    status: 'Design Phase',
    node: '28nm + 130/180nm SiP',
    keySpecs: ['64-bit AXI4 Matrix', 'AXI-REALM QoS', 'Triple-Lockstep Safe Domain', 'RV64 Linux'],
    highlights: ['Multi-die organic SiP', 'EVITA-Full HSM', 'ISO 26262 ASIL-D'],
    anchor: 'SDV OEMs',
    asp: 'Platform',
    tam: 'Platform',
    color: '#fb7185',
    badge: 'Platform',
  },
];

const categoryFilters = ['All', 'Commercial', 'Defence', 'Track B', 'Platform'];
const viewModes = ['Grid', 'Table', 'Timeline'];

/* === ProductCard Component === */
function ProductCard({ product }: { product: Product }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Card variant="interactive" padding="lg" className={cn('product-card', isOpen && 'open')} onClick={() => setIsOpen(!isOpen)}>
      <div className="product-header">
        <div className="product-icon" style={{ background: `${product.color}20`, color: product.color } as React.CSSProperties}>
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <rect x="4" y="4" width="16" height="16" rx="2" />
            <path d="M9 4v4M15 4v4M9 16v4M15 16v4" />
            <path d="M4 9h4M4 15h4M16 9h4M16 15h4" />
          </svg>
        </div>
        <div className="product-badges">
          <Badge variant="accent" size="sm" style={{ '--badge-color': product.color } as React.CSSProperties}>{product.badge}</Badge>
          <Badge variant={product.category === 'Defence' ? 'contested' : 'planned'} size="sm">{product.category}</Badge>
        </div>
      </div>

      <h3 className="product-name">{product.name}</h3>
      <p className="product-status">{product.status} · {product.node}</p>

      <div className="product-specs">
        <h4>Key Specs</h4>
        <ul>
          {product.keySpecs.map((spec, i) => (
            <li key={i}><CheckIcon className="spec-check" style={{ color: product.color }} /> {spec}</li>
          ))}
        </ul>
      </div>

      <div className="product-highlights">
        <h4>Highlights</h4>
        <ul>
          {product.highlights.map((hl, i) => (
            <li key={i}><CheckIcon className="spec-check" style={{ color: product.color }} /> {hl}</li>
          ))}
        </ul>
      </div>

      <div className="product-meta">
        <div className="meta-item">
          <span className="meta-label">Anchor</span>
          <span className="meta-value">{product.anchor}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">ASP</span>
          <span className="meta-value">{product.asp}</span>
        </div>
        <div className="meta-item">
          <span className="meta-label">TAM</span>
          <span className="meta-value">{product.tam}</span>
        </div>
      </div>

      <Button variant="outline" size="sm" rightIcon={<ArrowRightIcon />} className="product-cta w-full" onClick={(e) => { e.stopPropagation(); setIsOpen(!isOpen); }}>
        {isOpen ? 'Collapse' : 'View Details'}
      </Button>

      {/* Modal */}
      {isOpen && (
        <ProductModal product={product} onClose={() => setIsOpen(false)} />
      )}
    </Card>
  );
}

/* === ProductModal Component === */
function ProductModal({ product, onClose }: { product: Product; onClose: () => void }) {
  return (
    <motion.div className="product-modal-backdrop" onClick={onClose} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <motion.div className="product-modal" onClick={(e: React.MouseEvent) => e.stopPropagation()} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
        <button className="modal-close" onClick={onClose} aria-label="Close">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        <div className="modal-header" style={{ borderLeft: `4px solid ${product.color}` }}>
          <div>
            <Badge variant="accent" size="sm" style={{ '--badge-color': product.color } as React.CSSProperties}>{product.badge}</Badge>
            <Badge variant={product.category === 'Defence' ? 'contested' : 'planned'} size="sm" style={{ marginLeft: 'var(--space-2)' }}>{product.category}</Badge>
            <h2 style={{ marginTop: 'var(--space-3)' }}>{product.name}</h2>
            <p className="modal-status">{product.status} · {product.node}</p>
          </div>
        </div>

        <div className="modal-content">
          <div className="modal-section">
            <h3>Key Specifications</h3>
            <ul className="spec-list">
              {product.keySpecs.map((spec, i) => (
                <li key={i}><CheckIcon className="spec-check" style={{ color: product.color }} /> {spec}</li>
              ))}
            </ul>
          </div>

          <div className="modal-section">
            <h3>Highlights</h3>
            <ul className="spec-list">
              {product.highlights.map((hl, i) => (
                <li key={i}><CheckIcon className="spec-check" style={{ color: product.color }} /> {hl}</li>
              ))}
            </ul>
          </div>

          <div className="modal-meta">
            <div className="meta-item">
              <span className="meta-label">Anchor Customer</span>
              <span className="meta-value">{product.anchor}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Target ASP</span>
              <span className="meta-value">{product.asp}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Target TAM</span>
              <span className="meta-value">{product.tam}</span>
            </div>
          </div>

          <div className="modal-actions">
            <Button variant="outline" leftIcon={<ExternalLink />}>View Datasheet</Button>
            <Button variant="outline" leftIcon={<ExternalLink />}>Pinout PDF</Button>
            <Button variant="outline" leftIcon={<ExternalLink />}>Register Map</Button>
            <Button variant="outline" leftIcon={<ExternalLink />}>Thermal Model</Button>
            <Button variant="primary" leftIcon={<ArrowRightIcon />}>Start Evaluation</Button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

/* === ProductTableRow Component === */
function ProductTableRow({ product }: { product: Product }) {
  return (
    <motion.tr
      className="product-table-row"
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ duration: 0.3 }}
    >
      <td>
        <div className="table-product-info">
          <span className="table-product-icon" style={{ background: `${product.color}20`, color: product.color } as React.CSSProperties}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="4" y="4" width="16" height="16" rx="2" />
              <path d="M9 4v4M15 4v4M9 16v4M15 16v4" />
              <path d="M4 9h4M4 15h4M16 9h4M16 15h4" />
            </svg>
          </span>
          <div>
            <span className="table-product-name">{product.name}</span>
            <span className="table-product-category">{product.category}</span>
          </div>
        </div>
      </td>
      <td><Badge variant={product.status.includes('Taped') ? 'verified' : product.status.includes('Design') ? 'planned' : 'accent'} size="sm">{product.status}</Badge></td>
      <td><code>{product.node}</code></td>
      <td>{product.keySpecs.slice(0, 2).join(', ')}<span className="more-specs"> +{product.keySpecs.length - 2} more</span></td>
      <td>{product.anchor}</td>
      <td><code>{product.asp}</code></td>
      <td><code>{product.tam}</code></td>
      <td>
        <Button variant="ghost" size="sm" onClick={(e) => e.stopPropagation()}>Details</Button>
      </td>
    </motion.tr>
  );
}

/* === ProductPortfolio Component === */
export function ProductPortfolio() {
  const [activeFilter, setActiveFilter] = useState('All');
  const [viewMode, setViewMode] = useState<'grid' | 'table' | 'timeline'>('grid');

  const filteredProducts = activeFilter === 'All'
    ? products
    : products.filter(p => p.category === activeFilter);

  return (
    <section id="portfolio" className="portfolio-section" aria-labelledby="portfolio-heading">
      <Container size="wide">
        <div className="portfolio-header" style={{ marginBottom: 'var(--space-12)' }}>
          <Reveal delay={0.1}>
            <span className="section-kicker">Product Portfolio</span>
          </Reveal>
          <Reveal delay={0.2}>
            <h2 id="portfolio-heading" className="section-title">
              11 SKUs + Platform — One Method, Three Factories
            </h2>
          </Reveal>
          <Reveal delay={0.3}>
            <p className="section-subtitle">
              Commercial volume first (Chips 1,2), defence pathfinder next (Chip 6), high-margin monopoly last (Chips 3,4,7,8).
              Filter by category, switch views, click any card for full specs.
            </p>
          </Reveal>
        </div>

        {/* Controls */}
        <div className="portfolio-controls" role="group" aria-label="Portfolio filters and views">
          <div className="filter-group">
            <label htmlFor="category-filter" className="visually-hidden">Filter by category</label>
            <select
              id="category-filter"
              value={activeFilter}
              onChange={(e) => setActiveFilter(e.target.value)}
              className="filter-select"
            >
              {categoryFilters.map(cat => <option key={cat} value={cat}>{cat}</option>)}
            </select>
          </div>
          <div className="view-group" role="radiogroup" aria-label="View mode">
            {viewModes.map(mode => (
              <button
                key={mode}
                role="radio"
                aria-checked={viewMode === mode.toLowerCase()}
                className={cn('view-btn', viewMode === mode.toLowerCase() && 'active')}
                onClick={() => setViewMode(mode.toLowerCase() as 'grid' | 'table' | 'timeline')}
              >
                {mode}
              </button>
            ))}
          </div>
        </div>

        {/* Grid View */}
        <div className="portfolio-grid" role="list" style={{ display: viewMode === 'grid' ? 'grid' : 'none' }}>
          {filteredProducts.map((product, i) => (
            <motion.div
              key={product.id}
              role="listitem"
              className="product-wrapper"
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-50px' }}
              transition={{ duration: 0.4, delay: 0.05 * i, ease: [0.22, 1, 0.36, 1] }}
            >
              <ProductCard product={product} />
            </motion.div>
          ))}
        </div>

        {/* Table View */}
        <div className="portfolio-table-wrapper" role="region" aria-label="Product comparison table" style={{ display: viewMode === 'table' ? 'block' : 'none' }}>
          <table className="portfolio-table">
            <thead>
              <tr>
                <th scope="col">Product</th>
                <th scope="col">Status</th>
                <th scope="col">Node</th>
                <th scope="col">Key Specs</th>
                <th scope="col">Anchor</th>
                <th scope="col">ASP</th>
                <th scope="col">TAM</th>
                <th scope="col"></th>
              </tr>
            </thead>
            <tbody>
              {filteredProducts.map((product, i) => (
                <motion.tr
                  key={product.id}
                  initial={{ opacity: 0, y: 16 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: '-50px' }}
                  transition={{ duration: 0.3, delay: 0.03 * i }}
                >
                  <ProductTableRow product={product} />
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Timeline View */}
        <div className="portfolio-timeline" style={{ display: viewMode === 'timeline' ? 'block' : 'none' }}>
          <div className="timeline-phases">
            <TimelinePhase
              title="Cycle 1: Commercial Volume Launch"
              subtitle="Cash flow & factory credibility"
              products={products.filter(p => p.id === 'dg32-lite' || p.id === 'dg32-2dom')}
              color="#04b3c7"
            />
            <TimelinePhase
              title="Cycle 2: Pathfinder Screening"
              subtitle="Low-risk qualification learning"
              products={products.filter(p => p.id === 'supervisor')}
              color="#1ba271"
            />
            <TimelinePhase
              title="Cycle 3+: High-Margin Defence"
              subtitle="Monopoly pricing behind PIL barriers"
              products={products.filter(p => ['pmic', 'lockstep', 'radar', 'display'].includes(p.id))}
              color="#d7720b"
            />
            <TimelinePhase
              title="Track B & Platform"
              subtitle="Separate compute round + SiP integration"
              products={products.filter(p => p.id === 'd100' || p.id === 'dg-sdv')}
              color="#a78bfa"
            />
          </div>
        </div>

        {/* Sequencing Note */}
        <Reveal className="sequencing-note">
          <details>
            <summary>Sequencing Strategy: Why This Order?</summary>
            <div className="sequencing-content">
              <p><strong>Cycle 1 (CI2609):</strong> Chip 1 (Motor) + Chip 2 (Meter) → Commercial volume establishes tapeout track record and cash flow.</p>
              <p><strong>Cycle 2 (CI2612):</strong> Chip 6 (Supervisor) → Simplest SKU acts as MIL-STD-883 pathfinder, uncovers screening bottlenecks early.</p>
              <p><strong>Cycle 3+:</strong> Chips 3, 4, 7, 8 on proven silicon → Defence monopoly pricing (10x–100x commercial ASP) behind PIL import bans.</p>
              <p><strong>Track B (Separate):</strong> D100 Drone SoC on TSMC 28nm — completely ring-fenced from mature-node seed round.</p>
              <p><strong>Platform:</strong> DG SDV Reference Platform — 64-bit AXI4 crossbar + organic SiP integration of mature dies + 28nm compute.</p>
            </div>
          </details>
        </Reveal>
      </Container>
    </section>
  );
}

/* === TimelinePhase Component === */
function TimelinePhase({ title, subtitle, products, color }: { title: string; subtitle: string; products: Product[]; color: string }) {
  return (
    <div className="timeline-phase">
      <div className="phase-marker" style={{ background: color }} />
      <div className="phase-content">
        <div className="phase-header">
          <h3 className="phase-title">{title}</h3>
          <p className="phase-subtitle">{subtitle}</p>
        </div>
        <div className="phase-products">
          {products.map(p => (
            <span key={p.id} className="phase-product" style={{ borderColor: color }}>
              {p.name}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

/* === CSS for ProductPortfolio === */
export const portfolioStyles = `
.portfolio-section {
  padding: var(--section-padding-y-lg) 0;
  background: var(--color-bg);
}

.portfolio-header {
  text-align: center;
  max-width: 56rem;
  margin: 0 auto var(--space-12);
}

.portfolio-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: var(--space-6);
  margin-bottom: var(--space-12);
  padding: var(--space-4) var(--space-6);
  background: var(--color-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
}

.filter-group, .view-group {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.filter-select {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%238ea0b2' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right var(--space-3) center;
  padding-right: var(--space-10);
}

.filter-select:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-muted);
}

.view-btn {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-text-muted);
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.view-btn:hover {
  color: var(--color-text);
  background: var(--color-card);
}

.view-btn.active {
  color: var(--color-text-inverse);
  background: var(--color-accent);
  border-color: var(--color-accent);
}

/* Grid View */
.portfolio-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-5);
}

@media (min-width: 768px) {
  .portfolio-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .portfolio-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1440px) {
  .portfolio-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.product-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  overflow: visible;
}

.product-card.open {
  z-index: 10;
  box-shadow: var(--shadow-xl);
}

.product-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.product-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.product-badges {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  justify-content: flex-end;
}

.product-name {
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 4px;
}

.product-status {
  font-size: var(--text-xs);
  color: var(--color-text-dim);
  margin-bottom: var(--space-4);
}

.product-specs, .product-highlights {
  margin-bottom: var(--space-4);
}

.product-specs h4, .product-highlights h4 {
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-accent);
  margin-bottom: var(--space-2);
}

.product-specs ul, .product-highlights ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.product-specs li, .product-highlights li {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  line-height: 1.4;
}

.spec-check {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
  margin-top: 1px;
}

.product-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-top: auto;
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border);
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 80px;
}

.meta-label {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-text-dim);
}

.meta-value {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-text);
}

.product-cta {
  margin-top: var(--space-4);
  justify-content: center;
}

/* Table View */
.portfolio-table-wrapper {
  overflow-x: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background: var(--color-card);
}

.portfolio-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}

.portfolio-table th,
.portfolio-table td {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.portfolio-table th {
  background: var(--color-panel);
  font-weight: 700;
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-dim);
  position: sticky;
  top: 0;
  z-index: 1.
}

.portfolio-table tr:last-child td {
  border-bottom: none.
}

.table-product-info {
  display: flex.
  align-items: center.
  gap: var(--space-3).
}

.table-product-icon {
  width: 32px.
  height: 32px.
  border-radius: var(--radius-md).
  display: flex.
  align-items: center.
  justify-content: center.
}

.table-product-name {
  display: block.
  font-weight: 600.
  color: var(--color-text).
}

.table-product-category {
  display: block.
  font-size: var(--text-xs).
  color: var(--color-text-dim).
}

.more-specs {
  display: inline-block.
  margin-left: var(--space-2).
  font-size: var(--text-xs).
  color: var(--color-text-dim).
}

.product-table-row:hover td {
  background: var(--color-panel).
}

/* Timeline View */
.portfolio-timeline {
  max-width: 72rem.
  margin: 0 auto.
}

.timeline-phases {
  display: flex.
  flex-direction: column.
  gap: var(--space-8).
  position: relative.
}

.timeline-phases::before {
  content: ''.
  position: absolute.
  left: 28px.
  top: 0.
  bottom: 0.
  width: 2px.
  background: linear-gradient(180deg, var(--color-border), var(--color-accent), var(--color-border)).
}

.timeline-phase {
  display: flex.
  gap: var(--space-6).
  position: relative.
}

.phase-marker {
  width: 16px.
  height: 16px.
  border-radius: 50%.
  flex-shrink: 0.
  margin-top: 4px.
  box-shadow: 0 0 0 4px var(--color-bg), 0 0 0 6px var(--color-border).
  z-index: 1.
}

.phase-content {
  flex: 1.
  padding-top: var(--space-2).
}

.phase-header {
  margin-bottom: var(--space-3).
}

.phase-title {
  font-size: var(--text-lg).
  font-weight: 700.
  color: var(--color-text).
  margin-bottom: 4px.
}

.phase-subtitle {
  font-size: var(--text-sm).
  color: var(--color-text-muted).
}

.phase-products {
  display: flex.
  flex-wrap: wrap.
  gap: var(--space-2).
}

.phase-product {
  padding: var(--space-1) var(--space-3).
  font-size: var(--text-sm).
  font-weight: 500.
  color: var(--color-text).
  background: var(--color-panel).
  border: 1px solid var(--color-border).
  border-radius: var(--radius-full).
  border-left-width: 3px.
  transition: all var(--transition-fast).
}

.phase-product:hover {
  border-color: currentColor.
  color: var(--color-text).
}

/* Sequencing Note */
.sequencing-note {
  margin-top: var(--space-12).
  text-align: center.
}

.sequencing-note summary {
  cursor: pointer.
  font-weight: 600.
  color: var(--color-accent).
  padding: var(--space-3).
  display: inline-flex.
  align-items: center.
  gap: var(--space-2).
  list-style: none.
}

.sequencing-note summary::-webkit-details-marker { display: none; }

.sequencing-note summary::after {
  content: ''.
  width: 12px.
  height: 12px.
  border-right: 2px solid currentColor.
  border-bottom: 2px solid currentColor.
  transform: rotate(45deg).
  transition: transform var(--transition-fast).
}

.sequencing-note[open] summary::after {
  transform: rotate(-135deg).
}

.sequencing-content {
  margin-top: var(--space-6).
  padding: var(--space-6).
  background: var(--color-panel).
  border: 1px solid var(--color-border).
  border-radius: var(--radius-lg).
  text-align: left.
  font-size: var(--text-sm).
  color: var(--color-text-muted).
  line-height: 1.8.
}

.sequencing-content p {
  margin-bottom: var(--space-3).
}

.sequencing-content p:last-child {
  margin-bottom: 0.
}

/* Modal */
.product-modal-backdrop {
  position: fixed.
  inset: 0.
  background: rgba(0,0,0,0.8).
  backdrop-filter: blur(8px).
  z-index: var(--z-modal).
  display: flex.
  align-items: center.
  justify-content: center.
  padding: var(--space-6).
  animation: fadeIn 0.2s ease-out.
}

.product-modal {
  width: 100%.
  max-width: 600px.
  max-height: 90vh.
  background: var(--color-card).
  border: 1px solid var(--color-border).
  border-radius: var(--radius-xl).
  overflow: hidden.
  display: flex.
  flex-direction: column.
  animation: slideUp 0.3s ease-out.
}

.modal-close {
  position: absolute.
  top: var(--space-4).
  right: var(--space-4).
  z-index: 10.
  width: 40px.
  height: 40px.
  border-radius: var(--radius-full).
  background: rgba(4,13,22,0.9).
  border: 1px solid var(--color-border).
  color: var(--color-text).
  display: flex.
  align-items: center.
  justify-content: center.
  cursor: pointer.
  transition: all var(--transition-fast).
}

.modal-close:hover {
  background: var(--color-accent).
  border-color: var(--color-accent).
  color: var(--color-text-inverse).
}

.modal-header {
  padding: var(--space-6).
  border-bottom: 1px solid var(--color-border).
}

.modal-status {
  font-size: var(--text-sm).
  color: var(--color-text-muted).
  margin-top: var(--space-1).
}

.modal-content {
  padding: var(--space-6).
  overflow-y: auto.
  flex: 1.
}

.modal-section {
  margin-bottom: var(--space-6).
}

.modal-section h3 {
  font-size: var(--text-sm).
  font-weight: 700.
  text-transform: uppercase.
  letter-spacing: 0.08em.
  color: var(--color-accent).
  margin-bottom: var(--space-3).
}

.spec-list {
  list-style: none.
  display: flex.
  flex-direction: column.
  gap: var(--space-2).
}

.spec-list li {
  display: flex.
  align-items: flex-start.
  gap: var(--space-2).
  font-size: var(--text-sm).
  color: var(--color-text-muted).
}

.modal-meta {
  display: grid.
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)).
  gap: var(--space-4).
  padding: var(--space-4).
  background: var(--color-panel).
  border: 1px solid var(--color-border).
  border-radius: var(--radius-lg).
  margin-bottom: var(--space-6).
}

.modal-actions {
  display: flex.
  flex-wrap: wrap.
  gap: var(--space-3).
  justify-content: center.
}

@media (max-width: 768px) {
  .portfolio-controls {
    flex-direction: column.
    align-items: stretch.
  }

  .filter-group, .view-group {
    justify-content: center.
  }

  .portfolio-table th,
  .portfolio-table td {
    padding: var(--space-2) var(--space-3).
  }

  .timeline-phases::before {
    left: 20px.
  }

  .phase-marker {
    width: 12px.
    height: 12px.
  }
}
`;