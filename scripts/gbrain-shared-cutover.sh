#!/usr/bin/env bash
# gbrain-shared-cutover.sh — consolidate GBrain onto ONE HTTP MCP server that
# Hermes + OpenClaw + Claude Code all connect to as clients.
#
# WHY: PGLite is single-connection. Multiple processes opening ~/.gbrain/brain.pglite
# directly = corruption (already happened 2026-06-20). This makes exactly one writer
# (the systemd service) and turns every agent into a client of it.
#
# RUN THIS AFTER CLOSING CLAUDE CODE — a running Claude session holds the DB lock
# via its stdio gbrain MCP. The script refuses to proceed while the DB is held.
#
# Idempotent. Safe to re-run.
#
# ── AUTH MODEL (corrected 2026-06-28) ───────────────────────────────────────
# The /mcp endpoint validates bearers via the OAuth verifier — the admin
# BOOTSTRAP token is NOT a valid /mcp bearer (it only mints browser magic-links
# at /admin/api/issue-magic-link). Clients must use a real access token from
# `gbrain auth create`. That command opens the DB directly, so we mint it while
# the service is STOPPED (sole writer), then persist it to a 0600 file and reuse
# it on every re-run. The bootstrap token stays in shared-http.env for the
# server's own admin surface; it is never handed to a client.
set -euo pipefail

ENV_FILE="$HOME/.gbrain/shared-http.env"
CLIENT_TOKEN_FILE="$HOME/.gbrain/shared-clients.token"
DB="$HOME/.gbrain/brain.pglite"
GBRAIN_SRC="$HOME/gbrain"
CTR="openclaw-openclaw-gateway-1"
MCP_LOCAL="http://127.0.0.1:3131/mcp"                  # Hermes (native) + Claude Code
MCP_CONTAINER="http://host.docker.internal:3131/mcp"  # OpenClaw (in Docker)

say() { printf '\n\033[1;36m== %s\033[0m\n' "$*"; }
die() { printf '\n\033[1;31mABORT: %s\033[0m\n' "$*" >&2; exit 1; }

[ -f "$ENV_FILE" ] || die "missing $ENV_FILE (run the prep step first)"

# ---------------------------------------------------------------------------
say "0. Corruption guard — is anything holding brain.pglite?"
if command -v lsof >/dev/null 2>&1 && lsof +D "$DB" 2>/dev/null | grep -q .; then
  lsof +D "$DB" 2>/dev/null | awk 'NR==1||/bun|node|gbrain/{print}'
  die "brain.pglite is still open (close Claude Code / stop any gbrain stdio server first)."
fi
echo "OK — DB is free, no competing writer."

# ---------------------------------------------------------------------------
say "1. Ensure a client access token exists (mint once, sole writer)"
if [ -s "$CLIENT_TOKEN_FILE" ]; then
  echo "Reusing existing client token at $CLIENT_TOKEN_FILE"
else
  echo "No client token yet — minting 'shared-clients' with the service stopped."
  systemctl --user stop gbrain-http.service 2>/dev/null || true
  for i in $(seq 1 10); do lsof +D "$DB" 2>/dev/null | grep -q . || break; sleep 1; done
  OUT=$(cd "$GBRAIN_SRC" && bun run src/cli.ts auth create "shared-clients" 2>&1) \
    || die "auth create failed: $OUT"
  TOK=$(printf '%s\n' "$OUT" | grep -oE '^[[:space:]]+[A-Za-z0-9_-]{32,}$' | tr -d '[:space:]' | head -1)
  [ -n "$TOK" ] || die "could not parse minted token from: $OUT"
  umask 077; printf '%s' "$TOK" > "$CLIENT_TOKEN_FILE"
  echo "Minted and saved client token to $CLIENT_TOKEN_FILE"
fi
TOKEN="$(cat "$CLIENT_TOKEN_FILE")"

# ---------------------------------------------------------------------------
say "2. Start the single GBrain HTTP server (systemd --user)"
systemctl --user daemon-reload
systemctl --user enable --now gbrain-http.service
loginctl enable-linger "$USER" 2>/dev/null || echo "(note: enable-linger needs privilege; service still runs while logged in)"

say "   Waiting for /health ..."
for i in $(seq 1 30); do
  if curl -fsS "http://127.0.0.1:3131/health" >/dev/null 2>&1; then echo "healthy."; break; fi
  [ "$i" = 30 ] && { journalctl --user -u gbrain-http.service -n 30 --no-pager 2>/dev/null; die "server did not become healthy"; }
  sleep 1
done

say "   Verifying the client token authenticates against /mcp ..."
code=$(curl -sS -o /dev/null -w '%{http_code}' -X POST "$MCP_LOCAL" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"cutover","version":"1"}}}')
[ "$code" = 200 ] || die "client token rejected by /mcp (HTTP $code). Delete $CLIENT_TOKEN_FILE and re-run to re-mint."
echo "token OK (HTTP 200)."

# ---------------------------------------------------------------------------
say "3. Repoint Claude Code off the direct-DB stdio wrapper → HTTP client"
python3 - "$TOKEN" <<'PY'
import json, os, sys
token = sys.argv[1]
http = {"type": "http", "url": "http://127.0.0.1:3131/mcp",
        "headers": {"Authorization": f"Bearer {token}"}}
def rewrite(path):
    if not os.path.exists(path): return
    with open(path) as f: data = json.load(f)
    n = [0]
    def walk(o):
        if isinstance(o, dict):
            srv = o.get("mcpServers")
            if isinstance(srv, dict) and "gbrain" in srv:
                srv["gbrain"] = dict(http); n[0]+=1
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(data)
    if n[0]:
        with open(path, "w") as f: json.dump(data, f, indent=2)
        print(f"  {path}: rewrote {n[0]} gbrain entr(y/ies) -> http")
    else:
        print(f"  {path}: no gbrain mcpServers entry found (ok)")
rewrite(os.path.expanduser("~/.claude.json"))
rewrite(os.path.expanduser("~/.claude/settings.json"))
PY
echo "  (takes effect next time Claude Code launches — it will be a client, not a writer)"

# ---------------------------------------------------------------------------
say "4. Wire OpenClaw (container → host.docker.internal) and reload its gateway"
docker exec "$CTR" openclaw mcp remove gbrain 2>/dev/null || true
docker exec "$CTR" openclaw mcp add gbrain \
  --url "$MCP_CONTAINER" \
  --transport streamable-http \
  --header "Authorization=Bearer ${TOKEN}" \
  --parallel \
  && echo "  OpenClaw: gbrain MCP added." \
  || echo "  OpenClaw: add reported an error — check 'docker exec $CTR openclaw mcp list'."
# The running gateway caches MCP runtimes; force a reload so the new server connects.
docker exec "$CTR" openclaw mcp reload 2>/dev/null || true

# ---------------------------------------------------------------------------
say "5. Wire Hermes (native) — write config + .env directly (non-interactive)"
# Hermes stores the token in ~/.hermes/.env as MCP_GBRAIN_API_KEY (bare, no
# 'Bearer ' prefix) and references it from config.yaml via ${MCP_GBRAIN_API_KEY}.
HERMES_AGENT_DIR="${HERMES_AGENT_DIR:-$HOME/hermes-agent}"
HERMES_PY="$HERMES_AGENT_DIR/venv/bin/python3"
if [ -x "$HERMES_PY" ]; then
  ( cd "$HERMES_AGENT_DIR" && "$HERMES_PY" - "$TOKEN" <<'PY'
import sys
token = sys.argv[1]
from hermes_cli.config import save_env_value
from hermes_cli.mcp_config import _save_mcp_server, _env_key_for_server, _strip_bearer_prefix
env_key = _env_key_for_server("gbrain")
save_env_value(env_key, _strip_bearer_prefix(token))
cfg = {"url": "http://127.0.0.1:3131/mcp",
       "headers": {"Authorization": f"Bearer ${{{env_key}}}"},
       "enabled": True}
print("  Hermes: saved =", _save_mcp_server("gbrain", cfg), f"(env {env_key})")
PY
  ) || echo "  Hermes: direct config write failed — run 'hermes mcp add gbrain --url $MCP_LOCAL --auth header' and paste 'Bearer <token from $CLIENT_TOKEN_FILE>'."
else
  echo "  Hermes venv not found at $HERMES_PY — run:"
  echo "    hermes mcp add gbrain --url $MCP_LOCAL --auth header"
  echo "    (paste the token from $CLIENT_TOKEN_FILE when prompted; no 'Bearer ' prefix)"
fi

# ---------------------------------------------------------------------------
say "6. Smoke test"
echo "  server /health:"; curl -fsS "http://127.0.0.1:3131/health" || true; echo
echo "  OpenClaw probe:"; docker exec "$CTR" openclaw mcp probe 2>/dev/null | grep -i gbrain || echo "  (check manually)"
echo "  Hermes test:";    hermes mcp test gbrain 2>/dev/null | grep -iE "connected|tools" || echo "  (run: hermes mcp test gbrain)"

cat <<DONE

DONE — GBrain is now one server, three clients.
  • Server:    systemctl --user status gbrain-http.service   (port 3131, token-gated)
  • Client token: $CLIENT_TOKEN_FILE  (0600, NOT committed) — same token for all 3 clients
  • OpenClaw:  reaches it at host.docker.internal:3131
  • Hermes:    reaches it at 127.0.0.1:3131
  • Claude Code: relaunch to pick up the http client config

VERIFY the shared brain end-to-end:
  1. Hermes writes:  hermes chat -q "use gbrain put_page slug 'cutover-test' body 'shared brain works'" --yolo -Q
  2. OpenClaw reads: docker exec $CTR openclaw agent --session-key t --message "use gbrain get_page 'cutover-test'"
  3. Relaunch Claude Code and confirm gbrain search finds 'cutover-test'.
If all three see it, the layer in your diagram is real.
DONE
