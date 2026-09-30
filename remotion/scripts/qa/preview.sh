#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

QA_DIR="out/qa"
FIXTURE_DIR="$QA_DIR/fixture"
PREVIEW_FILE="$QA_DIR/preview.mp4"

mkdir -p "$FIXTURE_DIR"

SOURCE_BACKUP=""
AUDIO_BACKUP=""

cleanup() {
  if [[ -n "$SOURCE_BACKUP" && -f "$SOURCE_BACKUP" ]]; then
    cp "$SOURCE_BACKUP" public/source.mp4
  fi

  if [[ -n "$AUDIO_BACKUP" && -f "$AUDIO_BACKUP" ]]; then
    cp "$AUDIO_BACKUP" public/audio.wav
  fi
}

trap cleanup EXIT

if [[ -f public/source.mp4 ]]; then
  SOURCE_BACKUP="$FIXTURE_DIR/source.original.mp4"
  cp public/source.mp4 "$SOURCE_BACKUP"
fi

if [[ -f public/audio.wav ]]; then
  AUDIO_BACKUP="$FIXTURE_DIR/audio.original.wav"
  cp public/audio.wav "$AUDIO_BACKUP"
fi

echo "Creating synthetic test video..."

ffmpeg -y \
  -f lavfi \
  -i "color=c=black:s=1080x1920:r=30:d=3" \
  -c:v libx264 \
  -pix_fmt yuv420p \
  public/source.mp4

echo "Creating synthetic test audio..."

ffmpeg -y \
  -f lavfi \
  -i "sine=frequency=440:sample_rate=48000:duration=3" \
  -c:a pcm_s16le \
  public/audio.wav

echo "Rendering safe three-second preview..."

npx remotion render \
  src/index.ts \
  EgeOlimpiada \
  "$PREVIEW_FILE" \
  --frames=0-89

echo "Validating rendered MP4..."

bash scripts/qa/validate-mp4.sh "$PREVIEW_FILE"

echo "Safe preview render passed."
