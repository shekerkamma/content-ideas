import { Reveal, Button, Container, cn, GithubIcon, LinkedinIcon, MailIcon, DownloadIcon, CalendarIcon, ExternalLinkIcon, ShieldIcon, ZapIcon, LockIcon, GlobeIcon, CpuIcon, Badge } from './common';
import { motion } from 'framer-motion';

/* === TrustFooter Component === */
export function TrustFooter() {
  return (
    <footer id="footer" className="trust-footer" role="contentinfo">
      <Container size="wide">
        {/* Compliance Badges */}
        <div className="footer-section compliance-section" style={{ marginBottom: 'var(--space-16)' }}>
          <Reveal delay={0.1}>
            <h3 className="footer-section-title">Compliance & Standards</h3>
          </Reveal>
          <Reveal delay={0.2}>
            <div className="compliance-grid" role="list">
              {complianceItems.map((item, i) => (
                <motion.div
                  key={item.name}
                  role="listitem"
                  className={cn('compliance-badge', item.status === 'verified' && 'verified', item.status === 'in-progress' && 'in-progress')}
                  initial={{ opacity: 0, y: 16 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: '-50px' }}
                  transition={{ duration: 0.3, delay: 0.03 * i, ease: [0.22, 1, 0.36, 1] }}
                >
                  <Badge
                    variant={item.status === 'verified' ? 'verified' : item.status === 'in-progress' ? 'accent' : 'planned'}
                    size="sm"
                    className="compliance-status"
                  >
                    {item.status === 'verified' ? '✓ Verified' : item.status === 'in-progress' ? '◑ In Progress' : '◐ Planned'}
                  </Badge>
                  <span className="compliance-name">{item.name}</span>
                  <span className="compliance-skus">{item.skus}</span>
                </motion.div>
              ))}
            </div>
          </Reveal>
        </div>

        {/* Anchor Customers */}
        <div className="footer-section anchors-section" style={{ marginBottom: 'var(--space-16)' }}>
          <Reveal delay={0.1}>
            <h3 className="footer-section-title">Anchor Customers & Partners</h3>
          </Reveal>
          <Reveal delay={0.2}>
            <div className="anchors-grid" role="list">
              {anchorCustomers.map((anchor, i) => (
                <motion.div
                  key={anchor.name}
                  role="listitem"
                  className="anchor-card"
                  initial={{ opacity: 0, y: 16 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: '-50px' }}
                  transition={{ duration: 0.3, delay: 0.05 * i, ease: [0.22, 1, 0.36, 1] }}
                >
                  <span className="anchor-name">{anchor.name}</span>
                  <span className="anchor-role">{anchor.role}</span>
                  <span className="anchor-sku">{anchor.sku}</span>
                </motion.div>
              ))}
            </div>
          </Reveal>
        </div>

        {/* Primary CTA */}
        <div className="footer-section cta-section" style={{ marginBottom: 'var(--space-16)', textAlign: 'center' }}>
          <Reveal delay={0.1}>
            <h3 className="footer-section-title">Ready to Evaluate?</h3>
          </Reveal>
          <Reveal delay={0.2}>
            <p className="cta-description">
              Start your evaluation journey. We'll route you to the right technical resources, reference designs, and support tier.
            </p>
          </Reveal>
          <Reveal delay={0.3}>
            <div className="cta-buttons">
              <Button size="xl" leftIcon={<ShieldIcon />} variant="primary" className="primary-cta">
                Start Evaluation
              </Button>
              <Button size="lg" leftIcon={<DownloadIcon />} variant="outline">
                Download Master Whitepaper (71 pages)
              </Button>
              <Button size="lg" leftIcon={<CalendarIcon />} variant="ghost">
                Schedule Technical Call
              </Button>
              <Button size="lg" leftIcon={<GithubIcon />} variant="ghost">
                View SDK on GitHub
              </Button>
            </div>
          </Reveal>
        </div>

        {/* Secondary CTAs */}
        <div className="footer-section secondary-ctas" style={{ marginBottom: 'var(--space-16)' }}>
          <Reveal>
            <div className="secondary-grid">
              <a href="#investor" className="secondary-card">
                <span className="secondary-icon">
                  <ShieldIcon />
                </span>
                <div>
                  <span className="secondary-title">Investor Data Room</span>
                  <span className="secondary-desc">Financial model, cap table, stop rules, stress tests</span>
                </div>
                <ExternalLinkIcon />
              </a>
              <a href="#engineer" className="secondary-card">
                <span className="secondary-icon">
                  <CpuIcon />
                </span>
                <div>
                  <span className="secondary-title">Engineer Deep Dive</span>
                  <span className="secondary-desc">Architecture, register maps, SDK, pinout, thermal</span>
                </div>
                <ExternalLinkIcon />
              </a>
              <a href="#procurement" className="secondary-card">
                <span className="secondary-icon">
                  <GlobeIcon />
                </span>
                <div>
                  <span className="secondary-title">Procurement Hub</span>
                  <span className="secondary-desc">BOM comparison, qualification tracker, PIL mapping</span>
                </div>
                <ExternalLinkIcon />
              </a>
              <a href="#partner" className="secondary-card">
                <span className="secondary-icon">
                  <ZapIcon />
                </span>
                <div>
                  <span className="secondary-title">Partner Program</span>
                  <span className="secondary-desc">Reference designs, support SLAs, training, certification</span>
                </div>
                <ExternalLinkIcon />
              </a>
            </div>
          </Reveal>
        </div>

        {/* Footer Bottom */}
        <div className="footer-bottom">
          <div className="footer-brand">
            <div className="brand-logo">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <rect width="32" height="32" rx="7" fill="#04b3c7" />
                <text x="16" y="22" font-family="sans-serif" font-size="15" font-weight="700" fill="#04131d" text-anchor="middle">DG</text>
              </svg>
            </div>
            <p className="brand-tagline">India's sovereign motor-control silicon. Deterministic. Safe. Scalable.</p>
          </div>

          <nav className="footer-links" aria-label="Footer navigation">
            <div className="link-group">
              <h4>Product</h4>
              <a href="#portfolio">Portfolio</a>
              <a href="#engineer">Technical Deep Dive</a>
              <a href="#usecases">Use Cases</a>
              <a href="#media">Architecture Films</a>
            </div>
            <div className="link-group">
              <h4>Company</h4>
              <a href="#investor">Investor Relations</a>
              <a href="#procurement">Procurement</a>
              <a href="#partner">Partner Program</a>
              <a href="mailto:contact@deepgrid.in">Contact</a>
            </div>
            <div className="link-group">
              <h4>Resources</h4>
              <a href="#" download>Master Whitepaper</a>
              <a href="#" download>SKU Datasheets</a>
              <a href="#" download>Qualification Reports</a>
              <a href="https://github.com/deepgrid" target="_blank" rel="noopener">GitHub</a>
            </div>
            <div className="link-group">
              <h4>Legal</h4>
              <a href="#">Privacy Policy</a>
              <a href="#">Terms of Use</a>
              <a href="#">Export Compliance</a>
              <a href="#">IP Notice</a>
            </div>
          </nav>

          <div className="footer-social">
            <a href="https://github.com/deepgrid" target="_blank" rel="noopener" aria-label="GitHub" className="social-link">
              <GithubIcon />
            </a>
            <a href="https://linkedin.com/company/deepgrid" target="_blank" rel="noopener" aria-label="LinkedIn" className="social-link">
              <LinkedinIcon />
            </a>
            <a href="mailto:contact@deepgrid.in" aria-label="Email" className="social-link">
              <MailIcon />
            </a>
          </div>
        </div>

        {/* Copyright */}
        <div className="footer-copyright">
          <p>© 2026 DeepGrid Semi Pvt Ltd. Hyderabad, India. All rights reserved.</p>
          <p className="copyright-note">
            DG32-LITE (CI2609) & DG32-2DOM (CI2612) — SkyWater 130nm shuttle slots secured.
            <br />
            This page contains forward-looking statements. See <a href="#">Risk Factors</a>.
          </p>
        </div>
      </Container>
    </footer>
  );
}

/* === Compliance Data === */
const complianceItems = [
  { name: 'DAP-2020 Buy(Indian)', status: 'verified', skus: 'All SKUs' },
  { name: 'DAP-2020 Buy(Indian-IDDM)', status: 'in-progress', skus: 'Defence SKUs (SCL Mohali)' },
  { name: 'PIL-1 through PIL-5', status: 'verified', skus: 'Chips 1, 3, 7, 8 mapped' },
  { name: 'SRIJAN NSG-5962', status: 'verified', skus: 'Chip 3 (28V PMIC)' },
  { name: 'ISO 26262 ASIL-D', status: 'in-progress', skus: 'Chip 4 (Lockstep MCU)' },
  { name: 'IEC 61508 SIL-3', status: 'in-progress', skus: 'Chip 4 (Lockstep MCU)' },
  { name: 'DO-160G / MIL-STD-461', status: 'in-progress', skus: 'Chips 3, 7, 8' },
  { name: 'MIL-STD-883K', status: 'in-progress', skus: 'Chip 6 (Pathfinder)' },
  { name: 'AEC-Q100 Grade 0/1', status: 'in-progress', skus: 'Chips 1, 4, 5, 9' },
  { name: 'CEMILAC', status: 'in-progress', skus: 'Chips 7, 8 (Avionics)' },
];

/* === Anchor Customers === */
const anchorCustomers = [
  { name: 'Airgap Technology', role: 'EV Powertrain OEM', sku: 'Chip 1 (BLDC Motor)' },
  { name: 'Ripple Metering', role: 'Smart Meter Operator (250M)', sku: 'Chip 2 (Smart Meter SoC)' },
  { name: 'MCEME / Indian Army', role: 'Defence Anchor (₹1.01 Cr)', sku: 'Chip 4 (Lockstep MCU)' },
  { name: 'Chakravayu CPDL', role: 'Drone Platform Anchor', sku: 'D100 Drone SoC' },
  { name: 'Infinis Agritech', role: 'Precision Agriculture (₹1.25 Cr)', sku: 'FPGA Prototype Systems' },
  { name: 'Axitech Solar', role: 'Tracker Controllers (₹0.62 Cr)', sku: 'FPGA Prototype Systems' },
  { name: 'BEL Defence Electronics', role: 'PSU — Display, EW, Radar', sku: 'Chips 3, 7, 8 (PIL)' },
  { name: 'SkyWater Technology', role: 'Foundry Partner (USA)', sku: '130nm sky130' },
  { name: 'IHP Leibniz Institute', role: 'Foundry Partner (Germany)', sku: 'SG13G2 SiGe 77GHz' },
  { name: 'SCL Mohali', role: 'Foundry Partner (India)', sku: '180nm Sovereign Defence' },
];

/* === CSS for TrustFooter === */
export const footerStyles = `
.trust-footer {
  background: var(--color-bg-elevated);
  border-top: 1px solid var(--color-border);
  padding: var(--space-20) 0 var(--space-12);
  margin-top: var(--space-20);
}

.footer-section-title {
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--space-8);
  text-align: center;
}

/* Compliance Grid */
.compliance-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
  max-width: 72rem;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .compliance-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .compliance-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}

.compliance-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  text-align: center;
  transition: all var(--transition-base);
}

.compliance-badge.verified {
  border-color: var(--color-success);
  background: var(--color-success-muted);
}

.compliance-badge.in-progress {
  border-color: var(--color-accent);
  background: var(--color-accent-muted);
}

.compliance-badge:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.compliance-status {
  font-weight: 700;
}

.compliance-name {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.3;
}

.compliance-skus {
  font-size: 10px;
  color: var(--color-text-dim);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* Anchors Grid */
.anchors-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-3);
  max-width: 72rem;
  margin: 0 auto;
}

@media (min-width: 640px) {
  .anchors-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .anchors-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}

.anchor-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: var(--space-4);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  text-align: center;
  transition: all var(--transition-base);
}

.anchor-card:hover {
  border-color: var(--color-accent);
  box-shadow: var(--shadow-md);
}

.anchor-name {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.3;
}

.anchor-role {
  font-size: var(--text-xs);
  color: var(--color-accent);
  font-weight: 500;
}

.anchor-sku {
  font-size: 10px;
  color: var(--color-text-dim);
  font-family: var(--font-mono);
}

/* CTA Section */
.cta-description {
  font-size: var(--text-base);
  color: var(--color-text-muted);
  max-width: 48rem;
  margin: 0 auto var(--space-8);
}

.cta-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  justify-content: center;
}

.primary-cta {
  box-shadow: var(--shadow-lg);
}

.primary-cta:hover {
  box-shadow: var(--shadow-xl);
}

/* Secondary CTAs */
.secondary-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
  max-width: 72rem;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .secondary-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.secondary-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-3);
  padding: var(--space-5);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  color: var(--color-text);
  text-decoration: none;
  transition: all var(--transition-base);
}

.secondary-card:hover {
  border-color: var(--color-accent);
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}

.secondary-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: var(--color-accent-muted);
  color: var(--color-accent);
  display: flex;
  align-items: center;
  justify-content: center;
}

.secondary-icon svg {
  width: 24px;
  height: 24px;
}

.secondary-title {
  font-size: var(--text-base);
  font-weight: 700;
  color: var(--color-text);
}

.secondary-desc {
  font-size: var(--text-xs);
  color: var(--color-text-dim);
  line-height: 1.4;
}

.secondary-card svg:last-child {
  width: 20px;
  height: 20px;
  color: var(--color-text-dim);
  margin-top: auto;
}

/* Footer Bottom */
.footer-bottom {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-12);
  padding-top: var(--space-12);
  border-top: 1px solid var(--color-border);
  margin-top: var(--space-8);
}

@media (min-width: 768px) {
  .footer-bottom {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
  }
}

.footer-brand {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  text-align: center;
  max-width: 20rem;
}

@media (min-width: 768px) {
  .footer-brand {
    align-items: flex-start;
    text-align: left;
  }
}

.brand-tagline {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  line-height: 1.5;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-10);
  flex: 1;
  justify-content: center;
}

@media (min-width: 768px) {
  .footer-links {
    justify-content: flex-end;
  }
}

.link-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  min-width: 140px;
}

.link-group h4 {
  font-size: var(--text-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-dim);
  margin-bottom: var(--space-2);
}

.link-group a {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  transition: color var(--transition-fast);
}

.link-group a:hover {
  color: var(--color-accent);
}

.footer-social {
  display: flex;
  gap: var(--space-4);
}

.social-link {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.social-link:hover {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: var(--color-text-inverse);
}

.social-link svg {
  width: 20px;
  height: 20px;
}

/* Copyright */
.footer-copyright {
  width: 100%;
  text-align: center;
  padding-top: var(--space-8);
  border-top: 1px solid var(--color-border);
  margin-top: var(--space-8);
}

.footer-copyright p {
  font-size: var(--text-sm);
  color: var(--color-text-dim);
  margin-bottom: var(--space-2);
}

.copyright-note {
  font-size: var(--text-xs) !important;
  color: var(--color-text-dim) !important;
  line-height: 1.6;
}

.copyright-note a {
  color: var(--color-accent);
}

@media (max-width: 768px) {
  .compliance-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .anchors-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }

  .cta-buttons button {
    width: 100%;
    justify-content: center;
  }

  .secondary-grid {
    grid-template-columns: 1fr;
  }

  .footer-links {
    display: none;
  }
}
`;