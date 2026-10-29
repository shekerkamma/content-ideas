import crypto from "node:crypto";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const baseUrl = process.env.MCP_BASE_URL ?? "http://127.0.0.1:5173";
const password =
  process.env.MCP_TEST_PASSWORD ??
  process.env.SHARED_PASSWORD ??
  "local-test-only";
const redirectUri = "http://127.0.0.1:7777/callback";

function base64url(value) {
  return Buffer.from(value).toString("base64url");
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const verifier = base64url(crypto.randomBytes(48));
const challenge = base64url(crypto.createHash("sha256").update(verifier).digest());
const state = base64url(crypto.randomBytes(24));

const health = await fetch(`${baseUrl}/health`, {
  headers: { Origin: "https://shekerkamma.github.io" }
});
assert(health.ok, `Health check failed: ${health.status}`);
assert(
  health.headers.get("access-control-allow-origin") ===
    "https://shekerkamma.github.io",
  "Expected GitHub Pages CORS origin."
);

const registrationResponse = await fetch(`${baseUrl}/oauth/register`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Origin: "https://shekerkamma.github.io"
  },
  body: JSON.stringify({
    client_name: "DeepGrid OAuth smoke test",
    redirect_uris: [redirectUri],
    token_endpoint_auth_method: "none",
    grant_types: ["authorization_code", "refresh_token"],
    response_types: ["code"]
  })
});
assert(registrationResponse.ok, `Registration failed: ${registrationResponse.status}`);
const registration = await registrationResponse.json();

const authorizeUrl = new URL(`${baseUrl}/authorize`);
authorizeUrl.search = new URLSearchParams({
  response_type: "code",
  client_id: registration.client_id,
  redirect_uri: redirectUri,
  code_challenge: challenge,
  code_challenge_method: "S256",
  state,
  resource: `${baseUrl}/mcp`
}).toString();
const approvalResponse = await fetch(authorizeUrl, { redirect: "manual" });
assert(approvalResponse.ok, `Authorization page failed: ${approvalResponse.status}`);
const approvalHtml = await approvalResponse.text();
const nonce = approvalHtml.match(/name="nonce" value="([^"]+)"/)?.[1];
assert(nonce, "Authorization nonce was not rendered.");

const approvalSubmit = await fetch(`${baseUrl}/authorize`, {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ nonce, password }),
  redirect: "manual"
});
assert(approvalSubmit.status === 302, `Approval failed: ${approvalSubmit.status}`);
const setCookie = approvalSubmit.headers.get("set-cookie") ?? "";
assert(setCookie.includes("deepgrid_trusted_browser="), "Trusted-browser cookie missing.");
assert(setCookie.includes("HttpOnly"), "Trusted-browser cookie must be HttpOnly.");
assert(setCookie.includes("Secure"), "Trusted-browser cookie must be Secure.");
assert(setCookie.includes("SameSite=Lax"), "Trusted-browser cookie must use SameSite=Lax.");
const trustCookie = setCookie.split(";", 1)[0];
const callback = new URL(approvalSubmit.headers.get("location"));
assert(callback.searchParams.get("state") === state, "OAuth state mismatch.");
const code = callback.searchParams.get("code");
assert(code, "OAuth authorization code missing.");

const rememberedVerifier = base64url(crypto.randomBytes(48));
const rememberedChallenge = base64url(
  crypto.createHash("sha256").update(rememberedVerifier).digest()
);
const rememberedState = base64url(crypto.randomBytes(24));
const rememberedAuthorizeUrl = new URL(authorizeUrl);
rememberedAuthorizeUrl.searchParams.set("code_challenge", rememberedChallenge);
rememberedAuthorizeUrl.searchParams.set("state", rememberedState);
const rememberedApproval = await fetch(rememberedAuthorizeUrl, {
  headers: { Cookie: trustCookie },
  redirect: "manual"
});
assert(rememberedApproval.status === 302, "Trusted browser was not auto-approved.");
const rememberedCallback = new URL(rememberedApproval.headers.get("location"));
assert(
  rememberedCallback.searchParams.get("state") === rememberedState,
  "Trusted-browser OAuth state mismatch."
);
assert(
  rememberedCallback.searchParams.get("code"),
  "Trusted-browser authorization code missing."
);

const tokenResponse = await fetch(`${baseUrl}/oauth/token`, {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
    Origin: "https://shekerkamma.github.io"
  },
  body: new URLSearchParams({
    grant_type: "authorization_code",
    client_id: registration.client_id,
    redirect_uri: redirectUri,
    code,
    code_verifier: verifier,
    resource: `${baseUrl}/mcp`
  })
});
assert(tokenResponse.ok, `Token exchange failed: ${tokenResponse.status}`);
const token = await tokenResponse.json();
assert(token.access_token, "OAuth access token missing.");

const client = new Client({ name: "deepgrid-smoke", version: "1.0.0" });
const transport = new StreamableHTTPClientTransport(new URL(`${baseUrl}/mcp`), {
  requestInit: { headers: { Authorization: `Bearer ${token.access_token}` } }
});
await client.connect(transport);
const listed = await client.listTools();
const names = listed.tools.map((tool) => tool.name).sort();
assert(
  JSON.stringify(names) ===
    JSON.stringify([
      "monitor_competitor_changes",
      "refresh_market_intelligence",
      "share_brief"
    ]),
  `Unexpected tool list: ${names.join(", ")}`
);

const monitor = await client.callTool({
  name: "monitor_competitor_changes",
  arguments: { limit: 5 }
});
assert(!monitor.isError, "Monitor tool returned an error.");

const refreshed = await client.callTool({
  name: "refresh_market_intelligence",
  arguments: { competitor: "Aptiv", force: true }
});
assert(!refreshed.isError, "Refresh tool returned an MCP error.");
const refreshPayload = JSON.parse(refreshed.content[0].text);
assert(refreshPayload.sourceCount === 1, "Refresh did not select exactly one Aptiv source.");

const shared = await client.callTool({
  name: "share_brief",
  arguments: {
    title: "DeepGrid smoke-test brief",
    markdown: "# Verified\n\nOAuth, KV persistence, and MCP execution passed.",
    expiresInDays: 1
  }
});
assert(!shared.isError, "Share tool returned an error.");
const sharedPayload = JSON.parse(shared.content[0].text);
const sharedPage = await fetch(sharedPayload.url);
assert(sharedPage.ok, `Shared brief readback failed: ${sharedPage.status}`);
assert((await sharedPage.text()).includes("OAuth, KV persistence"), "Shared brief content missing.");

await client.close();
console.log(
  JSON.stringify(
    {
      health: "ok",
      cors: "ok",
      oauth: "ok",
      trustedBrowser: "ok",
      tools: names,
      monitor: "ok",
      refresh: {
        status: "ok",
        outcome: refreshPayload.results[0]?.outcome,
        errors: refreshPayload.errorCount
      },
      shareBrief: "ok"
    },
    null,
    2
  )
);
