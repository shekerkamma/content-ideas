import { Reveal, Card, Badge, Button, Container, cn, PlayIcon, ExternalLink } from './common';
import { motion } from 'framer-motion';
import { useState } from 'react';

/* === Media Data === */
const films = [
  {
    id: 'film-1',
    title: 'The 198-Day Silicon Loop',
    subtitle: 'Automated RTL-to-GDSII flow, MPW economics, three-factory sovereignty',
    duration: '12 min',
    poster: '/assets/film-1-poster.jpg',
    videoUrl: 'https://www.youtube.com/watch?v=QhmhUgccaS0&t=10s',
    chapters: [
      { time: '0:00', title: 'Introduction: The $9B Import Funnel' },
      { time: '2:30', title: 'Open-Source EDA: 10x Cost Reduction' },
      { time: '5:15', title: 'The 198-Day Loop: 30d Design + 168d Fab' },
      { time: '8:00', title: 'Three-Factory Sovereignty: SkyWater → IHP → SCL' },
      { time: '11:00', title: 'Call to Action: Join the Movement' },
    ],
  },
  {
    id: 'film-2',
    title: 'Deterministic Control in 6 µs',
    subtitle: 'FOC hardware pipeline, CORDIC engine, lockstep safety, 100 kHz bandwidth',
    duration: '10 min',
    poster: '/assets/film-2-poster.jpg',
    videoUrl: 'https://www.youtube.com/watch?v=QhmhUgccaS0&t=10s',
    chapters: [
      { time: '0:00', title: 'Why Determinism Matters for Motor Control' },
      { time: '1:45', title: 'FOC Pipeline Breakdown: 300 Cycles Fixed' },
      { time: '4:20', title: 'CORDIC Engine: sin/cos/atan2 in 53–58 Cycles' },
      { time: '6:30', title: 'Lockstep Safety: 39-Cycle Fault-to-Bridge-Off' },
      { time: '9:00', title: 'Roadmap: 200 MHz ASIC, 50 kHz Loops' },
    ],
  },
];

const miniCards = [
  {
    id: 'dg32-lite-datasheet',
    title: 'DG32-LITE Datasheet',
    subtitle: '50 MHz scalar · CORDIC · 32 KB SRAM · 30 use cases',
    type: 'datasheet',
    color: '#04b3c7',
    link: '/datasheets/DG32-LITE.pdf',
  },
  {
    id: 'dg32-2dom-datasheet',
    title: 'DG32-2DOM Datasheet',
    subtitle: '50/114 MHz dual-clock · INT8 attention · 47K-param AVIP',
    type: 'datasheet',
    color: '#60a5fa',
    link: '/datasheets/DG32-2DOM.pdf',
  },
  {
    id: 'tapein-confirmation',
    title: 'Tape-In Confirmation',
    subtitle: 'CI2609 (Sep 16 2026) + CI2612 (Dec 7 2026) — slots secured',
    type: 'confirmation',
    color: '#1ba271',
    link: '/docs/tapein-confirmation.pdf',
  },
];

/* === FilmCard Component === */
function FilmCard({ film }: { film: typeof films[0] }) {
  const [isHovered, setIsHovered] = useState(false);
  const [showModal, setShowModal] = useState(false);

  return (
    <Card variant="interactive" padding="none" className="film-card">
      <div className="film-poster" style={{ backgroundImage: `url(${film.poster})` }}>
        <div className="film-overlay" style={{ opacity: isHovered ? 1 : 0 }}>
          <Button
            variant="primary"
            size="lg"
            leftIcon={<PlayIcon />}
            onClick={(e) => { e.stopPropagation(); setShowModal(true); }}
          >
            Watch Film
          </Button>
        </div>
        <div className="film-duration">{film.duration}</div>
        <div className="film-play-hint" style={{ opacity: isHovered ? 0 : 1 }}>
          <PlayIcon />
          <span>Click to play</span>
        </div>
      </div>
      <div className="film-info">
        <Badge variant="accent" size="sm" className="film-badge">Film</Badge>
        <h3 className="film-title">{film.title}</h3>
        <p className="film-subtitle">{film.subtitle}</p>
        <Button
          variant="ghost"
          size="sm"
          rightIcon={<ExternalLink />}
          onClick={(e) => { e.stopPropagation(); window.open(film.videoUrl, '_blank'); }}
        >
          View on YouTube
        </Button>
      </div>

      {showModal && (
        <FilmModal film={film} onClose={() => setShowModal(false)} />
      )}
    </Card>
  );
}

/* === FilmModal Component === */
function FilmModal({ film, onClose }: { film: typeof films[0]; onClose: () => void }) {
  return (
    <motion.div className="film-modal-backdrop" onClick={onClose} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
      <motion.div className="film-modal" onClick={(e: React.MouseEvent) => e.stopPropagation()} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
        <button className="modal-close" onClick={onClose} aria-label="Close modal">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
        <div className="modal-video">
          <iframe
            src={film.videoUrl.replace('watch?v=', 'embed/')}
            title={film.title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>
        <div className="modal-info">
          <h3>{film.title}</h3>
          <p>{film.subtitle}</p>
          <div className="modal-chapters">
            <h4>Chapters</h4>
            <ul>
              {film.chapters.map((ch, i) => (
                <li key={i}>
                  <span className="chapter-time">{ch.time}</span>
                  <span className="chapter-title">{ch.title}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

/* === MiniCard Component === */
function MiniCard({ card }: { card: typeof miniCards[0] }) {
  return (
    <Card variant="interactive" padding="md" className="mini-card">
      <div className="mini-card-icon" style={{ background: `${card.color}20`, color: card.color }}>
        {card.type === 'datasheet' ? (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
            <polyline points="10 9 9 9 8 9" />
          </svg>
        ) : (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </svg>
        )}
      </div>
      <div className="mini-card-content">
        <Badge variant="accent" size="sm">{card.type === 'datasheet' ? 'Datasheet' : 'Confirmation'}</Badge>
        <h3 className="mini-card-title">{card.title}</h3>
        <p className="mini-card-subtitle">{card.subtitle}</p>
      </div>
      <Button
        variant="outline"
        size="sm"
        rightIcon={<ExternalLink />}
        className="mini-card-btn"
        onClick={(e) => { e.stopPropagation(); window.open(card.link, '_blank'); }}
      >
        Download
      </Button>
    </Card>
  );
}

/* === MediaProof Component === */
export function MediaProof() {
  return (
    <section id="media" className="media-section" aria-labelledby="media-heading">
      <Container size="wide">
        <div className="media-header" style={{ marginBottom: 'var(--space-12)' }}>
          <Reveal delay={0.1}>
            <span className="section-kicker">Media Proof</span>
          </Reveal>
          <Reveal delay={0.2}>
            <h2 id="media-heading" className="section-title">
              Architecture Films & Technical Documentation
            </h2>
          </Reveal>
          <Reveal delay={0.3}>
            <p className="section-subtitle">
              Two deep-dive architecture films and three technical documents — all evidence-backed, all accessible.
            </p>
          </Reveal>
        </div>

        {/* Films Carousel */}
        <div className="films-section" style={{ marginBottom: 'var(--space-16)' }}>
          <Reveal>
            <h3 className="subsection-title">Architecture Films</h3>
          </Reveal>
          <div className="films-grid" role="list">
            {films.map((film, i) => (
              <motion.div
                key={film.id}
                role="listitem"
                className="film-wrapper"
                initial={{ opacity: 0, y: 24 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-50px' }}
                transition={{ duration: 0.5, delay: 0.1 + i * 0.1, ease: [0.22, 1, 0.36, 1] }}
              >
                <FilmCard film={film} />
              </motion.div>
            ))}
          </div>
        </div>

        {/* Mini Cards */}
        <div className="mini-cards-section">
          <Reveal>
            <h3 className="subsection-title">Technical Documents</h3>
          </Reveal>
          <div className="mini-cards-grid" role="list">
            {miniCards.map((card, i) => (
              <motion.div
                key={card.id}
                role="listitem"
                className="mini-card-wrapper"
                initial={{ opacity: 0, y: 24 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-50px' }}
                transition={{ duration: 0.5, delay: 0.1 + i * 0.1, ease: [0.22, 1, 0.36, 1] }}
              >
                <MiniCard card={card} />
              </motion.div>
            ))}
          </div>
        </div>
      </Container>
    </section>
  );
}

/* === CSS for MediaProof === */
export const mediaStyles = `
.media-section {
  padding: var(--section-padding-y-lg) 0;
  background: var(--color-bg);
}

.media-header {
  text-align: center;
  max-width: 56rem;
  margin: 0 auto var(--space-12);
}

.subsection-title {
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--space-8);
  text-align: center;
}

/* Films */
.films-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-6);
}

@media (min-width: 1024px) {
  .films-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.film-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.film-poster {
  position: relative;
  aspect-ratio: 16 / 9;
  background-size: cover;
  background-position: center;
  background-color: var(--color-panel);
}

.film-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(4,13,22,0.6) 0%, rgba(4,13,22,0.9) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
  transition: opacity var(--transition-base);
}

.film-duration {
  position: absolute;
  bottom: var(--space-3);
  right: var(--space-3);
  background: rgba(0,0,0,0.8);
  color: white;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.film-play-hint {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  color: rgba(255,255,255,0.7);
  font-size: var(--text-sm);
  transition: opacity var(--transition-base);
}

.film-play-hint svg {
  width: 48px;
  height: 48px;
}

.film-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: var(--space-5);
}

.film-badge {
  align-self: flex-start;
}

.film-title {
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text);
}

.film-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  line-height: 1.5;
}

/* Mini Cards */
.mini-cards-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
}

@media (min-width: 640px) {
  .mini-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .mini-cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.mini-card {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  height: 100%;
}

.mini-card-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.mini-card-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mini-card-title {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--color-text);
}

.mini-card-subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.mini-card-btn {
  flex-shrink: 0;
}

/* Modal */
.film-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.9);
  backdrop-filter: blur(8px);
  z-index: var(--z-modal);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.film-modal {
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-close {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  z-index: 10;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: rgba(4,13,22,0.9);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.modal-close:hover {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: var(--color-text-inverse);
}

.modal-video {
  aspect-ratio: 16 / 9;
  background: #000;
}

.modal-video iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.modal-info {
  padding: var(--space-6);
}

.modal-info h3 {
  font-size: var(--text-xl);
  font-weight: 700;
  margin-bottom: var(--space-2);
}

.modal-info p {
  color: var(--color-text-muted);
  margin-bottom: var(--space-6);
}

.modal-chapters h4 {
  font-size: var(--text-sm);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-dim);
  margin-bottom: var(--space-3);
}

.modal-chapters ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.modal-chapters li {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: var(--color-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
}

.chapter-time {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--color-accent);
  min-width: 60px;
}

.chapter-title {
  color: var(--color-text);
}

@media (max-width: 768px) {
  .film-modal {
    max-height: 100vh;
    border-radius: 0;
    max-width: 100%;
  }

  .modal-info {
    padding: var(--space-4);
  }
}
`;