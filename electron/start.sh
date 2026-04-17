#!/bin/bash
# ∅ NXS+ Sphere Network — Quick Start (macOS / Linux)
# Usage: ./start.sh [options]
#   --port 8765      Custom port
#   --model small    Whisper model (tiny/base/small/medium/large-v2)
#   --no-whisper     Disable local transcription (use OpenAI API)
#   --electron       Launch as desktop app (requires Node.js)

set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ∅ NXS+ Sphere Network"
echo "  CognitiveNexus Research Practice"
echo -e "${NC}"

# ── Mode: Electron desktop ────────────────────────────────────────────────────
if [[ "$*" == *"--electron"* ]]; then
    echo -e "${YELLOW}Launching as Electron desktop app...${NC}"
    if ! command -v node &>/dev/null; then
        echo "Node.js not found. Download from https://nodejs.org"
        exit 1
    fi
    if [ ! -d "node_modules" ]; then
        echo "Installing Node dependencies..."
        npm install
    fi
    npm start
    exit 0
fi

# ── Mode: Direct browser (no server needed) ───────────────────────────────────
if [[ "$*" == *"--browser"* ]]; then
    echo -e "${GREEN}Opening directly in browser (no Whisper)...${NC}"
    if command -v open &>/dev/null; then
        open index.html
    elif command -v xdg-open &>/dev/null; then
        xdg-open index.html
    else
        echo "Open this file in your browser: $DIR/index.html"
    fi
    exit 0
fi

# ── Mode: Python server (default) ────────────────────────────────────────────
echo -e "${YELLOW}Starting Python server...${NC}"

# Check Python
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "Python not found. Download from https://python.org"
    echo ""
    echo "Alternatively, open index.html directly in your browser."
    echo "(Whisper transcription won't be available without Python.)"
    exit 1
fi

echo -e "${GREEN}Using Python: $(which $PYTHON)${NC}"

# Strip --electron and --browser flags before passing to start.py
ARGS=$(echo "$@" | sed 's/--electron//g' | sed 's/--browser//g')

exec $PYTHON start.py $ARGS
