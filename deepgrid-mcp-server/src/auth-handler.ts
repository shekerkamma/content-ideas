import type {
  AuthRequest,
  OAuthHelpers
} from "@cloudflare/workers-oauth-provider";
import { Hono, type Context } from "hono";
import type { Env } from "./server";

interface Brief {
  id: string;
  title: string;
  markdown: string;
  createdAt: string;
  expiresAt: string;
}

type Bindings = Env & { OAUTH_PROVIDER: OAuthHelpers };
const app = new Hono<{ Bindings: Bindings }>();
const TRUST_COOKIE_NAME = "deepgrid_trusted_browser";
const TRUST_TTL_SECONDS = 30 * 24 * 60 * 60;

function escapeHtml(value: string) {
  return value.replace(/[&<>'"]/g, (character) => {
    const entities: Record<string, string> = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "'": "&#39;",
      '"': "&quot;"
    };
    return entities[character];
  });
}

async function passwordMatches(provided: string, expected: string) {
  const encoder = new TextEncoder();
  const [providedHash, expectedHash] = await Promise.all([
    crypto.subtle.digest("SHA-256", encoder.encode(provided)),
    crypto.subtle.digest("SHA-256", encoder.encode(expected))
  ]);
  const left = new Uint8Array(providedHash);
  const right = new Uint8Array(expectedHash);
  let difference = left.length ^ right.length;
  for (let index = 0; index < Math.max(left.length, right.length); index += 1) {
    difference |= (left[index] ?? 0) ^ (right[index] ?? 0);
  }
  return difference === 0;
}

function encodeBase64Url(value: Uint8Array | string) {
  const bytes = typeof value === "string" ? new TextEncoder().encode(value) : value;
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary).replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/, "");
}

function decodeBase64Url(value: string) {
  const padded = value.replaceAll("-", "+").replaceAll("_", "/").padEnd(
    Math.ceil(value.length / 4) * 4,
    "="
  );
  const binary = atob(padded);
  return new TextDecoder().decode(Uint8Array.from(binary, (character) => character.charCodeAt(0)));
}

async function signTrustPayload(payload: string, password: string) {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(password),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const signature = await crypto.subtle.sign(
    "HMAC",
    key,
    new TextEncoder().encode(`deepgrid-trust-v1.${payload}`)
  );
  return encodeBase64Url(new Uint8Array(signature));
}

function readCookie(request: Request, name: string) {
  const cookies = request.headers.get("Cookie") ?? "";
  for (const entry of cookies.split(";")) {
    const separator = entry.indexOf("=");
    if (separator < 0) continue;
    if (entry.slice(0, separator).trim() === name) {
      return entry.slice(separator + 1).trim();
    }
  }
  return undefined;
}

async function createTrustCookie(password: string) {
  const payload = encodeBase64Url(
    JSON.stringify({ version: 1, expiresAt: Date.now() + TRUST_TTL_SECONDS * 1000 })
  );
  const signature = await signTrustPayload(payload, password);
  return `${TRUST_COOKIE_NAME}=${payload}.${signature}; Max-Age=${TRUST_TTL_SECONDS}; Path=/; HttpOnly; Secure; SameSite=Lax`;
}

async function hasValidTrustCookie(request: Request, password: string) {
  const token = readCookie(request, TRUST_COOKIE_NAME);
  if (!token) return false;
  const [payload, suppliedSignature, extra] = token.split(".");
  if (!payload || !suppliedSignature || extra) return false;
  const expectedSignature = await signTrustPayload(payload, password);
  if (!(await passwordMatches(suppliedSignature, expectedSignature))) return false;
  try {
    const parsed = JSON.parse(decodeBase64Url(payload)) as {
      version?: number;
      expiresAt?: number;
    };
    return parsed.version === 1 &&
      typeof parsed.expiresAt === "number" &&
      parsed.expiresAt > Date.now();
  } catch {
    return false;
  }
}

async function completeAuthorization(
  c: Context<{ Bindings: Bindings }>,
  oauthRequest: AuthRequest,
  clientName: string,
  rememberBrowser: boolean
) {
  const { redirectTo } = await c.env.OAUTH_PROVIDER.completeAuthorization({
    request: oauthRequest,
    userId: "shekerkamma",
    metadata: {
      label: "DeepGrid market intelligence",
      clientName
    },
    scope: oauthRequest.scope,
    props: { userId: "shekerkamma", username: "Sheker Kamma" }
  });
  const response = c.redirect(redirectTo, 302);
  response.headers.set("Cache-Control", "no-store");
  if (rememberBrowser) {
    response.headers.append("Set-Cookie", await createTrustCookie(c.env.SHARED_PASSWORD));
  }
  return response;
}

function authorizationPage(
  nonce: string,
  clientName: string,
  clientUri: string | undefined,
  scopes: string[],
  error?: string
) {
  return `<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>Authorize DeepGrid tools</title>
<style>:root{font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:#f7f8fa;background:#071014}body{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px}main{width:min(520px,100%);background:#0f1b20;border:1px solid #29404a;border-radius:18px;padding:30px;box-shadow:0 24px 80px #0008}h1{margin:0 0 8px;font-size:25px}.muted{color:#9eb0b8}.client{margin:22px 0;padding:14px;border-radius:10px;background:#14252c}label{display:block;margin:18px 0 7px;font-weight:650}input{box-sizing:border-box;width:100%;padding:12px;border:1px solid #41606c;border-radius:9px;background:#081317;color:#fff;font-size:16px}button{width:100%;margin-top:16px;padding:12px;border:0;border-radius:9px;background:#11b8cc;color:#041014;font-weight:800;font-size:16px;cursor:pointer}.error{padding:11px;border-radius:8px;background:#51252a;color:#ffd5d8}code,a{color:#8fe8f1}</style></head>
<body><main><h1>Authorize DeepGrid remote tools</h1><p class="muted">Enter the server password to allow this MCP client to refresh sources, read monitoring history, and create expiring share links.</p><p class="muted">Approval is remembered in this browser for 30 days using a signed, HttpOnly cookie.</p>
${error ? `<p class="error">${escapeHtml(error)}</p>` : ""}
<div class="client"><strong>${escapeHtml(clientName)}</strong>${clientUri ? `<br><a href="${escapeHtml(clientUri)}" rel="noreferrer">${escapeHtml(clientUri)}</a>` : ""}<p class="muted">Scopes: ${escapeHtml(scopes.join(", ") || "default")}</p></div>
<form method="post" action="/authorize"><input type="hidden" name="nonce" value="${escapeHtml(nonce)}"><label for="password">Server password</label><input id="password" name="password" type="password" autocomplete="current-password" required autofocus><button type="submit">Approve access</button></form>
</main></body></html>`;
}

app.get("/authorize", async (c) => {
  const oauthRequest = await c.env.OAUTH_PROVIDER.parseAuthRequest(c.req.raw);
  const client = await c.env.OAUTH_PROVIDER.lookupClient(oauthRequest.clientId);
  if (!client) return c.text("Invalid client_id", 400);
  if (
    c.env.SHARED_PASSWORD &&
    await hasValidTrustCookie(c.req.raw, c.env.SHARED_PASSWORD)
  ) {
    return completeAuthorization(
      c,
      oauthRequest,
      client.clientName || "MCP client",
      false
    );
  }
  const nonce = crypto.randomUUID();
  await c.env.OAUTH_KV.put(`authorization:${nonce}`, JSON.stringify(oauthRequest), {
    expirationTtl: 600
  });
  return c.html(
    authorizationPage(
      nonce,
      client.clientName || "MCP client",
      client.clientUri,
      oauthRequest.scope
    )
  );
});

app.post("/authorize", async (c) => {
  if (!c.env.SHARED_PASSWORD) {
    return c.text("SHARED_PASSWORD is not configured.", 503);
  }
  const form = await c.req.formData();
  const nonce = form.get("nonce");
  const password = form.get("password");
  if (typeof nonce !== "string" || typeof password !== "string") {
    return c.text("Missing authorization fields.", 400);
  }
  const oauthRequest = await c.env.OAUTH_KV.get<AuthRequest>(
    `authorization:${nonce}`,
    "json"
  );
  if (!oauthRequest) return c.text("Authorization request expired.", 400);
  const client = await c.env.OAUTH_PROVIDER.lookupClient(oauthRequest.clientId);
  if (!client) return c.text("Invalid client_id", 400);

  if (!(await passwordMatches(password, c.env.SHARED_PASSWORD))) {
    return c.html(
      authorizationPage(
        nonce,
        client.clientName || "MCP client",
        client.clientUri,
        oauthRequest.scope,
        "Incorrect password."
      ),
      401
    );
  }

  await c.env.OAUTH_KV.delete(`authorization:${nonce}`);
  return completeAuthorization(
    c,
    oauthRequest,
    client.clientName || "MCP client",
    true
  );
});

app.get("/brief/:id", async (c) => {
  const id = c.req.param("id");
  if (!/^[a-f0-9]{20}$/.test(id)) return c.text("Brief not found.", 404);
  const brief = await c.env.DEEPGRID_DATA.get<Brief>(`brief:${id}`, "json");
  if (!brief) return c.text("Brief not found or expired.", 404);
  return c.html(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(brief.title)}</title>
<style>body{margin:0;background:#071014;color:#eaf2f4;font:16px/1.65 Inter,ui-sans-serif,system-ui,sans-serif}main{max-width:860px;margin:auto;padding:48px 24px 80px}h1{line-height:1.2}.meta{color:#91a8b1;border-bottom:1px solid #29404a;padding-bottom:18px}pre{white-space:pre-wrap;word-break:break-word;font:15px/1.65 ui-monospace,SFMono-Regular,Consolas,monospace;background:#0f1b20;border:1px solid #29404a;border-radius:12px;padding:22px}</style></head>
<body><main><h1>${escapeHtml(brief.title)}</h1><p class="meta">Created ${escapeHtml(brief.createdAt)} · Expires ${escapeHtml(brief.expiresAt)} · Anyone with this link can read it.</p><pre>${escapeHtml(brief.markdown)}</pre></main></body></html>`);
});

app.get("/health", (c) =>
  c.json({
    ok: true,
    service: "deepgrid-market-intelligence-mcp",
    endpoint: "/mcp",
    authentication: "oauth-2.1-shared-password-trusted-browser"
  })
);

app.get("/", (c) =>
  c.html(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DeepGrid MCP</title><style>body{max-width:760px;margin:60px auto;padding:0 24px;background:#071014;color:#eaf2f4;font:16px/1.6 system-ui}code,a{color:#8fe8f1}</style></head><body><h1>DeepGrid Market Intelligence MCP</h1><p>Authenticated remote tools for source refresh, competitor-change monitoring, and expiring brief links.</p><p>MCP endpoint: <code>/mcp</code></p><p>Health check: <a href="/health">/health</a></p></body></html>`)
);

export { app as AuthHandler };
