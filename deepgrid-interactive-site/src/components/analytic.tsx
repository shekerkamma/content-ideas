import { motion } from "framer-motion";
import type { ReactNode } from "react";
import {
  buildbuy,
  competitors,
  countermoves,
  differentjob,
  displacement,
  donotcompete,
  execcompare,
  lifecycle,
  narrativecounter,
  oneprogramme,
  pricing,
  reshape,
  silicon,
  universe,
  valuenet,
} from "../data";
import { fadeUpChild, Pill, staggerParent } from "./common";

const VERDICT: Record<string, string> = {
  VERIFIED: "#1BA271", EVIDENCED: "#1BA271", BUY: "#1BA271", ATTACH: "#1BA271",
  LOW: "#04B3C7", MONITOR: "#04B3C7", "PARTNER + COUNTER": "#D7720B", "CHANNEL DILIGENCE": "#D7720B",
  MEDIUM: "#D7720B", ATTRIBUTED: "#D7720B", PARTNER: "#D7720B", UNTESTED: "#D7720B", UNRESOLVED: "#D7720B",
  "ATTACH / BENCHMARK": "#1BA271", "ATTACH / BOUNDARY": "#1BA271",
  "DIFFERENT JOB — note and leave": "#04B3C7",
  HIGH: "#E06767", STRUCTURAL: "#E06767", "UNEVIDENCED IN INDIA CV": "#E06767",
  "FAILS ITS OWN SOURCE": "#E06767", "DO NOT BUILD": "#E06767",
  "DISPLACE OR DIFFERENTIATE": "#E06767", OCCUPIED: "#E06767",
  "UNWINNABLE ON TIME": "#E06767", "STRUCTURALLY CLOSED": "#E06767",
  "ADVANTAGE IS WORTHLESS HERE": "#E06767", "NO ROUTE TO MARKET": "#E06767",
  "NO CERTIFICATION": "#E06767", "HARD CEILING": "#E06767", "HOLDS THE SEAT": "#E06767",
  "OWNS THE PLATFORM": "#D7720B", "OWNS THE SAFETY CASE": "#D7720B",
};
const vc = (s: string) => VERDICT[s] ?? "#8EA0B2";

function Wrap({ children }: { children: ReactNode }) {
  return (
    <motion.div className="arc-grid" initial="hidden" whileInView="show" viewport={{ once: true, margin: "-40px" }} variants={staggerParent}>
      {children}
    </motion.div>
  );
}

function Item({ children, accent }: { children: ReactNode; accent?: string }) {
  return (
    <motion.article className="arcard" variants={fadeUpChild} whileHover={{ y: -4 }} style={accent ? { borderTop: `3px solid ${accent}` } : undefined}>
      {children}
    </motion.article>
  );
}

function F({ k, v, ev }: { k: string; v: string; ev?: boolean }) {
  return (
    <div className="f">
      <span className="fk">{k}</span>
      <span className={`fv ${ev ? "ev" : ""}`}>{v}</span>
    </div>
  );
}

export function Valuenet() {
  return (
    <>
      <div className="vnet">
        {valuenet.quadrants.map(([name, desc, items, ev], i) => {
          const color = ["#1BA271", "#E06767", "#D7720B", "#04B3C7"][i % 4];
          return (
            <motion.div
              className="quad"
              key={name}
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-40px" }}
              transition={{ duration: 0.5, delay: i * 0.07, ease: "easeOut" }}
              style={{ borderTop: `3px solid ${color}` }}
            >
              <h4 style={{ color }}>{name}</h4>
              <p className="qd">{desc}</p>
              <ul style={{ color }}>
                {items.map((it) => (
                  <li key={it}>{it}</li>
                ))}
              </ul>
              <span className="vev">{ev}</span>
            </motion.div>
          );
        })}
      </div>
      <p className="sowhat">{valuenet.sowhat}</p>
    </>
  );
}

export function Lifecycle() {
  return (
    <>
      <Wrap>
        {lifecycle.rows.map(([co, mech, desc, ev]) => (
          <Item key={co} accent={co === "DeepGrid Semi" ? "#E06767" : "#04B3C7"}>
            <h4>{co}</h4>
            <p className="arcard-sub">{mech}</p>
            <div className="arcard-fields">
              <F k="Channel" v={desc} />
              <F k="Evidence" v={ev} ev />
            </div>
          </Item>
        ))}
      </Wrap>
      <p className="sowhat">{lifecycle.sowhat}</p>
    </>
  );
}

export function BuildBuy() {
  return (
    <Wrap>
      {buildbuy.rows.map(([decision, verb, why, ev]) => (
        <Item key={decision} accent={vc(verb)}>
          <h4>
            {decision}
            <span className="tag" style={{ background: vc(verb) }}>{verb}</span>
          </h4>
          <div className="arcard-fields">
            <F k="Why" v={why} />
            <F k="Evidence" v={ev} ev />
          </div>
        </Item>
      ))}
    </Wrap>
  );
}

export function Pricing() {
  return (
    <>
      <Wrap>
        {pricing.evidence.map(([claim, detail, status]) => (
          <Item key={claim} accent={vc(status)}>
            <h4>
              {claim}
              <span className="tag" style={{ background: vc(status) }}>{status}</span>
            </h4>
            <p className="arcard-sub">{detail}</p>
          </Item>
        ))}
      </Wrap>
      <h3 className="block">Banned from any slide</h3>
      <div className="arc-grid">
        {pricing.banned.map((b) => (
          <motion.article key={b} className="arcard" variants={fadeUpChild} style={{ borderLeft: "3px solid #E06767" }}>
            <p className="ban" style={{ margin: 0 }}>{b}</p>
          </motion.article>
        ))}
      </div>
      <p className="sowhat">{pricing.instead}</p>
    </>
  );
}

export function Silicon() {
  return (
    <>
      <Wrap>
        {silicon.rows.map(([co, chip, note, status, ev]) => (
          <Item key={co} accent={vc(status)}>
            <h4>
              {co}
              <span className="tag" style={{ background: vc(status) }}>{status}</span>
            </h4>
            <p className="arcard-sub">{chip}</p>
            <div className="arcard-fields">
              <F k="Read" v={note} />
              <F k="Evidence" v={ev} ev />
            </div>
          </Item>
        ))}
      </Wrap>
      <p className="sowhat">{silicon.sowhat}</p>
    </>
  );
}

export function Countermoves() {
  return (
    <>
      <p className="arcard-sub" style={{ color: "var(--muted)", maxWidth: "76ch" }}>{countermoves.note}</p>
      <Wrap>
        {countermoves.rows.map(([rival, trigger, counter, risk, answerable, ev]) => (
          <Item key={`${rival}-${trigger}`} accent={vc(risk)}>
            <h4>
              {rival}
              <span className="tag" style={{ background: vc(risk) }}>{risk} risk</span>
            </h4>
            <p className="arcard-sub">{trigger}</p>
            <div className="arcard-fields">
              <F k="Their counter" v={counter} />
              <F k="Answerable" v={answerable} />
              <F k="Evidence" v={ev} ev />
            </div>
          </Item>
        ))}
      </Wrap>
    </>
  );
}

export function Donotcompete() {
  return (
    <>
      <p className="arcard-sub" style={{ color: "var(--muted)", maxWidth: "76ch" }}>{donotcompete.note}</p>
      <Wrap>
        {donotcompete.rows.map(([arena, verdict, why, reopen]) => (
          <Item key={arena} accent={vc(verdict)}>
            <h4>
              {arena}
              <span className="tag" style={{ background: vc(verdict) }}>{verdict}</span>
            </h4>
            <div className="arcard-fields">
              <F k="Why" v={why} />
              <F k="Reopen if" v={reopen} />
            </div>
          </Item>
        ))}
      </Wrap>
    </>
  );
}

export function Execcompare() {
  return (
    <Wrap>
      {execcompare.rows.map(([co, model, ev, threat, partner, move]) => (
        <Item key={co} accent={vc(ev)}>
          <h4>{co}</h4>
          <p className="arcard-sub">{model}</p>
          <div className="arcard-fields">
            <F k="Evidence" v={ev} />
            <F k="Threat" v={threat} />
            <F k="Partner" v={partner} />
            <F k="Move" v={move} />
          </div>
        </Item>
      ))}
    </Wrap>
  );
}

export function Universe() {
  const W = 640, H = 560, P = 46, pw = W - P * 2, ph = H - P * 2 - 30;
  const sx = (x: number) => P + (x / 100) * pw;
  const sy = (y: number) => P + ((100 - y) / 100) * ph;
  const midX = sx(50), midY = sy(50);
  return (
    <div className="univ">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Competitive universe 2x2">
        {universe.zones.map(([name, desc, x, y, color]) => {
          const left = x < 50 ? P : midX;
          const top = y >= 50 ? P : midY;
          return (
            <g key={name}>
              <rect x={left} y={top} width={midX - P} height={midY - P} fill={color} opacity={0.12} rx={10} />
              <text x={sx(x)} y={sy(y) - 12} fill={color} fontSize={15} fontWeight={800} textAnchor="middle">{name}</text>
              <text x={sx(x)} y={sy(y) + 4} fill="#8ea0b2" fontSize={10} textAnchor="middle">{desc.slice(0, 34)}</text>
            </g>
          );
        })}
        <line x1={midX} y1={P} x2={midX} y2={H - P - 30} stroke="#1a2f45" strokeWidth={1.5} />
        <line x1={P} y1={midY} x2={W - P} y2={midY} stroke="#1a2f45" strokeWidth={1.5} />
        <text x={W / 2} y={H - 8} fill="#5b7187" fontSize={11} textAnchor="middle" letterSpacing="2">{universe.xlab}</text>
        <text x={14} y={H / 2} fill="#5b7187" fontSize={11} textAnchor="middle" letterSpacing="2" transform={`rotate(-90 14 ${H / 2})`}>{universe.ylab}</text>
        {universe.players.map(([name, x, y, zone]) => {
          const color = universe.zones.find((z) => z[0] === zone)?.[4] ?? "#04B3C7";
          return (
            <g key={name}>
              <circle cx={sx(x)} cy={sy(y)} r={6} fill={color} stroke="#050d18" strokeWidth={2} />
              <text x={sx(x) + 10} y={sy(y) + 4} fill="#e6edf3" fontSize={11} fontWeight={600}>{name}</text>
            </g>
          );
        })}
      </svg>
      <div className="legend">
        {universe.zones.map(([name, , , , color]) => (
          <span key={name}><i style={{ background: color }} />{name}</span>
        ))}
      </div>
    </div>
  );
}

export function Differentjob() {
  return (
    <Wrap>
      {differentjob.rows.map(([co, job, buyer, clock, why, proves, ev]) => (
        <Item key={co} accent="#04B3C7">
          <h4>{co}</h4>
          <p className="arcard-sub">{job}</p>
          <div className="arcard-fields">
            <F k="Buyer" v={buyer} />
            <F k="Clock" v={clock} />
            <F k="Why not" v={why} />
            <F k="Proves" v={proves} />
            <F k="Evidence" v={ev} ev />
          </div>
        </Item>
      ))}
    </Wrap>
  );
}

export function Narrativecounter() {
  return (
    <Wrap>
      {narrativecounter.rows.map(([claim, who, shows, settles, cost, ev]) => (
        <Item key={claim} accent="#E06767">
          <h4>{claim}</h4>
          <p className="arcard-sub">{who}</p>
          <div className="arcard-fields">
            <F k="Evidence shows" v={shows} />
            <F k="Settles with" v={settles} />
            <F k="Cost if unanswered" v={cost} />
            <F k="Evidence" v={ev} ev />
          </div>
        </Item>
      ))}
    </Wrap>
  );
}

export function Displacement() {
  return (
    <>
      <div className="arc-grid">
        {displacement.contest.map(([k, v, ev]) => (
          <motion.article key={k} className="arcard" variants={fadeUpChild} style={{ borderTop: "3px solid #E06767" }}>
            <h4>{k}</h4>
            <p className="arcard-sub">{v}</p>
            <span className="fv ev">{ev}</span>
          </motion.article>
        ))}
      </div>
      <h3 className="block">Five levers, three moves, one falsifier</h3>
      <Wrap>
        {displacement.levers.map(([name, test, status, reason, ev, color]) => (
          <Item key={name} accent={color === "red" ? "#E06767" : color === "amber" ? "#D7720B" : "#1BA271"}>
            <h4>
              {name}
              <span className="tag" style={{ background: vc(status) }}>{status}</span>
            </h4>
            <p className="arcard-sub">{test}</p>
            <div className="arcard-fields">
              <F k="Read" v={reason} />
              <F k="Evidence" v={ev} ev />
            </div>
          </Item>
        ))}
      </Wrap>
    </>
  );
}

export function Reshape() {
  return (
    <>
      <div className="reshape">
        <div className="rr head">
          <div className="cell">What the dossier does now</div>
          <div className="cell">What the pattern says it should do</div>
        </div>
        {reshape.rows.slice(1).map(([before, after], i) => (
          <motion.div
            className="rr"
            key={i}
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-30px" }}
            transition={{ duration: 0.45, delay: i * 0.05, ease: "easeOut" }}
          >
            <div className="cell before">{before}</div>
            <div className="cell after">{after}</div>
          </motion.div>
        ))}
      </div>
      <p className="sowhat">{reshape.sowhat}</p>
    </>
  );
}

export function OneProgramme() {
  return (
    <div className="oneprog">
      {[oneprogramme.left, oneprogramme.right].map((side) => (
        <motion.div
          className="side"
          key={side.title}
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-40px" }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        >
          <h4>{side.title}</h4>
          <div className="arcard-fields">
            {side.rows.map(([k, v]) => (
              <F key={k} k={k} v={v} />
            ))}
            <F k="Evidence" v={side.ev} ev />
          </div>
        </motion.div>
      ))}
      <div className="verdict">{oneprogramme.verdict}</div>
      <p className="sowhat" style={{ gridColumn: "1 / -1" }}>{oneprogramme.sowhat}</p>
    </div>
  );
}

export function ThreatArena() {
  const arenas = ["Government / PSU", "OEM / Tier-1", "Fleet / mining"];
  const color = (r: string) => (r === "HIGH" ? "#E06767" : r === "MEDIUM" ? "#D7720B" : "#04B3C7");
  return (
    <div className="heatmap">
      <div className="row">
        <div className="cell h">Competitor</div>
        {arenas.map((a) => (
          <div className="cell h" key={a}>{a}</div>
        ))}
      </div>
      {competitors.map((c, i) => (
        <motion.div
          className="row"
          key={c.id}
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.35, delay: i * 0.03 }}
        >
          <div className="cell name">{c.name}</div>
          {arenas.map((a) => {
            const [rating, note] = c.arenas[a] ?? ["—", ""];
            return (
              <div className="cell" key={a} title={note}>
                <Pill color={color(rating)}>{rating}</Pill>
              </div>
            );
          })}
        </motion.div>
      ))}
    </div>
  );
}
