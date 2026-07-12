#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const RUN = "/home/shekerk/content-ideas/runs/2026-07-02-video-to-deck-rerun";
const SERVER = "http://127.0.0.1:3000";

const P = {
  bg: "#101113",
  board: "#15181c",
  card: "#22262c",
  blue: "#1f3447",
  green: "#173c31",
  yellow: "#42351a",
  rose: "#432231",
  line: "#f1f3f5",
  muted: "#c8ced6",
  accent: "#ffd43b",
  teal: "#63e6be",
  white: "#ffffff",
};

let seq = 0;
function id(prefix) { seq += 1; return `${prefix}_${seq}`; }
function base(type, extra) {
  return {
    id: id(type), type, x: 0, y: 0, width: 100, height: 100, angle: 0,
    strokeColor: P.line, backgroundColor: "transparent", fillStyle: "solid",
    strokeWidth: 2, strokeStyle: "solid", roughness: 1.2, opacity: 100,
    groupIds: [], frameId: null, roundness: null, seed: 1000 + seq,
    version: 1, versionNonce: 2000 + seq, isDeleted: false, boundElements: null,
    updated: Date.now(), link: null, locked: false, ...extra,
  };
}
function rect(x, y, w, h, fill = P.card, stroke = P.line) {
  return base("rectangle", { x, y, width: w, height: h, backgroundColor: fill, strokeColor: stroke, roundness: { type: 3 } });
}
function ellipse(x, y, w, h, fill = P.blue, stroke = P.line) {
  return base("ellipse", { x, y, width: w, height: h, backgroundColor: fill, strokeColor: stroke });
}
function text(x, y, value, size = 20, color = P.white, width = 500, height = 40, align = "left") {
  return base("text", {
    x, y, width, height, strokeColor: color, backgroundColor: "transparent",
    text: value, originalText: value, fontSize: size, fontFamily: 1,
    textAlign: align, verticalAlign: "top", autoResize: true, lineHeight: 1.2,
    baseline: Math.round(size * 1.15),
  });
}
function arrow(x, y, w, h = 0, color = P.line) {
  return base("arrow", { x, y, width: w, height: h, points: [[0, 0], [w, h]], endArrowhead: "arrow", strokeColor: color });
}
function card(e, x, y, w, h, title, body, fill = P.card) {
  e.push(rect(x, y, w, h, fill));
  e.push(text(x + 18, y + 16, title, 20, P.accent, w - 36, 28));
  if (body) e.push(text(x + 18, y + 54, body, 15, P.white, w - 36, h - 62));
}
function title(e, value, sub = "") {
  e.push(text(64, 42, value, 31, P.white, 980, 42));
  if (sub) e.push(text(68, 88, sub, 16, P.muted, 980, 24));
}
function scene(name, elements) {
  return {
    name,
    data: {
      type: "excalidraw",
      version: 2,
      source: "content-ideas-video-to-deck-v3-excalidraw",
      elements: [rect(0, 0, 1200, 675, P.bg, P.bg), ...elements],
      appState: { viewBackgroundColor: "#ffffff", gridSize: null },
      files: {},
    },
  };
}

function market() {
  const e = []; title(e, "SaaS packaged repeatable work", "Agents package executed work: the next value layer after software workflows.");
  e.push(text(105, 155, "SaaS adoption curve", 20, P.white, 300, 28));
  const vals = [50, 75, 105, 150, 205, 270, 350];
  vals.forEach((v, i) => {
    e.push(rect(110 + i * 52, 470 - v, 32, v, i < 5 ? P.blue : P.green, "transparent"));
  });
  ["Early","CRM","Collab","FinOps","Vertical","AI apps","Agents"].forEach((lab, i) => e.push(text(96 + i * 52, 485, lab, 13, P.muted, 58, 20, "center")));
  card(e, 560, 170, 210, 86, "Shopify", "commerce workflow", P.green);
  card(e, 820, 170, 210, 86, "Slack", "team workflow", P.blue);
  card(e, 560, 300, 210, 86, "Airbnb", "market workflow", P.rose);
  card(e, 820, 300, 210, 86, "Stripe", "payment workflow", P.yellow);
  e.push(text(565, 460, "Pattern: winners own a repeated workflow, then expose controls.", 21, P.teal, 500, 32));
  return scene("v3-market-context", e);
}
function thesis() {
  const e = []; title(e, "AI agents are the new SaaS", "Only when they own a narrow paid workflow end to end.");
  card(e, 95, 210, 210, 150, "Paid workflow", "already funded\nfrequent\npainful", P.rose);
  e.push(arrow(325, 285, 95));
  card(e, 445, 210, 210, 150, "Observed spec", "trigger\ncontext\ntools\nrules", P.yellow);
  e.push(arrow(675, 285, 95));
  card(e, 795, 210, 210, 150, "Agent business", "does work\nlogs work\nasks when stuck", P.green);
  e.push(text(125, 455, "Do not start with a generic bot. Start where work is already paid for.", 24, P.teal, 900, 38));
  return scene("v3-thesis-workflow", e);
}
function economics() {
  const e = []; title(e, "The unit economics crush", "The wedge is cost compression plus faster response.");
  card(e, 120, 175, 260, 110, "Human agent", "$3.00-$6.00\n6+ hr first response", P.card);
  e.push(arrow(410, 230, 130));
  card(e, 570, 175, 260, 110, "AI agent", "$0.25-$0.50\n<4 min first response", P.blue);
  e.push(text(870, 205, "90%+\nlower cost", 30, P.teal, 220, 90));
  [["First response","6+ hrs","<4 min"],["Resolution","32+ hrs","32 min"],["ROI path","Year 1","Year 2-3"]].forEach((r, i) => {
    const y = 365 + i * 56; e.push(rect(130, y, 850, 42, "#191b1f", "#60656d"));
    e.push(text(150, y + 11, r[0], 15, P.white, 250, 20));
    e.push(text(455, y + 11, r[1], 15, P.muted, 160, 20));
    e.push(text(700, y + 11, r[2], 15, P.teal, 180, 20));
  });
  return scene("v3-unit-economics", e);
}
function workflowScore() {
  const e = []; title(e, "Pick a workflow with a paycheck attached", "Score work before you build.");
  [["Frequency","daily / hourly"],["Pain","missed calls\nslow replies"],["Pattern","booking\ntriage\napproval"],["Tools","email\ncalendar\nCRM"],["Budget","employee\nagency\nBPO"]].forEach((c, i) => card(e, 80 + i * 215, 190, 170, 140, c[0], c[1], i === 4 ? P.green : P.card));
  e.push(rect(115, 430, 900, 58, P.rose, "#d6336c"));
  e.push(text(145, 448, "First rep: one niche -> 20 annoying jobs -> score each one.", 21, P.white, 830, 30));
  return scene("v3-workflow-scorecard", e);
}
function examples() {
  const e = []; title(e, "Founder-sized wedges", "Named examples point to narrow jobs with budget and urgency.");
  card(e, 75, 160, 245, 150, "Slang AI", "restaurant calls\nreservations\nVIP routing", P.yellow);
  card(e, 360, 160, 245, 150, "Same Day", "home-services calls\nbooking\nrescheduling", P.blue);
  card(e, 645, 160, 245, 150, "Property ops", "tenant requests\nfront-door triage\nhandoff", P.green);
  card(e, 930, 160, 205, 150, "Contact center", "reception\ndispatch\nfollow-up", P.rose);
  e.push(text(105, 425, "Good wedge = urgent + repeated + software-touched + already paid.", 27, P.teal, 930, 38));
  return scene("v3-wedge-examples", e);
}
function shadow() {
  const e = []; title(e, "Shadow the human before you build", "The spec lives inside real operator behavior.");
  card(e, 100, 195, 250, 165, "Watch 10-20 runs", "screen record\nnarrate decisions\ncopy/paste spots", P.card);
  e.push(arrow(375, 275, 115));
  card(e, 520, 195, 250, 165, "Extract the spec", "trigger\ncontext\ntools\nrules\napproval", P.yellow);
  e.push(arrow(795, 275, 115));
  card(e, 940, 195, 190, 165, "Define trust", "stuck?\nask?\nlog?", P.green);
  e.push(text(120, 460, "A prompt is not a workflow spec.", 28, P.teal, 620, 38));
  return scene("v3-shadow-human", e);
}
function smallAgent() {
  const e = []; title(e, "Build the smallest useful agent", "Ship one bounded loop before expanding.");
  [["1 Draft","write reply\nsummarize\nnext step"],["2 Triage","classify\nprioritize\nroute"],["3 Coordinate","check slots\nnotify humans\nsync systems"],["4 Act","book\nupdate\nsend"]].forEach((c, i) => {
    card(e, 110 + i * 255, 205, 205, 145, c[0], c[1], [P.card, P.yellow, P.blue, P.green][i]);
    if (i < 3) e.push(arrow(322 + i * 255, 278, 45));
  });
  e.push(rect(165, 455, 800, 55, P.rose, "#d6336c"));
  e.push(text(200, 472, "Good promise: answer missed calls, find providers, book qualified jobs.", 20, P.white, 740, 28));
  return scene("v3-smallest-agent", e);
}
function architecture() {
  const e = []; title(e, "Agentic workflows need a control pattern", "Sequential for stable paths; hierarchical for review and escalation.");
  card(e, 110, 190, 420, 210, "Sequential workflow", "intake -> classify -> draft -> approve -> send\n\nBest for repeatable processes.", P.blue);
  card(e, 670, 190, 420, 210, "Hierarchical workflow", "delegate -> inspect -> escalate -> resolve\n\nBest for judgment and quality gates.", P.green);
  e.push(text(145, 485, "Architecture references should become founder-operating diagrams, not pasted text cards.", 20, P.teal, 900, 30));
  return scene("v3-agentic-workflows", e);
}
function wrapper() {
  const e = []; title(e, "The wrapper makes it SaaS", "The agent does the job. The control room creates trust.");
  e.push(ellipse(105, 215, 190, 100, P.blue));
  e.push(text(145, 246, "AI worker\ndoes job", 19, P.white, 125, 52, "center"));
  e.push(arrow(320, 265, 110));
  card(e, 455, 190, 275, 155, "Control room", "logs\napprovals\nsettings\nhandoffs\nanalytics", P.yellow);
  e.push(arrow(755, 265, 110));
  card(e, 895, 190, 230, 155, "Customer trust", "what happened?\nwhy?\nwhat needs review?", P.green);
  e.push(rect(130, 450, 900, 50, "#191b1f", "#777"));
  e.push(text(160, 466, "Eval gym: run real work through the flow -> inspect failures -> improve controls.", 19, P.white, 850, 26));
  return scene("v3-wrapper-saas", e);
}
function pilot() {
  const e = []; title(e, "Sell the pilot like labor, then productize", "Same niche. Same workflow. Same promise.");
  card(e, 115, 205, 255, 150, "Pilot promise", "answer calls\nqualify demand\ntriage requests", P.yellow);
  e.push(arrow(395, 280, 110));
  card(e, 540, 205, 255, 150, "Simple pricing", "$1,500 setup\n+ $1,000/mo\nor outcome fee", P.blue);
  e.push(arrow(820, 280, 110));
  card(e, 965, 205, 190, 150, "Product pattern", "same scripts\nsame rules\nsame controls", P.green);
  e.push(text(150, 455, "You earn the software by doing the work first.", 27, P.teal, 800, 38));
  return scene("v3-pilot-productize", e);
}
function ownWorkflow() {
  const e = []; title(e, "Earn the software by doing the work first", "Productize the repeated pattern after real pilots.");
  card(e, 115, 200, 260, 160, "Manual + AI pilot", "do the work\nwatch breaks\nlearn approvals", P.rose);
  e.push(arrow(405, 280, 105));
  card(e, 540, 200, 260, 160, "Repeated pattern", "same scripts\nsame checks\nsame handoffs", P.green);
  e.push(arrow(830, 280, 105));
  card(e, 965, 200, 190, 160, "Product", "wrapper\nevals\npricing\nonboarding", P.yellow);
  e.push(text(145, 455, "Do the work first. Build software around what repeats.", 25, P.teal, 850, 35));
  return scene("v3-own-workflow", e);
}
function coverage() {
  const e = []; title(e, "Visual beats accounted for", "Dense-frame inventory drives the deck; presenter-only frames are excluded.");
  const rows = [
    ["Market + SaaS winners", "market / thesis"],
    ["SIT + scorecard", "workflow search"],
    ["Slang + home services + Samday", "wedge examples"],
    ["Shadow + smallest agent", "build method"],
    ["Architecture + wrapper + pilot + own workflow", "operating model"],
    ["Presenter-only frames", "excluded"],
  ];
  rows.forEach((r, i) => {
    const y = 155 + i * 62; e.push(rect(140, y, 880, 42, i % 2 ? "#171a1f" : "#20242a", "#5a626c"));
    e.push(text(165, y + 10, r[0], 16, P.white, 430, 20));
    e.push(text(650, y + 10, r[1], 16, i === 5 ? P.accent : P.teal, 310, 20));
  });
  return scene("v3-coverage-map", e);
}

const scenes = [market(), thesis(), economics(), workflowScore(), examples(), shadow(), smallAgent(), architecture(), wrapper(), pilot(), ownWorkflow(), coverage()];

async function postJson(url, body, method = "POST") {
  const res = await fetch(url, { method, headers: { "content-type": "application/json" }, body: body ? JSON.stringify(body) : undefined });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || data.success === false) throw new Error(`${method} ${url} failed: ${res.status} ${JSON.stringify(data)}`);
  return data;
}
async function renderScene(scene) {
  const excalidrawPath = path.join(RUN, `ai-agents-new-saas-${scene.name}.excalidraw`);
  const pngPath = path.join(RUN, `ai-agents-new-saas-${scene.name}.png`);
  fs.writeFileSync(excalidrawPath, JSON.stringify(scene.data, null, 2));
  await fetch(`${SERVER}/api/elements/clear`, { method: "DELETE" });
  await postJson(`${SERVER}/api/elements/sync`, { elements: scene.data.elements, timestamp: new Date().toISOString() });
  const exported = await postJson(`${SERVER}/api/export/image`, { format: "png", background: true });
  fs.writeFileSync(pngPath, Buffer.from(exported.data, "base64"));
  console.log(`${scene.name}: ${path.basename(excalidrawPath)} -> ${path.basename(pngPath)}`);
}
async function main() { for (const s of scenes) await renderScene(s); }
main().catch((err) => { console.error(err); process.exit(1); });
