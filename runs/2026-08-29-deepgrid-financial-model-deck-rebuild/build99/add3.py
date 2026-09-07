"""Add three narrated simulator slides to the embedded 99-slide deck.

Uses the deck's own video-interstitial pattern (slides 26 and 38): three text
shapes plus a full-bleed picture at (192,148) 896x504, and crucially **no footer
and no page number** -- so inserting them renumbers nothing.

Placement follows the deck's existing narrative, not convenience:
  after 24 "Eleven inputs, one compute product"       -> computebox
  after 34 "Compute waits when data queues"           -> problem
  after 36 "Data placement is an architectural choice"-> landscape
"""
import re, zipfile
from pathlib import Path

R = Path('/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild')
SRC = R / 'build99/DeepGrid-Semi-Product-Portfolio-99-Slides-Embedded-draft.pptx'
OUT = R / 'build99/DeepGrid-Semi-Product-Portfolio-102-Slides-Embedded-draft.pptx'
SLIDE_CT = 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'
VIDEO_T = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/video'
MEDIA_T = 'http://schemas.microsoft.com/office/2007/relationships/media'
IMAGE_T = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'
LAYOUT_T = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout'

TPL_TITLE = 'See the flat-to-cube compute comparison'
TPL_DISC  = 'Illustrative arithmetic demonstration—not a measured application speedup.'
TPL_CAP   = 'Click the video to play · Holt narration · No music'

NEW = [
 # (after this original slide, part idx, clip path, title, disclaimer)
 (24, 201, 'media/narrated-v2/computebox.mp4',
  'See eleven inputs become one AD2 output',
  'Illustrative sensor-fusion timing—not a measured production latency.'),
 (34, 202, 'media/narrated-new/problem.mp4',
  'See what a shared data engine costs',
  'Illustrative dispatch comparison—not a measured application speedup.'),
 (36, 203, 'media/narrated-v3/landscape.mp4',
  'See where DGrid sits on the memory spectrum',
  'Illustrative architecture comparison—vendor figures from public sources.'),
]
CAP = 'Click the video to play · Narrated · No music'

z = zipfile.ZipFile(SRC)
parts = {n: z.read(n) for n in z.namelist()}
z.close()
tpl = parts['ppt/slides/slide38.xml'].decode('utf8')

pres = parts['ppt/presentation.xml'].decode('utf8')
lst = re.search(r'<p:sldIdLst>(.*?)</p:sldIdLst>', pres, re.S).group(1)
entries = re.findall(r'<p:sldId[^>]*?id="(\d+)"[^>]*?r:id="([^"]+)"[^>]*/>', lst)
assert len(entries) == 99, len(entries)
rels = parts['ppt/_rels/presentation.xml.rels'].decode('utf8')
def target(rid):
    m = re.search(r'<Relationship Id="%s"[^>]*Target="([^"]+)"' % re.escape(rid), rels)
    return m.group(1)
order = [(i, r, int(re.search(r'slide(\d+)\.xml', target(r)).group(1))) for i, r in entries]

nxt_id = max(int(i) for i, _ in entries) + 1
insert_after = {}
for k, (after, idx, clip, title, disc) in enumerate(NEW):
    media_part = f'media/mediadata{7+k}.mp4'
    img_part = f'ppt/media/image{100+k}.png'
    parts[media_part] = (R / clip).read_bytes()
    parts[img_part] = (R / f'build99/poster-{Path(clip).stem}.png').read_bytes()

    x = tpl
    for old, new in ((TPL_TITLE, title), (TPL_DISC, disc), (TPL_CAP, CAP)):
        assert f'<a:t>{old}</a:t>' in x, old[:40]
        x = x.replace(f'<a:t>{old}</a:t>', f'<a:t>{new}</a:t>')
    # hyperlink pic -> embedded video pic
    x = x.replace('<a:hlinkClick r:id="rId3"/>', '<a:hlinkClick r:id="" action="ppaction://media"/>')
    x = x.replace('<p:nvPr/></p:nvPicPr>',
        '<p:nvPr><a:videoFile xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:link="rId3"/>'
        '<p:extLst><p:ext uri="{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230}">'
        '<p14:media xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId5"/>'
        '</p:ext></p:extLst></p:nvPr></p:nvPicPr>', 1)
    parts[f'ppt/slides/slide{idx}.xml'] = x.encode('utf8')
    parts[f'ppt/slides/_rels/slide{idx}.xml.rels'] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'<Relationship Id="rId1" Type="{LAYOUT_T}" Target="../slideLayouts/slideLayout1.xml"/>'
        f'<Relationship Id="rId3" Type="{VIDEO_T}" Target="/{media_part}"/>'
        f'<Relationship Id="rId5" Type="{MEDIA_T}" Target="/{media_part}"/>'
        f'<Relationship Id="rId4" Type="{IMAGE_T}" Target="/{img_part}"/>'
        '</Relationships>').encode('utf8')
    rid = f'rIdNew{idx}'
    rels = rels.replace('</Relationships>',
        f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"'
        f' Target="slides/slide{idx}.xml"/></Relationships>')
    insert_after[after] = (str(nxt_id + k), rid)
    print(f'  after slide {after:>3}: "{title}"  <- {Path(clip).name}')

seq = []
for i, r, orig in order:
    seq.append((i, r))
    if orig in insert_after:
        seq.append(insert_after[orig])
assert len(seq) == 102, len(seq)
NS = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
parts['ppt/presentation.xml'] = pres.replace(lst,
    ''.join(f'<p:sldId {NS} id="{i}" r:id="{r}"/>' for i, r in seq)).encode('utf8')
parts['ppt/_rels/presentation.xml.rels'] = rels.encode('utf8')

ct = parts['[Content_Types].xml'].decode('utf8')
ct = ct.replace('</Types>', ''.join(
    f'<Override PartName="/ppt/slides/slide{idx}.xml" ContentType="{SLIDE_CT}"/>'
    for _, idx, _, _, _ in NEW) + '</Types>')
parts['[Content_Types].xml'] = ct.encode('utf8')

zo = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
for k, v in parts.items(): zo.writestr(k, v)
zo.close()
print(f'\nwritten: {OUT.name}  {OUT.stat().st_size:,} bytes  ({len(seq)} slides)')
