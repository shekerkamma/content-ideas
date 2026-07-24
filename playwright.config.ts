import { existsSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { defineConfig, devices } from "@playwright/test";

const cachedChromium = path.join(
  homedir(),
  ".cache",
  "ms-playwright",
  "chromium-1223",
  "chrome-linux64",
  "chrome"
);
const chromiumExecutable =
  process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ||
  (existsSync(cachedChromium) ? cachedChromium : undefined);

// Port 3000 is owned by the repo's mcp_excalidraw server on dev machines, and
// `next dev` silently falls back to another port while webServer keeps polling
// the configured URL. Pin the e2e server to its own port instead.
const e2ePort = Number(process.env.E2E_PORT || 3100);

export default defineConfig({
  testDir: "./tests/e2e",
  outputDir: "./test-results/e2e",
  fullyParallel: true,
  reporter: [["list"], ["html", { open: "never" }]],
  retries: process.env.CI ? 1 : 0,
  use: {
    ...devices["Desktop Chrome"],
    baseURL: `http://127.0.0.1:${e2ePort}`,
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
    launchOptions: {
      args: ["--no-sandbox"],
      ...(chromiumExecutable ? { executablePath: chromiumExecutable } : {})
    }
  },
  webServer: {
    command: `npm run dev -- -p ${e2ePort}`,
    url: `http://127.0.0.1:${e2ePort}/domain-workflows/kyc-screening`,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000
  }
});
