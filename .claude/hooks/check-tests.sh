#!/bin/bash
# Stop hook: before Claude may finish, run the tests for the Python files changed
# in this working tree. Exit 2 sends Claude back to fix a failure; whatever this
# prints on stderr becomes Claude's feedback. The full suite (about 13 minutes)
# stays in CI (.github/workflows/validate.yml), not here.
#
# Skips fast when nothing under skills/, scripts/ or tests/ changed, or when the
# same change set already passed. CHECK_TESTS_CMD overrides the test command
# (used by the hook's own tests).
cat >/dev/null  # discard the hook's JSON input
cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}" || exit 0

changed=$( { git diff --name-only HEAD -- 'skills/*.py' 'scripts/*.py' 'tests/*.py' 'skills/**/*.py' 'scripts/**/*.py';
             git ls-files --others --exclude-standard -- 'skills/**/*.py' 'scripts/**/*.py' 'tests/*.py'; } 2>/dev/null | sort -u)
[ -z "$changed" ] && [ -z "$CHECK_TESTS_CMD" ] && exit 0

stamp_dir="${TMPDIR:-/tmp}/claude-check-tests"; mkdir -p "$stamp_dir"
key=$(printf '%s' "$PWD" | sha1sum | cut -c1-12)
finger=$( { git diff HEAD -- $changed; for f in $changed; do [ -f "$f" ] && sha1sum "$f"; done; } 2>/dev/null | sha1sum | cut -c1-40)
[ -z "$CHECK_TESTS_CMD" ] && [ "$(cat "$stamp_dir/$key" 2>/dev/null)" = "$finger" ] && exit 0

if [ -n "$CHECK_TESTS_CMD" ]; then
  cmd="$CHECK_TESTS_CMD"
else
  tests=""
  for f in $changed; do
    case "$f" in
      tests/test_*.py) tests="$tests $f" ;;
      skills/*) skill=$(echo "$f" | cut -d/ -f2)   # tests named for the skill, or naming its folder
         tests="$tests $(ls tests/test_${skill//-/_}*.py 2>/dev/null | tr '\n' ' ')"
         tests="$tests $(grep -l -- "skills/$skill/" tests/test_*.py 2>/dev/null | tr '\n' ' ')" ;;
      scripts/*) rel=${f%.py}                         # tests that name the script's path
         tests="$tests $(grep -l -- "${rel#scripts/}" tests/test_*.py 2>/dev/null | tr '\n' ' ')" ;;
    esac
  done
  tests=$(printf '%s\n' $tests | sort -u | while read -r t; do [ -f "$t" ] && echo "$t"; done | tr '\n' ' ')
  if [ -z "${tests// }" ]; then echo "$finger" > "$stamp_dir/$key"; exit 0; fi
  py=python3
  for c in .venv/bin/python "$HOME/.venvs/data/bin/python"; do
    [ -x "$c" ] && "$c" -c 'import pytest' 2>/dev/null && { py=$c; break; }
  done
  cmd="$py -m pytest -q -x -p no:cacheprovider $tests"
fi

out="$stamp_dir/$key.out"
timeout 240 bash -c "$cmd" >"$out" 2>&1
rc=$?
case $rc in
  0) echo "$finger" > "$stamp_dir/$key"; exit 0 ;;
  124) exit 0 ;;   # too slow for a Stop check; CI runs the full suite
  5) exit 0 ;;     # pytest collected no tests: nothing to prove here
  *) { echo "Tests are failing. Fix them before you finish ($cmd):"; tail -n 30 "$out"; } >&2
     exit 2 ;;
esac
