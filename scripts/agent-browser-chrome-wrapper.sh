#!/bin/bash

set -euo pipefail

export LD_LIBRARY_PATH="/home/shekerk/content-ideas/.browser-libs:/snap/bruno/113/usr/lib/x86_64-linux-gnu:/snap/gnome-3-28-1804/198/usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

exec /home/shekerk/snap/codex/64/.agent-browser/browsers/chrome-149.0.7827.115/chrome "$@"
