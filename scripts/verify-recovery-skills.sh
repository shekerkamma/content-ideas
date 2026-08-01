#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills=(docx pdf improve storm-research)
expected_storm_template_sha256="14a130135fe37de055007ff4da4575845819b1f83c27817ca56f9996832c9028"
pycache_root="$(mktemp -d)"
trap 'rm -rf "${pycache_root}"' EXIT

for skill in "${skills[@]}"; do
  skill_root="${repo_root}/skills/${skill}"
  test -s "${skill_root}/SKILL.md" || {
    echo "missing or empty skill manifest: ${skill_root}/SKILL.md" >&2
    exit 1
  }
done

if find "${repo_root}/skills/docx" \
        "${repo_root}/skills/pdf" \
        "${repo_root}/skills/improve" \
        "${repo_root}/skills/storm-research" \
        \( -type d -name __pycache__ -o -type f -name '*.pyc' \) \
        -print -quit | grep -q .; then
  echo "generated Python cache found in portable skills" >&2
  exit 1
fi

while IFS= read -r -d '' path; do
  if python3 -c 'import pathlib, sys; raise SystemExit(0 if b"\0" in pathlib.Path(sys.argv[1]).read_bytes() else 1)' "${path}"; then
    echo "NUL byte found in source file: ${path}" >&2
    exit 1
  fi
done < <(find "${repo_root}/skills/docx" \
               "${repo_root}/skills/pdf" \
               "${repo_root}/skills/improve" \
               "${repo_root}/skills/storm-research" \
               -type f -print0)

while IFS= read -r -d '' path; do
  PYTHONPYCACHEPREFIX="${pycache_root}" python3 -m py_compile "${path}"
done < <(find "${repo_root}/skills/docx" \
               "${repo_root}/skills/pdf" \
               "${repo_root}/skills/improve" \
               "${repo_root}/skills/storm-research" \
               -type f -name '*.py' -print0)

storm_template="${repo_root}/skills/storm-research/report-template.html"
actual_storm_template_sha256="$(sha256sum "${storm_template}" | awk '{print $1}')"
if [[ "${actual_storm_template_sha256}" != "${expected_storm_template_sha256}" ]]; then
  echo "unexpected storm-research template hash" >&2
  exit 1
fi

echo "recovery skill verification passed: ${skills[*]}"
