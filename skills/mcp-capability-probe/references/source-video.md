# Source video

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=nI0Mhzcl2Fk |
| Title | I Built an AI Competitor Research System Without Scrapers |
| Uploader | Eric Tech |
| Uploaded | 2026-08-24 |
| Duration | 10:08 |
| Derived on | 2026-08-25 |
| Capture | 1080p (format 137), 124 frames at scene threshold 0.08, max gap 14.9s |

## Why this file exists

The claims below are only as current as the video. When a step stops working,
check the upload date first.

**The video is a sponsored vendor demo**, with a promo code and the vendor's own
benchmark table at the end. The MCP mechanics it shows are protocol-level and
were re-verified here against an unrelated server; the vendor's efficiency
claims were not, and nothing in this skill rests on them.

## Demonstration span for this skill

01:33 – 02:56. The wider video covers a second job — declarative collection into
a local store — which is derived separately as `dataset-collect`.

## Cited moments

| Timestamp | What it establishes | Evidence |
|---|---|---|
| 01:36 | The vendor's MCP page offers Claude Desktop, **Claude Code**, Cursor, and n8n as targets, with an OAuth URL and a direct API-key URL | frame |
| 01:51 | The config written to `~/.cursor/mcp.json`: `mcpServers` → `url` + `Authorization: Bearer <jwt>` header | frame |
| 01:52 | The opening move is a discovery question — "show me what LinkedIn company endpoints are available" — before any real call | narration + frame |
| 02:18 | Discovery returns three endpoints (`company`, `company_posts`, `company_employee_stats`) with paths and required params | frame |
| 02:18 | **The assistant notes the docs reference a `company/employees` flow that discovery did not list** | frame |
| 02:04 | Rationale: without discovery you would "find an API, build a scraper, or manually figure out how to pull this data" | narration |

## The moment this skill exists for

At 02:18 the on-screen response says the vendor's documentation references an
endpoint that the live discovery response did not expose. That is the whole
argument for probing rather than reading: the server is the authority on its own
surface, and documentation drifts.

`show --tool <name>` returns exit 1 with that reminder when a name is absent, so
the lesson is enforced rather than merely written down.

## What was changed in the derivation

| In the video | Here | Why |
|---|---|---|
| Discovery happens in a chat turn | Discovery happens in a script, writing to a file | A 96-tool server is 85.5 KiB of schemas. In a transcript that is spent every time; on disk it is grepped. |
| One vendor's hosted MCP server | Any HTTP MCP server | The protocol is not vendor-specific. Verified against `gbrain`. |
| Bearer JWT pasted into a config file | `--bearer-env` names an environment variable | A token in a config file gets committed. |
| Cursor's "Add MCP" button | Direct JSON-RPC | Removes the editor from the dependency list entirely. |

## Claims not carried forward

- The vendor's benchmark table against Apify and Bright Data (07:28–08:54) is
  the vendor's own published comparison, presented on a sponsored channel. Not
  used as evidence for anything.
- "AI-generated endpoints and self-healing extraction" (08:04) is a product
  claim about how the vendor maintains its endpoints. Unverifiable from the
  video and irrelevant to probing any server.
