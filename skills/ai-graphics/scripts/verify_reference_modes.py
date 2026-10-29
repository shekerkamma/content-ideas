#!/usr/bin/env python3
"""Paired verification for codex_image_edit.py's reference modes.

Runs two arms per mode — WITH the reference and a no-reference CONTROL on the
identical spec — because a single passing render cannot distinguish "the model
honored the attached reference" from "the model read my prompt back to me".
The control is the whole measurement.

  python3 verify_reference_modes.py --mode edit --out-dir runs/imgverify
  python3 verify_reference_modes.py --mode style --wait-until 14:25

Designing the spec is the part that decides whether this proves anything: the
prompt must NOT enumerate the things only the reference knows. In the shipped
fixtures the box labels are named (so the control can draw a diagram at all) but
the model captions and connector labels are not — those strings exist only
inside the reference image, so their presence in the with-ref arm and absence in
the control is the evidence. Weaken that asymmetry and the test goes green
without measuring anything.

Quota: the ChatGPT plan cap stops image renders for hours at a time. --wait-until
holds for a reset rather than burning retries against a wall.
"""
import argparse
import datetime as dt
import subprocess
import sys
import time
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
QUOTA = "hit your usage limit"

# mode -> (reference asset, spec fixture)
ARMS = {
    "edit": ("ref-editorial-diagram.png", "spec-edit.txt"),
    "style": ("ref-dense-infographic.png", "spec-style.txt"),
    "variation": ("ref-editorial-diagram.png", "spec-variation.txt"),
}


def _hold(until: str) -> None:
    h, m = (int(x) for x in until.split(":"))
    now = dt.datetime.now(dt.timezone.utc)
    target = now.replace(hour=h, minute=m, second=0, microsecond=0)
    if target <= now:
        target += dt.timedelta(days=1)
    wait = (target - now).total_seconds()
    print(f"holding {wait / 60:.0f} min until {until} UTC for the quota reset…")
    time.sleep(wait)


def _run(label: str, cmd: list[str], out: Path, attempts: int, log_dir: Path) -> bool:
    log = log_dir / f"{label}.log"
    for i in range(1, attempts + 1):
        proc = subprocess.run(cmd, capture_output=True, text=True)
        log.write_text((proc.stdout or "") + (proc.stderr or ""))
        if out.exists() and out.stat().st_size > 0:
            print(f"  {label}: OK on attempt {i}")
            return True
        if QUOTA in log.read_text():
            print(f"  {label}: quota-blocked, retrying in 5 min (attempt {i}/{attempts})")
            time.sleep(300)
            continue
        print(f"  {label}: FAILED — {log.read_text()[-300:]}", file=sys.stderr)
        return False
    print(f"  {label}: gave up, still quota-blocked", file=sys.stderr)
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=sorted(ARMS), required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--wait-until", default=None, metavar="HH:MM",
                    help="UTC time to hold for before starting (quota reset)")
    ap.add_argument("--attempts", type=int, default=24)
    ap.add_argument("--model", default=None, help="pin the mainline host")
    a = ap.parse_args()

    ref_name, spec_name = ARMS[a.mode]
    ref = SKILL / "assets" / ref_name
    spec = SKILL / "tests" / "fixtures" / spec_name
    for f in (ref, spec):
        if not f.is_file():
            print(f"BLOCKED: missing {f}", file=sys.stderr)
            return 2

    out_dir = Path(a.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    if a.wait_until:
        _hold(a.wait_until)

    pin = ["--model", a.model] if a.model else []
    with_ref = out_dir / f"{a.mode}-with-ref.png"
    control = out_dir / f"{a.mode}-control.png"

    print(f"mode={a.mode}  reference={ref_name}  spec={spec_name}")
    ok_a = _run(f"{a.mode}-with-ref", [
        sys.executable, str(SKILL / "scripts" / "codex_image_edit.py"),
        "--mode", a.mode, "--ref", str(ref), "--prompt-file", str(spec),
        "--out", str(with_ref), *pin], with_ref, a.attempts, out_dir)
    ok_b = _run(f"{a.mode}-control", [
        sys.executable, str(SKILL / "scripts" / "codex_image.py"),
        "--prompt-file", str(spec), "--out", str(control), *pin],
        control, a.attempts, out_dir)

    if a.mode == "style" and ok_a and ok_b:
        print("\npalette distance to the style reference (with-ref must be LOWER):")
        subprocess.run([sys.executable, str(SKILL / "scripts" / "palette_distance.py"),
                        str(ref), str(with_ref), str(control)])

    print(f"\nartifacts in {out_dir}. Read BOTH images: the metric supports the "
          f"judgement, it does not replace it.")
    return 0 if (ok_a and ok_b) else 1


if __name__ == "__main__":
    sys.exit(main())
