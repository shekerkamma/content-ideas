import { motion, useScroll, useSpring } from "framer-motion";
import { useCallback, useEffect, useState } from "react";
import { Hero } from "./components/Hero";
import { ValuePropBar } from "./components/ValuePropBar";
import { Pillars } from "./components/Pillars";
import { VerificationLadder } from "./components/VerificationLadder";
import { ProcurementScorecard } from "./components/ProcurementScorecard";
import { UseCasesAccordion } from "./components/UseCasesAccordion";
import { MediaProof } from "./components/MediaProof";
import { PersonaTabs } from "./components/PersonaTabs";
import { ProductPortfolio } from "./components/ProductPortfolio";
import { TrustFooter } from "./components/TrustFooter";
import { Reveal } from "./components/common";

/* Chapter IDs for scroll spy */
const CHAPTERS = [
  { id: 'hero', label: 'Overview' },
  { id: 'pillars', label: 'Pillars' },
  { id: 'verification', label: 'Verification' },
  { id: 'procurement', label: 'Procurement' },
  { id: 'usecases', label: 'Use Cases' },
  { id: 'media', label: 'Media' },
  { id: 'personas', label: 'Deep Dives' },
  { id: 'portfolio', label: 'Portfolio' },
  { id: 'footer', label: 'Contact' },
] as const;

type ChapterId = typeof CHAPTERS[number]['id'];

export default function App() {
  const [active, setActive] = useState<ChapterId>("hero");
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, { stiffness: 100, damping: 30, restDelta: 0.001 });

  const navigateToSection = useCallback((section: ChapterId) => {
    const element = document.getElementById(section);
    if (element) {
      const root = document.documentElement;
      const previousScrollBehavior = root.style.scrollBehavior;
      root.style.scrollBehavior = "auto";
      element.scrollIntoView({ behavior: "auto", block: "start" });
      root.style.scrollBehavior = previousScrollBehavior;
    }
    setActive(section);
  }, []);

  useEffect(() => {
    const onScroll = () => {
      let cur: ChapterId = CHAPTERS[0].id;
      for (const ch of CHAPTERS) {
        const el = document.getElementById(ch.id);
        if (el && el.getBoundingClientRect().top <= 140) cur = ch.id;
      }
      setActive(cur);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <>
      {/* Scroll Progress Bar */}
      <motion.div
        className="scroll-progress"
        style={{
          scaleX,
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          height: 3,
          zIndex: 100,
          transformOrigin: "0 50%",
          background: "linear-gradient(90deg, var(--color-accent), #22d3ee)",
        }}
      />

      {/* Skip Link for Accessibility */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      {/* Hero Section */}
      <Hero />

      {/* Value Proposition Bar (Sticky) */}
      <ValuePropBar />

      {/* Sticky Navigation */}
      <nav className="top" aria-label="Sections" role="navigation">
        {CHAPTERS.map((ch) => (
          <a
            key={ch.id}
            href={`#${ch.id}`}
            className={active === ch.id ? "active" : ""}
            onClick={(e) => {
              e.preventDefault();
              navigateToSection(ch.id);
            }}
          >
            {ch.label}
          </a>
        ))}
      </nav>

      <main id="main-content" role="main">
        {/* Pillars Section */}
        <Pillars />

        {/* Verification Ladder */}
        <VerificationLadder />

        {/* Procurement Scorecard */}
        <ProcurementScorecard />

        {/* Use Cases Accordion */}
        <UseCasesAccordion />

        {/* Media Proof */}
        <MediaProof />

        {/* Persona Deep Dives */}
        <PersonaTabs />

        {/* Product Portfolio */}
        <ProductPortfolio />

        {/* Trust Footer */}
        <TrustFooter />
      </main>
    </>
  );
}