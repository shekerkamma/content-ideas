#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const RUN = "/home/shekerk/content-ideas/runs/2026-07-02-video-to-deck-rerun";
const SERVER = "http://127.0.0.1:3000";

const palette = {
  bg: "#111111",
  panel: "#1f1f1f",
  card: "#2b2b2b",
  green: "#20352f",
  blue: "#243447",
  yellow: "#3a2f1d",
  rose: "#3a2430",
  line: "#e9ecef",
  muted: "#cfd4da",
  accent: "#ffd43b",
  teal: "#63e6be",
  white: "#f8f9fa",
};

let counter = 0;
function id(prefix) {
  counter += 1;
  return `${prefix}_${counter}`;
}

function base(type, extra) {
  return {
    id: id(type),
    type,
    x: 0,
    y: 0,
    width: 100,
    height: 100,
    angle: 0,
    strokeColor: palette.line,
    backgroundColor: "transparent",
    fillStyle: "solid",
    strokeWidth: 2,
    strokeStyle: "solid",
    roughness: 1,
    opacity: 100,
    groupIds: [],
    frameId: null,
    roundness: null,
    seed: Math.floor(Math.random() * 1000000),
    version: 1,
    versionNonce: Math.floor(Math.random() * 1000000),
    isDeleted: false,
    boundElements: null,
    updated: Date.now(),
    link: null,
    locked: false,
    ...extra,
  };
}

function rect(x, y, width, height, fill = palette.card, stroke = palette.line) {
  return base("rectangle", {
    x,
    y,
    width,
    height,
    strokeColor: stroke,
    backgroundColor: fill,
    roundness: { type: 3 },
  });
}

function ellipse(x, y, width, height, fill = palette.blue, stroke = palette.line) {
  return base("ellipse", {
    x,
    y,
    width,
    height,
    strokeColor: stroke,
    backgroundColor: fill,
  });
}

function text(x, y, value, size = 20, color = palette.white, width = 400, height = 40) {
  return base("text", {
    x,
    y,
    width,
    height,
    strokeColor: color,
    backgroundColor: "transparent",
    text: value,
    fontSize: size,
    fontFamily: 1,
    textAlign: "left",
    verticalAlign: "top",
    baseline: Math.round(size * 1.25),
    originalText: value,
    autoResize: true,
    lineHeight: 1.25,
  });
}

function arrow(x, y, width, height = 0) {
  return base("arrow", {
    x,
    y,
    width,
    height,
    points: [[0, 0], [width, height]],
    endArrowhead: "arrow",
    startArrowhead: null,
    strokeColor: palette.line,
    backgroundColor: "transparent",
  });
}

function card(elements, x, y, w, h, title, body, fill = palette.card) {
  elements.push(rect(x, y, w, h, fill));
  elements.push(text(x + 18, y + 16, title, 20, palette.accent, w - 36, 30));
  elements.push(text(x + 18, y + 54, body, 15, palette.white, w - 36, h - 64));
}

function scene(name, elements) {
  return {
    name,
    data: {
      type: "excalidraw",
      version: 2,
      source: "video-to-deck-excalidraw-recreation",
      elements: [
        rect(0, 0, 1200, 675, palette.bg, palette.bg),
        ...elements,
      ],
      appState: {
        viewBackgroundColor: "#ffffff",
        gridSize: null,
      },
      files: {},
    },
  };
}

function unitEconomics() {
  const e = [];
  e.push(text(70, 48, "the unit economics crush", 28, palette.white, 600, 40));
  e.push(text(105, 120, "Cost per customer interaction", 18, palette.muted, 500, 28));
  card(e, 105, 170, 310, 105, "Human agent", "$3.00 - $6.00", palette.card);
  card(e, 515, 170, 310, 105, "AI agent", "$0.25 - $0.50", palette.blue);
  e.push(arrow(420, 222, 85));
  e.push(text(875, 202, "90% cost reduction", 24, palette.teal, 250, 40));
  const rows = [
    ["First response time", "Human: 6+ hrs", "AI: <4 min", "98% faster"],
    ["Resolution time", "Human: 32+ hrs", "AI: 32 min", "98% faster"],
    ["ROI year 1", "", "41%", ""],
    ["ROI year 2", "", "87%", ""],
    ["ROI year 3", "", "124%", ""],
    ["Leading orgs", "", "3.5x-8x return on $1 spent", ""],
  ];
  let y = 340;
  for (const r of rows) {
    e.push(rect(105, y, 920, 38, "#191919", "#555555"));
    e.push(text(124, y + 9, r[0], 14, palette.muted, 220, 20));
    e.push(text(365, y + 9, r[1], 14, palette.white, 150, 20));
    e.push(text(555, y + 9, r[2], 14, palette.teal, 260, 20));
    e.push(text(850, y + 9, r[3], 14, palette.teal, 150, 20));
    y += 44;
  }
  return scene("unit-economics", e);
}

function workflowScorecard() {
  const e = [];
  e.push(text(70, 48, "PICK A WORKFLOW WITH A PAYCHECK ATTACHED", 28, palette.accent, 780, 40));
  e.push(text(75, 90, "Find work that happens often, has a finish line, touches software, and costs money when dropped.", 15, palette.muted, 900, 24));
  e.push(text(75, 140, "SCORE THE JOB", 20, palette.white, 300, 30));
  const cards = [
    ["Frequency", "daily / hourly"],
    ["Pain", "missed calls\nslow replies\ndropped leads"],
    ["Pattern lens", "booking\ntriage\napproval\nchase"],
    ["Tools", "Gmail\nSlack\ndialer\ncalendar\napp/form"],
    ["Budget", "employee\nagency\nVA\nBPO"],
  ];
  cards.forEach((c, i) => card(e, 90 + i * 205, 200, 165, 145, c[0], c[1], i === 4 ? palette.green : palette.card));
  e.push(rect(105, 410, 935, 52, palette.rose, "#d6336c"));
  e.push(text(126, 426, "FIRST REP: pick one niche -> list 20 annoying jobs -> score each one.", 18, palette.white, 900, 24));
  return scene("workflow-scorecard", e);
}

function shadowHuman() {
  const e = [];
  e.push(text(70, 48, "SHADOW THE HUMAN BEFORE YOU BUILD", 28, palette.accent, 780, 40));
  e.push(text(75, 90, "The product is hidden inside the real workflow details.", 15, palette.muted, 760, 24));
  card(e, 105, 185, 240, 180, "WATCH 10-20 RUNS", "screen record\nnarrate steps\ncopy/paste spots\nedge cases\nmanager approvals", palette.card);
  e.push(arrow(370, 275, 130));
  card(e, 520, 185, 240, 180, "EXTRACT THE SPEC", "trigger\ncontext\ntools\nrules\napproval\nescalation\nsuccess", palette.yellow);
  e.push(arrow(785, 275, 130));
  card(e, 935, 185, 210, 180, "TRUSTED AGENT", "knows the job\nknows if stuck\nknows when to ask", palette.green);
  e.push(text(95, 430, "Example: home services CSR is ready during urgency, service area, capacity, membership, financing, and job value.", 17, palette.white, 950, 32));
  return scene("shadow-human", e);
}

function agenticWorkflows() {
  const e = [];
  e.push(text(80, 55, "Agentic workflows", 32, palette.white, 500, 44));
  e.push(text(80, 120, "Agentic workflows define the structure of how agents operate, communicate, hand off tasks, and collaborate toward shared objectives.", 19, palette.white, 960, 60));
  e.push(text(80, 208, "Unlike individual agents, workflows are predefined and static. Two common patterns are sequential and hierarchical.", 18, palette.muted, 940, 56));
  card(e, 90, 335, 465, 165, "Sequential workflows", "Predetermined control flow with defined execution paths. Best for repeatable processes such as approvals or compliance checks.", palette.card);
  card(e, 635, 335, 465, 165, "Hierarchical workflows", "Structured delegation and review. Best when work needs oversight, escalation, and quality control across agent roles.", palette.green);
  return scene("agentic-workflows", e);
}

function wrapperSaas() {
  const e = [];
  e.push(text(70, 48, "THE WRAPPER MAKES IT SAAS", 28, palette.accent, 700, 40));
  e.push(text(75, 90, "The agent does the work. The control room creates trust.", 15, palette.muted, 760, 24));
  e.push(ellipse(105, 200, 170, 100, palette.blue));
  e.push(text(138, 232, "AI WORKER\nDOES JOB", 18, palette.white, 120, 50));
  e.push(arrow(300, 250, 130));
  card(e, 455, 180, 250, 160, "CONTROL ROOM", "logs\napprovals\nsettings\nhandoffs\nanalytics\npolicy editor", palette.yellow);
  e.push(arrow(730, 250, 130));
  card(e, 890, 180, 230, 160, "CUSTOMER TRUST", "what happened?\nwhy?\nwhat needs review?\nwhere did it fail?", palette.green);
  e.push(rect(110, 430, 935, 52, "#191919", "#777777"));
  e.push(text(130, 446, "EVAL GYM: 50 real calls / tickets / leads -> run the agent -> find failure modes -> improve.", 17, palette.white, 890, 24));
  return scene("wrapper-saas", e);
}

function pilotProductize() {
  const e = [];
  e.push(text(70, 48, "SELL THE PILOT LIKE LABOR, THEN PRODUCTIZE", 28, palette.accent, 900, 40));
  e.push(text(75, 90, "Three customers. Same niche. Same workflow. Same pain.", 15, palette.muted, 760, 24));
  card(e, 100, 190, 245, 160, "PILOT PROMISE", "We will answer and qualify missed calls.\n\nWe will triage maintenance requests.", palette.yellow);
  e.push(arrow(370, 270, 130));
  card(e, 530, 190, 245, 160, "SIMPLE PRICING", "$1,500 setup\n+ $1,000/mo\n\nor\n$30/booked job", palette.blue);
  e.push(arrow(800, 270, 130));
  card(e, 960, 190, 220, 160, "PRODUCT PATTERN", "Same scripts\nSame rules\nSame controls\nSame emails", palette.green);
  e.push(text(110, 445, "You earn the software by doing the work first.", 22, palette.white, 700, 35));
  return scene("pilot-productize", e);
}

const scenes = [
  unitEconomics(),
  workflowScorecard(),
  shadowHuman(),
  agenticWorkflows(),
  wrapperSaas(),
  pilotProductize(),
];

async function postJson(url, body, method = "POST") {
  const res = await fetch(url, {
    method,
    headers: { "content-type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || data.success === false) {
    throw new Error(`${method} ${url} failed: ${res.status} ${JSON.stringify(data)}`);
  }
  return data;
}

async function renderScene(scene) {
  const excalidrawPath = path.join(RUN, `ai-agents-new-saas-${scene.name}.excalidraw`);
  const pngPath = path.join(RUN, `ai-agents-new-saas-${scene.name}.png`);
  fs.writeFileSync(excalidrawPath, JSON.stringify(scene.data, null, 2));

  await fetch(`${SERVER}/api/elements/clear`, { method: "DELETE" });
  await postJson(`${SERVER}/api/elements/sync`, {
    elements: scene.data.elements,
    timestamp: new Date().toISOString(),
  });
  const exported = await postJson(`${SERVER}/api/export/image`, { format: "png", background: true });
  fs.writeFileSync(pngPath, Buffer.from(exported.data, "base64"));
  console.log(`${scene.name}: ${path.basename(excalidrawPath)} -> ${path.basename(pngPath)}`);
}

async function main() {
  for (const s of scenes) {
    await renderScene(s);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
