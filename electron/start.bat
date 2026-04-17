@echo off
REM ∅ NXS+ Sphere Network — Quick Start (Windows)
REM Double-click to run, or call from Command Prompt with options:
REM   start.bat --port 8765
REM   start.bat --model medium
REM   start.bat --no-whisper
REM   start.bat --electron   (requires Node.js)
REM   start.bat --browser    (open HTML directly, no server)

setlocal
cd /d "%~dp0"

echo.
echo   ∅ NXS+ Sphere Network
echo   CognitiveNexus Research Practice
echo.

REM ── Electron mode ──────────────────────────────────────────────────────────
echo %* | findstr /i "electron" >nul
if not errorlevel 1 (
    echo Launching Electron desktop app...
    where node >nul 2>&1
    if errorlevel 1 (
        echo Node.js not found. Download from https://nodejs.org
        pause & exit /b 1
    )
    if not exist "node_modules" (
        echo Installing Node dependencies...
        npm install
    )
    npm start
    exit /b
)

REM ── Direct browser mode ─────────────────────────────────────────────────────
echo %* | findstr /i "browser" >nul
if not errorlevel 1 (
    echo Opening directly in browser...
    start "" index.html
    exit /b
)

REM ── Python server mode (default) ────────────────────────────────────────────
echo Starting Python server...

where python >nul 2>&1
if errorlevel 1 (
    where python3 >nul 2>&1
    if errorlevel 1 (
        echo Python not found. Download from https://python.org
        echo.
        echo Alternatively, double-click index.html to open in browser.
        echo ^(Whisper transcription won't be available without Python.^)
        pause
        exit /b 1
    )
    set PYTHON=python3
) else (
    set PYTHON=python
)

echo Using: %PYTHON%
echo.

REM Remove --electron and --browser flags
set ARGS=%*
set ARGS=%ARGS:--electron=%
set ARGS=%ARGS:--browser=%

%PYTHON% start.py %ARGS%

pause
