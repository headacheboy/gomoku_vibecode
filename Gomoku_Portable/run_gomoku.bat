@echo off
REM Gomoku Game Launcher
REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.5+ and add it to PATH.
    pause
    exit /b 1
)

REM Check if required modules are installed
python -c "import pygame, numba, numpy" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    python -m pip install pygame numba numpy
)

REM Launch the Gomoku game
echo Starting Gomoku Game...
python -m gomoku.main
