#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const RUN = "/home/shekerk/content-ideas/runs/2026-07-02-video-to-deck-rerun";
const SERVER = "http://127.0.0.1:3000";
const P = {
  bg: "#101113", card: "#22262c", blue: "#1f3447", green: "#173c31",
  yellow: "#42351a", rose: "#432231", line: "#f1f3f5", muted: "#c8ced6",
  accent: "#ffd43b", teal: "#63e6be", white: "#ffffff",
};
let seq = 0;
function id(prefix) { seq += 1; return `${prefix}_${seq}`; }
function base(type, extra) {
  return { id: id(type), type, x: 0, y: 0, width: 100, height: 100, angle: 0,
    strokeColor: P.line, backgroundColor: "transparent", fillStyle: "solid",
    strokeWidth: 2, strokeStyle: "solid", roughness: 1.2, opacity: 100,
    groupIds: [], frameId: null, roundness: null, seed: 4000 + seq,
    version: 1, versionNonce: 5000 + seq, isDeleted: false, boundElements: null,
    updated: Date.now(), link: null, locked: false, ...extra };
}
function rect(x, y, w, h, fill = P.card, stroke = P.line) {
  return base("rectangle", { x, y, width: w, height: h, backgroundColor: fill, strokeColor: stroke, roundness: { type: 3 } });
}
function text(x, y, value, size = 20, color = P.white, width = 500, height = 40, align = "left") {
  return base("text", { x, y, width, height, strokeColor: color, backgroundColor: "transparent", text: value,
    originalText: value, fontSize: size, fontFamily: 1, textAlign: align, verticalAlign: "top",
    autoResize: true, lineHeight: 1.2, baseline: Math.round(size * 1.15) });
}
function arrow(x, y, w, h = 0) {
  return base("arrow", { x, y, width: w, height: h, points: [[0, 0], [w, h]], endArrowhead: "arrow", strokeColor: P.line });
}
function card(e, x, y, w, h, title, body, fill = P.card) {
  e.push(rect(x, y, w, h, fill));
  e.push(text(x + 18, y + 15, title, 20, P.accent, w - 36, 28));
  e.push(text(x + 18, y + 55, body, 15, P.white, w - 36, h - 62));
}
function scene(name, elements) {
  return { name, data: { type: "excalidraw", version: 2, source: "video-to-deck-v4-zero-to-100",
    elements: [rect(0, 0, 1200, 675, P.bg, P.bg), ...elements],
    appState: { viewBackgroundColor: "#ffffff", gridSize: null }, files: {} } };
}
function zeroTo100() {
  const e = [];
  e.push(text(64, 42, "The zero-to-100 plan in 30 days", 31, P.white, 900, 42));
  e.push(text(68, 88, "Distribution is workflow teardowns: old way -> agent way -> painkiller.", 16, P.muted, 980, 24));
  const cols = [
    ["Days 1-3", "Pick one niche\nList 20 annoying jobs\nScore pain + budget"],
    ["Week 1", "Shadow operators\nWrite trigger/context/rules\nBuild eval set"],
    ["Week 2", "Ship smallest useful agent\nDraft / triage / coordinate / act"],
    ["Week 3", "Sell 3 pilots\nSetup + monthly\nSame niche, same workflow"],
    ["Week 4", "Publish teardown engine\n50 posts\nChecklists + benchmarks\nAds behind winners"],
  ];
  cols.forEach((c, i) => {
    card(e, 65 + i * 220, 180, 180, 180, c[0], c[1], [P.rose, P.yellow, P.blue, P.green, P.card][i]);
    if (i < 4) e.push(arrow(250 + i * 220, 390, 45));
  });
  e.push(rect(135, 455, 910, 60, "#191b1f", "#777"));
  e.push(text(170, 473, "Show the painful old way, show the agent way, sell the painkiller.", 23, P.teal, 860, 30));
  return scene("v4-zero-to-100-plan", e);
}
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
renderScene(zeroTo100()).catch((err) => { console.error(err); process.exit(1); });
