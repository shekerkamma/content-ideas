#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
claude_root=/home/sheke/.claude/skills
codex_root=/home/sheke/.codex/skills
dest_root="$repo_root/skills"
run_root="$repo_root/runs/skill-port"
manifest="$run_root/manifest.tsv"
exclusions="$run_root/exclusions.tsv"

mkdir -p "$run_root"
printf 'skill\tsource_host\tsource_path\tdestination\taction\n' >"$manifest"
printf 'skill\ttype\tpath\n' >"$exclusions"

rsync_args=(
  -aL
  --exclude=.git/
  --exclude=node_modules/
  --exclude=__pycache__/
  --exclude='*.pyc'
  --include='.env.example'
  --include='.env.template'
  --exclude='.env'
  --exclude='.env.*'
)

declare -A names=()
for root in "$claude_root" "$codex_root"; do
  while IFS= read -r -d '' entry; do
    name=$(basename "$entry")
    if [[ -f "$entry/SKILL.md" ]]; then
      names["$name"]=1
    elif [[ -L "$entry" && ! -e "$entry" ]]; then
      printf '%s\tbroken-symlink\t%s -> %s\n' \
        "$name" "$entry" "$(readlink "$entry")" >>"$exclusions"
      if [[ -f "$repo_root/portable-skills/$name/SKILL.md" ]]; then
        names["$name"]=1
      fi
    fi
  done < <(find "$root" -mindepth 1 -maxdepth 1 -print0)
done

while IFS= read -r name; do
  dest="$dest_root/$name"
  source_host=
  source_path=

  if [[ -f "$dest/SKILL.md" ]]; then
    printf '%s\trepository\t%s\t%s\tpreserved-existing\n' \
      "$name" "$dest" "$dest" >>"$manifest"
    continue
  fi

  # A physical Codex directory is an explicit Codex adaptation and wins over
  # a same-name Claude source. Valid Codex symlinks are used next, followed by
  # Claude-only sources.
  if [[ -d "$codex_root/$name" && ! -L "$codex_root/$name" && -f "$codex_root/$name/SKILL.md" ]]; then
    source_host=codex-physical
    source_path="$codex_root/$name"
  elif [[ -f "$codex_root/$name/SKILL.md" ]]; then
    source_host=codex-linked
    source_path="$codex_root/$name"
  elif [[ -f "$claude_root/$name/SKILL.md" ]]; then
    source_host=claude
    source_path="$claude_root/$name"
  elif [[ -f "$repo_root/portable-skills/$name/SKILL.md" ]]; then
    source_host=recovered-portable
    source_path="$repo_root/portable-skills/$name"
  else
    printf '%s\tunresolved\t%s\n' "$name" "$name" >>"$exclusions"
    continue
  fi

  mkdir -p "$dest"
  rsync "${rsync_args[@]}" "$source_path/" "$dest/"
  printf '%s\t%s\t%s\t%s\tcopied\n' \
    "$name" "$source_host" "$(readlink -f "$source_path")" "$dest" >>"$manifest"

  while IFS= read -r excluded; do
    [[ -n "$excluded" ]] || continue
    printf '%s\tsecret-env\t%s\n' "$name" "$excluded" >>"$exclusions"
  done < <(find -L "$source_path" -type f \( -name .env -o -name '.env.*' \) \
    ! -name .env.example ! -name .env.template -print 2>/dev/null)
done < <(printf '%s\n' "${!names[@]}" | sort)

printf 'skills_total\t%s\n' "$(tail -n +2 "$manifest" | wc -l)"
printf 'skills_copied\t%s\n' "$(awk -F '\t' '$5 == "copied" {count++} END {print count+0}' "$manifest")"
printf 'skills_preserved\t%s\n' "$(awk -F '\t' '$5 == "preserved-existing" {count++} END {print count+0}' "$manifest")"
printf 'manifest\t%s\n' "$manifest"
printf 'exclusions\t%s\n' "$exclusions"
