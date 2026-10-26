# GBrain setup and operations

<!-- Moved out of CLAUDE.md so it only loads when needed. Read on demand. -->

The usage rules and cost guardrails stay in `CLAUDE.md`. This file holds the
machine setup and day-to-day operations.

### Location & config
- Repo: `~/gbrain` (cloned from `github.com/garrytan/gbrain`)
- Brain: `~/.gbrain/brain.pglite` (local embedded Postgres, zero DB cost)
- Engine: PGLite
- Search mode: `conservative` (cheapest tier)
- Embeddings: `google:gemini-embedding-001`, 768 dims (requires
  `GOOGLE_GENERATIVE_AI_API_KEY` — get one at
  `https://aistudio.google.com/apikey`; this is a different credential from
  the Gemini CLI's OAuth-personal login and cannot be substituted for it)
- Chat/synthesis: `google:gemini-2.0-flash-exp` (chat), `google:gemini-2.0-flash`
  (query expansion)
- Cost: **$0.00/month** on free tier

### Running it — systemd user service, not an ad hoc background process
- Server process: `~/.config/systemd/user/gbrain.service` runs
  `gbrain serve --http --port 3131` with `Restart=on-failure`.
- `systemctl --user enable gbrain.service` is set, and
  `loginctl enable-linger sheke` is enabled, so the service survives both a
  closed terminal and a full logout — it starts on WSL boot, not just on
  login.
- To check it: `systemctl --user status gbrain.service` /
  `curl http://127.0.0.1:3131/health`.
- `gbrain reinit-pglite` (or any full reinit) wipes the auth-tokens table —
  every connected host's bearer token goes invalid at once and needs
  `gbrain auth create <name>` + `gbrain connect ... --install --force` again
  per host.
- MCP registration is **project-scoped per working directory**, not global —
  `gbrain connect --install` only updates the entry for whatever directory
  you ran it from. Re-run it from `content-ideas` specifically after any
  token rotation, or other projects silently keep the stale token.

### GBrain commands (via MCP or CLI)
```bash
gbrain search <query>        # keyword search (free)
gbrain query <question>      # hybrid search + synthesis (costs tokens)
gbrain get <slug>            # read a page (free)
gbrain put <slug>            # write/update a page (embedding cost)
gbrain list --type <T>       # list pages (free)
```

