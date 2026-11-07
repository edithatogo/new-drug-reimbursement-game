# Tech stack

- Python 3.11 or later with setuptools, Ruff, `ty` for routine type checking,
  basedpyright before pull requests, and unittest.
- Rust application workspace with immutable Paignia Git dependencies, rustfmt,
  Clippy and Cargo tests. Local integration is checked with Rust 1.75; hosted
  application CI retains its stable profile.
- RDF, JSON-LD, and SHACL artifacts aligned to pinned UOGTO semantics.
- GitHub Actions for hosted Python and Rust validation.
- Repository-local Conductor records for plans, evidence, and external gates.

Dependencies and capability ownership are governed by `ecosystem.lock.toml` and
`DEPENDENCY_MIGRATION_PLAN.md`.
