---
name: dual-host
description: 'Use when a Claude Code change must land on both the WSL and the Windows install — "on both WSL and Windows", "port this to the Windows install too", "install this mod on both hosts", "is it on both?", "compare WSL and Windows", or /dual-host <change>. Backs up both settings.json files, applies the same plugin, mod, skill or settings change on each host, then proves it with a parity check of plugins and skills. Not for Codex skill mirroring (scripts/sync-codex-skills.sh does that).'
argument-hint: '<change to apply, or "parity" to only compare>'
license: MIT
metadata:
  category: Infrastructure Ops
  cost-tier: Sonnet
---

# Dual Host

This machine runs two independent Claude Code installs: WSL (`~/.claude`) and Windows
(`C:\Users\<user>\.claude`, seen from WSL at `/mnt/c/Users/<user>/.claude`). Each has its own
settings, plugins, skills and transcripts. Between 18 and 21 Oct 2026, 9 requests asked for a
change to be made on both hosts or ported to the second one. This skill applies it to both in
one pass and proves the result.

Helper: `scripts/dual_host.py` (stdlib, run from WSL). `paths`, `backup <label>`,
`claude -- <args>` (same claude command on both hosts; stdin is passed to both) and
`parity [--full]`.

## Workflow

Input: `$ARGUMENTS`. "parity" or a question like "is it on both?" → step 1 and stop.

1. **Baseline.** `python3 "${SKILL_DIR}/scripts/dual_host.py" paths` then `parity`.
   Keep the parity output; the final check compares against it.
2. **Back up both settings files** before any write:
   `dual_host.py backup <change>-<YYYYMMDD>` (it refuses to overwrite an existing backup).
3. **Apply the change on both hosts**, by kind:
   - Marketplace plugin or mod: `dual_host.py claude -- plugin marketplace add <source>`, then
     `dual_host.py claude -- plugin install <id> --scope user`.
   - Vendored local mod: copy the folder into `~/claude-mods-local/plugins/` and the Windows
     `claude-mods-local/plugins/`, add it to both `marketplace.json` files, then install as above.
   - Switch a mod on or off: `echo "/<mod> on" | dual_host.py claude -- -p` (stdin, no model call).
   - Skill: symlink on WSL (`~/.claude/skills/<name>` → repo); on Windows copy the folder,
     because Windows Claude cannot follow a WSL symlink.
   - Settings key or hook: edit each `settings.json` separately with an exact edit, then
     `python3 -c 'import json;json.load(open(p))'` on each to prove it still parses.
4. **Prove it.** Run `parity` again. Show the before and after lines for the changed item.
   For a mod, also run a command it registers on both hosts and a negative control
   (`echo "/nonexistent-cmd-xyz" | dual_host.py claude -- -p`) to show the reply differs.
5. **Report** per host: what changed, the backup path, and the proof line.

## Judgment rules

Editable policy.

- Apply to both hosts or neither. If Windows fails after WSL succeeded, say so and offer to
  roll WSL back from the backup; do not leave a silent one-host install.
- A mod that shells out to Unix tools (`sleep`, `bash`, `/tmp`) needs a Windows check before install:
  read its hooks first. Blast Radius needed a Git Bash patch on Windows for this reason.
- Windows hooks call Python by full path (`.../Programs/Python/Python312/python.exe`); bare
  `python` there resolves to a Hermes venv.
- Pre-existing parity differences are information, not work. Report them; fix only what was asked.
- Windows-only items (codex computer use bridge, two-mods-windows) are expected to differ.

## Gotchas

- Run `claude.exe` from a Windows folder (`/mnt/c/Users/<user>`), never from a `\\wsl$` path;
  the helper sets that working folder.
- WSL and Windows `claude` versions can differ; `plugin list --json` fields have stayed the same so far.
- `claude -p --debug "prompt"` eats the prompt as the debug filter. Pipe prompts on stdin.
- Sessions on the two hosts never see each other's transcripts, handoffs or folder-mates cards.
- Skill counts differ hugely (hundreds on WSL, dozens on Windows) by design; `parity` caps that list
  at 15 per side unless `--full`.
- Windows `settings.json` may have CRLF line endings; keep them when editing.

## Skill Relationships

### Category
Infrastructure Ops

### Dependencies
- WSL with the Windows drive mounted at `/mnt/c`, and `claude` installed on both hosts.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `plugin-authoring` | Sequential upstream | the mod is being written or changed, not just installed | mod folder |
| `update-config` | Alternative / Peer | the change is one host's settings only | — |

### Runtime Preamble
"Using dual-host. I'll back up both settings.json files, apply the change on WSL and Windows, then show a before-and-after parity check. For a single-host settings change, /update-config fits better."

## Host Compatibility

### Target Hosts
- Claude Code on WSL: yes — `~/.claude/skills/dual-host` symlinks to `skills/dual-host/`.
- Codex/OpenAI, OpenHands / DSH: yes from WSL — `.agents/skills/dual-host/` copy; the helper only needs Python 3 and both `claude` binaries.
- Windows-native hosts: no. Run it from WSL.

### Canonical Source
`skills/dual-host/`.

### Tool Mapping
- `Edit` on settings.json → any exact-replace file edit; never rewrite the whole file.

### Source / Tool Order
1. Both hosts' `settings.json`, `plugin list --json` and skill folders. 2. The mod's own README and hooks. No web search.

### Environment
- `DUAL_HOST_WIN_HOME` — Windows home as seen from WSL; default `/mnt/c/Users/$USER`.
- `DUAL_HOST_WIN_CLAUDE` — Windows `claude.exe`; default `<win home>/.local/bin/claude.exe`.
