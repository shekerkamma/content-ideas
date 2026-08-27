import { motion } from "framer-motion";
import { SCALE } from "../data";

const LO = 5.5;
const HI = 10.8;

export function ScaleChart() {
  return (
    <div>
      {SCALE.map((row, i) => {
        const pct = Math.max(3, ((row.log - LO) / (HI - LO)) * 100);
        return (
          <motion.div
            className="scale-row"
            key={row.name}
            initial={{ opacity: 0, y: 14 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-40px" }}
            transition={{ duration: 0.45, delay: i * 0.05, ease: "easeOut" }}
          >
            <div className="scale-name">
              {row.name}
              <span>{row.tick}</span>
            </div>
            <div className="scale-track">
              <motion.div
                className="scale-bar"
                style={{ background: row.color }}
                initial={{ width: 0 }}
                whileInView={{ width: `${pct}%` }}
                viewport={{ once: true, margin: "-40px" }}
                transition={{ duration: 1.1, delay: i * 0.05, ease: [0.22, 1, 0.36, 1] }}
              />
            </div>
            <div className="scale-label">{row.label}</div>
          </motion.div>
        );
      })}
    </div>
  );
}
