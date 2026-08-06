# research-to-deck run log

date: 2026-08-04  
topic: CRN — The 10 Coolest Semiconductor Startups of 2026  
style: neon  
kb: `kb/`

## Stage results

- Stage 0 GBrain Recall: ✓ semantic MCP query completed; 0 matching pages
- Stage 1 Research: ✓ `semiconductor-startups-2026-research.md` (1,488 words)
- Research acquisition: ✓ You.com native Livecrawl; ✓ Level 2 You.com discovery → Exa fresh extraction; failed secondary extractions excluded
- Stage 2 Compile: ⚠ 1 document and 1 summary; 0 concepts, so documented direct-source fallback used
- Stage 3 Synthesis: ✓ `semiconductor-startups-2026-synthesis.md`
- Stage 4 Deck: ✓ 13 slides, Aurora Glass neon HTML
- Stage 5 QA: ✓ OpenKB grammar validator; ✓ HTML parse; ✓ Chromium at 1440×900 with 0 overflowing slides; ✓ cover/closing visual review
- Stage 6 PPTX: ✓ 13 native editable slides built; status `draft` because the real Office-render gate is unavailable on this host

## Deliverables

- Research brief: `semiconductor-startups-2026-research.md`
- Synthesis: `semiconductor-startups-2026-synthesis.md`
- Reviewed deck: `semiconductor-startups-2026-deck-reviewed.html`
- QA evidence: `qa/browser/`
- Native PPTX: `semiconductor-startups-2026-decision-deck-draft.pptx`
- PPTX QA evidence: `qa/pptx/`

## Recovery performed

- Replaced the NUL-corrupted OpenKB launcher with official VectifyAI/OpenKB commit `ff54396e575ee6feb0113b631a34caa082b441cc`.
- Installed matching OpenKB deck and critic skills for Claude and Codex; broken Claude symlinks were retained as timestamped backups.
- Reconstructed `~/.claude/skills/voice.md` from surviving repo rules because no byte-identical source existed; the NUL-filled original remains timestamped and recoverable.
- Rejected the all-NUL host branded-template fallback and used the valid governed repo-local `skills/branded-pptx-deck/resources/template.pptx` theme/master package.
