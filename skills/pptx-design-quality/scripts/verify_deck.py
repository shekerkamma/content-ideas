#!/usr/bin/env python3
"""Deck verification: canvas bounds, text collisions, and background-aware WCAG contrast.

Complements lint_pptx.py rather than replacing it. Three checks it adds:
  1. OOB      - any shape extending past the 1280x720 canvas.
  2. OVERLAP  - text-vs-text, and text sitting on top of an opaque fill band
                (the case lint's text-box rule misses, because a table header
                or card body is an empty rect and carries no text of its own).
  3. CONTRAST - resolves each glyph's ACTUAL background by hit-testing the fill
                rects behind it, then applies the WCAG large-text threshold
                (3:1 at >=24pt, or >=18.66pt bold) instead of a flat 4.5:1.
Exit 0 clean, 2 findings.
"""
import re, sys, zipfile
from xml.etree import ElementTree as ET

P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
E=914400/96.0; W,H=1280,720
# Dark-background slides, for contrast resolution. Override per deck:
#   DECK_DARK_SLIDES=1,6,12 python verify_deck.py <deck>.pptx
import os as _os
DARK={int(x) for x in _os.environ.get('DECK_DARK_SLIDES','').split(',') if x.strip().isdigit()}

def lum(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda v: v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    r,g,b=[f(v) for v in c]; return 0.2126*r+0.7152*g+0.0722*b
def ratio(a,b):
    la,lb=lum(a),lum(b); return (max(la,lb)+0.05)/(min(la,lb)+0.05)

def run(path):
    z=zipfile.ZipFile(path)
    slides=sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',n)],
                  key=lambda n:int(re.search(r'(\d+)',n.split('/')[-1]).group(1)))
    findings=[]
    for i,n in enumerate(slides,1):
        root=ET.fromstring(z.read(n)); page='#0A1628' if i in DARK else '#FFFFFF'
        texts=[]; fills=[]
        for order, sp in enumerate(root.iter(f'{{{P}}}sp')):
            xf=sp.find(f'.//{{{A}}}xfrm')
            if xf is None: continue
            o=xf.find(f'{{{A}}}off'); e=xf.find(f'{{{A}}}ext')
            if o is None or e is None: continue
            x,y=int(o.get('x'))/E,int(o.get('y'))/E
            w,h=int(e.get('cx'))/E,int(e.get('cy'))/E
            t="".join(tt.text or "" for tt in sp.iter(f'{{{A}}}t')).strip()
            if x<-0.5 or y<-0.5 or x+w>W+0.5 or y+h>H+0.5:
                findings.append(f"s{i} OOB   ({x:.0f},{y:.0f}) {w:.0f}x{h:.0f} bottom={y+h:.0f} :: {t[:40]!r}")
            if t:
                d=sp.find(f'.//{{{A}}}defRPr'); col=None; sz=13.0; bold=False
                if d is not None:
                    sc=d.find(f'.//{{{A}}}srgbClr')
                    if sc is not None: col='#'+sc.get('val')
                    sz=int(d.get('sz','1300'))/100; bold=d.get('b')=='1'
                texts.append((x,y,w,h,t,col,sz,bold,order))
            else:
                # Any drawn shape carrying no text is an occluder. Do NOT gate this on
                # finding a solidFill: an earlier version looked for
                # spPr/solidFill/srgbClr, matched nothing, and reported zero occluders
                # on a deck where OfficeCLI found fifteen.
                sf = sp.find(f'.//{{{A}}}solidFill/{{{A}}}srgbClr')
                col = '#' + sf.get('val') if sf is not None else '#FFFFFF'
                if w > 8 and h > 8:
                    fills.append((x, y, w, h, col, order))
        # text vs text
        for a_ in range(len(texts)):
            for b_ in range(a_+1,len(texts)):
                x1,y1,w1,h1,t1,*_=texts[a_]; x2,y2,w2,h2,t2,*_=texts[b_]
                ix=min(x1+w1,x2+w2)-max(x1,x2); iy=min(y1+h1,y2+h2)-max(y1,y2)
                if ix>4 and iy>4 and min(w1*h1,w2*h2)>0 and (ix*iy)/min(w1*h1,w2*h2)>0.30:
                    findings.append(f"s{i} OVL   {t1[:32]!r} <> {t2[:32]!r}")
        # text hidden behind a LATER opaque shape (OfficeCLI's O-class)
        for x,y,w,h,t,col,sz,bold,o1 in texts:
            for fx,fy,fw,fh,fc,fo in fills:
                if fo <= o1: continue
                ix=min(x+w,fx+fw)-max(x,fx); iy=min(y+h,fy+fh)-max(y,fy)
                if ix>2 and iy>2 and (ix*iy)/(w*h) > 0.25:
                    findings.append(f"s{i} OCCL  {t[:34]!r} under shape at ({fx:.0f},{fy:.0f}) {fw:.0f}x{fh:.0f}")
                    break

        # contrast against resolved background
        for x,y,w,h,t,col,sz,bold,_o in texts:
            if not col: continue
            cx,cy=x+w/2,y+h/2; bg=page
            for fx,fy,fw,fh,fc,_fo in fills:
                if fx-1<=cx<=fx+fw+1 and fy-1<=cy<=fy+fh+1: bg=fc
            need=3.0 if (sz>=24 or (sz>=18.66 and bold)) else 4.5
            r=ratio(col,bg)
            if r<need:
                findings.append(f"s{i} CONTR {col} on {bg} {r:.2f}:1 (need {need}) {sz}pt :: {t[:32]!r}")
    return findings, len(slides)

if __name__=='__main__':
    f,n=run(sys.argv[1])
    print(f"slides scanned: {n}")
    for x in f: print("  "+x)
    print(f"\n{'PASS - no findings' if not f else f'{len(f)} FINDING(S)'}")
    sys.exit(0 if not f else 2)
