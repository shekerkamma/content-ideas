# Playwright

Run the browser smoke tests with:

```bash
npm run test:e2e
```

Run only the KYC workflow test:

```bash
npm run test:e2e:kyc
```

Open a visible Chromium browser:

```bash
npm run test:e2e:headed
```

If the Playwright browser cache is missing, install Chromium:

```bash
npm run test:e2e:install
```

The config uses `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` when set. Otherwise it
falls back to the cached Chromium under `~/.cache/ms-playwright` when present,
then to Playwright's default browser resolution.
