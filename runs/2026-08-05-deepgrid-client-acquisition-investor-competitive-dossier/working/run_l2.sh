#!/usr/bin/env bash
# You.com Level 2 = discovery + fresh Exa extraction. Unset poisoned WSL vars first.
q="$1"; slug="$2"
env -u YOU_API_KEY -u YDC_API_KEY python3 ~/.claude/skills/you-com-search/scripts/level2_search.py "$q" \
  > "working/captures/${slug}.json" 2>"working/captures/${slug}.err"
python3 - "$slug" "$q" <<'PY'
import json,sys,pathlib
slug,q=sys.argv[1],sys.argv[2]
p=pathlib.Path(f"working/captures/{slug}.json")
try: d=json.loads(p.read_text())
except Exception as e: print(f"  {slug}: FAILED ({e})"); raise SystemExit
disc=d.get("discovery",{}).get("results",{}).get("web",[])
ext=d.get("extracted",{}).get("results",[])
st=d.get("extracted",{}).get("statuses",[])
ok=sum(1 for s in st if str(s.get("status","")).startswith("2") or s.get("ok"))
print(f"  {slug}: discovery={len(disc)} extracted={len(ext)} statuses={len(st)}")
PY
