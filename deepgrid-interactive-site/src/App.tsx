import { motion, useScroll, useSpring } from "framer-motion";
import { useCallback, useEffect, useState, type ReactNode } from "react";
import { companies, execaction, patterns, pyramid, regulatory, supplierside, TIER_META, type Tier } from "./data";
import { CHAPTERS, type ChapterId } from "./chapters";
import { WebMCPTools } from "./WebMCPTools";
import { RemoteMCPBridge } from "./RemoteMCPBridge";
import { Hero } from "./components/Hero";
import { ScaleChart } from "./components/ScaleChart";
import { RelationshipMap } from "./components/RelationshipMap";
import { RankingChart } from "./components/RankingChart";
import { CompetitiveTimeline, Regulatory } from "./components/Timelines";
import { CertTable, SupplierTable } from "./components/Tables";
import { CompanyExplorer } from "./components/CompanyExplorer";
import { ExecAction, HostileAccordion, Posture } from "./components/Cards";
import {
  BuildBuy, Countermoves, Differentjob, Displacement, Donotcompete, Execcompare,
  Lifecycle, Narrativecounter, OneProgramme, Pricing, Reshape, Silicon, ThreatArena,
  Universe, Valuenet,
} from "./components/analytic";
import { Reveal, fadeUpChild, staggerParent } from "./components/common";

function ActuationSplit() {
  const tiers: Tier[] = ["P-ACT", "P-WARN", "P-ADJ"];
  return (
    <motion.div className="mode-grid" initial="hidden" whileInView="show" viewport={{ once: true, margin: "-40px" }} variants={staggerParent}>
      {tiers.map((t) => {
        const meta = TIER_META[t];
        const list = companies.filter((c) => c.tier === t);
        return (
          <motion.article className="mode" key={t} style={{ borderTop: `3px solid ${meta.color}` }} variants={fadeUpChild}>
            <h4 style={{ color: meta.color }}>{t} · {meta.label}</h4>
            <div className="mode-who">{meta.note}</div>
            <ul className="mode-list" style={{ color: meta.color }}>
              {list.map((c) => (
                <li key={c.id}>{c.name}</li>
              ))}
            </ul>
          </motion.article>
        );
      })}
    </motion.div>
  );
}

function SectionHead({ kicker, title, sub }: { kicker: string; title: string; sub?: string }) {
  return (
    <Reveal className="ch-head">
      <span className="ch-kicker">{kicker}</span>
      <h2>{title}</h2>
      {sub && <p className="ch-sub">{sub}</p>}
    </Reveal>
  );
}

function Block({ children, title }: { children: ReactNode; title: string }) {
  return (
    <>
      <h3 className="block">{title}</h3>
      {children}
    </>
  );
}

export default function App() {
  const [active, setActive] = useState<ChapterId>("verdict");
  const [selectedCompany, setSelectedCompany] = useState(companies[0].id);
  const [openQuestion, setOpenQuestion] = useState<number | null>(null);
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

  const showCompany = useCallback((companyId: string) => {
    setSelectedCompany(companyId);
  }, []);

  const showQuestion = useCallback((questionIndex: number) => {
    setOpenQuestion(questionIndex);
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
      <WebMCPTools
        onNavigateSection={navigateToSection}
        onShowCompany={showCompany}
        onShowQuestion={showQuestion}
      />
      <RemoteMCPBridge />
      <motion.div className="progress" style={{ scaleX, position: "fixed", top: 0, left: 0, right: 0, height: 3, zIndex: 100, transformOrigin: "0 50%", background: "linear-gradient(90deg, var(--accent), #60a5fa)" }} />

      <Hero />

      <nav className="top" aria-label="Chapters">
        {CHAPTERS.map((ch) => (
          <a key={ch.id} href={`#${ch.id}`} className={active === ch.id ? "active" : ""}>
            {ch.label}
          </a>
        ))}
      </nav>

      <main>
        {/* ── Act I · Verdict ── */}
        <section className="chapter" id="verdict">
          <SectionHead kicker="Act I · The verdict" title="The argument in one shape" sub="Lead with the answer, then the three supports that hold it up." />
          <div className="pyr">
            <Reveal className="gov"><b>{pyramid.governing_thought}</b></Reveal>
            <motion.div className="supports" initial="hidden" whileInView="show" viewport={{ once: true, margin: "-40px" }} variants={staggerParent}>
              {pyramid.supports.map((s) => (
                <motion.div className="sup" key={s.claim} variants={fadeUpChild}>
                  <b>{s.claim}</b>
                  <p>{s.because}</p>
                  <span>{s.proof}</span>
                </motion.div>
              ))}
            </motion.div>
          </div>
          <Block title="The field spans four orders of magnitude">
            <ScaleChart />
            <p className="ch-sub" style={{ color: "var(--muted)", fontSize: 13, marginTop: 12 }}>
              Bar length is log₁₀ of USD value. On a linear axis the bottom half of this market is invisible — which is the point.
            </p>
          </Block>
        </section>

        {/* ── Act II · The field ── */}
        <section className="chapter" id="field">
          <SectionHead kicker="Act II · The field" title="Two markets, one mandate clock" sub="CMVR rule 96(12) obliges AEBS — a system that brakes. A system that only warns cannot satisfy it at any price." />
          <ActuationSplit />

          <Block title="The competitive universe — one direct fight, three routes to market">
            <Universe />
          </Block>

          <Block title="Every competitor, its evidence boundary, and the move it implies">
            <Execcompare />
          </Block>

          <Block title="The Value Net — a company can be customer and rival at once">
            <Valuenet />
          </Block>

          <Block title="The notified instrument — and who still cites the draft">
            <div className="pyr"><Reveal className="gov" style={{ borderLeftColor: "#1BA271" }}><b>{regulatory.instrument}</b><p>{regulatory.superseded}</p></Reveal></div>
            <Regulatory />
          </Block>

          <Block title="Certification, not capability, is the gate">
            <CertTable />
          </Block>

          <Block title="Supply dependency — the seat-holder owns no silicon at all">
            <Silicon />
          </Block>

          <Block title="Eight months, seven competitive moves">
            <CompetitiveTimeline />
          </Block>

          <Block title="An unresolved question — Aptiv's win and STRADVISION's win may be one programme">
            <OneProgramme />
          </Block>
        </section>

        {/* ── Act III · The contest ── */}
        <section className="chapter" id="contest">
          <SectionHead kicker="Act III · The contest" title={patterns.title} sub={patterns.sub} />
          <RelationshipMap />

          <Block title="STRADVISION holds the slot — the displacement plan">
            <Displacement />
          </Block>

          <Block title="Three companies that are not in the same bid — note and leave">
            <Differentjob />
          </Block>

          <Block title="Two companies compete for the indigenous-champion story — counter the claim">
            <Narrativecounter />
          </Block>

          <Block title="Threat × arena — rated only within the substitute row">
            <ThreatArena />
          </Block>

          <Block title="Who each of the nine actually is">
            <CompanyExplorer active={selectedCompany} onActiveChange={setSelectedCompany} />
          </Block>

          <Block title="The companies that set the cost floor are not on the map">
            <SupplierTable />
          </Block>
        </section>

        {/* ── Act IV · The ranking ── */}
        <section className="chapter" id="ranking">
          <SectionHead kicker="Act IV · The ranking" title="The re-derived ranking — execution × access × leverage" sub="Weights: leverage 45% · access 35% · execution 20%. A company is dangerous when it owns something DeepGrid must pass through." />
          <RankingChart />

          <Block title="What this changes — a market map wearing a dossier's clothes">
            <Reshape />
          </Block>

          <Block title="What they do when we start winning">
            <Countermoves />
          </Block>

          <Block title="Four contests to lose deliberately">
            <Donotcompete />
          </Block>
        </section>

        {/* ── Act V · The wedge ── */}
        <section className="chapter" id="wedge">
          <SectionHead kicker="Act V · The wedge" title="Compete in one arena, attach in another, refuse the full-stack fight" sub="Every mode carries the boundary that keeps it bounded." />
          <Posture />

          <Block title="Four rivals keep earning after the sale — DeepGrid stops at the invoice">
            <Lifecycle />
          </Block>

          <Block title="Buy the certification, partner the homologation, build only the perception">
            <BuildBuy />
          </Block>

          <Block title="No competitor's India unit price is quotable — say so before you are asked">
            <Pricing />
          </Block>
        </section>

        {/* ── Act VI · The plan ── */}
        <section className="chapter" id="plan">
          <SectionHead kicker="Act VI · The plan" title={execaction.title} sub={execaction.sub} />
          <ExecAction />
          <p style={{ color: "#e0a3a3", fontSize: 14, marginTop: 20 }}>
            <b>Do not fund:</b> {execaction.donotfund}
          </p>
        </section>

        {/* ── Appendix ── */}
        <section className="chapter" id="appendix">
          <SectionHead kicker="Appendix · The rest of the field" title="Six questions this deck must survive" sub="The hostile questions — and the answers that hold." />
          <HostileAccordion open={openQuestion} onOpenChange={setOpenQuestion} />
        </section>

        <footer className="legend">
          <span><i className="dot" style={{ background: "#1BA271" }} />Verified / evidenced</span>
          <span><i className="dot" style={{ background: "#D7720B" }} />Attributed / company-claimed</span>
          <span><i className="dot" style={{ background: "#E06767" }} />Contested / unverified</span>
          <span>Native animated data story · {companies.length} competitors · evidence ledger EV-*</span>
        </footer>
      </main>
    </>
  );
}
