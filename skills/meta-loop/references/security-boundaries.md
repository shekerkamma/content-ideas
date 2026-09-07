# Security boundaries

The Codex worker adapter disables user configuration, MCP servers, and hooks; it also uses read-only sandboxes, ephemeral sessions, empty temporary working directories, stdin prompts, a narrow environment allowlist, and separate logs. This reduces accidental access but is not a container: authenticated CLI state under the user profile and model-provider network access may remain available.

The Claude Opus adapter disables tools, MCP servers, slash commands, and session persistence. It preserves ordinary Claude authentication and receives only the supplied aggregation packet.

Before every call:

- Remove secrets, credentials, private keys, and unnecessary personal data.
- Paste the smallest sufficient inputs instead of exposing broad directories.
- Keep workers output-only and apply accepted changes serially.
- Never delegate production, payment, identity, credential, destructive, or externally mutating operations.
- Treat model/provider logs and temporary files as possible disclosure surfaces.

If stronger isolation is required, use an explicitly approved container or VM and record the degraded boundary.
