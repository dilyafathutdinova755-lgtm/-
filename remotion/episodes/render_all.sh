#!/bin/bash
set -e
cd /home/user/-/remotion
BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell

for i in 1 2 3 4 5 6; do
  echo "=== EPISODE $i: preparing assets ==="
  cp "episodes/ep${i}_clip.mp4" public/source.mp4
  cp "episodes/ep${i}_audio.wav" public/audio.wav
  cp "episodes/ep${i}_cards.json" src/data/cards.json
  cp "episodes/ep${i}_running_caption.json" src/data/running_caption.json
  cp "episodes/ep${i}_words.json" src/data/words.json
  cp "episodes/ep${i}_duration.json" src/data/duration.json

  echo "=== EPISODE $i: rendering ==="
  rm -f "episodes/ep${i}_final.mp4"
  npx remotion render src/index.ts EgeOlimpiada "episodes/ep${i}_final.mp4" --browser-executable="$BROWSER" --log=verbose

  echo "=== EPISODE $i: DONE ==="
done

echo "ALL_EPISODES_DONE"
