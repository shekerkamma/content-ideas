// Single source of truth — bundled from the run's JSON artifacts. Nothing here
// is re-typed by hand; every number comes from the evidence-ledger-backed JSONs.
import profRaw from "./data/company-profiles.json";
import scoringRaw from "./data/scoring.json";
import stratRaw from "./data/strategy-sections.json";
import narRaw from "./data/narrative.json";

export type Tier = "P-ACT" | "P-WARN" | "P-ADJ";
export type Posture = "VERIFIED" | "CONTESTED" | "UNVERIFIED" | "ATTRIBUTED";

export interface Company {
  id: string;
  name: string;
  legal: string;
  tier: Tier;
  founded: string;
  founded_note: string;
  hq: string;
  status: string;
  ticker: string;
  value: string;
  value_usd: string;
  value_asof: string;
  value_move: string;
  value_dir: string;
  people: string;
  parent: string;
  sells: string;
  ai: [string, string][];
  evidence: string;
  posture: Posture;
  read: string;
  detail: [string, string][];
  gaps: string[];
}

export interface Competitor {
  id: string;
  name: string;
  execution: number;
  access: number;
  leverage: number;
  ev: string;
  tier: Tier;
  why_e: string;
  why_a: string;
  why_l: string;
  conf: string;
  conf_note: string;
  arenas: Record<string, [string, string]>;
  score: number;
  blocker: number;
  blocker_why: string;
}

export const companies = (profRaw as any).companies as Company[];
export const certification = (profRaw as any).certification as [string, string, string, string][];
export const timeline = (profRaw as any).timeline as [string, string, string][];
export const regulatory = (profRaw as any).regulatory as {
  instrument: string;
  rules: string;
  amended: string;
  superseded: string;
  gazette: string;
  obligations: [string, string, string, string, string][];
  propagators: [string, string, string][];
};

export const competitors = (scoringRaw as any).competitors as Competitor[];
export const weights = (scoringRaw as any).weights as { execution: number; access: number; leverage: number };

export const patterns = (stratRaw as any).patterns as {
  kicker: string; title: string; sub: string; sowhat: string;
  rows: [string, string, string, string, string, string, string][];
};
export const posture = (stratRaw as any).posture as {
  kicker: string;
  title: string;
  sub: string;
  modes: [string, string, string, string, string][];
  choice: string;
};
export const supplierside = (stratRaw as any).supplierside as {
  kicker: string; title: string; sub: string; cols: string[]; sowhat: string;
  rows: [string, string, string, string, string, string][];
};
export const execaction = (stratRaw as any).execaction as {
  kicker: string; title: string; sub: string; donotfund: string;
  rows: [string, string, string, string, string][];
};
export const displacement = (stratRaw as any).displacement as {
  kicker: string; title: string; sub: string;
  contest: [string, string, string][];
  levers: [string, string, string, string, string, string][];
};

export const coreMessage = (narRaw as any).core_message as string;
export const scqa = (narRaw as any).scqa as { situation: string; complication: string; question: string; answer: string };
export const pyramid = (narRaw as any).pyramid as {
  governing_thought: string;
  supports: { claim: string; because: string; proof: string }[];
};
export const hostileQuestions = (narRaw as any).hostile_questions as [string, string][];

export const EVIDENCE_ROWS = 79;

// Scale spread (mirrors the deck's log-scale exhibit). value = log10(USD).
export const SCALE: { name: string; tick: string; label: string; log: number; color: string }[] = [
  { name: "ZF Group (parent)", tick: "PRIVATE", label: "€41.4bn sales · 161,600 staff", log: 10.8, color: "#E06767" },
  { name: "Aptiv PLC", tick: "NYSE: APTV", label: "$10.2bn · −34.6% YoY", log: 10.0, color: "#E06767" },
  { name: "ZF CVCS India", tick: "NSE: ZFCVINDIA", label: "₹29,642 Cr · ~$3.4bn", log: 9.53, color: "#E06767" },
  { name: "Roadzen (drivebuddyAI)", tick: "Nasdaq: RDZN", label: "~$112m · share $1.26", log: 8.05, color: "#D7720B" },
  { name: "Sterling Tools", tick: "NSE: STERTOOLS", label: "₹806 Cr · ~$92m", log: 7.96, color: "#D7720B" },
  { name: "bitsensing", tick: "PRIVATE", label: "$42m raised", log: 7.62, color: "#D7720B" },
  { name: "Netrasemi", tick: "PRIVATE", label: "₹107 Cr Series A · ~$12m", log: 7.08, color: "#04B3C7" },
  { name: "STRADVISION", tick: "PRIVATE", label: "no public valuation · 300+ staff", log: 6.78, color: "#04B3C7" },
  { name: "Starkenn", tick: "PRIVATE", label: "$2.0m raised · 57 staff", log: 6.3, color: "#04B3C7" },
  { name: "Gahan AI", tick: "PRIVATE", label: "no funding disclosed · 15 staff", log: 5.78, color: "#04B3C7" },
];

export const TIER_META: Record<Tier, { label: string; note: string; color: string }> = {
  "P-ACT": { label: "Reaches brake actuation", note: "can satisfy CMVR rule 96(12) AEBS", color: "#E06767" },
  "P-WARN": { label: "Warning only", note: "cannot satisfy rule 96(12) at any price", color: "#D7720B" },
  "P-ADJ": { label: "Adjacent", note: "not competing for the mandate today", color: "#04B3C7" },
};

export const POSTURE_COLOR: Record<Posture, string> = {
  VERIFIED: "#1BA271",
  CONTESTED: "#E06767",
  UNVERIFIED: "#E06767",
  ATTRIBUTED: "#D7720B",
};

// ── sections that were in the run but not previously rendered ──────────────
export const valuenet = (stratRaw as any).valuenet as {
  kicker: string; title: string; sub: string; sowhat: string;
  quadrants: [string, string, string[], string][];
};
export const lifecycle = (stratRaw as any).lifecycle as {
  kicker: string; title: string; sub: string; sowhat: string;
  rows: [string, string, string, string][];
};
export const buildbuy = (stratRaw as any).buildbuy as {
  kicker: string; title: string; sub: string;
  rows: [string, string, string, string][];
};
export const pricing = (stratRaw as any).pricing as {
  kicker: string; title: string; sub: string;
  evidence: [string, string, string][];
  banned: string[]; instead: string; gate: string;
};
export const silicon = (stratRaw as any).silicon as {
  kicker: string; title: string; sub: string; sowhat: string;
  rows: [string, string, string, string, string][];
};
export const countermoves = (stratRaw as any).countermoves as {
  kicker: string; title: string; sub: string; note: string;
  rows: [string, string, string, string, string, string][];
};
export const donotcompete = (stratRaw as any).donotcompete as {
  kicker: string; title: string; sub: string; note: string;
  rows: [string, string, string, string][];
};
export const execcompare = (stratRaw as any).execcompare as {
  kicker: string; title: string; sub: string; cols: string[];
  rows: [string, string, string, string, string, string][];
};
export const universe = (stratRaw as any).universe as {
  kicker: string; title: string; sub: string; xlab: string; ylab: string;
  zones: [string, string, number, number, string][];
  players: [string, number, number, string, string][];
};
export const differentjob = (stratRaw as any).differentjob as {
  kicker: string; title: string; sub: string; cols: string[];
  rows: [string, string, string, string, string, string, string][];
};
export const narrativecounter = (stratRaw as any).narrativecounter as {
  kicker: string; title: string; sub: string; cols: string[];
  rows: [string, string, string, string, string, string][];
};
export const oneprogramme = (stratRaw as any).oneprogramme as {
  kicker: string; title: string; sub: string; verdict: string; sowhat: string;
  left: { title: string; rows: [string, string][]; ev: string };
  right: { title: string; rows: [string, string][]; ev: string };
};
export const reshape = (stratRaw as any).reshape as {
  kicker: string; title: string; sub: string; sowhat: string;
  rows: [string, string][];
};
