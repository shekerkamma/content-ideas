import { AnimatePresence, motion } from "framer-motion";
import { execaction, hostileQuestions, posture } from "../data";

export function Posture() {
  return (
    <motion.div
      className="mode-grid"
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, margin: "-40px" }}
      variants={{ hidden: {}, show: { transition: { staggerChildren: 0.08 } } }}
    >
      {posture.modes.map(([verb, who, color, why, boundary]) => (
        <motion.article
          className="mode"
          key={verb}
          style={{ borderTop: `3px solid ${color}` }}
          variants={{ hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0, transition: { duration: 0.55, ease: "easeOut" } } }}
          whileHover={{ y: -5 }}
        >
          <h4 style={{ color }}>{verb}</h4>
          <div className="mode-who">{who}</div>
          <p className="mode-why">{why}</p>
          <p className="mode-b">{boundary}</p>
        </motion.article>
      ))}
    </motion.div>
  );
}

export function ExecAction() {
  return (
    <motion.div
      className="exec-grid"
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, margin: "-40px" }}
      variants={{ hidden: {}, show: { transition: { staggerChildren: 0.1 } } }}
    >
      {execaction.rows.map(([num, verb, act, gate, owner]) => (
        <motion.article
          className="exec"
          key={num}
          variants={{ hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0, transition: { duration: 0.55, ease: "easeOut" } } }}
        >
          <span className="exec-no">{num}</span>
          <h4>{verb}</h4>
          <p>{act}</p>
          <div className="exec-gate">
            <b>Proof gate</b>
            {gate}
          </div>
          <span className="exec-owner">{owner}</span>
        </motion.article>
      ))}
    </motion.div>
  );
}

interface HostileAccordionProps {
  open: number | null;
  onOpenChange: (questionIndex: number | null) => void;
}

export function HostileAccordion({ open, onOpenChange }: HostileAccordionProps) {
  return (
    <div>
      {hostileQuestions.map(([q, a], i) => (
        <div className={`hq ${open === i ? "open" : ""}`} key={i}>
          <button className="hq-q" onClick={() => onOpenChange(open === i ? null : i)} aria-expanded={open === i}>
            <span>{q}</span>
            <span className="chev">+</span>
          </button>
          <AnimatePresence initial={false}>
            {open === i && (
              <motion.div
                className="hq-a"
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3, ease: "easeOut" }}
              >
                <p>{a}</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      ))}
    </div>
  );
}
