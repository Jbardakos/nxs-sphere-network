# Bridge-Concept Evaluation Rubric

Each second-order novel object (n*) produced by the collision engine is assessed on **six criteria**. The rubric is designed to replace benchmark accuracy with **cultural usefulness** as the primary evaluation standard.

> *Current creative MAS and cultural KG work support the move toward richer evaluation criteria, but no standard rubric for transdisciplinary creative AI exists. This rubric represents a methodological contribution of the project.*

---

## Rubric Table

| Criterion | Definition | Measurement Method | Threshold |
|---|---|---|---|
| **Traceability** | Every element of n* can be traced to specific source nodes and morphisms | Provenance graph; all parent nodes and bridge morphisms logged | 100% of n* content traceable |
| **Disciplinary Distance** | The two source nodes belong to genuinely distinct disciplinary regimes | Graph edit distance between neighbourhood subgraphs; semantic embedding distance | δ > 0.40; disciplines from different SCC divisions |
| **Conceptual Coherence** | n* forms an internally consistent concept, not a contradictory collage | Expert review (2 domain specialists); internal consistency check against hybrid ontology | Both reviewers assign ≥ 3/5 |
| **Categorical Novelty** | n* is not expressible as a composition of morphisms from either source category alone | Irreducibility test: attempt to derive n* from Cᴬ alone, then Cᴮ alone | Derivation fails in both attempts |
| **Pedagogical Value** | n* generates a usable teaching proposition, course module, or studio brief | SCC faculty panel assessment; student pilot test | ≥ 1 faculty member adopts within one semester |
| **Artistic Usefulness** | n* opens a productive direction for artistic research, exhibition, or practice | Villa Lab artistic research committee review | ≥ 1 practice-led project initiated within the academic year |

---

## Criterion 1: Traceability

**Why it matters**: LLM-generated bridge-concepts can appear plausible while being conceptually hollow or hallucinatory. Full provenance tracking is the primary safeguard against this failure mode.

**How it works**:
- Every word, claim, and structural feature in n* must link back to specific nodes and connection types in the source graphs
- The Archivist agent maintains the provenance log throughout the collision event
- The evaluation dashboard displays the provenance trace graph for each n*

**Scoring**:
- ✅ Pass: All elements traceable to source graph
- ❌ Fail: Any element without traceable source → n* is returned to generation for revision

---

## Criterion 2: Disciplinary Distance

**Why it matters**: A bridge-concept between two closely related sub-fields of the same discipline is not a genuine transdisciplinary contribution. The collision must cross a real epistemic boundary.

**How it works**:
- Graph edit distance computed between the neighbourhood subgraphs of the two source nodes
- Semantic embedding distance computed from the `words[]` arrays
- Both metrics must exceed threshold δ > 0.40

**Scoring** (0–5):
- 5 — Nodes from entirely different SCC divisions (e.g., architecture + music; design + philosophy)
- 4 — Different departments, clearly distinct methodological traditions
- 3 — Adjacent fields with shared vocabulary but distinct practices
- 2 — Closely related sub-fields; marginal distance
- 1 — Same field, different approach; not a genuine bridge
- 0 — Same concept restated in different terminology

**Threshold**: Score ≥ 3 required; score ≥ 4 preferred for flagship outputs.

---

## Criterion 3: Conceptual Coherence

**Why it matters**: A bridge-concept must be internally consistent. It should not merely juxtapose two incompatible frameworks but produce a concept that can stand on its own terms.

**How it works**:
- Two domain specialists (drawn from SCC faculty or visiting researchers) review the n* independently
- Each assigns a coherence score 1–5
- The n* is also checked for consistency against the hybrid ontology (where available)

**Scoring** (1–5 per reviewer):
- 5 — Fully coherent; could be published as a standalone concept
- 4 — Coherent with minor clarification needed
- 3 — Coherent in outline; requires further development
- 2 — Partially coherent; internal tensions remain unresolved
- 1 — Incoherent; contradictory collage

**Threshold**: Both reviewers ≥ 3/5.

---

## Criterion 4: Categorical Novelty

**Why it matters**: The bridge-concept must be genuinely new — not reducible to a concept already expressible within either source discipline alone. This is the formal test for whether a collision has produced something genuinely transdisciplinary.

**How it works**: The **Irreducibility Test**
1. Attempt to derive n* using only morphisms and concepts from Cᴬ (discipline A)
2. Attempt to derive n* using only morphisms and concepts from Cᴮ (discipline B)
3. If either derivation succeeds, n* is not novel — it is already expressible within an existing framework

**Scoring**:
- ✅ Pass: Derivation fails in both attempts
- ⚠️ Partial: n* is novel but closely approximated by an existing concept in one discipline → flag for revision
- ❌ Fail: n* is fully derivable from one source → not a genuine bridge-concept

---

## Criterion 5: Pedagogical Value

**Why it matters**: For SCC, the practical test of a bridge-concept is whether it can generate productive teaching. A concept that cannot be translated into a brief, a reading, or a studio prompt has limited institutional value regardless of its theoretical interest.

**How it works**:
- The Educator agent proposes at least one pedagogical application for each n*
- SCC faculty panel reviews the proposal (3 faculty members)
- Optional: student pilot test in a seminar or studio context within one semester

**Scoring** (qualitative):
- **Transformative** — Generates a new course module or cross-programme initiative
- **Fertile** — Multiple studio briefs or seminar readings possible
- **Plausible** — At least one clear pedagogical application
- **Underdeveloped** — Potential is unclear; needs further elaboration
- **Trivial** — No pedagogical application identified

**Threshold**: At least one faculty member adopts n* in course design within one semester from evaluation.

---

## Criterion 6: Artistic Usefulness

**Why it matters**: NXS+ is embedded in an artistic research practice context. Bridge-concepts must be evaluated for whether they open productive directions for practice-led research, not only for their theoretical or pedagogical interest.

**How it works**:
- The Aesthetic Critic and Curator agents propose at least one artistic research or exhibition direction for each n*
- Villa Lab artistic research committee reviews (PI + 2 committee members)
- Optional: practice-led project or exhibition proposal developed from n* within the academic year

**Scoring** (qualitative):
- **Transformative** — Generates a major exhibition or practice-research direction
- **Fertile** — Multiple practice-led projects possible
- **Plausible** — At least one clear artistic application
- **Underdeveloped** — Potential is unclear; needs further elaboration
- **Trivial** — No artistic application identified

**Threshold**: At least one practice-led project initiated from n* within the academic year.

---

## Output Classification

After applying the full rubric, each n* is assigned one of six classifications:

| Classification | Description |
|---|---|
| **Transformative** | Passes all criteria at highest level; major contribution |
| **Fertile** | Passes all criteria; generates multiple downstream applications |
| **Plausible** | Passes minimum thresholds on all criteria |
| **Underdeveloped** | Passes traceability and novelty but lacks clear application |
| **Misleading** | Appears plausible but fails coherence or irreducibility test |
| **Trivial** | Fails disciplinary distance or novelty; returned to collision for revision |

---

## Dashboard Format

Each evaluated n* is stored with its rubric scores in structured YAML on the node's `notes` field:

```yaml
evaluation:
  date: "2026-04-18"
  evaluators: ["Dr. A", "Dr. B"]
  traceability: true
  disciplinary_distance: 0.71
  conceptual_coherence:
    reviewer_1: 4
    reviewer_2: 4
  categorical_novelty: true
  pedagogical_value: "fertile"
  artistic_usefulness: "plausible"
  classification: "fertile"
  notes: "Strong structural analogy; clear studio brief potential; needs artistic development."
```

Scores are exportable to CSV from the evaluation dashboard.

---

## References

- Maree, M. (2025). Quantifying relational exploration in cultural heritage knowledge graphs with LLMs. *Data*, 10(4), 52.
- UNESCO (2025). Artificial Intelligence and Culture. Policy brief.
- Punjabi, M. et al. (2025). Knowledge integration in cross-disciplinary collaborations: A conceptual framework. Preprint.

---

*See also: [`COLLISION_TYPES.md`](COLLISION_TYPES.md) · [`AGENT_ROLES.md`](AGENT_ROLES.md) · [`DATA_MODEL.md`](DATA_MODEL.md)*
