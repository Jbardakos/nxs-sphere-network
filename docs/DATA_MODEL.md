# Sphere-Node Data Model

## Entity Object

Each sphere-node is a structured JavaScript object serialised to JSON on vault save. All five content fields are arrays stored directly on the entity.

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "label": "Threshold",
  "position": { "x": 12.4, "y": -8.1, "z": 3.7 },
  "velocity": { "x": 0, "y": 0, "z": 0 },
  "color": "#4a9eff",
  "type": "concept",
  "group": null,
  "words": [
    "threshold",
    "boundary",
    "liminal",
    "membrane"
  ],
  "notes": "# Threshold\n\nA boundary condition that mediates transition between states. See also: membrane (cell biology), edge (graph theory), interface (architecture).",
  "frames": [
    {
      "data": "data:image/png;base64,iVBORw0KGgo...",
      "opacity": 1.0
    }
  ],
  "urls": [
    "https://en.wikipedia.org/wiki/Threshold_(disambiguation)",
    "https://plato.stanford.edu/entries/boundary/"
  ],
  "audios": [
    "data:audio/webm;base64,GkXfo59ChoEB..."
  ],
  "meta": {
    "created": "2026-04-18T09:30:00Z",
    "modified": "2026-04-18T11:45:00Z",
    "discipline": "architecture",
    "epistemic_function": "boundary-concept",
    "resonance_score": null,
    "collision_type": null
  }
}
```

---

## Field Reference

### Core Identity

| Field | Type | Description |
|---|---|---|
| `id` | `string` (UUID v4) | Stable unique identifier |
| `label` | `string` | Display name shown on sphere in 3D scene |
| `position` | `{x, y, z}` | 3D world position (float) |
| `velocity` | `{x, y, z}` | Physics velocity vector (reset on manual drag) |
| `color` | `string` (hex) | Sphere colour, colour-coded by type or discipline |
| `type` | `string` | One of: `concept`, `method`, `actor`, `media`, `problem`, `bridge` |
| `group` | `string` \| `null` | Group ID for cluster membership |

### Content Arrays

#### `words[]` — Transcribed Tokens
Array of word-strings, primarily populated by Whisper ASR from voice recordings. Also accepts manual entries. Used as the primary input for embedding-based resonance computation.

```json
"words": ["threshold", "boundary", "membrane", "liminal space"]
```

#### `notes` — Free-text Annotation
A single Markdown-compatible string. Supports headings, links, bold/italic. Rendered in the notes panel. Exported as the body of the Obsidian Markdown file.

```json
"notes": "# Threshold\n\nSee Aldo van Eyck on the threshold as *the place of encounter*."
```

#### `frames[]` — Sketch Animation Frames
Array of frame objects, max 30 frames. Each frame stores a `base64`-encoded PNG canvas snapshot and a floating-point opacity value (0.0–1.0). On export, frames are encoded to an animated GIF at 5, 15, or 30 fps using a pure-JavaScript LZW encoder with per-frame local colour table quantisation.

```json
"frames": [
  { "data": "data:image/png;base64,...", "opacity": 1.0 },
  { "data": "data:image/png;base64,...", "opacity": 0.85 }
]
```

#### `urls[]` — Embedded URL References
Array of URL strings. Each URL is openable as an embedded iframe panel within the NXS+ interface. Useful for linking to sources, datasets, live tools, or documentation pages without leaving the graph environment.

```json
"urls": [
  "https://plato.stanford.edu/entries/boundary/",
  "https://doi.org/10.1234/example"
]
```

#### `audios[]` — Audio Recordings
Array of `base64` dataURL strings. Format depends on browser: `WebM/Opus`, `OGG`, or `MP4`. Blobs are saved to this array **immediately** on recording stop, before any transcription call, ensuring audio is never lost if the transcription endpoint is unavailable.

```json
"audios": [
  "data:audio/webm;base64,GkXfo59ChoEB..."
]
```

---

## Connection Object

```json
{
  "id": "conn-uuid",
  "source": "node-uuid-A",
  "target": "node-uuid-B",
  "type": "analogical",
  "weight": 0.74,
  "label": "shared boundary-condition role",
  "resonance_score": 0.82,
  "collision_type": "analogy",
  "provenance": {
    "created_by": "scout-agent",
    "created_at": "2026-04-18T14:00:00Z",
    "source_discipline": "architecture",
    "target_discipline": "cell-biology"
  }
}
```

### Connection Types

| Type | Description | Visual |
|---|---|---|
| `causal` | A causes or enables B | Solid arrow |
| `analogical` | A and B share structural role in their respective domains | Dashed |
| `oppositional` | A and B are in tension or contradiction | Red dashed |
| `generative` | A produces or gives rise to B | Thick solid |
| `historical` | A precedes or contextualises B temporally | Dotted |
| `bridge` | Cross-discipline resonance connection (auto-generated) | Pulsing, colour-coded by collision type |

---

## Vault Document (top-level JSON)

```json
{
  "version": "2.1.0",
  "created": "2026-04-18T09:00:00Z",
  "modified": "2026-04-18T15:30:00Z",
  "discipline": "architecture",
  "description": "Threshold concepts in spatial design",
  "entities": [ /* array of node objects */ ],
  "connections": [ /* array of connection objects */ ],
  "groups": [ /* array of group cluster objects */ ],
  "meta": {
    "node_count": 42,
    "connection_count": 67,
    "author": "Dr. Iannis Bardakos",
    "institution": "SCC, BNBU",
    "project": "Transdisciplinary Knowledge Ecology"
  }
}
```

---

## Bridge-Concept Node (n*)

Second-order novel objects produced by the collision engine carry additional provenance fields:

```json
{
  "id": "n-star-uuid",
  "label": "Threshold-Membrane",
  "type": "bridge",
  "color": "#ff9f40",
  "words": ["threshold-membrane", "bounded permeability", "selective passage"],
  "notes": "A concept emerging from the collision of 'threshold' (architecture) and 'membrane' (cell biology): a surface that is both boundary and passage, selective rather than absolute.",
  "provenance": {
    "source_node_A": "node-uuid-architecture-threshold",
    "source_node_B": "node-uuid-biology-membrane",
    "collision_type": "analogy",
    "resonance_score": 0.87,
    "disciplinary_distance": 0.71,
    "spawned_by": "bridge-builder-agent",
    "spawned_at": "2026-04-18T16:00:00Z",
    "evaluation": {
      "traceability": true,
      "disciplinary_distance": 0.71,
      "conceptual_coherence": 4,
      "categorical_novelty": true,
      "pedagogical_value": "pending",
      "artistic_usefulness": "pending"
    }
  }
}
```

---

*See also: [`VAULT_FORMAT.md`](VAULT_FORMAT.md) · [`COLLISION_TYPES.md`](COLLISION_TYPES.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)*
