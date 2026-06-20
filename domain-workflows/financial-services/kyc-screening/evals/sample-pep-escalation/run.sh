#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

python3 "$ROOT/scripts/run_kyc_screening.py" \
  "$ROOT/evals/sample-pep-escalation/input.json" \
  --rules "$ROOT/references/rules-grid.json" \
  --out "$ROOT/out"

python3 "$ROOT/scripts/validate_kyc_disposition.py" \
  "$ROOT/out/kyc-disposition.json" \
  --input "$ROOT/evals/sample-pep-escalation/input.json" \
  --rules "$ROOT/references/rules-grid.json" \
  --expected-minimum "$ROOT/evals/sample-pep-escalation/expected-minimum.json"
