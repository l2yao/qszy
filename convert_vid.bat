@echo off
if "%~1"=="" (
    echo Usage: %~nx0 file_prefix
    echo Example: %~nx0 14-004-0004a
    exit /b 1
)
set "name=%~1"
ffmpeg -loop 1 -i images/shifu.jpg -i "mp3/%name%.mp3" -vf "subtitles=txt/%name%.srt" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "mp4/%name%.mp4"