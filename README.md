# ∅ NXS+ Sphere Network

> **A browser-based 3D concept-network environment for transdisciplinary knowledge ecology research.**

Part of the **Cognitive Nexus Research Practice** · School of Culture & Creativity, BNBU, Zhuhai  
Principal Investigator: **Dr. Iannis Bardakos**

---

## Overview

The NXS+ Sphere Network is a self-contained, browser-based research instrument for building, annotating, and navigating concept networks in three-dimensional space. It requires no installation beyond a modern web browser and no proprietary services for its core functionality.

Each **sphere-node** holds a rich data bundle: Whisper-transcribed voice notes, free-text annotations, multi-frame sketches (exported as animated GIFs), embedded URL panels, and audio recordings. Networks are serialised to portable JSON vaults and exportable as Obsidian-compatible Markdown archives.

The system is the operational substrate of the **Agentic Transdisciplinary Observatory** project (2025–2028), which extends NXS+ with multi-vault loading, embedding-based resonance detection, a nine-role AI agent society, a six-type collision engine, and a human-in-the-loop evaluation layer.

---

## Key Features

| Feature | Status |
|---|---|
| 3D sphere-node graph (Three.js r160) | ✅ Live |
| Typed connections (causal, analogical, oppositional, generative) | ✅ Live |
| Voice recording + Whisper transcription (local or OpenAI API) | ✅ Live |
| Multi-frame sketch / animated GIF export | ✅ Live |
| URL browser (iframe panels) | ✅ Live |
| Audio retention per node | ✅ Live |
| JSON vault serialisation | ✅ Live |
| Obsidian vault export (ZIP, wikilinks, embedded assets) | ✅ Live |
| Physics simulation (spring-damper, repulsion) | ✅ Live |
| Local Whisper Python server (faster-whisper) | ✅ Live |
| Multi-vault simultaneous loading | 🔄 Year 1 |
| Embedding-based resonance computation | 🔄 Year 1 |
| Role-differentiated agent society (9 roles) | 🔄 Year 2 |
| Collision engine (6 types) | 🔄 Year 2 |
| Bridge-concept spawning (n*) | 🔄 Year 2 |
| Provenance tracing dashboard | 🔄 Year 2 |
| Ontology construction layer (OWL/Turtle) | 🔄 Year 2 |
| Evaluation rubric interface | 🔄 Year 3 |
| SCC corpus + KG dataset | 🔄 Year 3 |

---

## Quick Start

### Run directly in browser

```bash
git clone https://github.com/YOUR_USERNAME/nxs-sphere-network.git
cd nxs-sphere-network
open src/nxs-plus.html        # macOS
# or: xdg-open src/nxs-plus.html   # Linux
# or: simply drag the file into any modern browser window
```

No build step. No dependencies to install. The application is a **single HTML file**.

### Enable local Whisper transcription (optional)

```bash
pip install faster-whisper fastapi uvicorn
cd src/server
python whisper_server.py
```

The server starts at `http://localhost:8765/transcribe`. The browser app auto-detects it on launch.

---

## Repository Structure

```
nxs-sphere-network/
├── src/
│   ├── nxs-plus.html          # Main application (single-file, self-contained)
│   └── server/
│       └── whisper_server.py  # Optional local Whisper transcription server
├── docs/
│   ├── ARCHITECTURE.md        # System architecture and component map
│   ├── DATA_MODEL.md          # Sphere-node data bundle specification
│   ├── COLLISION_TYPES.md     # Six collision type taxonomy
│   ├── AGENT_ROLES.md         # Nine agent role definitions
│   ├── EVALUATION_RUBRIC.md   # Bridge-concept evaluation criteria
│   ├── VAULT_FORMAT.md        # JSON vault and Obsidian export spec
│   └── ROADMAP.md             # Three-year development plan
├── examples/
│   ├── demo-vault.json        # Sample vault with annotated sphere-nodes
│   └── obsidian-export/       # Sample Obsidian vault export
├── assets/
│   └── diagrams/              # Architecture diagrams and figures
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## Technical Architecture

### Runtime and Rendering

The application runs entirely client-side as a single HTML file with embedded JavaScript.

- **3D Engine**: Three.js r160 (MIT licence) via ES module import
- **Renderer**: `WebGLRenderer` with `PerspectiveCamera`, spherical orbit controls, fog, multi-light setup
- **Physics**: Custom Euler integrator with spring-damper connections and repulsion forces
- **No build tools**: No webpack, no npm, no compilation step required

### Sphere-Node Data Model

Each node is a structured entity holding five independent content arrays:

```json
{
  "id": "uuid-v4",
  "label": "Threshold",
  "position": { "x": 0, "y": 0, "z": 0 },
  "color": "#4a9eff",
  "words": ["threshold", "boundary", "membrane"],
  "notes": "Free-text markdown-compatible annotation",
  "frames": [
    { "data": "base64-PNG...", "opacity": 1.0 }
  ],
  "urls": ["https://example.com"],
  "audios": ["base64-dataURL-webm..."]
}
```

See [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) for the full specification.

### Voice Transcription Pipeline

Audio recording uses the browser's `MediaRecorder` API. The blob (WebM/Opus, OGG, or MP4 depending on browser) is saved immediately as a `base64` dataURL on the node's `audios[]` array **before** any network call, ensuring audio is never lost if transcription fails.

Transcription routes:
1. **Local** — Python server running `faster-whisper` (CTranslate2-optimised) via FastAPI
2. **Remote** — OpenAI `/v1/audio/transcriptions` endpoint (API key required)

### Serialisation and Interoperability

- **JSON vault** — complete network state serialised to a portable `.json` file
- **Obsidian ZIP export** — one Markdown file per sphere with YAML frontmatter, wikilink connections, embedded image references, and audio file attachments

---

## Planned Extensions (Observatory)

The three-year development plan transforms NXS+ into the **Agentic Transdisciplinary Observatory**:

### Year 1 — Foundations
- Multi-vault loader: load two discipline graphs simultaneously in the same 3D scene
- Embedding-based resonance: cosine similarity across `words[]` arrays to detect high-Φ node pairs
- Bridge connection generation: auto-connect resonant pairs with typed bridge material

### Year 2 — System Build
- **Agent society** (9 roles): Archivist, Historian, Formaliser, Sceptic, Bridge-builder, Aesthetic Critic, Methodologist, Curator, Educator
- **Collision engine** (6 types): Analogy, Contradiction, Grafting, Scale Shift, Ontological Mismatch, Method Transfer
- **n\* spawning**: second-order novel concept nodes with full provenance tracing
- Ontology layer: OWL/Turtle export via RDFLib

### Year 3 — Deployment
- Evaluation rubric dashboard (6 criteria: Traceability, Disciplinary Distance, Conceptual Coherence, Categorical Novelty, Pedagogical Value, Artistic Usefulness)
- SCC corpus + open KG dataset release
- Full pilot in BNBU seminars and research clusters

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the complete timeline.

---

## Research Context

NXS+ is the operational substrate of the **Transdisciplinary Knowledge Ecology** project (BNBU SCC, 2025–2028). The research proposes that disciplines are not containers of information but **knowledge ecologies** — structured terrains of concepts, methods, assumptions, values, and historical formations represented as graph structures.

The system stages **structured encounters** between heterogeneous epistemic positions using role-differentiated AI agents, producing **bridge-concepts** (n\*) — candidate ideas, questions, or methods that neither network could generate in isolation.

### Related Documents
- [`docs/COLLISION_TYPES.md`](docs/COLLISION_TYPES.md) — the six collision grammar types
- [`docs/AGENT_ROLES.md`](docs/AGENT_ROLES.md) — nine epistemic agent role definitions
- [`docs/EVALUATION_RUBRIC.md`](docs/EVALUATION_RUBRIC.md) — cultural usefulness rubric

### Publications and Proposals
- Bardakos, I. (2025). *∅ Entanglement Field: A Conceptual, Philosophical and Mathematical Model for Transdisciplinary Collision and Second-Order Novelty*. Working document, CognitiveNexus Research Practice, BNBU, Zhuhai.

---

## Acknowledgement

Projects using the Centre's GPU resources should include affiliation with the **BNBU Centre for Computational Culture and Heritage | NVIDIA DLI** in publications. Projects not directly using Centre resources should acknowledge the Centre.

---

## License

This project is licensed under the MIT License — see [`LICENSE`](LICENSE) for details.

---

## Contributing

See [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) for contribution guidelines, issue templates, and code style.

---

*CognitiveNexus Research Practice · School of Culture & Creativity · BNU-HKBU United International College, Zhuhai · 2026*
