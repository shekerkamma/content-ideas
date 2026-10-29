# DeepGrid Market Intelligence MCP

Authenticated remote MCP server for the DeepGrid India ADAS competitor dossier.

- Server: `https://deepgrid-market-intelligence-mcp.shekerkamma.workers.dev`
- MCP endpoint: `/mcp`
- Health endpoint: `/health`
- Schedule: daily at 03:17 UTC / 08:47 IST

## Tools

- `refresh_market_intelligence` fetches fixed, allowlisted competitor sources, hashes snapshots, and records detected changes in Cloudflare KV.
- `monitor_competitor_changes` reads saved source status and change history without fetching external pages.
- `share_brief` publishes supplied Markdown as an unlisted, expiring public-by-link brief.

## Security model

- OAuth 2.1 dynamic client registration and authorization-code flow with PKCE.
- A shared owner password protects the authorization page. The password is stored as a Cloudflare Worker secret.
- Successful approval sets a signed, HttpOnly, Secure, SameSite=Lax browser cookie for 30 days. Later OAuth connections auto-approve without exposing or resubmitting the password.
- Browser access is limited by CORS to the GitHub Pages origin and local development origins.
- Refresh accepts competitor identifiers, not arbitrary URLs. Source URLs are fixed in `src/sources.ts`.
- Access tokens live in the website tab's `sessionStorage`, not persistent browser storage.
- Shared briefs are public to anyone who has the random link until expiry; do not submit confidential material.

## Local setup

Use Node 22. Copy `.dev.vars.example` to `.dev.vars` and set a strong local password. Never commit `.dev.vars`.

```sh
npm ci
npm run typecheck
npm run build
npm run dev
```

## Cloudflare setup and deployment

The production KV namespace IDs and daily trigger are in `wrangler.jsonc`. Upload the password separately, then deploy:

```sh
npx wrangler secret put SHARED_PASSWORD
npm run deploy
```

Run the end-to-end OAuth and MCP smoke test with the password supplied only in the process environment:

```sh
SHARED_PASSWORD='...' npm run smoke -- \
  https://deepgrid-market-intelligence-mcp.shekerkamma.workers.dev
```

The smoke test checks health, CORS, OAuth/PKCE, trusted-browser auto-approval, tool discovery, a read-only monitor call, one allowlisted refresh, and an expiring brief round trip.

## Source map

- `src/server.ts` — MCP tools, health route, brief route, and scheduled refresh
- `src/auth-handler.ts` — password authorization UI and OAuth approval
- `src/sources.ts` — allowlisted competitor sources
- `test/oauth-smoke.mjs` — production protocol smoke test
- `wrangler.jsonc` — Worker, KV, compatibility, and cron configuration
