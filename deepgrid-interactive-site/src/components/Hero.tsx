import { motion, useScroll, useTransform, useSpring } from 'framer-motion';
import { Reveal, Counter, ShieldIcon, ZapIcon, LockIcon, ArrowRightIcon, Container, Button, fadeUpChild } from './common';

/* === Hero Section === */
export function Hero() {
  const stats = [
    { n: 39, label: 'Cycle Fault Isolation' },
    { n: 100, label: 'kHz Deterministic Loop', suffix: '+' },
    { n: 2, label: 'Foundry Sovereignty', suffix: '+' },
  ];

  const ease = [0.22, 1, 0.36, 1] as const;

  return (
    <header className="hero" id="hero">
      {/* Background Atmosphere */}
      <div className="hero-atmosphere" aria-hidden="true">
        <motion.div className="orb orb-1" animate={{ x: [-40, 40, -40], y: [0, 20, 0] }} transition={{ duration: 18, repeat: Infinity, ease: 'easeInOut' }} />
        <motion.div className="orb orb-2" animate={{ x: [30, -30, 30], y: [15, -15, 15] }} transition={{ duration: 22, repeat: Infinity, ease: 'easeInOut' }} />
        <motion.div className="orb orb-3" animate={{ x: [0, -25, 0], y: [0, 15, 0] }} transition={{ duration: 26, repeat: Infinity, ease: 'easeInOut' }} />
        <div className="grid-overlay" />
      </div>

      {/* 3D Die Model - Hero Centerpiece */}
      <div className="hero-model" aria-label="DG32 SoC die visualization">
        <div className="die-model-wrapper">
          <div className="die-model" id="die-model">
            <div className="die-core"></div>
            <div className="die-cache"></div>
            <div className="die-periphery"></div>
            <div className="die-io-ring"></div>
            <div className="die-label">DG32</div>
          </div>
          <div className="die-specs">
            <div className="spec-item">
              <span className="spec-value">130nm</span>
              <span className="spec-label">Process</span>
            </div>
            <div className="spec-item">
              <span className="spec-value">15.3mm²</span>
              <span className="spec-label">Die Area</span>
            </div>
            <div className="spec-item">
              <span className="spec-value">50/114</span>
              <span className="spec-label">MHz Dual-Clock</span>
            </div>
          </div>
        </div>
        <motion.div className="scroll-hint" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.5, duration: 1 }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 5v14M19 12l-7 7-7-7" />
          </svg>
          <span>Scroll to explore</span>
        </motion.div>
      </div>

      {/* Content */}
      <div className="hero-content">
        <Container size="narrow">
          <Reveal delay={0.1} y={20}>
            <span className="hero-kicker">DeepGrid Semi · India Sovereign Silicon</span>
          </Reveal>

          <Reveal delay={0.2} y={24}>
            <h1 className="hero-title">
              India's sovereign motor-control silicon.
              <br />
              <span className="accent">Deterministic.</span> Safe. Scalable.
            </h1>
          </Reveal>

          <Reveal delay={0.3} y={24}>
            <p className="hero-subtitle">
              DG32-LITE and DG32-2DOM: dual-core lockstep RISC-V SoCs on 130nm.
              <br />
              First silicon: CI2609 (Sep 2026) & CI2612 (Dec 2026) shuttle slots secured.
            </p>
          </Reveal>

          <Reveal delay={0.4} y={24} className="hero-stats">
            {stats.map((stat, i) => (
              <motion.div key={stat.label} className="stat-card" variants={fadeUpChild} style={{ transitionDelay: `${i * 80}ms` } as React.CSSProperties}>
                <Counter to={stat.n} duration={1.4} />
                <span className="stat-suffix">{stat.suffix || ''}</span>
                <span className="stat-label">{stat.label}</span>
              </motion.div>
            ))}
          </Reveal>

          <Reveal delay={0.6} y={24} className="hero-cta">
            <Button size="xl" leftIcon={<ArrowRightIcon />} className="w-full sm:w-auto">
              Explore the Platform
            </Button>
            <div className="hero-trust">
              <span className="trust-item">
                <ShieldIcon className="trust-icon" />
                <span>DAP-2020 Buy(Indian-IDDM) Compliant</span>
              </span>
              <span className="trust-item">
                <ZapIcon className="trust-icon" />
                <span>198-Day Tapeout Loop</span>
              </span>
              <span className="trust-item">
                <LockIcon className="trust-icon" />
                <span>ISO 26262 ASIL-D Path</span>
              </span>
            </div>
          </Reveal>
        </Container>
      </div>

      {/* Scroll Progress Indicator */}
      <motion.div className="scroll-progress" style={{ position: 'fixed', top: 0, left: 0, right: 0, height: 3, zIndex: 100, transformOrigin: '0 50%', background: 'linear-gradient(90deg, var(--color-accent), #22d3ee)' }} />
    </header>
  );
}

/* CSS for Hero - included via global styles or separate CSS file */
export const heroStyles = `
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(180deg, #061422 0%, #040d16 60%, #040d16 100%);
  border-bottom: 1px solid var(--color-border);
}

.hero-atmosphere {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  pointer-events: none;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle at 30% 30%, rgba(4, 179, 199, 0.25), transparent 70%);
  top: -150px;
  right: -100px;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle at 70% 70%, rgba(6, 182, 212, 0.15), transparent 70%);
  bottom: -150px;
  left: -80px;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle at 50% 50%, rgba(96, 165, 250, 0.1), transparent 70%);
  top: 40%;
  left: 55%;
  opacity: 0.25;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  opacity: 0.04;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(4,179,199,.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(4,179,199,.08) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at 50% 0%, #000 40%, transparent 80%);
}

.hero-model {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12) var(--space-6);
  perspective: 1000px;
}

.die-model-wrapper {
  position: relative;
  width: 320px;
  height: 320px;
}

.die-model {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  animation: dieFloat 8s ease-in-out infinite;
}

@keyframes dieFloat {
  0%, 100% { transform: rotateX(2deg) rotateY(-3deg) translateZ(0); }
  25% { transform: rotateX(1deg) rotateY(2deg) translateZ(10px); }
  50% { transform: rotateX(-1deg) rotateY(-1deg) translateZ(0); }
  75% { transform: rotateX(0.5deg) rotateY(1deg) translateZ(-5px); }
}

.die-model:hover {
  animation-play-state: paused;
}

.die-core {
  position: absolute;
  inset: 20%;
  background: linear-gradient(135deg, #1a3a4a 0%, #0d2835 100%);
  border: 2px solid rgba(4, 179, 199, 0.4);
  border-radius: 8px;
  box-shadow:
    inset 0 0 40px rgba(4, 179, 199, 0.1),
    0 0 60px rgba(4, 179, 199, 0.08);
}

.die-core::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60%;
  height: 60%;
  background: linear-gradient(135deg, rgba(4, 179, 199, 0.15), transparent);
  border-radius: 4px;
}

.die-cache {
  position: absolute;
  top: 10%;
  left: 10%;
  width: 35%;
  height: 35%;
  background: linear-gradient(135deg, #1e3d4a 0%, #102a35 100%);
  border: 1px solid rgba(4, 179, 199, 0.3);
  border-radius: 4px;
  box-shadow: inset 0 0 20px rgba(4, 179, 199, 0.08);
}

.die-periphery {
  position: absolute;
  top: 10%;
  right: 10%;
  width: 35%;
  height: 35%;
  background: linear-gradient(135deg, #1e3d4a 0%, #102a35 100%);
  border: 1px solid rgba(4, 179, 199, 0.3);
  border-radius: 4px;
  box-shadow: inset 0 0 20px rgba(4, 179, 199, 0.08);
}

.die-io-ring {
  position: absolute;
  inset: 4%;
  border: 1px solid rgba(4, 179, 199, 0.2);
  border-radius: 12px;
}

.die-io-ring::before,
.die-io-ring::after {
  content: '';
  position: absolute;
  width: 8px;
  height: 8px;
  background: rgba(4, 179, 199, 0.6);
  border-radius: 2px;
}

.die-io-ring::before { top: -4px; left: 20%; }
.die-io-ring::after { bottom: -4px; right: 20%; }

.die-label {
  position: absolute;
  bottom: -12%;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.2em;
  color: var(--color-accent);
  text-transform: uppercase;
}

.die-specs {
  display: flex;
  justify-content: center;
  gap: var(--space-8);
  margin-top: var(--space-8);
  padding: var(--space-4) var(--space-6);
  background: rgba(16, 38, 58, 0.5);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  backdrop-filter: blur(12px);
}

.spec-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.spec-value {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-accent);
  line-height: 1;
}

.spec-label {
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text-dim);
}

.scroll-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text-dim);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  animation: scrollPulse 2s ease-in-out infinite;
}

@keyframes scrollPulse {
  0%, 100% { opacity: 0.5; transform: translateY(0); }
  50% { opacity: 1; transform: translateY(4px); }
}

.hero-content {
  position: relative;
  z-index: 10;
  padding: var(--space-16) var(--space-6) var(--space-20);
  max-width: 100%;
}

.hero-kicker {
  display: inline-block;
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-accent);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-accent);
}

.hero-title {
  font-size: clamp(2.5rem, 5.5vw, 4.5rem);
  line-height: 1.05;
  font-weight: 800;
  margin-bottom: var(--space-6);
  background: linear-gradient(135deg, #ffffff 0%, #9fd8e2 50%, #60a5fa 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.hero-title .accent {
  background: linear-gradient(135deg, #04b3c7 0%, #22d3ee 100%);
  -webkit-background-clip: text;
  background-clip: text;
}

.hero-subtitle {
  font-size: var(--text-lg);
  line-height: var(--leading-relaxed);
  color: var(--color-text-muted);
  max-width: 60ch;
  margin-bottom: var(--space-8);
}

.hero-subtitle br {
  display: none;
}

@media (min-width: 768px) {
  .hero-subtitle br {
    display: inline;
  }
}

.hero-stats {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-6);
  margin-bottom: var(--space-10);
}

.stat-card {
  flex: 1;
  min-width: 140px;
  max-width: 200px;
  background: rgba(16, 38, 58, 0.7);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5) var(--space-6);
  text-align: center;
}

.stat-card .num {
  display: block;
  font-size: var(--text-3xl);
  font-weight: 800;
  color: var(--color-text);
  font-variant-numeric: tabular-nums;
  line-height: 1;
}

.stat-suffix {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: 800;
  color: var(--color-accent);
  line-height: 1;
}

.stat-label {
  display: block;
  margin-top: var(--space-2);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text-dim);
}

.hero-cta {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-6);
}

@media (min-width: 640px) {
  .hero-cta {
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
  }
}

.hero-trust {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.trust-item {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  padding: var(--space-2) var(--space-4);
  background: rgba(16, 38, 58, 0.5);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  transition: all var(--transition-base);
}

.trust-item:hover {
  border-color: var(--color-accent);
  color: var(--color-text);
}

.trust-icon {
  width: 18px;
  height: 18px;
  color: var(--color-accent);
  flex-shrink: 0;
}

@media (max-width: 1024px) {
  .die-model-wrapper {
    width: 280px;
    height: 280px;
  }

  .die-specs {
    gap: var(--space-6);
  }
}

@media (max-width: 768px) {
  .hero {
    min-height: auto;
    padding-bottom: var(--space-20);
  }

  .hero-model {
    order: -1;
    padding: var(--space-8) var(--space-4);
  }

  .die-model-wrapper {
    width: 260px;
    height: 260px;
  }

  .die-specs {
    flex-wrap: wrap;
    gap: var(--space-4);
  }

  .hero-content {
    padding-top: var(--space-8);
  }

  .hero-title {
    font-size: clamp(2rem, 6vw, 3rem);
  }

  .hero-stats {
    justify-content: center;
  }

  .stat-card {
    min-width: 120px;
  }
}

@media (max-width: 480px) {
  .die-model-wrapper {
    width: 220px;
    height: 220px;
  }

  .die-specs {
    display: none;
  }

  .hero-trust {
    flex-direction: column;
    width: 100%;
  }

  .trust-item {
    width: 100%;
    justify-content: center;
  }
}
`;