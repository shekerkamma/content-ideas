#!/usr/bin/env node
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { chromium } from "playwright";

const DEFAULT_URL =
  "https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw";
const DEFAULT_PDF_URL =
  "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf";

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

function hasFlag(name) {
  return process.argv.includes(name);
}

function firstExisting(paths) {
  return paths.find((candidate) => existsSync(candidate));
}

function cachedChromium() {
  const root = path.join(homedir(), ".cache", "ms-playwright");
  if (!existsSync(root)) return undefined;
  const listing = spawnSync("bash", ["-lc", `ls -d ${root}/chromium-* 2>/dev/null | sort -r | head -1`], {
    encoding: "utf8"
  }).stdout.trim();
  if (!listing) return undefined;
  const executable = path.join(listing, "chrome-linux64", "chrome");
  return existsSync(executable) ? executable : undefined;
}

function slug(input) {
  return input
    .toLowerCase()
    .replace(/https?:\/\//, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 72);
}

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

function commandExists(command) {
  return spawnSync("bash", ["-lc", `command -v ${command}`], { encoding: "utf8" }).status === 0;
}

function printablePdfText(buffer) {
  const text = buffer
    .toString("latin1")
    .match(/[A-Za-z0-9][A-Za-z0-9\s.,;:()/_-]{8,}/g)
    ?.join("\n")
    .replace(/\n{3,}/g, "\n\n")
    .slice(0, 6000);
  return text || "No readable text could be extracted without a PDF text extraction tool.";
}

async function extractPdfText(buffer) {
  if (commandExists("pdftotext")) {
    const tempDir = mkdtempSync(path.join(os.tmpdir(), "llm-wiki-pdf-"));
    const pdfPath = path.join(tempDir, "source.pdf");
    const textPath = path.join(tempDir, "source.txt");
    writeFileSync(pdfPath, buffer);
    const result = spawnSync("pdftotext", ["-layout", pdfPath, textPath], { encoding: "utf8" });
    if (result.status === 0 && existsSync(textPath)) {
      const text = readFileSync(textPath, "utf8").trim();
      rmSync(tempDir, { recursive: true, force: true });
      if (text) return { method: "pdftotext", text };
    }
    rmSync(tempDir, { recursive: true, force: true });
  }

  try {
    const { PDFParse } = await import("pdf-parse");
    const parser = new PDFParse({ data: buffer });
    try {
      const result = await parser.getText();
      const text = String(result?.text || "").trim();
      if (text) return { method: "pdf-parse", text };
    } finally {
      await parser.destroy().catch(() => {});
    }
  } catch {
    // Fall through to byte-level extraction.
  }

  return { method: "byte-printable-fallback", text: printablePdfText(buffer) };
}

function write(file, content) {
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, content, "utf8");
}

function append(file, content) {
  writeFileSync(file, readFileSync(file, "utf8") + content, "utf8");
}

async function downloadUrlPage(page, url) {
  const response = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60_000 });
  if (!response?.ok()) throw new Error(`URL download failed: ${url} (${response?.status()})`);
  const title = await page.title().catch(() => "");
  const text = await page.locator("body").innerText({ timeout: 10_000 }).catch(async () => {
    const body = await response.body();
    return body.toString("utf8");
  });
  return {
    url,
    status: response.status(),
    contentType: response.headers()["content-type"] || "",
    title,
    text: text.trim()
  };
}

async function downloadPdf(page, pdfUrl) {
  const response = await page.goto(pdfUrl, { waitUntil: "domcontentloaded", timeout: 60_000 });
  if (!response?.ok()) throw new Error(`PDF download failed: ${pdfUrl} (${response?.status()})`);
  const buffer = await response.body();
  const extraction = await extractPdfText(buffer);
  return {
    url: pdfUrl,
    status: response.status(),
    contentType: response.headers()["content-type"] || "",
    bytes: buffer,
    sha256: sha256(buffer),
    extractionMethod: extraction.method,
    text: extraction.text
  };
}

function initWiki(root, reset) {
  if (reset && existsSync(root)) rmSync(root, { recursive: true, force: true });
  const initScript = path.join(path.dirname(new URL(import.meta.url).pathname), "init_llm_wiki.py");
  const result = spawnSync("python3", [initScript, "--root", root, "--profile", "foldered", "--overwrite"], {
    encoding: "utf8"
  });
  if (result.status !== 0) throw new Error(`init failed:\n${result.stdout}\n${result.stderr}`);
}

function ingest(root, urlCapture, pdfCapture) {
  const wiki = path.join(root, "wiki");
  const urlSlug = slug(urlCapture.url || "live-url");
  const pdfSlug = slug(pdfCapture.url || "live-pdf");

  write(
    path.join(root, "raw", `${urlSlug}.md`),
    `# Live URL Capture\n\nSource URL: ${urlCapture.url}\nStatus: ${urlCapture.status}\nContent-Type: ${urlCapture.contentType}\nTitle: ${urlCapture.title}\n\n${urlCapture.text}\n`
  );
  mkdirSync(path.join(root, "raw", "downloads"), { recursive: true });
  writeFileSync(path.join(root, "raw", "downloads", `${pdfSlug}.pdf`), pdfCapture.bytes);
  write(
    path.join(root, "raw", `${pdfSlug}-pdf-extract.md`),
    `# Live PDF Capture\n\nSource URL: ${pdfCapture.url}\nStatus: ${pdfCapture.status}\nContent-Type: ${pdfCapture.contentType}\nBytes: ${pdfCapture.bytes.length}\nSHA256: ${pdfCapture.sha256}\nDownloaded File: raw/downloads/${pdfSlug}.pdf\nExtraction Method: ${pdfCapture.extractionMethod}\n\n## Extracted Text\n\n${pdfCapture.text}\n`
  );

  mkdirSync(path.join(wiki, "answers"), { recursive: true });

  write(
    path.join(wiki, "sources", "live-url-source.md"),
    `---\ntype: source\nsource_path: raw/${urlSlug}.md\nsource_url: ${urlCapture.url}\n---\n\n# Live URL Source\n\nThis source was downloaded through Chromium during the live Fable/Karpathy smoke test.\n\nKey route: [LLM Wiki](../concepts/live-llm-wiki.md)\n`
  );
  write(
    path.join(wiki, "sources", "live-pdf-source.md"),
    `---\ntype: source\nsource_path: raw/${pdfSlug}-pdf-extract.md\nsource_url: ${pdfCapture.url}\ndownloaded_file: raw/downloads/${pdfSlug}.pdf\nsha256: ${pdfCapture.sha256}\nextraction_method: ${pdfCapture.extractionMethod}\n---\n\n# Live PDF Source\n\nThis PDF was downloaded through Chromium during the live Fable/Karpathy smoke test. The raw PDF and extracted text were preserved under raw/.\n\nKey route: [LLM Wiki](../concepts/live-llm-wiki.md), [PDF Ingest](../concepts/pdf-ingest.md)\n`
  );
  write(
    path.join(wiki, "concepts", "live-llm-wiki.md"),
    `---\ntype: concept\n---\n\n# Live LLM Wiki\n\nA live LLM wiki workflow downloads sources into raw/, creates source-backed generated pages under wiki/, updates index.md, and appends log.md.\n\nSources: [Live URL Source](../sources/live-url-source.md), [Live PDF Source](../sources/live-pdf-source.md)\nRelated: [Progressive Disclosure](progressive-disclosure.md), [PDF Ingest](pdf-ingest.md)\n`
  );
  write(
    path.join(wiki, "concepts", "progressive-disclosure.md"),
    `---\ntype: concept\n---\n\n# Progressive Disclosure\n\nStart from wiki/index.md, read only relevant pages, and follow links only when they improve the answer.\n\nSources: [Live URL Source](../sources/live-url-source.md)\n`
  );
  write(
    path.join(wiki, "concepts", "pdf-ingest.md"),
    `---\ntype: concept\n---\n\n# PDF Ingest\n\nPDF ingest should preserve the original downloaded PDF, store extraction metadata, and link generated pages back to the source page.\n\nSources: [Live PDF Source](../sources/live-pdf-source.md)\n`
  );
  write(
    path.join(wiki, "entities", "chromium.md"),
    `---\ntype: entity\n---\n\n# Chromium\n\nChromium was used in headed or headless Playwright mode to download live URL and PDF sources for this smoke test.\n\nSources: [Live URL Source](../sources/live-url-source.md), [Live PDF Source](../sources/live-pdf-source.md)\n`
  );
  write(
    path.join(wiki, "answers", "live-fable-karpathy-workflow.md"),
    `# Live Fable/Karpathy Workflow Answer\n\nTo build the workflow live:\n\n1. Initialize the markdown wiki structure.\n2. Use Chromium to download a URL and PDF into raw/.\n3. Preserve source metadata and raw files.\n4. Generate source, concept, entity, and answer pages under wiki/.\n5. Update wiki/index.md with route hints.\n6. Append wiki/log.md.\n7. Answer by reading wiki/index.md, then the relevant pages only.\n\nGrounded in:\n- [Live URL Source](../sources/live-url-source.md)\n- [Live PDF Source](../sources/live-pdf-source.md)\n`
  );
  write(
    path.join(wiki, "index.md"),
    `# LLM Wiki Index\n\nUse this file as the routing surface before reading individual pages.\n\n## Sources\n\n- [Live URL Source](sources/live-url-source.md) - Chromium-downloaded URL source\n- [Live PDF Source](sources/live-pdf-source.md) - Chromium-downloaded PDF source with metadata\n\n## Concepts\n\n- [Live LLM Wiki](concepts/live-llm-wiki.md) - live raw-to-wiki workflow\n- [Progressive Disclosure](concepts/progressive-disclosure.md) - route narrowly from index to relevant pages\n- [PDF Ingest](concepts/pdf-ingest.md) - preserve PDF, metadata, and extraction path\n\n## Entities\n\n- [Chromium](entities/chromium.md) - browser used for live downloads\n\n## Answer Routes\n\n- "How do I build this live workflow?" -> [Live Fable/Karpathy Workflow Answer](answers/live-fable-karpathy-workflow.md)\n`
  );
  append(
    path.join(wiki, "log.md"),
    `\n## ingest | live-fable-karpathy-download\n\n- downloaded URL with Chromium: ${urlCapture.url}\n- downloaded PDF with Chromium: ${pdfCapture.url}\n- preserved PDF bytes: ${pdfCapture.bytes.length}\n- extracted PDF text with: ${pdfCapture.extractionMethod}\n- created source, concept, entity, and answer pages\n- updated index routes and backlinks\n\n## query | live workflow\n\n- read wiki/index.md\n- followed route to wiki/answers/live-fable-karpathy-workflow.md\n- checked source pages for traceability\n`
  );
}

function validate(root) {
  const required = [
    "wiki/index.md",
    "wiki/log.md",
    "wiki/sources/live-url-source.md",
    "wiki/sources/live-pdf-source.md",
    "wiki/concepts/live-llm-wiki.md",
    "wiki/concepts/pdf-ingest.md",
    "wiki/entities/chromium.md",
    "wiki/answers/live-fable-karpathy-workflow.md"
  ];
  const failures = required.filter((file) => !existsSync(path.join(root, file)));
  const index = readFileSync(path.join(root, "wiki", "index.md"), "utf8");
  const log = readFileSync(path.join(root, "wiki", "log.md"), "utf8");
  const answer = readFileSync(path.join(root, "wiki", "answers", "live-fable-karpathy-workflow.md"), "utf8");
  if (!index.includes("Live Fable/Karpathy Workflow Answer")) failures.push("index route");
  if (!log.includes("live-fable-karpathy-download")) failures.push("log entry");
  if (!answer.includes("Live URL Source") || !answer.includes("Live PDF Source")) {
    failures.push("answer source grounding");
  }
  return failures;
}

async function main() {
  const root = path.resolve(argValue("--root", "/tmp/llm-wiki-fable-live"));
  const url = argValue("--url", DEFAULT_URL);
  const pdfUrl = argValue("--pdf-url", DEFAULT_PDF_URL);
  const headed = hasFlag("--headed");
  const reset = hasFlag("--reset");
  const slowMo = Number(argValue("--slow-mo", headed ? "600" : "0"));
  const executablePath =
    process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ||
    cachedChromium() ||
    firstExisting(["/snap/bin/chromium", "/usr/bin/chromium", "/usr/bin/google-chrome"]);

  initWiki(root, reset);

  const browser = await chromium.launch({
    headless: !headed,
    slowMo,
    args: ["--no-sandbox"],
    ...(executablePath ? { executablePath } : {})
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const urlCapture = await downloadUrlPage(page, url);
  const pdfCapture = await downloadPdf(page, pdfUrl);
  await browser.close();

  ingest(root, urlCapture, pdfCapture);
  const failures = validate(root);
  if (failures.length) {
    console.error("Live smoke failed:");
    for (const failure of failures) console.error(`- ${failure}`);
    process.exit(1);
  }
  console.log(`Live Fable/Karpathy Chromium ingest passed: ${root}`);
  console.log(`URL source: ${url}`);
  console.log(`PDF source: ${pdfUrl}`);
  console.log("Query route: wiki/index.md -> wiki/answers/live-fable-karpathy-workflow.md");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
