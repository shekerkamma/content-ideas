import { AnimatePresence, motion } from "framer-motion";
import { companies, POSTURE_COLOR, TIER_META } from "../data";
import { Pill } from "./common";

interface CompanyExplorerProps {
  active: string;
  onActiveChange: (companyId: string) => void;
}

export function CompanyExplorer({ active, onActiveChange }: CompanyExplorerProps) {
  const c = companies.find((x) => x.id === active) ?? companies[0];

  return (
    <div>
      <div className="co-bar">
        {companies.map((co) => (
          <button
            key={co.id}
            className={`co-chip ${co.id === active ? "active" : ""}`}
            style={co.id === active ? { background: POSTURE_COLOR[co.posture], borderColor: POSTURE_COLOR[co.posture] } : undefined}
            onClick={() => onActiveChange(co.id)}
          >
            {co.name}
          </button>
        ))}
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={c.id}
          className="co-panel"
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.28, ease: "easeOut" }}
        >
          <h4>{c.name}</h4>
          <div className="co-badges">
            <Pill color={TIER_META[c.tier].color}>{c.tier}</Pill>
            <Pill color={POSTURE_COLOR[c.posture]}>{c.posture}</Pill>
          </div>
          <div className="co-facts">
            {[
              ["Founded", c.founded],
              ["Headquarters", c.hq],
              ["Status", c.status],
              ["Value", c.value],
            ].map(([k, v]) => (
              <div className="co-fact" key={k}>
                <span>{k}</span>
                <b>{v}</b>
              </div>
            ))}
          </div>
          <p className="co-sells">{c.sells}</p>
          <div className="co-cols">
            <div className="co-col">
              <h5>What its AI actually does</h5>
              <ul>
                {(c.ai ?? []).map(([k, v]) => (
                  <li key={k}>
                    <b style={{ color: "#fff" }}>{k}</b> — {v}
                  </li>
                ))}
              </ul>
            </div>
            <div className="co-col">
              <h5>Detail</h5>
              <ul>
                {(c.detail ?? []).map(([k, v]) => (
                  <li key={k}>
                    {k} — {v}
                  </li>
                ))}
              </ul>
            </div>
            <div className="co-col">
              <h5>Open on this company</h5>
              <ul>
                {(c.gaps ?? []).map((g) => (
                  <li className="g" key={g}>
                    {g}
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <p className="co-read">{c.read}</p>
          <span className="co-ev">{c.evidence}</span>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
