#!/usr/bin/env bash
# Install scripts/cliproxy_forward.py as the systemd user service cliproxy-forward.service,
# so WSL 127.0.0.1:8317 reaches CLIProxyAPI on Windows. Idempotent.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
UNIT="$HOME/.config/systemd/user/cliproxy-forward.service"
mkdir -p "$(dirname "$UNIT")"
cat > "$UNIT" <<EOF
[Unit]
Description=Forward WSL 127.0.0.1:8317 to CLIProxyAPI on Windows (gateway re-resolved per connection)
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $REPO/scripts/cliproxy_forward.py
Restart=on-failure
RestartSec=3

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now cliproxy-forward.service
systemctl --user restart cliproxy-forward.service
sleep 1
systemctl --user is-active cliproxy-forward.service
