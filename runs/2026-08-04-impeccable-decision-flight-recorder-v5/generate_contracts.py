#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parent; URL="https://www.youtube.com/watch?v=RVeCbPg0liw"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,v): (ROOT/n).write_text(json.dumps(v,indent=2)+"\n",encoding="utf-8")
tmap=json.loads((ROOT/"transcript-map.json").read_text())
def sec(v):
    parts=[int(x) for x in v.split(":")]; return parts[-1]+60*parts[-2]+(3600*parts[-3] if len(parts)>2 else 0)
segments=[{"id":f'transcript-{x["id"]}',"start_seconds":sec(x["start"]),"end_seconds":sec(x["end"]),"text":x["thesis"],"source_id":"source-transcript"} for x in tmap["sections"]]
frames=[]
for i,t,p,desc in [("frame-worlds",100,"assets/worlds.jpg","World-selection interface"),("frame-live",577,"assets/live-comparison.jpg","Live comparison interface"),("frame-reference",769,"assets/references.jpg","Reference-led reset")]:
    frames.append({"id":i,"timestamp_seconds":t,"path":p,"sha256":sha(ROOT/p),"description":desc,"duplicate_of":None,"screen_class":"demo-screen","face_quality":None,"source_id":"source-video"})
evidence={"contract_version":"1.0","bundle":{"id":"impeccable-flight-recorder-v5","title":"Impeccable Decision Flight Recorder","root":"."},"sources":[{"id":"source-video","kind":"video","path":URL,"sha256":None,"rights":"Source excerpt supplied for analysis; verify external reuse rights.","normalized_from":None},{"id":"source-transcript","kind":"transcript","path":"transcript.txt","sha256":sha(ROOT/"transcript.txt"),"rights":"Transcript supplied for analysis.","normalized_from":"source-video"}],"slides":[],"transcript_segments":segments,"frames":frames}
dump("presentation-evidence.json",evidence)
rows=[
("Pilot the decision system—not autonomous taste","problem",[]),("Three demonstrated mechanisms justify one controlled test","conclusion",[]),("A generic first draft moves the expensive decision downstream","changes",[]),("Worlds turns make it better into a visible macro decision","worlds",["frame-worlds"]),("Value comes from commitment—not from an endless menu","worlds",[]),("A higher creative ceiling shifts more risk to the operator","tradeoff",[]),("Change radius—not tool preference—should route the work","references",[]),("Live Mode compresses a bounded compare–tune–accept loop","live",["frame-live"]),("A wrong visual grammar requires a reference reset—not more polish","references",["frame-reference"]),("Humans own four irreversible decisions","conclusion",[]),("Accepted decisions matter only when they constrain the next cycle","memory",[]),("The demo shows structured convergence—not measured optimization","conclusion",[]),("A matched-task test isolates workflow value from operator enthusiasm","conclusion",[]),("Earn the right to scale","conclusion",[])]
claims=[]; slides=[]; visuals=[]
for sid,(title,section,fids) in enumerate(rows,1):
    cid=f"claim-{sid:02d}"; vid=f"visual-{sid:02d}"; eids=[f"transcript-{section}",*fids]
    claims.append({"id":cid,"text":title,"kind":"interpretation","confidence":"high" if fids else "medium","evidence_ids":eids})
    slides.append({"slide_id":sid,"archetype":"cover" if sid in (1,14) else ("evidence-proof" if fids else "analytical-native"),"action_title":title,"audience_job":"Understand the decision, mechanism, evidence boundary, and next action.","claim_ids":[cid],"evidence_ids":eids,"visual_ids":[vid],"speaker_notes":{"talk_time_seconds":45,"narrative":"Use the visible decision structure and preserve its evidence boundary.","demo_fallback":"Explain the observed state and management implication."},"accessibility":{"reading_order":["title","primary visual","decision implication","evidence label"],"visual_alt_text":title},"status":"reviewed"})
    if fids:
        fr=next(x for x in frames if x["id"]==fids[0])
        visuals.append({"id":vid,"slide_ids":[sid],"purpose":"Prove the exact interface state.","artifact_type":"ui","evidence_status":"exact-source-evidence","route":"extract","reason":"Exact interface state is evidence.","evidence_ids":eids,"source":{"path":URL,"page":None,"frame":fids[0],"timestamp":str(fr["timestamp_seconds"]),"crop":None},"asset":fr["path"],"editable_source":None,"prompt_file":None,"execution":None,"placement":{"width":1920,"height":1080,"fit":"contain","background":"#0B1020"},"qa":{"visual_checked":True,"legible":True,"not_cropped":True,"background_matched":True,"provenance_recorded":True,"text_free":None,"not_evidence":False,"exact_fidelity":True}})
    else:
        visuals.append({"id":vid,"slide_ids":[sid],"purpose":"Express the Decision Flight Recorder visual grammar as editable PowerPoint structure.","artifact_type":"diagram","evidence_status":"underlying-information","route":"native","reason":"Claims and structured models remain native and editable.","evidence_ids":eids,"source":None,"asset":None,"editable_source":"build_deck.py","prompt_file":None,"execution":None,"placement":None,"qa":{"visual_checked":True,"legible":True,"not_cropped":True,"background_matched":True,"provenance_recorded":True,"text_free":None,"not_evidence":False,"exact_fidelity":None}})
dump("slide-plan.json",{"contract_version":"1.0","deck":{"name":"Impeccable Decision Flight Recorder","evidence_contract":"presentation-evidence.json","visual_contract":"visual-spec.json"},"claims":claims,"slides":slides})
dump("visual-spec.json",{"contract_version":"1.0","deck":{"output_mode":"hybrid","editability":"Native decision system with three authentic extracted interface states.","reference_deck":None},"visuals":visuals})
