#!/usr/bin/env python3
"""Validate bounded authoring batches and consolidated slide-contract coverage."""
import argparse,json,sys
from pathlib import Path

def load(p): return json.loads(p.read_text())
def slide_rows(d):
 if isinstance(d,list): return d
 for k in ('slides','contracts'):
  if isinstance(d.get(k),list): return d[k]
 return []
def sid(x): return x.get('slide_id',x.get('slide_number'))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('run',type=Path);ap.add_argument('--manifest',default='authoring/batch-manifest.json');ap.add_argument('--json-out',type=Path);a=ap.parse_args();r=a.run.resolve();m=load(r/a.manifest);errors=[];warnings=[];seen=[];version=m.get('invariant_version');max_size=int(m.get('max_batch_size',4))
 for b in m.get('batches',[]):
  ids=b.get('slide_ids',[])
  if len(ids)>max_size: errors.append(f"{b.get('batch_id')}: {len(ids)} slides exceeds {max_size}")
  if len(ids)!=len(set(ids)): errors.append(f"{b.get('batch_id')}: duplicate requested IDs")
  if b.get('invariant_version',version)!=version: errors.append(f"{b.get('batch_id')}: invariant version drift")
  path=b.get('validated_output_path') or b.get('raw_output_path')
  if not path or not (r/path).is_file(): errors.append(f"{b.get('batch_id')}: output missing");continue
  rows=slide_rows(load(r/path));got=[sid(x) for x in rows]
  if got!=ids: errors.append(f"{b.get('batch_id')}: returned IDs {got} != requested {ids}")
  seen.extend(got)
 order=m.get('authoritative_slide_order',[])
 if seen!=order: errors.append(f'batch union/order does not match authoritative order: got {len(seen)}, expected {len(order)}')
 if len(seen)!=len(set(seen)): errors.append('slide IDs duplicated across batches')
 for key in ('consolidated_content','consolidated_design'):
  p=r/m.get(key,'')
  if not p.is_file(): errors.append(f'{key} missing');continue
  got=[sid(x) for x in slide_rows(load(p))]
  if got!=order: errors.append(f'{key} IDs/order do not match authoritative order')
 result={'status':'pass' if not errors else 'fail','invariant_version':version,'batch_count':len(m.get('batches',[])),'slide_count':len(order),'errors':errors,'warnings':warnings}
 out=json.dumps(result,indent=2);print(out)
 if a.json_out:a.json_out.parent.mkdir(parents=True,exist_ok=True);a.json_out.write_text(out+'\n')
 return 0 if not errors else 2
if __name__=='__main__':sys.exit(main())
