# GOAL: Harden + port vault-presales-pptx-pipeline image-gen chain

TASK: Harden the vault-presales-pptx-pipeline image-generation dependency chain
(image-generation-router + visual routing references) and port the skill and its
dependencies to Antigravity IDE and Codex hosts.

WHY: Client-ready PPTX decks are built across Claude Code, Codex, and Antigravity.
Image generation must route reliably on each host, and the Antigravity copy was a
fabricated SKILL.md claiming Kimi K3 performs image generation (it cannot — Kimi
is a VLM). That copy was a live routing hazard.

OUTCOME: (as contracted — see iteration log for delivery evidence)

CONSTRAINTS: honored — no execution-path enum gained a Kimi entry; no keys logged;
Codex system imagegen untouched; scripts stdlib-only; fabricated file backed up.

VERIFICATION:
- [x] V1 validate_contract.py exit 0 — "image-generation routing contract: valid"
- [x] V2 pytest -q router+pptx-visual-spec tests — 33 passed
- [x] V3 audit_portability.py exit 0 for claude/codex/project-agents AND
      antigravity/gemini-config (--windows-home /mnt/c/Users/sheke)
- [x] V4 ported SKILL.md at both Antigravity targets: exists, byte-identical to
      canonical, zero "kimi" mentions
- [x] V5 kimi_adapter.py --probe without key: exit 1, clear KIMI_API_KEY error,
      no traceback, no key echoed

## State
- Status: done
- Turns used: 6 / 30

## Iteration log
1. Recon: install_cross_host.py supports codex/antigravity/gemini-config; Codex
   already had the vault symlink (~/.codex/skills → hyundai-ai-vault canonical)
   and image-generation-router. Fabricated 3.3KB Kimi SKILL.md confirmed identical
   in both Antigravity roots.
2. Built scripts/kimi_adapter.py (stdlib, helper-only: --refine-prompt,
   --describe-image, --probe, --list-models; sidecar declares
   is_image_generation:false, no execution_path field) + tests/test_kimi_adapter.py
   (10 tests incl. enum-stays-kimi-free guard). Documented "Kimi K3 Helper (Not A
   Provider)" in router SKILL.md + reference.md; frontmatter permissions updated.
3. V1/V2/V5 green.
4. Ported vault skill: backed up fabricated SKILL.md → SKILL.md.fabricated.bak,
   copied canonical SKILL.md+references/+scripts/+assets/ to
   C:\Users\sheke\.gemini\config\skills\vault-presales-pptx-pipeline and
   D:\New folder\Antigravity-test\antigravity-skills\.agents\skills\...,
   wrote .ported-from provenance marker in each.
5. install_cross_host.py --host codex/antigravity/gemini-config for
   image-generation-router: codex ok (already managed), antigravity + gemini-config
   installed. Audits exit 0 (V3). V4 green.
6. skill_evals run: pre-existing findings only (drift on wrapper descriptions,
   OBF02 false-positive on generate_gemini base64 image decode, cosmetic
   cross-skill path lint) — verified via git stash baseline; my edits added none.

## Follow-on (2026-07-21, same session)
7. Key resolved: it is a ZenMux aggregator key, not native Kimi. Adapter gained
   config-file KIMI_BASE_URL support + moonshotai/kimi-k3-free preferred default;
   live-verified probe, prompt refinement, and vision review (found a real defect
   on docs/reports/_preview/slide_01.png). 34 tests green. Memory saved:
   reference_kimi_zenmux_key.md.
8. Full pipeline ported: installer refreshed pptx-visual-spec, branded-pptx-deck,
   genspark-branded-deck, genspark-slides, video-to-deck, excalidraw,
   image-generation-router on codex + antigravity + gemini-config (audits exit 0).
   ai-graphics copied to both Windows roots (examples/ omitted); vault skill
   copied to the .gemini/antigravity root too. officecli intentionally NOT
   installed on Windows roots — registry restricts it to claude/codex hosts
   (CLI runtime unverified on Windows-native); Antigravity QA falls back to
   preview contact sheets until that's verified.

## Live-key note (superseded — see item 7)
Stale as of item 7: the key is not invalid, it authenticates as a ZenMux
aggregator key against https://zenmux.ai/api/v1, not the native Kimi endpoint.
Config now carries both KIMI_API_KEY and KIMI_BASE_URL in ~/.config/kimi/.env.
Rotation is still recommended — the key appeared in plain text in transcripts.

## Codification pass (2026-07-22, same GOAL, new session after /compact)
9. User asked to "codify instructions, contracts, rules, if any further" —
   turned ad hoc manual-porting knowledge into durable docs:
   - New `skills/pptx-visual-spec/references/externally-ported-skills.md`:
     documents vault-presales-pptx-pipeline (5 manual copies + refresh script
     + kimi-regression grep check) and ai-graphics (2 manual copies + refresh
     script), both invisible to install_cross_host.py (external ownership /
     no repo source).
   - `skill-registry.json` gained `note` fields on the `officecli` and
     `vault-presales-pptx-pipeline` entries cross-referencing that file.
   - `external-capabilities.md` cross-references the new file (hosted
     connectors vs. externally-ported skills are separate concerns).
10. Post-codification verification (this is the chain that reported exit 1
    under a background task last session, whose output file no longer
    existed after /compact — re-ran from scratch instead of trusting stale
    IDs): validate_contract.py valid; 34/34 pytest green; registry JSON valid;
    audit_portability.py per-host (script takes one `--host` value at a time,
    not repeatable — my earlier chained `--host a --host b` invocation was
    invalid usage, not a real failure signal).
    - Found and fixed two REAL drift gaps predating this pass:
      (a) `agents` host was missing image-generation-router entirely
          (~/.agents/skills/) — installed via `install_cross_host.py --host
          agents --skill image-generation-router`.
      (b) `antigravity` and `gemini-config` Windows copies of
          `pptx-visual-spec` and `image-generation-router` had drifted behind
          this session's Kimi-adapter and codification edits — refreshed both
          with `install_cross_host.py --host <h> --skill pptx-visual-spec
          --skill image-generation-router --windows-home /mnt/c/Users/sheke`.
    - All 6 host groups (claude, codex, agents, project-agents, antigravity,
      gemini-config) now audit clean (exit 0).
    - Re-ran the vault-skill kimi-regression grep: only hits are the
      intentional `.ported-from` marker and `SKILL.md.fabricated.bak`; live
      SKILL.md files are clean on all 3 manually-ported copies.
    - Re-ran `tools/skill_evals/run_all.py`: no new issues beyond the
      pre-triaged backlog in CLAUDE.md. One new-looking CRITICAL
      (image-generation-router OBF02 generate_gemini.py:143) is a false
      positive — `base64.b64decode` to save image bytes, not exec/eval;
      pre-existing code, not touched this session. Two DRIFT findings
      (aianalyst-competitor-analysis, image-generation-router description
      differs across repo-relative `.agents/skills`/`.claude/skills`
      copies) are the documented-elsewhere "discovery wrappers are
      intentional" pattern (see memory `project_skills_audit_2026_07`) —
      confirmed via `git status` that neither wrapper file was touched this
      session.

Status: all 5 verification checks (V1-V5) still green; the two drift gaps
found during re-verification are now fixed, not just diagnosed.
