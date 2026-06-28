#!/usr/bin/env bash
# gbrain-shared-cutover.sh — consolidate GBrain onto ONE HTTP MCP server that
# Hermes + OpenClaw + Claude Code all connect to as clients.
#
# WHY: PGLite is single-connection. Multiple processes opening ~/.gbrain/brain.pglite
# directly = corruption (already happened 2026-06-20). This makes exactly one writer
# (the systemd service) and turns every agent into a client of it.
#
# RUN THIS AFTER CLOSING CLAUDE CODE — the running Claude session holds the DB lock
# via its stdio gbrain MCP. The script refuses to proceed while the DB is held.
#
# Idempotent. Safe to re-run.
set -euo pipefail

ENV_FILE="$HOME/.gbrain/shared-http.env"
DB="$HOME/.gbrain/brain.pglite"
CTR="openclaw-openclaw-gateway-1"
MCP_LOCAL="http://127.0.0.1:3131/mcp"          # Hermes (native) + Claude Code
MCP_CONTAINER="http://host.docker.internal:3131/mcp"  # OpenClaw (in Docker)

say() { printf '\n\033[1;36m== %s\033[0m\n' "$*"; }
die() { printf '\n\033[1;31mABORT: %s\033[0m\n' "$*" >&2; exit 1; }

[ -f "$ENV_FILE" ] || die "missing $ENV_FILE (run the prep step first)"
# shellcheck disable=SC1090
source "$ENV_FILE"
TOKEN="${GBRAIN_ADMIN_BOOTSTRAP_TOKEN:?token missing in env file}"

# ---------------------------------------------------------------------------
say "0. Corruption guard — is anything holding brain.pglite?"
if command -v lsof >/dev/null 2>&1 && lsof +D "$DB" 2>/dev/null | grep -q .; then
  lsof +D "$DB" 2>/dev/null | awk 'NR==1||/bun|node|gbrain/{print}'
  die "brain.pglite is still open (close Claude Code / stop any gbrain stdio server first)."
fi
echo "OK — DB is free, no competing writer."

# ---------------------------------------------------------------------------
say "1. Start the single GBrain HTTP server (systemd --user)"
systemctl --user daemon-reload
systemctl --user enable --now gbrain-http.service
loginctl enable-linger "$USER" 2>/dev/null || echo "(note: enable-linger needs privilege; service still runs while logged in)"

say "   Waiting for /health ..."
for i in $(seq 1 30); do
  if curl -fsS "http://127.0.0.1:3131/health" >/dev/null 2>&1; then echo "healthy."; break; fi
  [ "$i" = 30 ] && { journalctl --user -u gbrain-http.service -n 30 --no-pager 2>/dev/null; die "server did not become healthy"; }
  sleep 1
done

# ---------------------------------------------------------------------------
say "2. Repoint Claude Code off the direct-DB stdio wrapper → HTTP client"
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
say "3. Wire OpenClaw (container → host.docker.internal)"
docker exec "$CTR" openclaw mcp remove gbrain 2>/dev/null || true
docker exec "$CTR" openclaw mcp add gbrain \
  --url "$MCP_CONTAINER" \
  --transport streamable-http \
  --header "Authorization=Bearer ${TOKEN}" \
  --parallel \
  && echo "  OpenClaw: gbrain MCP added." \
  || echo "  OpenClaw: add reported an error — check 'docker exec $CTR openclaw mcp list'."

# ---------------------------------------------------------------------------
say "4. Wire Hermes (native)"
echo "  Running: hermes mcp add gbrain --url $MCP_LOCAL --auth header"
echo "  If it prompts for the Authorization header/token, paste:"
echo "      Bearer ${TOKEN}"
hermes mcp add gbrain --url "$MCP_LOCAL" --auth header || \
  echo "  Hermes: if non-interactive add failed, run the command above in a terminal and paste the token."

# ---------------------------------------------------------------------------
say "5. Smoke test"
echo "  server /health:"; curl -fsS "http://127.0.0.1:3131/health" || true; echo
echo "  OpenClaw sees gbrain tools:"; docker exec "$CTR" openclaw mcp list 2>/dev/null | grep -i gbrain || echo "  (check manually)"
echo "  Hermes sees gbrain:"; hermes mcp list 2>/dev/null | grep -i gbrain || echo "  (check manually)"

cat <<DONE

DONE — GBrain is now one server, three clients.
  • Server:    systemctl --user status gbrain-http.service   (port 3131, token-gated)
  • OpenClaw:  reaches it at host.docker.internal:3131
  • Hermes:    reaches it at 127.0.0.1:3131
  • Claude Code: relaunch to pick up the http client config

VERIFY the shared brain end-to-end:
  1. Ask Hermes to write a fact:  hermes -z "use the gbrain tool to put a page 'cutover-test' with body 'shared brain works'"
  2. Ask OpenClaw to read it:     docker exec $CTR openclaw agent --session-key t -m "use gbrain to get the page 'cutover-test'"
  3. Relaunch Claude Code and confirm gbrain search finds 'cutover-test'.
If all three see it, the layer in your diagram is real.
DONE
