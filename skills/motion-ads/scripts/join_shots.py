#!/usr/bin/env python3
"""Join generated shots into one continuous camera move.

Each shot was generated from a first frame and a last frame, so shot N ends on the exact picture
shot N+1 starts on. But video models ease in at the start of every clip and slow down at the end,
so a plain join looks like the camera stops dead at each keyframe. This script re-times every clip
so the speed carries across each join:

  1. measure how much the picture changes on every frame of every clip (a stand-in for camera speed),
  2. choose which source frames to keep so the on-screen speed follows one smooth curve
     (fast, then slower, never zero), skipping frames where the model dawdles, never repeating one,
  3. drop the first frame of each following clip (it is the same picture as the frame before it),
  4. write all kept frames as one video, re-encoded (a stream-copy join wrote broken timestamps).

Plan file (JSON), paths relative to the plan:
{
  "fps": 24, "size": [1920, 1080],
  "shots": [
    {"file": "shots/s1.mp4", "frames": 72},
    {"file": "shots/s2.mp4", "frames": 72, "bump": 0.5, "tail": 3, "marks": {"click": 59}},
    {"file": "shots/s3.mp4", "frames": 78, "end": 0.1}
  ]
}
  frames  how many frames this shot gets in the film (72 at 24 fps = 3 s)
  bump    how strong the early swell of speed is (default 1.0; 0 = even speed)
  tail    skip this many of the model's dead-still final frames (default 0)
  start   below 1 eases in from a slow previous shot (default 1.0)
  end     below 1 lets the last shot settle to that fraction of speed (default 1.0)
  marks   named source frames (the frame where the button goes in), reported as film times

Writes next to the output: <out>.events.json (shot starts, marks and "end", in seconds, for the sound)
and <out>.report.json (the difference across each join and the speed either side of it).

Needs: numpy, ffmpeg, ffprobe.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("plan", help="the plan file (JSON)")
    p.add_argument("out", help="the joined video, e.g. picture.mov (.mov = ProRes master, .mp4 = H.264)")
    p.add_argument("--max-step", type=float, default=7.0, help="never skip more than this many source frames at once (default 7)")
    a = p.parse_args()

    import numpy as np

    plan = json.load(open(a.plan))
    fps = plan["fps"]
    W, H = plan["size"]
    base = os.path.dirname(os.path.abspath(a.plan))
    work = tempfile.mkdtemp(prefix="join_")

    def frame_count(path):
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                              "stream=nb_read_frames", "-of", "csv=p=0", path], capture_output=True, text=True, check=True).stdout
        return int(out.strip().split(",")[0])

    def thumbnails(path, n):
        w, h = 192, 108
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                             capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.uint8).reshape(-1, h, w)[:n].astype(np.float32)

    def motion(frames):
        change = np.abs(frames[1:] - frames[:-1]).mean(axis=(1, 2))
        kernel = np.array([1, 2, 3, 2, 1], np.float32)
        kernel /= kernel.sum()
        return np.maximum(np.convolve(np.pad(change, 2, mode="edge"), kernel, "valid"), 0.15)

    def wanted_speed(u, bump, end, start):
        # 1 at both joins, an early swell in between, an optional settle at the very end
        swell = 1.0 + bump * (u ** 0.8) * ((1 - u) ** 2.2) / 0.118
        settle = 1.0 - (1.0 - end) * u ** 2.5
        ramp = min(1.0, u / 0.3)
        ease = start + (1.0 - start) * ramp * ramp * (3 - 2 * ramp)
        return swell * settle * ease

    def choose(change, count, first, shot):
        last = len(change) - shot.get("tail", 0)
        bump, end, start = shot.get("bump", 1.0), shot.get("end", 1.0), shot.get("start", 1.0)

        def walk(scale):
            pos, picked = float(first), [first]
            for j in range(1, count):
                i = min(int(pos), last - 1)
                step = min(a.max_step, max(1.0, scale * wanted_speed(j / (count - 1), bump, end, start) / change[i]))
                pos += step
                picked.append(min(last, max(picked[-1] + 1, int(round(pos)))))
            return picked, pos

        lo, hi = 0.01, 400.0
        for _ in range(60):                                     # find the scale that lands exactly on the last frame
            mid = (lo + hi) / 2
            if walk(mid)[1] < last:
                lo = mid
            else:
                hi = mid
        picked = walk(hi)[0]
        picked[-1] = last
        for j in range(len(picked) - 2, -1, -1):
            if picked[j] >= picked[j + 1]:
                picked[j] = picked[j + 1] - 1
        if picked[0] < 0:
            sys.exit(f"{shot['file']}: asked for {count} frames but the clip is too short. Lower 'frames' or 'tail'.")
        return picked

    parts, report, events, previous_last, at = [], [], [], None, 0
    for k, shot in enumerate(plan["shots"]):
        src = os.path.join(base, shot["file"])
        n = frame_count(src)
        thumbs = thumbnails(src, n)
        change = motion(thumbs)
        keep = choose(change, shot["frames"], 0 if k == 0 else 1, shot)
        on_screen = [float(change[min(i, len(change) - 1)] * (keep[j + 1] - i)) for j, i in enumerate(keep[:-1])]
        report.append({
            "shot": k + 1, "file": shot["file"], "source_frames": n, "kept": len(keep),
            "join_difference": None if previous_last is None else round(float(np.abs(thumbs[0] - previous_last).mean()), 2),
            "speed_at_start": round(float(np.mean(on_screen[:3])), 2), "speed_at_end": round(float(np.mean(on_screen[-3:])), 2),
        })
        previous_last = thumbs[n - 1]
        events.append({"name": f"shot{k + 1}.start", "t": round(at / fps, 4)})
        for name, source_frame in shot.get("marks", {}).items():
            j = next((j for j, i in enumerate(keep) if i >= source_frame), len(keep) - 1)
            events.append({"name": name, "t": round((at + j) / fps, 4)})
        at += len(keep)

        runs, run_start = [], keep[0]
        for x, y in zip(keep, keep[1:] + [None]):
            if y != x + 1:
                runs.append((run_start, x))
                run_start = y
        select = "+".join(f"eq(n\\,{s})" if s == e else f"between(n\\,{s}\\,{e})" for s, e in runs)
        part = os.path.join(work, f"part{k + 1}.mov")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf",
                        f"select='{select}',setpts=N/{fps}/TB,scale={W}:{H}:flags=lanczos,setsar=1", "-r", str(fps), "-an",
                        "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", part], check=True)
        parts.append(part)

    cmd = ["ffmpeg", "-v", "error", "-y"]
    for part in parts:
        cmd += ["-i", part]
    graph = "".join(f"[{i}:v]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0,setpts=N/{fps}/TB[v]"
    codec = (["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le"] if a.out.lower().endswith(".mov")
             else ["-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"])
    subprocess.run(cmd + ["-filter_complex", graph, "-map", "[v]", "-r", str(fps)] + codec + [a.out], check=True)

    events.append({"name": "end", "t": round(at / fps, 4)})
    stem = os.path.splitext(a.out)[0]
    json.dump(events, open(stem + ".events.json", "w"), indent=1)
    json.dump(report, open(stem + ".report.json", "w"), indent=1)
    for r in report:
        print(r)
        if r["join_difference"] is not None and r["join_difference"] > 6:
            print(f"  CHECK: shot {r['shot']} does not start on the picture the last shot ended on. Was it made from the same keyframe?")
    print(f"{at} frames = {at / fps:.3f} s -> {a.out}")
    print(f"beats -> {stem}.events.json")


if __name__ == "__main__":
    main()
