#!/usr/bin/env python3
"""Validate the minimum governed artifact set for a client-ready strategy PPTX run."""
import argparse, json, sys
from pathlib import Path

REQUIRED = ['deck-brief.md','deck-design.json','template-profile.json','slide-plan.json','visual-spec.json','slide-content-contracts.json','slide-design-contracts.json']
CONTENT = ['slide_id','assertion_title','analytical_question','executive_answer','evidence_blocks','comparison_logic','counterargument','implication','decision','owner','trigger','exhibit','source_note']
DESIGN = ['slide_number','family','visual_thesis','design_prompt','layout_contract','graphic_contract','typography_contract','content_limits','evidence_regions','visual_routes','prohibited','qa_questions']

def load(path):
 try: return json.loads(path.read_text())
 except Exception as e: raise ValueError(f'{path}: {e}')
def rows(data, keys):
 if isinstance(data,list): return data
 for k in keys:
  if isinstance(data.get(k),list): return data[k]
 return []

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('run_dir',type=Path); ap.add_argument('--json',action='store_true'); ap.add_argument('--competitor',action='store_true',help='require competitor evidence and Grill-Me → Meta LOOP artifacts'); ap.add_argument('--reviewed',action='store_true',help='require reviewed-promotion artifacts and manifest'); a=ap.parse_args(); r=a.run_dir.resolve(); errors=[]; warnings=[]
 for n in REQUIRED:
  if not (r/n).is_file(): errors.append(f'missing {n}')
 if not errors:
  try:
   content=rows(load(r/'slide-content-contracts.json'),['slides','contracts'])
   design=rows(load(r/'slide-design-contracts.json'),['slides','contracts'])
   if not content: errors.append('slide-content-contracts.json has no slides')
   if not design: errors.append('slide-design-contracts.json has no slides')
   for i,x in enumerate(content,1):
    for k in CONTENT:
     if x.get(k) in (None,'',[]): errors.append(f'content slide {i}: missing {k}')
    if len(x.get('evidence_blocks',[])) not in range(2,5): warnings.append(f'content slide {i}: expected 2–4 evidence blocks')
   for i,x in enumerate(design,1):
    for k in DESIGN:
     if x.get(k) in (None,'',[]): errors.append(f'design slide {i}: missing {k}')
    if len(x.get('qa_questions',[])) < 5: errors.append(f'design slide {i}: fewer than five QA questions')
   if len(content)!=len(design): errors.append(f'contract count mismatch: content={len(content)} design={len(design)}')
   plan=load(r/'slide-plan.json'); plan_rows=rows(plan,['slides'])
   if plan_rows and len(plan_rows)!=len(content): errors.append(f'slide-plan count {len(plan_rows)} != content count {len(content)}')
  except ValueError as e: errors.append(str(e))
 pptx=list((r/'client-package').glob('*-reviewed.pptx')) if (r/'client-package').exists() else []
 if pptx and not (r/'qa/officecli/qa-summary.md').is_file() and not (r/'client-package/qa/officecli/qa-summary.md').is_file(): errors.append('reviewed deck exists without OfficeCLI qa-summary.md')
 if a.competitor:
  competitor_required=['outputs/evidence-ledger.csv','outputs/metric-definitions.md','outputs/data-quality-report.md','outputs/scoring-model.md','outputs/allowed-numbers.yaml','outputs/competitor-brief.md','outputs/story-architect-pack.md','grill-ledger.json','meta-loop/final-rewrite-blueprint.json']
  for n in competitor_required:
   if not (r/n).exists(): errors.append(f'competitor pipeline missing {n}')
  if (r/'grill-ledger.json').is_file():
   try:
    controls=rows(load(r/'grill-ledger.json'),['controls'])
    if not controls: errors.append('grill-ledger.json has no controls')
   except ValueError as e: errors.append(str(e))
  if (r/'meta-loop/final-rewrite-blueprint.json').is_file():
   try:
    bp=load(r/'meta-loop/final-rewrite-blueprint.json')
    if not bp.get('slides'): errors.append('final-rewrite-blueprint.json has no slide dispositions')
   except ValueError as e: errors.append(str(e))
 if a.reviewed:
  reviewed_required=['claim-slide-traceability.json','client-package/delivery-manifest.json']
  for n in reviewed_required:
   if not (r/n).is_file(): errors.append(f'reviewed promotion missing {n}')
  summaries=list(r.glob('qa/officecli/qa-summary.md'))+list(r.glob('client-package/qa/officecli/qa-summary.md'))
  if not summaries: errors.append('reviewed promotion missing OfficeCLI qa-summary.md')
  elif not any('Status: passed' in p.read_text() or 'Status: reviewed' in p.read_text() for p in summaries): errors.append('OfficeCLI QA summary is not passed')
  if (r/'client-package/delivery-manifest.json').is_file():
   try:
    dm=load(r/'client-package/delivery-manifest.json')
    if dm.get('status')!='reviewed': errors.append('delivery manifest status is not reviewed')
    if not (dm.get('delivery') or {}).get('sha256_source'): errors.append('delivery manifest lacks source checksum')
    if not (dm.get('delivery') or {}).get('sha256_destination'): errors.append('delivery manifest lacks destination checksum')
   except ValueError as e: errors.append(str(e))
 result={'status':'pass' if not errors else 'fail','run_dir':str(r),'errors':errors,'warnings':warnings}
 print(json.dumps(result,indent=2) if a.json else '\n'.join([f"Status: {result['status']}"]+[f'ERROR: {x}' for x in errors]+[f'WARN: {x}' for x in warnings]))
 return 0 if not errors else 2
if __name__=='__main__': sys.exit(main())
