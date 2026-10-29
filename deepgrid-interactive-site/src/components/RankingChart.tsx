import { motion } from "framer-motion";
import { competitors } from "../data";

export function RankingChart() {
  const sorted = [...competitors].sort((a, b) => b.score - a.score);
  return (
    <div>
      {sorted.map((c, i) => {
        const pct = (c.score / 5) * 100;
        const color = c.score >= 4.5 ? "#E06767" : c.score >= 2 ? "#D7720B" : "#04B3C7";
        return (
          <motion.div
            className="rank-row"
            key={c.id}
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-40px" }}
            transition={{ duration: 0.4, delay: i * 0.05, ease: "easeOut" }}
          >
            <span className="rank-no">{i + 1}</span>
            <span className="rank-name">{c.name}</span>
            <div className="rank-track">
              <motion.div
                className="rank-bar"
                style={{ background: color }}
                initial={{ width: 0 }}
                whileInView={{ width: `${pct}%` }}
                viewport={{ once: true, margin: "-40px" }}
                transition={{ duration: 1, delay: i * 0.05, ease: [0.22, 1, 0.36, 1] }}
              />
            </div>
            <span className="rank-score">{c.score.toFixed(1)}</span>
            <span className="rank-blocker" title={c.blocker_why}>
              blocker {c.blocker}
            </span>
          </motion.div>
        );
      })}
    </div>
  );
}
