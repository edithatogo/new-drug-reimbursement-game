# Tech stack

- CPython 3.15.2 from `.python-version`, with locked dependencies in
  `target/dev-python`. The checks use setuptools, pytest, Ruff, `ty` and
  basedpyright.
- Rust application workspace with immutable Paignia Git dependencies, rustfmt,
  Clippy and Cargo tests. Local integration is checked with Rust 1.75; hosted
  application CI retains its stable profile.
- RDF, JSON-LD, and SHACL artifacts aligned to pinned UOGTO semantics.
- GitHub Actions for hosted Python and Rust validation.
- Repository-local Conductor records for plans, evidence, and external gates.

Dependencies and capability ownership are governed by `ecosystem.lock.toml` and
`DEPENDENCY_MIGRATION_PLAN.md`.
