@echo off
REM Gomoku Game - Portable Version
echo Installing/checking dependencies...
python -m pip install -q pygame numba numpy >nul 2>&1
echo Launching Gomoku...
python gomoku_launcher.py
pause
