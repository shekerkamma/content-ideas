import { motion } from "framer-motion";
import { patterns } from "../data";

const colors = ["#04B3C7", "#1BA271", "#D7720B", "#60A5FA", "#A78BFA", "#FB7185"];

export function RelationshipMap() {
  return (
    <motion.div
      className="rel-grid"
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, margin: "-40px" }}
      variants={{ hidden: {}, show: { transition: { staggerChildren: 0.08 } } }}
    >
      {patterns.rows.map((r, i) => {
        const [pat, what, who, rate, move, , ev] = r;
        const c = colors[i % colors.length];
        return (
          <motion.article
            className="rel-card"
            key={pat}
            style={{ borderTop: `3px solid ${c}` }}
            variants={{ hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0, transition: { duration: 0.55, ease: "easeOut" } } }}
            whileHover={{ y: -5, boxShadow: "0 18px 40px rgba(0,0,0,.45)" }}
          >
            <h4 style={{ color: c }}>{pat}</h4>
            <p className="rel-what">{what}</p>
            <div className="rel-who">
              <b>Who</b> {who}
              <em style={{ color: c }}>{rate}</em>
            </div>
            <p className="rel-move">{move}</p>
            <span className="rel-ev">{ev}</span>
          </motion.article>
        );
      })}
    </motion.div>
  );
}
