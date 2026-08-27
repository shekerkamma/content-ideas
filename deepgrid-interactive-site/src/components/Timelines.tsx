import { motion } from "framer-motion";
import { regulatory, timeline } from "../data";

export function CompetitiveTimeline() {
  return (
    <div className="tl">
      {timeline.map(([when, who, what], i) => (
        <motion.div
          className="tl-item"
          key={`${when}-${who}`}
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-40px" }}
          transition={{ duration: 0.5, delay: i * 0.08, ease: "easeOut" }}
        >
          <motion.span
            className="tl-dot"
            initial={{ scale: 0 }}
            whileInView={{ scale: 1 }}
            viewport={{ once: true }}
            transition={{ type: "spring", stiffness: 300, damping: 18, delay: i * 0.08 }}
          />
          <time>{when}</time>
          <b>{who}</b>
          <p>{what}</p>
        </motion.div>
      ))}
    </div>
  );
}

export function Regulatory() {
  return (
    <div>
      {regulatory.obligations.map(([name, std, new_, all, rule], i) => (
        <motion.div
          className="reg-row"
          key={name}
          initial={{ opacity: 0, x: -16 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-30px" }}
          transition={{ duration: 0.45, delay: i * 0.06, ease: "easeOut" }}
        >
          <b>{name}</b>
          <span className="reg-std">{std}</span>
          <span className="reg-date">{new_}</span>
          <span className="reg-date all">{all}</span>
          <code>{rule}</code>
        </motion.div>
      ))}
      <div className="prop-grid">
        {regulatory.propagators.map(([who, what, ev], i) => (
          <motion.div
            className="prop"
            key={who}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-30px" }}
            transition={{ duration: 0.45, delay: i * 0.06, ease: "easeOut" }}
          >
            <b>{who}</b>
            <p>{what}</p>
            <span>{ev}</span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
