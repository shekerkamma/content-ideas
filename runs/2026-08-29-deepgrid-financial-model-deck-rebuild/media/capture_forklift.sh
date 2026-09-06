set -e
R=/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild
cd $R/media
export PATH="$HOME/.nvm/versions/node/v24.18.1/bin:$PATH"
export DISPLAY=:0 PULSE_SERVER=unix:/mnt/wslg/PulseServer
rm -f forklift-av.mkv
# Start the driver first so the window exists, then grab it. One ffmpeg process
# takes BOTH streams, so audio and video share a clock and cannot drift.
node drive_forklift.mjs "$R/refs/forklift-sim.html" > drive.log 2>&1 &
NODE=$!
sleep 6
ffmpeg -hide_banner -loglevel error -y \
  -f x11grab -framerate 30 -video_size 1600x900 -i :0.0+6,27 \
  -f pulse -i RDPSink.monitor \
  -t 68 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 128k forklift-av.mkv
wait $NODE 2>/dev/null || true
echo CAPTURE_DONE
