#!/usr/bin/env python3
"""Run reproducible OfficeCLI package/issues/render QA, including native Windows PowerPoint render."""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

def run(cmd, cwd=None):
 p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True); return p.returncode,p.stdout,p.stderr
def parse(s):
 try:return json.loads(s)
 except:return {'raw':s}
def sha(path):
 h=hashlib.sha256();
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('deck',type=Path); ap.add_argument('--out',type=Path,required=True); ap.add_argument('--required',action='store_true'); ap.add_argument('--native-windows',action='store_true'); ap.add_argument('--grid',default='5'); a=ap.parse_args()
 deck=a.deck.resolve(); out=a.out.resolve(); out.mkdir(parents=True,exist_ok=True); failures=[]
 if not deck.is_file(): print(f'missing deck: {deck}',file=sys.stderr); return 2
 if not shutil.which('officecli'): print('officecli not found',file=sys.stderr); return 2
 rc,stdout,stderr=run(['officecli','--version']); version=(stdout or stderr).strip()
 rc,vout,verr=run(['officecli','validate',str(deck),'--json']); validation=parse(vout); (out/'validate.json').write_text(json.dumps(validation,indent=2));
 if rc or not validation.get('success'): failures.append('OpenXML validation failed')
 rc,iout,ierr=run(['officecli','view',str(deck),'issues','--limit','5000','--json']); issues=parse(iout); (out/'issues.json').write_text(json.dumps(issues,indent=2)); count=((issues.get('data') or {}).get('count')) if isinstance(issues.get('data'),dict) else None
 if rc or count not in (0,None): failures.append(f'OfficeCLI issues={count}')
 rc,sout,serr=run(['officecli','view',str(deck),'stats','--json']); stats=parse(sout); (out/'stats.json').write_text(json.dumps(stats,indent=2)); slides=((stats.get('data') or {}).get('slides')) if isinstance(stats.get('data'),dict) else None
 html=out/'contact-html.png'; pages=f'1-{slides}' if slides else '1-999'
 rc,hout,herr=run(['officecli','view',str(deck),'screenshot','--page',pages,'--grid',str(a.grid),'--render','html','--screenshot-width','2400','--screenshot-height','1600','-o',str(html),'--json'])
 if rc or not html.is_file(): failures.append('HTML contact-sheet render failed')
 native=None
 if a.native_windows:
  winbin=Path('/mnt/c/Users')
  candidates=list(winbin.glob('*/AppData/Local/OfficeCLI/officecli.exe')) if winbin.exists() else []
  if not candidates or not shutil.which('powershell.exe'): failures.append('Windows OfficeCLI or PowerShell unavailable')
  else:
   tmp=Path('/mnt/c/Temp')/f'client-ready-pptx-qa-{os.getpid()}'; tmp.mkdir(parents=True,exist_ok=True); staged=tmp/'input.pptx'; shutil.copy2(deck,staged); native_win=tmp/'contact-native.png'
   user=str(candidates[0]).split('/')[4]; binwin=f'C:\\Users\\{user}\\AppData\\Local\\OfficeCLI\\officecli.exe'; ps=f"Set-Location 'C:\\Temp\\{tmp.name}'; & '{binwin}' view 'C:\\Temp\\{tmp.name}\\input.pptx' screenshot --page {pages} --grid {a.grid} --render native --screenshot-width 2400 --screenshot-height 1600 -o 'C:\\Temp\\{tmp.name}\\contact-native.png' --json"
   rc,nout,nerr=run(['powershell.exe','-NoProfile','-Command',ps]); native=out/'contact-native.png'
   if rc or not native_win.is_file():
    detail=(nout+' '+nerr).strip().replace('\n',' ')[:500]
    failures.append('native Microsoft PowerPoint render failed'+(f': {detail}' if detail else ''))
   else: shutil.copy2(native_win,native)
 status='passed' if not failures else ('blocked' if a.required else 'partial')
 summary=['# OfficeCLI QA summary','',f'- Status: {status}',f'- Deck: `{deck.name}`',f'- SHA-256: `{sha(deck)}`',f'- OfficeCLI: `{version}`',f'- Slides: {slides}',f'- OpenXML validation: {"passed" if "OpenXML validation failed" not in failures else "failed"}',f'- OfficeCLI issues: {count}',f'- HTML contact sheet: {html.name if html.is_file() else "failed"}',f'- Native PowerPoint contact sheet: {native.name if native and native.is_file() else "not produced"}','', '## Required human review','', '- Inspect every slide in the contact sheets.','- Record clipping, hierarchy, missing content, evidence encoding, and render differences.','- Do not promote solely from this automated result.']
 if failures: summary += ['','## Failures','']+[f'- {x}' for x in failures]
 (out/'qa-summary.md').write_text('\n'.join(summary)+'\n'); print('\n'.join(summary)); return 0 if status=='passed' else 2
if __name__=='__main__': sys.exit(main())
