# Presentation pipeline cross-host contract

## Canonical source and installations

- Canonical portable source: `/home/sheke/content-ideas/skills/<skill>/`
- Claude Code installation: `/home/sheke/.claude/skills/<skill>/`
- Hermes Desktop installation, accessed from WSL:
  `/mnt/c/Users/sheke/AppData/Local/hermes/skills/<skill>/`
- Antigravity IDE installation, accessed from WSL:
  `/mnt/c/Users/sheke/.agent/skills/<skill>/`

Host installations are mirrors, not sources of truth. Improvements must be made or recovered into
the repository first and then synchronized.

## Governed bundle

The client-presentation bundle consists of:

- routing and source control: `present`, `watch`, and `presentation-source-bundle`;
- compound competitor analysis: `evidence-led-competitor-pipeline`,
  `competitor-analysis-pipeline`, `aianalyst-competitor-analysis`, and
  `compound-competitor-analysis-pptx`;
- analysis and review controls: `ai-analyst`, `story-architect`, `grill-me`, `meta-loop`, and
  `llm-council`;
- content and visual production: `presentation-content-writer`, `impeccable`,
  `explainer-graphic`, and `ai-graphics`; and
- native PPTX construction and QA: `branded-pptx-deck`, `pptx-toolkit`,
  `pptx-design-quality`, `pptx-visual-spec`, and `officecli`.

The compound competitor-analysis capability is portable only when the complete chain is present:
evidence-led orchestration → analytical evidence product → competitor client package → bounded
slide contracts and review-control integration → native build and Office QA. Installing only the
final PPTX skill is an incomplete port.

The specialized competitor-analysis overlay is machine-readable in
`config/compound-competitor-analysis-hosts.json`. It carries the competitor orchestrators,
Grill-Me → Meta LOOP → optional LLM Council review controls, and per-slide visual-contract layer.
It requires the generic presentation bundle above for source normalization, Story Architect,
native construction, and Office QA.

`video-to-deck` is intentionally excluded. Video intake must route through `watch`; presentation
construction must route through `present` and its selected native engine.

## Installation contract

Run:

```bash
bash scripts/sync-presentation-pipeline-hosts.sh
```

When the generic presentation bundle is already installed and only the compound competitor
capability changed, run the scoped overlay installer:

```bash
bash scripts/sync-compound-competitor-analysis-hosts.sh
```

The installer:

1. validates every canonical skill directory exists;
2. rejects `.env`, bytecode, and invalid text NUL content;
3. skips byte-identical installations;
4. moves a differing host installation to a timestamped recoverable backup;
5. copies the complete named skill directory; and
6. verifies the installed tree against the canonical source.

Target roots can be overridden with `CONTENT_IDEAS_ROOT`, `CLAUDE_SKILLS_ROOT`,
`HERMES_SKILLS_ROOT`, and `ANTIGRAVITY_SKILLS_ROOT`. Never infer a Windows host root from the
WSL Claude root.

## Runtime contract

- Both hosts must read `present/references/visible-skill-application-contract.md` for multi-skill
  deck work.
- A stage earns credit only when `skill-application-manifest.json` records its proper layer,
  artifact, and visible impact.
- Run `present/scripts/validate_skill_application.py <manifest> --check-files` before promotion.
- Client decks remain `draft` until contract validation, design lint, OfficeCLI real-render QA,
  manual visual inspection, and independent finish review all pass.
- Windows-native commands launched from WSL must receive explicit Windows paths and working
  directories; do not rely on a UNC current directory.
- LibreOffice is a Windows-host dependency on this machine, not a WSL package. Resolve it as
  `C:\Program Files\LibreOffice\program\soffice.exe` or, from WSL,
  `/mnt/c/Program Files/LibreOffice/program/soffice.exe`. A failed `command -v libreoffice` in
  Ubuntu does not establish that LibreOffice is missing from the host.

## Verification

After synchronization:

```bash
diff -qr skills/present /home/sheke/.claude/skills/present
diff -qr skills/present /mnt/c/Users/sheke/AppData/Local/hermes/skills/present
diff -qr skills/present /mnt/c/Users/sheke/.agent/skills/present
HERMES_HOME=/mnt/c/Users/sheke/AppData/Local/hermes hermes skills audit
HERMES_HOME=/mnt/c/Users/sheke/AppData/Local/hermes hermes skills list --source local
```

Verification reports must name the exact roots checked. A healthy Claude installation does not
prove the Hermes installation is healthy, or vice versa.

The machine-readable bundle and host roots live in `config/presentation-pipeline-hosts.json`.
Run the complete parity, integrity, runtime-path, and Hermes discovery gate with:

```bash
python3 scripts/verify-presentation-pipeline-hosts.py
```

Verify the compound overlay independently with:

```bash
python3 scripts/verify-presentation-pipeline-hosts.py \
  --manifest config/compound-competitor-analysis-hosts.json
```
