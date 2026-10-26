# Local host setup (WSL, Windows proxies, key locations)

<!-- Moved out of CLAUDE.md so it only loads when needed. Read on demand. -->

## API key two-layer pattern

- API keys used by this project's skills follow a two-layer pattern, because
  Claude Code and Codex have no shared secrets mechanism:
  - **`.claude/settings.local.json`'s `env` block** — Claude-Code-specific.
    Injected directly into every session for this project regardless of how
    the session was launched; works even in non-interactive Bash tool calls,
    which don't source `~/.bashrc`. Gitignored (`.gitignore` has the
    `.claude/settings.local.json` pattern) — never the committed
    `.claude/settings.json`.
  - **`~/.bashrc` `export`** — the cross-host baseline. Codex reads secrets
    from its own process environment directly (e.g. `bearer_token_env_var`
    in `~/.codex/config.toml` for the gbrain MCP server); it has no
    settings.local.json equivalent, so this layer is what Codex — and any
    interactively-launched Claude Code session — actually relies on.
  - Write to both layers together; neither replaces the other. Never put a
    real key in `~/.config/content/.env`'s tracked convention notes, a
    commit, or any file under version control.
  - Currently configured this way: `SUPADATA_API_KEY`, `GBRAIN_REMOTE_TOKEN`,
    `OPENAI_API_KEY`, `EXA_API_KEY`, `GOOGLE_GENERATIVE_AI_API_KEY`,
    `GROQ_API_KEY`. When hunting for an already-configured key before asking
    the user for a new one, check beyond this repo and beyond WSL paths —
    Windows-side app configs (e.g. `/mnt/c/Users/<user>/AppData/Local/hermes/.env`,
    `/mnt/c/Users/<user>/.config/watch/.env`, `/mnt/c/Users/<user>/.fcc/.env`,
    `/mnt/c/Users/<user>/.cli-proxy-api/config.yaml`) have held real values
    that their WSL-side namesakes didn't.

## Local AI-gateway/router proxies

- Local AI-gateway/router proxies on the Windows side are common places to
  find already-configured provider keys and model routing before assuming a
  tool is broken or asking for new credentials:
  - **`free-claude-code` (fcc)** — `~/.fcc/.env` (provider keys plus
    `MODEL`/`MODEL_OPUS`/`MODEL_SONNET`/`MODEL_HAIKU` routing), binaries at
    `~/.local/bin/fcc-*.exe`. Actively developed upstream — before trusting a
    hard failure, check whether the installed build predates the commit that
    fixed it (`fcc-server --version`), and update via the installer one-liner
    in its README before debugging further.
  - **OmniRoute** — dashboard/API on `127.0.0.1:20128`; the gateway API key
    lives in its SQLite-backed dashboard, not `.env` (`~/OmniRoute/.env` only
    holds server-runtime secrets like `INITIAL_PASSWORD`/`JWT_SECRET`). Use
    the bundled `omniroute` CLI (`providers list`, `models <provider>`,
    `usage logs`, `setup-claude`, `setup-kilo`, `launch --profile <name>`)
    instead of the dashboard when a CLI path exists — no login needed.
    `providers list` / `models` catalog entries are not proof a model ID is
    actually routable, and `auto/*` combos can silently pick a different
    provider than expected — confirm with a real `/v1/chat/completions` call
    and cross-check `omniroute usage logs` for the provider/status that
    actually served it.
  - **cli-proxy-api** (`router-for-me/CLIProxyAPI`, often bundled inside
    another tool's `bin/`, e.g. Hermes) — config at
    `~/.cli-proxy-api/config.yaml`, OAuth credentials as
    `<provider>-<email>.json` in the same directory. Must be launched with an
    explicit `-config <path>` flag; it does not reliably resolve the config
    path from a WSL-launched process's working directory. Stored OAuth
    tokens refresh lazily on the next proxied request, not on a timer — a
    stale `expired` timestamp with the process not currently running is not
    itself a bug.
  - **Hermes Agent** (NousResearch, git install) — `~/AppData/Local/hermes/`.
    `hermes skills list-modified` lists real user-customized skills by name;
    a noisy `git status` in its `hermes-agent` checkout (e.g. from a botched
    update stash/restore) does not by itself threaten them — Hermes tracks
    skill customizations separately from raw git diff state.

## WSL and Windows processes

- PowerShell or native `.exe` processes launched from a WSL Bash shell
  inherit the WSL cwd, which Windows renders as a `\\wsl.localhost\<distro>\...`
  UNC path — cmd.exe refuses it outright, and some native exes silently
  resolve relative config paths against it and fail instead of erroring
  clearly. Pass an explicit Windows working directory or absolute paths
  rather than relying on the invoked process's own relative-path resolution.
