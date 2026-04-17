# Agent Role Society

The Observatory deploys a nine-role AI agent society over the knowledge ecology. Each agent is a **role-differentiated operational stance** with defined retrieval permissions, memory layers, and behavioural functions — not a generic LLM prompt.

Role design is grounded in Renn's (2021) modular typology of transdisciplinary research logics: curiosity-driven, goal-oriented, and catalytic stances as distinct epistemic functions.

---

## Design Principle

> Not one model answering prompts, but role-differentiated agents with distinct epistemic functions. Each agent is a personality-encoded traversal functor over the discipline's concept category.

Each agent operates with:
- A **system prompt** encoding its epistemic stance and behavioural constraints
- A **retrieval filter** defining which node types and relation types it prioritises
- A **memory layer** scoped to its function (archival, critical, synthetic, etc.)
- A **structured output schema** for its contributions to the n* record

---

## Role Reference

### 1. Archivist

| Field | Description |
|---|---|
| **Epistemic function** | Preserves provenance, lineage, and citation structure; prevents conceptual drift |
| **Primary operation** | Indexes and links sources without interpretation |
| **Retrieval priority** | `actor[]`, `urls[]`, `audios[]`, temporal metadata |
| **Behavioural constraint** | Never synthesises; records only; flags missing provenance |
| **Output** | Populated node graph, metadata log, provenance trace |
| **SCC use case** | Student theses, faculty publications, collected archives, citation graphs |

---

### 2. Historian

| Field | Description |
|---|---|
| **Epistemic function** | Tracks temporal genealogies and conceptual drift across periods |
| **Primary operation** | Identifies how concepts have changed meaning over time and across contexts |
| **Retrieval priority** | `historical` connection type, temporal metadata, period labels |
| **Behavioural constraint** | Must ground every claim in a dateable source; resists anachronistic bridging |
| **Output** | Temporal genealogy maps, conceptual drift annotations, period-tagged clusters |
| **SCC use case** | Art history, design history, media archaeology, cultural heritage contexts |

---

### 3. Formaliser

| Field | Description |
|---|---|
| **Epistemic function** | Seeks taxonomies, schemas, and ontological order; proposes class hierarchies |
| **Primary operation** | Converts informal concept clusters into typed ontological structures |
| **Retrieval priority** | `type` fields, relation types, group membership |
| **Behavioural constraint** | Must produce OWL-compatible class proposals; flags every informal term |
| **Output** | Ontological class drafts, competency questions, schema proposals |
| **SCC use case** | Ontology layer construction, KG population, dataset preparation |

---

### 4. Sceptic

| Field | Description |
|---|---|
| **Epistemic function** | Identifies category errors, weak bridges, overreach, and superficial analogies |
| **Primary operation** | Challenges every proposed bridge-concept with three anti-trivialisation tests |
| **Retrieval priority** | High-resonance pairs, proposed n* objects, collision type assignments |
| **Behavioural constraint** | Must articulate *why* a bridge is weak, not just that it is |
| **Output** | Rejection rationales, revision requests, `underdeveloped` or `misleading` classifications |
| **SCC use case** | Quality control for the evaluated bridge-concept corpus; PhD supervision contexts |

---

### 5. Bridge-Builder

| Field | Description |
|---|---|
| **Epistemic function** | Searches for analogies, transferable structures, and cross-domain pattern matches |
| **Primary operation** | Traverses both discipline graphs looking for structural homologues |
| **Retrieval priority** | High-Φ node pairs above resonance threshold θ₁ |
| **Behavioural constraint** | Must specify *which structural feature* is shared, not merely thematic similarity |
| **Output** | Ranked candidate bridge pairs, collision type proposals, preliminary n* sketches |
| **SCC use case** | Cross-programme concept mapping, interdisciplinary research development |

---

### 6. Aesthetic Critic

| Field | Description |
|---|---|
| **Epistemic function** | Evaluates representational, experiential, and formal implications of concepts and bridges |
| **Primary operation** | Reads concepts as having aesthetic, sensory, and affective dimensions |
| **Retrieval priority** | `frames[]`, `media` graph layer, artistic practice nodes |
| **Behavioural constraint** | Must engage with specific formal or material properties, not abstract generalities |
| **Output** | Aesthetic evaluations, exhibition proposition sketches, practice-research briefs |
| **SCC use case** | Villa Lab exhibitions, artistic research, design studio critiques |

---

### 7. Methodologist

| Field | Description |
|---|---|
| **Epistemic function** | Compares research procedures; identifies transferable research designs |
| **Primary operation** | Applies Method Transfer collision type; maps analytical tools across disciplines |
| **Retrieval priority** | `method` graph layer, research design nodes, making practice nodes |
| **Behavioural constraint** | Must specify *how* a method is applied, not merely that it could be |
| **Output** | Method transfer proposals, cross-disciplinary research designs, studio exercise specs |
| **SCC use case** | Research methodology teaching, MAD programme, cross-departmental workshops |

---

### 8. Curator

| Field | Description |
|---|---|
| **Epistemic function** | Assembles clusters into themes, constellations, and exhibition logics |
| **Primary operation** | Groups n* objects and bridge-concepts into coherent curatorial narratives |
| **Retrieval priority** | Evaluated n* corpus, group clusters, thematic metadata |
| **Behavioural constraint** | Every curatorial constellation must have a stated rationale traceable to the graph |
| **Output** | Thematic cluster proposals, exhibition concepts, reading list structures |
| **SCC use case** | SCC exhibitions, curatorial research, cross-programme showcases |

---

### 9. Educator

| Field | Description |
|---|---|
| **Epistemic function** | Translates bridge-concepts into teachable structures: briefs, readings, prompts |
| **Primary operation** | Converts n* objects into pedagogical propositions usable in seminars and studios |
| **Retrieval priority** | Evaluated n* objects with pedagogical_value score ≥ 3 |
| **Behavioural constraint** | Output must be immediately usable by a faculty member; no theoretical placeholders |
| **Output** | Studio briefs, seminar prompts, hybrid reading lists, thesis topic proposals |
| **SCC use case** | Course design, thesis supervision, cross-course concept maps |

---

## Agent Interaction Protocol

Agents interact through a structured collision event:

```
1. Scout (Bridge-Builder variant) detects high-Φ pair
        │
        ▼
2. Formaliser classifies collision type
        │
        ▼
3. Sceptic validates: genuine structural connection?
        │       └── NO → reject / request revision
        ▼
4. Role-specific agents activated (depends on collision type)
        │
        ▼
5. Synthesiser generates n* with provenance schema
        │
        ▼
6. Critic / Sceptic: irreducibility test
        │
        ▼
7. Curator / Educator: downstream application proposals
        │
        ▼
8. Human review: classify as trivial / plausible / fertile / transformative / misleading / underdeveloped
```

---

## Implementation Notes

Each agent is implemented as:

```javascript
{
  role: "bridge-builder",
  system_prompt: "You are a Bridge-Builder agent...",  // full persona encoding
  retrieval_filter: {
    node_types: ["concept", "method"],
    connection_types: ["analogical", "generative"],
    min_resonance: 0.65
  },
  output_schema: {
    type: "n_star_candidate",
    required: ["source_node_A", "source_node_B", "collision_type", "structural_feature", "bridge_label", "provenance"]
  }
}
```

API calls are structured as JSON with the node subgraph context included in the user message. Responses are parsed into the n* schema and spawned via `spawnSphere()` in the NXS+ entity system.

---

## References

- Renn, O. (2021). Transdisciplinarity: Synthesis towards a modular approach. *Futures*, 130, 102744.
- Lin, Y.-C. et al. (2025). Creativity in LLM-based multi-agent systems: A survey. EMNLP 2025.
- Ghafarollahi, A. & Buehler, M. J. (2025). SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning. *Advanced Materials*.

---

*See also: [`COLLISION_TYPES.md`](COLLISION_TYPES.md) · [`EVALUATION_RUBRIC.md`](EVALUATION_RUBRIC.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)*
