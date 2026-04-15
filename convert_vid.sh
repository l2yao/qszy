#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <base-name>"
  echo "Example: $0 14-004-0006b"
  exit 1
fi

BASE="$1"
MP3_FILE="${BASE}.mp3"
SRT_FILE="${BASE}.srt"
OUTPUT_FILE="${BASE}.mp4"

if [ ! -f "$MP3_FILE" ]; then
  echo "MP3 file not found: $MP3_FILE"
  exit 2
fi

if [ ! -f "$SRT_FILE" ]; then
  echo "Subtitle file not found: $SRT_FILE"
  exit 3
fi

ffmpeg -loop 1 -i shifu3.jpg -i "$MP3_FILE" -vf "subtitles=$SRT_FILE" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "$OUTPUT_FILE"