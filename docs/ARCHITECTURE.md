# NXS+ System Architecture

## Overview

The NXS+ Sphere Network is a self-contained, browser-based research application. It requires no installation beyond a modern web browser and no proprietary services for core functionality.

```
┌─────────────────────────────────────────────────────────┐
│                        BROWSER                          │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Three.js r160│  │ Entity System│  │ Physics Engine│  │
│  │ WebGL render │  │Nodes+Connect.│  │Euler·spring   │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │MediaRecorder│  │ Canvas 2D API│  │JSON+ZIP encode│  │
│  │ Audio capture│  │Sketch·GIF enc│  │Vault·Obsidian │  │
│  └──────┬──────┘  └──────────────┘  └───────────────┘  │
│         │                                    │          │
└─────────┼────────────────────────────────────┼──────────┘
          │                                    │
          ▼                                    ▼
┌─────────────────────┐              ┌──────────────────┐
│ OPTIONAL LOCAL      │              │  FETCH API       │
│ PYTHON SERVER       │              │  LLM / Whisper   │
│                     │              │  remote endpoint │
│ faster-whisper      │              └──────────────────┘
│ CTranslate2 ASR     │
│ FastAPI /transcribe │
└─────────────────────┘

          ─ ─ ─ PLANNED EXTENSIONS (this proposal) ─ ─ ─

┌──────────────┐ ┌────────────────┐ ┌───────────────────┐
│ Multi-vault  │ │ Embedding API  │ │ Agent Society     │
│ loader       │ │ (resonance)    │ │ LLM roles         │
└──────────────┘ └────────────────┘ └───────────────────┘
┌──────────────┐ ┌────────────────┐
│ Ontology     │ │ Evaluation     │
│ layer OWL/KG │ │ dashboard      │
└──────────────┘ └────────────────┘
```

---

## Component Map

### Browser Layer

| Component | Technology | Role |
|---|---|---|
| 3D Renderer | Three.js r160 (WebGL) | Scene, camera, lighting, orbit controls |
| Entity System | Custom JS | Sphere-node objects, typed connection edges |
| Physics Engine | Custom Euler integrator | Spring-damper forces, repulsion between nodes |
| Panel System | Vanilla JS + CSS | Floating windows: notes, sketch, URL, audio |
| Audio Capture | `MediaRecorder` API | Record voice notes per node |
| Sketch System | `Canvas 2D` API | Multi-frame drawing, animated GIF export |
| Serialiser | JSON + ZIP encoder | Vault save/load, Obsidian export |
| Fetch Layer | Browser `fetch` | Whisper transcription, LLM API calls |

### Optional Local Server

| Component | Technology | Role |
|---|---|---|
| Transcription server | Python · FastAPI · faster-whisper | Local Whisper ASR (tiny → large-v2) |
| ASR Engine | CTranslate2-optimised Whisper | Offline speech-to-text |

### Planned Observatory Extensions

| Component | Technology | Year |
|---|---|---|
| Multi-vault loader | Modified `loadVault()` | Y1 |
| Resonance computation | Embedding API + cosine similarity matrix | Y1 |
| Bridge connection generation | `addConnection()` + resonance metadata | Y1 |
| Agent society | LLM system-prompt roles + subgraph context | Y2 |
| Ontology layer | RDFLib · OWL · Turtle | Y2 |
| Evaluation dashboard | YAML rubric scores + CSV export | Y3 |
| LLM auto-annotation | On-vault-load pass | Y2–3 |
| Semantic search + fly-to | Vector embedding + camera animation | Y2 |
| Temporal playback | Session journal + timeline scrubber | Y3 |
| Multimodal node generation | Vision-language model on drag-drop | Y2–3 |
| Citation + provenance graph | Zotero API / BibTeX import | Y3 |

---

## Data Flow

```
User action
    │
    ▼
Entity update (position, label, connection)
    │
    ├──► Physics loop (spring-damper, repulsion)
    │
    ├──► Panel sync (notes, sketch, URL, audio)
    │
    ├──► MediaRecorder → base64 blob → node.audios[]
    │         └──► Fetch /transcribe → node.words[]
    │
    └──► Vault serialise → JSON file
              └──► Obsidian export → ZIP archive
```

---

## Three.js Scene Setup

```
PerspectiveCamera (FOV 60, near 0.1, far 5000)
    └── OrbitControls (spherical, drag-rotate, scroll-zoom)

Scene
    ├── AmbientLight (0.6)
    ├── DirectionalLight (0.8, pos 100,200,100)
    ├── PointLight × 2 (accent fill)
    ├── Fog (near 800, far 3000)
    ├── SphereGeometry nodes × N
    │       └── MeshPhongMaterial (colour-coded by type)
    └── Line2 connections × M
            └── Typed material (causal/analogical/oppositional/generative/bridge)
```

---

## Security and Privacy

- **No data leaves the browser** unless the user explicitly enables remote Whisper or LLM API
- All vault data is stored locally (JSON file download / local filesystem)
- No tracking, analytics, or telemetry
- Optional server communication is plaintext HTTP to localhost only (default config)

---

*See also: [`DATA_MODEL.md`](DATA_MODEL.md) · [`VAULT_FORMAT.md`](VAULT_FORMAT.md) · [`ROADMAP.md`](ROADMAP.md)*
