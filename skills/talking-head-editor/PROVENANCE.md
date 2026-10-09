# Provenance

Vendored verbatim from [griffinwooldridge/talking-head-editor](https://github.com/griffinwooldridge/talking-head-editor)
at commit `0a73a3e` (2026-10-08), MIT (see `LICENSE`, copyright Griffin Wooldridge; fonts under OFL). Source video:
"Opus 5.5 Is the First AI That Can Actually Edit Video", youtube.com/watch?v=Tac-a8XdAJY (2026-10-09).

Do not edit the skill body here; to update, re-copy the upstream tree (without `.git`) and bump the commit above.

## Installing on this machine (WSL, 2026-10-09)

`scripts/setup.sh` as written fails here twice. Run it like this instead:

```bash
cd skills/talking-head-editor
uv venv --seed --python 3.11 .venv                 # system python3 has no ensurepip, so `python3 -m venv` fails
.venv/bin/pip install "numpy<2" torch==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cpu
PYTHON=$PWD/.venv/bin/python scripts/setup.sh      # skips the existing venv; torch==2.5.1 is already satisfied
```

- **Python 3.11, not 3.12:** `deepfilterlib` publishes Linux wheels only up to cp311; on 3.12 pip tries a Rust build
  and fails with "Cargo ... is not installed".
- **CPU torch:** the default torch 2.5.1 wheel pulls about 2.5 GB of CUDA libraries for a 4 GB GTX 1050 Ti. Whisper here
  runs with `fp16=False`, so the CPU build is the same work.
- `.venv/` (about 2.2 GB) and `mg/vendor/gsap.min.js` are gitignored by the skill's own `.gitignore`.
- Measured on a 40 s 1080p clip: voice 1m45s, transcribe about 1 min after a one-time 461 MB whisper `small.en`
  download, reframed cut render 1m43s.
