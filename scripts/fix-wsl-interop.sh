#!/usr/bin/env bash
# Restore WSL Windows-interop (running .exe from WSL) and make it survive reboots.
#
# Symptom this fixes:
#   /mnt/c/.../soffice.exe: cannot execute binary file: Exec format error
#   ...or the .exe being parsed as a shell script ("MZ...: not found")
#
# Cause: binfmt_misc is mounted and enabled, but the `WSLInterop` handler is not
# registered. This happens in systemd mode (`systemd=true` in /etc/wsl.conf)
# when the unit that registers it does not run. It is NOT caused by
# `[interop] enabled=false` — check that separately if this script does not help.
#
# Why it matters here: the PPTX delivery gate in CLAUDE.md requires rendering a
# deck to contact sheets for visual QA. Without interop there is no renderer on
# this host (matplotlib is absent too), so decks can never leave `draft`.
#
# Run:  sudo bash scripts/fix-wsl-interop.sh
set -euo pipefail

REG=/proc/sys/fs/binfmt_misc/register
UNIT=/etc/systemd/system/wsl-binfmt.service
LINE=':WSLInterop:M::MZ::/init:PF'

if [[ $EUID -ne 0 ]]; then
  echo "error: must run as root — try: sudo bash $0" >&2
  exit 1
fi

if [[ ! -e /proc/sys/fs/binfmt_misc/status ]]; then
  echo "binfmt_misc not mounted; mounting..."
  mount -t binfmt_misc binfmt_misc /proc/sys/fs/binfmt_misc
fi

if [[ -e /proc/sys/fs/binfmt_misc/WSLInterop ]]; then
  echo "WSLInterop already registered — nothing to do."
else
  echo "Registering WSLInterop handler..."
  echo "$LINE" > "$REG"
  echo "  done."
fi

# Persist across reboots. WSL re-creates binfmt_misc on boot, so the handler
# must be re-registered each time; a systemd unit is the durable way to do it.
echo "Installing $UNIT for persistence..."
cat > "$UNIT" <<'EOF'
[Unit]
Description=Register WSL Windows interop binfmt handler
After=local-fs.target
ConditionPathExists=/init
ConditionPathExists=!/proc/sys/fs/binfmt_misc/WSLInterop

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/sh -c 'echo ":WSLInterop:M::MZ::/init:PF" > /proc/sys/fs/binfmt_misc/register'

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable wsl-binfmt.service >/dev/null 2>&1 || true
echo "  enabled."

echo
echo "Verifying..."
if /mnt/c/Windows/System32/cmd.exe /c "echo interop-ok" 2>/dev/null | grep -q interop-ok; then
  echo "  PASS — Windows executables now run from WSL."
else
  echo "  FAIL — still cannot run .exe. Check for '[interop] enabled=false' or"
  echo "         'appendWindowsPath=false' in /etc/wsl.conf, then run:"
  echo "         wsl.exe --shutdown   (from Windows) and reopen the shell."
  exit 1
fi
