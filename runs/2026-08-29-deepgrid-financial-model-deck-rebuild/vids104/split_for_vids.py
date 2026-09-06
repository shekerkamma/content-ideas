"""Split the 104-slide embedded deck into three Vids-sized parts.

Vids caps a Slides import at 45 slides, so 104 needs three. Boundaries are the
deck's own section dividers (PART TWO at 31, PART THREE at 63) so each part
opens on context rather than mid-SKU:  1-30 | 31-62 | 63-104.

Video is stripped from these copies: Vids flattens an embedded clip to its
poster frame on import, so the mp4 bytes are dead weight for the upload and the
render is identical. Each video <p:pic> is reverted to a plain picture (its
poster) and the video/media rels are dropped. Uploads go 59 MB -> ~3.6 MB.
The live clips are composited back into the exported MP4 afterwards.
"""
