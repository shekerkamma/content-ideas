---
name: mcp-capability-probe
description: "Check configured MCP servers and discover their actual tools before relying on a capability."
---

# mcp-capability-probe

This is a Codex discovery adapter. The canonical workflow is
[skills/mcp-capability-probe/SKILL.md](../../../skills/mcp-capability-probe/SKILL.md).

1. Read [Codex/WSL compatibility](../../../docs/codex-wsl-skill-compatibility.md)
   once per session, then read the complete canonical workflow before executing.
2. Resolve its scripts, references, templates and relative links from
   `skills/mcp-capability-probe/`, never from this adapter. Preserve all workflow constraints.
3. Use available Codex tools for Claude interaction names and run Linux scripts
   through WSL with the documented PATH. Check required capabilities before use.
4. Report missing runtime gates precisely; discovery is not end-to-end validation.
