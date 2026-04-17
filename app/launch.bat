@echo off
title ∅ SPHERE NETWORK — Local Whisper
echo.
echo   Starting Sphere Network with local Whisper...
echo   Keep this window open while using the app.
echo.

:: Try python, then python3
python --version >nul 2>&1
if %errorlevel% == 0 (
    python launch.py
) else (
    python3 --version >nul 2>&1
    if %errorlevel% == 0 (
        python3 launch.py
    ) else (
        echo   ERROR: Python not found.
        echo   Install from https://www.python.org/downloads/
        echo   Make sure to check "Add Python to PATH" during install.
    )
)

pause
