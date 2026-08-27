import { useCallback, useEffect, useState } from "react";
import { createWebMcpProxy } from "webmcp-proxy";

const MCP_BASE_URL = (
  import.meta.env.VITE_DEEPGRID_MCP_URL ??
  "https://deepgrid-market-intelligence-mcp.shekerkamma.workers.dev"
).replace(/\/$/, "");
const ACCESS_TOKEN_KEY = "deepgrid-mcp-access-token";
const TOKEN_EXPIRY_KEY = "deepgrid-mcp-token-expiry";
const OAUTH_STATE_KEY = "deepgrid-mcp-oauth-state";
const OAUTH_VERIFIER_KEY = "deepgrid-mcp-oauth-verifier";
const OAUTH_CLIENT_KEY = "deepgrid-mcp-oauth-client";

type Status = "unconfigured" | "disconnected" | "authorizing" | "connected" | "error";

function base64url(bytes: Uint8Array) {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary).replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/, "");
}

function randomValue(size = 48) {
  return base64url(crypto.getRandomValues(new Uint8Array(size)));
}

async function pkceChallenge(verifier: string) {
  return base64url(
    new Uint8Array(
      await crypto.subtle.digest("SHA-256", new TextEncoder().encode(verifier))
    )
  );
}

function redirectUri() {
  return `${window.location.origin}${window.location.pathname}`;
}

function currentToken() {
  const token = sessionStorage.getItem(ACCESS_TOKEN_KEY);
  const expiry = Number(sessionStorage.getItem(TOKEN_EXPIRY_KEY) ?? "0");
  if (!token || !expiry || Date.now() >= expiry) {
    sessionStorage.removeItem(ACCESS_TOKEN_KEY);
    sessionStorage.removeItem(TOKEN_EXPIRY_KEY);
    return null;
  }
  return token;
}

async function registerClient() {
  const response = await fetch(`${MCP_BASE_URL}/oauth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      client_name: "DeepGrid competitor dossier",
      client_uri: redirectUri(),
      redirect_uris: [redirectUri()],
      token_endpoint_auth_method: "none",
      grant_types: ["authorization_code", "refresh_token"],
      response_types: ["code"]
    })
  });
  if (!response.ok) throw new Error(`MCP client registration failed (${response.status}).`);
  return (await response.json()) as { client_id: string };
}

export function RemoteMCPBridge() {
  const [status, setStatus] = useState<Status>(MCP_BASE_URL ? "disconnected" : "unconfigured");
  const [message, setMessage] = useState(
    MCP_BASE_URL ? "Remote tools are disconnected." : "Remote MCP deployment is pending."
  );

  const connect = useCallback(async () => {
    if (!MCP_BASE_URL) return;
    setStatus("authorizing");
    setMessage("Opening secure authorization…");
    try {
      const client = await registerClient();
      const verifier = randomValue();
      const state = randomValue(32);
      sessionStorage.setItem(OAUTH_CLIENT_KEY, client.client_id);
      sessionStorage.setItem(OAUTH_VERIFIER_KEY, verifier);
      sessionStorage.setItem(OAUTH_STATE_KEY, state);
      const authorize = new URL(`${MCP_BASE_URL}/authorize`);
      authorize.search = new URLSearchParams({
        response_type: "code",
        client_id: client.client_id,
        redirect_uri: redirectUri(),
        code_challenge: await pkceChallenge(verifier),
        code_challenge_method: "S256",
        state,
        scope: "deepgrid:read deepgrid:write",
        resource: `${MCP_BASE_URL}/mcp`
      }).toString();
      window.location.assign(authorize);
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : String(error));
    }
  }, []);

  const disconnect = useCallback(() => {
    sessionStorage.removeItem(ACCESS_TOKEN_KEY);
    sessionStorage.removeItem(TOKEN_EXPIRY_KEY);
    setStatus("disconnected");
    setMessage("Remote tools are disconnected.");
  }, []);

  useEffect(() => {
    if (!MCP_BASE_URL) return;
    const parameters = new URLSearchParams(window.location.search);
    const code = parameters.get("code");
    const returnedState = parameters.get("state");
    const oauthError = parameters.get("error");
    if (!code && !oauthError) return;

    const finishAuthorization = async () => {
      try {
        if (oauthError) {
          throw new Error(parameters.get("error_description") ?? oauthError);
        }
        if (!code) throw new Error("OAuth authorization code is missing.");
        const expectedState = sessionStorage.getItem(OAUTH_STATE_KEY);
        const verifier = sessionStorage.getItem(OAUTH_VERIFIER_KEY);
        const clientId = sessionStorage.getItem(OAUTH_CLIENT_KEY);
        if (!expectedState || returnedState !== expectedState || !verifier || !clientId) {
          throw new Error("OAuth callback validation failed. Start the connection again.");
        }
        const response = await fetch(`${MCP_BASE_URL}/oauth/token`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            grant_type: "authorization_code",
            client_id: clientId,
            redirect_uri: redirectUri(),
            code,
            code_verifier: verifier,
            resource: `${MCP_BASE_URL}/mcp`
          })
        });
        if (!response.ok) throw new Error(`Token exchange failed (${response.status}).`);
        const tokens = (await response.json()) as {
          access_token: string;
          expires_in?: number;
        };
        sessionStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
        sessionStorage.setItem(
          TOKEN_EXPIRY_KEY,
          String(Date.now() + Math.max(60, tokens.expires_in ?? 3600) * 1000 - 30_000)
        );
        setStatus("connected");
        setMessage("Remote tools connected for this browser tab.");
      } catch (error) {
        setStatus("error");
        setMessage(error instanceof Error ? error.message : String(error));
      } finally {
        sessionStorage.removeItem(OAUTH_STATE_KEY);
        sessionStorage.removeItem(OAUTH_VERIFIER_KEY);
        const cleaned = new URL(window.location.href);
        for (const key of ["code", "state", "error", "error_description"]) {
          cleaned.searchParams.delete(key);
        }
        window.history.replaceState({}, "", cleaned);
      }
    };
    void finishAuthorization();
  }, []);

  useEffect(() => {
    if (!MCP_BASE_URL) return;
    const token = currentToken();
    if (!token) return;
    setStatus("connected");
    setMessage("Remote tools connected for this browser tab.");

    let active = true;
    let proxy: Awaited<ReturnType<typeof createWebMcpProxy>> | undefined;
    void createWebMcpProxy({
      url: `${MCP_BASE_URL}/mcp`,
      headers: { Authorization: `Bearer ${token}` }
    })
      .then((connectedProxy) => {
        if (!active) {
          void connectedProxy.disconnect();
          return;
        }
        proxy = connectedProxy;
        setMessage(
          `Remote tools connected: ${connectedProxy.tools.map((tool) => tool.name).join(", ")}.`
        );
      })
      .catch((error) => {
        sessionStorage.removeItem(ACCESS_TOKEN_KEY);
        sessionStorage.removeItem(TOKEN_EXPIRY_KEY);
        setStatus("error");
        setMessage(error instanceof Error ? error.message : String(error));
      });

    return () => {
      active = false;
      if (proxy) void proxy.disconnect();
    };
  }, [status]);

  return (
    <aside className={`remote-mcp remote-mcp--${status}`} aria-live="polite">
      <div>
        <strong>Remote intelligence</strong>
        <span>{message}</span>
      </div>
      {status === "connected" ? (
        <button type="button" onClick={disconnect}>Disconnect</button>
      ) : status !== "unconfigured" && status !== "authorizing" ? (
        <button type="button" onClick={() => void connect()}>Connect</button>
      ) : null}
    </aside>
  );
}
