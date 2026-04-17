# Contributing to NXS+ Sphere Network

Thank you for your interest in contributing to the NXS+ Sphere Network. This project is part of an active research practice at the School of Culture & Creativity, BNBU. Contributions are welcome from collaborators, researchers, and developers.

---

## Ways to Contribute

- **Bug reports** — something broken in the browser app or Whisper server
- **Feature requests** — new functionality aligned with the Observatory roadmap
- **Documentation** — improvements to specs, guides, or examples
- **Vault examples** — well-annotated example vaults for new disciplines
- **Research feedback** — if you use NXS+ in a research or teaching context

---

## Bug Reports

Use the [Bug Report issue template](.github/ISSUE_TEMPLATE/bug_report.md).

Please include:
- Browser and version (NXS+ runs client-side; browser matters)
- Steps to reproduce
- Expected vs. actual behaviour
- Console errors if any (open DevTools → Console)
- Your vault file if the bug is data-specific (remove personal content first)

---

## Feature Requests

Use the [Feature Request issue template](.github/ISSUE_TEMPLATE/feature_request.md).

Before opening a request, check:
- The [`docs/ROADMAP.md`](../docs/ROADMAP.md) — your feature may already be planned
- Open issues — someone may have already requested it

Feature requests that align with the Observatory roadmap (multi-vault, agent society, collision engine, evaluation dashboard) are prioritised.

---

## Pull Requests

### Before submitting

1. Open an issue first for anything beyond small fixes
2. Discuss the approach in the issue before writing code
3. Keep PRs focused — one concern per PR

### Code style

The core application is a **single HTML file** (`src/nxs-plus.html`) with embedded CSS and JavaScript. This is intentional: zero-dependency, browser-run-anywhere.

- **No build tools**: do not introduce webpack, rollup, or any bundler
- **No npm dependencies** for the core app (Three.js is loaded via ES module import from CDN)
- **Vanilla JS**: no frameworks in the core app
- External libraries for the Whisper server (Python) follow standard conventions

### Testing

- Test in Chrome, Firefox, and Safari before submitting
- Test vault save/load round-trip (save → reload → verify all node data intact)
- Test Obsidian export if you've touched the serialisation layer

---

## Vault Contributions

If you want to contribute an annotated example vault for a new discipline:

1. Create a vault in NXS+ with at least 10 annotated nodes
2. Ensure all nodes have `words[]`, `notes`, and correct `type` and `meta.discipline` fields
3. Remove any personal or sensitive content
4. Save as `examples/{discipline-slug}-demo.json`
5. Open a PR with a brief description of the discipline and the concepts covered

---

## Research Use

If you use NXS+ in a research or teaching context, we'd love to hear about it. Open a Discussion or email the PI directly. Publications using the BNBU Centre's GPU resources should acknowledge the **BNBU Centre for Computational Culture and Heritage | NVIDIA DLI**.

---

## Code of Conduct

Be respectful, constructive, and patient. This is a research project — ideas are provisional, experiments fail, and iteration is the method.

---

*Questions? Open a Discussion or contact: Dr. Iannis Bardakos · School of Culture & Creativity, BNBU*
