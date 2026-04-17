# Vault Format Specification

NXS+ uses two serialisation formats: a **JSON vault** for primary storage and round-tripping, and an **Obsidian-compatible ZIP archive** for human-readable export and interoperability.

---

## JSON Vault

### File naming convention
```
{discipline-slug}_{YYYY-MM-DD}.nxsvault.json
```
Example: `architecture-thresholds_2026-04-18.nxsvault.json`

### Top-level structure

```json
{
  "nxs_version": "2.1.0",
  "schema": "https://github.com/YOUR_USERNAME/nxs-sphere-network/blob/main/docs/VAULT_FORMAT.md",
  "created": "2026-04-18T09:00:00Z",
  "modified": "2026-04-18T15:30:00Z",
  "discipline": "architecture",
  "description": "Threshold concepts in spatial design — SCC corpus seed",
  "author": {
    "name": "Dr. Iannis Bardakos",
    "institution": "SCC, BNBU",
    "orcid": "0000-0000-0000-0000"
  },
  "project": {
    "name": "Transdisciplinary Knowledge Ecology",
    "grant": "BNBU Centre for Computational Culture and Heritage | NVIDIA DLI",
    "period": "2025–2028"
  },
  "entities": [],
  "connections": [],
  "groups": [],
  "session_log": [],
  "meta": {
    "node_count": 0,
    "connection_count": 0,
    "group_count": 0,
    "evaluated_bridges": 0
  }
}
```

### `entities[]` array
Array of sphere-node objects. See [`DATA_MODEL.md`](DATA_MODEL.md) for the full node specification.

### `connections[]` array

```json
{
  "id": "conn-uuid",
  "source": "node-uuid-A",
  "target": "node-uuid-B",
  "type": "analogical",
  "weight": 0.74,
  "label": "shared boundary-condition role",
  "directed": true,
  "resonance_score": null,
  "collision_type": null,
  "provenance": null
}
```

**Connection type enum**: `causal` | `analogical` | `oppositional` | `generative` | `historical` | `bridge`

### `groups[]` array

```json
{
  "id": "group-uuid",
  "label": "Boundary Concepts",
  "members": ["node-uuid-1", "node-uuid-2", "node-uuid-3"],
  "color": "#7c3aed",
  "notes": "Cluster of nodes related to spatial and conceptual boundary conditions",
  "agent_summary": null
}
```

### `session_log[]` array

Temporal log of network mutations. Used for provenance tracing and temporal playback.

```json
{
  "timestamp": "2026-04-18T11:30:00Z",
  "action": "node_created",
  "entity_id": "node-uuid",
  "user": "bardakos",
  "data": { "label": "Threshold" }
}
```

**Action enum**: `node_created` | `node_updated` | `node_deleted` | `connection_created` | `connection_deleted` | `annotation_added` | `n_star_spawned` | `evaluation_recorded`

---

## Obsidian ZIP Export

### Structure inside the ZIP

```
vault-name/
├── .obsidian/
│   └── app.json          # Minimal Obsidian config
├── nodes/
│   ├── Threshold.md
│   ├── Membrane.md
│   └── Threshold-Membrane.md   # bridge concept n*
├── attachments/
│   ├── threshold-sketch.gif
│   ├── threshold-audio-1.webm
│   └── membrane-sketch.gif
├── _index.md             # Vault overview with node count, date, discipline
└── _graph-export.json    # Copy of the full JSON vault
```

### Markdown file format (per node)

```markdown
---
id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
label: Threshold
type: concept
discipline: architecture
color: "#4a9eff"
group: boundary-concepts
created: 2026-04-18T09:30:00Z
modified: 2026-04-18T11:45:00Z
tags: [concept, boundary, spatial-design]
---

# Threshold

A boundary condition that mediates transition between states.

See also: [[Membrane]], [[Edge (Graph Theory)]], [[Interface (Architecture)]]

## Words
threshold · boundary · liminal · membrane

## Notes
A boundary condition that mediates transition between states. See Aldo van Eyck on the threshold as *the place of encounter*.

## Sketches
![[threshold-sketch.gif]]

## Audio
![[threshold-audio-1.webm]]

## URLs
- [Boundary — Stanford Encyclopedia](https://plato.stanford.edu/entries/boundary/)

## Connections
- [[Membrane]] — analogical (shared boundary-condition role, resonance: 0.87)
- [[Interface (Architecture)]] — causal (threshold enables interface)
```

### Bridge-concept node (n*)

```markdown
---
id: n-star-uuid
label: Threshold-Membrane
type: bridge
collision_type: analogy
source_A: Threshold
source_B: Membrane
resonance_score: 0.87
disciplinary_distance: 0.71
classification: fertile
tags: [bridge-concept, n-star, evaluated]
---

# Threshold-Membrane

> Bridge-concept generated from collision: [[Threshold]] (architecture) × [[Membrane]] (cell biology)
> Collision type: **Analogy** · Resonance: 0.87 · Distance: 0.71

A concept of **bounded permeability** applicable to both spatial and biological boundary design: a surface that is both boundary and passage, selective rather than absolute in its mediation.

## Provenance
- Source A: [[Threshold]] — structural role: boundary mediating inside/outside transition
- Source B: [[Membrane]] — structural role: selective passage between cytoplasm and environment
- Shared feature: boundary-condition with selective permeability

## Evaluation
```yaml
traceability: true
disciplinary_distance: 0.71
conceptual_coherence: 4/5
categorical_novelty: true
pedagogical_value: fertile
artistic_usefulness: plausible
classification: fertile
```
```

---

## Loading a Vault

### JavaScript (browser)

```javascript
// Load from file input
async function loadVault(file) {
  const text = await file.text();
  const vault = JSON.parse(text);
  
  // Validate schema version
  if (!vault.nxs_version) throw new Error('Not a valid NXS+ vault');
  
  // Populate entity system
  vault.entities.forEach(entity => spawnSphere(entity));
  vault.connections.forEach(conn => addConnection(conn));
  vault.groups.forEach(group => createGroup(group));
  
  console.log(`Loaded vault: ${vault.description}`);
  console.log(`${vault.meta.node_count} nodes, ${vault.meta.connection_count} connections`);
}
```

### Multi-vault loading (Year 1 extension)

```javascript
async function loadMultiVault(files, disciplineColors) {
  const vaults = await Promise.all(files.map(f => f.text().then(JSON.parse)));
  
  vaults.forEach((vault, index) => {
    const offset = { x: index * 200, y: 0, z: 0 };  // spatial separation
    const color = disciplineColors[index];
    
    vault.entities.forEach(entity => {
      spawnSphere({
        ...entity,
        position: {
          x: entity.position.x + offset.x,
          y: entity.position.y + offset.y,
          z: entity.position.z + offset.z
        },
        color: color,
        vault_discipline: vault.discipline
      });
    });
  });
  
  // Trigger resonance computation after all nodes loaded
  computeResonance();
}
```

---

## Versioning

| Version | Changes |
|---|---|
| `1.0.0` | Initial format: entities, connections |
| `2.0.0` | Added groups, session_log, meta block |
| `2.1.0` | Added provenance fields, n* schema, evaluation YAML |
| `3.0.0` *(planned Y1)* | Multi-vault support, resonance scores, discipline metadata |

---

*See also: [`DATA_MODEL.md`](DATA_MODEL.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)*
