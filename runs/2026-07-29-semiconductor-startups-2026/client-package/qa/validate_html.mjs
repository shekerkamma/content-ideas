#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "@playwright/test";

const qaDir = path.dirname(new URL(import.meta.url).pathname);
const htmlPath = path.resolve(qaDir, "../site/index.html");
const outDir = path.resolve(qaDir, "html");
fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const report = {
  status: "passed",
  htmlPath,
  checks: {},
  consoleErrors: [],
  pageErrors: [],
  checkedAt: new Date().toISOString(),
};

try {
  for (const profile of [
    { name: "desktop", viewport: { width: 1440, height: 1000 } },
    { name: "mobile", viewport: { width: 390, height: 844 } },
  ]) {
    const page = await browser.newPage({ viewport: profile.viewport });
    page.on("console", (message) => {
      if (message.type() === "error") report.consoleErrors.push(message.text());
    });
    page.on("pageerror", (error) => report.pageErrors.push(error.message));
    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "load" });
    const h1 = (await page.locator("h1").textContent())?.trim();
    const sections = await page.locator("main section").count();
    const links = await page.locator("nav a").evaluateAll((nodes) =>
      nodes.map((node) => node.getAttribute("href"))
    );
    const missingTargets = await page.evaluate((hrefs) =>
      hrefs
        .filter((href) => href?.startsWith("#"))
        .filter((href) => !document.querySelector(href))
    , links);
    await page.screenshot({
      path: path.join(outDir, `${profile.name}.png`),
      fullPage: true,
    });
    report.checks[profile.name] = {
      h1,
      sections,
      navigationLinks: links.length,
      missingTargets,
      passed:
        Boolean(h1?.includes("Semiconductor Startups")) &&
        sections >= 40 &&
        links.length >= 6 &&
        missingTargets.length === 0,
    };
    await page.close();
  }
} finally {
  await browser.close();
}

if (
  Object.values(report.checks).some((check) => !check.passed) ||
  report.consoleErrors.length ||
  report.pageErrors.length
) {
  report.status = "failed";
}

fs.writeFileSync(
  path.join(outDir, "report.json"),
  `${JSON.stringify(report, null, 2)}\n`,
);
process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
process.exitCode = report.status === "passed" ? 0 : 1;
