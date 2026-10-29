"""Replace the 99-slide deck's six external Drive hyperlinks with EMBEDDED video.

Google Slides cannot embed video -- Insert > Video only links to YouTube/Drive --
so the exported deck carries clickable poster images with TargetMode="External"
and zero mp4 parts. A viewer must be online, signed in, and click out to Drive.
Native PPTX can embed, so the video bytes go into the package and each poster
becomes the video's own poster frame.

Per-slide surgery:
  <a:hlinkClick r:id=rIdN/>              -> <a:hlinkClick r:id="" action="ppaction://media"/>
  <p:nvPr/>                              -> <p:nvPr><a:videoFile r:link/><p14:media r:embed/></p:nvPr>
  blipFill                                  unchanged -- the existing poster is kept
  rels: hyperlink(External) -> video + ms-media, both to /media/mediadataN.mp4
"""
import re, shutil, zipfile
from pathlib import Path

R = Path('/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild')
SRC = R / 'inspect99/deck99.pptx'
OUT = R / 'build99/DeepGrid-Semi-Product-Portfolio-99-Slides-Embedded-draft.pptx'
CLIPS = R / 'inspect99/clips'

# slide -> clip file.  Mapping read off each slide's own copy, not assumed.
MAP = {17: 'slide17-indoor-amr.mp4', 23: 'slide23-truck-adas.mp4',
       26: 'slide26-truck-sensor.mp4', 38: 'slide38-flat-to-cube.mp4',
       69: 'slide69-seaport-yard.mp4', 88: 'slide88-sentinel.mp4'}

VIDEO_T = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/video'
MEDIA_T = 'http://schemas.microsoft.com/office/2007/relationships/media'
RNS = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
P14 = 'xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main"'

z = zipfile.ZipFile(SRC)
parts = {n: z.read(n) for n in z.namelist()}
z.close()

for i, (slide, clip) in enumerate(sorted(MAP.items()), start=1):
    media_part = f'media/mediadata{"" if i == 1 else i}.mp4'
    parts[media_part] = (CLIPS / clip).read_bytes()

    skey = f'ppt/slides/slide{slide}.xml'
    rkey = f'ppt/slides/_rels/slide{slide}.xml.rels'
    x = parts[skey].decode('utf8')
    rels = parts[rkey].decode('utf8')

    # which rId is the external hyperlink on this slide?
    m = re.search(r'<Relationship Id="([^"]+)" Type="[^"]*hyperlink"[^>]*TargetMode="External"\s*/>', rels)
    assert m, f'slide {slide}: no external hyperlink rel'
    hl = m.group(1)
    vid_rid, med_rid = hl, f'rIdMedia{slide}'

    # 1. hyperlink -> media action
    old_link = f'<a:hlinkClick r:id="{hl}"/>'
    assert old_link in x, f'slide {slide}: hlinkClick {hl} not found'
    x = x.replace(old_link, '<a:hlinkClick r:id="" action="ppaction://media"/>')

    # 2. empty nvPr -> videoFile + p14:media
    nvpr = (f'<p:nvPr><a:videoFile {RNS} r:link="{vid_rid}"/>'
            f'<p:extLst><p:ext uri="{{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230}}">'
            f'<p14:media {P14} {RNS} r:embed="{med_rid}"/></p:ext></p:extLst></p:nvPr>')
    # only the video pic has an empty <p:nvPr/> right after cNvPicPr
    assert x.count('<p:nvPr/></p:nvPicPr>') >= 1, f'slide {slide}: no empty nvPr on a pic'
    x = x.replace('<p:nvPr/></p:nvPicPr>', nvpr + '</p:nvPicPr>', 1)
    parts[skey] = x.encode('utf8')

    # 3. rels: hyperlink -> video, plus the ms-media rel
    rels = re.sub(r'<Relationship Id="%s" Type="[^"]*hyperlink"[^>]*/>' % re.escape(hl),
                  f'<Relationship Id="{vid_rid}" Type="{VIDEO_T}" Target="/{media_part}"/>'
                  f'<Relationship Id="{med_rid}" Type="{MEDIA_T}" Target="/{media_part}"/>',
                  rels)
    parts[rkey] = rels.encode('utf8')
    print(f'  slide {slide:>3} <- {clip:<28} as /{media_part}')

# mp4 must have a content-type; Google's export has no mp4 Default
ct = parts['[Content_Types].xml'].decode('utf8')
if 'Extension="mp4"' not in ct:
    ct = ct.replace('<Types ', '<Types ', 1)
    ct = re.sub(r'(<Types[^>]*>)', r'\1<Default Extension="mp4" ContentType="video/mp4"/>', ct, count=1)
    print('  added <Default Extension="mp4">')
parts['[Content_Types].xml'] = ct.encode('utf8')

zo = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
for k, v in parts.items():
    zo.writestr(k, v)
zo.close()
print(f'\nwritten: {OUT.name}  {OUT.stat().st_size:,} bytes')
