#!/usr/bin/env bash
# Sync selected WSL-canonical skills into the Windows-side Antigravity skills dir.
#
# Antigravity IDE is Windows-native and does NOT support WSL — it cannot read the
# WSL filesystem, so skills must be COPIED to C:\Users\<user>\.agents\skills\.
# Symlinks can't bridge WSL->Windows for a native app, so there is no live
# propagation: re-run this script after editing any listed skill.
#
# Canonical source of truth stays in WSL (~/.claude/skills/... or ~/.agents/skills/...).
# This script is the single place that defines WHICH skills Antigravity gets.
set -euo pipefail

WIN_USER="${WIN_USER:-sheke}"
# Antigravity reads user skills from these roots on Windows (the IDE's ~100 skills
# live in .gemini/antigravity/skills; .gemini/config/skills is the Gemini-CLI mirror).
# NOTE: NOT ~/.agents/skills — that is a separate toolset Antigravity does not load.
TARGET_ROOTS=(
  "/mnt/c/Users/${WIN_USER}/.gemini/antigravity/skills"
  "/mnt/c/Users/${WIN_USER}/.gemini/config/skills"
)

# dest-name = canonical WSL source path. Add skills here to push them to Antigravity.
declare -A SKILLS=(
  [watch]="$HOME/.claude/skills/watch"
  [marp]="$HOME/.claude/skills/marp"
  [genspark-slides]="$HOME/.claude/skills/genspark-slides"
  [watch-video]="$HOME/.claude/skills/watch-video"
  [refero-design]="$HOME/.agents/skills/refero-design"
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

found_root=0
for root in "${TARGET_ROOTS[@]}"; do
  [ -d "$root" ] || { echo "skip root (not found): $root"; continue; }
  found_root=1
  for name in "${!SKILLS[@]}"; do
    src="${SKILLS[$name]}"
    if [ ! -e "$src" ]; then echo "skip $name (source missing: $src)"; continue; fi
    dest="$root/$name"
    rm -rf "$dest"
    # -L resolves symlinks so Windows receives real files, not dangling links.
    cp -rL "$src" "$dest"
    echo "synced $name -> $dest"
  done
done

# --- HyperFrames bundle ---------------------------------------------------
# HyperFrames ships ~19 interdependent skills (~/hyperframes/skills/*) that
# cross-reference each other with ../sibling/ relative paths and run a Node CLI
# (`npx hyperframes ...`). They must be copied as INDIVIDUAL top-level sibling
# skill dirs (NOT one nested folder) so those ../ references still resolve.
# RUNTIME NOTE: Antigravity executes on Windows, so to actually render you also
# need Node >=22, FFmpeg, and `npm i -g hyperframes` installed on Windows.
HF_SKILLS="$HOME/hyperframes/skills"
if [ -d "$HF_SKILLS" ]; then
  for root in "${TARGET_ROOTS[@]}"; do
    [ -d "$root" ] || continue
    n=0
    for d in "$HF_SKILLS"/*/; do
      name="$(basename "$d")"
      dest="$root/$name"
      rm -rf "$dest"
      cp -rL "$d" "$dest"
      n=$((n + 1))
    done
    echo "synced HyperFrames bundle ($n skills) -> $root"
  done
else
  echo "skip HyperFrames bundle (source missing: $HF_SKILLS — clone github.com/heygen-com/hyperframes)"
fi

[ "$found_root" = 1 ] || { echo "ERROR: no Antigravity skill root found" >&2; exit 1; }

# Reconcile every PPTX-producing skill through the repo-canonical portability registry.
# This runs after the legacy list because several entries overlap; the managed pass restores
# canonical content, writes copy markers, and backs up any genuinely divergent host copy.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PPTX_INSTALLER="$REPO_ROOT/skills/pptx-visual-spec/scripts/install_cross_host.py"
if [ -f "$PPTX_INSTALLER" ]; then
  python3 "$PPTX_INSTALLER" \
    --host antigravity \
    --host gemini-config \
    --windows-home "/mnt/c/Users/${WIN_USER}" \
    --mode copy \
    --adopt-identical \
    --replace-unmanaged
else
  echo "skip managed PPTX skills (installer missing: $PPTX_INSTALLER)"
fi

echo "Done. Restart Antigravity to pick up changes."
