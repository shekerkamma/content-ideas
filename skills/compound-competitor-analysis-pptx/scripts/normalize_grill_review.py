#!/usr/bin/env python3
"""Normalize a slide-level grill-me review into the canonical atomic control ledger."""
import argparse,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('review',type=Path);ap.add_argument('out',type=Path);a=ap.parse_args();d=json.loads(a.review.read_text());controls=[]
 for i,s in enumerate(d.get('slides',[]),1):
  slide=s.get('slide',i); disp=str(s.get('disposition','TIGHTEN')).lower()
  layer='story' if slide<=4 else 'content'
  controls.append({
   'control_id':f'G-{i:03d}','question':s.get('hostile_question',''),'answer':s.get('recommended_answer',''),'recommended_answer':s.get('recommended_answer',''),'answer_source':'self-answered' if d.get('self_answered_decisions') else 'user-confirmed','applies_to':{'scope':'slide','slide_ids':[slide]},'layer':layer,'required_visible_change':s.get('required_revision',''),'acceptance_test':f"Disposition {disp} is visible in title, exhibit, evidence boundary and decision rail",'evidence_ids':s.get('evidence_ids',[]),'status':'open','review_scores':s.get('scores',{}),'source_disposition':disp,'source_title':s.get('title',''),'source_archetype':s.get('archetype','')
  })
 out={'contract_version':'1.0','deck':d.get('deck',''),'governing_answer':d.get('governing_answer',''),'self_answered_decisions':d.get('self_answered_decisions',{}),'controls':controls}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,ensure_ascii=False));print(f'wrote {len(controls)} controls to {a.out}')
if __name__=='__main__':main()
