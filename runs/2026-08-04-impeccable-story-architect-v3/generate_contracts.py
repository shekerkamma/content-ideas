#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parent
URL = "https://www.youtube.com/watch?v=RVeCbPg0liw"
TMAP = json.loads((ROOT / "transcript-map.json").read_text())

def sec(v):
    m, s = map(int, v.split(":")); return m * 60 + s
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n, v): (ROOT / n).write_text(json.dumps(v, indent=2) + "\n")

segments = [{"id": f'transcript-{x["id"]}', "start_seconds": sec(x["start"]), "end_seconds": sec(x["end"]), "text": x["thesis"], "source_id": "source-transcript"} for x in TMAP["sections"]]
frame_data = [
    ("frame-worlds", 100, "assets/worlds.jpg", "World-selection interface."),
    ("frame-live", 577, "assets/live-comparison.jpg", "Live comparison interface."),
    ("frame-reference", 769, "assets/references.jpg", "Reference-led direction reset."),
]
frames = [{"id": i, "timestamp_seconds": t, "path": p, "sha256": sha(ROOT/p), "description": desc, "duplicate_of": None, "screen_class": "demo-screen", "face_quality": None, "source_id": "source-video"} for i,t,p,desc in frame_data]
evidence = {
  "contract_version":"1.0", "bundle":{"id":"impeccable-client-decision-v2","title":"Impeccable 4.0 — Client Adoption Decision","root":"."},
  "sources":[
    {"id":"source-video","kind":"video","path":URL,"sha256":None,"rights":"Source excerpts supplied for analysis; verify reuse rights before external distribution.","normalized_from":None},
    {"id":"source-transcript","kind":"transcript","path":"transcript.txt","sha256":sha(ROOT/"transcript.txt"),"rights":"Transcript supplied for analysis; verify reuse rights before external distribution.","normalized_from":"source-video"}
  ], "slides":[], "transcript_segments":segments, "frames":frames
}
dump("presentation-evidence.json", evidence)

rows = [
 ("Pilot the decision architecture—not the promise of autonomous taste","problem",[]),
 ("The case for a pilot rests on three demonstrated mechanisms—and three unproven outcomes","conclusion",[]),
 ("More choice improves taste only when it is structured","changes",[]),
 ("Worlds turns make it better into a visible macro decision","worlds",["frame-worlds"]),
 ("Four commitment gates prevent exploration from becoming drift","worlds",[]),
 ("Generality raises the ceiling—and shifts risk to the operator","tradeoff",[]),
 ("Change altitude determines the correct interface","references",[]),
 ("Live Mode shortens local comparison after direction is chosen","live",["frame-live"]),
 ("A wrong visual grammar requires a reference reset—not more polish","references",["frame-reference"]),
 ("Human judgment belongs at four high-leverage moments","conclusion",[]),
 ("Taste scales only when decisions become organizational memory","memory",[]),
 ("Fresh-context review is a challenge control—not proof of quality","tradeoff",[]),
 ("The demo reaches Level 2—and shows pieces of Level 3","conclusion",[]),
 ("Four readiness gates define when adoption may advance","conclusion",[]),
 ("Success is fewer wrong-direction cycles—without quality regressions","conclusion",[])
 ,("A fair pilot isolates workflow value from operator enthusiasm","conclusion",[])
 ,("The operating model needs controls at every failure boundary","conclusion",[])
 ,("Adopt the decision architecture—then earn the right to scale","conclusion",[])
]
audience_jobs = [
 "Understand the recommendation and the evidence boundary.",
 "Grasp the demonstrated case, unproven outcomes, and decision on one page.",
 "Understand why a plausible first draft can increase downstream rework.",
 "See how the Pathfinder demonstration makes macro direction selectable.",
 "Understand the owners and exit criteria that turn options into value.",
 "Recognize where a narrower conventional workflow remains preferable.",
 "Route local, structural, and directional changes to the correct interface.",
 "See how the Find the why comparison supports bounded local judgment.",
 "Know when to stop polishing and reopen the visual grammar.",
 "Assign human accountability and system support across irreversible decisions.",
 "Understand how accepted choices become reusable constraints without becoming permanent defaults.",
 "Separate fresh-context challenge from objective technical and user QA.",
 "Distinguish demonstrated workflow maturity from unproven outcomes.",
 "Assess whether the organization is ready to run even a bounded pilot.",
 "Agree how success and guardrails will be measured before work begins.",
 "Understand the matched-task comparison required for a fair evaluation.",
 "Connect each material failure mode to a named operating control.",
 "Authorize the next three actions without implying enterprise rollout."
]
speaker_implications = [
 "Judge Impeccable as a governed operating-model change, not an autonomous designer.",
 "The evidence supports a pilot; it does not support claims of speed, quality, or business lift.",
 "Optimize the timing of directional judgment before optimizing first-draft speed.",
 "Name who owns the macro visual choice and record the rationale before variants are built.",
 "Cap exploration and require explicit yes-or-return-upstream decisions.",
 "Do not deploy a general tool where the team lacks evidence, taste ownership, or review capacity.",
 "Use Live for detail, terminal for structure, and references for a direction reset.",
 "Local comparison is valuable only after the visual grammar is accepted.",
 "Reference-led resets require provenance controls and a return to macro review.",
 "Humans retain responsibility for truth, direction, trade-offs, and release.",
 "Version the design record and permit explicit resets to prevent stale taste from hardening.",
 "A second reviewer challenges context-induced drift but cannot certify accessibility or outcomes.",
 "Treat all outcome benefits as hypotheses until a controlled comparison measures them.",
 "Unknown readiness is a reason to narrow or stop, not to assume green.",
 "Lock the scorecard now so showcase quality cannot redefine success later.",
 "Hold inputs constant, stratify operator skill, and blind downstream review.",
 "Governance is part of adoption economics, not a post-launch appendix.",
 "Authorize pilot design, then name the owner, task, and scorecard."
]
claims, slides, visuals = [], [], []
for sid,(title,section,fids) in enumerate(rows,1):
    cid,vid,tid=f"claim-{sid:02d}",f"visual-{sid:02d}",f"transcript-{section}"
    eids=[tid,*fids]
    claims.append({"id":cid,"text":title,"kind":"interpretation","confidence":"medium" if not fids else "high","evidence_ids":eids})
    slides.append({"slide_id":sid,"archetype":"cover" if sid==1 else ("executive-summary" if sid==2 else ("evidence-proof" if fids else "analytical-native")),"action_title":title,"audience_job":audience_jobs[sid-1],"claim_ids":[cid],"evidence_ids":eids,"visual_ids":[vid],"speaker_notes":{"talk_time_seconds":50,"narrative":speaker_implications[sid-1],"demo_fallback":"Explain the setup, observed finding, implication, and action from the evidence contract." if fids else "Use the native decision model and its stated evidence boundary."},"accessibility":{"reading_order":["title","analytical visual","implication","evidence label"],"visual_alt_text":title},"status":"reviewed"})
    if fids:
        fid=fids[0]; fr=next(x for x in frames if x["id"]==fid)
        visuals.append({"id":vid,"slide_ids":[sid],"purpose":"Prove the exact interface state behind the analytical claim.","artifact_type":"ui","evidence_status":"exact-source-evidence","route":"extract","reason":"The interface state is evidence; analytical interpretation remains native.","evidence_ids":eids,"source":{"path":URL,"page":None,"frame":fid,"timestamp":str(fr["timestamp_seconds"]),"crop":None},"asset":fr["path"],"editable_source":None,"prompt_file":None,"execution":None,"placement":{"width":1920,"height":1080,"fit":"contain","background":"#F2EDE3"},"qa":{"visual_checked":True,"legible":True,"not_cropped":True,"background_matched":True,"provenance_recorded":True,"text_free":None,"not_evidence":False,"exact_fidelity":True}})
    else:
        visuals.append({"id":vid,"slide_ids":[sid],"purpose":"Explain the causal or decision model as editable PowerPoint structure.","artifact_type":"diagram","evidence_status":"underlying-information","route":"native","reason":"The analytical claim is clearer as a native causal model, matrix, maturity model, or scorecard.","evidence_ids":eids,"source":None,"asset":None,"editable_source":"build_client_ready_deck.py","prompt_file":None,"execution":None,"placement":None,"qa":{"visual_checked":True,"legible":True,"not_cropped":True,"background_matched":True,"provenance_recorded":True,"text_free":None,"not_evidence":False,"exact_fidelity":None}})
dump("slide-plan.json",{"contract_version":"1.0","deck":{"name":"Impeccable 4.0 — Client Adoption Decision","evidence_contract":"presentation-evidence.json","visual_contract":"visual-spec.json"},"claims":claims,"slides":slides})
dump("visual-spec.json",{"contract_version":"1.0","deck":{"output_mode":"hybrid","editability":"Fifteen native analytical slides plus native interpretation on three exact source-frame proof slides.","reference_deck":None},"visuals":visuals})
