import { OAuthProvider } from "@cloudflare/workers-oauth-provider";
import { McpServer } from "@modelcontextprotocol/server";
import { createMcpHandler } from "agents/mcp/server";
import { z } from "zod";
import { AuthHandler } from "./auth-handler";
import {
  COMPETITOR_NAMES,
  INTELLIGENCE_SOURCES,
  type IntelligenceSource
} from "./sources";

export interface Env {
  OAUTH_KV: KVNamespace;
  DEEPGRID_DATA: KVNamespace;
  SHARED_PASSWORD: string;
}

interface Snapshot {
  sourceId: string;
  competitor: string;
  title: string;
  url: string;
  checkedAt: string;
  digest: string;
  status: number;
  contentType: string;
  byteLength: number;
  etag?: string;
  lastModified?: string;
}

interface ChangeRecord {
  id: string;
  sourceId: string;
  competitor: string;
  title: string;
  url: string;
  detectedAt: string;
  previousDigest: string | null;
  currentDigest: string;
}

interface RefreshResult {
  sourceId: string;
  competitor: string;
  title: string;
  url: string;
  checkedAt: string;
  outcome: "baseline_created" | "changed" | "unchanged" | "not_modified" | "error";
  status?: number;
  error?: string;
}

const SITE_ORIGIN = "https://shekerkamma.github.io";
const LOCAL_ORIGINS = new Set([
  "http://localhost:5173",
  "http://127.0.0.1:5173",
  "http://localhost:4173",
  "http://127.0.0.1:4173"
]);
const MAX_SOURCE_BYTES = 5_000_000;
const MAX_CHANGES = 500;

function jsonText(value: Record<string, unknown>) {
  return {
    content: [{ type: "text" as const, text: JSON.stringify(value, null, 2) }],
    structuredContent: value
  };
}

function normalizeCompetitor(value?: string) {
  if (!value) return undefined;
  const normalized = value.trim().toLocaleLowerCase();
  const match = COMPETITOR_NAMES.find(
    (candidate) => candidate.toLocaleLowerCase() === normalized
  );
  if (!match) {
    throw new Error(
      `Unknown competitor \`${value}\`. Choose one of: ${COMPETITOR_NAMES.join(", ")}.`
    );
  }
  return match;
}

function toHex(bytes: ArrayBuffer) {
  return [...new Uint8Array(bytes)]
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

async function sha256(value: ArrayBuffer) {
  return toHex(await crypto.subtle.digest("SHA-256", value));
}

async function readChangeIndex(env: Env): Promise<ChangeRecord[]> {
  return (await env.DEEPGRID_DATA.get<ChangeRecord[]>("changes:index", "json")) ?? [];
}

async function refreshSource(
  env: Env,
  source: IntelligenceSource,
  force: boolean
): Promise<{ result: RefreshResult; change?: ChangeRecord }> {
  const checkedAt = new Date().toISOString();
  const previous = await env.DEEPGRID_DATA.get<Snapshot>(
    `snapshot:${source.id}`,
    "json"
  );
  const headers = new Headers({
    Accept: "text/html,application/pdf,text/plain;q=0.9,*/*;q=0.5",
    "User-Agent": "DeepGrid-Market-Intelligence-Monitor/1.0 (+https://shekerkamma.github.io/content-ideas/deepgrid-semi-competitor-analysis/)"
  });

  if (!force && previous?.etag) headers.set("If-None-Match", previous.etag);
  if (!force && previous?.lastModified) {
    headers.set("If-Modified-Since", previous.lastModified);
  }

  try {
    const response = await fetch(source.url, {
      headers,
      redirect: "follow",
      signal: AbortSignal.timeout(20_000)
    });

    if (response.status === 304 && previous) {
      await env.DEEPGRID_DATA.put(
        `snapshot:${source.id}`,
        JSON.stringify({ ...previous, checkedAt })
      );
      return {
        result: {
          sourceId: source.id,
          competitor: source.competitor,
          title: source.title,
          url: source.url,
          checkedAt,
          outcome: "not_modified",
          status: 304
        }
      };
    }

    if (!response.ok) throw new Error(`Source returned HTTP ${response.status}.`);
    const contentLength = Number(response.headers.get("content-length") ?? "0");
    if (contentLength > MAX_SOURCE_BYTES) {
      throw new Error(`Source exceeded the ${MAX_SOURCE_BYTES}-byte safety limit.`);
    }
    const body = await response.arrayBuffer();
    if (body.byteLength > MAX_SOURCE_BYTES) {
      throw new Error(`Source exceeded the ${MAX_SOURCE_BYTES}-byte safety limit.`);
    }

    const digest = await sha256(body);
    const etag = response.headers.get("etag") ?? undefined;
    const lastModified = response.headers.get("last-modified") ?? undefined;
    const snapshot: Snapshot = {
      sourceId: source.id,
      competitor: source.competitor,
      title: source.title,
      url: source.url,
      checkedAt,
      digest,
      status: response.status,
      contentType: response.headers.get("content-type") ?? "application/octet-stream",
      byteLength: body.byteLength,
      ...(etag ? { etag } : {}),
      ...(lastModified ? { lastModified } : {})
    };
    await env.DEEPGRID_DATA.put(`snapshot:${source.id}`, JSON.stringify(snapshot));

    const changed = Boolean(previous && previous.digest !== digest);
    const result: RefreshResult = {
      sourceId: source.id,
      competitor: source.competitor,
      title: source.title,
      url: source.url,
      checkedAt,
      outcome: previous ? (changed ? "changed" : "unchanged") : "baseline_created",
      status: response.status
    };
    if (!changed) return { result };
    return {
      result,
      change: {
        id: crypto.randomUUID(),
        sourceId: source.id,
        competitor: source.competitor,
        title: source.title,
        url: source.url,
        detectedAt: checkedAt,
        previousDigest: previous?.digest ?? null,
        currentDigest: digest
      }
    };
  } catch (error) {
    return {
      result: {
        sourceId: source.id,
        competitor: source.competitor,
        title: source.title,
        url: source.url,
        checkedAt,
        outcome: "error",
        error: error instanceof Error ? error.message : String(error)
      }
    };
  }
}

export async function refreshMarketIntelligence(
  env: Env,
  competitor?: string,
  force = false
) {
  const selectedCompetitor = normalizeCompetitor(competitor);
  const sources = selectedCompetitor
    ? INTELLIGENCE_SOURCES.filter((source) => source.competitor === selectedCompetitor)
    : INTELLIGENCE_SOURCES;
  const refreshed = await Promise.all(
    sources.map((source) => refreshSource(env, source, force))
  );
  const newChanges = refreshed.flatMap(({ change }) => (change ? [change] : []));
  if (newChanges.length) {
    const existing = await readChangeIndex(env);
    await env.DEEPGRID_DATA.put(
      "changes:index",
      JSON.stringify([...newChanges, ...existing].slice(0, MAX_CHANGES))
    );
  }
  const results = refreshed.map(({ result }) => result);
  return {
    refreshedAt: new Date().toISOString(),
    competitor: selectedCompetitor ?? "all",
    sourceCount: sources.length,
    changedCount: newChanges.length,
    errorCount: results.filter((result) => result.outcome === "error").length,
    results
  };
}

function createServer(env: Env, requestOrigin: string) {
  const server = new McpServer({
    name: "DeepGrid Market Intelligence",
    version: "1.0.0"
  });

  server.registerTool(
    "refresh_market_intelligence",
    {
      description:
        "Fetch the fixed, allowlisted DeepGrid competitor and regulatory sources now, compare them with stored snapshots, and persist detected changes.",
      inputSchema: {
        competitor: z.string().trim().min(1).optional(),
        force: z.boolean().default(false)
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true
      }
    },
    async ({ competitor, force }) =>
      jsonText(await refreshMarketIntelligence(env, competitor, force))
  );

  server.registerTool(
    "monitor_competitor_changes",
    {
      description:
        "Read persisted competitor-source changes and current source-check status. This does not fetch the web; call refresh_market_intelligence first for an on-demand check.",
      inputSchema: {
        competitor: z.string().trim().min(1).optional(),
        since: z.iso.datetime().optional(),
        limit: z.number().int().min(1).max(100).default(25)
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: false
      }
    },
    async ({ competitor, since, limit }) => {
      const selectedCompetitor = normalizeCompetitor(competitor);
      const sinceTime = since ? Date.parse(since) : 0;
      const changes = (await readChangeIndex(env))
        .filter(
          (change) =>
            (!selectedCompetitor || change.competitor === selectedCompetitor) &&
            Date.parse(change.detectedAt) >= sinceTime
        )
        .slice(0, limit);
      const sources = INTELLIGENCE_SOURCES.filter(
        (source) => !selectedCompetitor || source.competitor === selectedCompetitor
      );
      const snapshots = (
        await Promise.all(
          sources.map((source) =>
            env.DEEPGRID_DATA.get<Snapshot>(`snapshot:${source.id}`, "json")
          )
        )
      ).filter((snapshot): snapshot is Snapshot => Boolean(snapshot));
      return jsonText({
        competitor: selectedCompetitor ?? "all",
        since: since ?? null,
        changeCount: changes.length,
        changes,
        sourceStatus: sources.map((source) => ({
          sourceId: source.id,
          competitor: source.competitor,
          title: source.title,
          url: source.url,
          snapshot: snapshots.find((item) => item.sourceId === source.id) ?? null
        }))
      });
    }
  );

  server.registerTool(
    "share_brief",
    {
      description:
        "Publish supplied Markdown as a private-by-link, time-limited page and return its URL. Anyone with the URL can read it until expiry.",
      inputSchema: {
        title: z.string().trim().min(1).max(120),
        markdown: z.string().min(1).max(100_000),
        expiresInDays: z.number().int().min(1).max(90).default(14)
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: true
      }
    },
    async ({ title, markdown, expiresInDays }) => {
      const id = crypto.randomUUID().replaceAll("-", "").slice(0, 20);
      const createdAt = new Date().toISOString();
      const expiresAt = new Date(
        Date.now() + expiresInDays * 24 * 60 * 60 * 1000
      ).toISOString();
      await env.DEEPGRID_DATA.put(
        `brief:${id}`,
        JSON.stringify({ id, title, markdown, createdAt, expiresAt }),
        { expirationTtl: expiresInDays * 24 * 60 * 60 }
      );
      return jsonText({
        id,
        title,
        createdAt,
        expiresAt,
        visibility: "anyone_with_link",
        url: `${requestOrigin}/brief/${id}`
      });
    }
  );
  return server;
}

const apiHandler = {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    const handler = createMcpHandler(
      () => createServer(env, new URL(request.url).origin),
      {
        route: "/mcp",
        corsOptions: false,
        allowedOriginHostnames: [
          "shekerkamma.github.io",
          "localhost",
          "127.0.0.1"
        ]
      }
    );
    return handler(request, env, ctx);
  }
};

const oauthProvider = new OAuthProvider({
  authorizeEndpoint: "/authorize",
  tokenEndpoint: "/oauth/token",
  clientRegistrationEndpoint: "/oauth/register",
  apiRoute: "/mcp",
  apiHandler,
  defaultHandler: {
    fetch(request: Request, env: Env, ctx: ExecutionContext) {
      return AuthHandler.fetch(request, env, ctx);
    }
  }
});

function corsOrigin(request: Request) {
  const origin = request.headers.get("origin");
  if (!origin) return null;
  if (origin === SITE_ORIGIN || LOCAL_ORIGINS.has(origin)) return origin;
  return null;
}

function withCors(response: Response, origin: string | null) {
  if (!origin) return response;
  const headers = new Headers(response.headers);
  headers.set("Access-Control-Allow-Origin", origin);
  headers.set("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS");
  headers.set(
    "Access-Control-Allow-Headers",
    "Authorization, Content-Type, Accept, MCP-Protocol-Version, Mcp-Method, Mcp-Name"
  );
  headers.set("Access-Control-Expose-Headers", "mcp-session-id");
  headers.set("Access-Control-Max-Age", "86400");
  headers.append("Vary", "Origin");
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  });
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    const origin = corsOrigin(request);
    if (request.headers.has("origin") && !origin) {
      return new Response("Origin not allowed", { status: 403 });
    }
    if (request.method === "OPTIONS") {
      return withCors(new Response(null, { status: 204 }), origin);
    }
    return withCors(await oauthProvider.fetch(request, env, ctx), origin);
  },
  async scheduled(_controller: ScheduledController, env: Env, ctx: ExecutionContext) {
    ctx.waitUntil(refreshMarketIntelligence(env));
  }
} satisfies ExportedHandler<Env>;
