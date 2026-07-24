# V5 QA Report

Status: `reviewed`

## Deliverables

- PPTX: `agent-native-apps-local-rebuild-v5-reviewed.pptx`
- PDF: `agent-native-apps-local-rebuild-v5-reviewed.pdf`
- Slide count: 31
- Preview folder: `v5-preview/`
- Builder script: `build_agent_native_v5.py`
- Research synthesis: `v5-research-synthesis.md`

## QA Checks

- Branded workflow: used fallback branded template `/home/shekerk/.claude/templates/branded-template.pptx` and local `branded-pptx-deck` / `pptxkit` builder.
- PPTX structural validation: `CLEAN`.
- PowerPoint repair-risk check: no `<p:cxnSp>` connector XML in slide files.
- Preview QA: contact sheets rendered; final pass showed no red overflow markers.
- Local reopen check: python-pptx opened the generated PPTX and both Windows-copied PPTX files with 31 slides.
- PDF generated from the final slide preview images using ReportLab because LibreOffice is unavailable in this host.

## Windows Delivery

Copied to:

- `C:\Users\sheke\OneDrive\Desktop\agent-native-apps-local-rebuild-v5-reviewed.pptx`
- `C:\Users\sheke\OneDrive\Desktop\agent-native-apps-local-rebuild-v5-reviewed.pdf`
- `C:\Users\sheke\Desktop\agent-native-apps-local-rebuild-v5-reviewed.pptx`
- `C:\Users\sheke\Desktop\agent-native-apps-local-rebuild-v5-reviewed.pdf`

Opening status:

- Attempted Windows launch through PowerShell and cmd from WSL.
- Blocked by this WSL host: Windows `.exe` launchers exist on disk but cannot be executed from the shell.
- This is an interop/host launch issue, not a PPTX validation issue.

## Source And Pipeline Notes

- Genspark and other subscription-gated slide generators were excluded.
- GBrain recall was attempted but blocked by a PGLite lock.
- Source-backed deck narrative uses the supplied YouTube transcript plus official OpenAI Codex, MCP, Notion MCP, and Cursor documentation.
