#!/bin/bash
# ∅ SPHERE NETWORK — Mac/Linux launcher
# Make executable: chmod +x launch.sh
# Then run: ./launch.sh

echo ""
echo "  ∅  Starting Sphere Network with local Whisper..."
echo ""

# Try python3 first, then python
if command -v python3 &>/dev/null; then
    python3 launch.py
elif command -v python &>/dev/null; then
    python launch.py
else
    echo "  ERROR: Python not found."
    echo ""
    echo "  Install Python:"
    echo "    macOS  : brew install python3"
    echo "    Ubuntu : sudo apt install python3 python3-pip"
    echo ""
    read -p "  Press Enter to exit..."
fi
