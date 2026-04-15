@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo Running convert_vid.sh for all MP3 files in %CD%
for %%F in (*.mp3) do (
  set "basename=%%~nF"
  echo.
  echo Converting !basename! ...
  bash -lc "./convert_vid.sh \"!basename!\""
)

echo.
echo All done.
endlocal
