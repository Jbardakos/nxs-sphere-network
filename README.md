# NXS+ Sphere Network

A self-contained browser-based research tool for building 3D concept networks — sphere-nodes connected in navigable space, each carrying voice transcriptions, notes, sketches, URLs, and audio recordings.

Built for the **BNBU Centre for Computational Culture and Heritage / NVIDIA DLI** research programme at the School of Culture & Creativity, BNU-HKBU United International College, Zhuhai.

---

## Quick Start

**Browser only (no install):**
Open `app/appearance-trigger.html` in Chrome or Firefox. Everything runs client-side.

**With local Whisper transcription:**
```bash
cd app
python start.py        # installs deps, starts FastAPI server on :8765
# then open appearance-trigger.html
```

**Electron desktop app:**
```bash
cd electron
npm install
npm start
```

---

## Key Controls

| Key | Action |
|-----|--------|
| `[1]` hold | Activate spawn window |
| `[2]` hold+release | Spawn sphere (size = hold duration) |
| `[3]` | Connect two selected spheres |
| `[4]` hold | Record voice note |
| `N` | Open notes window |
| `K` | Open sketch window |
| `U` | Open URL window |
| `V` | Open word display |
| `M` | Toggle key reference |
| `Space` + drag | Pan camera |
| `Shift` | Multi-select |
| `⌫` | Delete selected |

---

## Project Structure

```
├── app/
│   ├── appearance-trigger.html   # Main app (self-contained)
│   ├── start.py                  # Local Whisper server (FastAPI)
│   ├── launch.py                 # Auto-launcher
│   ├── setup.py                  # Dependency installer
│   ├── launch.sh                 # macOS/Linux launcher
│   └── launch.bat                # Windows launcher
├── electron/
│   ├── main.js                   # Electron wrapper
│   ├── package.json
│   ├── start.sh
│   └── start.bat
├── proposals/
│   ├── villa-proposal.html       # BNBU SCC research proposal (HTML)
│   ├── entanglement-field.pdf    # ∅ Entanglement Field: conceptual/mathematical model
│   ├── entanglement-field.tex    # LaTeX source
│   ├── sota-matrix.pdf           # State-of-the-art matrix
│   ├── sota-matrix.tex
│   ├── proposal.pdf              # Main grant proposal
│   └── proposal.tex
└── README.md
```

---

## Research Context

Part of the **∅ Entanglement Field** research practice (CognitiveNexus / Bardakos, 2025–2026). The system models disciplines as graph ecologies and uses AI agents to stage structured encounters between them, producing traceable bridge-concepts for artistic, curatorial, and pedagogical use.

**PI:** Dr. Iannis Bardakos, School of Culture & Creativity, BNBU  
**Lab:** BNBU Centre for Computational Culture and Heritage | NVIDIA DLI

---

## Tech Stack

- [Three.js r160](https://threejs.org/) — 3D rendering (WebGL)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — local speech transcription
- [FastAPI](https://fastapi.tiangolo.com/) — local transcription server
- Pure-JS GIF encoder, ZIP encoder, Obsidian vault export — no external dependencies

## License

MIT
