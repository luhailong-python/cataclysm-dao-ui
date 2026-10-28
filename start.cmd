@echo off
setlocal
cd /d "%~dp0"
python -m app --width 1600 --height 900
if errorlevel 1 (
  echo.
  echo Launcher could not start. Install Python 3.11+ and run:
  echo python -m pip install -r requirements.txt
  pause
)
endlocal
