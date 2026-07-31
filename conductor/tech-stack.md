# Tech stack

- Python 3.11 or later with setuptools, Ruff, mypy, and unittest.
- Stable Rust workspace with rustfmt, Clippy, and Cargo tests.
- RDF, JSON-LD, and SHACL artifacts aligned to pinned UOGTO semantics.
- GitHub Actions for hosted Python and Rust validation.
- Repository-local Conductor records for plans, evidence, and external gates.

Dependencies and capability ownership are governed by `ecosystem.lock.toml` and
`DEPENDENCY_MIGRATION_PLAN.md`.
