# Browser Testing Across Codex And Claude Code

This repo supports Playwright browser validation in both Codex and Claude Code.
Use the same npm scripts in either host.

## LLM Wiki Agent Demo

Headless smoke test:

```bash
npm run browser:test
```

Visible browser test:

```bash
npm run browser:test:headed
```

Manual preview server:

```bash
npm run browser:demo
```

Then open:

```text
http://127.0.0.1:8766/
```

## Browser Resolution

The demo Playwright config resolves Chromium in this order:

1. `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`
2. cached Playwright Chromium under `~/.cache/ms-playwright`
3. common system binaries such as `/snap/bin/chromium`, `/usr/bin/chromium`,
   `/usr/bin/google-chrome`, and macOS Google Chrome

To force a browser:

```bash
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/snap/bin/chromium npm run browser:test
```

To install Playwright's managed Chromium:

```bash
npm run test:e2e:install
```

## Codex Notes

- Headless mode is preferred for verification.
- Headed mode needs GUI permission and a working desktop display.
- In this sandbox, Snap Chromium may require escalation for headed or headless
  launches because `snap-confine` needs host capabilities.

## Claude Code Notes

- Headless mode works in most terminal sessions once Chromium is installed.
- Headed mode requires a real display: local desktop, WSLg, X server, VNC, or a
  VS Code/browser environment that can open windows.
- If headed mode fails with a display error, use headless mode or VS Code Simple
  Browser for manual viewing.

## Existing App E2E Tests

The existing Next.js tests still use the root config:

```bash
npm run test:e2e
npm run test:e2e:headed
npm run test:e2e:kyc
```

The LLM Wiki Agent demo uses `playwright.demo.config.ts` so its static server
does not interfere with the app server on port `3000`.
