# Collision Type Taxonomy

The collision engine stages structured encounters between heterogeneous epistemic positions. Six collision types are specified, each producing a structurally different class of bridge-concept (n*).

This taxonomy fills a gap in current AI literature: coordination and synthesis are well-supported; a richer collision grammar for cultural AI remains open terrain.

---

## Overview

| Type | Core Condition | Example Domain Pair | n* Class |
|---|---|---|---|
| **Analogy** | Shared structural role, different semantic domains | Architecture ↔ Cell Biology | Structural homologue |
| **Contradiction** | Direct negation of core proposition | Classical Design ↔ Buddhist Philosophy | Dialectical synthesis |
| **Grafting** | Morphism absent in B but observable effects resonate | Architecture ↔ Music Theory | Transferred mechanism |
| **Scale Shift** | Same concept at radically different scales | City Planning ↔ Textile Fibre | Scalar invariant |
| **Ontological Mismatch** | Cannot share parent class; metaphysical conflict | Whitehead Process ↔ Computational Process | Hybrid ontology |
| **Method Transfer** | Analytical procedure from A applied to B's objects | Film Analysis ↔ Urban Design | Methodological import |

---

## Type 1: Analogy

**Definition**: Two nodes share a structural role within their respective graphs despite operating in different semantic domains.

**Formal condition**:
- Resonance ρ(nᴬᵢ, nᴮⱼ) > θ₁ (high similarity)
- Structural divergence δ(Nᵢ, Nⱼ) < θ₂ (similar graph neighbourhood)

**Example**:
- Node A: `threshold` (architecture) — a surface mediating transition between inside and outside
- Node B: `membrane` (cell biology) — a surface mediating selective passage between cytoplasm and environment
- n*: A concept of **bounded permeability** applicable to both spatial and biological boundary design

**Agent lead**: Bridge-builder, Methodologist

**Typical output**: New design principle, transferable structural pattern, cross-domain teaching analogy

---

## Type 2: Contradiction

**Definition**: Two nodes directly negate each other's core proposition across disciplines; productive when each negation is disciplinarily grounded rather than superficial.

**Formal condition**:
- Semantic polarity < −θ₃
- High semantic proximity with inverted valence

**Example**:
- Node A: `permanence` (classical design) — value placed on durability, endurance, timeless form
- Node B: `impermanence` (Buddhist philosophy/wabi-sabi) — value placed on transience, decay, the beauty of change
- n*: A design philosophy of **designed ephemerality** — objects intentionally engineered to age, decay, or transform as part of their value

**Agent lead**: Sceptic, Aesthetic Critic, Educator

**Typical output**: Dialectical synthesis, philosophical proposition, studio brief exploring productive opposites

---

## Type 3: Grafting

**Definition**: A morphism type (relation, causal chain, procedure) present in discipline A's neighbourhood of a concept is absent in discipline B's equivalent, but the *effects* of that morphism are observable in B.

**Formal condition**:
- Morphism f ∈ Cᴬ has no pre-image in Cᴮ at the interface
- But f's target is resonant with a Cᴮ node

**Example**:
- In architecture: the causal chain `light → shadow → mood → spatial affect` is well-formalised
- In music theory: `tone colour` resonates with `mood`, but the intermediate `shadow` morphism has no equivalent
- n*: A concept of **tonal shadow** — the way harmonic darkening in music functions analogously to shadow in spatial affect

**Agent lead**: Formaliser, Bridge-builder

**Typical output**: New explanatory concept, missing link in a theoretical chain, candidate for formal modelling

---

## Type 4: Scale Shift

**Definition**: The same concept operates at a radically different scale in each discipline, creating a productive size-gap that generates insight when bridged.

**Formal condition**:
- ρ > θ₁ (high resonance)
- Scale parameter of nᴬᵢ and nᴮⱼ differ by > k orders of magnitude

**Example**:
- Node A: `pattern` at city-planning scale — street grid, neighbourhood morphology, urban typology
- Node B: `pattern` at textile-fibre scale — weave structure, fibre alignment, surface texture
- n*: A multi-scalar pattern language that explicitly links urban morphology to material organisation — enabling cross-scale design thinking from the fibre to the city block

**Agent lead**: Historian, Cartographer, Methodologist

**Typical output**: Multi-scalar framework, cross-resolution design methodology, curatorial theme spanning micro and macro

---

## Type 5: Ontological Mismatch

**Definition**: Two nodes cannot share a common ontological parent class despite high semantic similarity; their underlying metaphysical commitments differ fundamentally.

**Formal condition**:
- No common parent class in either ontology
- Classification conflict in the hybrid KG

**Example**:
- Node A: `process` (Whitehead's process philosophy) — a temporal event, an occasion of experience, irreducibly dynamic
- Node B: `process` (computer science) — a computational procedure, a sequence of discrete operations, executable and repeatable
- n*: A concept of **experiential computation** — asking what it would mean to design software processes that are genuinely event-like rather than procedural, or to model Whiteheadian occasions formally

**Agent lead**: Formaliser, Sceptic, Historian

**Typical output**: Hybrid ontology class, philosophical-technical proposition, research question for formal modelling

---

## Type 6: Method Transfer

**Definition**: An analytical or making procedure from discipline A is applied to the objects or questions of discipline B, revealing new structure in B's material.

**Formal condition**:
- Method mᴬ ∈ Cᴬ is defined on object class Oᴬ
- Discipline B contains objects Oᴮ structurally similar to Oᴬ
- Applying mᴬ to Oᴮ yields non-trivial results

**Example**:
- Method A: `close reading` (literary studies) — slow, attention to detail, interpretive, sensitive to ambiguity
- Object B: urban façade (architecture) — a surface typically analysed through proportion, material, function
- n*: A method of **architectural close reading** — applying literary interpretive attention to built surfaces, treating façades as texts with grammar, register, and rhetorical strategy

**Agent lead**: Methodologist, Educator, Curator

**Typical output**: New research method, studio exercise, curatorial practice, cross-disciplinary analytical tool

---

## Collision Protocol

Each collision event follows a structured protocol:

1. **Interface detection** — Scout agent identifies high-Φ node pairs above resonance threshold θ₁
2. **Collision type assignment** — Formaliser + Sceptic classify the pair into one of the six types
3. **Agent society activation** — Relevant role-agents are activated for that collision type (see [`AGENT_ROLES.md`](AGENT_ROLES.md))
4. **Structural gap diagnosis** — Collider agent identifies the structural gap requiring n*
5. **n* generation** — Synthesiser agent generates candidate bridge-concept with provenance
6. **Human review** — Expert review classifies n* before it enters the evaluated corpus

---

## Preventing Superficial Collisions

The Sceptic agent applies three anti-trivialisation checks:

- **Proximity without structure**: Are the two nodes actually from distinct disciplinary regimes (δ > 0.40), or merely different vocabulary for the same concept?
- **Thematic association**: Does the proposed n* identify a genuine structural connection, or merely a shared keyword?
- **Irreducibility test**: Can n* be derived from either source category alone? If yes, it is not a genuine bridge-concept.

---

*See also: [`AGENT_ROLES.md`](AGENT_ROLES.md) · [`EVALUATION_RUBRIC.md`](EVALUATION_RUBRIC.md) · [`DATA_MODEL.md`](DATA_MODEL.md)*
