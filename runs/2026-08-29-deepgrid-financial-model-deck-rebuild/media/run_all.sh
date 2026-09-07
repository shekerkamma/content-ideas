set -e
R=/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild
cd $R/media
export PATH="$HOME/.nvm/versions/node/v24.18.1/bin:$PATH"
DISPLAY=:0 node capture_sim.mjs "$R/refs/forklift-sim.html" "$R/media/forklift" '[[null,3000,"settle"],["button[data-t=putaway]",14000,"inbound put-away"],["button[data-t=pick]",14000,"pick run"],["button[data-t=peak]",16000,"peak-hour floor"]]'
DISPLAY=:0 node capture_sim.mjs "$R/refs/yard-sim.html" "$R/media/yard" '[["#startBtn",4000,"enter terminal"],["button[data-s=quay]",14000,"quay discharge"],["button[data-s=canyon]",14000,"container canyon"],["#bConf",4000,"confidence"],["button[data-s=peak]",14000,"peak mixed traffic"]]'
DISPLAY=:0 node capture_sim.mjs "$R/refs/sentinel-sim.html" "$R/media/sentinel" '[["#start",4000,"open console"],["button[data-s=intrusion]",16000,"coordinated intrusion"],["button[data-s=patrol]",13000,"perimeter patrol"],["button[data-s=maritime]",13000,"maritime approach"]]'
echo ALLDONE
