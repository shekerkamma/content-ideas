set -e
R=/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild
cd $R/media
export PATH="$HOME/.nvm/versions/node/v24.18.1/bin:$PATH" DISPLAY=:0 PULSE_SERVER=unix:/mnt/wslg/PulseServer
rm -rf fk-av fk-audio.wav; mkdir -p fk-av
ffmpeg -hide_banner -loglevel error -f pulse -i RDPSink.monitor -t 90 -y fk-audio.wav &
FF=$!
node capture_av.mjs "$R/refs/forklift-sim.html" "$R/media/fk-av" 2>&1
wait $FF 2>/dev/null || true
echo DONE
