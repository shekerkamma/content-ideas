import { motion } from "framer-motion";
import { companies, coreMessage, EVIDENCE_ROWS, scqa } from "../data";
import { Counter } from "./common";

const stats = [
  { n: companies.length, label: "Competitors" },
  { n: 4, label: "Control points" },
  { n: 7, label: "Moves in 8 months" },
  { n: EVIDENCE_ROWS, label: "Evidence rows" },
];

const ease = [0.22, 1, 0.36, 1] as const;

export function Hero() {
  return (
    <header className="mast">
      <motion.div className="orb orb-a" animate={{ x: [-20, 20, -20], y: [0, 16, 0] }} transition={{ duration: 14, repeat: Infinity, ease: "easeInOut" }} />
      <motion.div className="orb orb-b" animate={{ x: [16, -16, 16], y: [10, -10, 10] }} transition={{ duration: 18, repeat: Infinity, ease: "easeInOut" }} />
      <motion.div className="orb orb-c" animate={{ x: [0, -24, 0], y: [0, 12, 0] }} transition={{ duration: 22, repeat: Infinity, ease: "easeInOut" }} />
      <div className="grid-overlay" />
      <div className="mast-inner">
        <motion.div className="kicker" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, ease }}>
          DeepGrid Semi · India ADAS Competitor Dossier · Confidential
        </motion.div>
        <motion.h1 initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.08, ease }}>
          {coreMessage}
        </motion.h1>
        <motion.p className="sub" initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.18, ease }}>
          <b>Situation.</b> {scqa.situation}
          <br />
          <b>Complication.</b> {scqa.complication}
          <br />
          <b style={{ color: "#04b3c7" }}>Answer.</b> {scqa.answer}
        </motion.p>
        <motion.div className="stats" initial="hidden" animate="show" variants={{ hidden: {}, show: { transition: { staggerChildren: 0.08, delayChildren: 0.3 } } }}>
          {stats.map((s) => (
            <motion.div className="stat" key={s.label} variants={{ hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0, transition: { duration: 0.5, ease } } }}>
              <Counter to={s.n} />
              <span className="lbl">{s.label}</span>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </header>
  );
}
