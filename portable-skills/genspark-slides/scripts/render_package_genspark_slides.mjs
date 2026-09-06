#!/usr/bin/env node
import fs from "node:fs/promises";
import fssync from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import Module from "node:module";

Module.Module?._initPaths?.();
const require = createRequire(import.meta.url);

function arg(name, fallback = undefined) {
  const idx = process.argv.indexOf(`--${name}`);
  return idx >= 0 ? process.argv[idx + 1] : fallback;
}

const htmlDir = arg("html-dir");
const outPptx = arg("out-pptx");
const title = arg("title", "Genspark Recreated Slides");
const chrome = arg("chrome") || process.env.CHROME_PATH;

if (!htmlDir || !outPptx) {
  console.error("Usage: node render_package_genspark_slides.mjs --html-dir <dir> --out-pptx <file.pptx> [--title <title>] [--chrome <path>]");
  process.exit(2);
}

const pngDir = path.join(path.dirname(outPptx), `${path.basename(outPptx, ".pptx")}-renders`);
await fs.mkdir(pngDir, { recursive: true });
await fs.mkdir(path.dirname(outPptx), { recursive: true });

const htmlFiles = (await fs.readdir(htmlDir))
  .filter(name => /^slide-\d+\.html$/i.test(name))
  .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));

if (htmlFiles.length === 0) {
  throw new Error(`No slide-XX.html files found in ${htmlDir}`);
}

const { chromium } = require("playwright");
const pptxgen = require("pptxgenjs");

const launchOptions = { headless: true };
if (chrome) launchOptions.executablePath = chrome;

const browser = await chromium.launch(launchOptions);
const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
const pngs = [];

for (const name of htmlFiles) {
  const input = path.resolve(htmlDir, name);
  const output = path.join(pngDir, name.replace(/\.html$/i, ".png"));
  await page.goto(`file:///${input.replace(/\\/g, "/")}`, { waitUntil: "load", timeout: 30000 });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: output, clip: { x: 0, y: 0, width: 1280, height: 720 } });
  pngs.push(output);
}

await browser.close();

const pptx = new pptxgen();
pptx.defineLayout({ name: "GENSPARK_WIDE", width: 13.333333, height: 7.5 });
pptx.layout = "GENSPARK_WIDE";
pptx.author = "Codex";
pptx.subject = "Recreated from Genspark slide HTML";
pptx.title = title;
pptx.theme = { headFontFace: "Montserrat", bodyFontFace: "Inter", lang: "en-US" };

for (const png of pngs) {
  const slide = pptx.addSlide();
  slide.background = { color: "FFFFFF" };
  slide.addImage({ path: png, x: 0, y: 0, w: 13.333333, h: 7.5 });
}

await pptx.writeFile({ fileName: outPptx });

const stats = fssync.statSync(outPptx);
console.log(`Created ${outPptx}`);
console.log(`Slides: ${pngs.length}`);
console.log(`Bytes: ${stats.size}`);
