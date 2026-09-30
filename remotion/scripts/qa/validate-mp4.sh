#!/usr/bin/env bash
set -euo pipefail

FILE="${1:-}"

if [[ -z "$FILE" ]]; then
  echo "ERROR: MP4 path was not provided."
  exit 1
fi

if [[ ! -f "$FILE" ]]; then
  echo "ERROR: MP4 does not exist: $FILE"
  exit 1
fi

if [[ ! -s "$FILE" ]]; then
  echo "ERROR: MP4 is empty: $FILE"
  exit 1
fi

echo "Checking video stream..."

VIDEO_CODEC="$(
  ffprobe -v error \
    -select_streams v:0 \
    -show_entries stream=codec_name \
    -of default=noprint_wrappers=1:nokey=1 \
    "$FILE"
)"

if [[ -z "$VIDEO_CODEC" ]]; then
  echo "ERROR: No video stream found."
  exit 1
fi

echo "Checking dimensions..."

WIDTH="$(
  ffprobe -v error \
    -select_streams v:0 \
    -show_entries stream=width \
    -of default=noprint_wrappers=1:nokey=1 \
    "$FILE"
)"

HEIGHT="$(
  ffprobe -v error \
    -select_streams v:0 \
    -show_entries stream=height \
    -of default=noprint_wrappers=1:nokey=1 \
    "$FILE"
)"

if [[ -z "$WIDTH" || -z "$HEIGHT" ]]; then
  echo "ERROR: Could not determine video dimensions."
  exit 1
fi

if [[ "$WIDTH" -le 0 || "$HEIGHT" -le 0 ]]; then
  echo "ERROR: Invalid video dimensions: ${WIDTH}x${HEIGHT}"
  exit 1
fi

echo "Checking duration..."

DURATION="$(
  ffprobe -v error \
    -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 \
    "$FILE"
)"

if [[ -z "$DURATION" ]]; then
  echo "ERROR: Could not determine video duration."
  exit 1
fi

awk -v duration="$DURATION" 'BEGIN {
  if (duration <= 0) {
    print "ERROR: Video duration must be greater than zero."
    exit 1
  }
}'

echo "Checking full decode..."

ffmpeg -v error -i "$FILE" -f null -

echo "MP4 validation passed:"
echo "  codec: $VIDEO_CODEC"
echo "  dimensions: ${WIDTH}x${HEIGHT}"
echo "  duration: ${DURATION}s"
