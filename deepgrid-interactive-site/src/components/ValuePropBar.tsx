import { motion, useScroll, useTransform } from 'framer-motion';
import { Container, cn, useRef } from './common';

/* === Value Proposition Bar === */
export function ValuePropBar() {
  const metrics = [
    {
      value: '39-cycle',
      label: 'Fault Isolation',
      detail: 'Hardware lockstep → PWM bridge-off',
      icon: '⚡',
    },
    {
      value: '100 kHz',
      label: 'Deterministic Loop',
      detail: 'CORDIC FOC in 6 µs, zero jitter',
      icon: '🎯',
    },
    {
      value: 'Dual-Foundry',
      label: 'Sovereign Supply',
      detail: 'SkyWater + SCL Mohali, DAP-2020 IDDM',
      icon: '🏭',
    },
    {
      value: '198-day',
      label: 'Tapeout Loop',
      detail: '30d digital sprint + 168d fab window',
      icon: '🔄',
    },
    {
      value: 'Zero',
      label: 'NRE Licensing',
      detail: 'Open EDA (Yosys/OpenROAD) + RISC-V',
      icon: '📜',
    },
    {
      value: '82%',
      label: 'CPU Headroom',
      detail: 'At 10 kHz FOC, 300 cycles fixed HW',
      icon: '📊',
    },
  ];

  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start start', 'end start'],
  });

  const opacity = useTransform(scrollYProgress, [0, 0.15, 0.3], [0, 0.5, 1]);
  const y = useTransform(scrollYProgress, [0, 0.15, 0.3], [40, 20, 0]);

  return (
    <motion.div
      ref={containerRef}
      className="value-prop-bar"
      role="region"
      aria-label="Key value propositions"
      style={{ opacity, y }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
    >
      <Container size="wide">
        <div className="value-prop-grid" role="list">
          {metrics.map((metric, i) => (
            <motion.div
              key={metric.label}
              className="value-prop-item"
              role="listitem"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.08 * i, ease: 'easeOut' }}
            >
              <span className="value-prop-icon" aria-hidden="true">{metric.icon}</span>
              <div className="value-prop-content">
                <span className="value-prop-value">{metric.value}</span>
                <span className="value-prop-label">{metric.label}</span>
                <span className="value-prop-detail">{metric.detail}</span>
              </div>
            </motion.div>
          ))}
        </div>
      </Container>
    </motion.div>
  );
}

/* === CSS for ValuePropBar === */
export const valuePropBarStyles = `
.value-prop-bar {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  background: linear-gradient(180deg, rgba(4, 13, 22, 0.95) 0%, rgba(4, 13, 22, 0.98) 100%);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-5) 0;
  margin-top: calc(var(--space-16) * -1);
}

.value-prop-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
}

@media (min-width: 768px) {
  .value-prop-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .value-prop-grid {
    grid-template-columns: repeat(6, 1fr);
  }
}

.value-prop-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: rgba(16, 38, 58, 0.5);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

.value-prop-item:hover {
  background: rgba(16, 38, 58, 0.8);
  border-color: var(--color-border-strong);
  box-shadow: var(--shadow-md);
}

.value-prop-icon {
  font-size: var(--text-xl);
  line-height: 1;
  filter: drop-shadow(0 0 8px rgba(4, 179, 199, 0.3));
}

.value-prop-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.value-prop-value {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 800;
  color: var(--color-accent);
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.value-prop-label {
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text);
  line-height: 1.3;
}

.value-prop-detail {
  font-size: 10px;
  color: var(--color-text-dim);
  line-height: 1.2;
  max-width: 160px;
}

@media (max-width: 640px) {
  .value-prop-bar {
    padding: var(--space-4) 0;
  }

  .value-prop-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-3);
  }

  .value-prop-item {
    padding: var(--space-3);
  }

  .value-prop-value {
    font-size: var(--text-base);
  }

  .value-prop-detail {
    display: none;
  }
}
`;