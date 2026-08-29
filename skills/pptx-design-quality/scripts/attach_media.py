#!/usr/bin/env python3
"""Drop captured clips into the seats a deck build reserved for them.

The builder writes `<deck>-video-seats.json` naming, per slide, the exact rect
it left empty behind a frame. This reads that file rather than guessing where a
video should sit, so the clip lands inside its frame instead of near it.

officecli only persists writes to Windows-side paths, so both the deck and the
media must be staged under C:\\ before this runs; the caller does the staging
and passes Windows paths.
"""
from __future__ import annotations
import json, sys

PX_TO_IN = 13.333 / 1280      # the 1280px stage on a 13.333in slide


def build(seats_json: str, media_dir_win: str, out_path: str,
          poster: bool = True) -> int:
    seats = json.load(open(seats_json))['seats']
    cmds = []
    for st in seats:
        props = {
            "src": f"{media_dir_win}\\{st['video']}.mp4",
            "x": f"{st['x'] * PX_TO_IN:.3f}in",
            "y": f"{st['y'] * PX_TO_IN:.3f}in",
            "width": f"{st['w'] * PX_TO_IN:.3f}in",
            "height": f"{st['h'] * PX_TO_IN:.3f}in",
            # Not autoPlay: an investor scrubbing a deck should start it, and a
            # clip that fires on slide entry fights the build animation.
            "autoPlay": "false",
            "loop": "false",
            "volume": "0",
        }
        if poster:
            props["poster"] = f"{media_dir_win}\\{st['video']}-poster.png"
        cmds.append({"command": "add", "parent": f"/slide[{st['slide']}]",
                     "type": "media", "props": props})
    json.dump(cmds, open(out_path, 'w'))
    return len(cmds)


if __name__ == '__main__':
    print(build(sys.argv[1], sys.argv[2], sys.argv[3]), 'media commands')
