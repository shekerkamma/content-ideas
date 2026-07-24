import { existsSync, readdirSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { defineConfig, devices } from "@playwright/test";

const demoPort = process.env.LLM_WIKI_DEMO_PORT || "8766";
const demoUrl = `http://127.0.0.1:${demoPort}`;

function firstExisting(paths: string[]): string | undefined {
  return paths.find((candidate) => existsSync(candidate));
}

function cachedChromium(): string | undefined {
  const root = path.join(homedir(), ".cache", "ms-playwright");
  if (!existsSync(root)) return undefined;

  const candidates = readdirSync(root)
    .filter((name) => name.startsWith("chromium-"))
    .sort()
    .reverse()
    .map((name) => path.join(root, name, "chrome-linux64", "chrome"));

  return firstExisting(candidates);
}

const chromiumExecutable =
  process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ||
  cachedChromium() ||
  firstExisting([
    "/snap/bin/chromium",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  ]);

export default defineConfig({
  testDir: "./tests/browser",
  outputDir: "./test-results/browser",
  fullyParallel: false,
  reporter: [["list"], ["html", { outputFolder: "playwright-report/browser", open: "never" }]],
  retries: process.env.CI ? 1 : 0,
  use: {
    ...devices["Desktop Chrome"],
    baseURL: demoUrl,
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
    launchOptions: {
      args: ["--no-sandbox"],
      ...(chromiumExecutable ? { executablePath: chromiumExecutable } : {})
    }
  },
  webServer: {
    command: `python3 -m http.server ${demoPort} --bind 127.0.0.1 --directory runs/2026-07-04-fable5-llm-wiki-pattern/interactive-demo`,
    url: demoUrl,
    reuseExistingServer: !process.env.CI,
    timeout: 30_000
  }
});
