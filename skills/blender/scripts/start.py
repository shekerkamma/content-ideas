#!/usr/bin/env python3
import argparse,json,os,socket,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--log',default='runs/blender/blender.log');p.add_argument('--doctor',action='store_true');args=p.parse_args()
s=socket.socket();s.settimeout(2);running=s.connect_ex(('127.0.0.1',9876))==0;s.close()
if args.doctor or running:
 print(json.dumps({'bridgeListening':running,'blenderExecutable':Path('/usr/bin/blender').exists()}))
 raise SystemExit(0 if running else 1)
log=Path(args.log);log.parent.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['DISABLE_TELEMETRY']='true'
with log.open('a') as out:
 process=subprocess.Popen(['/usr/bin/blender','--python',str(Path(__file__).with_name('enable_bridge.py'))],stdout=out,stderr=out,env=env,start_new_session=True)
print(json.dumps({'startedPid':process.pid,'log':str(log),'state':'starting'}))
