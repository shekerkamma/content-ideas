#!/usr/bin/env bash
# Stage WSL-canonical skills into a Windows-reachable bundle for Claude Desktop / Cowork.
#
# WHY A BUNDLE (not a symlink/copy-into-place like Antigravity):
# Claude Cowork runs in its OWN isolated sandbox. That sandbox's filesystem is
# neither the WSL filesystem (where Claude Code reads ~/.claude/skills) nor the
# shared C:\ mount. There is no folder on disk that both hosts read, so skills
# cannot be propagated by copy/symlink. The only transfer path into Cowork is
# THROUGH the Cowork chat: upload this bundle (or its .zip) into a Cowork session
# and tell the agent to unpack each skill into its own skills dir
# (e.g. ClaudeOS/skills/<name>/ or ~/.claude/skills/<name>/).
#
# Claude CODE (in Claude Desktop, WSL-backed) already reads ~/.claude/skills
# directly — it needs nothing from this script. This bundle exists purely to
# carry the SAME skills across the Cowork sandbox boundary.
#
# Canonical source of truth stays in WSL. Re-run after editing any listed skill.
set -euo pipefail

WIN_USER="${WIN_USER:-sheke}"
OUT_DIR="${CLAUDE_DESKTOP_BUNDLE:-/mnt/c/Users/${WIN_USER}/claude-skills-bundle}"
STAGE="$OUT_DIR/skills"
ZIP_PATH="$OUT_DIR/claude-skills-bundle.zip"

# dest-name = canonical WSL source path. Same portable set as the Antigravity sync.
declare -A SKILLS=(
  [watch]="$HOME/.claude/skills/watch"
  [marp]="$HOME/.claude/skills/marp"
  [refero-design]="$HOME/.agents/skills/refero-design"
  [learn-anything]="$HOME/.claude/skills/learn-anything"
  [genspark-slides]="$HOME/.claude/skills/genspark-slides"
  [watch-video]="$HOME/.claude/skills/watch-video"
  [content-ideas]="$HOME/content-ideas/skills/content-ideas"
  [pipeline-runner]="$HOME/content-ideas/skills/pipeline-runner"
  [storm-research]="$HOME/content-ideas/skills/storm-research"
  [you-com-search]="$HOME/content-ideas/skills/you-com-search"
  [ai-head-of-engineering]="$HOME/content-ideas/skills/ai-head-of-engineering"
  [ai-head-of-engineering-scope-killer]="$HOME/content-ideas/skills/ai-head-of-engineering-scope-killer"
  [ai-head-of-engineering-scope-architect]="$HOME/content-ideas/skills/ai-head-of-engineering-scope-architect"
  [ai-head-of-engineering-stack-picker]="$HOME/content-ideas/skills/ai-head-of-engineering-stack-picker"
  [ai-head-of-engineering-build-vs-buy-auditor]="$HOME/content-ideas/skills/ai-head-of-engineering-build-vs-buy-auditor"
  [ai-head-of-engineering-build-estimator]="$HOME/content-ideas/skills/ai-head-of-engineering-build-estimator"
  [ai-head-of-engineering-ai-use-case-validator]="$HOME/content-ideas/skills/ai-head-of-engineering-ai-use-case-validator"
  [ai-head-of-engineering-custom-internal-tool-designer]="$HOME/content-ideas/skills/ai-head-of-engineering-custom-internal-tool-designer"
  [ai-head-of-engineering-pre-launch-auditor]="$HOME/content-ideas/skills/ai-head-of-engineering-pre-launch-auditor"
  [ai-head-of-engineering-30-day-build-roadmap]="$HOME/content-ideas/skills/ai-head-of-engineering-30-day-build-roadmap"
  [exa-api]="$HOME/content-ideas/skills/exa-api"
  [firecrawl]="$HOME/content-ideas/skills/firecrawl"
  [goal-loop-orchestrator]="$HOME/content-ideas/skills/goal-loop-orchestrator"
  [master-implementation-blueprint]="$HOME/content-ideas/skills/master-implementation-blueprint"
  [agentic-blueprint-pipeline]="$HOME/content-ideas/skills/agentic-blueprint-pipeline"
  [disruptive-teardown-pipeline]="$HOME/content-ideas/skills/disruptive-teardown-pipeline"
  [strategy-consulting]="$HOME/content-ideas/skills/strategy-consulting"
  [aeo-orchestrator]="$HOME/content-ideas/skills/aeo-orchestrator"
  [aeo-query-planner]="$HOME/content-ideas/skills/aeo-query-planner"
  [saas-gap-analyzer]="$HOME/content-ideas/skills/saas-gap-analyzer"
  [reddit-new-factcheck]="$HOME/content-ideas/skills/reddit-new-factcheck"
  [reddit-seo-pipeline]="$HOME/content-ideas/skills/reddit-seo-pipeline"
  [aeo-source-discovery]="$HOME/content-ideas/skills/aeo-source-discovery"
  [aeo-reddit-opportunity-finder]="$HOME/content-ideas/skills/aeo-reddit-opportunity-finder"
  [aeo-evidence-sprint-loop]="$HOME/content-ideas/skills/aeo-evidence-sprint-loop"
  [founders-build-stack]="$HOME/content-ideas/.claude/skills/founders-build-stack"
  [gcc-roadmap]="$HOME/content-ideas/.agents/skills/gcc-roadmap"
  [improve]="$HOME/content-ideas/.agents/skills/improve"
  [skill-builder]="$HOME/content-ideas/.claude/skills/skill-builder"
)

[ -d "$(dirname "$OUT_DIR")" ] || { echo "ERROR: Windows mount not found: $(dirname "$OUT_DIR")" >&2; exit 1; }
rm -rf "$STAGE"; mkdir -p "$STAGE"

synced=0
for name in "${!SKILLS[@]}"; do
  src="${SKILLS[$name]}"
  if [ ! -e "$src" ]; then echo "skip $name (source missing: $src)"; continue; fi
  # -L resolves symlinks so the bundle carries real files, not dangling links.
  cp -rL "$src" "$STAGE/$name"
  synced=$((synced + 1))
  echo "staged $name"
done

# Zip via Python stdlib (no `zip` binary required on WSL).
python3 - "$STAGE" "$ZIP_PATH" <<'PY'
import sys, zipfile, os
stage, zip_path = sys.argv[1], sys.argv[2]
if os.path.exists(zip_path):
    os.remove(zip_path)
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(stage):
        for f in files:
            full = os.path.join(root, f)
            # arcname keeps a top-level "skills/" prefix for tidy unpacking
            arc = os.path.join("skills", os.path.relpath(full, stage))
            z.write(full, arc)
print(f"zipped -> {zip_path}")
PY

echo
echo "Done. Staged $synced skills."
echo "  Folder: $OUT_DIR/skills"
echo "  Zip:    $ZIP_PATH"
echo
echo "To load into Claude Cowork: open a Cowork session, upload the .zip, and ask"
echo "the agent to unpack each folder into its skills dir (ClaudeOS/skills/<name>/)."
