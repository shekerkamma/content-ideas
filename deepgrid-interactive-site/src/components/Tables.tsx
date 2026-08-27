import { motion } from "framer-motion";
import { certification, supplierside } from "../data";
import { Pill } from "./common";

const CERT_COLOR: Record<string, string> = {
  HELD: "#1BA271",
  CLAIMED: "#D7720B",
  IMPLIED: "#D7720B",
  "CATEGORY ERROR": "#E06767",
  ABSENT: "#E06767",
  CAPPED: "#E06767",
};

export function CertTable() {
  return (
    <div>
      {certification.map(([co, cred, status, note], i) => (
        <motion.div
          className="cert-row"
          key={co}
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-30px" }}
          transition={{ duration: 0.4, delay: i * 0.04, ease: "easeOut" }}
        >
          <b>{co}</b>
          <span className="cert-cred">{cred}</span>
          <Pill color={CERT_COLOR[status] ?? "#8EA0B2"}>{status}</Pill>
          <span className="cert-note">{note}</span>
        </motion.div>
      ))}
    </div>
  );
}

export function SupplierTable() {
  return (
    <div>
      {supplierside.rows.map((r, i) => {
        const [who, sets, pos, , status, ev] = r;
        const color = status === "EVIDENCED" ? "#1BA271" : "#E06767";
        return (
          <motion.div
            className="sup-row"
            key={who}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-30px" }}
            transition={{ duration: 0.45, delay: i * 0.05, ease: "easeOut" }}
          >
            <div className="sup-who">
              {who}
              <span className="sup-ev">{ev}</span>
            </div>
            <div>
              <b>{sets}</b>
              <p>{pos}</p>
            </div>
            <Pill color={color}>{status}</Pill>
          </motion.div>
        );
      })}
    </div>
  );
}
